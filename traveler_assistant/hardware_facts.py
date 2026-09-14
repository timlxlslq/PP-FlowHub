"""自动五金的原子替换、来源隔离和出库后差异审计。"""
from collections import Counter
from datetime import datetime
import hashlib
import json
import math
from pathlib import Path


# These Server report SKUs count individual runners; inventory counts pairs.
SERVER_PIECE_RAIL_SKUS = frozenset({"M1094", "M1095", "M1096", "M1097"})


def server_hardware_quantity(product_code, quantity, unit, *, factory_order='', name=''):
    """Convert raw Server counts once, before creating canonical hardware facts.

    Never call on database rows: existing H/L-Rail pair folding and manual
    hardware already use their own quantity basis and must remain untouched.
    """
    quantity = float(quantity or 0)
    if str(product_code).strip().upper() not in SERVER_PIECE_RAIL_SKUS:
        return {"quantity": quantity, "unit": unit}
    if not math.isfinite(quantity) or quantity < 0 or quantity % 2 != 0:
        from .core import RuleError
        raise RuleError(
            'server_rail_pair_quantity_invalid',
            f"工厂单 {factory_order} 的 {name}（SKU {product_code}）报表数量为 {quantity:g} 个，"
            "必须为非负偶数才能按一对换算；请核对报表后重新预览，暂未写入。",
            factory_order=factory_order, product_code=product_code,
            name=name, source_quantity=quantity,
        )
    return {"quantity": quantity / 2, "unit": "对"}


def assert_source_isolation(database, sources, *, test_mode=False):
    """测试来源只能写入独立数据库，不能污染正式业务库。"""
    production = Path.home() / 'Documents/pp-flowhub/data/workflow.sqlite3'
    if Path(database).resolve() != production.resolve():
        return
    for source in sources:
        parts = {part.casefold() for part in Path(str(source)).parts}
        if test_mode or parts.intersection({'server-test-fixtures', 'local-source', 'test-fixtures'}):
            from .core import RuleError
            raise RuleError('test_database_required', '测试来源不能写入正式数据库，请使用独立的测试 state-dir。')


