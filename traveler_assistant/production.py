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


def _order_material_rows(connection: sqlite3.Connection, order_id: str) -> list[dict]:
    """Read one row per order-material identity, including duplicate sources."""
    rows = connection.execute(
        """select material_type, color, thickness, edge, unit, coalesce(sum(quantity), 0) quantity
           from material_items
           where order_id=?
           group by material_type, color, thickness, edge, unit
           order by material_type, color, thickness, edge, unit""",
        (order_id,),
    ).fetchall()
    return [_material_row(row) for row in rows]


def _inventory_name_key(value: object) -> str:
    return "".join(character for character in str(value or "").casefold() if character.isalnum())


def _material_display_name(item: dict) -> str:
    material_type = _normal(item.get("material_type")).casefold()
    color = _normal(item.get("color"))
    thickness = _normal(item.get("thickness"))
    if material_type in {"panel", "back"}:
        return f"{thickness}mm--{color}"
    if material_type == "edge":
        return f"Edge banding--{color}"
    if material_type == "plywood":
        return f"{thickness}mm--Plywood"
    return ""


def _historical_material_product_codes(
    connection: sqlite3.Connection,
    materials: list[dict],
) -> dict[str, str]:
    """Resolve current material facts to inventory SKUs for legacy documents.

    New production writes already store material quantities in
    ``manual_production_batch_materials``.  Older inventory documents only
    retain SKU/quantity in the audit JSON, so use the saved mapping first and
    the product catalog as a deterministic fallback.  Ambiguous products are
    deliberately ignored rather than guessed.
    """
    display_names = {
        _inventory_name_key(_material_display_name(item)): item["key"]
        for item in materials
        if _material_display_name(item)
    }
    code_by_material_key: dict[str, str] = {}
    if connection.execute(
        "select 1 from sqlite_master where type='table' and name='inventory_resolution_rules'"
    ).fetchone():
        for row in connection.execute(
            "select normalized_name, product_code from inventory_resolution_rules where rule_type='mapping'"
        ).fetchall():
            material_key_value = display_names.get(_inventory_name_key(row[0]))
            if material_key_value and row[1]:
                code_by_material_key[material_key_value] = str(row[1]).strip().upper()

    if not connection.execute(
        "select 1 from sqlite_master where type='table' and name='products'"
    ).fetchone():
        return code_by_material_key

    products = connection.execute(
        "select code, name, spec, category, status from products"
    ).fetchall()
    for item in materials:
        key = item["key"]
        if key in code_by_material_key:
            continue
        material_type = _normal(item.get("material_type")).casefold()
        color_key = _inventory_name_key(item.get("color"))
        thickness_key = _inventory_name_key(item.get("thickness"))
        candidates = []
        for product in products:
            if str(product[4] or "").strip() not in {"", "启用"}:
                continue
            category_key = _inventory_name_key(product[3])
            name_key = _inventory_name_key(product[1])
            spec_key = _inventory_name_key(product[2])
            if material_type == "edge":
                category_matches = "edge" in category_key or "封边" in category_key
            elif material_type == "plywood":
                category_matches = "plywood" in category_key or "夹板" in category_key
            else:
                category_matches = "panel" in category_key or "板" in category_key
            if not category_matches or (color_key and color_key not in name_key):
                continue
            if material_type != "edge" and thickness_key and thickness_key not in spec_key:
                continue
            candidates.append(str(product[0]).strip().upper())
        if len(set(candidates)) == 1:
            code_by_material_key[key] = candidates[0]
    return code_by_material_key


