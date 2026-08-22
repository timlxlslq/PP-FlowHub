"""Read-only order detail projections for the desktop dashboard and future web API."""

from __future__ import annotations

import sqlite3
import re
from pathlib import Path

from .core import Config, _normalize_name
from .database import ensure_schema
from .inventory import InventoryMappings, ignored_hardware_reason


def _panel_products_by_name(connection: sqlite3.Connection) -> dict[str, list[dict[str, str]]]:
    """Return active Panel catalog rows grouped by their canonical name.

    Material facts intentionally keep the business color and thickness only.
    The product catalog supplies the presentation-only SKU, brand and image key.
    """
    table = connection.execute(
        "select 1 from sqlite_master where type='table' and name='products'"
    ).fetchone()
    if table is None:
        return {}
    columns = {str(row[1]) for row in connection.execute("pragma table_info(products)").fetchall()}
    if "brand" not in columns:
        return {}
    rows = connection.execute(
        """
        select code, name, brand, spec, status
        from products
        where normalized_category = ?
        order by code
        """,
        (_normalize_name("Panel"),),
    ).fetchall()
    grouped: dict[str, list[dict[str, str]]] = {}
    for row in rows:
        if row[4] not in ("", "启用"):
            continue
        grouped.setdefault(_normalize_name(row[1]), []).append({
            "code": str(row[0] or ""),
            "name": str(row[1] or ""),
            "brand": str(row[2] or ""),
            "spec": str(row[3] or ""),
        })
    return grouped


def _panel_product_for_color(
    products: dict[str, list[dict[str, str]]], color: str
) -> dict[str, str]:
    """Choose one color-level image identity, independent of thickness."""
    candidates = list(products.get(_normalize_name(color), []))
    if not candidates:
        return {"product_code": "", "brand": ""}

    def rank(item: dict[str, str]) -> tuple[int, str]:
        numbers = re.findall(r"\d+(?:\.\d+)?", item["spec"])
        thickness = float(numbers[0]) if numbers else 0.0
        # Prefer the standard 19.1mm product as the canonical color image.
        return (0 if abs(thickness - 19.1) < 0.6 else 1, item["code"])

    selected = sorted(candidates, key=rank)[0]
    return {"product_code": selected["code"], "brand": selected["brand"]}


def order_detail(config: Config, order_id: str) -> dict:
    ensure_schema(config.workflow_database)
    connection = sqlite3.connect(config.workflow_database)
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
                   report_state, ownership_status, has_hardware, optimized,
                   outbound_status, outbound_document, outbound_mode,
                   outbound_fingerprint, production_batch_id
            from factory_orders where order_id=? and aimes_status='active' order by factory_order
            """, (order_id.upper(),)
        ).fetchall()
        materials = connection.execute(
            """
            select material_type, color, thickness,
                   quantity, unit, edge, source_type, source_path, updated_at
            from material_items where order_id=? order by material_type, color, thickness
            """, (order_id.upper(),)
        ).fetchall()
        panel_products = _panel_products_by_name(connection)
        material_records = []
        for row in materials:
            record = dict(row)
            if record.get("material_type") == "panel":
                record.update(_panel_product_for_color(panel_products, record.get("color", "")))
            else:
                record.update({"product_code": "", "brand": ""})
            material_records.append(record)
        hardware_rows = connection.execute(
            """
            select factory_order, scope, product_code, source_code, name, spec, quantity,
                   unit, source_type, active, remarks, updated_at
            from hardware_items
            where order_id=? and active=1
              and exists (
                  select 1 from factory_orders
                  where factory_orders.factory_order=hardware_items.factory_order
                    and factory_orders.order_id=hardware_items.order_id
                    and factory_orders.aimes_status='active'
              )
            order by factory_order, product_code, name
            """, (order_id.upper(),)
        ).fetchall()
        mappings = InventoryMappings(config.workflow_database)
        hardware = [
            row for row in hardware_rows
            if ignored_hardware_reason(mappings, row[4], row[2], row[3]) is None
        ]
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
            from active_issues where order_id=? and status='open' order by last_seen desc
            """, (order_id.upper(),)
        ).fetchall()
        return {
            "order": dict(order) if order else {"order_id": order_id.upper()},
            "installation": installation,
            "factory_orders": [dict(row) for row in factories],
            "materials": material_records,
            "hardware": [dict(row) for row in hardware],
            "outbound_documents": [dict(row) for row in outbound],
            "issues": [dict(row) for row in issues],
        }
    finally:
        connection.close()
