#!/usr/bin/env python3
"""核实并恢复 PP0072/PP0057 的本地五金；不访问外部库存。

默认只读生成计划。--apply 必须同时指定新的备份目录；所有数量须与
已关联的成功出库单一致，遇到额外或变化的数据即停止，不猜测业务事实。
"""
import argparse
from collections import Counter
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sqlite3

from traveler_assistant.database import ensure_schema
from traveler_assistant.hardware_facts import replace_factory_hardware, audit_factory_hardware, hardware_integrity_findings

ORDERS = ('PP0072', 'PP0057')


def records(connection, sql, parameters=()):
    cursor = connection.execute(sql, parameters)
    columns = [item[0] for item in cursor.description]
    return [dict(zip(columns, row)) for row in cursor.fetchall()]


def quantities(rows):
    result = Counter()
    for row in rows:
        result[str(row.get('product_code', row.get('productCode', ''))).upper()] += float(row['quantity'])
    return result


def plan_repair(connection, reference):
    factories = records(connection, "select * from factory_orders where order_id in (?,?) and aimes_status='active' order by factory_order", ORDERS)
    if Counter(row['order_id'] for row in factories) != Counter({'PP0072': 5, 'PP0057': 2}):
        raise ValueError('当前工厂单范围发生变化，停止恢复')
    plan = []
    for factory in factories:
        number = factory['factory_order']
        before = records(connection, 'select * from hardware_items where factory_order=? order by id', (number,))
        if factory['order_id'] == 'PP0072':
            desired = [row for row in before if row['source_type'] == 'aicnc' and row['source_path'].startswith('/Volumes/server/')]
            other = [row for row in before if row['source_type'] == 'aicnc' and not row['source_path'].startswith('/Volumes/server/')]
            if any('/server-test-fixtures/' not in row['source_path'] for row in other):
                raise ValueError(f'{number} 包含未确认的其他五金来源')
            if other and quantities(other) != quantities(desired):
                raise ValueError(f'{number} 测试来源与正式来源数量不同，不能自动清理')
        else:
            desired = [row for row in records(reference,
                "select * from hardware_items where factory_order=? and source_type='aicnc' order by id", (number,))
                if row.get('active', 1) == 1]  # Historical backups may still have the removed column.
            current_auto = [row for row in before if row['source_type'] == 'aicnc']
            if current_auto and quantities(current_auto) != quantities(desired):
                raise ValueError(f'{number} 当前自动五金已有其他变化，停止恢复')
        if not desired or any(not row.get('active', 1) for row in desired):
            raise ValueError(f'{number} 缺少已确认的有效来源')
        manual = [row for row in before if row['source_type'] != 'aicnc']
        documents = records(connection, """select d.*,f.created_at as factory_issued_at from outbound_documents d
            join outbound_document_factories f on f.document_number=d.document_number
            where f.factory_order=? and d.order_id=? and d.document_type='hardware' and d.status='已出库'""", (number, factory['order_id']))
        matching = [doc for doc in documents if quantities(json.loads(doc['items_json'])) == quantities(desired + manual)]
        if len(matching) != 1:
            raise ValueError(f'{number} 修复后五金无法唯一对应已确认出库单')
        doc = matching[0]
        completed_at = factory['outbound_completed_at'] or doc['factory_issued_at'] or doc['issued_at']
        if not completed_at:
            raise ValueError(f'{number} 没有历史业务时间')
        plan.append({'factory_order': number, 'order_id': factory['order_id'], 'before': before, 'after_auto': desired,
            'manual_preserved': manual, 'document_number': doc['document_number'], 'outbound_completed_at': completed_at})
    return plan


def digest_documents(connection):
    tables = ['outbound_documents', 'outbound_document_factories']
    return hashlib.sha256(json.dumps({table: records(connection, 'select * from '+table+' order by id') for table in tables}, sort_keys=True).encode()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database', type=Path, default=Path('data/workflow.sqlite3'))
    parser.add_argument('--reference', type=Path, default=Path('data/database-backups/workflow-2026-08-30.sqlite3'))
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--backup-dir', type=Path)
    args = parser.parse_args()
    reference = sqlite3.connect(args.reference.resolve().as_uri() + '?mode=ro', uri=True)
    source = sqlite3.connect(args.database.resolve().as_uri() + '?mode=ro', uri=True)
    plan = plan_repair(source, reference)
    before_digest = digest_documents(source)
    summary = [{'factory_order': row['factory_order'], 'before_count': len(row['before']),
        'after_count': len(row['after_auto'])+len(row['manual_preserved']), 'document': row['document_number']} for row in plan]
    if not args.apply:
        print(json.dumps({'apply': False, 'plan': summary, 'integrity_findings': hardware_integrity_findings(source)}, ensure_ascii=False, indent=2))
        return
    if args.backup_dir is None:
        raise ValueError('--apply 必须指定 --backup-dir')
    args.backup_dir.mkdir(parents=True, exist_ok=False)
    backup = sqlite3.connect(args.backup_dir / 'workflow.sqlite3')
    source.backup(backup)
    backup.close()
    source.close()
    ensure_schema(args.database)
    connection = sqlite3.connect(args.database)
    try:
        connection.execute('begin immediate')
        if digest_documents(connection) != before_digest or plan_repair(connection, reference) != plan:
            raise ValueError('预检后数据库发生变化，停止恢复')
        now = datetime.now().astimezone().isoformat(timespec='seconds')
        for row in plan:
            replace_factory_hardware(connection, row['factory_order'], row['after_auto'], observed_at=now,
                reason='经用户确认恢复 PP0072/PP0057 历史五金；逐工厂单与原出库单核对')
            connection.execute("""update factory_orders set outbound_status='已出库',outbound_document=?,
                outbound_mode='inventory',outbound_fingerprint='',outbound_completed_at=?,updated_at=? where factory_order=?""",
                (row['document_number'], row['outbound_completed_at'], now, row['factory_order']))
            audit_factory_hardware(connection, row['factory_order'], now)
        for order in ORDERS:
            connection.execute("update orders set stage='已出货',updated_at=? where order_id=?", (now,order))
            connection.execute("insert into sync_changes(observed_at,severity,kind,order_id,message) values(?,'info','hardware_history_repaired',?,?)",
                (now,order,'已核对原出库单，恢复五金与出货进度；未操作外部库存。'))
        assert digest_documents(connection) == before_digest
        assert connection.execute('pragma integrity_check').fetchone()[0] == 'ok'
        after = records(connection,"select factory_order,order_id,outbound_status,outbound_document,outbound_completed_at from factory_orders where order_id in (?,?) order by factory_order",ORDERS)
        report = {'repaired_at': now, 'plan': plan, 'after': after, 'outbound_documents_sha256': before_digest,
            'remaining_integrity_findings': hardware_integrity_findings(connection)}
        (args.backup_dir/'repair-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2))
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
        reference.close()
    print(json.dumps({'apply': True, 'plan': summary, 'backup': str(args.backup_dir.resolve()), 'outbound_documents_unchanged': True},ensure_ascii=False,indent=2))


if __name__ == '__main__':
    main()