def _legacy_inventory_consumed(
    config: Config,
    connection: sqlite3.Connection,
    order_id: str,
) -> dict[str, float]:
    """Read material consumed by pre-transaction legacy production records.

    The legacy migration marked shipped factories as produced but had no
    material rows.  Their confirmed inventory documents are still reliable
    evidence, so use them only for those legacy batches.  Once a batch has
    explicit material rows, this path skips it and avoids double counting.
    """
    material_rows = []
    for item in _order_material_rows(connection, order_id):
        item["total_quantity"] = item.pop("quantity")
        material_rows.append(item)
    code_by_material_key = _historical_material_product_codes(connection, material_rows)
    material_key_by_code = {code: key for key, code in code_by_material_key.items()}
    if not material_key_by_code:
        return {}

    documents = connection.execute(
        """select document_number, document_type, status, factory_order, items_json
           from outbound_documents where order_id=?""",
        (order_id,),
    ).fetchall()
    consumed: dict[str, float] = {}
    for document in documents:
        document_number = str(document[0] or "").strip()
        try:
            items = json.loads(document[4] or "[]")
        except (TypeError, json.JSONDecodeError):
            items = []
        kind = str(document[1] or "").strip().casefold()
        if kind not in {"materials", "material", "板材", "材料"}:
            continue
        status = str(document[2] or "").strip()
        if status != "已出库":
            continue
        links = [
            str(row[0]).strip().upper()
            for row in connection.execute(
                "select factory_order from outbound_document_factories where document_number=? and order_id=?",
                (document_number, order_id),
            ).fetchall()
            if str(row[0]).strip()
        ]
        if not links and str(document[3] or "").strip().upper() != order_id:
            links = [str(document[3]).strip().upper()]
        if not links:
            continue
        legacy_factories = []
        for factory_order in set(links):
            legacy = connection.execute(
                """select b.batch_id
                   from manual_production_batch_factories f
                   join manual_production_batches b on b.batch_id=f.batch_id
                   where f.order_id=? and f.factory_order=?
                     and b.status='completed' and b.source='legacy-outbound-migration'
                     and not exists (
                         select 1 from manual_production_batch_materials m
                         where m.batch_id=b.batch_id
                     ) limit 1""",
                (order_id, factory_order),
            ).fetchone()
            if legacy:
                legacy_factories.append(factory_order)
        if not legacy_factories:
            continue
        for item in items:
            if not isinstance(item, dict):
                continue
            code = str(item.get("productCode", "")).strip().upper()
            material_key_value = material_key_by_code.get(code)
            if not material_key_value:
                continue
            try:
                quantity = float(item.get("quantity", 0) or 0)
            except (TypeError, ValueError):
                continue
            if quantity > 0:
                consumed[material_key_value] = consumed.get(material_key_value, 0.0) + quantity
    return consumed


