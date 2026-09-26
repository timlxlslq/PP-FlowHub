"""仅在确认业务写入时持久保存用户批准的五金来源。"""
import hashlib
import json
import sqlite3
from datetime import datetime
from pathlib import Path


def decision_revision(value):
    """计算来源决策 value 的稳定内容指纹；空值返回空字符串。"""
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True).encode()).hexdigest() if value else ''


def load_source_decisions(config):
    """读取已确认的五金来源；config 提供共享连接或数据库路径，独立打开时使用只读连接。"""
    connection = config.workflow_connection
    owns = connection is None
    if connection is None:
        if not config.workflow_database.is_file():
            return {}
        connection = sqlite3.connect(f'file:{config.workflow_database}?mode=ro', uri=True)
    try:
        if not connection.execute("select 1 from sqlite_master where name='hardware_source_decisions'").fetchone():
            return {}
        return {factory: json.loads(value) for factory, value in connection.execute(
            'select factory_order, decision_json from hardware_source_decisions')}
    finally:
        if owns:
            connection.close()


def commit_source_decisions(connection, payload, factories, skipped_orders):
    """校验预览基准后保存符合范围的来源决策，过期预览报错。

    参数：connection 为事务连接；payload 为确认预览；factories 为可写工厂单；skipped_orders 为跳过订单。
    """
    from .core import RuleError
    proposals = payload.get('hardware_source_decisions', {})
    bases = payload.get('hardware_source_decision_bases', {})
    eligible = {str(row.get('factory_order', '')).upper() for row in payload.get('write_records', {}).get('factory_orders', [])
                if str(row.get('order_id', '')).upper() not in skipped_orders} & set(factories)
    for factory in eligible:
        current = connection.execute('select decision_json from hardware_source_decisions where factory_order=?', (factory,)).fetchone()
        old = json.loads(current[0]) if current else None
        proposal = proposals.get(factory)
        if old and proposal is None:
            if payload.get('include_hardware', True):
                raise RuleError('hardware_source_stale', f'{factory} 已固定五金来源，请重新预览后确认')
            continue
        if proposal is None:
            continue
        if decision_revision(old) != bases.get(factory, '') and old != proposal:
            raise RuleError('hardware_source_stale', f'{factory} 的五金来源记录已更新，请重新预览')
        connection.execute('insert into hardware_source_decisions(factory_order, decision_json) values(?,?) '
                           'on conflict(factory_order) do update set decision_json=excluded.decision_json',
                           (factory, json.dumps(proposal, ensure_ascii=False, sort_keys=True)))


def with_source_decisions(function):
    """为同步或 Traveler 入口应用已确认的来源锁定；function 为被包装的入口函数。"""
    from functools import wraps
    @wraps(function)
    def run(config, *args, **kwargs):
        """复用或创建来源读取上下文；config 为配置，args、kwargs 原样传给入口。"""
        from .report_read_context import current_report_context, report_read_session
        if current_report_context() is not None:
            return function(config, *args, **kwargs)
        with report_read_session() as context:
            # 这些入口可能生成材料或 Traveler 文件；目录列表复用只用于只读 Server 预览。
            context.reuse_reports = False
            context.locked_decisions = load_source_decisions(config)
            return function(config, *args, **kwargs)
    return run