def replace_factory_hardware(connection, factory_order, rows, *, source_path='', observed_at='', reason='Server 五金同步', allow_empty=False):
    """完整校验后按工厂单替换自动五金；调用方负责外层事务提交。"""
    factory_order = str(factory_order).strip().upper()
    rows = [dict(row) for row in rows]
    if not factory_order:
        raise ValueError('五金替换缺少工厂单号')
    if not rows and not allow_empty:
        return False
    columns = ('order_id', 'factory_order', 'scope', 'product_code', 'source_code', 'name', 'spec', 'quantity', 'unit', 'source_type', 'source_path', 'active', 'remarks', 'updated_at')
    now = observed_at or datetime.now().astimezone().isoformat(timespec='seconds')
    normalized = []
    for row in rows:
        if str(row.get('factory_order', factory_order)).strip().upper() != factory_order:
            raise ValueError('五金替换包含其他工厂单')
        if row.get('source_type', 'aicnc') != 'aicnc':
            raise ValueError('自动五金替换不能包含手工五金')
        quantity = float(row.get('quantity', 0))
        if not math.isfinite(quantity) or quantity < 0 or not row.get('order_id'):
            raise ValueError('五金替换包含无效数量或订单')
        normalized.append({**dict.fromkeys(columns, ''), **row, 'factory_order': factory_order,
            'scope': 'factory_order', 'source_type': 'aicnc', 'active': 1,
            'source_path': row.get('source_path') or str(source_path), 'quantity': quantity, 'updated_at': now})
    if len({str(row['order_id']).strip().upper() for row in normalized}) > 1:
        raise ValueError('同一工厂单的五金不能分属多个订单')
    database = next((row[2] for row in connection.execute('pragma database_list') if row[1] == 'main'), '')
    if database:
        assert_source_isolation(database, [row['source_path'] for row in normalized])
    cursor = connection.execute("select * from hardware_items where factory_order=? and source_type='aicnc' order by id", (factory_order,))
    names = [col[0] for col in cursor.description]
    before = [dict(zip(names, row)) for row in cursor.fetchall()]
    business = ('order_id', 'factory_order', 'product_code', 'source_code', 'name', 'spec', 'quantity', 'unit', 'active')
    signature = lambda items: Counter(tuple(row.get(key, '') for key in business) for row in items)
    version = connection.execute('select fingerprint from hardware_source_versions where factory_order=?', (factory_order,)).fetchone()
    fingerprint = hashlib.sha256(json.dumps(sorted(signature(normalized).elements()), ensure_ascii=False).encode()).hexdigest()
    if signature(before) == signature(normalized) and version and version[0] == fingerprint:
        return False
    # SAVEPOINT prevents a caught insertion error from committing an earlier deletion.
    if not connection.in_transaction:
        connection.execute('begin')
    connection.execute('savepoint replace_factory_hardware')
    try:
        connection.execute("delete from hardware_items where factory_order=? and source_type='aicnc'", (factory_order,))
        connection.executemany(f"insert into hardware_items({','.join(columns)}) values({','.join('?' for _ in columns)})", [tuple(row[col] for col in columns) for row in normalized])
        order_id = (normalized or before)[0]['order_id'] if normalized or before else ''
        connection.execute("""insert into hardware_source_versions(factory_order,order_id,fingerprint,source_paths_json,row_count,updated_at)
            values(?,?,?,?,?,?) on conflict(factory_order) do update set order_id=excluded.order_id,
            fingerprint=excluded.fingerprint,source_paths_json=excluded.source_paths_json,
            row_count=excluded.row_count,updated_at=excluded.updated_at""",
            (factory_order, order_id, fingerprint, json.dumps(sorted({row['source_path'] for row in normalized} or {str(source_path)})), len(normalized), now))
        message = json.dumps({'reason': reason, 'fingerprint': fingerprint, 'before': before, 'after': normalized}, ensure_ascii=False)
        connection.execute('insert into sync_changes(observed_at,severity,kind,order_id,factory_order,path,message) values(?,?,?,?,?,?,?)',
            (now, 'info', 'hardware_projection_replaced', order_id, factory_order, str(source_path), message))
        audit_factory_hardware(connection, factory_order, now)
        connection.execute('release replace_factory_hardware')
    except Exception:
        connection.execute('rollback to replace_factory_hardware')
        connection.execute('release replace_factory_hardware')
        raise
    return True


def audit_factory_hardware(connection, factory_order, now=None):
    """资料差异独立提示；不改变历史已出库事实。"""
    now = now or datetime.now().astimezone().isoformat(timespec='seconds')
    if not connection.execute("select 1 from sqlite_master where name='factory_orders'").fetchone():
        return
    factory = connection.execute('select order_id from factory_orders where factory_order=?', (factory_order,)).fetchone()
    if not factory:
        return
    documents = connection.execute("""select d.document_number,d.items_json from outbound_documents d
        join outbound_document_factories f on f.document_number=d.document_number
        where f.factory_order=? and d.document_type='hardware' and d.status='已出库'""", (factory_order,)).fetchall()
    if not documents:
        return
    current = Counter()
    for code, quantity in connection.execute('select product_code,quantity from hardware_items where factory_order=? and active=1', (factory_order,)):
        current[str(code).strip().upper()] += float(quantity)
    totals = []
    for number, content in documents:
        quantities = Counter()
        for row in json.loads(content or '[]'):
            quantities[str(row.get('productCode', row.get('product_code', ''))).strip().upper()] += float(row.get('quantity', 0))
        totals.append(quantities)
    key = 'outbound_hardware_difference:' + factory_order
    if current in totals:
        connection.execute("update active_issues set status='resolved',resolved_at=?,last_seen=? where issue_key=? and status='open'", (now, now, key))
        return
    message = '出库后五金资料与已确认出库单不一致，请核对资料；原出库事实保持有效。单据：' + '、'.join(row[0] for row in documents)
    connection.execute("""insert into active_issues(issue_key,kind,order_id,factory_order,path,message,status,first_seen,last_seen,resolved_at)
        values(?,?,?,?,?,?,'open',?,?,'') on conflict(issue_key) do update set
        message=excluded.message,status='open',last_seen=excluded.last_seen,resolved_at=''""",
        (key, 'outbound_hardware_difference', factory[0], factory_order, '', message, now, now))


