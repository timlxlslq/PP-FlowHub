#!/usr/bin/env python3
"""恢复 2026-09-16 明确获批的 PP0072 六条材料数量。

默认只读校验。--apply 必须指定新的备份目录；强制执行演练、完整数据库备份、
事务检查和审计，不进行外部系统读写。
"""
import argparse
from datetime import datetime
import hashlib
import json
from pathlib import Path
import sqlite3

APPROVED = {'M0004': 22.0, 'M0003': 5.0, 'M0002': 9.0,
            'M0021': 18.0, 'M1134': 3.0, 'M0022': 320.0}
IDENTITIES = {'M0004': ('plywood', '', '18'), 'M0003': ('plywood', '', '14.5'),
              'M0002': ('plywood', '', '5.4'), 'M0021': ('panel', 'Rosales 3', '19.1'),
              'M1134': ('panel', 'Rosales 3', '8'), 'M0022': ('edge', 'Rosales 3', '')}


def normal_thickness(value):
    """把非空厚度转成无多余小数零的数字文本。

    参数：value：待转换的单元格值或厚度。
    """
    return format(float(value), 'g') if str(value).strip() else ''


def rows(c, sql, args=()):
    """执行参数化查询并返回字典记录列表。

    参数：c：待校验或写入的数据库连接；sql：待执行的 SQL 查询；args：查询占位符对应的参数值。
    """
    return [dict(r) for r in c.execute(sql, args)]


def connect(path):
    """打开数据库并启用字典行与外键检查。

    参数：path：待读取或写入的文件路径。
    """
    c = sqlite3.connect(path)
    c.row_factory = sqlite3.Row
    c.execute('pragma foreign_keys=on')
    return c


def validate(c, reference):
    """核对六条获批材料的身份、数量和生产消耗，生成可恢复记录。

    参数：c：待校验或写入的数据库连接；reference：只读历史备份连接。
    """
    if c.execute("select count(*) from material_items where order_id='PP0072'").fetchone()[0]:
        raise ValueError('PP0072 already has material facts; stop rather than overwrite')
    result = []
    for r in rows(reference, "select * from material_items where order_id='PP0072'"):
        identity = (r['material_type'], r['color'], normal_thickness(r['thickness']))
        codes = [code for code, expected in IDENTITIES.items() if expected == identity]
        if len(codes) != 1:
            raise ValueError(f'Unexpected backup material identity: {identity}')
        code = codes[0]
        if r['quantity'] != APPROVED[code] or r['source_type'] != 'aihouse':
            raise ValueError('Backup quantity/source differs from approval')
        p = c.execute('select * from products where code=?', (code,)).fetchone()
        if not p or (p['material_kind'], p['material_color'], normal_thickness(p['material_thickness'])) != identity:
            raise ValueError(f'Current product identity differs: {code}')
        result.append(dict(order_id='PP0072', product_code=code, quantity=r['quantity'],
                           source_type=r['source_type'], source_path=r['source_path'],
                           source_fingerprint='v2:' + hashlib.sha256(('\x1f'.join((r['source_fingerprint'], code))).encode()).hexdigest(),
                           updated_at=datetime.now().astimezone().isoformat(timespec='seconds')))
    if len(result) != 6 or {r['product_code']: r['quantity'] for r in result} != APPROVED:
        raise ValueError('Backup is not the complete approved six-row set')
    consumed = dict(c.execute("select product_code,sum(quantity) from manual_production_batch_materials m "
                             "join manual_production_batches b on b.batch_id=m.batch_id "
                             "where m.order_id='PP0072' and b.status='completed' group by product_code").fetchall())
    if consumed != APPROVED:
        raise ValueError('Production consumption changed; stop for review')
    return result


def protected_digest(c):
    """计算受保护业务数据摘要，排除本次允许恢复的 PP0072 材料。

    参数：c：待校验或写入的数据库连接。
    """
    tables = [r[0] for r in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'")]
    data = {}
    for table in tables:
        query = 'select * from "' + table.replace('"', '""') + '"'
        if table == 'material_items':
            query += " where order_id!='PP0072'"
        data[table] = sorted([list(r) for r in c.execute(query)], key=repr)
    return hashlib.sha256(json.dumps(data, sort_keys=True, default=str).encode()).hexdigest()


def restore(c, reference, expected_digest=None):
    """在事务中复核备份摘要并恢复获批材料，失败时回滚。

    参数：c：待校验或写入的数据库连接；reference：只读历史备份连接；expected_digest：备份时受保护数据摘要；为空时跳过预检比较。
    """
    c.execute('begin immediate')
    try:
        if expected_digest is not None and protected_digest(c) != expected_digest:
            raise ValueError('Database changed after backup; retry with fresh backup')
        material = validate(c, reference)
        before = protected_digest(c)
        c.executemany('insert into material_items(order_id,product_code,quantity,source_type,source_path,source_fingerprint,updated_at) '
                      'values(:order_id,:product_code,:quantity,:source_type,:source_path,:source_fingerprint,:updated_at)', material)
        assert protected_digest(c) == before, 'Unrelated data changed'
        assert c.execute('pragma integrity_check').fetchone()[0] == 'ok'
        assert not c.execute('pragma foreign_key_check').fetchall()
        c.commit()
        return {'restored': material, 'protected_tables_sha256': before, 'integrity': 'ok',
                'foreign_key_violations': [], 'remaining_by_sku': {code: 0 for code in APPROVED}}
    except BaseException:
        c.rollback()
        raise


def main():
    """解析恢复选项，完成只读预检；明确应用时先备份演练再恢复并写审计。

    参数：无；使用脚本配置和命令行选项。
    """
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--database', type=Path, default=Path('data/workflow.sqlite3'))
    p.add_argument('--reference', type=Path, default=Path('data/database-backups/workflow-20260831-pre-ui-bundle.sqlite3'))
    p.add_argument('--apply', action='store_true')
    p.add_argument('--backup-dir', type=Path)
    args = p.parse_args()
    reference = sqlite3.connect(args.reference.resolve().as_uri() + '?mode=ro', uri=True)
    reference.row_factory = sqlite3.Row
    source = sqlite3.connect(args.database.resolve().as_uri() + '?mode=ro', uri=True)
    source.row_factory = sqlite3.Row
    material = validate(source, reference)
    if not args.apply:
        print(json.dumps({'approved': material}, ensure_ascii=False, indent=2)); return
    if not args.backup_dir:
        p.error('--apply requires --backup-dir')
    args.backup_dir.mkdir(parents=True, exist_ok=False)
    with connect(args.backup_dir / 'workflow-before.sqlite3') as backup:
        source.backup(backup)
    rehearsal = connect(args.backup_dir / 'rehearsal.sqlite3')
    source.backup(rehearsal)
    rehearsal_result = restore(rehearsal, reference)
    rehearsal.close()
    c = connect(args.database)
    backup = connect(args.backup_dir / 'workflow-before.sqlite3')
    result = restore(c, reference, expected_digest=protected_digest(backup))
    result.update(timestamp=datetime.now().astimezone().isoformat(), reference=str(args.reference),
                  rehearsal=rehearsal_result, approval='User confirmed quantities and M1134 8mm; no outbound changes')
    (args.backup_dir / 'audit.json').write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
