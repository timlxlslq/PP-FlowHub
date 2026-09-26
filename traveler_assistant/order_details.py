"""组装桌面看板及后续网页接口使用的订单详情，入口会确保数据库结构可用。"""

from __future__ import annotations

import sqlite3
from pathlib import Path

from .core import Config
from .database import connect_database, ensure_schema


def order_detail(config: Config, order_id: str) -> dict:
    """汇总订单、安装安排、工厂单、材料、五金及出库记录等详情。

    参数：config 提供数据库配置；order_id 为查询订单号。读取前会确保所需表结构存在。
    """
    ensure_schema(config.workflow_database)
    connection = connect_database(config.workflow_database)
    connection.row_factory = sqlite3.Row
    try:
        connection.execute(
            """
            create table if not exists order_installation_days(
                order_id text not null,
                date_type text not null check(date_type in ('planned', 'actual')),
                install_date text not null,
                installer text not null default '',
                updated_at text not null,
                primary key(order_id, date_type, install_date)
            )
            """
        )
        order = connection.execute(
            "select * from orders where order_id=?", (order_id.upper(),)
        ).fetchone()
        installation_rows = connection.execute(
            """
            select date_type, install_date, installer
            from order_installation_days
            where order_id=?
            order by date_type, install_date
            """,
            (order_id.upper(),),
        ).fetchall()
        installation = {"planned": [], "actual": []}
        for row in installation_rows:
            installation[row[0]].append({"date": row[1], "installer": row[2]})
        factories = connection.execute(
            """
            select factory_order, factory_name, sales_order_name, split_time,
                   report_state, ownership_status, has_hardware, (stage in ('已优化','已生产','已出货')) as optimized,
                   (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document, outbound_mode,
                   outbound_fingerprint
            from factory_orders where order_id=? and aimes_status='active' order by factory_order
            """, (order_id.upper(),)
        ).fetchall()
        materials = connection.execute(
            """
            select m.product_code,
                   p.material_kind as material_type,
                   p.material_color as color,
                   p.material_thickness as thickness,
                   m.quantity, p.unit,
                   case when p.material_kind='edge' then p.material_color else '' end as edge,
                   m.source_type, m.source_path, m.updated_at,
                   p.brand, p.name as product_name, p.spec as product_spec,
                   p.catalog_present, p.status as product_status
            from material_items m
            join products p on p.code=m.product_code
            where m.order_id=?
            order by p.material_kind, p.material_color, p.material_thickness, m.product_code
            """, (order_id.upper(),)
        ).fetchall()
        material_records = [dict(row) for row in materials]
        hardware_rows = connection.execute(
            """select h.factory_order, h.scope, h.product_code, p.name, p.spec, h.quantity,
                      p.unit, h.source_type, h.remarks, h.updated_at
               from hardware_items h join products p on p.code=h.product_code
               where h.order_id=? and exists (
                   select 1 from factory_orders f where f.factory_order=h.factory_order
                     and f.order_id=h.order_id and f.aimes_status='active'
               ) order by h.factory_order,h.product_code,h.id""", (order_id.upper(),)
        ).fetchall()
        hardware = [{**dict(row), "display_name": row["name"]} for row in hardware_rows]
        outbound = connection.execute(
            """
            select od.document_number, od.document_type,
                   coalesce(
                       (
                           select group_concat(linked.factory_order, ',')
                           from outbound_document_factories linked
                           where linked.document_number = od.document_number
                           order by linked.factory_order
                       ),
                       od.factory_order
                   ) as factory_order,
                   od.status, od.source, od.issued_at, od.source_path, od.updated_at
            from outbound_documents od
            where od.order_id=? order by od.issued_at desc, od.document_number
            """, (order_id.upper(),)
        ).fetchall()
        issues = connection.execute(
            """
            select issue_key, kind, factory_order, path, message, status, last_seen
            from pending_issues where order_id=? and status='open' order by last_seen desc
            """, (order_id.upper(),)
        ).fetchall()
        return {
            "order": dict(order) if order else {"order_id": order_id.upper()},
            "installation": installation,
            "factory_orders": [dict(row) for row in factories],
            "materials": material_records,
            "hardware": hardware,
            "outbound_documents": [dict(row) for row in outbound],
            "issues": [dict(row) for row in issues],
        }
    finally:
        connection.close()
