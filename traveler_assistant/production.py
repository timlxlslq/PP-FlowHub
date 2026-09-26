"""人工生产事实及订单级材料消耗。

记录表示已确认的生产，不是来源目录的批次标签；工厂单直接关联唯一生产记录。
"""

from __future__ import annotations

import json
import math
import sqlite3
import uuid
from datetime import datetime
from typing import Iterable

from .core import Config, RuleError
from .database import connect_database, ensure_schema


def _now() -> str:
    """返回带本地时区、精确到秒的当前时间字符串；无参数。"""
    return datetime.now().astimezone().isoformat(timespec="seconds")


def _normal(value: object) -> str:
    """把 value 转为去除首尾空白的字符串；空值按空字符串处理。"""
    return str(value or "").strip()


def material_key(row: dict) -> str:
    """从材料记录 row 取得已确认的商品 SKU；缺少 SKU 时拒绝按属性重新匹配。"""
    product_code = _normal(row.get("product_code")).upper()
    if not product_code:
        raise RuleError(
            "production_material_sku",
            "生产材料缺少已确认商品 SKU，不能按颜色、厚度或单位重新识别",
        )
    return product_code


def production_material_code(row: dict) -> str:
    """从生产材料记录 row 读取 SKU，并检查 key 与 product_code 是否一致。

    App 将已确认 SKU 放在 key 中提交，操作日志保留此结构。
    """
    key = _normal(row.get("key")).upper()
    code = _normal(row.get("product_code")).upper()
    if key and code and key != code:
        raise RuleError("production_material_sku", "生产材料 key 与商品 SKU 不一致")
    return material_key({"product_code": code or key})


def _material_row(row: sqlite3.Row | dict) -> dict:
    """将数据库或字典记录 row 转为含标准化材料属性、数量及 SKU 键的字典。"""
    result = {name: _normal(row[name]) for name in (
        "product_code", "material_type", "color", "thickness", "edge", "unit"
    )}
    result["quantity"] = float(row["quantity"] or 0)
    result["key"] = material_key(result)
    return result


def _connect(config: Config) -> sqlite3.Connection:
    """确保结构可用后打开支持按列名读取的数据库连接；config 为业务配置。"""
    ensure_schema(config.workflow_database)
    connection = connect_database(config.workflow_database)
    connection.row_factory = sqlite3.Row
    return connection


def assert_order_active(connection: sqlite3.Connection, order_id: str) -> None:
    """拒绝已中止订单；connection 为数据库连接，order_id 为待检查订单号。"""
    # 历史独立库存库可能没有订单索引表。
    if not connection.execute("select 1 from sqlite_master where type='table' and name='orders'").fetchone():
        return
    row = connection.execute("select stage from orders where order_id=?", (_normal(order_id).upper(),)).fetchone()
    if row is not None and row[0] == "已中止":
        raise RuleError("order_aborted", "订单已中止，不能继续生产或出库")


