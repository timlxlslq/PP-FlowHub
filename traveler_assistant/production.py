"""Manual production facts and order-level material consumption.

These tables deliberately do not reuse ``production_batches``.  That table is
the evidence imported from AIMES/CNC reports; this module records the user's
actual production and the material quantities consumed by that production.
"""

from __future__ import annotations

import json
import sqlite3
import uuid
from datetime import datetime
from typing import Iterable

from .core import Config, RuleError
from .database import ensure_schema


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _normal(value: object) -> str:
    return str(value or "").strip()


def material_key(row: dict) -> str:
    return "|".join(
        _normal(row.get(name))
        for name in ("material_type", "color", "thickness", "edge", "unit")
    )


def _material_row(row: sqlite3.Row | dict) -> dict:
    result = {name: _normal(row[name]) for name in ("material_type", "color", "thickness", "edge", "unit")}
    result["quantity"] = float(row["quantity"] or 0)
    result["key"] = material_key(result)
    return result


def _connect(config: Config) -> sqlite3.Connection:
    ensure_schema(config.workflow_database)
    connection = sqlite3.connect(config.workflow_database)
    connection.row_factory = sqlite3.Row
    return connection


def _selected_factory_rows(connection: sqlite3.Connection, order_id: str, factory_orders: Iterable[str]) -> list[sqlite3.Row]:
    selected = sorted({_normal(value).upper() for value in factory_orders if _normal(value)})
    if not selected:
        raise RuleError("production_selection", "生产必须至少选择一个工厂单")
    placeholders = ",".join("?" for _ in selected)
    rows = connection.execute(
        f"""select factory_order, factory_name, order_id, ownership_status, optimized, outbound_status
            from factory_orders
            where order_id=? and aimes_status='active' and factory_order in ({placeholders})
            order by factory_order""",
        [order_id, *selected],
    ).fetchall()
    found = {str(row["factory_order"]).upper() for row in rows}
    missing = sorted(set(selected) - found)
    if missing:
        raise RuleError("production_factory_unknown", "数据库中找不到所选工厂单：" + "、".join(missing), factory_orders=missing)
    return rows


def _consumed(connection: sqlite3.Connection, order_id: str) -> dict[str, float]:
    rows = connection.execute(
        """select material_type, color, thickness, edge, unit, coalesce(sum(quantity), 0) quantity
           from manual_production_batch_materials m
           join manual_production_batches b on b.batch_id=m.batch_id
           where m.order_id=? and b.status='completed'
           group by material_type, color, thickness, edge, unit""",
        (order_id,),
    ).fetchall()
    return {material_key(dict(row)): float(row["quantity"] or 0) for row in rows}


def production_preview(config: Config, order_id: str, factory_orders: Iterable[str]) -> dict:
    normalized = _normal(order_id).upper()
    connection = _connect(config)
    try:
        factories = _selected_factory_rows(connection, normalized, factory_orders)
        not_optimized = [row["factory_order"] for row in factories if not bool(row["optimized"])]
        if not_optimized:
            raise RuleError("production_not_optimized", "以下工厂单尚未优化，不能生产：" + "、".join(not_optimized), factory_orders=not_optimized)
        already_produced = [row["factory_order"] for row in factories if connection.execute(
            """select 1 from manual_production_batch_factories f
               join manual_production_batches b on b.batch_id=f.batch_id
               where f.order_id=? and f.factory_order=? and b.status='completed' limit 1""",
            (normalized, row["factory_order"]),
        ).fetchone()]
        if already_produced:
            raise RuleError("production_already_completed", "以下工厂单已经生产，不能重复生产：" + "、".join(already_produced), factory_orders=already_produced)
        materials = []
        consumed = _consumed(connection, normalized)
        for row in connection.execute(
            """select material_type, color, thickness, edge, unit, quantity
               from material_items where order_id=? order by material_type, color, thickness, edge""",
            (normalized,),
        ).fetchall():
            item = _material_row(row)
            item["total_quantity"] = item.pop("quantity")
            item["consumed_quantity"] = consumed.get(item["key"], 0.0)
            item["remaining_quantity"] = max(0.0, item["total_quantity"] - item["consumed_quantity"])
            materials.append(item)
        return {
            "ok": True,
            "order_id": normalized,
            "selected_factory_orders": [row["factory_order"] for row in factories],
            "factories": [
                {"factory_order": row["factory_order"], "factory_name": row["factory_name"], "production_status": "未生产", "optimized": bool(row["optimized"])}
                for row in factories
            ],
            "materials": materials,
            "production_time": _now(),
            "ready": True,
        }
    finally:
        connection.close()


def _decode_materials(value: object) -> list[dict]:
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise RuleError("production_materials", "生产材料数量不是有效 JSON") from exc
    if not isinstance(value, list):
        raise RuleError("production_materials", "生产材料数量必须是数组")
    return [item for item in value if isinstance(item, dict)]


