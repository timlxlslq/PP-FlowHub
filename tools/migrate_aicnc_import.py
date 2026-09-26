#!/usr/bin/env python3
"""显式启用新版优化台账；默认只读输出旧监控范围，--apply 前须取得真实库结构批准。"""
import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from traveler_assistant.aicnc_import import migrate, enabled


def legacy_scope(connection):
    """按既有监控策略固定切换名单，不把以后新订单加入旧监控。"""
    folders = {row[0] for row in connection.execute(
        "select source_folder from orders where source_folder<>'' and server_scan_policy in ('active','watching')")}
    folders.update(row[0] for row in connection.execute(
        "select source_folder from temporary_orders where server_scan_policy in ('watching','manual_pending')"))
    result = []
    for folder in sorted(folders):
        files = {r[0]: dict(path=r[0],kind=r[1]) for r in connection.execute(
            'select path,kind from server_scan_xml_state where source_folder=?',(folder,))}
        for r in connection.execute('select path,kind from source_files where source_folder=? and kind<>\'folder\'',(folder,)):
            files.setdefault(r[0],dict(path=r[0],kind=r[1]))
        result.append(dict(path=folder,files=list(files.values())))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--database',type=Path,required=True)
    parser.add_argument('--apply',action='store_true')
    parser.add_argument('--backup-dir',type=Path)
    args=parser.parse_args()
    source=sqlite3.connect(args.database.resolve().as_uri()+'?mode=ro',uri=True)
    try:
        scope=legacy_scope(source)
        if not args.apply:
            print(json.dumps(dict(enabled=enabled(source),legacy=scope,
                added_tables=['aicnc_import_settings','aicnc_optimizations','aicnc_material_allocations','aicnc_legacy_watch']),ensure_ascii=False,indent=2))
            return
        if not args.backup_dir:
            parser.error('--apply 必须指定 --backup-dir；真实库迁移必须已获用户批准')
        args.backup_dir.mkdir(parents=True,exist_ok=True)
        backup=args.backup_dir/f'aicnc-before-{datetime.now():%Y%m%d-%H%M%S-%f}.sqlite3'
        with sqlite3.connect(backup) as target: source.backup(target)
    finally: source.close()
    connection=sqlite3.connect(args.database)
    try:
        connection.execute('pragma foreign_keys=on')
        migrate(connection,scope)
        if connection.execute('pragma integrity_check').fetchone()[0]!='ok' or connection.execute('pragma foreign_key_check').fetchall():
            raise RuntimeError('迁移后的完整性检查失败，请保留备份并停止发布')
        print(json.dumps(dict(ok=True,backup=str(backup),legacy_count=len(scope)),ensure_ascii=False))
    finally: connection.close()


if __name__=='__main__': main()
