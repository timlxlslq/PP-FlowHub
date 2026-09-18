"""Order-scoped manual hardware editor; drafts commit in one SQLite transaction."""
from __future__ import annotations

import hashlib
import json
import math
import sqlite3
from datetime import datetime

from .core import Config, RuleError
from .database import connect_database
from .inventory import ProductDatabase, InventoryMappings, ignored_hardware_reason


def _snapshot(connection, order: str) -> dict:
    factories = [dict(row) for row in connection.execute(
        """select factory_order, factory_name, aimes_status, (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status
           from factory_orders where order_id=? order by factory_order""", (order,))]
    items = [dict(row) for row in connection.execute(
        """select h.id, h.factory_order, h.product_code, p.name, p.spec, h.quantity, p.unit, h.remarks, h.updated_at
           from hardware_items h join products p on p.code=h.product_code
           where h.order_id=? and h.source_type='manual'
           order by h.factory_order, h.id""", (order,))]
    version = hashlib.sha256(json.dumps([factories, items], ensure_ascii=False,
                                        sort_keys=True).encode()).hexdigest()
    for factory in factories:
        factory['editable'] = (factory['aimes_status'] == 'active'
                               and factory['outbound_status'] != '已出库')
    return {'order_id': order, 'factories': factories, 'items': items, 'version': version}


def list_manual_hardware(config: Config, order_id: str) -> dict:
    order = order_id.strip().upper()
    if not order:
        raise RuleError('invalid_arguments', '请选择订单')
    connection = connect_database(config.workflow_database)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute('begin')
        return _snapshot(connection, order)
    finally:
        connection.close()


def save_manual_hardware(config: Config, order_id: str, payload: dict, *, confirm_write=False) -> dict:
    if not confirm_write:
        raise RuleError('write_confirmation_required', '请点击保存更改后再写入人工五金')
    if not config.storage_prepared:
        raise RuleError('database_not_prepared', '中央数据库尚未准备完成')
    order = order_id.strip().upper()
    if not order or not isinstance(payload, dict):
        raise RuleError('invalid_arguments', '人工五金保存请求无效')
    additions, deletions = payload.get('additions'), payload.get('deletions')
    if (not isinstance(additions, list) or not isinstance(deletions, list)
            or not all(type(item) is int for item in deletions)
            or not all(isinstance(item, dict) for item in additions)):
        raise RuleError('invalid_arguments', '人工五金新增或删除列表无效')
    with ProductDatabase(config.workflow_database) as catalog:
        connection = catalog.connection
        connection.row_factory = sqlite3.Row
        try:
            connection.execute('begin immediate')
            snapshot = _snapshot(connection, order)
            if payload.get('version') != snapshot['version']:
                raise RuleError('manual_hardware_conflict', '人工五金或工厂单已变化，请重新载入后编辑')
            factories = {item['factory_order']: item for item in snapshot['factories']}
            records = {item['id']: item for item in snapshot['items']}

            def require_factory(factory):
                if factory not in factories:
                    raise RuleError('manual_hardware_factory_missing', '工厂单必须属于当前订单')
                if not factories[factory]['editable']:
                    raise RuleError('manual_hardware_factory_locked', '已出库或失效的工厂单不能修改人工五金')

            for item_id in deletions:
                if item_id not in records:
                    raise RuleError('manual_hardware_delete_scope', '只能删除本订单的人工五金')
                require_factory(records[item_id]['factory_order'])
            prepared = []
            mappings = InventoryMappings(config.workflow_database, connection=connection)
            for item in additions:
                factory = str(item.get('factory_order') or '').strip()
                require_factory(factory)
                raw_quantity = item.get('quantity')
                try:
                    quantity = float(raw_quantity)
                except (TypeError, ValueError):
                    quantity = float('nan')
                if (isinstance(raw_quantity, bool) or not math.isfinite(quantity)
                        or quantity <= 0 or not quantity.is_integer()):
                    raise RuleError('manual_hardware_quantity', '人工五金数量必须是正整数')
                product = catalog.require_code(str(item.get('product_code') or '').strip().upper())
                if ignored_hardware_reason(mappings, product.name, product.code) is not None:
                    raise RuleError('hardware_ignored', f'五金已被全局忽略：{product.name}')
                prepared.append((factory, product, int(quantity)))
            observed = datetime.now().astimezone().isoformat(timespec='microseconds')
            connection.executemany(
                'delete from hardware_items where id=?',
                [(item_id,) for item_id in set(deletions)])
            for factory, product, quantity in prepared:
                # Aggregate same-SKU draft additions, preserving existing source evidence.
                rows = connection.execute(
                    """select id, quantity from hardware_items where order_id=? and factory_order=?
                       and product_code=? and source_type='manual' order by id""",
                    (order, factory, product.code)).fetchall()
                if rows:
                    connection.execute('update hardware_items set quantity=?, updated_at=? where id=?',
                                       (sum(row['quantity'] for row in rows) + quantity, observed, rows[0]['id']))
                    connection.executemany('delete from hardware_items where id=?',
                                           [(row['id'],) for row in rows[1:]])
                else:
                    connection.execute(
                        """insert into hardware_items(order_id,factory_order,scope,product_code,
                           quantity,source_type,source_path,remarks,updated_at)
                           values(?,?,'factory_order',?,?,'manual','','',?)""",
                        (order, factory, product.code, quantity, observed))
            result = _snapshot(connection, order)
            connection.commit()
            return {**result, 'saved': True}
        except Exception:
            connection.rollback()
            raise