def cumulative_production_materials(
    config: Config,
    order_id: str,
    current_materials: Iterable[dict],
) -> list[dict]:
    """Return the order-level cumulative material quantity for inventory.

    A production draft contains only the quantity consumed by the currently
    selected factories.  JDY, however, keeps one material outbound document
    per order.  Updating that document therefore requires completed manual
    batches, legacy confirmed consumption, and the current draft to be added
    together.  This helper is read-only; the current draft is still recorded
    separately after JDY confirms the save.
    """
    normalized = _normal(order_id).upper()
    connection = _connect(config)
    try:
        rows: list[dict] = []
        by_key: dict[str, dict] = {}
        for item in _order_material_rows(connection, normalized):
            item["total_quantity"] = item.pop("quantity")
            rows.append(item)
            by_key[item["key"]] = item

        cumulative = _consumed(connection, normalized)
        for key, quantity in _legacy_inventory_consumed(config, connection, normalized).items():
            cumulative[key] = cumulative.get(key, 0.0) + quantity

        for raw in current_materials:
            item = dict(raw)
            key = _normal(item.get("key")) or material_key(item)
            if key not in by_key:
                raise RuleError(
                    "production_material_unknown",
                    "生产材料包含订单中不存在的项目，已停止库存出库",
                )
            try:
                quantity = float(item.get("quantity", 0) or 0)
            except (TypeError, ValueError) as exc:
                raise RuleError("production_material_quantity", "生产材料数量无效") from exc
            if quantity < 0:
                raise RuleError("production_material_quantity", "生产材料数量不能小于 0")
            cumulative[key] = cumulative.get(key, 0.0) + quantity

        result = []
        for item in rows:
            quantity = cumulative.get(item["key"], 0.0)
            if quantity <= 0:
                continue
            if quantity > item["total_quantity"] + 1e-9:
                raise RuleError(
                    "production_material_quantity",
                    f"材料 {item['key']} 的累计生产数量超过订单总量："
                    f"{quantity:g} > {item['total_quantity']:g}",
                )
            result.append({
                "material_type": item["material_type"],
                "color": item["color"],
                "thickness": item["thickness"],
                "edge": item["edge"],
                "unit": item["unit"],
                "quantity": quantity,
                "key": item["key"],
            })
        return result
    finally:
        connection.close()


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
        for key, quantity in _legacy_inventory_consumed(config, connection, normalized).items():
            consumed[key] = consumed.get(key, 0.0) + quantity
        for item in _order_material_rows(connection, normalized):
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
    """Validate a production request without changing business state.

    Inventory is an external system.  Keep this step as an in-memory draft;
    the completed production batch is recorded only after inventory returns a
    confirmed saved document.
    """
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
    selected_materials = []
    for key, quantity in requested.items():
        if quantity <= 0:
            continue
        item = available[key]
        selected_materials.append({
            "material_type": item["material_type"],
            "color": item["color"],
            "thickness": item["thickness"],
            "edge": item["edge"],
            "unit": item["unit"],
            "quantity": quantity,
            "key": key,
        })
    now = _now()
    batch_number = f"MP-{datetime.now().strftime('%Y%m%d-%H%M%S')}-{uuid.uuid4().hex[:6].upper()}"
    return {
        **preview,
        "batch_number": batch_number,
        "production_time": now,
        "status": "draft",
        "materials": selected_materials,
    }


def record_completed_production(
    connection: sqlite3.Connection,
    draft: dict,
) -> dict:
    """Record a successfully completed production in an existing transaction."""
    order_id = _normal(draft.get("order_id")).upper()
    batch_number = _normal(draft.get("batch_number"))
    factory_orders = [
        _normal(value).upper()
        for value in draft.get("selected_factory_orders", [])
        if _normal(value)
    ]
    if not order_id or not batch_number or not factory_orders:
        raise RuleError("production_record", "生产完成记录缺少订单、批次或工厂单")

    existing = connection.execute(
        "select 1 from manual_production_batches where batch_number=?",
        (batch_number,),
    ).fetchone()
    if existing is not None:
        raise RuleError("production_duplicate", f"生产批次已经记录：{batch_number}")

    now = _normal(draft.get("production_time")) or _now()
    cursor = connection.execute(
        """insert into manual_production_batches(
               batch_number, order_id, production_time, source, status, created_at, updated_at
           ) values(?,?,?,?,?,?,?)""",
        (batch_number, order_id, now, "manual", "completed", now, _now()),
    )
    batch_id = cursor.lastrowid
    for factory_order in sorted(set(factory_orders)):
        connection.execute(
            "insert into manual_production_batch_factories(batch_id, order_id, factory_order) values(?,?,?)",
            (batch_id, order_id, factory_order),
        )
    for item in draft.get("materials", []):
        quantity = float(item.get("quantity", 0) or 0)
        if quantity <= 0:
            continue
        connection.execute(
            """insert into manual_production_batch_materials(
                   batch_id, order_id, material_type, color, thickness, edge, unit, quantity
               ) values(?,?,?,?,?,?,?,?)""",
            (
                batch_id,
                order_id,
                _normal(item.get("material_type")),
                _normal(item.get("color")),
                _normal(item.get("thickness")),
                _normal(item.get("edge")),
                _normal(item.get("unit")),
                quantity,
            ),
        )
    return {
        "ok": True,
        "batch_number": batch_number,
        "order_id": order_id,
        "factory_orders": sorted(set(factory_orders)),
        "status": "completed",
    }


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