def hardware_integrity_findings(connection):
    """只读检查跨路径重复投影及有报表索引却无自动五金的工厂单。"""
    findings = []
    has_versions = bool(connection.execute("select 1 from sqlite_master where name='hardware_source_versions'").fetchone())
    for factory, order in connection.execute("select factory_order,order_id from factory_orders where aimes_status='active'"):
        by_path = {}
        for path, code, source_code, name, spec, qty, unit in connection.execute("select source_path,product_code,source_code,name,spec,quantity,unit from hardware_items where factory_order=? and source_type='aicnc' and active=1", (factory,)):
            by_path.setdefault(path, []).append((code, source_code, name, spec, qty, unit))
        paths = list(by_path)
        repeated = any(Counter(by_path[a]) == Counter(by_path[b]) for i, a in enumerate(paths) for b in paths[i+1:])
        if repeated:
            findings.append({'factory_order': factory, 'order_id': order, 'message': '同一工厂单存在跨路径相同五金，请核对并保留唯一有效来源。'})
        elif not by_path:
            # CUT TO SIZE contracts intentionally do not import automatic hardware.
            if order.upper().startswith('CS'):
                continue
            complete_empty = has_versions and connection.execute('select 1 from hardware_source_versions where factory_order=? and row_count=0', (factory,)).fetchone()
            if complete_empty:
                continue
            indexed = any(factory in str(row[0]).split(',') for row in connection.execute("select factory_order from source_files where kind='fittings'"))
            if indexed:
                findings.append({'factory_order': factory, 'order_id': order, 'message': '存在五金报表索引，但没有有效自动五金；请核对是否全部忽略或资料缺失。'})
    return findings


def audit_hardware_integrity(connection):
    """把完整性检查保存到待处理中心，不自动猜测或修复业务数量。"""
    now = datetime.now().astimezone().isoformat(timespec='seconds')
    findings = hardware_integrity_findings(connection)
    keys = {'hardware_integrity:' + row['factory_order'] for row in findings}
    for key, in connection.execute("select issue_key from active_issues where kind='hardware_integrity' and status='open'").fetchall():
        if key not in keys:
            connection.execute("update active_issues set status='resolved',resolved_at=? where issue_key=?", (now, key))
    for row in findings:
        connection.execute("""insert into active_issues(issue_key,kind,order_id,factory_order,path,message,status,first_seen,last_seen,resolved_at)
            values(?,'hardware_integrity',?,?, '',?,'open',?,?,'') on conflict(issue_key) do update set
            message=excluded.message,status='open',last_seen=excluded.last_seen,resolved_at=''""",
            ('hardware_integrity:' + row['factory_order'], row['order_id'], row['factory_order'], row['message'], now, now))
    return findings


def preserve_confirmed_shipment(connection, factory_order):
    """预览中的旧状态不得覆盖已由库存单确认的工厂单出货事实。"""
    rows = connection.execute("""select d.document_number,coalesce(nullif(f.created_at,''),d.issued_at)
        from outbound_documents d join outbound_document_factories f on f.document_number=d.document_number
        join factory_orders fo on fo.factory_order=f.factory_order and fo.order_id=d.order_id
        where f.factory_order=? and d.document_type='hardware' and d.status='已出库'
        order by d.document_number""", (factory_order,)).fetchall()
    if not rows:
        return
    connection.execute("""update factory_orders set outbound_status='已出库',outbound_document=?,
        outbound_mode='inventory',outbound_completed_at=coalesce(nullif(outbound_completed_at,''),?)
        where factory_order=?""",
        ('、'.join(row[0] for row in rows), max(row[1] for row in rows), factory_order))