def prepare_production(config: Config, order_id: str, factory_orders: Iterable[str], materials: object) -> dict:
    preview = production_preview(config, order_id, factory_orders)
    requested = {
        _normal(item.get("key")) or material_key(item): float(item.get("quantity", 0) or 0)
        for item in _decode_materials(materials)
    }
    available = {item["key"]: item for item in preview["materials"]}
    unknown = sorted(set(requested) - set(available))
    if unknown:
        raise RuleError("production_material_unknown", "生产选择包含订单中不存在的材料")
    positive_total = sum(item["remaining_quantity"] for item in preview["materials"])
    if positive_total > 0 and not any(quantity > 0 for quantity in requested.values()):
        raise RuleError("production_material_empty", "请至少选择一项本次实际消耗的板材或封边数量")
    for key, quantity in requested.items():
        remaining = available[key]["remaining_quantity"]
        if quantity < 0 or quantity > remaining + 1e-9:
            raise RuleError("production_material_quantity", f"材料 {key} 的生产数量超过剩余可用数量：{remaining:g}")
    now = _now()
    batch_number = f"MP-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    connection = _connect(config)
    try:
        cursor = connection.execute(
            """insert into manual_production_batches(batch_number, order_id, production_time, source, status, created_at, updated_at)
               values(?,?,?,?,?,?,?)""",
            (batch_number, preview["order_id"], now, "manual", "prepared", now, now),
        )
        batch_id = cursor.lastrowid
        for factory_order in preview["selected_factory_orders"]:
            connection.execute(
                "insert into manual_production_batch_factories(batch_id, order_id, factory_order) values(?,?,?)",
                (batch_id, preview["order_id"], factory_order),
            )
        for key, quantity in requested.items():
            if quantity <= 0:
                continue
            item = available[key]
            connection.execute(
                """insert into manual_production_batch_materials(batch_id, order_id, material_type, color, thickness, edge, unit, quantity)
                   values(?,?,?,?,?,?,?,?)""",
                (batch_id, preview["order_id"], item["material_type"], item["color"], item["thickness"], item["edge"], item["unit"], quantity),
            )
        connection.commit()
    finally:
        connection.close()
    return {**preview, "batch_number": batch_number, "production_time": now, "status": "prepared"}


def complete_production_batch(config: Config, batch_number: str) -> dict:
    connection = _connect(config)
    try:
        row = connection.execute("select * from manual_production_batches where batch_number=?", (_normal(batch_number),)).fetchone()
        if row is None:
            raise RuleError("production_batch_unknown", f"找不到生产批次：{batch_number}")
        if row["status"] == "prepared":
            connection.execute("update manual_production_batches set status='completed', updated_at=? where batch_id=?", (_now(), row["batch_id"]))
            connection.commit()
        factories = [r[0] for r in connection.execute("select factory_order from manual_production_batch_factories where batch_id=? order by factory_order", (row["batch_id"],)).fetchall()]
        return {"ok": True, "batch_number": row["batch_number"], "order_id": row["order_id"], "factory_orders": factories, "status": "completed"}
    finally:
        connection.close()


def migrate_legacy_production_state(config: Config) -> dict:
    """Infer production for legacy factory orders that already have outbound evidence."""
    connection = _connect(config)
    migrated = []
    try:
        rows = connection.execute(
            """select factory_order, order_id, outbound_status, outbound_document
               from factory_orders where aimes_status='active' and order_id<>''
                 and (outbound_status in ('已出库','需要更新') or trim(coalesce(outbound_document,''))<>'')"""
        ).fetchall()
        for row in rows:
            if row["outbound_status"] == "需要更新" and _normal(row["outbound_document"]):
                # Legacy status meant the old combined material+hardware
                # document differed from current order materials.  Under the
                # new model materials are no longer part of factory shipment;
                # the existing document is retained as historical hardware
                # shipment evidence and the factory is treated as shipped.
                connection.execute(
                    "update factory_orders set outbound_status='已出库', updated_at=? where factory_order=? and order_id=?",
                    (_now(), row["factory_order"], row["order_id"]),
                )
            exists = connection.execute(
                """select 1 from manual_production_batch_factories f join manual_production_batches b on b.batch_id=f.batch_id
                   where f.order_id=? and f.factory_order=? and b.status='completed' limit 1""",
                (row["order_id"], row["factory_order"]),
            ).fetchone()
            if exists:
                continue
            now = _now()
            batch_number = f"LEGACY-{row['factory_order']}-{uuid.uuid4().hex[:6].upper()}"
            cursor = connection.execute(
                """insert into manual_production_batches(batch_number, order_id, production_time, source, status, created_at, updated_at)
                   values(?,?,?,?,?,?,?)""",
                (batch_number, row["order_id"], "", "legacy-outbound-migration", "completed", now, now),
            )
            connection.execute(
                "insert into manual_production_batch_factories(batch_id, order_id, factory_order) values(?,?,?)",
                (cursor.lastrowid, row["order_id"], row["factory_order"]),
            )
            migrated.append(row["factory_order"])
        connection.commit()
        return {"ok": True, "migrated_factory_orders": migrated, "production_time_missing": migrated}
    finally:
        connection.close()


def assert_shipment_allowed(config: Config, order_id: str, factory_orders: Iterable[str]) -> None:
    normalized = _normal(order_id).upper()
    connection = _connect(config)
    try:
        rows = _selected_factory_rows(connection, normalized, factory_orders)
        blocked = []
        for row in rows:
            if row["outbound_status"] == "已出库":
                blocked.append(f"{row['factory_order']}（已经出货）")
                continue
            if not connection.execute(
                """select 1 from manual_production_batch_factories f join manual_production_batches b on b.batch_id=f.batch_id
                   where f.order_id=? and f.factory_order=? and b.status='completed' limit 1""",
                (normalized, row["factory_order"]),
            ).fetchone():
                blocked.append(f"{row['factory_order']}（尚未生产）")
        if blocked:
            raise RuleError("shipment_not_allowed", "以下工厂单不能出货：" + "、".join(blocked), factory_orders=[row["factory_order"] for row in rows])
    finally:
        connection.close()