def _selected_factory_rows(connection: sqlite3.Connection, order_id: str, factory_orders: Iterable[str]) -> list[sqlite3.Row]:
    """校验非空工厂单选择并读取有效记录，未知单号或中止订单会报错。

    参数：connection 为数据库连接；order_id 为归属订单号；factory_orders 为所选工厂单号。
    """
    assert_order_active(connection, order_id)
    selected = sorted({_normal(value).upper() for value in factory_orders if _normal(value)})
    if not selected:
        raise RuleError("production_selection", "生产必须至少选择一个工厂单")
    placeholders = ",".join("?" for _ in selected)
    rows = connection.execute(
        f"""select factory_order, factory_name, order_id, ownership_status, (stage<>'已拆单') as optimized, case when stage='已出货' then '已出库' else '未出库' end as outbound_status
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


def _consumed(connection: sqlite3.Connection, order_id: str, *, include_rework: bool = True) -> dict[str, float]:
    """按 SKU 汇总已完成生产消耗；connection 为数据库连接，order_id 为订单号。"""
    rows = connection.execute(
        """select product_code, coalesce(sum(quantity), 0) quantity
           from production_materials m
           join production_records b on b.batch_id=m.batch_id
           where m.order_id=? and b.status='completed' and (? or b.source<>'aicnc_rework')
           group by product_code""",
        (order_id, include_rework),
    ).fetchall()
    return {str(row["product_code"] or "").upper(): float(row["quantity"] or 0) for row in rows}


def _order_material_rows(connection: sqlite3.Connection, order_id: str) -> list[dict]:
    """按 SKU 汇总订单材料数量，包含多个来源的数量。

    参数：connection 为数据库连接；order_id 为订单号。
    """
    rows = connection.execute(
        """select m.product_code, p.material_kind as material_type,
                  p.material_color as color, p.material_thickness as thickness,
                  case when p.material_kind='edge' then p.material_color else '' end as edge,
                  p.unit, coalesce(sum(m.quantity), 0) quantity
           from material_items m join products p on p.code=m.product_code
           where m.order_id=?
           group by m.product_code
           order by p.material_kind, p.material_color, p.material_thickness, m.product_code""",
        (order_id,),
    ).fetchall()
    return [_material_row(row) for row in rows]


def _historical_material_product_codes(
    connection: sqlite3.Connection,
    materials: list[dict],
) -> dict[str, str]:
    """建立材料键到已确认 SKU 的映射，供历史单据核对。

    参数：connection 为当前接口保留的连接参数，本函数不使用；materials 为材料记录。
    新生产已保存材料消耗；旧单据从审计 JSON 读取 SKU 并直接比较，不按属性重匹配。
    """
    return {
        item["key"]: _normal(item.get("product_code")).upper()
        for item in materials if _normal(item.get("product_code"))
    }


def _legacy_inventory_consumed(
    config: Config,
    connection: sqlite3.Connection,
    order_id: str,
) -> dict[str, float]:
    """从已确认出库单据补算没有材料明细的历史生产消耗。

    参数：config 为当前接口保留的配置参数，本函数不使用；connection 为连接；order_id 为订单号。
    历史迁移可能只标记工厂单已生产而没有材料行；已有明确材料行的批次会跳过，避免重复累计。
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
                   from factory_orders f
                   join production_records b on b.batch_id=f.production_record_id
                   where f.order_id=? and f.factory_order=?
                     and b.status='completed' and b.source='legacy-outbound-migration'
                     and not exists (
                         select 1 from production_materials m
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
    """汇总订单累计材料消耗，供更新订单级金蝶材料出库单。

    参数：config 为业务配置；order_id 为订单号；current_materials 为本次生产草稿材料。
    累计量包含已完成批次、历史确认消耗和当前草稿；此处不登记新生产事实，
    草稿须在金蝶确认保存后另行登记。
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

        # 返工已用独立补单扣库存，不能再次并入普通订单累计出库单。
        cumulative = _consumed(connection, normalized, include_rework=False)
        for key, quantity in _legacy_inventory_consumed(config, connection, normalized).items():
            cumulative[key] = cumulative.get(key, 0.0) + quantity

        for raw in current_materials:
            item = dict(raw)
            key = production_material_code(item)
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
                "product_code": item["product_code"],
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
    """校验工厂单生产资格并返回订单材料总量、已消耗量及剩余量。

    参数：config 为业务配置；order_id 为订单号；factory_orders 为所选工厂单号。
    """
    normalized = _normal(order_id).upper()
    connection = _connect(config)
    try:
        factories = _selected_factory_rows(connection, normalized, factory_orders)
        not_optimized = [row["factory_order"] for row in factories if not bool(row["optimized"])]
        if not_optimized:
            raise RuleError("production_not_optimized", "以下工厂单尚未优化，不能生产：" + "、".join(not_optimized), factory_orders=not_optimized)
        already_produced = [row["factory_order"] for row in factories if row["outbound_status"] == "已出库" or connection.execute(
            """select 1 from factory_orders f
               join production_records b on b.batch_id=f.production_record_id
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
    """将 value 从 JSON 字符串或列表解析成材料字典列表；无效结构报错，非字典项过滤。"""
    if isinstance(value, str):
        try:
            value = json.loads(value)
        except json.JSONDecodeError as exc:
            raise RuleError("production_materials", "生产材料数量不是有效 JSON") from exc
    if not isinstance(value, list):
        raise RuleError("production_materials", "生产材料数量必须是数组")
    return [item for item in value if isinstance(item, dict)]


def prepare_production(config: Config, order_id: str, factory_orders: Iterable[str], materials: object) -> dict:
    """校验生产请求并生成内存草稿，不登记生产完成事实。

    参数：config 为业务配置；order_id 为订单号；factory_orders 为所选工厂单；
    materials 为本次消耗的材料列表或 JSON。只有外部库存返回已保存单据后才能登记完成。
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
    if not any(quantity > 0 for quantity in requested.values()):
        raise RuleError("production_material_empty", "请至少选择一项本次实际消耗的板材或封边数量")
    for key, quantity in requested.items():
        remaining = available[key]["remaining_quantity"]
        if not math.isfinite(quantity) or quantity < 0 or quantity > remaining + 1e-9:
            raise RuleError("production_material_quantity", f"材料 {key} 的生产数量超过剩余可用数量：{remaining:g}")
    selected_materials = []
    for key, quantity in requested.items():
        if quantity <= 0:
            continue
        item = available[key]
        selected_materials.append({
            "product_code": item["product_code"],
            "material_type": item["material_type"],
            "color": item["color"],
            "thickness": item["thickness"],
            "edge": item["edge"],
            "unit": item["unit"],
            "quantity": quantity,
            "key": key,
        })
    now = _now()
    request_id = uuid.uuid4().hex
    return {
        **preview,
        "request_id": request_id,
        "production_time": now,
        "status": "draft",
        "materials": selected_materials,
    }


def confirm_production_without_materials(
    config: Config, order_id: str, factory_orders: list[str], materials: object, *, confirm: bool = False,
) -> dict:
    """本次数量全为零时显式确认工厂单生产，不修改订单材料或调用库存。

    参数：config 指向业务库；order_id、factory_orders 限定范围；materials 是本次草稿，
    必须为空或全部为有限零数量；confirm 必须为 True。不推断生产方式、不记录原因。
    """
    if confirm is not True:
        raise RuleError('production_confirmation', '仅确认生产、不扣减材料需要明确确认')
    if isinstance(materials, str):
        try:
            materials = json.loads(materials)
        except json.JSONDecodeError as exc:
            raise RuleError('production_materials', '生产材料数量不是有效 JSON') from exc
    if not isinstance(materials, list) or not all(isinstance(item, dict) for item in materials):
        raise RuleError('production_materials', '生产材料数量必须是材料对象数组')
    for item in materials:
        try:
            raw = item['quantity']
            if isinstance(raw, bool):
                raise ValueError('布尔值不是数量')
            quantity = float(raw)
        except (KeyError, TypeError, ValueError) as exc:
            raise RuleError('production_material_quantity', '生产材料数量无效') from exc
        if not math.isfinite(quantity) or quantity != 0:
            raise RuleError('production_material_quantity', '仅确认生产要求本次所有材料数量为 0；有新增领料请使用材料扣减流程')
    if not isinstance(factory_orders, list) or not all(isinstance(v, str) for v in factory_orders):
        raise RuleError('production_selection', '工厂单选择必须是单号数组')
    normalized = _normal(order_id).upper()
    connection = _connect(config)
    try:
        with connection:
            connection.execute('begin immediate')
            factories = _selected_factory_rows(connection, normalized, factory_orders)
            # 外部操作可能已经成功，先恢复原记录，不能用零消耗覆盖未核对的生产事实。
            pending = connection.execute("""select 1 from inventory_operations where order_id=?
                and status in ('submitting','verification_required','external_confirmed','partial_external_confirmed') limit 1""",
                (normalized,)).fetchone()
            if pending:
                raise RuleError('inventory_recovery_required', '该订单有库存操作尚待核对，请先在待处理中心核对并恢复')
            result = record_completed_production(connection, {
                'order_id': normalized,
                'selected_factory_orders': [row['factory_order'] for row in factories],
                'materials': [],
            })
        return result
    finally:
        connection.close()


def record_completed_production(connection: sqlite3.Connection, draft: dict) -> dict:
    """写入一次已确认生产并关联工厂单，每个工厂单只能关联一次。

    参数：connection 为调用方管理事务的数据库连接；draft 为已确认的生产草稿。
    调用方同时管理库存操作日志事务；材料行记录订单归属，生产记录自身不保存 order_id。
    """
    order_id = _normal(draft.get('order_id')).upper()
    factories = sorted({_normal(v).upper() for v in draft.get('selected_factory_orders', []) if _normal(v)})
    if not factories:
        raise RuleError('production_record', '生产完成记录缺少工厂单')
    owners = {}
    for factory in factories:
        row = connection.execute('select order_id,production_record_id,stage,aimes_status from factory_orders where factory_order=?',(factory,)).fetchone()
        if row is None or not row[0] or (order_id and row[0] != order_id):
            raise RuleError('production_factory_unknown', f'工厂单归属不一致：{factory}')
        if row[1] is not None or row[2] in ('已生产','已出货'):
            raise RuleError('production_duplicate', f'工厂单已经记录生产：{factory}')
        if row[2] != '已优化' or row[3] != 'active':
            raise RuleError('production_not_optimized', f'工厂单尚未优化或已失效：{factory}')
        owners[factory] = row[0]
    for owner in set(owners.values()):
        assert_order_active(connection, owner)
    materials = []
    for item in draft.get('materials', []):
        owner = _normal(item.get('order_id') or order_id).upper()
        if owner not in owners.values():
            raise RuleError('production_record', '生产材料缺少明确的参与订单归属')
        quantity = float(item.get('quantity', 0) or 0)
        if not math.isfinite(quantity) or quantity < 0:
            raise RuleError('production_material_quantity', '生产材料数量必须为有限非负数')
        if quantity:
            materials.append((owner, production_material_code(item), quantity))
    now = _now()
    cursor = connection.execute('''insert into production_records(production_time,source,status,created_at,updated_at)
        values(?,?,'completed',?,?)''',(_normal(draft.get('production_time')) or now,'manual',now,now))
    record_id = cursor.lastrowid
    for factory in factories:
        changed = connection.execute('''update factory_orders set production_record_id=?, stage='已生产'
            where factory_order=? and production_record_id is null''',(record_id,factory)).rowcount
        if changed != 1:
            raise RuleError('production_duplicate', f'工厂单已经记录生产：{factory}')
    for owner, code, quantity in materials:
        connection.execute('''insert into production_materials(batch_id,order_id,product_code,quantity)
            values(?,?,?,?) on conflict(batch_id,order_id,product_code)
            do update set quantity=production_materials.quantity+excluded.quantity''',(record_id,owner,code,quantity))
    return {'ok':True,'production_record_id':record_id,'order_ids':sorted(set(owners.values())),
            'factory_orders':factories,'status':'completed'}


def migrate_legacy_production_state(config: Config) -> dict:
    """为已有出库证据的历史工厂单补记生产事实；config 提供业务数据库配置。"""
    connection = _connect(config)
    migrated = []
    try:
        rows = connection.execute(
            """select factory_order, order_id, (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document
               from factory_orders where aimes_status='active' and order_id<>''
                 and ((case when stage='已出货' then '已出库' else '未出库' end) in ('已出库','需要更新') or trim(coalesce(outbound_document,''))<>'')"""
        ).fetchall()
        for row in rows:
            if row["outbound_status"] == "需要更新" and _normal(row["outbound_document"]):
                # 旧状态表示材料与五金合并单据和当前材料不一致。新模型不把材料算作工厂单出货，
                # 因而保留原单据作为历史五金出货证据，并视该工厂单为已出货。
                connection.execute(
                    "update factory_orders set stage='已出货', updated_at=? where factory_order=? and order_id=?",
                    (_now(), row["factory_order"], row["order_id"]),
                )
            exists = connection.execute(
                """select 1 from factory_orders f join production_records b on b.batch_id=f.production_record_id
                   where f.order_id=? and f.factory_order=? and b.status='completed' limit 1""",
                (row["order_id"], row["factory_order"]),
            ).fetchone()
            if exists:
                continue
            now = _now()
            cursor = connection.execute(
                """insert into production_records(production_time, source, status, created_at, updated_at)
                   values(?,?,?,?,?)""",
                ("", "legacy-outbound-migration", "completed", now, now),
            )
            connection.execute(
                "update factory_orders set production_record_id=? where order_id=? and factory_order=?",
                (cursor.lastrowid, row["order_id"], row["factory_order"]),
            )
            migrated.append(row["factory_order"])
        connection.commit()
        return {"ok": True, "migrated_factory_orders": migrated, "production_time_missing": migrated}
    finally:
        connection.close()


def assert_shipment_allowed(config: Config, order_id: str, factory_orders: Iterable[str]) -> None:
    """检查工厂单已生产且尚未出货，否则报错。

    参数：config 为业务配置；order_id 为订单号；factory_orders 为待出货工厂单号。
    """
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
                """select 1 from factory_orders f join production_records b on b.batch_id=f.production_record_id
                   where f.order_id=? and f.factory_order=? and b.status='completed' limit 1""",
                (normalized, row["factory_order"]),
            ).fetchone():
                blocked.append(f"{row['factory_order']}（尚未生产）")
        if blocked:
            raise RuleError("shipment_not_allowed", "以下工厂单不能出货：" + "、".join(blocked), factory_orders=[row["factory_order"] for row in rows])
    finally:
        connection.close()