def preview_manual_handling(config, order_id, factory_order):
    """只读生成绑定当前事实及报表字节版本的人工处理预览。

    参数：config 为配置；order_id 为归属订单号；factory_order 为工厂单号。
    """
    from .core import RuleError
    order, factory = order_id.strip().upper(), factory_order.strip().upper()
    with sqlite3.connect(f'file:{config.workflow_database}?mode=ro', uri=True) as connection:
        owner = connection.execute('select order_id from factory_orders where factory_order=?', (factory,)).fetchone()
        if not owner or owner[0] != order:
            raise RuleError('hardware_owner_invalid', f'本地校验：订单 {order} / 工厂单 {factory} 归属不匹配')
        saved = connection.execute('select decision_json from hardware_source_decisions where factory_order=?', (factory,)).fetchone()
        decision = json.loads(saved[0]) if saved else None
        if not decision or not decision.get('selected'):
            raise RuleError('hardware_source_missing', f'本地校验：订单 {order} / 工厂单 {factory} 尚无已确认来源，请先完成 Server 预览')
        paths = {str(Path(decision['selected']['path']).resolve()): decision['selected']['path']}
        for path, factories in connection.execute("select path,factory_order from source_files where kind='fittings'"):
            if factory in str(factories).split(','):
                paths[str(Path(path).resolve())] = path
        revisions = {}
        for path in sorted(paths.values()):
            try:
                revisions[path] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
            except OSError as exc:
                raise RuleError('server_report_read', f'Server 报表读取失败：订单 {order} / 工厂单 {factory}；文件 {path}：{exc}',
                                source='Server 报表', order_id=order, factory_order=factory, path=path) from exc
        facts = connection.execute("select order_id,factory_order,product_code,quantity,source_path from hardware_items where factory_order=? and source_type='aicnc' order by id", (factory,)).fetchall()
        version = connection.execute('select * from hardware_source_versions where factory_order=?', (factory,)).fetchone()
        proposal = {'order_id': order, 'factory_order': factory, 'decision': decision,
                    'report_versions': revisions, 'automatic_rows': facts, 'version': version}
        return {**proposal, 'token': decision_revision(proposal)}


def confirm_manual_handling(config, order_id, factory_order, token):
    """原子确认自动五金改为人工处理，不声明已出货，也不删除人工五金行。

    参数：config 为配置；order_id 为订单号；factory_order 为工厂单号；token 为预览确认版本。
    """
    from .core import RuleError
    from .order_index import OrderIndexStore
    from .hardware_facts import replace_factory_hardware
    if not token:
        raise RuleError('confirmation_required', '本地校验：请先预览人工处理并提供确认版本')
    store = OrderIndexStore(config.workflow_database)
    try:
        store.connection.execute('begin immediate')
        proposal = preview_manual_handling(config, order_id, factory_order)
        if proposal['token'] != token:
            raise RuleError('hardware_source_stale', f'本地校验：订单 {order_id} / 工厂单 {factory_order} 的报表或本地事实已变化，请重新预览')
        decision = {**proposal['decision'], 'handling': 'manual', 'report_versions': proposal['report_versions']}
        factory = proposal['factory_order']
        replace_factory_hardware(store.connection, factory, [], allow_empty=True,
                                 source_path=decision['selected']['path'], reason='用户确认人工处理自动五金')
        store.connection.execute('insert into hardware_source_decisions(factory_order,decision_json) values(?,?) '
                                 'on conflict(factory_order) do update set decision_json=excluded.decision_json',
                                 (factory, json.dumps(decision, ensure_ascii=False, sort_keys=True)))
        store.connection.execute('update hardware_source_versions set order_id=? where factory_order=?',
                                 (proposal['order_id'], factory))
        # 索引指纹必须对应上面实际确认的文件版本。
        for path, fingerprint in proposal['report_versions'].items():
            indexed_path = path
            saved = store.connection.execute('select factory_order from source_files where path=?', (indexed_path,)).fetchone()
            factories = sorted(set(str(saved[0]).split(',')) | {factory}) if saved else [factory]
            folder = store.connection.execute('select source_folder from source_files where path=?', (indexed_path,)).fetchone()
            store.upsert_source_file(Path(indexed_path), source_folder=Path(folder[0]) if folder else Path(indexed_path).parent, kind='fittings',
                                     order_id=proposal['order_id'], factory_order=','.join(x for x in factories if x),
                                     changed_at=datetime.now().isoformat())
            if hashlib.sha256(Path(path).read_bytes()).hexdigest() != fingerprint:
                raise RuleError('hardware_source_stale', f'Server 报表在确认期间变化：{path}')
        store.resolve_active_issue('hardware_integrity:' + factory)
        store.commit()
        return {'ok': True, 'order_id': proposal['order_id'], 'factory_order': factory, 'handling': 'manual'}
    except Exception:
        store.connection.rollback()
        raise
    finally:
        store.close()
