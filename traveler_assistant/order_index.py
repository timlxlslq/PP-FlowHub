"""订单索引、同步证据及待处理问题状态。

本模块将外部身份和报表观察连接到中央 SQLite 索引，不把 Server 文件元数据
直接当成生产事实。来源路径、指纹、AIMES 身份、出库证据及用户决定分别记录；
索引也用于恢复看板状态和待处理工作。
"""

from __future__ import annotations

from .hardware_facts import server_hardware_quantity, replace_factory_hardware, audit_factory_hardware, audit_hardware_integrity, preserve_confirmed_shipment

import json
import math
import hashlib
import os
import re
import sqlite3
import shutil
import time
import uuid
import xml.etree.ElementTree as ET
from collections import defaultdict
from functools import wraps
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

from .core import (
    AIMES_BULK_FETCH_LIMIT,
    Config,
    RuleError,
    progress,
    factory_name_order_mismatch,
    load_aimes_order_cache,
    load_factory_name_cache,
    save_aimes_order_cache,
    save_factory_name_cache,
)
from .operation_log import log_database_statement
from .fittings import is_fittings_report, select_latest_fittings, fittings_candidate, same_selected_fittings_source
from .report_read_context import report_paths, preview_read_session, current_report_context
from .hardware_source_decisions import load_source_decisions, decision_revision, commit_source_decisions, with_source_decisions
from .database import (
    collapse_actual_installation_days,
    connect_database,
    enable_foreign_keys,
    prepare_pending_session,
    ensure_outbound_document_factory_links,
    ensure_schema,
    server_material_identity_key,
)
from .inventory import (
    InventoryMappings,
    ProductDatabase,
    TravelerItem,
    confirm_product_material_attributes,
    match_item,
)


ORDER_ID_FROM_FACTORY_RE = re.compile(
    r"^(PP\d{4}(?:-\d+)?|CS\d{3})(?=$|[-\s_])",
    re.IGNORECASE,
)
ORDER_TOKEN_RE = re.compile(r"(PP\d{4}(?:-\d+)?|CS\d{3})(?=$|[-\s_])", re.IGNORECASE)
ORDER_FOLDER_RE = re.compile(r"^(PP\d{4}(?:-\d+)?|CS\d{3})$", re.IGNORECASE)
AIMES_ORDER_RE = re.compile(r"^(PP\d{4}(?:-\d+)?|CS\d{3})$", re.IGNORECASE)
FACTORY_RE = re.compile(r"^F\d+$", re.IGNORECASE)
FACTORY_DATE_RE = re.compile(r"^F(\d{6})\d+$", re.IGNORECASE)
INDEX_SCHEMA_VERSION = 11

# 常驻订单服务为中央库登记一个串行使用的 SQLite 连接；一次性 CLI 和测试不登记，仍按原有方式管理连接所有权。
_SHARED_WORKFLOW_PATH: Path | None = None
_SHARED_WORKFLOW_CONNECTION: sqlite3.Connection | None = None


def install_shared_workflow_connection(path: Path, connection: sqlite3.Connection) -> None:
    """登记供当前进程复用的数据库连接并启用外键；path 为数据库路径，connection 为连接。"""
    global _SHARED_WORKFLOW_PATH, _SHARED_WORKFLOW_CONNECTION
    enable_foreign_keys(connection)
    _SHARED_WORKFLOW_PATH = path.resolve()
    _SHARED_WORKFLOW_CONNECTION = connection


def clear_shared_workflow_connection() -> None:
    """清除进程内共享连接及路径登记，不在此关闭连接；无参数。"""
    global _SHARED_WORKFLOW_PATH, _SHARED_WORKFLOW_CONNECTION
    _SHARED_WORKFLOW_PATH = None
    _SHARED_WORKFLOW_CONNECTION = None


def _shared_workflow_connection(path: Path) -> sqlite3.Connection | None:
    """返回与 path 匹配的共享连接，未登记或路径不同则返回 None。"""
    if _SHARED_WORKFLOW_PATH == path.resolve():
        return _SHARED_WORKFLOW_CONNECTION
    return None
SERVER_SHIPPED_WATCH_DAYS = 7
TEMPORARY_SHIPPED_WATCH_DAYS = 3
SERVER_SNAPSHOT_MAX_WORKERS = 4
SERVER_SCAN_SNAPSHOT_FILENAME = "server-scan-snapshot.json"
SERVER_SCAN_XML_KINDS = {"optimization_input", "optimization_result"}
MATERIAL_ALLOCATION_EPSILON = 0.000001
TRAVELER_FILENAME_RE = re.compile(r"^Work Order Traveler\(.+\)\.xlsx$", re.IGNORECASE)


def _now() -> str:
    """返回精确到秒的本地当前时间字符串；无参数。"""
    return datetime.now().isoformat(timespec="seconds")


def _order_id_from_factory_name(name: str) -> str:
    """从工厂单名称 name 提取订单号前缀，无法识别时返回空字符串。"""
    match = ORDER_ID_FROM_FACTORY_RE.match(str(name or "").strip())
    return match.group(1).upper() if match else ""


def _order_type(order_id: str) -> str:
    """根据 order_id 前缀判断自有订单或 CUT TO SIZE 订单。"""
    return "cutToSize" if order_id.upper().startswith("CS") else "owned"


def _server_root_candidates(config: Config) -> list[Path]:
    """按稳定顺序返回两个生产来源根目录；config 提供来源配置。

    另一类订单目录从已配置目录的同级推导，使看板刷新、Server 处理和生产文件页面使用相同路由。"""
    configured = config.source_root.expanduser()
    if configured.name.casefold() == "cut to size":
        candidates = [configured, configured.parent / "Optimized Orders"]
    else:
        candidates = [configured, configured.parent / "CUT TO SIZE"]
    result: list[Path] = []
    seen: set[str] = set()
    for candidate in candidates:
        key = str(candidate)
        if key in seen:
            continue
        seen.add(key)
        result.append(candidate)
    return result


def _available_server_roots(config: Config) -> list[Path]:
    """筛选实际存在的生产来源目录；config 为来源配置。"""
    return [root for root in _server_root_candidates(config) if root.is_dir()]


def _server_root_order_type(root: Path) -> str:
    """根据目录 root 的名称判断其对应的订单类型。"""
    return "cutToSize" if root.name.casefold() == "cut to size" else "owned"


def _server_folder_matches_root(folder: Path, root: Path, order_ids: set[str]) -> bool:
    """判断目录是否属于当前扫描范围；folder 为候选目录，root 为来源根目录，order_ids 为允许的订单号。"""
    if not _is_standard_order_folder(folder.name):
        return True
    return (
        folder.name.upper() in order_ids
        and _order_type(folder.name) == _server_root_order_type(root)
    )


def _is_standard_order_folder(name: str) -> bool:
    """判断目录名称 name 是否符合支持的 PP 或 CS 标准订单格式。"""
    return bool(ORDER_FOLDER_RE.fullmatch(str(name or "")))


def _is_traveler_file(path: Path) -> bool:
    """判断路径 path 的文件名是否符合生产用 Traveler 命名规则。"""
    return bool(TRAVELER_FILENAME_RE.fullmatch(path.name))


def _folder_created_at(folder: Path) -> float:
    """返回目录 folder 的创建时间，文件系统不提供时使用可用的替代时间。"""
    stat = folder.stat()
    return float(getattr(stat, "st_birthtime", stat.st_ctime))


def _path_created_at(path: Path, stat=None) -> float:
    """返回路径 path 的创建时间；stat 为可选的已有元数据，不支持创建时间时使用 ctime。"""
    stat = stat or path.stat()
    return float(getattr(stat, "st_birthtime", stat.st_ctime))


def _display_timestamp(value: float) -> str:
    """把秒级时间戳 value 转为精确到秒的本地时间文本。"""
    return datetime.fromtimestamp(value).isoformat(timespec="seconds")


def _mtime_marker(stat) -> int:
    """从文件元数据 stat 生成可安全存入 SQLite 的毫秒修改时间标记。

    纳秒值在 REAL 浮点列中会丢失低位，导致未变文件被误判；毫秒值在当前日期范围内可精确表示。"""
    return int(stat.st_mtime_ns // 1_000_000)


def _file_content_fingerprint(path: Path) -> str:
    """分块读取 Server 报表 path 并计算 SHA-256 内容指纹。"""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _material_source_fingerprint(store: "OrderIndexStore", path: Path) -> str:
    """取得材料工作簿指纹，优先已有索引，否则读取文件；store 为索引库，path 为报表路径。"""
    row = store.connection.execute(
        "select content_fingerprint from source_files where path=?",
        (str(path),),
    ).fetchone()
    fingerprint = str(row[0] or "") if row else ""
    if fingerprint:
        return fingerprint
    try:
        return _file_content_fingerprint(path)
    except OSError:
        return ""


def _material_fact_fingerprint(source_fingerprint: str, product_code: str) -> str:
    """将材料证据绑定到确认时选定的 SKU；source_fingerprint 为来源指纹，product_code 为 SKU。"""
    payload = "\x1f".join((
        str(source_fingerprint or "").strip(),
        str(product_code or "").strip().upper(),
    ))
    return "v2:" + hashlib.sha256(payload.encode()).hexdigest()


def _replace_server_material_facts(
    store: "OrderIndexStore",
    order_id: str,
    path: Path,
    parsed_materials: list,
    parsed_edges: dict[str, float],
    mappings: InventoryMappings,
    observed_at: str,
) -> None:
    """替换订单的基础材料来源集合，保留独立补切来源。

    参数：store 为索引库；order_id 为订单号；path 为报表路径；parsed_materials 为板材；
    parsed_edges 为颜色到封边数量的映射；mappings 为商品匹配规则；observed_at 为观察时间。"""
    normalized_order_id = order_id.upper()
    # 基础材料工作簿完整替换基础集合，但嵌套补切报表是增量来源。
    # 不能清空全部来源，否则同次扫描稍后读取根工作簿时会抹掉刚写入的补切夹板。
    existing_paths = store.connection.execute(
        "select distinct source_path from material_items "
        "where order_id=? and source_type='aihouse'",
        (normalized_order_id,),
    ).fetchall()
    for (source_path,) in existing_paths:
        if not _is_recut_material_source(Path(str(source_path or ""))):
            store.connection.execute(
                "delete from material_items where order_id=? "
                "and source_type='aihouse' and source_path=?",
                (normalized_order_id, str(source_path or "")),
            )
    _insert_server_material_source_facts(
        store, normalized_order_id, path, parsed_materials, parsed_edges,
        mappings, observed_at,
    )


def _insert_server_material_source_facts(
    store: "OrderIndexStore",
    order_id: str,
    path: Path,
    parsed_materials: list,
    parsed_edges: dict[str, float],
    mappings: InventoryMappings,
    observed_at: str,
) -> None:
    """把单个来源的材料唯一匹配到商品 SKU 后写入事实，并保留来源指纹。

    参数：store 为索引库；order_id 为订单号；path 为来源路径；parsed_materials 为板材；
    parsed_edges 为封边数量映射；mappings 为商品匹配及忽略规则；observed_at 为观察时间。"""
    from .order_workflow import _material_inventory_name

    normalized_order_id = order_id.upper()
    source_fingerprint = _material_source_fingerprint(store, path)
    with ProductDatabase(store.path) as catalog:
        rows = [
            (item.kind, item.color, item.thickness, float(item.quantity),
             _material_inventory_name(item.kind, item.thickness, item.color))
            for item in parsed_materials
        ] + [
            ("edge", color, "", float(quantity), f"Edge banding--{color}")
            for color, quantity in parsed_edges.items()
        ]
        for kind, color, thickness, quantity, name in rows:
            if not math.isfinite(quantity) or quantity <= MATERIAL_ALLOCATION_EPSILON:
                continue
            if mappings.ignored_reason(name) is not None:
                continue
            matched = match_item(
                catalog, mappings,
                TravelerItem(0, "板材与封边", name, quantity, normalized_order_id),
            )
            codes = sorted({entry.product_code.strip().upper() for entry in matched})
            if len(codes) != 1:
                raise RuleError(
                    "order_inventory_mapping_required",
                    f"材料 {name} 未唯一对应一个商品 SKU",
                )
            product_code = codes[0]
            confirm_product_material_attributes(
                store.connection, product_code, kind, color, thickness
            )
            store.connection.execute(
                """insert into material_items(
                    order_id,product_code,quantity,source_type,source_path,
                    source_fingerprint,updated_at
                ) values(?,?,?,?,?,?,?)
                on conflict(order_id,product_code,source_type,source_path)
                do update set quantity=material_items.quantity+excluded.quantity,
                    source_fingerprint=excluded.source_fingerprint,
                    updated_at=excluded.updated_at""",
                (normalized_order_id, product_code, quantity, "aihouse", str(path),
                 _material_fact_fingerprint(source_fingerprint, product_code), observed_at),
            )


def _replace_server_incremental_material_facts(
    store: "OrderIndexStore",
    order_id: str,
    path: Path,
    parsed_materials: list,
    parsed_edges: dict[str, float],
    mappings: InventoryMappings,
    observed_at: str,
) -> None:
    """只替换指定增量报表的材料事实，不替换订单基础来源。

    参数：store 为索引库；order_id 为订单号；path 为增量来源；parsed_materials 为板材；
    parsed_edges 为封边数量映射；mappings 为商品规则；observed_at 为观察时间。"""
    normalized_order_id = order_id.upper()
    store.connection.execute(
        "delete from material_items where order_id=? and source_type='aihouse' and source_path=?",
        (normalized_order_id, str(path)),
    )
    _insert_server_material_source_facts(
        store, normalized_order_id, path, parsed_materials, parsed_edges,
        mappings, observed_at,
    )


def _server_scan_baseline(config: Config) -> float:
    """解析 config 中的 Server 扫描基准时间，返回用于比较的时间戳。"""
    try:
        return datetime.fromisoformat(config.server_scan_baseline_at).timestamp()
    except ValueError:
        return 0.0


def _valid_aimes_order_id(value: str) -> str:
    """标准化并校验销售订单号 value，格式无效时返回空字符串。"""
    order_id = str(value or "").upper().strip()
    if not AIMES_ORDER_RE.fullmatch(order_id):
        return ""
    return order_id


def _normalize_split_time(value: str) -> str:
    """标准化拆单时间文本 value，统一日期分隔符和空白。"""
    text = str(value or "").strip().replace("/", "-")
    if not text:
        return ""
    text = re.sub(r"\s+", " ", text)
    try:
        return datetime.fromisoformat(text).isoformat(timespec="seconds")
    except ValueError:
        pass
    for pattern in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, pattern).isoformat(timespec="seconds")
        except ValueError:
            continue
    return ""


def _factory_order_date(factory_order: str) -> date | None:
    """从带日期的 AIMES 工厂单号 factory_order 中提取 YYMMDD 日期。"""
    match = FACTORY_DATE_RE.fullmatch(str(factory_order or "").strip().upper())
    if match is None:
        return None
    try:
        return datetime.strptime(match.group(1), "%y%m%d").date()
    except ValueError:
        return None


def _factory_order_before_initial_date(
    factory_order: str,
    split_time: str,
    initial_date: str,
) -> bool:
    """判断工厂单是否早于首次扫描日期。

    参数：factory_order 为工厂单号；split_time 为拆单时间；initial_date 为首次扫描日期。
    优先使用工厂单号内嵌日期，其次使用拆单时间；缺失或无效日期保留为正常待检查项。"""
    try:
        cutoff = date.fromisoformat(str(initial_date or "").strip())
    except ValueError:
        return False
    order_date = _factory_order_date(factory_order)
    if order_date is None:
        normalized = _normalize_split_time(split_time)
        if not normalized:
            return False
        try:
            order_date = datetime.fromisoformat(normalized).date()
        except ValueError:
            return False
    return order_date < cutoff


def _aimes_order_fingerprint(
    store: "OrderIndexStore",
    order_id: str,
) -> str:
    """计算订单持久 AIMES 身份的稳定指纹；store 为索引库，order_id 为订单号。

    指纹不含本地来源标签，避免同一身份从 Server 来源变成 AIMES 确认时被误判为业务变化。"""
    normalized_order = str(order_id or "").upper().strip()
    rows = store.connection.execute(
        """
        select factory_order, factory_name, sales_order_name, split_time,
               aimes_status, aimes_deleted_at
        from factory_orders
        where name_source = 'AIMES'
          and (order_id = ? or sales_order_name = ?)
        order by factory_order
        """,
        (normalized_order, normalized_order),
    ).fetchall()
    payload = [
        [str(value or "") for value in row]
        for row in rows
    ]
    return hashlib.sha256(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def _order_is_before_initial_date(
    config: Config,
    store: "OrderIndexStore",
    order_id: str,
    folder: Path,
) -> bool:
    """判断订单是否早于首次扫描，优先工厂单日期，否则使用目录创建时间。

    参数：config 提供基准日期；store 为索引库；order_id 为订单号；folder 为来源目录。"""
    normalized_order = str(order_id or "").upper().strip()
    rows = store.connection.execute(
        """
        select factory_order, split_time
        from factory_orders
        where order_id = ? or sales_order_name = ?
        """,
        (normalized_order, normalized_order),
    ).fetchall()
    if rows:
        return all(
            _factory_order_before_initial_date(factory_order, split_time, config.initial_date)
            for factory_order, split_time in rows
        )
    try:
        cutoff = datetime.fromisoformat(config.initial_date).timestamp()
        return _folder_created_at(folder) < cutoff
    except (OSError, ValueError):
        return False


def _order_has_active_aimes_mapping(store: "OrderIndexStore", order_id: str) -> bool:
    """检查订单是否有有效的 AIMES 身份映射；store 为索引库，order_id 为订单号。"""
    normalized_order = str(order_id or "").upper().strip()
    return store.connection.execute(
        """
        select 1 from factory_orders
        where name_source = 'AIMES'
          and aimes_status = 'active'
          and (order_id = ? or sales_order_name = ?)
        limit 1
        """,
        (normalized_order, normalized_order),
    ).fetchone() is not None


def _order_shipped_watch_until(
    store: "OrderIndexStore",
    order_id: str,
    now: str,
) -> str:
    """计算出货后观察截止时间，优先最新出货时间。

    参数：store 为索引库；order_id 为订单号；now 为没有可用出货时间时的基准时间。"""
    normalized_order = str(order_id or "").upper().strip()
    values = [
        str(row[0]).strip()
        for row in store.connection.execute(
            """
            select outbound_completed_at
            from factory_orders
            where order_id = ? or sales_order_name = ?
            """,
            (normalized_order, normalized_order),
        ).fetchall()
        if str(row[0] or "").strip()
    ]
    latest = now
    if values:
        parsed: list[tuple[float, datetime]] = []
        for value in values:
            try:
                parsed_value = datetime.fromisoformat(value)
                parsed.append((parsed_value.timestamp(), parsed_value))
            except (OSError, OverflowError, ValueError):
                continue
        if parsed:
            latest = max(parsed, key=lambda item: item[0])[1].isoformat(timespec="seconds")
    try:
        base = datetime.fromisoformat(latest)
    except (OSError, OverflowError, ValueError):
        base = datetime.now()
    return (base + timedelta(days=SERVER_SHIPPED_WATCH_DAYS)).isoformat(timespec="seconds")


def _datetime_timestamp(value: str) -> float:
    """把 ISO 时间文本 value 转为可比较的时间戳，兼容带时区或本地时间。"""
    return datetime.fromisoformat(str(value or "").strip()).timestamp()


def _visible_aimes_row(row: dict) -> dict | None:
    """校验并标准化 AIMES 记录 row，身份或归属无效时返回 None。"""
    factory_order = str(row.get("factory_order", "")).upper().strip()
    factory_name = str(row.get("factory_name", "")).strip()
    sales_order_name = str(row.get("sales_order_name", "")).upper().strip()
    if _aimes_row_issue(row) is not None or not FACTORY_RE.fullmatch(factory_order):
        return None
    order_id = _valid_aimes_order_id(sales_order_name)
    if not order_id:
        return None
    return {
        "factory_order": factory_order,
        "factory_name": factory_name,
        "sales_order_name": order_id,
        "split_time": _normalize_split_time(str(row.get("split_time", ""))),
    }


def _aimes_ignore_key(row: dict) -> str:
    """生成 AIMES 记录 row 的忽略键，优先工厂单号，无单号时使用名称内容指纹。"""
    factory_order = str(row.get("factory_order", "")).upper().strip()
    if factory_order:
        return f"factory:{factory_order}"
    identity = json.dumps(
        {
            "factory_name": str(row.get("factory_name", "")).strip(),
            "sales_order_name": str(row.get("sales_order_name", "")).strip(),
        },
        ensure_ascii=False,
        sort_keys=True,
    )
    return f"row:{hashlib.sha256(identity.encode('utf-8')).hexdigest()}"


def _aimes_row_issue(row: dict) -> dict | None:
    """检查 AIMES 记录 row 的单号、测试标记和订单归属，返回问题说明或 None。"""
    factory_order = str(row.get("factory_order", "")).upper().strip()
    factory_name = str(row.get("factory_name", "")).strip()
    sales_order_name = str(row.get("sales_order_name", "")).upper().strip()
    reasons: list[str] = []
    if not FACTORY_RE.fullmatch(factory_order):
        reasons.append("工厂单号不是 F 加数字的格式")
    if "test" in factory_name.casefold() or "test" in sales_order_name.casefold():
        reasons.append("工厂单名称或销售单名称包含 test")
    format_match = AIMES_ORDER_RE.fullmatch(sales_order_name)
    suggested_order_id = ""
    if not format_match:
        reasons.append("销售单名称不是 PP 加 4 位数字（可带数字后缀）或 CS 加 3 位数字")
        candidate = _order_id_from_factory_name(factory_name)
        suggested_order_id = _valid_aimes_order_id(candidate) if candidate else ""
    else:
        mismatch = factory_name_order_mismatch(factory_name, sales_order_name)
        if mismatch:
            prefix, order = mismatch
            reasons.append(f"工厂单名称订单前缀 {prefix} 与销售单名称 {order} 不一致")
    if not reasons:
        return None
    return {
        "id": _aimes_ignore_key(row),
        "ignore_key": _aimes_ignore_key(row),
        "factory_order": factory_order,
        "factory_name": factory_name,
        "sales_order_name": sales_order_name,
        "split_time": _normalize_split_time(str(row.get("split_time", ""))),
        "reason": "；".join(reasons),
        "suggested_order_id": suggested_order_id,
    }


def _partition_aimes_rows(
    rows: list[dict],
    ignored_keys: set[str],
    assignments: dict[str, str] | None = None,
) -> tuple[list[dict], list[dict]]:
    """将 AIMES 记录划分为可用数据及待处理问题。

    参数：rows 为来源记录；ignored_keys 为已忽略身份；assignments 为可选人工订单归属映射。"""
    visible: list[dict] = []
    issues: list[dict] = []
    seen_issues: set[str] = set()
    assignments = assignments or {}
    for raw in rows:
        ignore_key = _aimes_ignore_key(raw)
        if ignore_key in ignored_keys:
            continue
        factory_order = str(raw.get("factory_order", "")).upper().strip()
        assigned_order_id = assignments.get(ignore_key, "")
        if assigned_order_id and FACTORY_RE.fullmatch(factory_order):
            visible.append({
                "factory_order": factory_order,
                "factory_name": str(raw.get("factory_name", "")).strip(),
                "sales_order_name": assigned_order_id,
                "split_time": _normalize_split_time(str(raw.get("split_time", ""))),
            })
            continue
        issue = _aimes_row_issue(raw)
        if issue is not None:
            if issue["ignore_key"] not in seen_issues:
                issues.append(issue)
                seen_issues.add(issue["ignore_key"])
            continue
        row = _visible_aimes_row(raw)
        if row is not None:
            visible.append(row)
    return visible, issues


def _merge_aimes_recent_and_verified_rows(
    recent_rows: list[dict],
    verification_result: dict | None,
    *,
    cached_rows: list[dict] | None = None,
) -> list[dict]:
    """合并近期页面和窗口外精确核验记录。

    参数：recent_rows 为近期记录；verification_result 为核验结果；cached_rows 为可选已有记录。
    核验找到的记录也是权威身份数据，须用于持久保存，不仅表示未被删除。"""
    cached_by_factory = {
        str(row.get("factory_order", "")).upper().strip(): row
        for row in (cached_rows or [])
        if isinstance(row, dict) and str(row.get("factory_order", "")).strip()
    }

    def retain_cached_split_time(row: dict) -> dict:
        """为记录 row 补回已有拆单时间，仅在本次返回空值时使用缓存，不覆盖新时间。"""
        current = dict(row)
        if str(current.get("split_time", "")).strip():
            return current
        factory_order = str(current.get("factory_order", "")).upper().strip()
        cached = cached_by_factory.get(factory_order, {})
        cached_split_time = str(cached.get("split_time", "")).strip()
        if cached_split_time:
            current["split_time"] = cached_split_time
        return current

    merged: dict[str, dict] = {}
    for row in recent_rows:
        factory_order = str(row.get("factory_order", "")).upper().strip()
        if factory_order:
            merged[factory_order] = retain_cached_split_time(row)
    for row in (verification_result or {}).get("rows", []):
        if not isinstance(row, dict):
            continue
        factory_order = str(row.get("factory_order", "")).upper().strip()
        if factory_order and factory_order not in merged:
            merged[factory_order] = retain_cached_split_time(row)
    return list(merged.values())


def _business_validation_message(exc: Exception) -> str:
    """将解析或运行异常 exc 转换为便于用户处理的订单校验说明。"""
    message = str(exc).strip()
    lowered = message.casefold()
    if "找不到文件名包含 material" in message or "missing material" in lowered:
        return "未找到订单所需的 material 文件。请在订单根目录补充 material，或打开订单后选择自动生成，再重新处理 Server 变化。"
    if "缺少 order no." in lowered:
        return "Fittingslist 的订单编号区域无法识别。请确认使用正确版本的五金报表，修正后重新扫描 Server。"
    if "无法读取" in message or "文件损坏" in message or "badzipfile" in lowered:
        return "订单报表无法正常打开。请确认 Excel 文件未损坏、未被占用且格式正确，然后重新扫描 Server。"
    if "服务器目录不可访问" in message:
        return "Server 订单目录当前无法访问。请确认已连接公司网络并挂载 Server，然后重新扫描。"
    if isinstance(exc, RuleError) and message:
        return f"{message}。请按提示检查订单报表，修正后重新扫描 Server。"
    return "订单报表未能完成校验。请检查 material、板材清单和 Fittingslist 是否完整且可以打开，然后重新扫描 Server。"


def _business_aimes_message(exc: Exception) -> str:
    """将 AIMES 异常 exc 转换为对应查询阶段和错误类型的中文处理提示。"""
    raw_message = str(exc).strip()
    message = raw_message.casefold()
    code = str(getattr(exc, "code", "") or "").strip().casefold()
    if code == "aimes_table_not_ready" or "aimes_table_not_ready" in message or "表格尚未加载完成" in message:
        return "AIMES 工厂订单表尚未加载完成。请稍后重新获取。"
    if code == "aimes_table_schema" or "缺少必要列" in message or "表头" in message:
        return "AIMES 工厂订单表缺少必要列。请确认当前表格包含工厂单号、工厂单名称、销售单名称和拆单时间列后重新获取。"
    if code == "aimes_credentials" or any(word in message for word in ("password", "credential", "账号或密码错误", "用户名或密码", "登录失败", "凭证无效")):
        return "AIMES 登录未成功。请在设置中确认用户名和密码后重新获取。"
    if code == "aimes_timeout" or any(word in message for word in ("timeout", "timed out", "network", "connection", "网络", "超时")):
        return "AIMES 暂时没有响应。请确认网络连接正常，稍后重新获取。"
    if code == "aimes_factory_name_missing" or "找不到工厂单名称" in message:
        return "AIMES 未返回所需工厂单名称。请确认工厂单仍存在且可查询，然后重新获取。"
    return "AIMES 数据获取未完成。请确认网络、账号密码和 AIMES 可用状态后重新获取。"


def _business_server_message(exc: Exception) -> str:
    """将 Server 异常 exc 转换为目录或权限相关的中文处理提示。"""
    message = str(exc).strip().casefold()
    if "所选文件夹" in message or "订单文件夹" in message:
        return str(exc).strip()
    if any(word in message for word in ("permission", "not permitted", "权限")):
        return "App 没有访问 Server 订单目录的权限。请确认 Server 已挂载并允许 App 访问后重新扫描。"
    return "Server 订单目录当前无法访问。请确认已连接公司网络并挂载 Server，然后重新扫描。"


def _business_report_message(kind: str, path: Path) -> str:
    """生成报表读取失败提示；kind 为报表类别，path 为报表路径。"""
    report_name = "板材清单" if kind == "board" else "Fittingslist"
    return f"{report_name} {path.name} 无法读取。请确认文件完整、未被占用且格式正确，修正后重新扫描 Server。"


def _source_path_in_dashboard_scope(root: Path, value: str) -> bool:
    """判断已索引来源是否属于看板扫描范围；root 为扫描根目录，value 为来源路径。"""
    try:
        relative = Path(value).relative_to(root)
    except ValueError:
        return False
    if not relative.parts:
        return False
    folder_name = relative.parts[0]
    if folder_name.upper().startswith("PP"):
        return bool(_valid_aimes_order_id(folder_name))
    return True


def pending_check_session(function):
    """一次命令内共享临时检查结果；App 服务沿用已有连接，命令退出后普通问题消失。"""
    @wraps(function)
    def run(config, *args, **kwargs):
        if _shared_workflow_connection(config.workflow_database) is not None or getattr(config, "workflow_connection", None) is not None:
            return function(config, *args, **kwargs)
        store = OrderIndexStore(config.workflow_database)
        install_shared_workflow_connection(config.workflow_database, store.connection)
        try:
            return function(config, *args, **kwargs)
        finally:
            clear_shared_workflow_connection()
            store.close()
    return run


class OrderIndexStore:
    """订单看板使用的持久订单、工厂单及来源索引。"""

    def __init__(self, path: Path, *, connection: sqlite3.Connection | None = None):
        """建立订单索引存储，复用连接或准备数据库结构，并创建临时校验表。

        参数：path 为数据库路径；connection 为可选外部连接，不提供时优先使用已登记共享连接。"""
        shared_connection = connection is None and _shared_workflow_connection(path) is not None
        if connection is None:
            connection = _shared_workflow_connection(path)
            if connection is None:
                path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self._uses_shared_connection = shared_connection
        self._owns_connection = connection is None
        if connection is None:
            ensure_schema(path)
            self.connection = connect_database(path)
        else:
            self.connection = enable_foreign_keys(connection)
        prepare_pending_session(self.connection)
        self.connection.execute("""create temp table if not exists preview_validation(
            order_id text primary key,status text not null,message text not null)""")
        self.connection.set_trace_callback(lambda statement: log_database_statement(self.path, statement))
        version = self.connection.execute("pragma user_version").fetchone()[0]
        if version not in (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, INDEX_SCHEMA_VERSION):
            self.connection.close()
            raise RuntimeError(f"订单索引数据库版本不受支持：{version}")
        if self._uses_shared_connection:
            return
        self.connection.executescript(
            f"""
            create table if not exists orders(
                order_id text primary key,
                order_type text not null,
                source_folder text not null default '',
                source_folder_mtime real,
                stage text not null default '已设计',
                last_server_seen text not null default '',
                last_aimes_seen text not null default '',
                updated_at text not null,
                user_note text not null default '',
                server_scan_policy text not null default '',
                server_scan_aimes_fingerprint text not null default '',
                server_scan_watch_until text not null default '',
                server_scan_policy_updated_at text not null default ''
            );
            create table if not exists order_installation_days(
                order_id text not null,
                date_type text not null check(date_type in ('planned', 'actual')),
                install_date text not null,
                installer text not null default '',
                updated_at text not null,
                primary key(order_id, date_type, install_date)
            );
            create index if not exists idx_order_installation_days_order
                on order_installation_days(order_id, date_type, install_date);
            create table if not exists factory_orders(
                factory_order text primary key,
                order_id text not null default '',
                production_record_id integer references production_records(batch_id),
                factory_name text not null default '',
                sales_order_name text not null default '',
                split_time text not null default '',
                name_source text not null default '',
                source_folder text not null default '',
                report_state text not null default '未发现',
                ownership_status text not null default '待确认',
                has_hardware integer not null default 0,
                stage text not null default '已拆单' check(stage in ('已拆单','已优化','已生产','已出货')),
                outbound_document text not null default '',
                outbound_mode text not null default '',
                outbound_fingerprint text not null default '',
                last_server_seen text not null default '',
                last_aimes_seen text not null default '',
                updated_at text not null
            );
            create table if not exists source_files(
                path text primary key,
                source_folder text not null default '',
                kind text not null,
                order_id text not null default '',
                factory_order text not null default '',
                modified_at real not null default 0,
                size integer not null default 0,
                content_fingerprint text not null default '',
                last_seen text not null
            );
            create table if not exists server_scan_xml_state(
                path text primary key,
                source_folder text not null,
                kind text not null,
                order_id text not null default '',
                modified_at integer not null default 0,
                last_seen text not null
            );
            create index if not exists idx_server_scan_xml_state_folder
                on server_scan_xml_state(source_folder, kind);
            create table if not exists server_material_allocations(
                id integer primary key,
                source_path text not null default '',
                source_material_key text not null default '',
                product_code text not null check(trim(product_code) <> ''),
                source_quantity real not null default 0,
                order_id text not null,
                allocated_quantity real not null default 0,
                source_fingerprint text not null default '',
                created_at text not null,
                updated_at text not null,
                unique(source_path, source_material_key, order_id),
                foreign key(product_code) references products(code)
                    on update cascade on delete restrict
            );
            create index if not exists idx_server_material_allocations_source
                on server_material_allocations(source_path, source_material_key);
            create index if not exists idx_server_material_allocations_order
                on server_material_allocations(order_id);
            create table if not exists server_material_preview_scopes(
                source_folder text primary key
            );
            create table if not exists sync_runs(
                id integer primary key,
                started_at text not null,
                finished_at text not null,
                aimes_attempted integer not null default 0,
                aimes_succeeded integer not null default 0,
                aimes_count integer not null default 0,
                server_folder_count integer not null default 0,
                error text not null default ''
            );
            create table if not exists sync_changes(
                id integer primary key,
                observed_at text not null,
                severity text not null,
                kind text not null,
                order_id text not null default '',
                factory_order text not null default '',
                path text not null default '',
                message text not null
            );
            create table if not exists ignored_aimes_factory_orders(
                ignore_key text primary key,
                factory_order text not null default '',
                factory_name text not null default '',
                sales_order_name text not null default '',
                reason text not null default '',
                ignored_at text not null
            );
            create table if not exists aimes_order_assignments(
                ignore_key text primary key,
                factory_order text not null,
                factory_name text not null default '',
                original_sales_order_name text not null default '',
                assigned_order_id text not null,
                confirmed_at text not null
            );
            create table if not exists aimes_review_rows(
                ignore_key text primary key,
                factory_order text not null default '',
                factory_name text not null default '',
                sales_order_name text not null default '',
                reason text not null default '',
                suggested_order_id text not null default '',
                split_time text not null default '',
                last_seen text not null
            );
            create table if not exists active_issues(
                issue_key text primary key,
                kind text not null,
                order_id text not null default '',
                factory_order text not null default '',
                path text not null default '',
                message text not null,
                status text not null default 'open',
                first_seen text not null,
                last_seen text not null,
                resolved_at text not null default ''
            );
            create table if not exists temporary_orders(
                temporary_id text primary key,
                folder_name text not null,
                source_folder text not null unique,
                folder_created_at real not null default 0,
                content_fingerprint text not null default '',
                traveler_path text not null default '',
                traveler_fingerprint text not null default '',
                traveler_include_hardware integer not null default 1,
                traveler_status text not null default '未生成',
                traveler_generated_at text not null default '',
                processing_status text not null default '未处理',
                outbound_status text not null default '未出库',
                outbound_document text not null default '',
                processed_at text not null default '',
                outbound_at text not null default '',
                last_error text not null default '',
                server_scan_policy text not null default '',
                server_scan_watch_until text not null default '',
                server_scan_policy_updated_at text not null default '',
                updated_at text not null
            );
            create table if not exists optimization_artifacts(
                id integer primary key,
                source_path text not null,
                order_id text not null default '',
                factory_order text not null,
                file_modified_at real not null,
                file_created_at real not null default 0,
                completed_at text not null,
                copied_at text not null default '',
                first_seen_at text not null,
                last_seen_at text not null,
                size integer not null default 0,
                unique(source_path, file_modified_at, size, factory_order)
            );
            create index if not exists idx_optimization_artifacts_factory
                on optimization_artifacts(order_id, factory_order, completed_at);
            create table if not exists server_folder_ignores(
                path text primary key,
                ignored_at text not null
            );
            create index if not exists idx_factory_order_id on factory_orders(order_id);
            create index if not exists idx_sync_changes_observed on sync_changes(observed_at desc);
            create index if not exists idx_active_issues_status on active_issues(status, last_seen desc);
            """
        )
        # 旧的按月忽略目录功能已移除，删除旧版 App 留下的无效表。
        self.connection.execute("drop table if exists ignored_server_folders")
        collapse_actual_installation_days(self.connection)
        # 旧版索引把纳秒存入 REAL 列；在此一次性标准化，避免首次刷新让所有未变报表重新解析。
        self.connection.execute(
            """
            update source_files
            set modified_at = cast(modified_at / 1000000 as integer)
            where modified_at >= 1000000000000000
            """
        )
        factory_columns = {
            row[1] for row in self.connection.execute("pragma table_info(factory_orders)").fetchall()
        }
        if "sales_order_name" not in factory_columns:
            self.connection.execute(
                "alter table factory_orders add column sales_order_name text not null default ''"
            )
        if "split_time" not in factory_columns:
            self.connection.execute(
                "alter table factory_orders add column split_time text not null default ''"
            )
        if "outbound_mode" not in factory_columns:
            self.connection.execute(
                "alter table factory_orders add column outbound_mode text not null default ''"
            )
        if "outbound_fingerprint" not in factory_columns:
            self.connection.execute(
                "alter table factory_orders add column outbound_fingerprint text not null default ''"
            )
        order_columns = {
            row[1] for row in self.connection.execute("pragma table_info(orders)").fetchall()
        }
        if "user_note" not in order_columns:
            self.connection.execute(
                "alter table orders add column user_note text not null default ''"
            )
        for column, definition in (
            ("server_scan_policy", "text not null default ''"),
            ("server_scan_aimes_fingerprint", "text not null default ''"),
            ("server_scan_watch_until", "text not null default ''"),
            ("server_scan_policy_updated_at", "text not null default ''"),
        ):
            if column not in order_columns:
                self.connection.execute(
                    f"alter table orders add column {column} {definition}"
                )
        temporary_columns = {
            row[1] for row in self.connection.execute("pragma table_info(temporary_orders)").fetchall()
        }
        for column, definition in (
            ("handling_mode", "text not null default ''"),
            ("reference_order_ids", "text not null default '[]'"),
            ("traveler_fingerprint", "text not null default ''"),
            ("traveler_include_hardware", "integer not null default 1"),
            ("traveler_status", "text not null default '未生成'"),
            ("traveler_generated_at", "text not null default ''"),
            ("server_scan_policy", "text not null default ''"),
            ("server_scan_watch_until", "text not null default ''"),
            ("server_scan_policy_updated_at", "text not null default ''"),
        ):
            if column not in temporary_columns:
                self.connection.execute(
                    f"alter table temporary_orders add column {column} {definition}"
                )
        source_columns = {
            row[1] for row in self.connection.execute("pragma table_info(source_files)").fetchall()
        }
        if "content_fingerprint" not in source_columns:
            self.connection.execute(
                "alter table source_files add column content_fingerprint text not null default ''"
            )
        for column, definition in (
            ("aimes_status", "text not null default 'active'"),
            ("aimes_deleted_at", "text not null default ''"),
            ("aimes_last_verified_at", "text not null default ''"),
            ("optimization_first_completed_at", "text not null default ''"),
            ("optimization_latest_completed_at", "text not null default ''"),
            ("optimization_first_seen_at", "text not null default ''"),
            ("optimization_latest_seen_at", "text not null default ''"),
            ("optimization_source_path", "text not null default ''"),
            ("outbound_completed_at", "text not null default ''"),
        ):
            if column not in factory_columns:
                self.connection.execute(
                    f"alter table factory_orders add column {column} {definition}"
                )
        if version < 8 and self.connection.execute(
            "select 1 from sqlite_master where type='table' and name='outbound_documents'"
        ).fetchone() and self.connection.execute(
            "select 1 from sqlite_master where type='table' and name='outbound_document_factories'"
        ).fetchone():
            # 已有出库行保存了库存系统开单时间；一次性补齐，使月度完成数量依据最后工厂单出货时间，而不是后续索引刷新时间。
            self.connection.execute(
                """
                update factory_orders
                set outbound_completed_at = coalesce((
                    select max(coalesce(nullif(od.issued_at, ''), od.updated_at))
                    from outbound_document_factories odf
                    join outbound_documents od
                      on od.document_number = odf.document_number
                    where odf.order_id = factory_orders.order_id
                      and odf.factory_order = factory_orders.factory_order
                      and od.status = '已出库'
                ), '')
                where stage = '已出货'
                  and outbound_completed_at = ''
                """
            )
        self.connection.execute("update orders set stage = '已设计' where stage = '待拆单'")
        # 当前问题由读取配置的同步流程创建；仅打开数据库时不从所有未确认工厂单重建问题，避免恢复初始扫描日期之前的历史项。
        if version < 7:
            # 修复旧解析器未传入唯一订单目录提示导致的误报；真实 PP/CS 目录可明确归属，无需等下一次完整扫描。
            stale_rows = self.connection.execute(
                """
                select factory_order, source_folder
                from factory_orders
                where ownership_status <> '已确认'
                  and source_folder <> ''
                """
            ).fetchall()
            for factory_order, source_folder in stale_rows:
                folder_order = _valid_aimes_order_id(Path(source_folder).name)
                if not folder_order or not Path(source_folder).is_dir():
                    continue
                observed_at = _now()
                self.connection.execute(
                    """
                    update factory_orders
                    set order_id = ?, sales_order_name = ?, name_source = 'server_folder',
                        ownership_status = '已确认', updated_at = ?, last_server_seen = ?
                    where factory_order = ?
                    """,
                    (folder_order, folder_order, observed_at, observed_at, factory_order),
                )
                self.upsert_order(folder_order, source_folder=source_folder, server_seen=observed_at)
                self.connection.execute(
                    """
                    update active_issues
                    set status = 'resolved', order_id = ?, resolved_at = ?
                    where issue_key = ? and status = 'open'
                    """,
                    (folder_order, observed_at, f"factory_ownership:{factory_order}"),
                )
                self.connection.execute(
                    """
                    insert into sync_changes(
                        observed_at, severity, kind, order_id, factory_order, path, message
                    ) values(?,?,?,?,?,?,?)
                    """,
                    (
                        observed_at,
                        "info",
                        "factory_ownership_resolved",
                        folder_order,
                        factory_order,
                        source_folder,
                        f"已根据唯一订单文件夹 {Path(source_folder).name} 自动确认工厂单 {factory_order} 归属订单 {folder_order}",
                    ),
                )
        self.connection.execute(f"pragma user_version = {INDEX_SCHEMA_VERSION}")
        self.connection.commit()

    def close(self) -> None:
        """仅关闭本对象拥有的数据库连接；无显式参数，不关闭借用连接。"""
        if self._owns_connection:
            self.connection.close()

    def temporary_order(self, source_folder: str) -> dict | None:
        """按来源目录 source_folder 查询临时订单及处理状态，未找到时返回 None。"""
        row = self.connection.execute(
            """
            select temporary_id, folder_name, source_folder, folder_created_at,
                   content_fingerprint, traveler_path, traveler_fingerprint,
                   traveler_include_hardware, traveler_status, traveler_generated_at,
                   processing_status,
                   outbound_status, outbound_document, processed_at,
                   outbound_at, last_error, server_scan_policy,
                   server_scan_watch_until, server_scan_policy_updated_at, updated_at,
                   handling_mode, reference_order_ids
            from temporary_orders where source_folder = ?
            """,
            (source_folder,),
        ).fetchone()
        if row is None:
            return None
        keys = (
            "temporary_id", "folder_name", "source_folder", "folder_created_at",
            "content_fingerprint", "traveler_path", "traveler_fingerprint",
            "traveler_include_hardware", "traveler_status", "traveler_generated_at",
            "processing_status",
            "outbound_status", "outbound_document", "processed_at",
            "outbound_at", "last_error", "server_scan_policy",
            "server_scan_watch_until", "server_scan_policy_updated_at", "updated_at",
            "handling_mode", "reference_order_ids",
        )
        result = dict(zip(keys, row))
        result["reference_order_ids"] = json.loads(result["reference_order_ids"])
        return result

    def upsert_temporary_order(
        self,
        *,
        temporary_id: str,
        folder_name: str,
        source_folder: str,
        folder_created_at: float,
        content_fingerprint: str,
        traveler_path: str = "",
        traveler_fingerprint: str = "",
        traveler_include_hardware: bool | None = None,
        traveler_status: str = "",
        traveler_generated_at: str = "",
        processing_status: str = "未处理",
        outbound_status: str = "未出库",
        outbound_document: str = "",
        processed_at: str = "",
        outbound_at: str = "",
        last_error: str = "",
        server_scan_policy: str = "",
        server_scan_watch_until: str = "",
        server_scan_policy_updated_at: str = "",
        handling_mode: str = "",
        reference_order_ids: list[str] | None = None,
    ) -> None:
        """新增或更新临时订单，保留未提供的已有处理信息。

        参数：temporary_id 为标识；folder_name、source_folder 为目录名和路径；folder_created_at 为创建时间；
        content_fingerprint 为内容指纹；traveler_path、traveler_fingerprint 为生成文件及指纹；
        traveler_include_hardware 为是否含五金；traveler_status、traveler_generated_at 为生成状态及时间；
        processing_status 为处理状态；outbound_status、outbound_document 为出库状态及单据；
        processed_at、outbound_at 为处理及出库时间；last_error 为错误；server_scan_policy 为扫描策略；
        server_scan_watch_until、server_scan_policy_updated_at 为观察截止及策略更新时间；
        handling_mode 为处理方式；reference_order_ids 为关联订单号列表。"""
        previous = self.temporary_order(source_folder) or {}
        self.connection.execute(
            """
            insert into temporary_orders(
                temporary_id, folder_name, source_folder, folder_created_at,
                content_fingerprint, traveler_path, traveler_fingerprint,
                traveler_include_hardware, traveler_status, traveler_generated_at,
                processing_status,
                outbound_status, outbound_document, processed_at, outbound_at,
                last_error, server_scan_policy, server_scan_watch_until,
                server_scan_policy_updated_at, updated_at, handling_mode, reference_order_ids
            ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            on conflict(source_folder) do update set
                temporary_id=excluded.temporary_id,
                handling_mode=excluded.handling_mode,
                reference_order_ids=excluded.reference_order_ids,
                folder_name=excluded.folder_name,
                folder_created_at=excluded.folder_created_at,
                content_fingerprint=excluded.content_fingerprint,
                traveler_path=case when excluded.traveler_path <> '' then excluded.traveler_path else temporary_orders.traveler_path end,
                traveler_fingerprint=case when excluded.traveler_fingerprint <> '' then excluded.traveler_fingerprint else temporary_orders.traveler_fingerprint end,
                traveler_include_hardware=excluded.traveler_include_hardware,
                traveler_status=case when excluded.traveler_status <> '' then excluded.traveler_status else temporary_orders.traveler_status end,
                traveler_generated_at=case when excluded.traveler_generated_at <> '' then excluded.traveler_generated_at else temporary_orders.traveler_generated_at end,
                processing_status=excluded.processing_status,
                outbound_status=excluded.outbound_status,
                outbound_document=case when excluded.outbound_document <> '' then excluded.outbound_document else temporary_orders.outbound_document end,
                processed_at=case when excluded.processed_at <> '' then excluded.processed_at else temporary_orders.processed_at end,
                outbound_at=case when excluded.outbound_at <> '' then excluded.outbound_at else temporary_orders.outbound_at end,
                last_error=excluded.last_error,
                server_scan_policy=case when excluded.server_scan_policy <> '' then excluded.server_scan_policy else temporary_orders.server_scan_policy end,
                server_scan_watch_until=case when excluded.server_scan_watch_until <> '' then excluded.server_scan_watch_until else temporary_orders.server_scan_watch_until end,
                server_scan_policy_updated_at=case when excluded.server_scan_policy_updated_at <> '' then excluded.server_scan_policy_updated_at else temporary_orders.server_scan_policy_updated_at end,
                updated_at=excluded.updated_at
            """,
            (
                temporary_id,
                folder_name,
                source_folder,
                folder_created_at,
                content_fingerprint,
                traveler_path,
                traveler_fingerprint,
                int(traveler_include_hardware) if traveler_include_hardware is not None else int(previous.get("traveler_include_hardware", 1)),
                traveler_status or previous.get("traveler_status", ""),
                traveler_generated_at or previous.get("traveler_generated_at", ""),
                processing_status,
                outbound_status,
                outbound_document or previous.get("outbound_document", ""),
                processed_at or previous.get("processed_at", ""),
                outbound_at or previous.get("outbound_at", ""),
                last_error,
                server_scan_policy or previous.get("server_scan_policy", ""),
                server_scan_watch_until or previous.get("server_scan_watch_until", ""),
                server_scan_policy_updated_at or previous.get("server_scan_policy_updated_at", ""),
                _now(),
                handling_mode or previous.get("handling_mode", ""),
                json.dumps(reference_order_ids if reference_order_ids is not None else previous.get("reference_order_ids", [])),
            ),
        )

    def ignored_aimes_keys(self) -> set[str]:
        """读取全部已忽略 AIMES 身份键；无显式参数。"""
        return {
            row[0]
            for row in self.connection.execute(
                "select ignore_key from ignored_aimes_factory_orders"
            ).fetchall()
        }

    def ignored_aimes_factories(self) -> list[dict]:
        """读取已忽略工厂单及忽略原因，供管理界面展示；无显式参数。"""
        rows = self.connection.execute(
            """
            select ignore_key, factory_order, factory_name, sales_order_name, reason, ignored_at
            from ignored_aimes_factory_orders
            order by ignored_at desc, factory_order
            """
        ).fetchall()
        return [
            {
                "id": row[0],
                "ignore_key": row[0],
                "factory_order": row[1],
                "factory_name": row[2],
                "sales_order_name": row[3],
                "reason": row[4],
                "ignored_at": row[5],
            }
            for row in rows
        ]

    def aimes_assignments(self) -> dict[str, str]:
        """返回人工指定的 AIMES 身份到订单号的映射；无显式参数。"""
        return {
            row[0]: row[1]
            for row in self.connection.execute(
                "select ignore_key, assigned_order_id from aimes_order_assignments"
            ).fetchall()
        }

    def assigned_aimes_factories(self) -> list[dict]:
        """读取人工指定订单归属的工厂单记录；无显式参数。"""
        rows = self.connection.execute(
            """
            select ignore_key, factory_order, factory_name, original_sales_order_name,
                   assigned_order_id, confirmed_at
            from aimes_order_assignments
            order by confirmed_at desc, factory_order
            """
        ).fetchall()
        return [
            {
                "id": row[0],
                "ignore_key": row[0],
                "factory_order": row[1],
                "factory_name": row[2],
                "sales_order_name": row[3],
                "suggested_order_id": row[4],
                "reason": f"已按工厂单名称确认归入 {row[4]}",
                "ignored_at": row[5],
            }
            for row in rows
        ]

    def replace_aimes_review_rows(self, issues: list[dict]) -> None:
        """替换当前非标准 AIMES 待处理记录；issues 为待用户处理的问题列表。"""
        self.connection.execute("delete from pending_aimes_reviews")
        self.connection.executemany(
            """
            insert into pending_aimes_reviews(
                ignore_key, factory_order, factory_name, sales_order_name,
                reason, suggested_order_id, split_time, last_seen
            ) values(?,?,?,?,?,?,?,?)
            """,
            [
                (
                    str(issue.get("ignore_key", issue.get("id", ""))),
                    str(issue.get("factory_order", "")).upper().strip(),
                    str(issue.get("factory_name", "")).strip(),
                    str(issue.get("sales_order_name", "")).strip(),
                    str(issue.get("reason", "")).strip(),
                    str(issue.get("suggested_order_id", "")).strip(),
                    str(issue.get("split_time", "")).strip(),
                    _now(),
                )
                for issue in issues
                if str(issue.get("ignore_key", issue.get("id", ""))).strip()
            ],
        )

    def aimes_review_rows(self) -> list[dict]:
        """读取当前 AIMES 待处理记录；无显式参数。"""
        rows = self.connection.execute(
            """
            select ignore_key, factory_order, factory_name, sales_order_name,
                   reason, suggested_order_id, split_time, last_seen
            from pending_aimes_reviews
            order by last_seen desc, factory_order
            """
        ).fetchall()
        return [
            {
                "id": row[0],
                "ignore_key": row[0],
                "factory_order": row[1],
                "factory_name": row[2],
                "sales_order_name": row[3],
                "reason": row[4],
                "suggested_order_id": row[5],
                "split_time": row[6],
                "last_seen": row[7],
            }
            for row in rows
        ]

    def aimes_review_row(self, ignore_key: str) -> dict | None:
        """按 ignore_key 查找一项 AIMES 待处理记录，未找到时返回 None。"""
        return next(
            (row for row in self.aimes_review_rows() if row["ignore_key"] == ignore_key),
            None,
        )

    def remove_aimes_review_row(self, ignore_key: str) -> None:
        """删除 ignore_key 对应的 AIMES 待处理记录，不在此提交事务。"""
        self.connection.execute(
            "delete from pending_aimes_reviews where ignore_key = ?",
            (ignore_key,),
        )

    def assign_aimes_factory(self, issue: dict, order_id: str) -> None:
        """保存人工订单归属并移除待处理项；issue 为问题记录，order_id 为指定订单号。"""
        self.connection.execute(
            """
            insert into aimes_order_assignments(
                ignore_key, factory_order, factory_name, original_sales_order_name,
                assigned_order_id, confirmed_at
            ) values(?,?,?,?,?,?)
            on conflict(ignore_key) do update set
                factory_order=excluded.factory_order,
                factory_name=excluded.factory_name,
                original_sales_order_name=excluded.original_sales_order_name,
                assigned_order_id=excluded.assigned_order_id,
                confirmed_at=excluded.confirmed_at
            """,
            (
                issue["ignore_key"],
                issue["factory_order"],
                issue["factory_name"],
                issue["sales_order_name"],
                order_id,
                _now(),
            ),
        )
        self.remove_aimes_review_row(issue["ignore_key"])

    def restore_aimes_assignment(self, ignore_key: str) -> None:
        """撤销 ignore_key 对应的人工归属，并删除该指定归属下的工厂单索引行。"""
        row = self.connection.execute(
            "select factory_order, assigned_order_id from aimes_order_assignments where ignore_key = ?",
            (ignore_key,),
        ).fetchone()
        self.connection.execute(
            "delete from aimes_order_assignments where ignore_key = ?",
            (ignore_key,),
        )
        if row is not None:
            self.connection.execute(
                "delete from factory_orders where factory_order = ? and order_id = ?",
                (row[0], row[1]),
            )

    def ignore_aimes_factory(self, issue: dict) -> None:
        """将问题记录 issue 标记为忽略，移除对应人工归属、工厂单索引及待处理项。"""
        self.connection.execute(
            "delete from aimes_order_assignments where ignore_key = ?",
            (issue["ignore_key"],),
        )
        self.connection.execute(
            """
            insert into ignored_aimes_factory_orders(
                ignore_key, factory_order, factory_name, sales_order_name, reason, ignored_at
            ) values(?,?,?,?,?,?)
            on conflict(ignore_key) do update set
                factory_order=excluded.factory_order,
                factory_name=excluded.factory_name,
                sales_order_name=excluded.sales_order_name,
                reason=excluded.reason,
                ignored_at=excluded.ignored_at
            """,
            (
                issue["ignore_key"],
                issue["factory_order"],
                issue["factory_name"],
                issue["sales_order_name"],
                issue["reason"],
                _now(),
            ),
        )
        if issue["factory_order"]:
            self.connection.execute(
                "delete from factory_orders where factory_order = ?",
                (issue["factory_order"],),
            )
        self.remove_aimes_review_row(issue["ignore_key"])

    def restore_aimes_factory(self, ignore_key: str) -> None:
        """取消身份键 ignore_key 的忽略标记，使后续同步可重新处理。"""
        self.connection.execute(
            "delete from ignored_aimes_factory_orders where ignore_key = ?",
            (ignore_key,),
        )

    def upsert_order(
        self,
        order_id: str,
        *,
        order_type: str | None = None,
        source_folder: str = "",
        source_folder_mtime: float | None = None,
        validation_status: str | None = None,
        stage: str | None = None,
        server_seen: str = "",
        aimes_seen: str = "",
        ) -> None:
        """新增或更新订单来源和阶段，已中止状态不被普通更新覆盖。

        参数：order_id 为订单号；order_type 为可选类型；source_folder 为来源目录；source_folder_mtime 为修改时间；
        validation_status 为可选临时校验结果；stage 为可选阶段；server_seen、aimes_seen 为两侧最近观察时间。"""
        order_id = order_id.upper()
        current = self.connection.execute("select stage,order_type from orders where order_id=?",(order_id,)).fetchone()
        self.connection.execute("""insert into orders(order_id,order_type,source_folder,source_folder_mtime,stage,last_server_seen,last_aimes_seen,updated_at)
            values(?,?,?,?,?,?,?,?) on conflict(order_id) do update set
            order_type=excluded.order_type,
            source_folder=case when excluded.source_folder<>'' then excluded.source_folder else orders.source_folder end,
            source_folder_mtime=coalesce(excluded.source_folder_mtime,orders.source_folder_mtime),
            stage=case when orders.stage='已中止' then orders.stage else excluded.stage end,
            last_server_seen=case when excluded.last_server_seen<>'' then excluded.last_server_seen else orders.last_server_seen end,
            last_aimes_seen=case when excluded.last_aimes_seen<>'' then excluded.last_aimes_seen else orders.last_aimes_seen end,
            updated_at=excluded.updated_at""",
            (order_id,order_type or (current[1] if current else _order_type(order_id)),source_folder,source_folder_mtime,
             stage or (current[0] if current else '已设计'),server_seen,aimes_seen,_now()))
        if validation_status is not None:
            self.set_validation(order_id, validation_status)

    def set_validation(self, order_id: str, status: str, message: str = "") -> None:
        """将本次校验结果写入 SQLite 临时表，不持久保存为业务事实。

        参数：order_id 为订单号；status 为校验状态；message 为说明。"""
        self.connection.execute("""insert into preview_validation(order_id,status,message) values(?,?,?)
            on conflict(order_id) do update set status=excluded.status,message=excluded.message""",
            (order_id,status,message))

    def server_scan_policy(self, order_id: str) -> dict | None:
        """读取 order_id 的 Server 扫描策略、身份指纹及观察截止时间。"""
        row = self.connection.execute(
            """
            select order_id, source_folder, server_scan_policy,
                   server_scan_aimes_fingerprint, server_scan_watch_until,
                   server_scan_policy_updated_at
            from orders where order_id = ?
            """,
            (str(order_id or "").upper().strip(),),
        ).fetchone()
        if row is None:
            return None
        return {
            "order_id": row[0],
            "source_folder": row[1],
            "policy": row[2],
            "aimes_fingerprint": row[3],
            "watch_until": row[4],
            "updated_at": row[5],
        }

    def save_server_scan_policy(
        self,
        order_id: str,
        *,
        policy: str,
        aimes_fingerprint: str,
        watch_until: str = "",
        updated_at: str = "",
    ) -> None:
        """保存订单扫描策略。

        参数：order_id 为订单号；policy 为策略；aimes_fingerprint 为身份指纹；watch_until 为截止时间；updated_at 为更新时间。"""
        self.connection.execute(
            """
            update orders
            set server_scan_policy = ?,
                server_scan_aimes_fingerprint = ?,
                server_scan_watch_until = ?,
                server_scan_policy_updated_at = ?
            where order_id = ?
            """,
            (
                str(policy or "").strip(),
                str(aimes_fingerprint or "").strip(),
                str(watch_until or "").strip(),
                str(updated_at or _now()).strip(),
                str(order_id or "").upper().strip(),
            ),
        )

    def save_order_annotations(
        self,
        order_id: str,
        *,
        user_note: str,
        planned_days: list[dict[str, str]],
        actual_days: list[dict[str, str]],
    ) -> dict:
        """保存人工备注及计划、实际安装开始日期，每类最多一个日期。

        参数：order_id 为订单号；user_note 为备注；planned_days、actual_days 为计划及实际日期记录。
        Server 和 AIMES 的同步更新不触碰这些人工字段。"""
        order_id = str(order_id or "").strip().upper()
        if not order_id:
            raise ValueError("保存订单信息需要订单号")
        exists = self.connection.execute(
            "select 1 from orders where order_id = ?", (order_id,)
        ).fetchone()
        if exists is None:
            raise ValueError(f"找不到订单：{order_id}")

        normalized: dict[str, list[tuple[str, str]]] = {}
        for date_type, values in (("planned", planned_days), ("actual", actual_days)):
            if not isinstance(values, list):
                raise ValueError(f"{date_type} 安装日期格式不正确")
            if len(values) > 1:
                label = "计划" if date_type == "planned" else "实际"
                raise ValueError(f"{label}安装日期只能填写一个开始日期")
            rows: list[tuple[str, str]] = []
            seen_dates: set[str] = set()
            for value in values:
                if not isinstance(value, dict):
                    raise ValueError("安装日期明细格式不正确")
                install_date = str(value.get("date", "")).strip()
                installer = str(value.get("installer", "")).strip()
                try:
                    datetime.strptime(install_date, "%Y-%m-%d")
                except ValueError as exc:
                    raise ValueError(f"安装日期必须是 YYYY-MM-DD：{install_date}") from exc
                if install_date in seen_dates:
                    raise ValueError(f"{date_type} 安装日期重复：{install_date}")
                seen_dates.add(install_date)
                rows.append((install_date, installer))
            normalized[date_type] = sorted(rows)

        updated_at = _now()
        self.connection.execute(
            "update orders set user_note = ?, updated_at = ? where order_id = ?",
            (str(user_note or "").strip(), updated_at, order_id),
        )
        self.connection.execute(
            "delete from order_installation_days where order_id = ?", (order_id,)
        )
        self.connection.executemany(
            """
            insert into order_installation_days(
                order_id, date_type, install_date, installer, updated_at
            ) values(?,?,?,?,?)
            """,
            [
                (order_id, date_type, install_date, installer, updated_at)
                for date_type, rows in normalized.items()
                for install_date, installer in rows
            ],
        )
        self.connection.commit()
        summary = next(
            (item for item in self.summaries() if item["order_id"] == order_id),
            None,
        )
        if summary is None:
            summary = {
                "order_id": order_id,
                "user_note": str(user_note or "").strip(),
                "installation": {
                    date_type: {
                        "days": [
                            {"date": install_date, "installer": installer}
                            for install_date, installer in rows
                        ],
                        "start_date": rows[0][0] if rows else "",
                        "end_date": rows[-1][0] if rows else "",
                        "day_count": len(rows),
                    }
                    for date_type, rows in normalized.items()
                },
            }
        # SwiftUI 看板用此响应替换完整内存快照，因此返回完整摘要，避免保存一条订单备注后清空其他订单。
        return {"saved": True, "order": summary, "orders": self.summaries()}

    def upsert_factory(
        self,
        factory_order: str,
        *,
        order_id: str = "",
        factory_name: str = "",
        sales_order_name: str = "",
        split_time: str = "",
        name_source: str = "",
        source_folder: str = "",
        report_state: str | None = None,
        ownership_status: str | None = None,
        has_hardware: bool | None = None,
        optimized: bool | None = None,
        outbound_status: str | None = None,
        outbound_document: str | None = None,
        outbound_mode: str | None = None,
        outbound_fingerprint: str | None = None,
        server_seen: str = "",
        aimes_seen: str = "",
    ) -> None:
        """新增或更新工厂单身份、报表及业务状态，未提供的可选状态沿用现有值。

        参数：factory_order 为工厂单号；order_id 为归属；factory_name 为名称；sales_order_name 为销售单；
        split_time 为拆单时间；name_source 为名称来源；source_folder 为目录；report_state 为报表状态；
        ownership_status 为归属状态；has_hardware 为是否有五金；optimized 为优化标志；
        outbound_status、outbound_document、outbound_mode、outbound_fingerprint 为出库状态、单据、方式及指纹；
        server_seen、aimes_seen 为两侧最近观察时间。"""
        factory_order = factory_order.upper()
        current = self.connection.execute(
            """
            select report_state, ownership_status, has_hardware, (stage in ('已优化','已生产','已出货')) as optimized,
                   (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document, outbound_mode, outbound_fingerprint
            from factory_orders where factory_order = ?
            """,
            (factory_order,),
        ).fetchone()
        resolved_status = (
            report_state if report_state is not None
            else (current[0] if current else "未发现")
        )
        resolved_ownership = (
            ownership_status if ownership_status is not None
            else (current[1] if current else "待确认")
        )
        resolved_hardware = (
            has_hardware if has_hardware is not None
            else bool(current[2]) if current else False
        )
        resolved_optimized = (
            optimized if optimized is not None
            else bool(current[3]) if current else False
        )
        resolved_outbound_status = (
            outbound_status if outbound_status is not None
            else (current[4] if current else "未查询")
        )
        resolved_outbound_document = (
            outbound_document if outbound_document is not None
            else (current[5] if current else "")
        )
        resolved_outbound_mode = (
            outbound_mode if outbound_mode is not None
            else (current[6] if current else "")
        )
        resolved_outbound_fingerprint = (
            outbound_fingerprint if outbound_fingerprint is not None
            else (current[7] if current else "")
        )
        self.connection.execute(
            """
            insert into factory_orders(
                factory_order, order_id, factory_name, sales_order_name, split_time, name_source, source_folder,
                report_state, ownership_status, has_hardware, stage,
                outbound_document, outbound_mode, outbound_fingerprint, last_server_seen,
                last_aimes_seen, updated_at
            ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            on conflict(factory_order) do update set
                order_id=case when excluded.order_id <> '' then excluded.order_id else factory_orders.order_id end,
                factory_name=case when excluded.factory_name <> '' then excluded.factory_name else factory_orders.factory_name end,
                sales_order_name=case when excluded.sales_order_name <> '' then excluded.sales_order_name else factory_orders.sales_order_name end,
                split_time=case when excluded.split_time <> '' then excluded.split_time else factory_orders.split_time end,
                name_source=case when excluded.name_source <> '' then excluded.name_source else factory_orders.name_source end,
                source_folder=case when excluded.source_folder <> '' then excluded.source_folder else factory_orders.source_folder end,
                report_state=excluded.report_state,
                ownership_status=excluded.ownership_status,
                has_hardware=excluded.has_hardware,
                stage=case when factory_orders.production_record_id is not null and excluded.stage<>'已出货' then '已生产' else excluded.stage end,
                outbound_document=excluded.outbound_document,
                outbound_mode=excluded.outbound_mode,
                outbound_fingerprint=excluded.outbound_fingerprint,
                last_server_seen=case when excluded.last_server_seen <> '' then excluded.last_server_seen else factory_orders.last_server_seen end,
                last_aimes_seen=case when excluded.last_aimes_seen <> '' then excluded.last_aimes_seen else factory_orders.last_aimes_seen end,
                updated_at=excluded.updated_at
            """,
            (
                factory_order,
                order_id.upper(),
                factory_name,
                sales_order_name.upper(),
                split_time,
                name_source,
                source_folder,
                resolved_status,
                resolved_ownership,
                int(resolved_hardware),
                '已出货' if resolved_outbound_status=='已出库' else '已优化' if resolved_optimized else '已拆单',
                resolved_outbound_document,
                resolved_outbound_mode,
                resolved_outbound_fingerprint,
                server_seen,
                aimes_seen,
                _now(),
            ),
        )

    def upsert_aimes_factory(
        self,
        factory_order: str,
        *,
        order_id: str,
        factory_name: str,
        sales_order_name: str,
        split_time: str,
        seen_at: str,
    ) -> None:
        """更新 AIMES 管理的身份字段，保留 Server 派生状态。

        参数：factory_order 为工厂单号；order_id 为归属；factory_name 为名称；sales_order_name 为销售单；
        split_time 为拆单时间；seen_at 为观察时间。"""
        factory_order = factory_order.upper()
        self.connection.execute(
            """
            insert into factory_orders(
                factory_order, order_id, factory_name, sales_order_name, split_time,
                name_source, report_state, ownership_status, aimes_status,
                aimes_deleted_at, aimes_last_verified_at, last_aimes_seen, updated_at
            ) values(?,?,?,?,?,'AIMES','AIMES已发现','已确认','active','',?,?,?)
            on conflict(factory_order) do update set
                order_id=excluded.order_id,
                factory_name=excluded.factory_name,
                sales_order_name=excluded.sales_order_name,
                split_time=case
                    when excluded.split_time <> '' then excluded.split_time
                    else factory_orders.split_time
                end,
                name_source='AIMES',
                ownership_status='已确认',
                aimes_status='active',
                aimes_deleted_at='',
                aimes_last_verified_at=excluded.aimes_last_verified_at,
                last_aimes_seen=excluded.last_aimes_seen,
                updated_at=case
                    when factory_orders.order_id <> excluded.order_id
                      or factory_orders.factory_name <> excluded.factory_name
                      or factory_orders.sales_order_name <> excluded.sales_order_name
                      or factory_orders.split_time <> excluded.split_time
                      or factory_orders.name_source <> 'AIMES'
                    then excluded.updated_at
                    else factory_orders.updated_at
                end
            """,
            (
                factory_order,
                order_id.upper(),
                factory_name,
                sales_order_name.upper(),
                split_time,
                seen_at,
                seen_at,
                seen_at,
            ),
        )

    def mark_aimes_deleted(self, factory_orders: list[str], *, verified_at: str) -> int:
        """将核验删除的 AIMES 身份置为失效并保留审计信息。

        参数：factory_orders 为已核验缺失的工厂单号；verified_at 为核验时间。"""
        selected = sorted({str(value).upper().strip() for value in factory_orders if str(value).strip()})
        if not selected:
            return 0
        placeholders = ",".join("?" for _ in selected)
        cursor = self.connection.execute(
            f"""
            update factory_orders
            set aimes_status='deleted', aimes_deleted_at=?, aimes_last_verified_at=?, updated_at=?
            where factory_order in ({placeholders}) and aimes_status <> 'deleted'
            """,
            [verified_at, verified_at, verified_at, *selected],
        )
        self.connection.execute(
            f"""
            update pending_issues
            set status='resolved', resolved_at=?
            where status='open' and factory_order in ({placeholders})
            """,
            [verified_at, *selected],
        )
        for factory_order in selected:
            row = self.connection.execute(
                "select order_id from factory_orders where factory_order=?",
                (factory_order,),
            ).fetchone()
            self.add_change(
                severity="info",
                kind="aimes_deleted",
                order_id=str(row[0] or "") if row else "",
                factory_order=factory_order,
                message=f"AIMES 精确核验确认工厂单已删除：{factory_order}；保留数据库记录但不再参与业务处理",
                observed_at=verified_at,
            )
        return cursor.rowcount

    def upsert_source_file(
        self,
        path: Path,
        *,
        source_folder: Path,
        kind: str,
        order_id: str = "",
        factory_order: str = "",
        changed_at: str,
        metadata: dict | None = None,
    ) -> str:
        """更新来源文件元数据、身份及内容指纹。

        参数：path 为文件路径；source_folder 为所属目录；kind 为报表类型；order_id、factory_order 为归属；
        changed_at 为变化时间；metadata 为可选已读取元数据，省略时自行读取。"""
        if metadata is None:
            stat = path.stat()
            modified_at = float(_mtime_marker(stat))
            size = stat.st_size
        else:
            modified_at = float(metadata["modified_at"])
            size = int(metadata["size"])
        previous = self.connection.execute(
            """
            select modified_at, size, source_folder, kind, order_id, factory_order,
                   content_fingerprint
            from source_files where path = ?
            """,
            (str(path),),
        ).fetchone()
        # 目录修改时间属于文件系统记录，不代表业务资料变化；保留目录行用于发现、分组及删除检测，
        # 仅目录时间变化不推进业务基准，已识别工作簿仍按修改时间和大小检查。
        metadata_changed = (
            previous is None
            if kind == "folder"
            else previous is None or previous[:2] != (modified_at, size)
        )
        content_fingerprint = str(previous[6] if previous is not None else "")
        if kind != "folder" and metadata_changed:
            try:
                current_fingerprint = _file_content_fingerprint(path)
            except OSError:
                # 报表无法读取时仍保留为变化，让正常解析及错误流程提示用户修复。
                current_fingerprint = ""
                changed = True
            else:
                changed = previous is None or current_fingerprint != content_fingerprint
            content_fingerprint = current_fingerprint
        else:
            changed = metadata_changed
        identity_changed = previous is None or previous[2:4] != (str(source_folder), kind)
        if previous is not None:
            if order_id and not previous[4]:
                identity_changed = True
            if factory_order and not previous[5]:
                identity_changed = True
        if not changed and not identity_changed:
            # last_seen 仅用于诊断；来源未变时避免网络扫描触发 SQLite 更新，本次扫描范围和数量由扫描结果报告。
            return ""
        change_type = "added" if previous is None else ("modified" if changed else "")
        self.connection.execute(
            """
            insert into source_files(
                path, source_folder, kind, order_id, factory_order, modified_at, size,
                content_fingerprint, last_seen
            ) values(?,?,?,?,?,?,?,?,?)
            on conflict(path) do update set
                source_folder=excluded.source_folder,
                kind=excluded.kind,
                order_id=case when excluded.order_id <> '' then excluded.order_id else source_files.order_id end,
                factory_order=case when excluded.factory_order <> '' then excluded.factory_order else source_files.factory_order end,
                modified_at=excluded.modified_at,
                size=excluded.size,
                content_fingerprint=excluded.content_fingerprint,
                last_seen=excluded.last_seen
            """,
            (
                str(path), str(source_folder), kind, order_id.upper(), factory_order.upper(),
                modified_at, size, content_fingerprint, changed_at,
            ),
        )
        return change_type

    def add_change(
        self,
        *,
        severity: str,
        kind: str,
        message: str,
        order_id: str = "",
        factory_order: str = "",
        path: str = "",
        observed_at: str | None = None,
    ) -> None:
        """追加一条同步变化记录。

        参数：severity 为级别；kind 为变化类型；message 为说明；order_id、factory_order 为归属；path 为来源；observed_at 为观察时间。"""
        self.connection.execute(
            """
            insert into sync_changes(observed_at, severity, kind, order_id, factory_order, path, message)
            values(?,?,?,?,?,?,?)
            """,
            (observed_at or _now(), severity, kind, order_id.upper(), factory_order.upper(), path, message),
        )

    def upsert_active_issue(
        self,
        *,
        issue_key: str,
        kind: str,
        order_id: str = "",
        factory_order: str = "",
        path: str = "",
        message: str,
        seen_at: str | None = None,
    ) -> None:
        """按问题键新增或更新待处理项。

        参数：issue_key 为唯一键；kind 为类型；order_id、factory_order 为归属；path 为来源；message 为说明；seen_at 为观察时间。"""
        seen_at = seen_at or _now()
        self.connection.execute(
            """
            insert into pending_issues(
                issue_key, kind, order_id, factory_order, path, message,
                status, first_seen, last_seen, resolved_at
            ) values(?,?,?,?,?,?, 'open', ?, ?, '')
            on conflict(issue_key) do update set
                kind=excluded.kind,
                order_id=excluded.order_id,
                factory_order=excluded.factory_order,
                path=excluded.path,
                message=excluded.message,
                status='open',
                last_seen=excluded.last_seen,
                resolved_at=''
            """,
            (
                issue_key,
                kind,
                order_id.upper(),
                factory_order.upper(),
                path,
                message,
                seen_at,
                seen_at,
            ),
        )

    def active_issues(self) -> list[dict]:
        """读取未解决的待处理问题列表；无显式参数。"""
        rows = self.connection.execute(
            """
            select issue_key, kind, order_id, factory_order, path, message,
                   status, first_seen, last_seen, resolved_at
            from pending_issues
            where status = 'open'
            order by last_seen desc, issue_key
            """
        ).fetchall()
        from .inventory import pending_inventory_operations
        from .aicnc_import import enabled as aicnc_enabled
        maintenance = []
        if aicnc_enabled(self.connection):
            remaining = self.connection.execute("select count(*) from aicnc_legacy_watch where retired_at=''").fetchone()[0]
            dismissed = self.connection.execute("select value from aicnc_import_settings where key='cleanup_dismissed'").fetchone()
            if remaining == 0 and (not dismissed or dismissed[0] != '1'):
                maintenance = [dict(issue_key='aicnc_legacy_retired',kind='aicnc_legacy_retired',order_id='',factory_order='',path='',status='open',
                    message='旧版文件夹监控已全部结束，可以安排清理旧版监控代码及相关数据库结构',first_seen='',last_seen='',resolved_at='')]
        return [
            {
                "issue_key": row[0],
                "kind": row[1],
                "order_id": row[2],
                "factory_order": row[3],
                "path": row[4],
                "message": row[5],
                "status": row[6],
                "first_seen": row[7],
                "last_seen": row[8],
                "resolved_at": row[9],
            }
            for row in rows
        ] + maintenance + pending_inventory_operations(self.path, connection=self.connection)

    def delete_stale_factory_ownership_issues(self, initial_date: str) -> int:
        """删除早于 initial_date 的历史工厂单未解决归属问题，返回删除数量。"""
        rows = self.connection.execute(
            """
            select pending_issues.issue_key, pending_issues.factory_order,
                   coalesce(factory_orders.split_time, '')
            from pending_issues
            left join factory_orders
              on factory_orders.factory_order = pending_issues.factory_order
            where pending_issues.kind = 'factory_ownership'
              and pending_issues.status = 'open'
            """
        ).fetchall()
        stale_keys = [
            issue_key
            for issue_key, factory_order, split_time in rows
            if _factory_order_before_initial_date(factory_order, split_time, initial_date)
        ]
        if not stale_keys:
            return 0
        placeholders = ",".join("?" for _ in stale_keys)
        self.connection.execute(
            f"delete from pending_issues where issue_key in ({placeholders})",
            stale_keys,
        )
        return len(stale_keys)

    def resolve_active_issue(self, issue_key: str, *, resolved_at: str | None = None) -> None:
        """将 issue_key 对应的问题标为解决；resolved_at 为可选解决时间。"""
        self.connection.execute(
            "update pending_issues set status = 'resolved', resolved_at = ? where issue_key = ?",
            (resolved_at or _now(), issue_key),
        )

    def resolve_active_issues_not_in(
        self,
        issue_keys: set[str],
        *,
        scoped_folders: set[str] | None = None,
    ) -> None:
        """关闭已不在本次问题集合中的待处理项。

        参数：issue_keys 为仍有效的问题键；scoped_folders 为可选目录限制。"""
        scope_sql = ""
        scope_args: list[str] = []
        if scoped_folders is not None:
            if not scoped_folders:
                return
            clauses = []
            for folder in sorted(scoped_folders):
                clauses.append("(path = ? or path like ?)")
                scope_args.extend([folder, folder.rstrip("/") + "/%"])
            scope_sql = " and (" + " or ".join(clauses) + ")"
        if issue_keys:
            placeholders = ",".join("?" for _ in issue_keys)
            sql = f"update pending_issues set status = 'resolved', resolved_at = ? where status = 'open' and issue_key not in ({placeholders}){scope_sql}"
            self.connection.execute(sql, (_now(), *sorted(issue_keys), *scope_args))
        else:
            sql = f"update pending_issues set status = 'resolved', resolved_at = ? where status = 'open'{scope_sql}"
            self.connection.execute(sql, (_now(), *scope_args))

    def clear_server_folder_pending_records(self, folders: set[str]) -> None:
        """清理被排除目录的轻量扫描基准并关闭相关问题；folders 为目录路径集合。"""
        for folder in sorted(path.rstrip("/") for path in folders if path):
            prefix = folder + "/%"
            self.connection.execute(
                "delete from source_files where source_folder = ? or source_folder like ?",
                (folder, prefix),
            )
            self.connection.execute(
                """
                update pending_issues
                set status = 'resolved', resolved_at = ?
                where status = 'open' and (path = ? or path like ?)
                """,
                (_now(), folder, prefix),
            )

    def current_issue(self, issue_key: str) -> dict | None:
        """按 issue_key 查找当前未解决问题，未找到时返回 None。"""
        return next((issue for issue in self.active_issues() if issue["issue_key"] == issue_key), None)

    def update_source_file_identity(
        self,
        path: Path,
        *,
        order_id: str = "",
        factory_order: str = "",
    ) -> None:
        """更新已索引文件身份；path 为文件路径，order_id 为订单号，factory_order 为工厂单字段。"""
        self.connection.execute(
            "update source_files set order_id = ?, factory_order = ? where path = ?",
            (order_id.upper(), factory_order.upper(), str(path)),
        )
    def record_run(self, started: str, finished: str, *, aimes_attempted: bool, aimes_succeeded: bool,
                   aimes_count: int, server_folder_count: int, error: str = "") -> None:
        """记录一次同步运行结果。

        参数：started、finished 为起止时间；aimes_attempted、aimes_succeeded 为 AIMES 尝试及成功标志；
        aimes_count 为读取数量；server_folder_count 为扫描目录数；error 为可选错误说明。"""
        self.connection.execute(
            """
            insert into sync_runs(started_at, finished_at, aimes_attempted, aimes_succeeded, aimes_count, server_folder_count, error)
            values(?,?,?,?,?,?,?)
            """,
            (started, finished, int(aimes_attempted), int(aimes_succeeded), aimes_count, server_folder_count, error),
        )

    def commit(self) -> None:
        """提交当前数据库事务；无显式参数。"""
        self.connection.commit()

    def latest_sync(self) -> dict:
        """返回最近一次同步记录，尚无记录时返回 None；无显式参数。"""
        row = self.connection.execute(
            "select started_at, finished_at, aimes_attempted, aimes_succeeded, aimes_count, server_folder_count, error from sync_runs order by id desc limit 1"
        ).fetchone()
        if row is None:
            return {}
        return {
            "started_at": row[0],
            "finished_at": row[1],
            "aimes_attempted": bool(row[2]),
            "aimes_succeeded": bool(row[3]),
            "aimes_count": row[4],
            "server_folder_count": row[5],
            "error": row[6],
        }

    def has_successful_aimes_sync_on(self, day: str) -> bool:
        """检查日期 day 是否已有成功的 AIMES 同步记录。"""
        row = self.connection.execute(
            "select 1 from sync_runs where aimes_succeeded = 1 and finished_at like ? limit 1",
            (f"{day}%",),
        ).fetchone()
        return row is not None

    def latest_change_id(self) -> int:
        """返回最新同步变化编号，无记录时返回零；无显式参数。"""
        return int(self.connection.execute("select coalesce(max(id), 0) from sync_changes").fetchone()[0])

    def server_scan_xml_state(self) -> list[dict[str, object]]:
        """读取 Server XML 扫描基准记录；无显式参数。"""
        rows = self.connection.execute(
            """
            select path, source_folder, kind, order_id, modified_at, last_seen
            from server_scan_xml_state
            order by source_folder, path
            """
        ).fetchall()
        return [
            {
                "path": str(row[0] or ""),
                "source_folder": str(row[1] or ""),
                "kind": str(row[2] or ""),
                "order_id": str(row[3] or ""),
                "modified_at": int(row[4] or 0),
                "last_seen": str(row[5] or ""),
            }
            for row in rows
        ]

    def save_server_scan_xml_baseline(
        self,
        folders: Iterable[Path],
        entries: Iterable[dict[str, object]],
        *,
        observed_at: str,
    ) -> None:
        """仅替换明确完成扫描的目录基准。

        参数：folders 为完成目录；entries 为 XML 元数据条目；observed_at 为观察时间。"""
        normalized_folders = sorted({str(Path(folder)) for folder in folders if str(folder)})
        for folder in normalized_folders:
            self.connection.execute(
                "delete from server_scan_xml_state where source_folder = ?",
                (folder,),
            )
        for item in entries:
            kind = str(item.get("kind") or "")
            source_folder = str(item.get("source_folder") or "")
            path = str(item.get("path") or "")
            if kind not in SERVER_SCAN_XML_KINDS or not source_folder or not path:
                continue
            if source_folder not in normalized_folders:
                continue
            self.connection.execute(
                """
                insert into server_scan_xml_state(
                    path, source_folder, kind, order_id, modified_at, last_seen
                ) values(?,?,?,?,?,?)
                on conflict(path) do update set
                    source_folder=excluded.source_folder,
                    kind=excluded.kind,
                    order_id=excluded.order_id,
                    modified_at=excluded.modified_at,
                    last_seen=excluded.last_seen
                """,
                (
                    path,
                    source_folder,
                    kind,
                    str(item.get("order_id") or ""),
                    int(item.get("modified_at") or 0),
                    observed_at,
                ),
            )

    def latest_changes(self, limit: int = 20, after_id: int | None = None) -> list[dict]:
        """读取同步变化；limit 为最大数量，after_id 为可选的起始变化编号。"""
        if after_id is None:
            rows = self.connection.execute(
                "select id, observed_at, severity, kind, order_id, factory_order, path, message from sync_changes order by id desc limit ?",
                (limit,),
            ).fetchall()
        else:
            rows = self.connection.execute(
                "select id, observed_at, severity, kind, order_id, factory_order, path, message from sync_changes where id > ? order by id desc limit ?",
                (after_id, limit),
            ).fetchall()
        return [
            {
                "observed_at": row[1],
                "severity": row[2],
                "kind": row[3],
                "order_id": row[4],
                "factory_order": row[5],
                "path": row[6],
                "message": row[7],
            }
            for row in rows
        ]

    def summaries(self, *, persist: bool = True) -> list[dict]:
        """依据工厂单事实及安装安排组装订单看板摘要；persist 决定是否保存并提交派生阶段变化。"""
        orders = self.connection.execute(
            "select order_id, order_type, source_folder, source_folder_mtime, coalesce((select v.status from temp.preview_validation v where v.order_id=orders.order_id),'正常'), stage, case when exists(select 1 from material_items m where m.order_id=orders.order_id and m.quantity>0) then '板材 · 封边' else '待校验' end, last_server_seen, last_aimes_seen, updated_at, coalesce((select v.message from temp.preview_validation v where v.order_id=orders.order_id),''), user_note from orders order by order_id"
        ).fetchall()
        installation_rows = self.connection.execute(
            """
            select order_id, date_type, install_date, installer
            from order_installation_days
            order by order_id, date_type, install_date
            """
        ).fetchall()
        installation_by_order: dict[str, dict[str, list[dict[str, str]]]] = defaultdict(
            lambda: {"planned": [], "actual": []}
        )
        for installation_row in installation_rows:
            installation_by_order[installation_row[0]][installation_row[1]].append({
                "date": installation_row[2],
                "installer": installation_row[3],
            })
        factories = self.connection.execute(
            """select factory_order, order_id, factory_name, sales_order_name,
                      split_time, name_source, source_folder, report_state,
                      ownership_status, has_hardware, (stage in ('已优化','已生产','已出货')) as optimized, (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status,
                      outbound_document, outbound_mode, outbound_fingerprint, updated_at,
                      optimization_first_completed_at, optimization_latest_completed_at,
                      optimization_first_seen_at, optimization_latest_seen_at,
                      optimization_source_path, outbound_completed_at
               from factory_orders
               where aimes_status = 'active'
               order by factory_order"""
        ).fetchall()
        produced_rows = self.connection.execute(
            """select f.order_id, f.factory_order
               from factory_orders f
               join production_records b on b.batch_id=f.production_record_id
               where b.status='completed'
               group by f.order_id, f.factory_order"""
        ).fetchall() if self.connection.execute(
            "select 1 from sqlite_master where type='table' and name='production_records'"
        ).fetchone() else []
        produced_keys = {(str(row[0]).upper(), str(row[1]).upper()) for row in produced_rows}
        grouped: dict[str, list[dict]] = defaultdict(list)
        for row in factories:
            if not row[1]:
                continue
            grouped[row[1]].append({
                "factory_order": row[0],
                "order_id": row[1],
                "order_name": row[2],
                "sales_order_name": row[3],
                "split_time": row[4],
                "name_source": row[5],
                "source_folder": row[6],
                "report_state": row[7],
                "ownership_status": row[8],
                "has_hardware": bool(row[9]),
                "optimized": bool(row[10]),
                "outbound_status": row[11],
                "outbound_document": row[12],
                "outbound_mode": row[13],
                "outbound_fingerprint": row[14],
                "updated_at": row[15],
                "optimization_first_completed_at": row[16],
                "optimization_latest_completed_at": row[17],
                "optimization_first_seen_at": row[18],
                "optimization_latest_seen_at": row[19],
                "optimization_source_path": row[20],
                "outbound_completed_at": row[21],
                "produced": (str(row[1]).upper(), str(row[0]).upper()) in produced_keys,
            })
        result = []
        stage_changed = False
        for row in orders:
            order_id = row[0]
            is_temporary = row[1] == "temporary"
            if not _valid_aimes_order_id(order_id) and not is_temporary:
                continue
            if is_temporary:
                children = [
                    item for item in grouped.get(order_id, [])
                    if "test" not in item["order_name"].casefold()
                ]
            else:
                children = [
                    item for item in grouped.get(order_id, [])
                    if (
                        (
                            item["name_source"] == "AIMES"
                            and item["sales_order_name"] == order_id
                        )
                        or (
                            item["order_id"] == order_id
                            and item["ownership_status"] == "已确认"
                        )
                    )
                    and "test" not in item["order_name"].casefold()
                ]
            if not children and not is_temporary and row[5] != "已中止":
                continue
            children.sort(key=lambda item: (item["split_time"], item["factory_order"]), reverse=True)
            latest_split_time = max((item["split_time"] for item in children), default="")
            unresolved = [item for item in children if item["ownership_status"] != "已确认"]
            expected = len(children)
            optimized = sum(1 for item in children if item["optimized"] and item["ownership_status"] == "已确认")
            produced = sum(1 for item in children if item["produced"] and item["ownership_status"] == "已确认")
            shipped = sum(1 for item in children if item["outbound_status"] == "已出库")
            optimization_completed_at = (
                max((item["optimization_latest_completed_at"] for item in children), default="")
                if expected and optimized == expected
                else ""
            )
            completed_at = (
                max((item["outbound_completed_at"] for item in children), default="")
                if expected and shipped == expected
                else ""
            )
            if row[5] == "已中止":
                stage = "已中止"
            elif is_temporary:
                if expected and shipped == expected:
                    # 临时目录经人工处理后也可能表示已完成订单；以出库事实为最终状态，不因来源名称非标准而继续留在默认未完成列表。
                    stage = "已出货"
                else:
                    stage = "待人工处理"
            elif expected == 0:
                stage = "已设计"
            elif shipped == expected:
                stage = "已出货"
            elif optimized < expected:
                stage = "已拆单待优化" if optimized == 0 else "部分优化"
            elif shipped and produced < expected:
                stage = "部分生产，部分出货"
            elif shipped:
                stage = "部分出货"
            elif produced == expected:
                stage = "已生产"
            elif produced:
                stage = "部分生产"
            else:
                stage = "已优化"
            # 校验失败信息单独展示；普通订单保存由工厂单事实推导的业务阶段，使重启和直接数据库读取保持一致。
            if persist and row[5] != stage:
                self.connection.execute(
                    "update orders set stage = ?, updated_at = ? where order_id = ?",
                    (stage, _now(), order_id),
                )
                stage_changed = True
            result.append({
                "id": order_id,
                "order_id": order_id,
                "order_type": row[1],
                "source_folder": row[2],
                "modified_at": (
                    datetime.fromtimestamp(row[3]).isoformat(timespec="seconds")
                    if row[3]
                    else row[9] or row[7] or ""
                ),
                "validation_status": row[4],
                "validation_message": row[10],
                "user_note": row[11],
                "installation": {
                    date_type: {
                        "days": rows,
                        "start_date": rows[0]["date"] if rows else "",
                        "end_date": rows[-1]["date"] if rows else "",
                        "day_count": len(rows),
                    }
                    for date_type, rows in installation_by_order.get(
                        order_id, {"planned": [], "actual": []}
                    ).items()
                },
                "stage": stage,
                "material_status": row[6],
                "latest_split_time": latest_split_time,
                "optimization_completed_at": optimization_completed_at,
                "completed_at": completed_at,
                "factory_count": expected,
                "optimized_count": optimized,
                "produced_count": produced,
                "shipped_count": shipped,
                "optimization_progress": f"{optimized} / {expected}" if expected else "—",
                "production_progress": f"{produced} / {expected}" if expected else "—",
                "outbound_progress": f"{shipped} / {expected}" if expected else "—",
                "factories": children,
            })
        result.sort(
            key=lambda item: (bool(item["latest_split_time"]), item["latest_split_time"], item["order_id"]),
            reverse=True,
        )
        if stage_changed:
            self.connection.commit()
        return result


def _report_files(folder: Path) -> list[tuple[Path, str]]:
    """发现 folder 内的五金、板材和材料报表并标记类型，跳过临时工作簿。"""
    result = []
    for path in report_paths(folder):
        if path.name.startswith("~$"):
            continue
        lowered = path.name.lower()
        if is_fittings_report(path):
            result.append((path, "fittings"))
        elif "板材清单" in path.name:
            result.append((path, "board"))
        elif "material" in lowered and not lowered.startswith("panelmaterial"):
            result.append((path, "material"))
    return result


def _is_recut_material_source(path: Path) -> bool:
    """判断材料路径 path 是否位于补切目录范围。"""
    return any(
        part.casefold() == "recut" or part.casefold().endswith("-recut")
        for part in path.expanduser().resolve().parts[:-1]
    )


def _is_recut_server_report(path: Path, source_folder: Path) -> bool:
    """判断报表 path 是否属于 source_folder 内的嵌套补切目录。"""
    try:
        relative_parts = path.expanduser().resolve().relative_to(
            source_folder.expanduser().resolve()
        ).parts[:-1]
    except ValueError:
        return False
    return any(
        part.casefold() == "recut" or part.casefold().endswith("-recut")
        for part in relative_parts
    )


def _reconcile_authoritative_server_material_sources(
    store: "OrderIndexStore",
    folders_by_order: dict[str, set[str]],
) -> set[str]:
    """仅在存在完整等价替代来源时退役重复材料路径。

    参数：store 为索引库；folders_by_order 为订单到来源目录集合的映射。
    目录发现、工作簿缺失或解析失败都不能授权删除已确认事实；按订单比较完整来源，
    共享工作簿不得导致其他订单事实被删，数量变更仍由明确材料确认负责。"""
    removed_orders: set[str] = set()
    for raw_order_id, raw_folders in folders_by_order.items():
        order_id = str(raw_order_id or "").strip().upper()
        folders = sorted({str(folder) for folder in raw_folders if str(folder)})
        if not order_id or not folders:
            continue
        sources: dict[str, dict[str, float]] = defaultdict(dict)
        for path, code, quantity in store.connection.execute(
            "select source_path, product_code, sum(quantity) from material_items "
            "where order_id=? and source_type='aihouse' "
            "group by source_path, product_code", (order_id,),
        ):
            sources[str(path)][str(code)] = float(quantity)
        replacements = [
            values for path, values in sources.items()
            if _path_in_folders(path, folders) and any(q > 0 for q in values.values())
        ]
        for path, values in sources.items():
            if _path_in_folders(path, folders):
                continue
            if not any(
                values.keys() == replacement.keys()
                and all(abs(q - replacement[code]) <= MATERIAL_ALLOCATION_EPSILON
                        for code, q in values.items())
                for replacement in replacements
            ):
                continue
            store.connection.execute(
                "delete from material_items where order_id=? "
                "and source_type='aihouse' and source_path=?", (order_id, path),
            )
            store.connection.execute(
                "delete from server_material_allocations where order_id=? and source_path=?",
                (order_id, path),
            )
            # 只要仍有订单引用，就保留共享来源元数据。
            store.connection.execute(
                "delete from source_files where path=? "
                "and not exists (select 1 from material_items where source_path=?) "
                "and not exists (select 1 from server_material_allocations where source_path=?)",
                (path, path, path),
            )
            removed_orders.add(order_id)
    return removed_orders


def _hardware_report_paths(
    paths: Iterable[Path],
    source_folder: Path,
) -> list[Path]:
    """筛选五金候选报表；paths 为报表路径集合，source_folder 为接口保留的目录参数。

    每份报表均是候选，不能仅凭目录名决定五金范围。"""
    return sorted({Path(path) for path in paths}, key=lambda item: str(item).casefold())


def _selected_hardware_reports(source_rows: Iterable[tuple[str, str]]) -> dict:
    """根据来源选择规则返回工厂单对应报表；source_rows 为文件路径与所属目录的二元组集合。"""
    paths = [Path(path) for path, folder in source_rows if path and folder]
    selected, _, _, _ = select_latest_fittings(paths)
    return selected


def _selected_hardware_report_paths(source_rows: Iterable[tuple[str, str]]) -> set[str]:
    """返回最终所选五金报表的路径集合；source_rows 为文件路径与所属目录的二元组集合。"""
    return {str(source.path) for source in _selected_hardware_reports(source_rows).values()}


_OPTIMIZATION_ROOT_RELATIVE_PATHS = (
    ("Optimize file",),
    ("New Nesting", "Optimize file"),
    ("Auo-Label-CNC", "Optimize file"),
)

_OPTIMIZATION_MARKER_RELATIVE_PATHS = (
    ("Optimize file.xml",),
    ("nesting_result.xml",),
    ("layout file", "nesting_result.xml"),
    ("layout file 2", "nesting_result.xml"),
)


def _optimization_artifact_paths(folder: Path) -> tuple[list[Path], bool]:
    """在 folder 及其直接子目录的已知 AICNC 布局查找标记文件，不递归遍历全部输出。

    兼容现行 New Nesting 和旧 Auo-Label-CNC 布局，避免遍历网络目录中的 PNG、NC、CSV 文件。"""
    from .aicnc_import import OPTIMIZATION_RE
    scopes = [folder]
    scan_complete = True
    try:
        scopes.extend(
            sorted(
                (path for path in folder.iterdir() if not OPTIMIZATION_RE.fullmatch(path.name) and path.is_dir()),
                key=lambda path: str(path).casefold(),
            )
        )
    except OSError:
        scan_complete = False

    result: set[Path] = set()
    for scope in scopes:
        for root_relative in _OPTIMIZATION_ROOT_RELATIVE_PATHS:
            optimization_root = scope.joinpath(*root_relative)
            for marker_relative in _OPTIMIZATION_MARKER_RELATIVE_PATHS:
                marker = optimization_root.joinpath(*marker_relative)
                try:
                    if marker.is_file():
                        result.add(marker)
                except OSError:
                    scan_complete = False
    return sorted(result), scan_complete


def _optimization_artifacts(folder: Path) -> list[Path]:
    """返回 folder 已知布局中可识别的 CNC 优化产物。"""
    artifacts, _ = _optimization_artifact_paths(folder)
    return artifacts


def _optimization_result_artifacts(folder: Path) -> list[Path]:
    """返回 folder 内携带明确工厂单身份的 AICNC 排版结果文件。"""
    return [path for path in _optimization_artifacts(folder) if path.name.casefold() == "nesting_result.xml"]


def _optimization_result_artifacts_checked(folder: Path) -> tuple[list[Path], bool]:
    """返回 folder 的优化结果文件及固定路径发现是否成功完成的标志。"""
    artifacts, scan_complete = _optimization_artifact_paths(folder)
    return [
        path for path in artifacts
        if path.name.casefold() == "nesting_result.xml"
    ], scan_complete


def _server_optimization_monitor_files(folder: Path) -> list[tuple[Path, str]]:
    """返回 folder 中用于轻量变化监测的两类 XML 文件。"""
    result: list[tuple[Path, str]] = []
    for path in _optimization_artifacts(folder):
        kind = (
            "optimization_input"
            if path.name.casefold() == "optimize file.xml"
            else "optimization_result"
        )
        result.append((path, kind))
    return result


def _optimization_factory_orders(path: Path) -> set[str]:
    """流式读取 AICNC XML 文件 path 中的工厂单号，避免一次载入整个 XML。"""
    factory_orders: set[str] = set()
    for _, element in ET.iterparse(path, events=("start",)):
        factory_order = str(element.attrib.get("OrderID", "")).upper().strip()
        if FACTORY_RE.fullmatch(factory_order):
            factory_orders.add(factory_order)
        element.clear()
    return factory_orders


def _file_timestamp(value: float) -> str:
    """把秒级时间戳 value 转为本地时间文本；零值返回空字符串。"""
    return datetime.fromtimestamp(value).isoformat(timespec="seconds") if value else ""


def _canonical_source_folder(source_root: Path, folder_name: str) -> Path:
    """按文件系统实际大小写定位目录；source_root 为根目录，folder_name 为待找名称。

    避免大小写不敏感的文件系统与大小写敏感的 SQLite 路径键产生重复临时订单。"""
    root = source_root if source_root.is_absolute() else source_root.resolve()
    try:
        for candidate in root.iterdir():
            if candidate.is_dir() and candidate.name.casefold() == folder_name.casefold():
                return candidate
    except OSError:
        pass
    return root / folder_name


def _record_server_baseline(store: OrderIndexStore, folder: Path, *, order_id: str = "") -> None:
    """人工出库成功后记录当前 Server 元数据。

    参数：store 为索引库；folder 为处理目录；order_id 为可选归属订单号。"""
    observed_at = _now()
    store.upsert_source_file(
        folder,
        source_folder=folder,
        kind="folder",
        order_id=order_id,
        changed_at=observed_at,
    )
    for path, kind in _report_files(folder):
        store.upsert_source_file(
            path,
            source_folder=folder,
            kind=kind,
            order_id=order_id,
            changed_at=observed_at,
        )


def record_standard_outbound_baseline(config: Config, order_id: str) -> bool:
    """标准订单出库同步后登记当前来源报表基准；config 为配置，order_id 为订单号。"""
    store = OrderIndexStore(config.workflow_database)
    try:
        row = store.connection.execute(
            "select source_folder from orders where order_id = ?",
            (str(order_id).upper(),),
        ).fetchone()
        if not row or not row[0]:
            return False
        folder = Path(row[0])
        if not folder.is_dir():
            return False
        _record_server_baseline(store, folder, order_id=str(order_id).upper())
        store.commit()
        return True
    finally:
        store.close()


def _record_generated_material_baseline(
    store: OrderIndexStore,
    folder: Path,
    materials_path: Path,
    *,
    order_id: str = "",
) -> None:
    """登记 App 生成的材料文件，不同时确认其他来源变化。

    参数：store 为索引库；folder 为订单目录；materials_path 为生成文件；order_id 为可选订单号。"""
    # 保留调用方路径拼写，与目录枚举得到的快照一致；仅在此解析路径会把 /var 变成 /private/var，造成误报。
    folder = folder.expanduser()
    materials_path = materials_path.expanduser()
    if materials_path.parent != folder or not materials_path.is_file():
        raise RuleError(
            "server_baseline",
            f"无法登记 App 生成的 material：文件不在订单根目录或不存在：{materials_path}",
        )
    observed_at = _now()
    store.upsert_source_file(
        folder,
        source_folder=folder,
        kind="folder",
        order_id=order_id,
        changed_at=observed_at,
    )
    store.upsert_source_file(
        materials_path,
        source_folder=folder,
        kind="material",
        order_id=order_id,
        changed_at=observed_at,
    )


def _direct_report_files(folder: Path) -> list[tuple[Path, str]]:
    """只返回 folder 直属的可识别报表，不包括子目录中的文件。"""
    return [(path, kind) for path, kind in _report_files(folder) if path.parent == folder]


def _merge_candidate(candidates: dict[str, dict], factory_order: str, *, name: str = "", source: str,
                     order_id: str = "", sales_order_name: str = "", split_time: str = "",
                     folder: str = "", has_hardware: bool = False,
                     derive_order_from_name: bool = True, optimized: bool = False) -> None:
    """把工厂单来源信息合并到候选集合。

    参数：candidates 为候选字典；factory_order 为工厂单号；name 为名称；source 为来源标签；
    order_id 为订单号；sales_order_name 为销售单；split_time 为拆单时间；folder 为来源目录；
    has_hardware 为五金标志；derive_order_from_name 决定是否从名称推导订单；optimized 为优化标志。"""
    if not FACTORY_RE.fullmatch(factory_order or ""):
        return
    item = candidates.setdefault(factory_order.upper(), {
        "names": {},
        "orders": set(),
        "sales_orders": set(),
        "split_times": set(),
        "folders": set(),
        "has_hardware": False,
        "optimized": False,
    })
    if name:
        item["names"].setdefault(source, set()).add(name.strip())
        derived = _order_id_from_factory_name(name) if source != "aimes" and derive_order_from_name else ""
        if derived:
            item["orders"].add(derived)
    if sales_order_name:
        item["sales_orders"].add(sales_order_name.upper().strip())
    if split_time:
        item["split_times"].add(split_time)
    if order_id:
        item["orders"].add(order_id.upper())
    if folder:
        item["folders"].add(folder)
    item["has_hardware"] = item["has_hardware"] or has_hardware
    item["optimized"] = item["optimized"] or optimized


def _effective_factory_candidate(factory_order: str, candidate: dict) -> dict:
    """按来源优先级解析最终工厂单候选及冲突；factory_order 为单号，candidate 为已合并来源证据。"""
    aimes_names = sorted(candidate["names"].get("aimes", set()))
    exact_aimes_names = sorted(candidate["names"].get("aimes_exact", set()))
    server_names = sorted(candidate["names"].get("server", set()))
    factory_name = aimes_names[0] if aimes_names else (
        exact_aimes_names[0] if exact_aimes_names else (server_names[0] if server_names else "")
    )
    aimes_orders = {_valid_aimes_order_id(name) for name in candidate.get("sales_orders", set())}
    aimes_orders.discard("")
    if len(aimes_orders) == 1:
        # AIMES 是工厂单名称与归属的权威来源，过期或混合 Server 报表不能制造虚假的归属冲突。
        orders = aimes_orders
        ownership_status = "已确认"
    elif len(aimes_orders) > 1:
        orders = aimes_orders
        ownership_status = "归属冲突"
    else:
        orders = set(candidate["orders"])
        ownership_status = "已确认" if len(orders) == 1 else "待确认"
        if len(orders) > 1:
            ownership_status = "归属冲突"
    return {
        "factory_order": factory_order,
        "order_id": next(iter(orders)) if len(orders) == 1 else "",
        "factory_name": factory_name,
        "sales_order_name": next(iter(aimes_orders)) if len(aimes_orders) == 1 else "",
        "split_time": max(candidate.get("split_times", set()), default=""),
        "name_source": (
            "AIMES" if aimes_names or aimes_orders
            else ("AIMES精确查询" if exact_aimes_names else ("server_report" if server_names else "待获取"))
        ),
        "source_folder": sorted(candidate["folders"])[0] if candidate["folders"] else "",
        "ownership_status": ownership_status,
        "has_hardware": candidate["has_hardware"],
        "optimized": candidate["optimized"],
        "server_names": server_names,
        "aimes_names": aimes_names,
        "exact_aimes_names": exact_aimes_names,
    }


def _merge_cached_server_candidate(
    store: OrderIndexStore,
    candidates: dict[str, dict],
    path: Path,
    *,
    folder: Path,
    folder_order_ids: list[str],
    manual_folder: bool,
) -> bool:
    """复用未变化报表的已索引身份，返回是否成功复用。

    参数：store 为索引库；candidates 为候选集合；path 为报表；folder 为所属目录；
    folder_order_ids 为目录关联订单号；manual_folder 为人工目录标志。
    来源索引及工厂单表已有身份时无需重开工作簿，返回 False 时调用方回退到正常解析。"""
    row = store.connection.execute(
        "select order_id, factory_order, kind from source_files where path = ?",
        (str(path),),
    ).fetchone()
    if row is None or not row[1]:
        return False

    cached_factory_orders = [
        value.strip().upper()
        for value in str(row[1]).split(",")
        if FACTORY_RE.fullmatch(value.strip())
    ]
    if not cached_factory_orders:
        return False

    used = False
    for factory_order in cached_factory_orders:
        factory = store.connection.execute(
            """
            select order_id, factory_name, sales_order_name, split_time,
                   name_source, has_hardware, (stage in ('已优化','已生产','已出货')) as optimized, stage
            from factory_orders
            where factory_order = ? and aimes_status = 'active'
            """,
            (factory_order,),
        ).fetchone()
        if factory is None:
            continue
        cached_order_id = str(factory[0] or row[0] or "").upper()
        if not cached_order_id and len(folder_order_ids) == 1:
            cached_order_id = folder_order_ids[0].upper()
        name_source = str(factory[4] or "server_report")
        manual_locked = bool(
            current_report_context()
            and current_report_context().locked_decisions.get(factory_order, {}).get("handling") == "manual"
        )
        has_automatic_hardware = bool(store.connection.execute(
            "select 1 from hardware_items where factory_order=? and source_type='aicnc' limit 1",
            (factory_order,),
        ).fetchone())
        if (
            row[2] == "fittings"
            and not has_automatic_hardware
            and str(factory[7] or "") != "已出货"
            and not manual_locked
        ):
            # 未变化报表也要能修复“来源已索引但自动五金事实缺失”的中断状态；
            # 完整空报表会在正常解析后记录 row_count=0，人工处理则继续沿用锁定决定。
            return False
        candidate_source = {
            "AIMES": "aimes",
            "AIMES精确查询": "aimes_exact",
        }.get(name_source, "server")
        _merge_candidate(
            candidates,
            factory_order,
            name=str(factory[1] or ""),
            source=candidate_source,
            order_id=cached_order_id,
            sales_order_name=str(factory[2] or "") if candidate_source == "aimes" else "",
            split_time=str(factory[3] or "") if candidate_source == "aimes" else "",
            folder=str(folder),
            has_hardware=bool(factory[5]),
            derive_order_from_name=not manual_folder,
            optimized=bool(factory[6]),
        )
        used = True
    return used


def _confirmed_material_folders(store: OrderIndexStore, folders: list[Path]) -> list[Path]:
    """筛选已成功写入材料事实的目录；store 为索引库，folders 为候选目录列表。

    只有材料写入成功，才可建立业务 XML 基准。"""
    confirmed = {
        row[0] for row in store.connection.execute(
            """select distinct source_folder from orders
               where coalesce((select v.status from temp.preview_validation v where v.order_id=orders.order_id),'正常') = '正常' and exists (
                   select 1 from material_items
                   where material_items.order_id = orders.order_id and quantity > 0)
               and not exists (select 1 from factory_orders
                   where factory_orders.order_id = orders.order_id
                     and aimes_status = 'active' and (stage in ('已优化','已生产','已出货')) = 0)"""
        )
    }
    return [folder for folder in folders if str(folder) in confirmed]


def _refresh_cached_optimization_artifacts(
    store: OrderIndexStore,
    validation_rows: list[tuple[str, str]],
    *,
    timing_sink: list[dict[str, object]] | None = None,
) -> int:
    """只为材料已写入且校验通过的工厂单登记优化 XML 元数据。

    参数：store 为索引库；validation_rows 为校验目录与状态记录；timing_sink 为可选耗时收集列表。
    XML 的 OrderID 绑定工厂单；修改时间表示 AICNC 生成时间，创建时间可能只是复制到 Server 的时间，
    需同时保留这些时间和首次观察时间，不能把索引刷新时间当作业务发生时间。"""
    refreshed = 0
    for order_id, source_folder in validation_rows:
        folder = Path(source_folder)
        if not folder.is_dir():
            continue
        active_factory_orders = {
            str(row[0]).upper()
            for row in store.connection.execute(
                """
                select factory_order
                from factory_orders
                where order_id = ? and aimes_status = 'active' and ownership_status = '已确认' and (stage in ('已优化','已生产','已出货')) = 1
                  and exists (select 1 from material_items
                      where material_items.order_id = factory_orders.order_id and quantity > 0)
                """,
                (order_id,),
            ).fetchall()
        }
        if not active_factory_orders:
            continue
        observed_at = _now()
        artifacts, scan_complete = _optimization_result_artifacts_checked(folder)
        for artifact in artifacts:
            artifact_started = time.perf_counter()
            artifact_error = ""
            try:
                file_stat = artifact.stat()
            except OSError:
                scan_complete = False
                artifact_error = "文件无法读取"
                if timing_sink is not None:
                    timing_sink.append({
                        "source_folder": str(folder),
                        "path": str(artifact),
                        "kind": "optimization",
                        "duration_seconds": round(time.perf_counter() - artifact_started, 6),
                        "error": artifact_error,
                    })
                continue
            modified_at = float(file_stat.st_mtime)
            created_at = float(getattr(file_stat, "st_birthtime", 0) or 0)
            cached_factory_orders = {
                str(row[0]).upper()
                for row in store.connection.execute(
                    """
                    select factory_order from optimization_artifacts
                    where source_path=? and file_modified_at=? and size=?
                    """,
                    (str(artifact), modified_at, int(file_stat.st_size)),
                ).fetchall()
            }
            if cached_factory_orders:
                artifact_factory_orders = cached_factory_orders
                store.connection.execute(
                    """
                    update optimization_artifacts set last_seen_at=?
                    where source_path=? and file_modified_at=? and size=?
                    """,
                    (observed_at, str(artifact), modified_at, int(file_stat.st_size)),
                )
            else:
                try:
                    artifact_factory_orders = _optimization_factory_orders(artifact)
                except (OSError, ET.ParseError):
                    scan_complete = False
                    artifact_error = "XML 无法解析"
                    if timing_sink is not None:
                        timing_sink.append({
                            "source_folder": str(folder),
                            "path": str(artifact),
                            "kind": "optimization",
                            "duration_seconds": round(time.perf_counter() - artifact_started, 6),
                            "error": artifact_error,
                        })
                    continue
            for factory_order in sorted(artifact_factory_orders & active_factory_orders):
                store.connection.execute(
                    """
                    insert into optimization_artifacts(
                        source_path, order_id, factory_order, file_modified_at,
                        file_created_at, completed_at, copied_at, first_seen_at,
                        last_seen_at, size
                    ) values(?,?,?,?,?,?,?,?,?,?)
                    on conflict(source_path, file_modified_at, size, factory_order)
                    do update set last_seen_at=excluded.last_seen_at
                    """,
                    (
                        str(artifact), order_id, factory_order, modified_at,
                        created_at, _file_timestamp(modified_at),
                        _file_timestamp(created_at), observed_at, observed_at,
                        int(file_stat.st_size),
                    ),
                )
            if timing_sink is not None:
                timing_sink.append({
                    "source_folder": str(folder),
                    "path": str(artifact),
                    "kind": "optimization",
                    "duration_seconds": round(time.perf_counter() - artifact_started, 6),
                    "error": artifact_error,
                })
        # 材料校验已确定本次覆盖的工厂单状态，XML 时间只作为该写入的补充来源证据。
        if not scan_complete:
            continue
        for factory_order in sorted(active_factory_orders):
            evidence = store.connection.execute(
                """
                select min(completed_at), max(completed_at), min(first_seen_at),
                       max(last_seen_at)
                from optimization_artifacts
                where order_id=? and factory_order=?
                """,
                (order_id, factory_order),
            ).fetchone()
            latest_source = store.connection.execute(
                """
                select source_path
                from optimization_artifacts
                where order_id=? and factory_order=?
                order by completed_at desc, id desc limit 1
                """,
                (order_id, factory_order),
            ).fetchone()
            if not evidence or not evidence[1]:
                continue
            current = store.connection.execute(
                """
                select (stage in ('已优化','已生产','已出货')) as optimized, optimization_first_completed_at,
                       optimization_latest_completed_at, optimization_first_seen_at,
                       optimization_latest_seen_at, optimization_source_path
                from factory_orders where factory_order=?
                """,
                (factory_order,),
            ).fetchone()
            desired = (
                1,
                str(evidence[0] or "") if evidence else "",
                str(evidence[1] or "") if evidence else "",
                str(evidence[2] or "") if evidence else "",
                str(evidence[3] or "") if evidence else "",
                str(latest_source[0]) if latest_source else "",
            )
            if current == desired:
                continue
            store.connection.execute(
                """
                update factory_orders set
                    stage=case when stage in ('已生产','已出货') then stage when ? then '已优化' else '已拆单' end,
                    optimization_first_completed_at=?,
                    optimization_latest_completed_at=?,
                    optimization_first_seen_at=?,
                    optimization_latest_seen_at=?,
                    optimization_source_path=?,
                    report_state=case when ? then '已发现' else report_state end,
                    updated_at=?
                where factory_order=? and order_id=?
                """,
                desired + (1, observed_at, factory_order, order_id),
            )
            refreshed += 1
    return refreshed


def _load_outbound_records(config: Config) -> list[dict]:
    """读取本地持久出库记录用于对账；config 提供已准备存储的数据库配置。"""
    if config.storage_prepared and config.workflow_database.is_file():
        connection = sqlite3.connect(config.workflow_database)
        try:
            if connection.execute("select 1 from sqlite_master where type='table' and name='outbound_documents'").fetchone():
                rows = connection.execute(
                    """
                    select od.document_number, od.document_type, od.order_id,
                           coalesce(odf.factory_order, od.factory_order) as matched_factory_order,
                           od.factory_order as document_remark,
                           od.status, od.source, od.issued_at, od.source_path,
                           od.document_url, od.items_json, od.raw_fingerprint,
                           od.mapped_fingerprint
                    from outbound_documents od
                    left join outbound_document_factories odf
                      on odf.document_number = od.document_number
                    where odf.id is not null
                       or not exists (
                           select 1 from outbound_document_factories existing
                           where existing.document_number = od.document_number
                       )
                    order by od.document_number, matched_factory_order
                    """
                ).fetchall()
                return [
                    {
                        "document_number": row[0],
                        "kind": row[1],
                        "order_id": row[2],
                        "factory_order": row[3],
                        "remark": row[3],
                        # remark 用于精确匹配工厂单状态；单据主行字段标识来源单据，例如仅关联一个工厂单的订单级材料单。
                        "document_remark": row[4],
                        "status": row[5],
                        "source": row[6],
                        "synced_at": row[7],
                        "source_path": row[8],
                        "document_url": row[9],
                        "items": json.loads(row[10] or "[]") if row[10] else [],
                        "raw_fingerprint": row[11],
                        "mapped_fingerprint": row[12],
                        "traveler_path": row[8],
                    }
                    for row in rows
                ]
        finally:
            connection.close()
    # 存储切换后不回退到 JSON；中央库缺失意味着没有可用的权威出库事实。
    return []


def _outbound_key(value: object) -> str:
    """移除出库身份 value 中的空白、下划线及连字符并统一大小写，生成比较键。"""
    return re.sub(r"[\s_-]+", "", str(value or "")).casefold()


def _outbound_exact_aliases(factory: dict) -> set[str]:
    """返回能够安全标识工厂单记录 factory 的精确身份别名。"""
    return {
        _outbound_key(factory.get("factory_name")),
        _outbound_key(factory.get("factory_order")),
    } - {""}


def _outbound_record_matches_factory(record: dict, factory: dict, *, allow_order_alias: bool) -> bool:
    """判断出库记录是否匹配工厂单。

    参数：record 为出库记录；factory 为工厂单；allow_order_alias 决定是否允许仅订单号的别名匹配。"""
    if _outbound_key(record.get("order_id")) != _outbound_key(factory.get("order_id")):
        return False
    remark = _outbound_key(record.get("remark"))
    if not remark:
        return False
    if remark in _outbound_exact_aliases(factory):
        return True
    if allow_order_alias and remark in {
        _outbound_key(factory.get("order_id")),
        _outbound_key(factory.get("sales_order_name")),
    }:
        return True
    return False


def _has_factory_hardware_outbound_record(
    factory: dict,
    records: Iterable[dict],
) -> bool:
    """判断工厂单是否存在对应的已出库五金单据；factory 为工厂单，records 为候选出库记录。"""
    return any(
        str(record.get("kind", "")).strip().casefold() == "hardware"
        and str(record.get("status", "")).strip() == "已出库"
        and _outbound_record_matches_factory(record, factory, allow_order_alias=False)
        for record in records
    )


def _factory_outbound_metadata(config: Config, factory: dict) -> tuple[str, str]:
    """取得工厂单的出库方式及指纹；config 为配置，factory 为工厂单记录。"""
    mode = str(factory.get("outbound_mode", "")).strip()
    fingerprint = str(factory.get("outbound_fingerprint", "")).strip()
    if mode or fingerprint:
        return mode, fingerprint
    factory_order = str(factory.get("factory_order", "")).strip().upper()
    if not factory_order or not config.workflow_database.is_file():
        return "", ""
    connection = sqlite3.connect(config.workflow_database)
    try:
        row = connection.execute(
            "select outbound_mode, outbound_fingerprint from factory_orders where factory_order=?",
            (factory_order,),
        ).fetchone()
    finally:
        connection.close()
    return (
        str(row[0] or "").strip(),
        str(row[1] or "").strip(),
    ) if row else ("", "")


def _refresh_outbound_status(
    config: Config,
    factory: dict,
    records: list[dict] | None = None,
    factory_group: list[dict] | None = None,
) -> tuple[str, str]:
    """根据本地出库审计记录计算状态，不查询或写入金蝶。

    参数：config 为配置；factory 为工厂单；records 为可选已有出库记录；factory_group 为可选同组工厂单。"""
    if not factory["order_id"] or not factory["factory_name"]:
        return "未查询", ""
    records = _load_outbound_records(config) if records is None else records
    outbound_mode, stored_fingerprint = _factory_outbound_metadata(config, factory)
    allow_order_alias = bool(factory_group and len(factory_group) == 1)
    production_document_numbers = {
        str(record.get("document_number", "")).strip()
        for record in records
        if str(record.get("kind", "")).strip().casefold() in {"production_materials", "rework_materials"}
        and str(record.get("document_number", "")).strip()
    }
    exact_records = []
    order_alias_records = []
    exact_aliases = _outbound_exact_aliases(factory)
    for record in records:
        if _outbound_key(record.get("order_id")) != _outbound_key(factory.get("order_id")):
            continue
        if (
            str(record.get("kind", "")).strip().casefold() in {"production_materials", "rework_materials"}
            or str(record.get("document_number", "")).strip() in production_document_numbers
        ):
            continue
        remark = _outbound_key(record.get("remark"))
        if remark in exact_aliases:
            exact_records.append(record)
        elif allow_order_alias and remark in {
            _outbound_key(factory.get("order_id")),
            _outbound_key(factory.get("sales_order_name")),
        }:
            order_alias_records.append(record)
    # 同时存在时优先使用工厂单五金出库单，避免较早的订单级材料单号遮蔽实际工厂单出库单。
    matching_records = exact_records + order_alias_records
    # 分单可能同时有关联的历史材料单和新五金单；已有五金出货证据后，只核对该工厂单的五金单，
    # 不能因历史材料单而把已成功出货状态判为过期。
    hardware_records = [
        record for record in matching_records
        if str(record.get("kind", "")).strip().casefold() == "hardware"
    ]
    if hardware_records:
        matching_records = hardware_records
        # 已确认的工厂单出货是不可被资料变化撤销的业务事实；当前来源差异另行审计。
        confirmed = [str(record.get("document_number", "")).strip()
                     for record in hardware_records
                     if record.get("status") == "已出库"
                     and str(record.get("factory_order", "")).strip().upper()
                         == str(factory.get("factory_order", "")).strip().upper()
                     and record.get("document_number")]
        if confirmed:
            return "已出库", "、".join(dict.fromkeys(confirmed))
    has_inventory_record = bool(matching_records)
    if outbound_mode == "customer_supplied" and not has_inventory_record:
        try:
            from .inventory import database_outbound_fingerprint

            current_fingerprint = database_outbound_fingerprint(
                config,
                str(factory.get("order_id", "")),
                str(factory.get("factory_order", "")),
            )
        except (OSError, KeyError, TypeError, ValueError, RuleError):
            return "需要更新", ""
        if stored_fingerprint and current_fingerprint != stored_fingerprint:
            return "需要更新", ""
        return "已出库", ""
    document_numbers = []
    for record in matching_records:
        if record.get("status") == "已出库":
            document_number = str(record.get("document_number", ""))
            recorded_raw = str(record.get("raw_fingerprint", ""))
            traveler_path = Path(str(record.get("traveler_path", ""))).expanduser()
            if recorded_raw and traveler_path.is_file():
                try:
                    from .inventory import InventorySyncStore, database_document_items, parse_traveler

                    record_remark = _outbound_key(
                        record.get("document_remark") or record.get("remark")
                    )
                    current_items = []
                    try:
                        _, documents, _, _ = database_document_items(
                            config,
                            str(factory.get("order_id", "")),
                            [str(factory.get("factory_order", ""))],
                        )
                        current_items = next(
                            (
                                items for remark, items in documents.items()
                                if _outbound_key(remark) == record_remark
                            ),
                            [],
                        )
                        has_database_document = any(
                            _outbound_key(remark) == record_remark
                            for remark in documents
                        )
                    except (OSError, KeyError, TypeError, ValueError, RuleError):
                        has_database_document = False
                    # 订单中心材料预览以中央 SQLite 为来源；单据不再存在时不能把数据库路径当作 Traveler 解析，
                    # 应作为来源变化或删除，以空明细进行比较。
                    if not has_database_document and _is_traveler_file(traveler_path):
                        traveler = parse_traveler(traveler_path)
                        current_items = next(
                            (
                                items for remark, items in traveler.documents.items()
                                if _outbound_key(remark) == record_remark
                            ),
                            [],
                        )
                    elif not has_database_document and not _is_traveler_file(traveler_path):
                        # 标准订单出库记录的 traveler_path 可能保存材料工作簿路径，其布局并非 Traveler；
                        # 没有对应数据库单据时，不能从不兼容的来源文件推断出库单已变化。
                        if document_number:
                            document_numbers.append(document_number)
                        continue
                    if InventorySyncStore.raw_document_fingerprint(current_items) != recorded_raw:
                        document_numbers.append(document_number)
                        return "需要更新", "、".join(filter(None, document_numbers))
                except (OSError, KeyError, TypeError, ValueError, RuleError):
                    # 当前 Traveler 无法读取时保留最后确认的已出货状态，库存流程重试时会报告具体读取错误。
                    pass
            if document_number:
                document_numbers.append(document_number)
    if document_numbers:
        return "已出库", "、".join(dict.fromkeys(document_numbers))
    return "未出库", ""


def assert_factory_orders_outbound_allowed(
    config: Config,
    order_id: str,
    factory_orders: Iterable[str],
    changed_factory_orders: Iterable[str] | None = None,
) -> None:
    """依据 SQLite 事实检查标准订单出库资格。

    参数：config 为配置；order_id 为订单号；factory_orders 为所选工厂单；changed_factory_orders 为明确允许更新的变化工厂单。
    已出货工厂单只有映射后的来源确实变化且调用方显式列入更新范围时，才允许继续。"""
    selected = sorted({str(value).upper().strip() for value in factory_orders if str(value).strip()})
    changed = {
        str(value).upper().strip()
        for value in (changed_factory_orders or [])
        if str(value).strip()
    }
    if not selected:
        return
    store = OrderIndexStore(config.workflow_database)
    try:
        # 先刷新派生状态，使变化后的 Traveler 或报表能够被识别，再检查出库资格。
        reconcile_outbound_statuses(config, store, factory_orders=selected)
        placeholders = ",".join("?" for _ in selected)
        rows = store.connection.execute(
            f"""
            select factory_order, order_id, case when stage='已出货' then '已出库' else '未出库' end as outbound_status, outbound_document
            from factory_orders
            where factory_order in ({placeholders})
            """,
            selected,
        ).fetchall()
        by_factory = {str(row[0]).upper(): row for row in rows}
        missing = [factory_order for factory_order in selected if factory_order not in by_factory]
        if missing:
            raise RuleError(
                "inventory_factory_unknown",
                "数据库中找不到所选工厂单，已停止出库：" + "、".join(missing),
                factory_orders=missing,
            )
        wrong_order = [
            factory_order for factory_order in selected
            if str(by_factory[factory_order][1]).upper() != str(order_id).upper()
        ]
        if wrong_order:
            raise RuleError(
                "inventory_factory_order_mismatch",
                "所选工厂单不属于当前订单，已停止出库：" + "、".join(wrong_order),
                factory_orders=wrong_order,
            )
        shipped = [
            (
                factory_order,
                str(by_factory[factory_order][3] or "").strip(),
            )
            for factory_order in selected
            if str(by_factory[factory_order][2] or "") == "已出库"
            and factory_order not in changed
        ]
        if shipped:
            detail = "、".join(
                f"{factory_order}（{document or '已有出库记录'}）"
                for factory_order, document in shipped
            )
            raise RuleError(
                "inventory_already_outbound",
                f"工厂单 {detail} 已出库，不能重复出库",
                factory_orders=[factory_order for factory_order, _ in shipped],
            )
    finally:
        store.close()


def reconcile_outbound_statuses(
    config: Config,
    store: OrderIndexStore | None = None,
    *, order_ids=None, factory_orders=None,
) -> int:
    """把成功的本地出库证据对账到工厂单状态。

    参数：config 为配置；store 为可选索引库；order_ids、factory_orders 为可选订单和工厂单范围。
    仅有订单号的出库记录只有在订单存在唯一工厂单时才能归属，避免将多个分单误标已出货。"""
    owns_store = store is None
    store = store or OrderIndexStore(config.workflow_database)
    records = _load_outbound_records(config)
    scope_sql = ''
    scope_args = []
    if order_ids is not None:
        values = sorted({str(x).strip().upper() for x in order_ids})
        scope_sql += ' and order_id in (' + ','.join('?' for _ in values) + ')'
        scope_args.extend(values)
    if factory_orders is not None:
        values = sorted({str(x).strip().upper() for x in factory_orders})
        # 保留同订单其他工厂单身份，用于判断旧的仅订单号单据是否有歧义。
        scope_sql += ' and order_id in (select order_id from factory_orders where factory_order in (' + ','.join('?' for _ in values) + '))'
        scope_args.extend(values)
    rows = store.connection.execute(
        """
        select factory_order, order_id, factory_name, sales_order_name,
               (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document, outbound_mode, outbound_fingerprint,
               outbound_completed_at
        from factory_orders
        where order_id <> '' and aimes_status = 'active'
        """ + scope_sql, scope_args
    ).fetchall()
    factories = [
        {
            "factory_order": row[0],
            "order_id": row[1],
            "factory_name": row[2],
            "sales_order_name": row[3],
            "outbound_status": row[4],
            "outbound_document": row[5],
            "outbound_mode": row[6],
            "outbound_fingerprint": row[7],
            "outbound_completed_at": row[8],
        }
        for row in rows
    ]
    by_order: dict[str, list[dict]] = defaultdict(list)
    for factory in factories:
        by_order[_outbound_key(factory["order_id"])].append(factory)

    selected_orders = None if order_ids is None else {str(x).strip().upper() for x in order_ids}
    selected_factories = None if factory_orders is None else {str(x).strip().upper() for x in factory_orders}
    affected = [factory for factory in factories
                if (selected_orders is None or factory['order_id'].upper() in selected_orders)
                and (selected_factories is None or factory['factory_order'].upper() in selected_factories)]
    updated = 0
    for factory in affected:
        audit_factory_hardware(store.connection, factory["factory_order"])
        order_factories = by_order.get(_outbound_key(factory["order_id"]), [])
        status, matched_document = _refresh_outbound_status(
            config,
            factory,
            records,
            factory_group=order_factories,
        )
        production_document_numbers = {
            str(record.get("document_number", "")).strip()
            for record in records
            if str(record.get("kind", "")).strip().casefold() in {"production_materials", "rework_materials"}
            and str(record.get("document_number", "")).strip()
        }
        stale_production_status = (
            status == "未出库"
            and str(factory.get("outbound_document", "")).strip() in production_document_numbers
        )
        # 历史迁移分别保留五金出货与旧合并材料单证据，不能让旧材料单覆盖已确认五金出货。
        legacy_production = store.connection.execute(
            """select 1 from factory_orders f
               join production_records b on b.batch_id=f.production_record_id
               where f.order_id=? and f.factory_order=?
                 and b.status='completed' and b.source='legacy-outbound-migration'
               limit 1""",
            (factory["order_id"], factory["factory_order"]),
        ).fetchone()
        if legacy_production and matched_document:
            status = "已出库"
        if status not in {"已出库", "需要更新"} and not stale_production_status:
            continue
        if (
            not matched_document
            and factory["outbound_mode"] != "customer_supplied"
            and not stale_production_status
        ):
            continue
        if stale_production_status:
            store.connection.execute(
                "delete from outbound_document_factories where document_number=?",
                (str(factory.get("outbound_document", "")).strip(),),
            )
        desired_status = status
        matched_times = [
            str(record.get("synced_at", "")).strip()
            for record in records
            if str(record.get("document_number", "")).strip() == matched_document
            and str(record.get("synced_at", "")).strip()
        ]
        desired_completed_at = (
            max(matched_times)
            if desired_status == "已出库" and matched_times
            else factory["outbound_completed_at"]
            if desired_status == "已出库"
            else ""
        )
        if (
            factory["outbound_status"] == desired_status
            and factory["outbound_document"] == matched_document
            and factory["outbound_completed_at"] == desired_completed_at
        ):
            continue
        store.connection.execute(
            """
            update factory_orders
            set stage = case when ?='已出库' then '已出货' when production_record_id is not null then '已生产' when stage<>'已拆单' then '已优化' else '已拆单' end, outbound_document = ?, outbound_mode = ?,
                outbound_fingerprint = ?, outbound_completed_at = ?, updated_at = ?
            where factory_order = ?
            """,
            (
                desired_status,
                matched_document,
                "" if stale_production_status else "inventory" if matched_document else factory["outbound_mode"],
                "" if matched_document or stale_production_status else factory["outbound_fingerprint"],
                desired_completed_at,
                _now(),
                factory["factory_order"],
            ),
        )
        updated += 1
    resolved_issues = _resolve_fully_shipped_server_issues(config, store, order_ids={f["order_id"] for f in affected})
    if updated or resolved_issues or store.connection.in_transaction:
        store.commit()
    if owns_store:
        store.close()
    return updated


def _orders_requiring_server_scan(
    config: Config,
    store: OrderIndexStore,
    aimes_rows: list[dict] | None = None,
) -> set[str]:
    """返回工厂单尚未全部出货的 AIMES 订单集合。

    参数：config 为配置；store 为索引库；aimes_rows 为可选新读取记录。
    新记录在内存合并，使刚拆出的工厂单在下一次索引写入前即可触发扫描。"""
    factories = _aimes_factory_records(store, aimes_rows)
    grouped: dict[str, list[dict]] = defaultdict(list)
    for factory in factories.values():
        grouped[factory["order_id"]].append(factory)
    records = _load_outbound_records(config) if config.reconcile_outbound_on_read else None
    result: set[str] = set()
    for order_id, items in grouped.items():
        if config.reconcile_outbound_on_read:
            statuses = {
                _refresh_outbound_status(config, item, records or [], factory_group=items)[0]
                for item in items
            }
        else:
            # 出库状态在库存操作成功的事务中维护，普通 AIMES/Server 扫描直接使用，不逐一重开历史单据证明。
            statuses = {str(item.get("outbound_status") or "未查询") for item in items}
        if not statuses or statuses != {"已出库"}:
            result.add(order_id)
    return result


def _aimes_factory_records(
    store: OrderIndexStore,
    aimes_rows: list[dict] | None = None,
) -> dict[str, dict]:
    """读取有效 AIMES 工厂单事实并合并可选新记录；store 为索引库，aimes_rows 为新记录。"""
    factories: dict[str, dict] = {}
    for row in store.connection.execute(
        """
        select factory_order, order_id, factory_name, sales_order_name,
               split_time, (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document, outbound_mode,
               outbound_fingerprint
        from factory_orders
        where name_source = 'AIMES' and aimes_status = 'active' and order_id <> ''
        """
    ).fetchall():
        factories[row[0]] = {
            "factory_order": row[0],
            "order_id": row[1],
            "factory_name": row[2],
            "sales_order_name": row[3],
            "split_time": row[4],
            "outbound_status": row[5],
            "outbound_document": row[6],
            "outbound_mode": row[7],
            "outbound_fingerprint": row[8],
        }
    for row in aimes_rows or []:
        factory_order = str(row.get("factory_order", "")).upper().strip()
        order_id = _valid_aimes_order_id(row.get("sales_order_name", ""))
        if not factory_order or not order_id:
            continue
        previous = factories.get(factory_order, {})
        factories[factory_order] = {
            "factory_order": factory_order,
            "order_id": order_id,
            "factory_name": str(row.get("factory_name", "")).strip() or previous.get("factory_name", ""),
            "sales_order_name": order_id,
            "split_time": str(row.get("split_time", "")).strip() or previous.get("split_time", ""),
            "outbound_status": previous.get("outbound_status", "未查询"),
            "outbound_document": previous.get("outbound_document", ""),
            "outbound_mode": previous.get("outbound_mode", ""),
            "outbound_fingerprint": previous.get("outbound_fingerprint", ""),
        }

    return factories


def _server_order_scan_allowed(
    config: Config,
    store: OrderIndexStore,
    order_id: str,
    folder: Path,
    *,
    requires_scan: set[str],
    now: str,
) -> bool:
    """判断单个订单是否继续自动扫描。

    参数：config 为配置；store 为索引库；order_id 为订单号；folder 为来源目录；requires_scan 为必扫订单集合；now 为本次时间。"""
    normalized_order = str(order_id or "").upper().strip()
    if not normalized_order:
        return False
    if store.server_scan_policy(normalized_order) is None:
        store.upsert_order(
            normalized_order,
            order_type=_order_type(normalized_order),
            source_folder=str(folder),
        )
    existing = store.server_scan_policy(normalized_order) or {}
    fingerprint = _aimes_order_fingerprint(store, normalized_order)
    legacy = _order_is_before_initial_date(config, store, normalized_order, folder)
    fully_shipped = (
        _order_has_active_aimes_mapping(store, normalized_order)
        and normalized_order not in requires_scan
    )
    policy = str(existing.get("policy") or "").strip()
    if not policy:
        if legacy:
            policy = "legacy"
            watch_until = ""
        elif fully_shipped:
            policy = "watching"
            watch_until = _order_shipped_watch_until(store, normalized_order, now)
        else:
            policy = "active"
            watch_until = ""
        store.save_server_scan_policy(
            normalized_order,
            policy=policy,
            aimes_fingerprint=fingerprint,
            watch_until=watch_until,
            updated_at=now,
        )
        return policy not in {"legacy", "permanent"}

    if fingerprint != str(existing.get("aimes_fingerprint") or ""):
        # AIMES 身份变化本身触发扫描；目录实际扫描后才更新基准，失败或不可用的扫描不能消耗该变化。
        return True

    if policy in {"legacy", "permanent"}:
        return False
    if policy == "watching":
        try:
            if _datetime_timestamp(existing.get("watch_until", "")) <= _datetime_timestamp(now):
                store.save_server_scan_policy(
                    normalized_order,
                    policy="permanent",
                    aimes_fingerprint=fingerprint,
                    updated_at=now,
                )
                return False
        except (OSError, OverflowError, ValueError):
            # 观察截止时间缺失或无效时，保守地重新开始七天观察期。
            store.save_server_scan_policy(
                normalized_order,
                policy="watching",
                aimes_fingerprint=fingerprint,
                watch_until=_order_shipped_watch_until(store, normalized_order, now),
                updated_at=now,
            )
    return True


def _server_folder_scan_allowed(
    config: Config,
    store: OrderIndexStore,
    folder: Path,
    aimes_rows: list[dict] | None = None,
) -> bool:
    """应用历史订单及出货后七天扫描策略。

    参数：config 为配置；store 为索引库；folder 为候选目录；aimes_rows 为可选新读取记录。"""
    if _server_folder_is_ignored(store, folder):
        return False
    if _server_folder_handling_mode(store, folder, aimes_rows) in {"supplemental", "external_manual"}:
        return _temporary_folder_is_candidate(config, store, folder)
    order_ids = _server_folder_order_ids(folder)
    if not order_ids:
        return True
    requires_scan = _orders_requiring_server_scan(config, store, aimes_rows)
    now = _now()
    return any(
        _server_order_scan_allowed(
            config,
            store,
            order_id,
            folder,
            requires_scan=requires_scan,
            now=now,
        )
        for order_id in order_ids
    )


def _finalize_server_scan_policies(
    config: Config,
    store: OrderIndexStore,
    folders: Iterable[Path],
    scanned_at: str,
) -> None:
    """在对应目录扫描后提交 AIMES 策略基准。

    参数：config 为配置；store 为索引库；folders 为已扫目录；scanned_at 为扫描时间。"""
    requires_scan = _orders_requiring_server_scan(config, store)
    for folder in folders:
        if _server_folder_handling_mode(store, folder) in {"supplemental", "external_manual"}:
            continue
        order_ids = _server_folder_order_ids(folder)
        for order_id in order_ids:
            existing = store.server_scan_policy(order_id)
            if existing is None:
                continue
            fingerprint = _aimes_order_fingerprint(store, order_id)
            fingerprint_changed = fingerprint != str(existing.get("aimes_fingerprint") or "")
            legacy = _order_is_before_initial_date(config, store, order_id, folder)
            fully_shipped = (
                _order_has_active_aimes_mapping(store, order_id)
                and order_id not in requires_scan
            )
            if not fully_shipped:
                policy = "active"
                watch_until = ""
            elif legacy:
                policy = "legacy"
                watch_until = ""
            else:
                policy = "watching"
                watch_until = str(existing.get("watch_until") or "")
                if fingerprint_changed or not watch_until:
                    watch_until = _order_shipped_watch_until(store, order_id, scanned_at)
            store.save_server_scan_policy(
                order_id,
                policy=policy,
                aimes_fingerprint=fingerprint,
                watch_until=watch_until,
                updated_at=scanned_at,
            )


def _mark_initial_orders_shipped(config: Config, store: OrderIndexStore) -> int:
    """应用用户已确认的历史出货规则；config 提供初始日期，store 为索引库。"""
    updated = 0
    for root in _available_server_roots(config):
        try:
            folders = list(root.iterdir())
        except OSError:
            continue
        for folder in folders:
            if not folder.is_dir() or not _is_standard_order_folder(folder.name):
                continue
            if _order_type(folder.name) != _server_root_order_type(root):
                continue
            order_id = folder.name.upper()
            if not _order_is_before_initial_date(config, store, order_id, folder):
                continue
            now = _now()
            store.upsert_order(
                order_id,
                order_type=_order_type(order_id),
                source_folder=str(folder),
                stage="已出货",
            )
            stale_validation = store.connection.execute(
                "select coalesce((select v.status from temp.preview_validation v where v.order_id=orders.order_id),'正常') from orders where order_id = ?",
                (order_id,),
            ).fetchone()
            if stale_validation and stale_validation[0] == "数据异常":
                # 初始日期之前的历史目录不重新读取，材料校验保留待检查状态，但旧的缺报表错误不能覆盖用户确认的已出货阶段。
                store.set_validation(order_id, '待校验')
                store.add_change(
                    severity="info",
                    kind="historical_validation_reconciled",
                    order_id=order_id,
                    path=str(folder),
                    message=(
                        f"历史订单 {order_id} 已按初始日期规则跳过 Server 校验；"
                        "清理旧数据异常显示，材料状态保留为待校验"
                    ),
                    observed_at=now,
                )
            rows = store.connection.execute(
                """
                select factory_order, (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document, outbound_mode
                from factory_orders
                where order_id = ? or sales_order_name = ?
                """,
                (order_id, order_id),
            ).fetchall()
            for factory_order, status, document, mode in rows:
                if status == "已出库":
                    continue
                resolved_mode = mode or ("inventory" if document else "historical_initial_date")
                store.connection.execute(
                    """
                    update factory_orders
                    set stage = case when ?='已出库' then '已出货' when production_record_id is not null then '已生产' when stage<>'已拆单' then '已优化' else '已拆单' end, outbound_mode = ?, updated_at = ?
                    where factory_order = ?
                    """,
                    ("已出库", resolved_mode, now, factory_order),
                )
                updated += 1
                store.add_change(
                    severity="info",
                    kind="historical_outbound_confirmed",
                    order_id=order_id,
                    factory_order=factory_order,
                    path=str(folder),
                    message=f"按初始日期规则确认早期工厂单 {factory_order} 已出库；未写入虚构出库单号或日期",
                    observed_at=now,
                )
            store.save_server_scan_policy(
                order_id,
                policy="legacy",
                aimes_fingerprint=_aimes_order_fingerprint(store, order_id),
                updated_at=now,
            )
    if updated:
        store.commit()
    return updated


def _server_folder_order_ids(folder: Path) -> set[str]:
    """从标准或混合来源目录 folder 提取其代表的订单号。"""
    if _is_standard_order_folder(folder.name):
        return {folder.name.upper()}
    if _is_mixed_order_folder(folder):
        return set(_folder_order_ids(folder))
    return set()


def _server_folder_is_fully_shipped(
    config: Config,
    store: OrderIndexStore,
    folder: Path,
    aimes_rows: list[dict] | None = None,
) -> bool:
    """判断标准或混合目录内所有已知订单是否全部出货。

    参数：config 为配置；store 为索引库；folder 为来源目录；aimes_rows 为可选新记录。
    没有有效 AIMES 归属不能视作已出货；新发现工厂单可在本次同步中重新开启目录扫描。"""
    if _server_folder_handling_mode(store, folder, aimes_rows) in {"supplemental", "external_manual"}:
        return False
    order_ids = _server_folder_order_ids(folder)
    if not order_ids:
        return False
    factories = _aimes_factory_records(store, aimes_rows)
    mapped_order_ids = {
        str(factory.get("order_id") or "").upper()
        for factory in factories.values()
        if str(factory.get("order_id") or "").strip()
    }
    unmapped = order_ids - mapped_order_ids
    if unmapped:
        # 用户确认已出货的历史目录可长期不在普通 AIMES 映射中；后续 AIMES 身份变化会通过专用扫描策略重新开启观察。
        if not all(
            (store.server_scan_policy(order_id) or {}).get("policy") in {"legacy", "permanent"}
            for order_id in unmapped
        ):
            return False
    return not (order_ids & _orders_requiring_server_scan(config, store, aimes_rows))


def _server_folder_for_issue(issue_path: str) -> Path | None:
    """从问题路径 issue_path 向上定位所属标准或混合 Server 订单目录。"""
    path = Path(issue_path).expanduser()
    # 问题可能指向具体文件，也可能直接指向订单目录；向上定位时包含路径自身，使两者对应同一订单边界。
    for candidate in (path, path.parent, *path.parents):
        if candidate.is_dir() and (
            _is_standard_order_folder(candidate.name)
            or _is_mixed_order_folder(candidate)
        ):
            return candidate
    return None


def _resolve_fully_shipped_server_issues(
    config: Config,
    store: OrderIndexStore,
    *, order_ids=None,
) -> int:
    """关闭已全部出货目录中遗留的 Server 待处理项，保留历史变化记录。

    参数：config 为配置；store 为索引库；order_ids 为可选订单范围。
    全部出货后目录可能不再自动扫描，因此需主动关闭先前材料校验或五金来源选择的遗留问题。"""
    # 订单完全出货后仍可能残留校验错误，例如后续刷新中的短暂 AIMES 凭据错误。
    # 目录已退出自动扫描时需在此关闭过期待处理项，保留历史同步变化记录。
    resolvable_kinds = {
        "material_validation",
        "hardware_selection",
        "order_validation",
    }
    resolved = 0
    for issue in store.active_issues():
        if order_ids is not None and issue.get("order_id") not in order_ids:
            continue
        if issue.get("kind") not in resolvable_kinds or issue.get("status") != "open":
            continue
        folder = _server_folder_for_issue(str(issue.get("path") or ""))
        if folder is None:
            continue
        if not _server_folder_is_fully_shipped(config, store, folder):
            continue
        store.resolve_active_issue(str(issue.get("issue_key") or ""))
        resolved += 1
    return resolved


def _resolve_stale_produced_material_issues(
    store: OrderIndexStore,
) -> int:
    """关闭已完成生产后的过期材料问题；store 为索引库。

    保留历史变化记录；中央材料事实存在时恢复材料状态，新写入前仍须重新预览校验当前工作簿。"""
    issues = [
        issue for issue in store.active_issues()
        if issue.get("kind") == "material_validation"
        and issue.get("status") == "open"
    ]
    if not issues:
        return 0
    resolved = 0
    for issue in issues:
        folder = _server_folder_for_issue(str(issue.get("path") or ""))
        if folder is None:
            continue
        order_ids = sorted(_server_folder_order_ids(folder))
        if not order_ids:
            continue
        placeholders = ",".join("?" for _ in order_ids)
        factory_rows = store.connection.execute(
            f"""
            select order_id, factory_order
            from factory_orders
            where aimes_status = 'active' and order_id in ({placeholders})
            """,
            order_ids,
        ).fetchall()
        if not factory_rows:
            continue
        produced_rows = store.connection.execute(
            f"""
            select f.order_id, f.factory_order, max(b.production_time)
            from factory_orders f
            join production_records b on b.batch_id = f.production_record_id
            where b.status = 'completed' and f.order_id in ({placeholders})
            group by f.order_id, f.factory_order
            """,
            order_ids,
        ).fetchall()
        produced_by_factory = {
            (str(row[0]).upper(), str(row[1]).upper()): str(row[2] or "")
            for row in produced_rows
        }
        required_factories = {
            (str(row[0]).upper(), str(row[1]).upper()) for row in factory_rows
        }
        if not required_factories.issubset(produced_by_factory):
            continue
        production_times = [
            value for key, value in produced_by_factory.items()
            if key in required_factories and value
        ]
        if len(production_times) != len(required_factories):
            continue
        try:
            issue_seen = _datetime_timestamp(str(issue.get("last_seen") or ""))
            latest_production = max(_datetime_timestamp(value) for value in production_times)
        except (OSError, OverflowError, ValueError):
            continue
        if issue_seen <= latest_production:
            continue
        material_fact_rows = store.connection.execute(
            f"""
            select distinct order_id
            from material_items
            where order_id in ({placeholders})
            """,
            order_ids,
        ).fetchall()
        fact_orders = {str(row[0]).upper() for row in material_fact_rows}
        if not set(order_ids).issubset(fact_orders):
            continue
        store.resolve_active_issue(str(issue.get("issue_key") or ""))
        store.add_change(
            severity="info",
            kind="material_validation_reconciled",
            order_id=str(issue.get("order_id") or ""),
            message=(
                f"材料校验提示已关闭：订单 {str(issue.get('order_id') or '').upper()} "
                "已完成生产，保留历史记录；后续预览仍会校验当前 material 文件。"
            ),
            path=str(issue.get("path") or ""),
            observed_at=_now(),
        )
        store.connection.execute(
            f"""
            update orders
            set updated_at = ?
            where order_id in ({placeholders})
            """,
            [_now(), *order_ids],
        )
        resolved += 1
    return resolved


def _aimes_row_signature(rows: list[dict]) -> list[tuple[str, str, str, str]]:
    """为 AIMES 记录列表 rows 生成排序后的身份签名，供前后变化比较。"""
    return sorted(
        (
            row["factory_order"],
            row["factory_name"],
            row["sales_order_name"],
            row["split_time"],
        )
        for row in rows
    )


def _persist_valid_aimes_mapping(
    config: Config,
    rows: list[dict],
    warnings: list[dict],
    *,
    cached_rows: list[dict] | None = None,
) -> None:
    """仅持久保存校验有效的 AIMES 身份映射。

    参数：config 为配置；rows 为当前记录；warnings 为本次警告；cached_rows 为可选已有记录。
    无效记录只作为本次警告，不写来源缓存或名称缓存，避免错误销售单名称成为业务事实。"""
    # 在线接口只返回近期页面；本地身份缓存需累积保留，避免后续读取 50 条时让旧的有效身份消失。
    cached_rows = cached_rows if cached_rows is not None else load_aimes_order_cache(config)
    merged_rows = {
        str(row.get("factory_order", "")).upper().strip(): row
        for row in cached_rows
        if str(row.get("factory_order", "")).strip()
    }
    for warning in warnings:
        factory_order = str(warning.get("factory_order", "")).upper().strip()
        if factory_order:
            merged_rows.pop(factory_order, None)
    for row in rows:
        factory_order = str(row.get("factory_order", "")).upper().strip()
        if factory_order:
            merged_rows[factory_order] = row
    save_aimes_order_cache(config, list(merged_rows.values()))
    names = load_factory_name_cache(config)
    for warning in warnings:
        factory_order = str(warning.get("factory_order", "")).upper().strip()
        if factory_order:
            names.pop(factory_order, None)
    names.update(
        {
            str(row.get("factory_order", "")).upper().strip(): str(row.get("factory_name", "")).strip()
            for row in rows
            if str(row.get("factory_order", "")).strip() and str(row.get("factory_name", "")).strip()
        }
    )
    save_factory_name_cache(config, names)


def _active_aimes_factory_orders(store: OrderIndexStore) -> list[str]:
    """读取有资格精确核验的有效、未生产工厂单身份；store 为索引库。

    使用与看板一致的完成生产证据，近期窗口外仍以本地已完成生产事实为准。"""
    return [
        str(row[0]).upper()
        for row in store.connection.execute(
            """
            select factory_order
            from factory_orders
            where aimes_status='active'
              and factory_order like 'F%'
              and (order_id like 'PP%' or order_id like 'CS%')
              and not exists (
                  select 1
                  from factory_orders f
                  join production_records b on b.batch_id=f.production_record_id
                  where b.status='completed'
                    and upper(f.order_id)=upper(factory_orders.order_id)
                    and upper(f.factory_order)=upper(factory_orders.factory_order)
              )
            order by factory_order
            """
        ).fetchall()
        if str(row[0]).strip()
    ]


def _verify_missing_aimes_factories(
    config: Config,
    store: OrderIndexStore,
    fetched_rows: list[dict],
    *,
    verified_at: str,
    verification_result: dict | None = None,
) -> tuple[int, str]:
    """精确核验未出现在近期页面的本地有效未生产工厂单。

    参数：config 为配置；store 为索引库；fetched_rows 为近期记录；verified_at 为核验时间；verification_result 为可选已有核验结果。
    最近 50 条中缺失不等于删除，只有精确查询明确没有匹配记录才可转为失效审计状态。"""
    fetched = {
        str(row.get("factory_order", "")).upper().strip()
        for row in fetched_rows
        if str(row.get("factory_order", "")).strip()
    }
    candidates = [factory_order for factory_order in _active_aimes_factory_orders(store) if factory_order not in fetched]
    if not candidates:
        return 0, ""
    if verification_result is None:
        from .core import verify_aimes_factory_orders
        try:
            result = verify_aimes_factory_orders(config, candidates)
        except Exception as exc:
            return 0, str(exc)
    else:
        result = verification_result
    missing = [
        factory_order for factory_order in result["missing"]
        if factory_order in candidates
    ]
    return store.mark_aimes_deleted(missing, verified_at=verified_at), ""


@pending_check_session
def sync_aimes_index(config: Config, *, force: bool = False, if_needed: bool = False) -> dict:
    """仅刷新 AIMES 身份，不扫描或解析 Server 文件。

    参数：config 为配置；force 为强制刷新选项；if_needed 为按需同步选项。
    身份刷新与 Server 扫描分别记录证据，不能把身份变化误报为报表变化。"""
    from .core import refresh_aimes_recent_orders

    operation_started = time.perf_counter()
    started = _now()
    store = OrderIndexStore(config.workflow_database)
    today = date.today().isoformat()
    cached_source_rows = load_aimes_order_cache(config)
    cached_rows, _cached_issues = _partition_aimes_rows(
        cached_source_rows,
        store.ignored_aimes_keys(),
        store.aimes_assignments(),
    )
    persisted_issues = store.aimes_review_rows()
    already_succeeded_today = store.has_successful_aimes_sync_on(today)
    should_fetch = force or (if_needed and not already_succeeded_today)
    if not should_fetch:
        result = {
            "orders": store.summaries(),
            "aimes": {
                "attempted": False,
                "succeeded": already_succeeded_today,
                "skipped_today": already_succeeded_today,
                "changed": False,
                "count": len(cached_rows),
                "issue_count": 0,
                "warning_count": len(persisted_issues),
                "duration_seconds": round(time.perf_counter() - operation_started, 2),
                "error": "",
            },
            "aimes_issues": [],
            "aimes_warnings": persisted_issues,
            "ignored_aimes": store.ignored_aimes_factories(),
            "assigned_aimes": store.assigned_aimes_factories(),
            "database": str(store.path),
            "aimes_source_file": str(config.workflow_database),
            "operation_trace": {
                "aimes": _aimes_trace(
                    config,
                    source="cache",
                    rows=cached_source_rows,
                    wrote_cache=False,
                ),
            },
            "aimes_stage_durations": [],
        }
        store.close()
        return result

    fetch_stage_durations: list[dict[str, object]] = []
    verification_result: dict | None = None
    try:
        verification_candidates = _active_aimes_factory_orders(store)
        if verification_candidates:
            from .core import refresh_aimes_recent_orders_and_verify
            fetched, verification_result = refresh_aimes_recent_orders_and_verify(
                config,
                AIMES_BULK_FETCH_LIMIT,
                verification_candidates,
                timing_sink=fetch_stage_durations,
            )
            fetched = _merge_aimes_recent_and_verified_rows(
                fetched,
                verification_result,
                cached_rows=cached_source_rows,
            )
        else:
            fetched = refresh_aimes_recent_orders(
                config,
                AIMES_BULK_FETCH_LIMIT,
                persist=False,
                timing_sink=fetch_stage_durations,
            )
        rows, issues = _partition_aimes_rows(
            fetched,
            store.ignored_aimes_keys(),
            store.aimes_assignments(),
        )
    except Exception as exc:
        finished = _now()
        message = _business_aimes_message(exc)
        store.add_change(severity="error", kind="aimes", message=f"今日 AIMES 同步失败：{message}")
        store.record_run(
            started,
            finished,
            aimes_attempted=True,
            aimes_succeeded=False,
            aimes_count=len(cached_rows),
            server_folder_count=0,
            error=message,
        )
        store.commit()
        aimes_stage_durations = _flat_aimes_stage_durations(
            exc.context.get("aimes_timings", []) if isinstance(exc, RuleError) else []
        )
        result = {
            "orders": store.summaries(),
            "aimes": {
                "attempted": True,
                "succeeded": False,
                "skipped_today": False,
                "changed": False,
                "count": len(cached_rows),
                "issue_count": 0,
                "warning_count": len(persisted_issues),
                "duration_seconds": round(time.perf_counter() - operation_started, 2),
                "error": message,
            },
            "aimes_issues": [],
            "aimes_warnings": persisted_issues,
            "ignored_aimes": store.ignored_aimes_factories(),
            "assigned_aimes": store.assigned_aimes_factories(),
            "database": str(store.path),
            "aimes_source_file": str(config.workflow_database),
            "operation_trace": {
                "aimes": _aimes_trace(
                    config,
                    source="cache",
                    rows=cached_source_rows,
                    wrote_cache=False,
                    error=message,
                    elapsed_seconds=round(time.perf_counter() - operation_started, 2),
                    stage_durations=aimes_stage_durations,
                ),
            },
            "aimes_stage_durations": aimes_stage_durations,
        }
        store.close()
        return result

    changed = _aimes_row_signature(rows) != _aimes_row_signature(cached_rows)
    seen_at = _now()
    aimes_stage_durations = _flat_aimes_stage_durations(fetch_stage_durations)
    persist_started = time.perf_counter()
    _persist_valid_aimes_mapping(
        config,
        rows,
        issues,
        cached_rows=cached_rows,
    )
    for row in rows:
        store.upsert_order(row["sales_order_name"], aimes_seen=seen_at)
        store.upsert_aimes_factory(
            row["factory_order"],
            order_id=row["sales_order_name"],
            factory_name=row["factory_name"],
            sales_order_name=row["sales_order_name"],
            split_time=row["split_time"],
            seen_at=seen_at,
        )
    aimes_stage_durations.append({
        "stage": "mapping_write",
        "label": "写入有效映射和数据库",
        "duration_seconds": round(time.perf_counter() - persist_started, 6),
    })
    verify_started = time.perf_counter()
    deleted_count, deletion_check_error = _verify_missing_aimes_factories(
        config, store, fetched, verified_at=seen_at,
        verification_result=verification_result,
    )
    aimes_stage_durations.append({
        "stage": "deleted_verify",
        "label": "精确核验已删除工厂单",
        "duration_seconds": round(time.perf_counter() - verify_started, 6),
    })
    store.replace_aimes_review_rows(issues)
    audit_hardware_integrity(store.connection)
    finished = _now()
    elapsed_seconds = round(time.perf_counter() - operation_started, 6)
    aimes_stage_durations = _complete_aimes_stage_durations(
        aimes_stage_durations,
        elapsed_seconds,
    )
    store.record_run(
        started,
        finished,
        aimes_attempted=True,
        aimes_succeeded=True,
        aimes_count=len(rows),
        server_folder_count=0,
    )
    store.commit()
    result = {
        "orders": store.summaries(),
        "aimes": {
            "attempted": True,
            "succeeded": True,
            "skipped_today": False,
            "changed": changed,
            "count": len(rows),
            "issue_count": 0,
            "warning_count": len(issues),
            "duration_seconds": elapsed_seconds,
            "error": "",
            "deleted_count": deleted_count,
            "deletion_check_error": deletion_check_error,
        },
        "aimes_issues": [],
        "aimes_warnings": issues,
        "ignored_aimes": store.ignored_aimes_factories(),
        "assigned_aimes": store.assigned_aimes_factories(),
        "database": str(store.path),
        "aimes_source_file": str(config.workflow_database),
        "operation_trace": {
            "aimes": _aimes_trace(
                config,
                source="aimes",
                rows=fetched,
                wrote_cache=bool(fetched),
                warnings=issues,
                elapsed_seconds=elapsed_seconds,
                stage_durations=aimes_stage_durations,
            ),
        },
        "aimes_stage_durations": aimes_stage_durations,
    }
    store.close()
    return result


def _folder_name_order_ids(folder: Path) -> list[str]:
    """只从目录 folder 的名称提取订单引用，不打开报表，也不据此确定业务归属。"""
    return list(dict.fromkeys(match.group(1).upper() for match in ORDER_TOKEN_RE.finditer(folder.name)))


def _server_folder_handling_mode(
    store: OrderIndexStore, folder: Path, aimes_rows: list[dict] | None = None,
) -> str:
    """判断非标准目录的处理方式，外部加工保持独立，仅已知出货事实可证明补单。

    参数：store 为索引库；folder 为目录；aimes_rows 为可选新 AIMES 记录。未知订单或新增未出货工厂单不能证明补单。"""
    if _is_standard_order_folder(folder.name):
        return "standard"
    previous = store.temporary_order(str(folder)) or {}
    if previous.get("handling_mode") == "external_manual" or previous.get("processing_status") == "已人工处理":
        return "external_manual"
    order_ids = set(_folder_name_order_ids(folder))
    factories = _aimes_factory_records(store, aimes_rows)
    relevant = [row for row in factories.values() if row["order_id"] in order_ids]
    all_shipped = bool(order_ids) and {row["order_id"] for row in relevant} == order_ids and all(
        row.get("outbound_status") == "已出库" for row in relevant
    )
    known = store.connection.execute(
        "select 1 from source_files where source_folder=? limit 1", (str(folder),)
    ).fetchone()
    if all_shipped and (not known or previous.get("handling_mode") == "supplemental"):
        return "supplemental"
    return "mixed" if _is_mixed_order_folder(folder) else "temporary"


def _server_folder_is_ignored(store: OrderIndexStore, folder: Path) -> bool:
    """检查目录 folder 是否已有永久忽略决定；store 为索引库，不读取目录内容。"""
    return store.connection.execute(
        "select 1 from server_folder_ignores where path=?", (str(folder),)
    ).fetchone() is not None


def ignore_server_folder(config: Config, folder: Path) -> dict:
    """保存目录复核中的忽略决定，不声明外部业务完成；config 为配置，folder 为所选目录。"""
    roots = _available_server_roots(config)
    selected_resolved = folder.expanduser().resolve()
    root = next((root for root in roots if selected_resolved.parent == root.resolve()), None)
    if root is None or not selected_resolved.is_dir():
        raise ValueError("请选择 Server 根目录内的临时文件夹，不能选择根目录或内部子目录")
    selected = root / selected_resolved.name
    if _is_standard_order_folder(selected.name):
        raise ValueError("标准订单文件夹不能使用此忽略操作")
    path = str(selected)
    now = _now()
    store = OrderIndexStore(config.workflow_database)
    try:
        store.connection.execute("begin immediate")
        if _server_folder_handling_mode(store, selected) == "mixed" and _report_files(selected):
            raise ValueError("有报表的混单文件夹请核对预览，不能使用临时文件夹忽略")
        unchanged = _server_folder_is_ignored(store, selected)
        if not unchanged:
            store.connection.execute(
                "insert into server_folder_ignores(path, ignored_at) values(?,?)", (path, now)
            )
            store.add_change(severity="info", kind="server_folder_ignored", path=path,
                             message=f"已永久忽略文件夹 {selected.name}；不再观察或自动提醒", observed_at=now)
        for issue in store.active_issues():
            issue_path = str(issue.get("path") or "")
            if issue_path == path or issue_path.startswith(path + "/"):
                store.resolve_active_issue(issue["issue_key"], resolved_at=now)
        store.commit()
        return {"ok": True, "ignored_folder": path,
                "unchanged": unchanged, "current_issues": store.active_issues()}
    except Exception:
        store.connection.rollback()
        raise
    finally:
        store.close()


def _temporary_folder_is_candidate(config: Config, store: OrderIndexStore, folder: Path) -> bool:
    """选择符合时间或未处理条件的非标准目录；config 为配置，store 为索引库，folder 为候选目录。"""
    if _server_folder_is_ignored(store, folder):
        return False
    try:
        created_at = _folder_created_at(folder)
    except OSError:
        return False
    existing = store.temporary_order(str(folder))
    if existing and (existing.get("handling_mode") == "external_manual" or existing.get("processing_status") == "已人工处理"):
        policy = existing.get("server_scan_policy")
        if policy == "manual_pending":
            return True
        if policy == "permanent":
            return False
        deadline = existing.get("server_scan_watch_until", "")
        if deadline:
            if datetime.fromisoformat(deadline) <= datetime.now():
                store.connection.execute("update temporary_orders set server_scan_policy='permanent' where source_folder=?", (str(folder),))
                return False
            if not _temporary_xml_baseline_matches(store, folder):
                store.connection.execute("update temporary_orders set server_scan_policy='manual_pending' where source_folder=?", (str(folder),))
            return True
    baseline = _server_scan_baseline(config)

    # 旧的普通临时目录在递归枚举和指纹计算前先排除，以低成本日期检查保护网络目录扫描。
    if created_at < baseline and not existing:
        return False

    existing = store.temporary_order(str(folder))
    if existing and existing.get("outbound_status") == "已出库":
        # 已处理临时目录只观察轻量 XML 三天，与标准已出货订单类似，但期限更短；不再读取 Excel 报表。
        policy = str(existing.get("server_scan_policy") or "").strip()
        if policy == "permanent":
            return False
        marker_files = _server_optimization_monitor_files(folder)
        if not marker_files:
            # 没有任何受认可的 XML 标记时无法安全观察，沿用历史已出货处理，不递归读取工作簿。
            return False
        watch_until = str(existing.get("server_scan_watch_until") or "").strip()
        if not watch_until:
            processed_at = str(existing.get("processed_at") or "").strip()
            try:
                base = datetime.fromisoformat(processed_at)
            except (TypeError, ValueError):
                base = datetime.now()
            watch_until = (base + timedelta(days=TEMPORARY_SHIPPED_WATCH_DAYS)).isoformat(timespec="seconds")
            store.upsert_temporary_order(
                temporary_id=str(existing.get("temporary_id") or _temporary_order_id(folder)),
                folder_name=folder.name,
                source_folder=str(folder),
                folder_created_at=float(existing.get("folder_created_at") or 0),
                content_fingerprint=str(existing.get("content_fingerprint") or ""),
                server_scan_policy="watching",
                server_scan_watch_until=watch_until,
                server_scan_policy_updated_at=_now(),
                processing_status=str(existing.get("processing_status") or "Traveler 已生成"),
                outbound_status="已出库",
                last_error="",
            )
        try:
            if datetime.fromisoformat(watch_until) <= datetime.now():
                store.upsert_temporary_order(
                    temporary_id=str(existing.get("temporary_id") or _temporary_order_id(folder)),
                    folder_name=folder.name,
                    source_folder=str(folder),
                    folder_created_at=float(existing.get("folder_created_at") or 0),
                    content_fingerprint=str(existing.get("content_fingerprint") or ""),
                    server_scan_policy="permanent",
                    server_scan_watch_until=watch_until,
                    server_scan_policy_updated_at=_now(),
                    processing_status=str(existing.get("processing_status") or "Traveler 已生成"),
                    outbound_status="已出库",
                    last_error="",
                )
                return False
        except (TypeError, ValueError):
            return False
        if (existing.get("handling_mode") == "external_manual" or existing.get("processing_status") == "已人工处理") and not _temporary_xml_baseline_matches(store, folder):
            store.connection.execute(
                "update temporary_orders set server_scan_policy='manual_pending', updated_at=? where source_folder=?",
                (_now(), str(folder)),
            )
        return True

    if existing and existing.get("handling_mode") == "supplemental":
        return True
    recent_cutoff = max(
        time.time() - timedelta(days=30).total_seconds(),
        baseline,
    )
    processed = store.connection.execute(
        "select 1 from source_files where source_folder = ? limit 1",
        (str(folder),),
    ).fetchone() is not None
    return created_at >= recent_cutoff or not processed


def _temporary_folders_before_server_baseline(config: Config, root: Path) -> set[str]:
    """查找不应继续待处理的旧非标准目录；config 提供扫描基准，root 为来源根目录。"""
    baseline = _server_scan_baseline(config)
    stale: set[str] = set()
    try:
        folders = root.iterdir()
    except OSError:
        return stale
    for folder in folders:
        if not folder.is_dir() or _is_standard_order_folder(folder.name) or _is_mixed_order_folder(folder):
            continue
        try:
            if _folder_created_at(folder) < baseline:
                stale.add(str(folder))
        except OSError:
            continue
    return stale


def _clear_stale_server_pending_state(config: Config, store: OrderIndexStore) -> Path | None:
    """清除旧非标准目录的持久待处理状态；config 为配置，store 为索引库。"""
    roots = _available_server_roots(config)
    if not roots:
        return None
    stale_folders: set[str] = set()
    for root in roots:
        stale_folders.update(_temporary_folders_before_server_baseline(config, root))
    stale_folders = {path for path in stale_folders if not store.temporary_order(path)}
    if stale_folders:
        store.clear_server_folder_pending_records(stale_folders)
        store.commit()
    return roots[0]


def _folder_order_ids(folder: Path) -> list[str]:
    """从目录 folder 及其报表提取完整订单号集合。"""
    from .order_workflow import related_order_ids

    return list(dict.fromkeys(order_id.upper() for order_id in related_order_ids(folder) if order_id))


def _temporary_order_id(folder: Path) -> str:
    """根据来源目录 folder 生成稳定的临时订单内部标识。"""
    stat = folder.stat()
    identity = f"{folder.resolve()}\n{getattr(stat, 'st_ino', 0)}\n{_folder_created_at(folder):.6f}"
    return "TMP:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]


def _reconcile_temporary_order_projections(store: OrderIndexStore) -> int:
    """清除正式订单表中旧的临时目录投影；store 为索引库。

    临时和返工目录按来源路径保存在临时台账；旧投影可能覆盖正式订单类型和目录。
    有 AIMES 确认则保留正式订单，否则清除孤立投影，让临时任务只由待处理台账表示。"""
    rows = store.connection.execute(
        "select order_id, source_folder from orders where order_type = 'temporary' and stage <> '已中止'"
    ).fetchall()
    reconciled = 0
    for order_id, source_folder in rows:
        order_id = str(order_id or "").upper().strip()
        formal_sources = [
            str(row[0] or "")
            for row in store.connection.execute(
                """
                select source_folder
                from factory_orders
                where order_id = ? and aimes_status = 'active'
                  and name_source = 'AIMES' and sales_order_name = ?
                order by source_folder
                """,
                (order_id, order_id),
            ).fetchall()
            if str(row[0] or "")
        ]
        formal_source = next(
            (
                path for path in formal_sources
                if _is_standard_order_folder(Path(path).name)
            ),
            "",
        )
        if formal_sources:
            if not formal_source and _is_standard_order_folder(Path(str(source_folder)).name):
                formal_source = str(source_folder)
            store.connection.execute(
                """
                update orders
                set order_type = ?,
                    source_folder = case when ? <> '' then ? else source_folder end,
                    updated_at = ?
                where order_id = ?
                """,
                (_order_type(order_id), formal_source, formal_source, _now(), order_id),
            )
        else:
            store.connection.execute(
                "delete from order_installation_days where order_id = ?",
                (order_id,),
            )
            store.connection.execute("delete from orders where order_id = ?", (order_id,))
        reconciled += 1
    if reconciled:
        store.commit()
    return reconciled


def _temporary_folder_fingerprint(folder: Path) -> str:
    """计算目录 folder 相关工作簿的内容指纹，用于防止重复出库。"""
    entries = []
    for path in sorted(folder.rglob("*.xlsx"), key=lambda item: str(item).casefold()):
        if path.name.startswith("~$") or not path.is_file():
            continue
        # App 生成的材料工作簿是本次处理输出，不是新来源变化；否则下次扫描会对自己的输出安排重复出库。
        if path.parent == folder and path.stem.casefold().endswith(" materials"):
            continue
        digest = hashlib.sha256()
        with path.open("rb") as stream:
            for chunk in iter(lambda: stream.read(1024 * 1024), b""):
                digest.update(chunk)
        stat = path.stat()
        entries.append((str(path.relative_to(folder)), stat.st_size, digest.hexdigest()))
    return hashlib.sha256(json.dumps(entries, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def _temporary_xml_baseline_matches(store: OrderIndexStore, folder: Path) -> bool:
    """检查已处理临时目录是否仍符合 XML 基准；store 为索引库，folder 为目录。"""
    current = {
        str(item.get("path") or ""): int(item.get("modified_at") or 0)
        for item in _server_scan_xml_entries([folder])
        if str(item.get("path") or "")
    }
    previous = {
        str(row[0] or ""): int(row[1] or 0)
        for row in store.connection.execute(
            "select path, modified_at from server_scan_xml_state where source_folder = ?",
            (str(folder),),
        ).fetchall()
    }
    return bool(current) and current == previous


def _temporary_aimes_match(store: OrderIndexStore, folder: Path) -> dict | None:
    """把非标准目录 folder 的名称匹配到唯一 AIMES 工厂单名称；store 为索引库。"""
    wanted = re.sub(r"[\s_-]+", "", folder.name).casefold()
    if not wanted:
        return None
    rows = store.connection.execute(
        """
        select factory_order, factory_name
        from factory_orders
        where name_source = 'AIMES'
          and aimes_status = 'active'
          and factory_name <> ''
        """
    ).fetchall()
    matches = {
        (str(factory_order).upper(), str(factory_name).strip())
        for factory_order, factory_name in rows
        if re.sub(r"[\s_-]+", "", str(factory_name)).casefold() == wanted
    }
    if len(matches) > 1:
        raise RuleError(
            "temporary_aimes_ambiguous",
            f"临时订单文件夹“{folder.name}”匹配到多个 AIMES 工厂单，请人工确认",
            matches=sorted({factory_order for factory_order, _ in matches}),
        )
    if not matches:
        return None
    factory_order, factory_name = next(iter(matches))
    return {"factory_order": factory_order, "factory_name": factory_name}


def _is_mixed_order_folder(folder: Path) -> bool:
    """判断非标准目录 folder 的名称是否包含两个订单号，即共享混合订单。

    轻量扫描只检查名称，报表内容留待批准后的流程解析。"""
    name_order_ids = {
        match.group(1).upper()
        for match in ORDER_TOKEN_RE.finditer(folder.name)
    }
    return (
        not _is_standard_order_folder(folder.name)
        and len(name_order_ids) >= 2
    )


def _temporary_folder_layout_error(folder: Path) -> str:
    """检查临时目录 folder 中处理必需的材料或板材工作簿，返回布局问题。

    门板、包装、CNC 等辅助 Excel 不是输入报表，不因其存在而阻止临时订单。"""
    files = [
        path for path in folder.rglob("*.xlsx")
        if path.is_file() and not path.name.startswith("~$")
    ]
    recognized = {path for path, _ in _report_files(folder)}
    if not recognized:
        return "临时订单文件夹中没有 material、板材清单或 Fittingslist Excel，请人工检查文件格式"
    if not any(kind in {"material", "board"} for _, kind in _report_files(folder)):
        return "临时订单文件夹中缺少 material 或板材清单，无法准备出库材料，请人工检查"
    return ""


def record_temporary_outbound(config: Config, traveler_path: Path, outbound: dict) -> None:
    """把成功人工出库镜像到临时订单台账；config 为配置，traveler_path 为关联文件，outbound 为出库结果。"""
    traveler_path = Path(traveler_path).resolve()
    folder_name = traveler_path.parent.name.strip()
    if not folder_name or _is_standard_order_folder(folder_name) or _is_mixed_order_folder(traveler_path.parent):
        return
    source_folder = _canonical_source_folder(config.source_root, folder_name)
    if not source_folder.is_dir():
        return
    documents = sorted({
        str(item.get("documentNumber", "")).strip()
        for item in outbound.get("results", [])
        if str(item.get("documentNumber", "")).strip()
    })
    store = OrderIndexStore(config.workflow_database)
    previous = store.temporary_order(str(source_folder)) or {}
    processed_at = previous.get("processed_at", "") or _now()
    watch_until = ""
    if _server_optimization_monitor_files(source_folder):
        watch_until = (
            datetime.fromisoformat(processed_at)
            + timedelta(days=TEMPORARY_SHIPPED_WATCH_DAYS)
        ).isoformat(timespec="seconds")
    outbound_at = _now()
    store.upsert_temporary_order(
        temporary_id=previous.get("temporary_id") or _temporary_order_id(source_folder),
        folder_name=source_folder.name,
        source_folder=str(source_folder),
        folder_created_at=_folder_created_at(source_folder),
        content_fingerprint=_temporary_folder_fingerprint(source_folder),
        traveler_path=str(traveler_path),
        processing_status="Traveler 已生成",
        outbound_status="已出库",
        outbound_document="、".join(documents),
        processed_at=processed_at,
        outbound_at=outbound_at,
        last_error="",
        server_scan_policy="watching" if watch_until else "",
        server_scan_watch_until=watch_until,
        server_scan_policy_updated_at=outbound_at if watch_until else "",
    )
    _record_server_baseline(store, source_folder, order_id=source_folder.name.upper())
    store.save_server_scan_xml_baseline(
        [source_folder],
        _server_scan_xml_entries([source_folder]),
        observed_at=outbound_at,
    )
    store.resolve_active_issue(f"temporary_processing:{source_folder}")
    store.commit()
    store.close()


def mark_temporary_folder_manual(
    config: Config, folder: Path, *,
    reference_order_ids: list[str] | None = None,
    outbound_document: str = "",
) -> dict:
    """登记目录已在外部人工处理，不调用库存系统。

    参数：config 为配置；folder 为目录；reference_order_ids 为可选订单标签；outbound_document 为可选单据号。
    订单引用不改变归属或出货状态；相同报表与 XML 版本的重复登记保留原完成时间。"""
    roots = _available_server_roots(config)
    if not roots:
        from .order_workflow import resolve_source_root
        resolve_source_root(config.source_root)
        roots = _available_server_roots(config)
    selected_resolved = folder.expanduser().resolve()
    root = next((candidate for candidate in roots if _path_is_within(selected_resolved, candidate)), None)
    if not selected_resolved.is_dir() or root is None:
        raise ValueError("所选 Server 文件夹无法访问或不在 Server 根目录内")
    selected = root / selected_resolved.relative_to(root.resolve())
    if reference_order_ids is None:
        reference_order_ids = _folder_name_order_ids(selected)
    if not isinstance(reference_order_ids, list) or any(
        not isinstance(value, str) or not _is_standard_order_folder(value.strip().upper())
        for value in reference_order_ids
    ):
        raise ValueError("参考订单请填写 PP####、PP####-# 或 CS###；也可以全部留空")
    references = list(dict.fromkeys(value.strip().upper() for value in reference_order_ids))
    if not _server_optimization_monitor_files(selected):
        raise ValueError("该文件夹没有 Optimize file.xml 或 nesting_result.xml，无法建立三天 XML 观察基线")

    fingerprint = _temporary_folder_fingerprint(selected)
    xml_entries = _server_scan_xml_entries([selected])
    now = _now()
    store = OrderIndexStore(config.workflow_database)
    try:
        store.connection.execute("begin immediate")
        if _server_folder_handling_mode(store, selected) not in {"temporary", "supplemental", "external_manual"}:
            raise ValueError("已人工处理适用于普通临时文件夹或补单；补单要求相关订单全部出库且 AIMES 没有新增待处理工厂单")
        path = str(selected)
        previous = store.temporary_order(path) or {}
        same_revision = (
            previous.get("processing_status") == "已人工处理"
            and previous.get("outbound_status") == "已出库"
            and previous.get("content_fingerprint") == fingerprint
            and _temporary_xml_baseline_matches(store, selected)
        )
        watch_until = previous.get("server_scan_watch_until", "") if same_revision else (
            datetime.fromisoformat(now) + timedelta(days=TEMPORARY_SHIPPED_WATCH_DAYS)
        ).isoformat(timespec="seconds")
        policy = "permanent" if same_revision and previous.get("server_scan_policy") == "permanent" else "watching"
        store.upsert_temporary_order(
            temporary_id=previous.get("temporary_id") or _temporary_order_id(selected),
            folder_name=selected.name, source_folder=path,
            folder_created_at=_folder_created_at(selected), content_fingerprint=fingerprint,
            processing_status="已人工处理", outbound_status="已出库",
            processed_at=previous.get("processed_at", "") if same_revision else now,
            outbound_at=previous.get("outbound_at", "") if same_revision else now,
            last_error="", server_scan_policy=policy,
            server_scan_watch_until=watch_until,
            server_scan_policy_updated_at=previous.get("server_scan_policy_updated_at", "") if same_revision else now,
            handling_mode="external_manual", reference_order_ids=references,
        )
        # 这里有意使用空单据号，新版本不能继承旧外部单据。
        store.connection.execute(
            "update temporary_orders set outbound_document=? where source_folder=?",
            (outbound_document.strip(), path),
        )
        if not same_revision:
            _record_server_baseline(store, selected)
            store.save_server_scan_xml_baseline([selected], xml_entries, observed_at=now)
        for issue in store.active_issues():
            issue_path = str(issue.get("path") or "")
            if issue_path == path or issue_path.startswith(path + "/"):
                store.resolve_active_issue(issue["issue_key"], resolved_at=now)
        if not same_revision or references != previous.get("reference_order_ids", []) or outbound_document.strip() != previous.get("outbound_document", ""):
            store.add_change(
                severity="info", kind="temporary_manual_outbound_reconciled", path=path,
                message=(f"用户确认文件夹 {selected.name} 已在外部人工出库；"
                         f"参考订单：{'、'.join(references) or '无'}；"
                         f"外部单号：{outbound_document.strip() or '未填写'}；"
                         + ("保留本次完成时间及观察期限" if same_revision else "未来三天独立观察 XML")),
                observed_at=now,
            )
        store.commit()
        return {
            "ok": True, "temporary_manual_handled": path,
            "unchanged": same_revision, "reference_order_ids": references,
            "outbound_status": "已出库", "server_scan_policy": policy,
            "server_scan_watch_until": watch_until,
            "pending_server_changes": [], "current_issues": store.active_issues(),
        }
    except Exception:
        store.connection.rollback()
        raise
    finally:
        store.close()


def _temporary_order_ids(folder: Path) -> list[str]:
    """提取临时目录 folder 的订单号，无法提取时使用目录名作为标签。"""
    order_ids = _folder_order_ids(folder)
    # 临时目录可以没有 PP/CS 订单号；目录名作为用户可见身份，写入 Traveler、Usage List 和出库备注。
    return order_ids or [folder.name.strip()]


def _process_temporary_folder(
    config: Config,
    folder: Path,
    *,
    store: OrderIndexStore,
    include_hardware: bool = True,
) -> dict:
    """校验临时目录、准备 Traveler 并执行请求的临时出库。

    参数：config 为配置；folder 为目录；store 为索引库；include_hardware 决定是否包含五金。"""
    from .inventory import run_jdy
    from .order_workflow import (
        generate_material_from_reports,
        generate_order_traveler,
        find_existing_traveler,
        preview_order,
        update_order_traveler,
    )

    fingerprint = _temporary_folder_fingerprint(folder)
    existing_record = store.temporary_order(str(folder))
    if (
        existing_record
        and existing_record.get("outbound_status") == "已出库"
        and existing_record.get("content_fingerprint") == fingerprint
        and (
            not _server_optimization_monitor_files(folder)
            or _temporary_xml_baseline_matches(store, folder)
        )
    ):
        return {
            "folder": str(folder),
            "order_ids": [folder.name.strip()],
            "skipped": True,
            "reason": "文件内容没有变化，数据库已记录该临时订单出库成功",
            "outbound_document": existing_record.get("outbound_document", ""),
        }

    temporary_id = _temporary_order_id(folder)
    store.upsert_temporary_order(
        temporary_id=temporary_id,
        folder_name=folder.name,
        source_folder=str(folder),
        folder_created_at=_folder_created_at(folder),
        content_fingerprint=fingerprint,
        processing_status="处理中",
        outbound_status="出库状态未知" if existing_record else "未出库",
        last_error="",
    )
    layout_error = _temporary_folder_layout_error(folder)
    if layout_error:
        raise RuleError("temporary_folder_format", layout_error)

    order_ids = _temporary_order_ids(folder)
    processed: list[dict] = []
    for order_id in order_ids:
        stored_include_hardware = existing_record.get("traveler_include_hardware") if existing_record else None
        stored_traveler_path = Path(existing_record.get("traveler_path", "")) if existing_record and existing_record.get("traveler_path") else None
        reuse_traveler = bool(
            existing_record
            and existing_record.get("traveler_status") == "已生成"
            and existing_record.get("traveler_fingerprint") == fingerprint
            and stored_include_hardware is not None
            and bool(int(stored_include_hardware)) == include_hardware
            and stored_traveler_path is not None
            and stored_traveler_path.is_file()
        )
        if reuse_traveler:
            traveler = stored_traveler_path
            traveler_action = "reused"
        else:
            material_files = [
                path for path in folder.rglob("*.xlsx")
                if path.is_file()
                and not path.name.startswith("~$")
                and "material" in path.name.casefold()
                and not path.name.casefold().startswith("panelmaterial")
            ]
            exact_materials = [
                path for path in material_files
                if re.search(rf"(?<![A-Z0-9]){re.escape(order_id)}(?![A-Z0-9]|-\d)", path.stem, re.IGNORECASE)
            ]
            if not exact_materials:
                generic_materials = [
                    path for path in material_files
                    if not any(
                        re.search(rf"(?<![A-Z0-9]){re.escape(candidate)}(?![A-Z0-9]|-\d)", path.stem, re.IGNORECASE)
                        for candidate in order_ids
                    )
                ]
                if generic_materials and len(order_ids) > 1:
                    raise RuleError(
                        "material_assignment_required",
                        f"临时混单文件夹中的 material 文件无法唯一分配到 {order_id}，请人工确认",
                        files=[str(path) for path in generic_materials],
                    )
                if not material_files or not generic_materials:
                    generate_material_from_reports(folder, order_id)
            aimes_match = _temporary_aimes_match(store, folder)
            preview = preview_order(
                config,
                folder,
                order_id,
                include_hardware=include_hardware,
                temporary_factory_order=aimes_match["factory_order"] if aimes_match else "",
                temporary_factory_name=aimes_match["factory_name"] if aimes_match else folder.name,
                # 返工或补做由临时台账和待处理中心管理，其材料不能覆盖正式订单的中央材料和五金事实。
                persist_facts=False,
            )
            traveler = find_existing_traveler(config, order_id)
            if traveler is None:
                traveler = generate_order_traveler(config, preview)
                traveler_action = "created"
            else:
                traveler, backup = update_order_traveler(config, preview)
                traveler_action = "updated"
            store.upsert_temporary_order(
                temporary_id=temporary_id,
                folder_name=folder.name,
                source_folder=str(folder),
                folder_created_at=_folder_created_at(folder),
                content_fingerprint=fingerprint,
                traveler_path=str(traveler),
                traveler_fingerprint=fingerprint,
                traveler_include_hardware=include_hardware,
                traveler_status="已生成",
                traveler_generated_at=_now(),
                processing_status="Traveler 已生成",
                outbound_status="出库状态未知" if existing_record else "未出库",
                last_error="",
            )
        outbound = run_jdy(config, "outbound", traveler, confirm_save=True)
        if not outbound.get("saved"):
            raise RuleError("temporary_outbound_failed", f"{order_id} 出库未返回成功结果，请人工核对库存系统单据")
        documents = sorted({
            str(item.get("documentNumber", "")).strip()
            for item in outbound.get("results", [])
            if str(item.get("documentNumber", "")).strip()
        })
        traveler_path = str(traveler)
        processed_at = _now()
        watch_until = ""
        if _server_optimization_monitor_files(folder):
            watch_until = (
                datetime.fromisoformat(processed_at)
                + timedelta(days=TEMPORARY_SHIPPED_WATCH_DAYS)
            ).isoformat(timespec="seconds")
        store.upsert_temporary_order(
            temporary_id=temporary_id,
            folder_name=folder.name,
            source_folder=str(folder),
            folder_created_at=_folder_created_at(folder),
            content_fingerprint=fingerprint,
            traveler_path=traveler_path,
            traveler_fingerprint=fingerprint,
            traveler_include_hardware=include_hardware,
            traveler_status="已生成",
            traveler_generated_at=existing_record.get("traveler_generated_at", "") if existing_record else "",
            processing_status="Traveler 已生成",
            outbound_status="已出库",
            outbound_document="、".join(documents),
            processed_at=processed_at,
            outbound_at=processed_at,
            last_error="",
            server_scan_policy="watching" if watch_until else "",
            server_scan_watch_until=watch_until,
            server_scan_policy_updated_at=processed_at if watch_until else "",
        )
        processed.append({
            "order_id": order_id,
            "traveler": str(traveler),
            "traveler_action": traveler_action,
            "outbound": outbound,
            "outbound_document": "、".join(documents),
        })
    return {
        "folder": str(folder),
        "order_ids": order_ids,
        "processed": processed,
        "temporary_id": temporary_id,
        "skipped": False,
    }


def _server_snapshot_folder(
    folder: Path | tuple[Path, bool],
) -> tuple[dict[str, dict], dict[str, object]]:
    """只读建立单个来源目录快照，不访问 SQLite；folder 为目录或带扫描选项的目录二元组。"""
    xml_only = False
    if isinstance(folder, tuple):
        folder, xml_only = folder
    folder_started = time.perf_counter()
    is_order_folder = _is_standard_order_folder(folder.name)
    is_mixed_folder = _is_mixed_order_folder(folder)
    folder_order_ids = (
        _folder_order_ids(folder)
        if is_mixed_folder
        else ([folder.name.upper()] if is_order_folder else [])
    )
    # 标准 AICNC 目录用两类 XML 作为完整变化信号；临时和混合目录仍靠 Excel 报表发现或重试人工流程，保留报表元数据扫描。
    optimization_files = _server_optimization_monitor_files(folder)
    monitor_files = (
        optimization_files
        if is_order_folder or xml_only
        else _report_files(folder) + optimization_files
    )
    try:
        folder_stat = folder.stat()
    except OSError:
        return {}, {
            "source_folder": str(folder),
            "duration_seconds": round(time.perf_counter() - folder_started, 6),
            "files": [],
            "error": "文件夹无法读取",
        }
    manual_only = not (is_order_folder or is_mixed_folder)
    display_order_id = "、".join(folder_order_ids)
    snapshot = {
        str(folder): {
            "source_folder": str(folder),
            "kind": "folder",
            "order_id": display_order_id,
            "modified_at": float(_mtime_marker(folder_stat)),
            "size": folder_stat.st_size,
            "created_at": _path_created_at(folder, folder_stat),
            "manual_only": manual_only,
            "mixed_order": is_mixed_folder,
        }
    }
    file_timings: list[dict[str, object]] = []
    for path, kind in monitor_files:
        file_started = time.perf_counter()
        file_error = ""
        try:
            stat = path.stat()
        except OSError:
            file_error = "文件无法读取"
            file_timings.append({
                "path": str(path),
                "kind": kind,
                "duration_seconds": round(time.perf_counter() - file_started, 6),
                "error": file_error,
            })
            continue
        snapshot[str(path)] = {
            "source_folder": str(folder),
            "kind": kind,
            "order_id": display_order_id,
            "modified_at": float(_mtime_marker(stat)),
            "size": stat.st_size,
            "created_at": _path_created_at(path, stat),
            "manual_only": manual_only,
            "mixed_order": is_mixed_folder,
        }
        file_timings.append({
            "path": str(path),
            "kind": kind,
            "duration_seconds": round(time.perf_counter() - file_started, 6),
            "error": file_error,
        })
    return snapshot, {
        "source_folder": str(folder),
        # 显示给用户的目录处理耗时严格等于各文件耗时之和；目录取元数据、枚举和线程调度的墙钟耗时另存。
        "duration_seconds": round(
            sum(float(item.get("duration_seconds", 0) or 0) for item in file_timings),
            6,
        ),
        "wall_duration_seconds": round(time.perf_counter() - folder_started, 6),
        "unaccounted_seconds": round(
            max(
                0.0,
                (time.perf_counter() - folder_started)
                - sum(float(item.get("duration_seconds", 0) or 0) for item in file_timings),
            ),
            6,
        ),
        "files": file_timings,
        "error": "",
    }


def _server_snapshot(
    config: Config,
    store: OrderIndexStore,
    *,
    timing_sink: list[dict[str, object]] | None = None,
) -> tuple[Path, dict[str, dict]]:
    # 自动扫描使用持久化订单策略：历史单除 AIMES 变化外跳过，新全部出货订单观察七天。
    # 人工选择目录不走此快照路径，仍属于明确的手动处理请求。
    """汇总可扫描 Server 目录快照，并应用既有历史出货规则。

    参数：config 为配置；store 为索引库；timing_sink 为可选分阶段耗时收集列表。"""
    from .aicnc_import import enabled, legacy_snapshot
    if enabled(store.connection):
        return legacy_snapshot(config, store, timing_sink)
    _mark_initial_orders_shipped(config, store)
    roots = _available_server_roots(config)
    if not roots:
        from .order_workflow import resolve_source_root
        resolve_source_root(config.source_root)
    root = roots[0]
    folders = []
    for server_root in roots:
        for folder in sorted(server_root.iterdir(), key=lambda item: item.name.casefold()):
            if not folder.is_dir():
                continue
            if _server_folder_is_ignored(store, folder):
                continue
            mode = _server_folder_handling_mode(store, folder)
            if mode in {"temporary", "supplemental", "external_manual"}:
                if not _temporary_folder_is_candidate(config, store, folder):
                    continue
            elif mode == "standard":
                if _order_type(folder.name) != _server_root_order_type(server_root):
                    continue
                if not _server_folder_scan_allowed(config, store, folder):
                    continue
            elif not _server_folder_scan_allowed(config, store, folder):
                continue
            folders.append(folder)

    snapshot: dict[str, dict] = {}
    if not folders:
        return root, snapshot
    xml_only_folders = {
        str(folder)
        for folder in folders
        if not _is_standard_order_folder(folder.name)
        and (store.temporary_order(str(folder)) or {}).get("server_scan_policy") in {"watching", "manual_pending"}
    }
    scan_targets = [
        (folder, str(folder) in xml_only_folders)
        for folder in folders
    ]
    worker_count = min(SERVER_SNAPSHOT_MAX_WORKERS, len(scan_targets))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        for folder_snapshot, folder_timing in executor.map(_server_snapshot_folder, scan_targets):
            folder = Path(str(folder_timing["source_folder"]))
            mode = _server_folder_handling_mode(store, folder)
            previous = store.temporary_order(str(folder)) or {}
            references = previous.get("reference_order_ids", _folder_name_order_ids(folder))
            if mode == "supplemental" and not previous:
                store.upsert_temporary_order(
                    temporary_id=_temporary_order_id(folder), folder_name=folder.name,
                    source_folder=str(folder), folder_created_at=_folder_created_at(folder),
                    content_fingerprint="", processing_status="待人工处理",
                    handling_mode="supplemental", reference_order_ids=references,
                )
            for item in folder_snapshot.values():
                item["handling_mode"] = mode
                item["reference_order_ids"] = references
                if mode in {"supplemental", "external_manual"}:
                    item["manual_only"] = True
                    item["order_id"] = "、".join(references)
            snapshot.update(folder_snapshot)
            if timing_sink is not None:
                timing_sink.append(folder_timing)
    return root, snapshot


def _server_scan_xml_entries(folders: Iterable[Path]) -> list[dict[str, object]]:
    """读取已完成扫描目录 folders 中的 XML 标记元数据。"""
    entries: list[dict[str, object]] = []
    for folder in folders:
        snapshot, _ = _server_snapshot_folder((Path(folder), True))
        entries.extend(
            dict(item, path=path)
            for path, item in snapshot.items()
            if item.get("kind") in SERVER_SCAN_XML_KINDS
        )
    return entries


def _server_scan_snapshot_path(config: Config) -> Path:
    """返回配置 config 的状态目录中的扫描快照文件路径。"""
    return config.state_dir / SERVER_SCAN_SNAPSHOT_FILENAME


def _write_server_scan_snapshot(
    config: Config,
    *,
    root: Path,
    roots: list[Path],
    scanned_at: str,
    entries: dict[str, dict],
) -> Path:
    """保存只读扫描结果，供紧接的索引更新复用。

    参数：config 为配置；root 为主要根目录；roots 为全部根目录；scanned_at 为扫描时间；entries 为快照条目。"""
    path = _server_scan_snapshot_path(config)
    path.parent.mkdir(parents=True, exist_ok=True)
    draft = path.with_name(f".{path.name}.tmp")
    payload = {
        "root": str(root),
        "roots": [str(item) for item in roots],
        "scanned_at": scanned_at,
        "entries": entries,
    }
    draft.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
    os.replace(draft, path)
    return path


def _load_server_scan_snapshot(
    config: Config,
    snapshot_path: Path | None,
) -> tuple[Path, list[Path], dict[str, dict]] | None:
    """读取仍与当前来源根目录一致的快照；config 为配置，snapshot_path 为可选快照路径。"""
    if snapshot_path is None:
        return None
    try:
        payload = json.loads(snapshot_path.read_text(encoding="utf-8"))
        root = Path(str(payload["root"]))
        roots = [Path(str(item)) for item in payload["roots"]]
        entries = payload["entries"]
        if not isinstance(entries, dict) or not roots:
            return None
        if {str(item) for item in roots} != {str(item) for item in _available_server_roots(config)}:
            return None
        normalized = {
            str(path): item
            for path, item in entries.items()
            if isinstance(item, dict) and item.get("source_folder")
        }
        folders = sorted(
            {
                Path(path)
                for path, item in normalized.items()
                if item.get("kind") == "folder"
            },
            key=lambda item: (item.name.casefold(), str(item).casefold()),
        )
        return root, folders, normalized
    except (OSError, KeyError, TypeError, ValueError, json.JSONDecodeError):
        return None


def _server_change_message(change_type: str, item: dict, path: str) -> str:
    """生成来源变化的中文提示；change_type 为变化类型，item 为文件信息，path 为来源路径。"""
    if change_type == "missing_report":
        order_id = str(item.get("order_id") or "").strip()
        order_suffix = f"（订单 {order_id}）" if order_id else ""
        return (
            f"Server 混单文件夹缺少可识别的报表：{Path(path).name}{order_suffix}。"
            "请检查文件夹；确认有误时可选择忽略。"
        )
    action = {"added": "新增", "modified": "修改", "removed": "删除", "renamed": "改名"}[change_type]
    order_id = str(item.get("order_id") or "").strip()
    order_suffix = f"（订单 {order_id}）" if order_id else ""
    if item.get("mixed_order"):
        subject = "混单文件夹" if item["kind"] == "folder" else "混单报表"
        return f"Server {subject}{action}：{Path(path).name}{order_suffix}（路径：{path}）"
    if item.get("manual_only"):
        folder_name = Path(item.get("source_folder") or path).name
        if item["kind"] == "folder":
            return f"Server 临时订单文件夹{action}：{folder_name}{order_suffix}（路径：{path}），点击自动处理后将校验文件格式、准备材料并尝试出库"
        return f"Server 临时订单报表{action}：{Path(path).name}{order_suffix}（路径：{path}），点击自动处理后将校验并尝试出库"
    subject = (
        _source_file_data_label(item["kind"])
        if item["kind"] in SERVER_SCAN_XML_KINDS
        else ("订单文件夹" if item["kind"] == "folder" else "报表")
    )
    return f"Server {subject}{action}：{Path(path).name}{order_suffix}（路径：{path}）"


def _server_folder_rename_pairs(previous: dict[str, dict], current: dict[str, dict]) -> list[tuple[str, str]]:
    """保守匹配前后快照中改名的目录；previous 为原快照，current 为当前快照。

    仅接受同一父目录、非空且完全相同的报表元数据、同一订单身份且唯一的候选；
    有歧义或内容变化时仍作为普通新增和删除处理。"""
    def folders(entries: dict[str, dict], previous_entries: bool) -> dict[str, set[str]]:
        """按目录收集报表相对路径和元数据签名；entries 为快照，previous_entries 为当前未使用的保留参数。"""
        result: dict[str, set[str]] = {}
        for path, item in entries.items():
            if item.get("kind") == "folder":
                result.setdefault(path, set())
        for path, item in entries.items():
            folder = str(item.get("source_folder") or "")
            if not folder or item.get("kind") == "folder":
                continue
            if folder not in result:
                continue
            try:
                relative = str(Path(path).relative_to(folder))
            except ValueError:
                continue
            result[folder].add((relative, str(item.get("kind") or ""), int(item.get("modified_at", 0)), int(item.get("size", 0))))
        return result

    old_signatures = folders(previous, True)
    new_signatures = folders(current, False)
    old_orders = {
        folder: {value for value in str(previous.get(folder, {}).get("order_id", "")).split("、") if value}
        for folder in old_signatures
    }
    new_orders = {
        folder: {value for value in str(current.get(folder, {}).get("order_id", "")).split("、") if value}
        for folder in new_signatures
    }
    pairs: list[tuple[str, str]] = []
    used_old: set[str] = set()
    for new_folder, signature in sorted(new_signatures.items()):
        if not signature:
            continue
        def content_matches(old_folder: str, new_folder: str) -> bool:
            """比较候选改名前后的文件指纹；old_folder 为旧目录，new_folder 为新目录，读取失败视为不一致。"""
            for relative, _, _, _ in signature:
                previous_row = previous.get(str(Path(old_folder) / relative), {})
                fingerprint = str(previous_row.get("content_fingerprint") or "")
                if not fingerprint:
                    continue
                try:
                    if _file_content_fingerprint(Path(new_folder) / relative) != fingerprint:
                        return False
                except OSError:
                    return False
            return True
        candidates = [
            old_folder for old_folder, old_signature in old_signatures.items()
            if old_folder not in used_old
            and old_folder not in current
            and Path(old_folder).parent == Path(new_folder).parent
            and old_signature == signature
            and old_orders.get(old_folder)
            and old_orders.get(old_folder) == new_orders.get(new_folder)
            and content_matches(old_folder, new_folder)
        ]
        if len(candidates) == 1:
            old_folder = candidates[0]
            used_old.add(old_folder)
            pairs.append((old_folder, new_folder))
    return pairs


def _rebase_server_folder_paths(store: "OrderIndexStore", pairs: list[tuple[str, str]]) -> None:
    """在目录改名被确认后迁移索引路径；store 为索引库，pairs 为旧路径到新路径的二元组列表。"""
    for old_folder, new_folder in pairs:
        rows = store.connection.execute(
            "select path from source_files where source_folder=? order by path",
            (old_folder,),
        ).fetchall()
        for (old_path,) in rows:
            relative = Path(old_path).relative_to(old_folder)
            new_path = str(Path(new_folder) / relative)
            store.connection.execute(
                "update source_files set path=?, source_folder=? where path=?",
                (new_path, new_folder, old_path),
            )
        for table in ("orders", "factory_orders", "temporary_orders"):
            try:
                store.connection.execute(
                    f"update {table} set source_folder=? where source_folder=?",
                    (new_folder, old_folder),
                )
            except sqlite3.OperationalError:
                pass
        try:
            store.connection.execute(
                "update pending_issues set path=? where path=? or path like ?",
                (new_folder, old_folder, old_folder + "/%"),
            )
        except sqlite3.OperationalError:
            pass
        store.add_change(
            severity="info",
            kind="server_folder_renamed",
            path=new_folder,
            message=f"已识别订单文件夹改名：{Path(old_folder).name} → {Path(new_folder).name}",
        )


def _server_data_change_message(
    change_type: str,
    order_ids: list[str],
    factory_order: str,
    data_label: str,
    path: str = "",
) -> str:
    """生成业务资料变化提示。

    参数：change_type 为变化类型；order_ids 为订单号；factory_order 为工厂单号；data_label 为资料类别；path 为可选路径。"""
    action = {"added": "新增", "modified": "修改", "removed": "删除"}[change_type]
    visible_orders = "、".join(dict.fromkeys(order_id for order_id in order_ids if order_id)) or "相关订单"
    subject = f"订单 {visible_orders}"
    if factory_order:
        subject += f"（工厂单 {factory_order}）"
    if data_label == _source_file_data_label("folder"):
        action = {"added": "首次发现", "modified": "检测到变化", "removed": "删除"}[change_type]
    message = f"{action}{subject}的{data_label}"
    if path:
        message += f"（来源：{path}）"
    return message


def _source_file_data_label(kind: str) -> str:
    """将来源类别 kind 转换为面向用户的资料名称。"""
    return {
        "board": "板材信息",
        "fittings": "五金信息",
        "folder": "工厂单文件夹和报表目录",
        "optimization_input": "优化输入 XML",
        "optimization_result": "优化结果 XML",
    }.get(kind, "报表数据")


def _summarize_server_read_items(items: list[tuple[str, str, str]]) -> str:
    """汇总已索引来源的读取说明，供看板提示使用。

    参数：items 为文件路径、所属目录、类别三元组列表；完整路径仍留在索引及错误记录中，显示摘要保持简短。"""
    groups: dict[str, dict[str, int]] = {}
    group_order: list[str] = []
    for path, source_folder, kind in items:
        folder = source_folder or (path if kind == "folder" else str(Path(path).parent))
        if folder not in groups:
            groups[folder] = {}
            group_order.append(folder)
        if kind != "folder":
            groups[folder][kind] = groups[folder].get(kind, 0) + 1

    if not groups:
        return "没有读取到可展示的 Server 文件或文件夹。"

    kind_labels = {
        "material": "material 文件",
        "board": "板材清单",
        "fittings": "五金清单",
    }
    total_files = sum(sum(counts.values()) for counts in groups.values())
    examples: list[str] = []
    for folder in group_order[:6]:
        folder_name = Path(folder).name or folder
        counts = groups[folder]
        parts = [
            f"{count} 个{' ' if kind_labels.get(kind, '报表')[0].isascii() else ''}{kind_labels.get(kind, '报表')}"
            for kind, count in counts.items()
        ]
        suffix = f"（下属：{'、'.join(parts)}）" if parts else ""
        examples.append(f"{folder_name} 文件夹{suffix}")

    summary = f"读取 {len(groups)} 个文件夹及 {total_files} 个相关文件"
    if examples:
        summary += "；包括：" + "；".join(examples)
    remaining = len(group_order) - len(examples)
    if remaining > 0:
        summary += f"；另有 {remaining} 个文件夹已省略"
    return summary + "。"


def _trace_rows(rows: list[dict]) -> tuple[int, int]:
    """统计 rows 中不重复的订单和工厂单数量，供操作记录展示。"""
    orders = {
        str(row.get("sales_order_name") or row.get("order_id") or "").strip().upper()
        for row in rows
        if isinstance(row, dict)
    }
    factories = {
        str(row.get("factory_order") or "").strip().upper()
        for row in rows
        if isinstance(row, dict)
    }
    orders.discard("")
    factories.discard("")
    return len(orders), len(factories)


def _flat_aimes_stage_durations(values: object) -> list[dict[str, object]]:
    """从耗时数据 values 提取互不重叠的 AIMES 阶段，排除重复的汇总项。"""
    if not isinstance(values, list):
        return []
    return [
        item
        for item in values
        if isinstance(item, dict)
        and str(item.get("stage", "")).strip() not in {"attempt", "total"}
        and "总计用时" not in str(item.get("label", ""))
    ]


def _complete_aimes_stage_durations(
    values: object,
    total_seconds: float,
) -> list[dict[str, object]]:
    """补齐后台准备和清理耗时；values 为已有阶段数据，total_seconds 为端到端总耗时秒数。"""
    stages = _flat_aimes_stage_durations(values)
    tracked = sum(
        max(0.0, float(item.get("duration_seconds", 0)))
        for item in stages
    )
    residual = max(0.0, float(total_seconds) - tracked)
    if residual >= 0.005:
        stages.append({
            "stage": "backend_overhead",
            "label": "后台准备与收尾",
            "duration_seconds": round(residual, 6),
        })
    return stages


def _aimes_trace(
    config: Config,
    *,
    source: str,
    rows: list[dict],
    wrote_cache: bool,
    error: str = "",
    warnings: list[dict] | None = None,
    elapsed_seconds: float | None = None,
    stage_durations: list[dict] | None = None,
) -> list[str]:
    """组装 AIMES 操作的来源、计数、错误及耗时说明。

    参数：config 为配置；source 为来源类型；rows 为记录；wrote_cache 为是否写缓存；error 为错误；
    warnings 为可选警告；elapsed_seconds 为总耗时；stage_durations 为阶段耗时列表。"""
    order_count, factory_count = _trace_rows(rows)
    if error:
        return [
            f"从 AIMES 读取最近 {AIMES_BULK_FETCH_LIMIT} 条工厂单信息失败：{error}；"
            f"改为从本地数据库缓存读取订单号 {order_count} 个、"
            f"工厂单号 {factory_count} 个的缓存信息。",
            f"写入到了 {config.workflow_database} 的同步失败记录。",
        ]
    if source == "cache":
        return [
            f"从本地数据库缓存读取订单号 {order_count} 个、"
            f"工厂单号 {factory_count} 个的 AIMES 工厂单名称、销售单名称和拆单时间；"
            "本次已跳过在线获取。",
        ]
    writes = [str(config.workflow_database)]
    if wrote_cache:
        writes.append(str(config.workflow_database))
    trace = [
        f"从 AIMES 读取最近 {AIMES_BULK_FETCH_LIMIT} 条工厂单信息，得到订单号 {order_count} 个、"
        f"工厂单号 {factory_count} 个的工厂单名称、销售单名称和拆单时间；",
        f"写入到了 {', '.join(writes)}。",
    ]
    if stage_durations:
        trace.append(
            "阶段耗时："
            + "；".join(
                f"{item.get('label', '未命名')} {float(item.get('duration_seconds', 0)):.2f} 秒"
                for item in stage_durations
                if isinstance(item, dict)
            )
            + "。"
        )
    if warnings:
        trace.append(f"有 {len(warnings)} 条销售单名称格式异常，本次未写入数据库，也未进入待处理中心。")
        trace.extend(
            f"未写入：{item.get('factory_order', '')}，销售单名称“{item.get('sales_order_name', '')}”。"
            for item in warnings
        )
    return trace


def _server_scan_trace(
    stats: dict[str, int | float],
    roots: list[str] | None = None,
    folder_timings: list[dict[str, object]] | None = None,
) -> list[str]:
    """组装 Server 扫描统计及耗时说明；stats 为计数统计，roots 为可选根目录，folder_timings 为目录耗时。"""
    root_detail = f"（目录：{'、'.join(roots)}）" if roots else ""
    excel_detail = ""
    if int(stats.get("related_excel_count", 0) or 0):
        excel_detail = f"，临时/混单文件夹相关 Excel 文件 {stats['related_excel_count']} 个"
    checked_label = "相关 XML 文件" if not excel_detail else "相关文件"
    trace = [
        f"快速检查 {stats['quick_checked_file_count']} 个{checked_label}，"
        f"复用 {stats['reused_folder_count']} 个订单文件夹，"
        f"深度扫描 {stats['deep_scanned_folder_count']} 个订单文件夹，"
        f"总用时 {stats['duration_seconds']:.2f} 秒。",
        f"扫描范围：订单文件夹 {stats['order_folder_count']} 个，"
        f"相关 XML 文件 {stats['related_xml_count']} 个{excel_detail}{root_detail}。",
        f"变化统计：新增 {stats['added_count']} 个，修改 {stats['modified_count']} 个，删除 {stats['deleted_count']} 个，改名 {stats.get('renamed_count', 0)} 个。",
        "阶段耗时："
        f"读取并比对 Server 文件 {float(stats.get('metadata_scan_seconds', 0)):.2f} 秒；"
        "普通扫描不读取 material 文件（材料只在预览/确认前校验）；"
        f"写入扫描元数据和快照 {float(stats.get('finalize_seconds', 0)):.2f} 秒。",
    ]
    if folder_timings:
        trace.append("文件级扫描明细：")
        for folder in sorted(
            folder_timings,
            key=lambda item: str(item.get("source_folder", "")).casefold(),
        ):
            folder_path = str(folder.get("source_folder") or "")
            files = [item for item in folder.get("files", []) if isinstance(item, dict)]
            folder_seconds = float(folder.get("duration_seconds", 0) or 0)
            trace.append(
                f"文件夹 {folder_path}：共 {len(files)} 个 XML 文件，"
                f"文件夹扫描用时 {folder_seconds:.6f} 秒。"
            )
            for item in sorted(files, key=lambda value: str(value.get("path", "")).casefold()):
                error = f"，{item.get('error')}" if item.get("error") else ""
                trace.append(
                    f"文件 {item.get('path', '')}："
                    f"{float(item.get('duration_seconds', 0) or 0):.6f} 秒{error}。"
                )
    return trace


@pending_check_session
def scan_server_changes(config: Config) -> dict:
    """比较 Server 元数据，不推进已处理业务基准；config 为扫描配置。

    可清理配置基准外的过期待处理状态，但不将当前材料或报表标为已处理。
    优化 XML 仅在内存中发现，其证据、时间及比较基准由材料确认事务负责。"""
    scanned_at = _now()
    scan_started = time.perf_counter()
    store = OrderIndexStore(config.workflow_database)
    server_folder_timings: list[dict[str, object]] = []
    _clear_stale_server_pending_state(config, store)
    root, current = _server_snapshot(
        config,
        store,
        timing_sink=server_folder_timings,
    )
    _resolve_fully_shipped_server_issues(config, store)
    _resolve_stale_produced_material_issues(store)
    store.commit()
    scan_roots = _available_server_roots(config)
    current_folders = {item["source_folder"] for item in current.values()}
    current_xml = {
        path: item
        for path, item in current.items()
        if item.get("kind") in SERVER_SCAN_XML_KINDS
    }
    temporary_xml_watch_folders = {
        str(item.get("source_folder") or "")
        for item in current.values()
        if item.get("kind") == "folder"
        and not _is_standard_order_folder(Path(str(item.get("source_folder") or "")).name)
        and (store.temporary_order(str(item.get("source_folder") or "")) or {}).get("outbound_status") == "已出库"
        and (store.temporary_order(str(item.get("source_folder") or "")) or {}).get("server_scan_policy") in {"watching", "manual_pending"}
    }
    legacy_folders = {
        str(item.get("source_folder") or "")
        for item in current.values()
        if item.get("kind") == "folder"
        and not _is_standard_order_folder(Path(str(item.get("source_folder") or "")).name)
        and str(item.get("source_folder") or "") not in temporary_xml_watch_folders
    }
    current_legacy = {
        path: item
        for path, item in current.items()
        if item.get("source_folder") in legacy_folders
        and item.get("kind") not in SERVER_SCAN_XML_KINDS
    }
    previous_xml_rows = store.server_scan_xml_state()
    previous_all = {
        row["path"]: {
            "source_folder": row["source_folder"],
            "kind": row["kind"],
            "order_id": row["order_id"],
            "modified_at": row["modified_at"],
            "size": 0,
            "manual_only": False,
            "mixed_order": False,
        }
        for row in previous_xml_rows
    }
    previous_legacy = {
        row[0]: {
            "source_folder": row[1],
            "kind": row[2],
            "order_id": row[5] or (
                "、".join(_folder_order_ids(Path(row[1])))
                if row[1] and Path(row[1]).is_dir() and _is_mixed_order_folder(Path(row[1]))
                else (Path(row[1]).name.upper() if row[1] else "")
            ),
            "modified_at": row[3],
            "size": row[4],
            "manual_only": bool(
                row[1]
                and Path(row[1]).is_dir()
                and not _is_standard_order_folder(Path(row[1]).name)
                and not _is_mixed_order_folder(Path(row[1]))
            ),
            "mixed_order": bool(
                row[1] and Path(row[1]).is_dir() and _is_mixed_order_folder(Path(row[1]))
            ),
        }
        for row in store.connection.execute(
            "select path, source_folder, kind, modified_at, size, order_id from source_files"
        ).fetchall()
        if row[1] in legacy_folders
    }
    previous_all = {
        path: item for path, item in previous_all.items()
        if root is None or any(
            _path_is_within(Path(item["source_folder"]), scan_root)
            for scan_root in scan_roots
        )
    }
    previous = {
        path: item for path, item in previous_all.items()
        if item.get("source_folder") in current_folders
    }
    changes: list[dict] = []
    for path in sorted(current_xml.keys() - previous.keys()):
        item = current_xml[path]
        changes.append({
            "id": f"added:{path}",
            "change_type": "added",
            "kind": item["kind"],
            "order_id": item["order_id"],
            "path": path,
            "message": _server_change_message("added", item, path),
            "source_folder": item["source_folder"],
            "manual_only": bool(item.get("manual_only")),
            "mixed_order": bool(item.get("mixed_order")),
            "event_time": _display_timestamp(item["created_at"]),
        })
    for path in sorted(current_xml.keys() & previous.keys()):
        before = previous[path]
        after = current[path]
        if before["modified_at"] == after["modified_at"]:
            continue
        changes.append({
            "id": f"modified:{path}",
            "change_type": "modified",
            "kind": after["kind"],
            "order_id": after["order_id"],
            "path": path,
            "message": _server_change_message("modified", after, path),
            "source_folder": after["source_folder"],
            "manual_only": bool(after.get("manual_only")),
            "mixed_order": bool(after.get("mixed_order")),
            "event_time": _display_timestamp(after["modified_at"] / 1_000),
        })
    for path in sorted(previous.keys() - current_xml.keys()):
        item = previous[path]
        changes.append({
            "id": f"removed:{path}",
            "change_type": "removed",
            "kind": item["kind"],
            "order_id": item["order_id"],
            "path": path,
            "message": _server_change_message("removed", item, path),
            "source_folder": item["source_folder"],
            "manual_only": bool(item.get("manual_only")),
            "mixed_order": bool(item.get("mixed_order")),
            "event_time": _display_timestamp(item["modified_at"] / 1_000),
        })
    # 临时及混合目录继续使用报表元数据流程，不适用标准订单仅检查 XML 的约定。
    for path in sorted(current_legacy.keys() - previous_legacy.keys()):
        item = current_legacy[path]
        changes.append({
            "id": f"added:{path}",
            "change_type": "added",
            "kind": item["kind"],
            "order_id": item.get("order_id", ""),
            "path": path,
            "message": _server_change_message("added", item, path),
            "source_folder": item["source_folder"],
            "manual_only": bool(item.get("manual_only")),
            "mixed_order": bool(item.get("mixed_order")),
            "event_time": _display_timestamp(item["created_at"]),
        })
    for path in sorted(current_legacy.keys() & previous_legacy.keys()):
        before = previous_legacy[path]
        after = current_legacy[path]
        if before["kind"] == "folder" and after["kind"] == "folder":
            continue
        if (before["modified_at"], before["size"]) == (after["modified_at"], after["size"]):
            continue
        changes.append({
            "id": f"modified:{path}",
            "change_type": "modified",
            "kind": after["kind"],
            "order_id": after.get("order_id", ""),
            "path": path,
            "message": _server_change_message("modified", after, path),
            "source_folder": after["source_folder"],
            "manual_only": bool(after.get("manual_only")),
            "mixed_order": bool(after.get("mixed_order")),
            "event_time": _display_timestamp(after["modified_at"] / 1_000),
        })
    for path in sorted(previous_legacy.keys() - current_legacy.keys()):
        item = previous_legacy[path]
        changes.append({
            "id": f"removed:{path}",
            "change_type": "removed",
            "kind": item["kind"],
            "order_id": item.get("order_id", ""),
            "path": path,
            "message": _server_change_message("removed", item, path),
            "source_folder": item["source_folder"],
            "manual_only": bool(item.get("manual_only")),
            "mixed_order": bool(item.get("mixed_order")),
            "event_time": _display_timestamp(item["modified_at"] / 1_000),
        })
    # 先从名称识别混合订单目录；即使暂无可用报表，也保留待处理入口，实际解析留到明确预览或处理时。
    for path, item in sorted(current_legacy.items()):
        if item["kind"] != "folder" or not item.get("mixed_order"):
            continue
        folder = Path(path)
        if _report_files(folder):
            store.resolve_active_issue(f"server_missing_report:{path}")
            continue
        issue_key = f"server_missing_report:{path}"
        issue_message = _server_change_message("missing_report", item, path)
        store.upsert_active_issue(
            issue_key=issue_key,
            kind="server_missing_report",
            order_id=item.get("order_id", ""),
            path=path,
            message=issue_message,
            seen_at=scanned_at,
        )
        if not any(
            change.get("change_type") == "missing_report" and change.get("path") == path
            for change in changes
        ):
            changes.append({
                "id": f"missing_report:{path}",
                "change_type": "missing_report",
                "kind": "folder",
                "order_id": item.get("order_id", ""),
                "path": path,
                "message": issue_message,
                "source_folder": item.get("source_folder", path),
                "manual_only": False,
                "mixed_order": True,
                "event_time": _display_timestamp(item["modified_at"] / 1_000),
            })
    # 临时订单处理失败后仍须可操作，但不清除元数据基准；保留原路径比较基准，从当前问题生成待处理变化，
    # 避免未变化的重试被误报为新发现订单。
    failed_temporary_paths = {
        str(issue.get("path") or "")
        for issue in store.active_issues()
        if issue.get("kind") == "temporary_processing" and issue.get("path")
    }
    for folder_path in sorted(failed_temporary_paths):
        issue = next(
            (
                item for item in store.active_issues()
                if item.get("kind") == "temporary_processing"
                and str(item.get("path") or "") == folder_path
            ),
            None,
        )
        if issue is None:
            continue
        pending_paths = [
            path for path, item in sorted(current.items())
            if item.get("source_folder") == folder_path
        ]
        for path in pending_paths:
            item = current[path]
            changes.append({
                "id": f"processing_failed:{path}",
                "change_type": "processing_failed",
                "kind": item["kind"],
                "order_id": item.get("order_id", ""),
                "path": path,
                "message": f"上次处理失败，待重新处理：{issue['message']}",
                "source_folder": folder_path,
                "manual_only": True,
                "mixed_order": bool(item.get("mixed_order")),
                "event_time": str(issue.get("last_seen") or scanned_at),
            })
    for change in changes:
        folder_path = str(change.get("source_folder") or "")
        item = current.get(folder_path, {})
        change["handling_mode"] = item.get("handling_mode", "")
        change["reference_order_ids"] = item.get("reference_order_ids", [])
        if item.get("handling_mode") in {"supplemental", "external_manual"}:
            change["manual_only"] = True
            change["order_id"] = item.get("order_id", "")
    from .aicnc_import import enabled as aicnc_enabled, discover as discover_optimizations
    if aicnc_enabled(store.connection):
        changes.extend(discover_optimizations(config, store.connection))

    order_folder_count = sum(item["kind"] == "folder" for item in current.values())
    related_xml_count = len(current_xml)
    related_legacy_count = sum(item["kind"] != "folder" for item in current_legacy.values())
    metadata_finished = time.perf_counter()
    scan_stats: dict[str, int | float] = {
        # 此项与完整扫描总数分开；普通 Server 扫描仅比较元数据和 XML，材料解析属于明确预览及确认流程。
        "metadata_scan_seconds": round(metadata_finished - scan_started, 6),
        "order_folder_count": order_folder_count,
        # 当前扫描器只检查纳入目录中的两类优化 XML，工作簿仅在用户打开预览时解析。
        "quick_checked_file_count": related_xml_count + related_legacy_count,
        "reused_folder_count": 0,
        "deep_scanned_folder_count": order_folder_count,
        "related_xml_count": related_xml_count,
        # 保留旧字段名供已有客户端解码，但它不再代表当前 Server 扫描涉及的文件。
        "related_excel_count": related_legacy_count,
        "added_count": sum(item["change_type"] == "added" for item in changes),
        "modified_count": sum(item["change_type"] == "modified" for item in changes),
        "deleted_count": sum(item["change_type"] == "removed" for item in changes),
        "renamed_count": sum(item["change_type"] == "renamed" for item in changes),
    }
    finalize_started = time.perf_counter()
    folder_timing_by_path = {
        str(item["source_folder"]): item for item in server_folder_timings
        if item.get("source_folder")
    }
    _finalize_server_scan_policies(
        config,
        store,
        [
            Path(path)
            for path, item in current.items()
            if item.get("kind") == "folder"
        ],
        scanned_at,
    )
    current_issues = store.active_issues()
    orders = store.summaries()
    store.commit()
    store.close()
    snapshot_path = ""
    try:
        snapshot_path = str(
            _write_server_scan_snapshot(
                config,
                root=root,
                roots=_available_server_roots(config),
                scanned_at=scanned_at,
                entries={path: item for path, item in current.items()
                         if item.get("kind") not in SERVER_SCAN_XML_KINDS},
            )
        )
    except OSError:
        # 下一次同步可以安全回退到自行进行只读遍历。
        snapshot_path = ""
    completed = time.perf_counter()
    scan_stats["finalize_seconds"] = round(completed - finalize_started, 6)
    scan_stats["duration_seconds"] = round(completed - scan_started, 6)
    timing_stages = [
        {
            "stage": "server_metadata",
            "label": "读取并比对 Server 文件",
            "duration_seconds": scan_stats["metadata_scan_seconds"],
        },
        {
            "stage": "scan_finalize",
            "label": "写入扫描元数据和快照",
            "duration_seconds": scan_stats["finalize_seconds"],
        },
    ]
    scan_stats["duration_seconds"] = round(
        sum(float(stage["duration_seconds"]) for stage in timing_stages), 6
    )
    return {
        "server": {
            "scanned_at": scanned_at,
            "root": str(root),
            "roots": [str(item) for item in _available_server_roots(config)],
            "changed": bool(changes),
            "change_count": len(changes),
            "changes": changes,
            "scan_stats": scan_stats,
            "folder_file_timings": sorted(
                folder_timing_by_path.values(),
                key=lambda item: str(item.get("source_folder", "")).casefold(),
            ),
            "snapshot_path": snapshot_path,
        },
        "current_issues": current_issues,
        "orders": orders,
        "operation_trace": {
            "server": _server_scan_trace(
                scan_stats,
                [str(item) for item in _available_server_roots(config)],
                list(folder_timing_by_path.values()),
            ),
        },
        "operation_timing": {
            "total_seconds": scan_stats["duration_seconds"],
            "stages": timing_stages,
        }
    }


def _path_is_within(path: Path, root: Path) -> bool:
    """判断路径 path 是否位于根目录 root 内。"""
    try:
        path.resolve().relative_to(root.resolve())
    except ValueError:
        return False
    return True


def _server_folders_for_sync(
    config: Config,
    selected_folder: Path | None,
    *,
    selected_folders: list[Path] | None = None,
    store: OrderIndexStore | None = None,
    aimes_rows: list[dict] | None = None,
) -> tuple[Path, list[Path]]:
    """确定本次同步目录并校验来源范围。

    参数：config 为配置；selected_folder 为单选目录；selected_folders 为可选多选目录；
    store 为可选索引库；aimes_rows 为可选最新身份记录。"""
    roots = _available_server_roots(config)
    if not roots:
        from .order_workflow import resolve_source_root
        resolve_source_root(config.source_root)
    root = roots[0]

    def containing_root(candidate: Path) -> Path | None:
        """查找包含候选路径 candidate 的已配置 Server 根目录，未找到时返回 None。"""
        return next((server_root for server_root in roots if _path_is_within(candidate, server_root)), None)

    def assert_legacy_selection(candidate: Path) -> None:
        # 显式旧入口也不得绕过新版确认台账；尚未创建数据库时保持原目录校验。
        if not config.workflow_database.is_file():
            return
        from .aicnc_import import enabled as aicnc_enabled
        check_connection = store.connection if store is not None else connect_database(config.workflow_database)
        try:
            if aicnc_enabled(check_connection):
                legacy_paths = {Path(row[0]).resolve() for row in check_connection.execute('select path from aicnc_legacy_watch')}
                if candidate.resolve() not in legacy_paths:
                    raise RuleError('aicnc_preview_required','新版目录请在待处理中心选择单个优化文件夹，预览并确认后处理')
        finally:
            if store is None:
                check_connection.close()

    if selected_folders is not None:
        folders = []
        for selected in selected_folders:
            candidate = selected.expanduser().resolve()
            source_root = containing_root(candidate)
            if not candidate.is_dir() or source_root is None:
                raise RuleError("server_folder_invalid", f"所选 Server 文件夹无法访问或不在 Server 根目录内：{selected}")
            if not _is_standard_order_folder(candidate.name) and not _report_files(candidate):
                raise RuleError(
                    "server_folder_invalid",
                    f"无法识别所选文件夹：{candidate}。该目录及子目录中未找到可识别的 material、板材清单或 Fittingslist .xlsx 报表。请选择包含这些报表的订单目录；若选择的是优化结果目录，请返回上一级订单目录。",
                )
            assert_legacy_selection(candidate)
            # 独立目录记录保留配置中的扫描根路径拼写。
            if not _is_standard_order_folder(candidate.name):
                candidate = source_root / candidate.relative_to(source_root.resolve())
            folders.append(candidate)
        return root, list(dict.fromkeys(folders))

    if selected_folder is None:
        if store is None:
            store = OrderIndexStore(config.workflow_database)
            close_store = True
        else:
            close_store = False
        from .aicnc_import import enabled as aicnc_enabled
        if aicnc_enabled(store.connection):
            folders = [Path(row[0]) for row in store.connection.execute("select path from aicnc_legacy_watch where retired_at=''")
                       if Path(row[0]).is_dir() and _server_folder_scan_allowed(config, store, Path(row[0]), aimes_rows)]
            if close_store:
                store.close()
            return root, folders
        folders = []
        for server_root in roots:
            folders.extend(
                folder
                for folder in server_root.iterdir()
                if folder.is_dir()
                and not _server_folder_is_ignored(store, folder)
                and (
                    (
                        _is_standard_order_folder(folder.name)
                        and _order_type(folder.name) == _server_root_order_type(server_root)
                        and _server_folder_scan_allowed(config, store, folder, aimes_rows)
                    )
                    or (
                        _is_mixed_order_folder(folder)
                        and _server_folder_scan_allowed(config, store, folder, aimes_rows)
                    )
                    or (
                        not _is_standard_order_folder(folder.name)
                        and _temporary_folder_is_candidate(config, store, folder)
                    )
                )
            )
        folders.sort(key=lambda item: (_folder_created_at(item), item.name.casefold()), reverse=True)
        if close_store:
            store.close()
        return root, folders

    selected = selected_folder.expanduser().resolve()
    source_root = containing_root(selected)
    if not selected.is_dir() or source_root is None:
        raise RuleError("server_folder_invalid", "所选文件夹无法访问，请重新选择 Server 订单文件夹。")
    from .aicnc_import import OPTIMIZATION_RE
    if OPTIMIZATION_RE.fullmatch(selected.name):
        assert_legacy_selection(selected)
    if not _is_standard_order_folder(selected.name):
        selected = source_root / selected.relative_to(source_root.resolve())
    if _is_standard_order_folder(selected.name):
        assert_legacy_selection(selected)
        return selected, [selected]
    if _direct_report_files(selected):
        assert_legacy_selection(selected)
        # 包含已识别报表的非标准目录属于临时或混合订单，以目录自身为处理范围，不扩展为子订单目录。
        return selected, [selected]
    raise RuleError(
        "server_folder_invalid",
        "选错了文件夹：请选择订单文件夹，或选择包含 material、板材清单或 Fittingslist 的临时订单文件夹。",
    )


def _clear_stale_mapping_validation_status(
    store: OrderIndexStore,
    order_ids: set[str],
    current_issue_keys: set[str],
    seen_at: str,
) -> int:
    """在 SKU 映射已解决后清除旧校验错误。

    参数：store 为索引库；order_ids 为订单范围；current_issue_keys 为仍有效的问题；seen_at 为观察时间。"""
    cleared = 0
    for order_id in sorted({value.upper() for value in order_ids if value}):
        mapping_prefixes = (
            f"material_mapping:{order_id}:",
            f"hardware_mapping:{order_id}:",
        )
        if any(key.startswith(mapping_prefixes) for key in current_issue_keys):
            continue
        row = store.connection.execute(
            "select coalesce((select v.status from temp.preview_validation v where v.order_id=orders.order_id),'正常'), coalesce((select v.message from temp.preview_validation v where v.order_id=orders.order_id),'') from orders where order_id = ?",
            (order_id,),
        ).fetchone()
        if not row or row[0] != "数据异常" or "未完成商品 SKU 处理" not in (row[1] or ""):
            continue
        store.set_validation(order_id, '正常')
        cleared += 1
    return cleared


def _exact_resolve_unowned_factories(config: Config, candidates: dict[str, dict]) -> str:
    """仅对本地没有身份的新工厂单进行 AIMES 精确查询。

    参数：config 为配置；candidates 为候选集合。调用方先用持久身份补全候选，
    不能因 Server 报表只有部分名称就重复进行在线查询。"""
    missing = sorted(
        factory_order
        for factory_order, candidate in candidates.items()
        if not candidate.get("orders")
        and not candidate.get("names", {}).get("aimes")
    )
    if not missing:
        return ""
    from .core import lookup_aimes_names

    try:
        names = lookup_aimes_names(config, missing)
    except Exception as exc:
        return str(exc)
    for factory_order, factory_name in names.items():
        if factory_order in candidates and factory_name:
            _merge_candidate(
                candidates,
                factory_order,
                name=factory_name,
                source="aimes_exact",
                folder=sorted(candidates[factory_order]["folders"])[0] if candidates[factory_order]["folders"] else "",
            )
    return ""


def _merge_database_factory_candidates(
    store: OrderIndexStore,
    candidates: dict[str, dict],
) -> set[str]:
    """在线精确查询前复用持久工厂单身份；store 为索引库，candidates 为待补全候选集合。"""
    if not candidates:
        return set()
    placeholders = ",".join("?" for _ in candidates)
    rows = store.connection.execute(
        f"""
        select factory_order, order_id, factory_name, sales_order_name,
               split_time, name_source, has_hardware, (stage<>'已拆单') as optimized
        from factory_orders
        where aimes_status='active' and factory_order in ({placeholders})
        """,
        tuple(candidates),
    ).fetchall()
    found: set[str] = set()
    for row in rows:
        factory_order = str(row[0]).upper().strip()
        name_source = str(row[5] or "server_report")
        candidate_source = {
            "AIMES": "aimes",
            "AIMES精确查询": "aimes_exact",
        }.get(name_source, "server")
        _merge_candidate(
            candidates,
            factory_order,
            name=str(row[2] or ""),
            source=candidate_source,
            order_id=str(row[1] or ""),
            sales_order_name=str(row[3] or "") if candidate_source in {"aimes", "aimes_exact"} else "",
            split_time=str(row[4] or "") if candidate_source in {"aimes", "aimes_exact"} else "",
            has_hardware=bool(row[6]),
            optimized=bool(row[7]),
        )
        found.add(factory_order)
    return found


def _preview_fittings_groups(path: Path, cache: dict | None = None) -> list:
    """在单次预览内复用五金解析结果，不跨请求保存；path 为报表路径，cache 为可选请求内缓存。"""
    from .order_workflow import parse_fittings_groups

    stat = path.stat()
    key = (str(path), stat.st_mtime_ns, stat.st_size)
    if cache is not None and key in cache:
        return cache[key]
    groups = parse_fittings_groups(path)
    if cache is not None:
        cache[key] = groups
    return groups


@with_source_decisions
@pending_check_session
def sync_order_index(
    config: Config,
    *,
    refresh_aimes: bool = False,
    aimes_if_needed: bool = False,
    selected_folder: Path | None = None,
    selected_folders: list[Path] | None = None,
    process_temporary: bool = False,
    include_hardware: bool = True,
    full_refresh: bool = False,
    validate_selected_orders: bool = True,
    refresh_outbound_statuses: bool = True,
    reconcile_outbound: bool = True,
    server_snapshot_path: Path | None = None,
    fittings_cache: dict | None = None,
) -> dict:
    """同步 AIMES、Server 事实到订单索引并返回看板摘要。

    参数：config 为配置；refresh_aimes 为刷新身份；aimes_if_needed 为按需刷新；selected_folder、selected_folders 为所选目录；
    process_temporary 为是否处理临时目录；include_hardware 为是否包含五金；full_refresh 为完整重查；
    validate_selected_orders 为是否校验所选订单；refresh_outbound_statuses 为是否刷新出库状态；
    reconcile_outbound 为是否执行出库对账；server_snapshot_path 为可选扫描快照；fittings_cache 为请求内五金解析缓存。
    普通看板刷新复用未变化报表的元数据，仅重新预览受变化影响的订单；完整刷新用于明确的核查或诊断。"""
    from .order_workflow import (
        ORDER_FOLDER_RE as SOURCE_ORDER_FOLDER_RE,
        MaterialItem,
        _board_report_materials,
        parse_board_identity,
        parse_fittings_groups,
        parse_order_materials,
        _fittings_report_is_empty,
        _material_inventory_name,
        preview_order,
        related_order_ids,
        resolve_source_root,
    )

    operation_started = time.perf_counter()
    started = _now()
    phase_started = time.perf_counter()
    phase_durations: dict[str, float] = {}

    def finish_phase(name: str) -> None:
        """记录阶段 name 的耗时并重置下一阶段计时起点。"""
        nonlocal phase_started
        now = time.perf_counter()
        phase_durations[name] = round(now - phase_started, 3)
        phase_started = now

    inventory_mappings = (
        InventoryMappings(config.workflow_database, connection=config.workflow_connection)
        if config.storage_prepared else None
    )
    # 商品映射会另开短期读连接；在索引库开启结构事务前初始化，并在本次同步中复用。
    store = OrderIndexStore(config.workflow_database, connection=config.workflow_connection)
    store.connection.execute("delete from temp.preview_validation")
    _mark_initial_orders_shipped(config, store)
    _reconcile_temporary_order_projections(store)
    _clear_stale_server_pending_state(config, store)
    store.delete_stale_factory_ownership_issues(config.initial_date)
    store.commit()
    changes_before = store.latest_change_id()
    today = date.today().isoformat()
    cached_aimes_source_rows = load_aimes_order_cache(config)
    cached_aimes_rows, _cached_aimes_warnings = _partition_aimes_rows(
        cached_aimes_source_rows,
        store.ignored_aimes_keys(),
        store.aimes_assignments(),
    )
    persisted_aimes_warnings = store.aimes_review_rows()
    automatic_aimes = aimes_if_needed and not (
        store.has_successful_aimes_sync_on(today)
    )
    should_refresh_aimes = bool(refresh_aimes or automatic_aimes)
    aimes_attempted = should_refresh_aimes
    aimes_succeeded = False
    aimes_rows: list[dict] = []
    aimes_fetched_rows: list[dict] = []
    aimes_warnings: list[dict] = []
    aimes_duration_seconds: float | None = None
    aimes_stage_durations: list[dict] = []
    aimes_deleted_count = 0
    aimes_deletion_check_error = ""
    aimes_verification_result: dict | None = None
    errors: list[str] = []
    if should_refresh_aimes:
        try:
            from .core import refresh_aimes_recent_orders
            aimes_started = time.perf_counter()
            fetch_stage_durations: list[dict[str, object]] = []
            verification_candidates = _active_aimes_factory_orders(store)
            if verification_candidates:
                from .core import refresh_aimes_recent_orders_and_verify
                fetched_rows, aimes_verification_result = refresh_aimes_recent_orders_and_verify(
                    config,
                    AIMES_BULK_FETCH_LIMIT,
                    verification_candidates,
                    timing_sink=fetch_stage_durations,
                )
                fetched_rows = _merge_aimes_recent_and_verified_rows(
                    fetched_rows,
                    aimes_verification_result,
                    cached_rows=cached_aimes_source_rows,
                )
            else:
                fetched_rows = refresh_aimes_recent_orders(
                    config,
                    AIMES_BULK_FETCH_LIMIT,
                    persist=False,
                    timing_sink=fetch_stage_durations,
                )
            aimes_fetched_rows = fetched_rows
            aimes_rows, aimes_warnings = _partition_aimes_rows(
                fetched_rows,
                store.ignored_aimes_keys(),
                store.aimes_assignments(),
            )
            aimes_stage_durations = _flat_aimes_stage_durations(fetch_stage_durations)
            persist_started = time.perf_counter()
            _persist_valid_aimes_mapping(
                config,
                aimes_rows,
                aimes_warnings,
                cached_rows=cached_aimes_source_rows,
            )
            aimes_stage_durations.append({
                "stage": "mapping_write",
                "label": "写入有效映射和数据库",
                "duration_seconds": round(time.perf_counter() - persist_started, 6),
            })
            aimes_succeeded = True
            verify_started = time.perf_counter()
            aimes_deleted_count, aimes_deletion_check_error = _verify_missing_aimes_factories(
                config, store, fetched_rows, verified_at=_now(),
                verification_result=aimes_verification_result,
            )
            aimes_stage_durations.append({
                "stage": "deleted_verify",
                "label": "精确核验已删除工厂单",
                "duration_seconds": round(time.perf_counter() - verify_started, 6),
            })
            aimes_duration_seconds = round(time.perf_counter() - aimes_started, 6)
            aimes_stage_durations = _complete_aimes_stage_durations(
                aimes_stage_durations,
                aimes_duration_seconds,
            )
        except Exception as exc:
            message = _business_aimes_message(exc)
            errors.append(message)
            if isinstance(exc, RuleError):
                aimes_stage_durations = list(exc.context.get("aimes_timings", []))
            store.add_change(severity="error", kind="aimes", message=message)
    if not aimes_succeeded:
        aimes_rows = cached_aimes_rows
        aimes_warnings = persisted_aimes_warnings
    else:
        store.replace_aimes_review_rows(aimes_warnings)
    finish_phase("load_aimes_and_local_state")

    snapshot_data = None
    if selected_folder is None and selected_folders is None:
        snapshot_data = _load_server_scan_snapshot(config, server_snapshot_path)
    server_snapshot_entries: dict[str, dict] | None = None
    server_snapshot_reused = snapshot_data is not None
    if snapshot_data is not None:
        root, server_folders, server_snapshot_entries = snapshot_data
        server_folders = [folder for folder in server_folders
                          if not _server_folder_is_ignored(store, folder)]
        allowed_snapshot_folders = {str(folder) for folder in server_folders}
        server_snapshot_entries = {path: item for path, item in server_snapshot_entries.items()
                                   if item.get("source_folder") in allowed_snapshot_folders}
    else:
        try:
            root, server_folders = _server_folders_for_sync(
                config,
                selected_folder,
                selected_folders=selected_folders,
                store=store,
                aimes_rows=aimes_rows,
            )
        except Exception as exc:
            errors.append(_business_server_message(exc))
            root = None
            server_folders = []
    finish_phase("server_folder_selection")
    candidates: dict[str, dict] = {}
    candidate_aimes_rows = aimes_rows
    if selected_folder is not None or selected_folders is not None:
        selected_order_ids = {
            order_id.upper()
            for folder in server_folders
            for order_id in _server_folder_order_ids(folder)
        }
        candidate_aimes_rows = [
            row for row in aimes_rows
            if str(row.get("sales_order_name", "")).upper().strip() in selected_order_ids
        ]
    for row in candidate_aimes_rows:
        if _factory_order_before_initial_date(
            row["factory_order"], row.get("split_time", ""), config.initial_date
        ):
            continue
        _merge_candidate(
            candidates,
            row["factory_order"],
            name=row["factory_name"],
            source="aimes",
            sales_order_name=row["sales_order_name"],
            split_time=row["split_time"],
        )
        store.upsert_order(row["sales_order_name"], aimes_seen=_now())

    folder_count = 0
    server_seen = _now()
    seen_source_paths: set[str] = set()
    server_read_items: list[tuple[str, str, str]] = []
    server_reused_paths: list[str] = []
    server_parsed_paths: list[str] = []
    server_order_ids: set[str] = set()
    server_factory_orders: set[str] = set()
    changed_order_ids: set[str] = set()
    changed_order_level_ids: set[str] = set()
    changed_factory_orders: set[str] = set()
    scanned_server_folders: set[str] = set()
    current_issue_keys: set[str] = set()
    resolved_mapping_order_ids: set[str] = set()
    temporary_processing_errors: dict[str, str] = {}
    temporary_processing_results: list[dict] = []
    exact_lookup_error = ""
    canonical_order_folders: dict[str, Path] = {}
    scanned_folder_paths = {str(folder) for folder in server_folders}
    authoritative_material_folders: dict[str, set[str]] = defaultdict(set)
    if server_snapshot_entries is not None:
        previous_for_rename = {
            row[0]: {
                "source_folder": row[1],
                "kind": row[2],
                "order_id": row[3],
                "modified_at": row[4],
                "size": row[5],
                "content_fingerprint": row[6] or "",
            }
            for row in store.connection.execute(
                "select path, source_folder, kind, order_id, modified_at, size, content_fingerprint from source_files"
            ).fetchall()
        }
        rename_pairs = _server_folder_rename_pairs(previous_for_rename, server_snapshot_entries)
        if rename_pairs:
            _rebase_server_folder_paths(store, rename_pairs)
    previous_source_metadata = {
        row[0]: {
            "source_folder": row[1],
            "kind": row[2],
            "order_id": row[3],
            "factory_order": row[4],
        }
        for row in store.connection.execute(
            "select path, source_folder, kind, order_id, factory_order from source_files"
        ).fetchall()
        if root is None
        or selected_folder is not None
        or selected_folders is not None
        or row[1] in scanned_folder_paths
    }
    previous_source_paths = set(previous_source_metadata)
    if root is not None:
        for folder in server_folders:
            folder_count += 1
            scanned_server_folders.add(str(folder))
            server_read_items.append((str(folder), str(folder), "folder"))
            standard_folder = _is_standard_order_folder(folder.name)
            mixed_folder = _is_mixed_order_folder(folder)
            handling_mode = _server_folder_handling_mode(store, folder, aimes_rows)
            independent_manual = handling_mode in {"supplemental", "external_manual"}
            manual_folder = not (standard_folder or mixed_folder) or independent_manual
            if handling_mode == "supplemental" and not store.temporary_order(str(folder)):
                store.upsert_temporary_order(
                    temporary_id=_temporary_order_id(folder), folder_name=folder.name,
                    source_folder=str(folder), folder_created_at=_folder_created_at(folder),
                    content_fingerprint="", processing_status="待人工处理",
                    handling_mode="supplemental", reference_order_ids=_folder_name_order_ids(folder),
                )
            folder_metadata = (
                server_snapshot_entries.get(str(folder))
                if server_snapshot_entries is not None
                else None
            )
            if manual_folder and process_temporary and not independent_manual:
                try:
                    temporary_processing_results.append(
                        _process_temporary_folder(
                            config,
                            folder,
                            store=store,
                            include_hardware=include_hardware,
                        )
                    )
                except Exception as exc:
                    message = str(exc)
                    if not isinstance(exc, RuleError):
                        message = "临时订单文件夹解析或出库失败，请检查文件格式、材料映射和库存系统后重试"
                    temporary_processing_errors[str(folder)] = message
                    fingerprint = ""
                    try:
                        fingerprint = _temporary_folder_fingerprint(folder)
                        existing_temporary = store.temporary_order(str(folder)) or {}
                        store.upsert_temporary_order(
                            temporary_id=existing_temporary.get("temporary_id") or _temporary_order_id(folder),
                            folder_name=folder.name,
                            source_folder=str(folder),
                            folder_created_at=_folder_created_at(folder),
                            content_fingerprint=fingerprint,
                            traveler_path=existing_temporary.get("traveler_path", ""),
                            processing_status="处理失败",
                            outbound_status=existing_temporary.get("outbound_status", "未出库"),
                            outbound_document=existing_temporary.get("outbound_document", ""),
                            last_error=message,
                        )
                    except (OSError, sqlite3.Error):
                        pass
                    issue_key = f"temporary_processing:{folder}"
                    current_issue_keys.add(issue_key)
                    store.upsert_active_issue(
                        issue_key=issue_key,
                        kind="temporary_processing",
                        order_id="、".join(_folder_order_ids(folder)),
                        path=str(folder),
                        message=message,
                        seen_at=server_seen,
                    )
                    store.add_change(
                        severity="warning",
                        kind="temporary_processing",
                        order_id="、".join(_folder_order_ids(folder)),
                        message=message,
                        path=str(folder),
                    )
            if folder_metadata is not None and folder_metadata.get("order_id"):
                folder_order_ids = [
                    value.strip().upper()
                    for value in str(folder_metadata["order_id"]).split("、")
                    if value.strip()
                ]
            else:
                folder_order_ids = (
                    related_order_ids(folder) or [folder.name.upper()]
                    if standard_folder
                    else _folder_order_ids(folder)
                )
            display_order_id = "、".join(folder_order_ids)
            if not manual_folder:
                server_order_ids.update(order_id.upper() for order_id in folder_order_ids if order_id)
                for folder_order_id in folder_order_ids:
                    authoritative_material_folders[folder_order_id.upper()].add(str(folder))
            if standard_folder:
                for folder_order_id in folder_order_ids:
                    if folder.name.casefold() == folder_order_id.casefold():
                        canonical_order_folders[folder_order_id.upper()] = folder
            folder_change_type = store.upsert_source_file(
                folder,
                source_folder=folder,
                kind="folder",
                order_id=display_order_id,
                changed_at=server_seen,
                metadata=folder_metadata,
            )
            seen_source_paths.add(str(folder))
            if folder_change_type:
                store.add_change(
                    severity="info",
                    kind="folder_changed",
                    order_id=display_order_id,
                    message=_server_data_change_message(
                        folder_change_type,
                        folder_order_ids or [folder.name.upper()],
                        "",
                        _source_file_data_label("folder"),
                        str(folder),
                    ),
                    path=str(folder),
                )
            if not manual_folder:
                for order_id in folder_order_ids:
                    store.upsert_order(
                        order_id,
                        # 标准或混合 Server 目录可证明先前看似临时的订单已属于正常自有或 CUT TO SIZE 订单。
                        order_type=_order_type(order_id),
                        source_folder=str(folder),
                        server_seen=server_seen,
                    )
            if server_snapshot_entries is not None:
                report_files = sorted(
                    [
                        (Path(path), str(item["kind"]), item)
                        for path, item in server_snapshot_entries.items()
                        if item.get("source_folder") == str(folder)
                        and item.get("kind") in {"material", "board", "fittings"}
                    ],
                    key=lambda item: str(item[0]).casefold(),
                )
                # 轻量快照仅包含 XML 变化标记；明确预览及确认仍需当前 Excel，所以只在用户选择处理目录后发现这些文件。
                if not report_files:
                    report_files = [
                        (path, kind, None) for path, kind in _report_files(folder)
                    ]
            else:
                report_files = [(path, kind, None) for path, kind in _report_files(folder)]
            fittings_paths = [path for path, kind, _ in report_files if kind == "fittings"]
            hardware_fittings_paths = _hardware_report_paths(fittings_paths, folder)
            selected_fittings = {}
            fittings_selection_error: RuleError | None = None
            should_select_fittings = (
                include_hardware
                and bool(hardware_fittings_paths)
                and not manual_folder
                and not all(order_id.upper().startswith("CS") for order_id in folder_order_ids)
            )
            if should_select_fittings:
                try:
                    selected_fittings, _, _, _ = select_latest_fittings(hardware_fittings_paths)
                except RuleError as exc:
                    fittings_selection_error = exc
                    issue_key = f"hardware_selection:{display_order_id}:{folder}"
                    current_issue_keys.add(issue_key)
                    store.upsert_active_issue(
                        issue_key=issue_key,
                        kind="hardware_selection",
                        order_id=display_order_id,
                        path=str(folder),
                        message=str(exc),
                        seen_at=server_seen,
                    )
                    store.add_change(
                        severity="warning",
                        kind="hardware_selection",
                        order_id=display_order_id,
                        message=str(exc),
                        path=str(folder),
                        observed_at=server_seen,
                    )
            for path, kind, file_metadata in report_files:
                server_read_items.append((str(path), str(folder), kind))
                file_change_type = store.upsert_source_file(
                    path,
                    source_folder=folder,
                    kind=kind,
                    changed_at=server_seen,
                    metadata=file_metadata,
                )
                if file_change_type:
                    # 工作簿已变且解析失败时，不能回退到旧身份；只有未变化的工作簿可以安全复用已索引身份。
                    store.connection.execute(
                        "update source_files set order_id = '', factory_order = '' where path = ?",
                        (str(path),),
                    )
                seen_source_paths.add(str(path))
                # 临时或返工报表只通过待处理中心批准流程处理；此同步保留元数据基准，不解析或投影到正式业务事实。
                if manual_folder:
                    continue
                if file_change_type:
                    changed_order_ids.update(
                        order_id.upper() for order_id in folder_order_ids if order_id
                    )
                    if kind == "material":
                        changed_order_level_ids.update(
                            order_id.upper() for order_id in folder_order_ids if order_id
                        )
                # 五金属于用户可选输入，未选择时不解析或校验；非标准临时目录也只在批准处理时解析，
                # 届时依据是否匹配 AIMES 选择严格归属或无归属规则。
                if kind == "fittings" and not include_hardware:
                    continue
                if kind == "material" and config.storage_prepared:
                    from .order_workflow import (
                        _room_has_explicit_order_identity,
                        _select_room_materials,
                        parse_order_materials,
                        parse_material_room_rows,
                    )
                    from .inventory import resolve_inventory_items, TravelerItem

                    try:
                        # 房间级分配用于保留工厂单归属，但不能跳过订单材料工作簿校验；标准单目录即使有房间行，也须检查颜色及颜色汇总表。
                        validation_order_id = next(
                            iter(folder_order_ids),
                            display_order_id or Path(str(folder)).name,
                        )
                        parse_order_materials(validation_order_id, path)
                        room_rows = parse_material_room_rows(path)
                        if len(folder_order_ids) > 1 and not room_rows:
                            raise RuleError(
                                "material_room_owner_required",
                                f"{path.name} 同时涉及多个订单，但没有可用的 Room/section 明细；"
                                "请在每个材料明细行填写包含订单号的工厂单名称",
                            )
                        parsed_by_order: dict[str, tuple[list, dict[str, float]]] = {}
                        for material_order_id in folder_order_ids:
                            if room_rows and (
                                len(folder_order_ids) > 1
                                or _room_has_explicit_order_identity(room_rows)
                            ):
                                parsed_materials, parsed_edges, room_warnings = _select_room_materials(
                                    room_rows,
                                    material_order_id,
                                    {},
                                    known_order_ids=set(folder_order_ids),
                                )
                                if room_warnings and not parsed_materials and not parsed_edges:
                                    raise RuleError("material_room_owner_required", room_warnings[0])
                            else:
                                _, parsed_materials, parsed_edges = parse_order_materials(material_order_id, path)
                            if not parsed_materials and not parsed_edges:
                                raise RuleError(
                                    "material_room_owner_required",
                                    f"{material_order_id} 没有匹配到有效材料明细；请检查 Room/section 中的工厂单名称",
                                )
                            parsed_by_order[material_order_id] = (parsed_materials, parsed_edges)

                        mappings = inventory_mappings
                        if mappings is None:
                            raise RuleError("material_mapping", "库存映射数据库尚未准备好")
                        # 商品解析通过另一个 SQLite 连接读取规则；先提交来源元数据更新，避免阻塞该读连接。
                        store.commit()
                        for material_order_id, (parsed_materials, parsed_edges) in parsed_by_order.items():
                            resolution_items = [
                                (
                                    TravelerItem(
                                        row=index,
                                        section="板材与封边",
                                        name=_material_inventory_name(item.kind, item.thickness, item.color),
                                        quantity=item.quantity,
                                        document_remark=material_order_id,
                                    ),
                                    "",
                                )
                                for index, item in enumerate(parsed_materials, start=1)
                                if float(item.quantity or 0) > MATERIAL_ALLOCATION_EPSILON
                            ]
                            resolution_items.extend(
                                (
                                    TravelerItem(
                                        row=len(resolution_items) + index,
                                        section="板材与封边",
                                        name=f"Edge banding--{color}",
                                        quantity=quantity,
                                        document_remark=material_order_id,
                                    ),
                                    "",
                                )
                                for index, (color, quantity) in enumerate(parsed_edges.items(), start=1)
                                if float(quantity or 0) > MATERIAL_ALLOCATION_EPSILON
                            )
                            resolution = resolve_inventory_items(config, resolution_items)
                            if resolution["missing"]:
                                names = "、".join(dict.fromkeys(
                                    str(item.get("name", "")).strip()
                                    for item in resolution["missing"]
                                    if str(item.get("name", "")).strip()
                                )) or "材料"
                                raise RuleError(
                                    "material_mapping",
                                    f"订单 {material_order_id.upper()} 存在未完成商品 SKU 处理：{names}；"
                                    "请先设置映射或加入全局忽略清单，暂未写入新的材料事实。",
                                )

                        for material_order_id, (parsed_materials, parsed_edges) in parsed_by_order.items():
                            _replace_server_material_facts(
                                store,
                                material_order_id,
                                path,
                                parsed_materials,
                                parsed_edges,
                                mappings,
                                server_seen,
                            )
                            store.connection.execute(
                                "update orders set updated_at = ? where order_id = ?",
                                (server_seen, material_order_id.upper()),
                            )
                            resolved_mapping_order_ids.add(material_order_id.upper())
                        for issue in store.active_issues():
                            if (
                                issue.get("kind") == "material_validation"
                                and str(issue.get("path") or "") == str(path)
                            ):
                                store.resolve_active_issue(issue["issue_key"])
                    except Exception as exc:
                        if not isinstance(exc, RuleError):
                            exc = RuleError(
                                "material_validation",
                                f"无法读取或校验 material：{exc}",
                            )
                        issue_key = f"material_validation:{display_order_id}:{path}"
                        issue_message = f"material 文件 {path.name} 校验未通过：{exc}"
                        current_issue_keys.add(issue_key)
                        store.upsert_active_issue(
                            issue_key=issue_key,
                            kind="material_validation",
                            order_id=display_order_id,
                            path=str(path),
                            message=issue_message,
                            seen_at=server_seen,
                        )
                        store.add_change(
                            severity="warning",
                            kind="material_validation",
                            order_id=display_order_id,
                            message=issue_message,
                            path=str(path),
                            observed_at=server_seen,
                        )
                        continue
                if manual_folder and kind in {"board", "fittings"}:
                    continue
                if (
                    not file_change_type
                    and not full_refresh
                    and not (kind == "fittings" and current_report_context() is not None and current_report_context().choices)
                    and kind in {"board", "fittings"}
                    and _merge_cached_server_candidate(
                        store,
                        candidates,
                        path,
                        folder=folder,
                        folder_order_ids=folder_order_ids,
                        manual_folder=manual_folder,
                    )
                ):
                    server_reused_paths.append(str(path))
                    for factory_order in str(
                        store.connection.execute(
                            "select factory_order from source_files where path = ?",
                            (str(path),),
                        ).fetchone()[0]
                    ).split(","):
                        if factory_order:
                            server_factory_orders.add(factory_order.upper())
                    continue
                if kind in {"board", "fittings"}:
                    server_parsed_paths.append(str(path))
                if kind == "board":
                    try:
                        factory_order, name = parse_board_identity(path)
                        order_hint = _order_id_from_factory_name(name) or (
                            folder_order_ids[0] if len(folder_order_ids) == 1 else ""
                        )
                        if (
                            order_hint
                            and config.storage_prepared
                            and _is_recut_server_report(path, folder)
                        ):
                            if inventory_mappings is None:
                                raise RuleError(
                                    "material_mapping",
                                    "库存映射数据库尚未准备好，无法读取 recut 板材增量",
                                )
                            report_materials = _board_report_materials(
                                path, order_hint, allow_unscoped=False
                            )
                            incremental_materials = [
                                MaterialItem("plywood", thickness, "", quantity)
                                for thickness, quantity in report_materials["plywood"].items()
                                if quantity
                            ]
                            incremental_materials.extend(
                                MaterialItem("panel", thickness, color, quantity)
                                for (thickness, color), quantity in report_materials["panels"].items()
                                if quantity
                            )
                            _replace_server_incremental_material_facts(
                                store,
                                order_hint,
                                path,
                                incremental_materials,
                                report_materials["edges"],
                                inventory_mappings,
                                server_seen,
                            )
                            store.connection.execute(
                                "update orders set updated_at=? where order_id=?",
                                (server_seen, order_hint.upper()),
                            )
                        store.update_source_file_identity(
                            path,
                            order_id=order_hint,
                            factory_order=factory_order,
                        )
                        server_factory_orders.add(factory_order.upper())
                        if file_change_type:
                            changed_factory_orders.add(factory_order.upper())
                            store.add_change(
                                severity="info",
                                kind="server_data",
                                order_id=order_hint,
                                factory_order=factory_order,
                                message=_server_data_change_message(
                                    file_change_type,
                                    [order_hint] if order_hint else folder_order_ids,
                                    factory_order,
                                    _source_file_data_label(kind),
                                    str(path),
                                ),
                                path=str(path),
                            )
                        _merge_candidate(
                            candidates,
                            factory_order,
                            name=name,
                            source="server",
                            folder=str(folder),
                            derive_order_from_name=not manual_folder,
                        )
                        if file_change_type:
                            changed_order_ids.update(
                                order_id.upper()
                                for order_id in ([order_hint] + folder_order_ids)
                                if order_id
                            )
                    except Exception as exc:
                        issue_key = f"report_error:{path}"
                        origin = "本地数据库" if isinstance(exc, sqlite3.Error) else "Server 板材报表/本地校验"
                        issue_message = f"{origin}：订单 {','.join(folder_order_ids) or '未识别'}；文件 {path}：{exc}"
                        current_issue_keys.add(issue_key)
                        store.upsert_active_issue(
                            issue_key=issue_key,
                            kind="report_error",
                            order_id=folder_order_ids[0] if len(folder_order_ids) == 1 else "",
                            path=str(path),
                            message=issue_message,
                            seen_at=server_seen,
                        )
                        store.add_change(
                            severity="warning",
                            kind="report_error",
                            message=issue_message,
                            path=str(path),
                        )
                elif kind == "fittings":
                    # 目录推导的订单提示须同时供成功和错误路径使用；损坏的五金报表应报告自身问题，不能因变量未初始化再抛异常。
                    order_hint = folder_order_ids[0] if len(folder_order_ids) == 1 else ""
                    factory_orders = []
                    store.commit()  # 发现阶段元数据只是证据，不是已确认五金事实。
                    report_write_started = False
                    try:
                        groups = _preview_fittings_groups(path, fittings_cache)
                        factory_orders = [factory_order for factory_order, _ in groups]
                        server_factory_orders.update(factory_order.upper() for factory_order in factory_orders)
                        selected_groups = [
                            (factory_order, items)
                            for factory_order, items in groups
                            if (
                                not (
                                    current_report_context()
                                    and factory_order.upper() in current_report_context().keep_factories
                                    and (
                                        current_report_context().locked_decisions.get(
                                            factory_order.upper(), {}
                                        ).get("handling") == "manual"
                                        or store.connection.execute(
                                            "select 1 from hardware_items where factory_order=? and source_type='aicnc' limit 1",
                                            (factory_order.upper(),),
                                        ).fetchone()
                                    )
                                )
                                and selected_fittings.get(factory_order.upper()) is not None
                                and same_selected_fittings_source(
                                    selected_fittings[factory_order.upper()], path, items
                                )
                            )
                        ]
                        if config.storage_prepared:
                            from .inventory import ignored_hardware_reason, resolve_inventory_items, resolved_product_code, TravelerItem

                            mappings = inventory_mappings
                            if mappings is None:
                                raise RuleError("hardware_mapping", "库存映射数据库尚未准备好")
                            if (
                                not fittings_selection_error
                                and selected_groups
                                and not order_hint.upper().startswith("CS")
                            ):
                                resolution_items = [
                                    (
                                        TravelerItem(
                                            row=index,
                                            section="五金",
                                            name=item.name,
                                            quantity=item.quantity,
                                            document_remark="",
                                        ),
                                        item.code,
                                    )
                                    for index, item in enumerate(
                                        (item for _, items in selected_groups for item in items),
                                        start=1,
                                    )
                                ]
                                resolution = resolve_inventory_items(config, resolution_items)
                                if resolution["missing"]:
                                    names = "、".join(dict.fromkeys(
                                        str(item.get("name", "")).strip()
                                        for item in resolution["missing"]
                                        if str(item.get("name", "")).strip()
                                    )) or "五金"
                                    issue_key = f"hardware_mapping:{order_hint.upper()}:{path}"
                                    issue_message = (
                                        f"订单 {order_hint.upper()} 存在未完成商品 SKU 处理：{names}；"
                                        "请先设置映射或加入全局忽略清单，暂未写入新的五金事实。"
                                    )
                                    current_issue_keys.add(issue_key)
                                    store.upsert_active_issue(
                                        issue_key=issue_key,
                                        kind="hardware_mapping",
                                        order_id=order_hint,
                                        path=str(path),
                                        message=issue_message,
                                        seen_at=server_seen,
                                    )
                                    store.add_change(
                                        severity="warning",
                                        kind="hardware_mapping",
                                        order_id=order_hint,
                                        message=issue_message,
                                        path=str(path),
                                        observed_at=server_seen,
                                    )
                                    continue
                                hardware_rows_by_factory: dict[str, list[dict]] = {}
                                accepted_index = 0
                                for factory_order, items in selected_groups:
                                    normalized_factory_order = factory_order.upper()
                                    current_aimes_owner = next(
                                        (
                                            str(row.get("sales_order_name", "")).upper()
                                            for row in aimes_rows
                                            if str(row.get("factory_order", "")).upper() == factory_order.upper()
                                            and str(row.get("sales_order_name", "")).strip()
                                        ),
                                        "",
                                    )
                                    owner_row = store.connection.execute(
                                        "select order_id from factory_orders where factory_order=? and aimes_status='active' and order_id<>''",
                                        (factory_order.upper(),),
                                    ).fetchone()
                                    hardware_order_id = current_aimes_owner or (str(owner_row[0]).upper() if owner_row else order_hint.upper())
                                    hardware_rows = hardware_rows_by_factory.setdefault(
                                        normalized_factory_order,
                                        [],
                                    )
                                    for item in items:
                                        accepted = resolution.get("accepted", [])[accepted_index] if accepted_index < len(resolution.get("accepted", [])) else {}
                                        accepted_index += 1
                                        if ignored_hardware_reason(mappings, item.name, item.code) is not None:
                                            continue
                                        product_code = resolved_product_code(resolution, accepted_index - 1)
                                        hardware_rows.append({
                                            "order_id": hardware_order_id,
                                            "factory_order": normalized_factory_order,
                                            "product_code": product_code,
                                            "quantity": server_hardware_quantity(
                                                product_code, item.quantity, item.unit,
                                                factory_order=normalized_factory_order, name=item.name,
                                            )["quantity"],
                                        })
                                store.connection.execute("savepoint fittings_report_write")
                                report_write_started = True
                                for factory_order, hardware_rows in hardware_rows_by_factory.items():
                                    replace_factory_hardware(
                                        store.connection, factory_order, hardware_rows,
                                        source_path=str(path), observed_at=server_seen,
                                        allow_empty=True,
                                    )
                                context = current_report_context()
                                if context:
                                    for factory_order in hardware_rows_by_factory:
                                        proposal = context.decision_proposals.get(factory_order)
                                        if proposal:
                                            store.connection.execute('insert into hardware_source_decisions(factory_order,decision_json) values(?,?) '
                                                'on conflict(factory_order) do update set decision_json=excluded.decision_json',
                                                (factory_order, json.dumps(proposal, ensure_ascii=False, sort_keys=True)))
                                resolved_mapping_order_ids.add(order_hint.upper())
                        if not report_write_started:
                            store.connection.execute("savepoint fittings_report_write")
                            report_write_started = True
                        store.update_source_file_identity(
                            path,
                            order_id=order_hint,
                            factory_order=",".join(factory_orders),
                        )
                        if file_change_type:
                            changed_factory_orders.update(
                                factory_order.upper() for factory_order in factory_orders
                            )
                            for factory_order in factory_orders:
                                store.add_change(
                                    severity="info",
                                    kind="server_data",
                                    order_id=order_hint,
                                    factory_order=factory_order,
                                    message=_server_data_change_message(
                                        file_change_type,
                                        [order_hint] if order_hint else folder_order_ids,
                                        factory_order,
                                        _source_file_data_label(kind),
                                        str(path),
                                    ),
                                    path=str(path),
                                )
                        for factory_order, items in groups:
                            _merge_candidate(
                                candidates,
                                factory_order,
                                source="server",
                                folder=str(folder),
                                order_id=order_hint,
                                has_hardware=any(item.quantity > 0 for item in items),
                                derive_order_from_name=not manual_folder,
                            )
                        if file_change_type:
                            changed_order_ids.update(
                                order_id.upper() for order_id in folder_order_ids if order_id
                            )
                        store.connection.execute("release fittings_report_write")
                    except Exception as exc:
                        if report_write_started:
                            store.connection.execute("rollback to fittings_report_write")
                            store.connection.execute("release fittings_report_write")
                        if isinstance(exc, RuleError) and _fittings_report_is_empty(path):
                            store.add_change(
                                severity="info",
                                kind="report_empty",
                                order_id=order_hint,
                                message=f"五金报表 {path.name} 没有内容，已按无五金处理",
                                path=str(path),
                            )
                        else:
                            issue_key = f"report_error:{path}"
                            origin = "本地数据库" if isinstance(exc, sqlite3.Error) else "Server 报表/本地校验"
                            issue_message = f"{origin}：订单 {order_hint or '未识别'}；工厂单 {','.join(factory_orders) or '未识别'}；文件 {path}：{exc}"
                            current_issue_keys.add(issue_key)
                            store.upsert_active_issue(
                                issue_key=issue_key,
                                kind="report_error",
                                order_id=order_hint,
                                path=str(path),
                                message=issue_message,
                                seen_at=server_seen,
                            )
                            store.add_change(
                                severity="warning",
                                kind="report_error",
                                order_id=order_hint,
                                message=issue_message,
                                path=str(path),
                            )

    finish_phase("server_metadata_and_report_sync")

    candidates = {
        factory_order: candidate
        for factory_order, candidate in candidates.items()
        if not _factory_order_before_initial_date(
            factory_order,
            next(iter(candidate.get("split_times", set())), ""),
            config.initial_date,
        )
    }
    _merge_database_factory_candidates(store, candidates)
    exact_lookup_error = _exact_resolve_unowned_factories(config, candidates)
    effective = {}
    outbound_records = _load_outbound_records(config) if refresh_outbound_statuses else []
    outbound_metadata = {
        str(row[0]).upper(): (str(row[1] or ""), str(row[2] or ""))
        for row in store.connection.execute(
            "select factory_order, outbound_mode, outbound_fingerprint from factory_orders"
        ).fetchall()
    }
    for factory_order, candidate in candidates.items():
        item = _effective_factory_candidate(factory_order, candidate)
        effective[factory_order] = item
        if item["order_id"]:
            order_id_key = item["order_id"].upper()
            source_folder = str(canonical_order_folders.get(order_id_key, item["source_folder"]))
            store.upsert_order(item["order_id"], source_folder=source_folder, server_seen=server_seen, aimes_seen=_now() if item["name_source"] == "AIMES" else "")
        if item["ownership_status"] != "已确认":
            issue_key = f"factory_ownership:{factory_order}"
            issue_message = f"工厂单 {factory_order} 的订单归属无法唯一确认，请人工处理"
            if exact_lookup_error:
                issue_message += f"；AIMES 精确查询未完成：{exact_lookup_error}"
            current_issue_keys.add(issue_key)
            store.upsert_active_issue(
                issue_key=issue_key,
                kind="factory_ownership",
                order_id=item["order_id"],
                factory_order=factory_order,
                path=item["source_folder"],
                message=issue_message,
                seen_at=server_seen,
            )
            store.add_change(
                severity="warning",
                kind="factory_ownership",
                order_id=item["order_id"],
                factory_order=factory_order,
                message=issue_message,
                path=item["source_folder"],
            )
        item["outbound_mode"], item["outbound_fingerprint"] = outbound_metadata.get(
            factory_order.upper(), ("", "")
        )
        if refresh_outbound_statuses:
            outbound_status, outbound_document = _refresh_outbound_status(
                config,
                item,
                outbound_records,
            )
            if (
                outbound_status == "已出库"
                and (
                    factory_order.upper() in changed_factory_orders
                    or item["order_id"].upper() in changed_order_level_ids
                )
                # 订单材料来源可独立于工厂单五金出货变化；本地五金单仍已确认时，不重新打开已出货状态。
                and not _has_factory_hardware_outbound_record(item, outbound_records)
            ):
                outbound_status = "需要更新"
        else:
            outbound_status = None
            outbound_document = None
        item["outbound_status"] = outbound_status
        item["outbound_document"] = outbound_document
        store.upsert_factory(
            factory_order,
            order_id=item["order_id"],
            factory_name=item["factory_name"],
            sales_order_name=item["sales_order_name"],
            split_time=item["split_time"],
            name_source=item["name_source"],
            source_folder=item["source_folder"],
            report_state="已发现" if item["source_folder"] else "AIMES已发现",
            ownership_status=item["ownership_status"],
            has_hardware=item["has_hardware"],
            optimized=item["optimized"],
            outbound_status=outbound_status,
            outbound_document=outbound_document,
            server_seen=server_seen if item["source_folder"] else "",
            aimes_seen=_now() if item["name_source"] == "AIMES" else "",
        )
    finish_phase("candidate_resolution_and_status")

    if root is not None:
        for old_path in sorted(previous_source_paths - seen_source_paths):
            previous_folder = previous_source_metadata.get(old_path, {}).get("source_folder", "")
            if selected_folder is None and selected_folders is None and previous_folder not in scanned_folder_paths:
                continue
            if selected_folder is not None and not _path_is_within(Path(old_path), root):
                continue
            if selected_folders is not None and previous_folder not in scanned_server_folders:
                continue
            previous = previous_source_metadata.get(old_path, {})
            kind = previous.get("kind", "")
            order_id = previous.get("order_id", "")
            if not order_id:
                order_id = Path(previous.get("source_folder", "")).name.upper()
            factory_orders = [
                value for value in str(previous.get("factory_order", "")).split(",") if value
            ]
            if kind in {"board", "fittings"} and factory_orders:
                for factory_order in factory_orders:
                    store.add_change(
                        severity="warning",
                        kind="server_data",
                        order_id=order_id,
                        factory_order=factory_order,
                        message=_server_data_change_message(
                            "removed",
                            [order_id],
                            factory_order,
                            _source_file_data_label(kind),
                            old_path,
                        ),
                        path=old_path,
                    )
            else:
                store.add_change(
                    severity="warning",
                    kind="source_removed",
                    order_id=order_id,
                    message=f"删除订单 {order_id or '相关订单'} 的{_source_file_data_label(kind)}：{Path(old_path).name}",
                    path=old_path,
                )
            # 文件缺失只改变发现元数据，不改变已确认材料需求或历史分配；保留事实直至明确替换。
            store.connection.execute("delete from source_files where path = ?", (old_path,))
            if kind in {"board", "fittings", "material"}:
                changed_order_ids.update(
                    order_id.upper()
                    for order_id in [order_id, *str(previous.get("order_id", "")).split("、")]
                    if order_id
                )
    finish_phase("stale_source_cleanup")

    removed_material_orders = _reconcile_authoritative_server_material_sources(
        store, authoritative_material_folders
    )
    changed_order_ids.update(removed_material_orders)
    finish_phase("material_source_scope_reconciliation")

    validation_params: list[str] = []
    # 人工选择目录就是明确请求重查订单，不能因候选解析中的临时 Server 标签而跳过校验，
    # 否则预览库旧错误会让已修复报表一直显示异常。
    if selected_folder is not None or selected_folders is not None:
        selected_validation_folders = sorted(scanned_folder_paths)
        if selected_validation_folders:
            placeholders = ",".join("?" for _ in selected_validation_folders)
            validation_scope_sql = "orders.source_folder in (" + placeholders + ")"
            validation_params.extend(selected_validation_folders)
        else:
            validation_scope_sql = "1 = 0"
    else:
        validation_scope_sql = (
            "factory_orders.name_source = 'AIMES' and "
            "factory_orders.sales_order_name = orders.order_id"
        )
    validation_query = (
        "select distinct orders.order_id, orders.source_folder "
        "from orders join factory_orders on factory_orders.order_id = orders.order_id "
        "where orders.source_folder <> '' "
        "and orders.stage <> '已中止' "
        "and factory_orders.aimes_status = 'active' and ("
        + validation_scope_sql
        + ")"
    )
    all_validation_rows = list(
        store.connection.execute(validation_query, tuple(validation_params)).fetchall()
    )
    full_validation = bool(
        full_refresh
        or process_temporary
        or (
            validate_selected_orders
            and (selected_folder is not None or selected_folders is not None)
        )
    )
    validation_rows = all_validation_rows if full_validation else [
        row for row in all_validation_rows
        if str(row[0]).upper() in changed_order_ids
    ]

    # 按每个逻辑订单校验当前来源，以成功预览作为材料和工厂单证据。
    # preview_order 也会保存标准化事实，先提交报表解析事务，避免阻塞其独立 SQLite 连接。
    validations = store.connection.execute('select * from temp.preview_validation').fetchall()
    store.commit()
    store.close()
    store = OrderIndexStore(config.workflow_database, connection=config.workflow_connection)
    store.connection.executemany('insert or replace into temp.preview_validation values(?,?,?)',validations)
    for order in validation_rows:
        order_id, source_folder = order
        try:
            # 校验不能覆盖刚解析的来源级事实；历史 preview_order 会保存根材料工作簿并抹去补切增量，故在此禁止该覆盖。
            preview = preview_order(
                config, Path(source_folder), order_id, persist_facts=False, include_hardware=include_hardware
            )
            # AIMES 归属不能单独证明材料写入覆盖新工厂单；必须在所选报表或 XML 中有身份，XML 只界定范围，不单独确定状态。
            source_factory_ids = {
                factory.strip().upper()
                for row in store.connection.execute(
                    "select factory_order from source_files where source_folder=? and kind in ('board','fittings')",
                    (source_folder,),
                )
                for factory in str(row[0] or "").split(",") if factory.strip()
            }
            if store.connection.execute(
                "select 1 from material_items where order_id=? and quantity > 0 limit 1", (order_id,)
            ).fetchone():
                for artifact in _optimization_result_artifacts(Path(source_folder)):
                    try:
                        source_factory_ids.update(_optimization_factory_orders(artifact))
                    except (OSError, ET.ParseError):
                        pass
            factory_ids = {
                row[0] for row in store.connection.execute(
                    "select factory_order from factory_orders where order_id=? and aimes_status='active' and ownership_status='已确认'",
                    (order_id,),
                ) if row[0] in source_factory_ids
            }
            store.set_validation(order_id, '正常')
            for factory_order in factory_ids:
                store.connection.execute(
                    """update factory_orders set report_state = '已发现',
                       stage = case when stage in ('已生产','已出货') then stage
                           when exists(select 1 from material_items where order_id=? and quantity>0) then '已优化' else '已拆单' end, updated_at = ?
                       where factory_order = ? and order_id = ?""",
                    (order_id, _now(), factory_order, order_id),
                )
        except Exception as exc:
            validation_message = _business_validation_message(exc)
            indexed_factory_ids = {
                row[0]
                for row in store.connection.execute(
                    "select factory_order from factory_orders where order_id = ? and aimes_status = 'active' and ownership_status = '已确认'",
                    (order_id,),
                ).fetchall()
            }
            optimization_outputs = _optimization_result_artifacts(Path(source_folder))
            if order_id.upper().startswith("CS") and indexed_factory_ids and optimization_outputs:
                # 部分 CUT TO SIZE 导出只有生产报表和排版结果，没有材料工作簿；缺材料须保持待处理，XML 不能单独建立优化状态或处理基准。
                store.set_validation(order_id, '待校验',
                    f"已发现优化产物：{optimization_outputs[0].name}；material 尚未生成，材料数据仍待校验")
                continue
            store.set_validation(order_id, '数据异常', validation_message)
            store.add_change(
                severity="warning",
                kind="order_validation",
                order_id=order_id,
                message=f"订单校验未完成：{validation_message}",
                path=source_folder,
            )
        store.commit()

    artifact_refreshed = _refresh_cached_optimization_artifacts(store, validation_rows)
    finish_phase("order_validation")

    _clear_stale_mapping_validation_status(
        store,
        resolved_mapping_order_ids,
        current_issue_keys,
        server_seen,
    )

    if root is not None:
        store.resolve_active_issues_not_in(
            current_issue_keys,
            scoped_folders=scanned_server_folders,
        )
        try:
            store.save_server_scan_xml_baseline(
                _confirmed_material_folders(store, server_folders),
                _server_scan_xml_entries(_confirmed_material_folders(store, server_folders)),
                observed_at=server_seen,
            )
        except OSError:
            # 可选的扫描基准刷新中即使网络目录消失，已完成的业务同步仍可返回成功。
            pass
    finished = _now()
    store.record_run(
        started,
        finished,
        aimes_attempted=aimes_attempted,
        aimes_succeeded=aimes_succeeded,
        aimes_count=len(aimes_rows),
        server_folder_count=folder_count,
        error="；".join(errors),
    )
    store.commit()
    if reconcile_outbound:
        reconcile_outbound_statuses(config, store, factory_orders=server_factory_orders)
    finish_phase("finalize_and_commit")
    if root is None:
        server_trace = [
            "没有成功读取 Server 订单目录，因此没有解析板材或五金报表。",
            f"订单索引写入到了 {store.path}；错误信息：{'; '.join(errors) or '未知错误'}。",
        ]
    else:
        scanned_roots = sorted({str(folder.parent) for folder in server_folders})
        root_summary = "、".join(scanned_roots) if scanned_roots else str(root)
        server_trace = [
            f"从 Server 目录 {root_summary} 按订单类型读取订单号 {len(server_order_ids)} 个、工厂单号 {len(server_factory_orders)} 个的订单文件夹、板材报表和五金报表；",
            _summarize_server_read_items(server_read_items),
            f"写入到了 {store.path} 的订单、工厂单、报表状态和校验结果。",
        ]
    aimes_trace = _aimes_trace(
        config,
        source="aimes" if aimes_succeeded else "cache",
        rows=aimes_fetched_rows if aimes_succeeded else cached_aimes_source_rows,
        wrote_cache=aimes_succeeded,
        error=errors[0] if errors and should_refresh_aimes and not aimes_succeeded else "",
        warnings=aimes_warnings,
        elapsed_seconds=aimes_duration_seconds,
        stage_durations=aimes_stage_durations,
    )
    phase_trace = [
        "索引阶段耗时："
        + "；".join(f"{name} {duration:.3f} 秒" for name, duration in phase_durations.items())
        + "。"
    ]
    response = {
        "orders": store.summaries(),
        "changes": store.latest_changes(after_id=changes_before),
        "current_issues": store.active_issues(),
        "sync": store.latest_sync(),
        "aimes_issues": [],
        "aimes_warnings": aimes_warnings,
        "aimes_stage_durations": aimes_stage_durations,
        "ignored_aimes": store.ignored_aimes_factories(),
        "assigned_aimes": store.assigned_aimes_factories(),
        "database": str(store.path),
        "aimes_source_file": str(config.workflow_database),
        "operation_trace": {
            "aimes": aimes_trace,
            "server": server_trace,
            "sync": aimes_trace + server_trace + phase_trace,
        },
        "index_stats": {
            "incremental": not full_validation,
            "changed_order_count": len(changed_order_ids),
            "validated_order_count": len(validation_rows),
            "reused_report_count": len(server_reused_paths),
            "parsed_report_count": len(server_parsed_paths),
            "optimization_artifact_refresh_count": artifact_refreshed,
            "aimes_deleted_count": aimes_deleted_count,
            "aimes_deletion_check_error": aimes_deletion_check_error,
            "aimes_duration_seconds": aimes_duration_seconds,
            "server_snapshot_reused": server_snapshot_reused,
            "server_snapshot_entry_count": len(server_snapshot_entries or {}),
            "phase_durations": phase_durations,
        },
    }
    if process_temporary:
        response["temporary_processing"] = {
            "succeeded": temporary_processing_results,
            "failed": [
                {"folder": folder, "message": message}
                for folder, message in sorted(temporary_processing_errors.items())
            ],
        }
        response["pending_server_changes"] = scan_server_changes(config)["server"]["changes"]
    store.close()
    return response


def process_server_folder(
    config: Config,
    folder: Path,
    *,
    include_hardware: bool = True,
    process_temporary: bool = False,
) -> dict:
    """通过正常索引更新流程处理所选来源目录。

    参数：config 为配置；folder 为目录；include_hardware 为是否含五金；process_temporary 为是否处理临时目录。"""
    # 打开或更新索引前先校验人工选择的目录；无效选择必须作为明确错误返回，不能降为界面看似成功的普通警告。
    _server_folders_for_sync(config, folder)
    return sync_order_index(
        config,
        selected_folder=folder,
        process_temporary=process_temporary,
        include_hardware=include_hardware,
    )


def _server_preview_directory(config: Config) -> Path:
    """创建并返回配置 config 下的磁盘预览目录。"""
    directory = config.state_dir / "server-previews"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _server_preview_path(config: Config, token: str) -> Path:
    """校验预览令牌并定位影子数据库；config 为配置，token 为预览令牌。"""
    token = str(token or "").strip()
    if not re.fullmatch(r"[0-9a-f]{32}", token):
        raise ValueError("Server 预览标识无效，请重新扫描")
    path = _server_preview_directory(config) / token / "workflow.sqlite3"
    if not path.is_file():
        raise ValueError("Server 预览已失效，请重新扫描")
    return path


def _clone_workflow_database(config: Config, destination: Path) -> None:
    """通过 SQLite 备份机制复制数据库，不手工复制 WAL；config 为源配置，destination 为目标路径。"""
    destination.parent.mkdir(parents=True, exist_ok=True)
    if config.workflow_database.is_file():
        source = sqlite3.connect(config.workflow_database)
        target = sqlite3.connect(destination)
        try:
            source.backup(target)
        finally:
            target.close()
            source.close()
    else:
        target = sqlite3.connect(destination)
        target.close()


def _preview_config(config: Config, state_dir: Path) -> Config:
    """从 config 派生预览配置并使用隔离状态目录 state_dir。"""
    return Config(
        source_root=config.source_root,
        order_root=state_dir / "travelers",
        template=config.template,
        backup_root=config.backup_root,
        state_dir=state_dir,
        initial_date=config.initial_date,
        server_scan_baseline_folder=config.server_scan_baseline_folder,
        server_scan_baseline_at=config.server_scan_baseline_at,
        aimes_username=config.aimes_username,
        aimes_keychain_service=config.aimes_keychain_service,
        aimes_retry_delays=config.aimes_retry_delays,
        operation_log_enabled=False,
        storage_prepared=True,
    )


def _path_in_folders(path: str, folders: list[str]) -> bool:
    """判断路径 path 是否位于 folders 所列任一目录中。"""
    try:
        path_value = Path(path).expanduser().resolve()
        return any(
            path_value == (folder_value := Path(folder).expanduser().resolve())
            or folder_value in path_value.parents
            for folder in folders
        )
    except (OSError, RuntimeError, ValueError):
        return any(path == folder or path.startswith(folder.rstrip("/") + "/") for folder in folders)


def _server_material_allocation_rows(
    store: OrderIndexStore,
    source_path: str,
    material_key: str,
) -> list[dict]:
    """读取来源材料的订单分配记录；store 为索引库，source_path 为来源路径，material_key 为材料身份键。"""
    rows = store.connection.execute(
        """
        select order_id, allocated_quantity
        from server_material_allocations
        where source_path = ? and source_material_key = ?
        order by order_id
        """,
        (source_path, material_key),
    ).fetchall()
    return [
        {
            "order_id": str(row[0]).upper(),
            "quantity": float(row[1] or 0),
        }
        for row in rows
    ]


def _server_material_preview_row(store: OrderIndexStore, row: dict) -> dict:
    """组装材料行的来源数量及分配预览；store 为索引库，row 为来源材料记录。"""
    source_quantity = float(row.get("quantity", 0) or 0)
    source_path = str(row.get("source_path", "") or "")
    product_code = str(row.get("product_code", "") or "").strip().upper()
    material_key = server_material_identity_key(source_path, product_code)
    allocations = _server_material_allocation_rows(store, source_path, material_key)
    allocated_quantity = sum(item["quantity"] for item in allocations)
    return {
        "material_id": int(row["id"]),
        "source_order_id": str(row.get("order_id", "") or "").upper(),
        "product_code": product_code,
        "material_type": str(row.get("material_type", "") or ""),
        "color": str(row.get("color", "") or ""),
        "thickness": str(row.get("thickness", "") or ""),
        "quantity": source_quantity,
        "source_quantity": source_quantity,
        "allocated_quantity": allocated_quantity,
        "remaining_quantity": max(0.0, source_quantity - allocated_quantity),
        "unit": str(row.get("unit", "") or ""),
        "edge": str(row.get("edge", "") or ""),
        "source_path": source_path,
        "source_fingerprint": str(row.get("source_fingerprint", "") or ""),
        "allocations": allocations,
    }


def _server_material_source_rows(
    store: OrderIndexStore | sqlite3.Connection,
    folder_paths: list[str],
) -> list[dict]:
    """读取所选目录的材料来源行；store 为索引库或连接，folder_paths 为目录路径列表。"""
    connection = store.connection if isinstance(store, OrderIndexStore) else store
    rows = connection.execute(
        """
        select m.id, m.order_id, m.product_code,
               p.material_kind, p.material_color, p.material_thickness,
               m.quantity, p.unit,
               case when p.material_kind='edge' then p.material_color else '' end,
               m.source_path, m.source_fingerprint
        from material_items m
        join products p on p.code=m.product_code
        where m.source_type = 'aihouse'
        order by m.source_path, m.id
        """
    ).fetchall()
    names = (
        "id", "order_id", "product_code", "material_type", "color",
        "thickness", "quantity", "unit", "edge", "source_path",
        "source_fingerprint",
    )
    return [
        dict(zip(names, row))
        for row in rows
        if _path_in_folders(str(row[9] or ""), folder_paths)
    ]


def _server_material_sort_key(item: dict) -> tuple:
    """为材料预览记录 item 生成按类型、属性等排列的稳定排序键。"""
    kind = str(item.get("material_type", "")).casefold()
    try:
        thickness = float(item.get("thickness") or 0)
    except (TypeError, ValueError):
        thickness = 0.0
    return (
        {"plywood": 0, "panel": 1, "back": 2, "edge": 3}.get(kind, 9),
        str(item.get("color", "")).casefold(),
        thickness,
        str(item.get("source_path", "")).casefold(),
        int(item.get("material_id", 0) or 0),
    )


def _server_change_key(*values: object) -> tuple[str, ...]:
    """将可变参数 values 标准化为不区分大小写的比较元组，用于资料差异匹配。"""
    return tuple(str(value or "").strip().casefold() for value in values)


def _sqlite_table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
    """检查数据库连接 connection 中是否存在 table_name 指定的表。"""
    return connection.execute(
        "select 1 from sqlite_master where type='table' and name=?",
        (table_name,),
    ).fetchone() is not None


def _server_material_change_rows(
    current: sqlite3.Connection,
    preview: sqlite3.Connection,
    order_id: str,
    folder_paths: list[str],
) -> list[dict]:
    """比较订单级材料事实，先汇总重复来源行。

    参数：current 为当前库连接；preview 为预览连接；order_id 为订单号；folder_paths 为所选来源目录。"""
    def grouped(connection: sqlite3.Connection, source_paths: list[str]) -> dict[tuple[str, ...], dict]:
        """按商品 SKU 汇总订单材料；connection 为待比较连接，source_paths 为可选来源范围。"""
        if not _sqlite_table_exists(connection, "material_items"):
            return {}
        params: list[object] = [order_id]
        path_clause = ""
        if source_paths:
            path_clause = " and source_path in (" + ",".join("?" for _ in source_paths) + ")"
            params.extend(source_paths)
        rows = connection.execute(
            f"""select m.product_code, p.material_kind, p.material_color,
                       p.material_thickness, p.unit,
                       case when p.material_kind='edge' then p.material_color else '' end,
                       sum(m.quantity)
                from material_items m join products p on p.code=m.product_code
                where m.order_id=? and m.source_type='aihouse'{path_clause}
                group by m.product_code, p.material_kind, p.material_color,
                         p.material_thickness, p.unit""",
            params,
        ).fetchall()
        return {
            _server_change_key(row[0]): {
                "product_code": str(row[0] or ""),
                "material_type": str(row[1] or ""),
                "color": str(row[2] or ""),
                "thickness": str(row[3] or ""),
                "unit": str(row[4] or ""),
                "edge": str(row[5] or ""),
                "quantity": float(row[6] or 0),
            }
            for row in rows
        }

    preview_rows = _server_material_source_rows(preview, folder_paths)
    source_paths = sorted({str(row["source_path"] or "") for row in preview_rows if str(row["source_path"] or "")})
    current_rows = grouped(current, source_paths)
    preview_values: dict[tuple[str, ...], dict] = {}
    for row in preview_rows:
        if str(row["order_id"] or "").strip().upper() != order_id:
            continue
        key = _server_change_key(row["product_code"])
        item = preview_values.setdefault(key, {
            "product_code": str(row["product_code"] or ""),
            "material_type": str(row["material_type"] or ""),
            "color": str(row["color"] or ""),
            "thickness": str(row["thickness"] or ""),
            "unit": str(row["unit"] or ""),
            "edge": str(row["edge"] or ""), "quantity": 0.0,
        })
        item["quantity"] += float(row["quantity"] or 0)
    changes = []
    for key in sorted(set(current_rows) | set(preview_values)):
        old = current_rows.get(key, {})
        new = preview_values.get(key, {})
        old_quantity = float(old.get("quantity", 0) or 0)
        new_quantity = float(new.get("quantity", 0) or 0)
        delta = new_quantity - old_quantity
        if abs(delta) <= MATERIAL_ALLOCATION_EPSILON:
            continue
        base = new or old
        changes.append({
            "change_type": "新增" if old_quantity == 0 else ("删除" if new_quantity == 0 else "数量变化"),
            "product_code": base.get("product_code", ""),
            "material_type": base.get("material_type", ""),
            "color": base.get("color", ""),
            "thickness": base.get("thickness", ""),
            "unit": base.get("unit", ""),
            "edge": base.get("edge", ""),
            "old_quantity": old_quantity,
            "new_quantity": new_quantity,
            "delta": delta,
        })
    return changes


def _server_hardware_changes(
    current: sqlite3.Connection,
    preview: sqlite3.Connection,
    factory_order: str,
) -> list[dict]:
    """比较指定工厂单的五金资料变化；current 为当前库，preview 为预览库，factory_order 为工厂单号。"""
    def grouped(connection: sqlite3.Connection) -> dict[tuple[str, ...], dict]:
        """从连接 connection 按 SKU 汇总当前工厂单五金，不以显示名称或单位差异拆分身份。"""
        if not _sqlite_table_exists(connection, "hardware_items"):
            return {}
        rows = connection.execute(
            """select h.product_code, p.name, p.spec, p.unit, sum(h.quantity)
               from hardware_items h join products p on p.code=h.product_code
               where h.factory_order=? group by h.product_code""",
            (factory_order,),
        ).fetchall()
        grouped_rows: dict[tuple[str, ...], dict] = {}
        for row in rows:
            # SKU 是稳定业务身份；不同导出的五金名称、规格和本地化单位可能不同，比较这些显示字段会制造虚假的删除和新增。
            key = _server_change_key(row[0])
            item = grouped_rows.setdefault(key, {
                "product_code": str(row[0] or ""), "name": str(row[1] or ""),
                "spec": str(row[2] or ""), "unit": str(row[3] or ""),
                "quantity": 0.0,
            })
            item["quantity"] += float(row[4] or 0)
            if not item["name"] and row[1]:
                item["name"] = str(row[1])
        return grouped_rows
    old = grouped(current)
    new = grouped(preview)
    changes = []
    for key in sorted(set(old) | set(new)):
        old_item, new_item = old.get(key, {}), new.get(key, {})
        old_quantity = float(old_item.get("quantity", 0) or 0)
        new_quantity = float(new_item.get("quantity", 0) or 0)
        delta = new_quantity - old_quantity
        if abs(delta) <= MATERIAL_ALLOCATION_EPSILON:
            continue
        base = new_item or old_item
        changes.append({
            "change_type": "新增" if old_quantity == 0 else ("删除" if new_quantity == 0 else "数量变化"),
            "product_code": base.get("product_code", ""), "name": base.get("name", ""),
            "spec": base.get("spec", ""), "unit": base.get("unit", ""),
            "old_quantity": old_quantity, "new_quantity": new_quantity, "delta": delta,
        })
    return changes


def _refresh_server_preview_hardware(
    config: Config,
    preview_path: Path | None,
    folder_paths: list[str],
    *,
    skip_hardware_order_ids: Iterable[str] = (),
    preview_store: OrderIndexStore | None = None,
    fittings_cache: dict | None = None,
) -> list[dict]:
    """使用当前 SKU 规则重建预览五金，正式事实只在用户确认后写入。

    参数：config 为配置；preview_path 为预览库路径；folder_paths 为来源目录；skip_hardware_order_ids 为跳过订单；
    preview_store 为可选已打开预览库；fittings_cache 为请求内解析缓存。
    预览后可能补充商品映射，因此生成预览内容和最终写入前都需重新解析映射。"""
    from .inventory import TravelerItem, resolve_inventory_items, resolved_product_code
    from .order_workflow import parse_fittings_groups

    owns_preview = preview_store is None
    preview = preview_store or OrderIndexStore(preview_path)
    requirements: dict[str, dict] = {}
    skipped_orders = {
        str(order_id or "").strip().upper()
        for order_id in skip_hardware_order_ids
        if str(order_id or "").strip()
    }
    try:
        source_rows = preview.connection.execute(
            """select path, source_folder from source_files
               where kind='fittings' order by path"""
        ).fetchall()
        scoped_rows = [
            (str(path or ""), str(source_folder or ""))
            for path, source_folder in source_rows
            if _path_in_folders(str(source_folder or ""), folder_paths)
            and str(path or "")
        ]
        selected_reports = _selected_hardware_reports(scoped_rows)
        paths = sorted({str(source.path) for source in selected_reports.values()})
        for path in paths:
            try:
                groups = _preview_fittings_groups(Path(path), fittings_cache)
            except Exception:
                # 普通 Server 解析流程已记录损坏报表问题，此辅助步骤只负责 SKU 匹配。
                continue

            group_rows = []
            file_missing: list[dict] = []
            for factory_order, items in groups:
                locked = current_report_context()
                manual_locked = bool(
                    locked
                    and locked.locked_decisions.get(factory_order.upper(), {}).get("handling") == "manual"
                )
                has_automatic_hardware = bool(preview.connection.execute(
                    "select 1 from hardware_items where factory_order=? and source_type='aicnc' limit 1",
                    (factory_order.upper(),),
                ).fetchone())
                if locked and factory_order.upper() in locked.keep_factories and (manual_locked or has_automatic_hardware):
                    continue
                source = selected_reports.get(factory_order.upper())
                if source is None or not same_selected_fittings_source(source, Path(path), items):
                    continue
                factory = preview.connection.execute(
                    """select order_id, (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status from factory_orders
                       where factory_order=? and aimes_status='active'""",
                    (str(factory_order).strip().upper(),),
                ).fetchone()
                if factory is None or str(factory[1] or "") == "已出库":
                    continue
                order_id = str(factory[0] or "").strip().upper()
                if order_id in skipped_orders:
                    # 用户在订单级决定跳过 CUT TO SIZE 五金，不再要求该订单五金匹配，也不重建其预览五金。
                    group_rows.append((str(factory_order).strip().upper(), order_id, items, None))
                    continue
                pairs = [
                    (
                        TravelerItem(
                            row=index,
                            section="五金",
                            name=str(item.name or "").strip(),
                            quantity=float(item.quantity or 0),
                            document_remark="",
                        ),
                        str(item.code or "").strip(),
                    )
                    for index, item in enumerate(items, start=1)
                ]
                resolution = resolve_inventory_items(config, pairs)
                for missing in resolution.get("missing", []):
                    name = str(missing.get("name", "") or missing.get("source_code", "")).strip()
                    if not name:
                        continue
                    key = _server_change_key(name)
                    requirement = requirements.setdefault(key, {
                        "name": name,
                        "source_code": str(missing.get("source_code", "") or ""),
                        "factory_orders": set(),
                        "order_ids": set(),
                        "source_paths": set(),
                        "quantity": 0.0,
                        "message": str(missing.get("message", "需要指定库存 SKU")),
                    })
                    requirement["factory_orders"].add(str(factory_order).strip().upper())
                    requirement["order_ids"].add(order_id)
                    requirement["source_paths"].add(path)
                    requirement["quantity"] += float(missing.get("quantity", 0) or 0)
                    file_missing.append({"name": name, "source_code": str(missing.get("source_code", "") or "")})
                group_rows.append((str(factory_order).strip().upper(), order_id, items, resolution))

            # 预览中不能留下只重建一部分的五金报表；每项都匹配或明确忽略后，整份来源才可放行。
            if file_missing:
                continue
            hardware_rows_by_factory: dict[str, list[dict]] = {}
            for factory_order, order_id, items, resolution in group_rows:
                if resolution is None:
                    continue
                hardware_rows = hardware_rows_by_factory.setdefault(factory_order, [])
                ignored = {
                    (
                        str(item.get("name", "")).strip().casefold(),
                        str(item.get("source_code", "")).strip().casefold(),
                    )
                    for item in resolution.get("ignored", [])
                }
                for index, item in enumerate(items):
                    identity = (
                        str(item.name or "").strip().casefold(),
                        str(item.code or "").strip().casefold(),
                    )
                    if identity in ignored:
                        continue
                    product_code = resolved_product_code(resolution, index)
                    hardware_rows.append({
                        "order_id": order_id,
                        "factory_order": factory_order,
                        "product_code": product_code,
                        "quantity": server_hardware_quantity(
                            product_code, item.quantity, str(item.unit or ""),
                            factory_order=factory_order, name=item.name,
                        )["quantity"],
                    })
            for factory_order, hardware_rows in hardware_rows_by_factory.items():
                replace_factory_hardware(
                    preview.connection, factory_order, hardware_rows,
                    source_path=path, observed_at=_now(), allow_empty=True,
                )
        preview.commit()
    finally:
        if owns_preview:
            preview.close()

    return [
        {
            **item,
            "factory_orders": sorted(item["factory_orders"]),
            "order_ids": sorted(item["order_ids"]),
            "source_paths": sorted(item["source_paths"]),
            "quantity": float(item["quantity"]),
        }
        for item in sorted(requirements.values(), key=lambda value: value["name"].casefold())
    ]


def _server_preview_payload(
    config: Config,
    preview_path: Path | None,
    token: str,
    folders: list[Path],
    include_hardware: bool,
    *,
    preview_store: OrderIndexStore | None = None,
) -> dict:
    """组装 Server 预览中的订单、资料差异和待确认写入记录。

    参数：config 为配置；preview_path 为预览库路径；token 为预览令牌；folders 为来源目录；
    include_hardware 为是否包含五金；preview_store 为可选已打开的预览库。"""
    owns_store = preview_store is None
    store = preview_store or OrderIndexStore(preview_path)
    current = sqlite3.connect(config.workflow_database)
    from .inventory import InventoryMappings
    display_mappings = InventoryMappings(config.workflow_database, connection=current)
    folder_paths = [str(folder) for folder in folders]
    aborted_orders = {
        str(row[0]).upper()
        for row in current.execute("select order_id from orders where stage='已中止'")
    } if _sqlite_table_exists(current, "orders") else set()
    order_ids: set[str] = set()
    source_rows = store.connection.execute(
        "select path, source_folder, kind, order_id, factory_order from source_files"
    ).fetchall()
    # 共享目录中的历史报表仍保留，但已中止订单不进入本次确认及其写入记录。
    source_rows = [
        row for row in source_rows
        if not (
            owners := {value.strip().upper() for value in str(row[3] or "").split("、") if value.strip()}
        ) or not owners.issubset(aborted_orders)
    ]
    for path, source_folder, kind, order_id, factory_order in source_rows:
        if not _path_in_folders(str(source_folder), folder_paths):
            continue
        order_ids.update(
            value.strip().upper()
            for value in str(order_id or "").split("、")
            if value.strip() and value.strip().upper() not in aborted_orders
        )

    material_source_rows = [
        row for row in _server_material_source_rows(store, folder_paths)
        if str(row["order_id"]).upper() not in aborted_orders
    ]
    material_sources = [
        _server_material_preview_row(store, row)
        for row in material_source_rows
    ]
    for item in material_sources:
        if item["source_order_id"]:
            order_ids.add(item["source_order_id"])
    materials_by_order: dict[str, list[dict]] = defaultdict(list)
    for item in material_sources:
        order_id = str(item.get("source_order_id", "")).strip().upper()
        if order_id:
            materials_by_order[order_id].append(item)
    material_sources.sort(key=_server_material_sort_key)
    for items in materials_by_order.values():
        items.sort(key=_server_material_sort_key)

    factory_rows = store.connection.execute(
        """
        select factory_order, order_id, factory_name, sales_order_name, split_time,
               name_source, source_folder, report_state, ownership_status,
               has_hardware, (stage in ('已优化','已生产','已出货')) as optimized, (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document
        from factory_orders
        where order_id <> ''
        order by order_id, factory_order
        """
    ).fetchall()
    factories_by_order: dict[str, list[dict]] = defaultdict(list)
    selected_factories: set[str] = set()
    for row in factory_rows:
        factory_order, order_id = str(row[0]), str(row[1]).upper()
        if order_id in aborted_orders:
            continue
        source_folder = str(row[6] or "")
        if order_id not in order_ids and not _path_in_folders(source_folder, folder_paths):
            continue
        order_ids.add(order_id)
        selected_factories.add(factory_order.upper())
        hardware = []
        if include_hardware:
            hardware = [
                {
                    "product_code": str(item[0] or ""),
                    "name": str(item[1] or ""),
                    "display_name": display_mappings.display_name_for_hardware(
                        str(item[0] or ""), str(item[1] or "")
                    ),
                    "spec": str(item[2] or ""),
                    "quantity": float(item[3] or 0),
                    "unit": str(item[4] or ""),
                    "source_path": str(item[5] or ""),
                }
                for item in store.connection.execute(
                    """
                    select h.product_code, p.name, p.spec, h.quantity, p.unit, h.source_path
                    from hardware_items h join products p on p.code=h.product_code
                    where h.factory_order = ?
                    order by h.id
                    """,
                    (factory_order.upper(),),
                ).fetchall()
            ]
        factories_by_order[order_id].append({
            "factory_order": factory_order,
            "factory_name": str(row[2] or ""),
            "sales_order_name": str(row[3] or ""),
            "split_time": str(row[4] or ""),
            "name_source": str(row[5] or ""),
            "source_folder": source_folder,
            "report_state": str(row[7] or ""),
            "ownership_status": str(row[8] or ""),
            "has_hardware": bool(row[9]),
            "optimized": bool(row[10]),
            "outbound_status": str(row[11] or ""),
            "outbound_document": str(row[12] or ""),
            "hardware": hardware,
            "has_existing_hardware": bool(current.execute(
                "select 1 from hardware_items where factory_order=? limit 1",
                (factory_order.upper(),),
            ).fetchone()),
        })

    orders = []
    for order_id in sorted(order_ids):
        row = store.connection.execute(
            "select order_id, order_type, source_folder, coalesce((select v.status from temp.preview_validation v where v.order_id=orders.order_id),'正常'), coalesce((select v.message from temp.preview_validation v where v.order_id=orders.order_id),''), case when exists(select 1 from material_items m where m.order_id=orders.order_id and m.quantity>0) then '板材 · 封边' else '待校验' end from orders where order_id = ?",
            (order_id,),
        ).fetchone()
        if row is None:
            continue
        source_paths = sorted({
            str(path)
            for path, source_folder, kind, source_order_id, factory_order in source_rows
            if _path_in_folders(str(source_folder), folder_paths)
            and (
                order_id in str(source_order_id or "").upper().split("、")
                or order_id in str(store.connection.execute(
                    "select order_id from factory_orders where factory_order = ?",
                    (str(factory_order or "").split(",")[0].upper(),),
                ).fetchone() or "")
            )
        })
        current_factory_rows = {}
        if _sqlite_table_exists(current, "factory_orders"):
            current_factory_rows = {
                str(row[0]).upper(): row
                for row in current.execute(
                    """select factory_order, factory_name, sales_order_name, split_time,
                              report_state, ownership_status, has_hardware, (stage in ('已优化','已生产','已出货')) as optimized,
                              (case when stage='已出货' then '已出库' else '未出库' end) as outbound_status, outbound_document
                       from factory_orders where order_id=? and aimes_status='active'""",
                    (order_id,),
                ).fetchall()
            }
        actionable_factories: list[dict] = []
        excluded_factories: list[dict] = []
        hardware_changes: list[dict] = []
        for factory in factories_by_order.get(order_id, []):
            factory_order = str(factory["factory_order"]).upper()
            existing = current_factory_rows.get(factory_order)
            if existing is not None and str(existing[8] or "") == "已出库":
                excluded_factories.append({
                    **factory,
                    "exclude_reason": "已出货",
                    "outbound_status": "已出库",
                    "outbound_document": str(existing[9] or ""),
                })
                continue
            identity_changed = existing is None or any([
                str(existing[1] or "") != str(factory["factory_name"] or ""),
                str(existing[2] or "") != str(factory["sales_order_name"] or ""),
                str(existing[3] or "") != str(factory["split_time"] or ""),
                bool(str(existing[5] or "") == "已确认") != bool(factory["ownership_status"] == "已确认"),
                bool(existing[6]) != bool(factory["has_hardware"]),
                bool(existing[7]) != bool(factory["optimized"]),
            ])
            factory_hardware_changes = (
                _server_hardware_changes(current, store.connection, factory_order)
                if include_hardware else []
            )
            factory_hardware_changes = [
                {
                    **change,
                    "display_name": display_mappings.display_name_for_hardware(
                        str(change.get("product_code", "")), str(change.get("name", ""))
                    ),
                }
                for change in factory_hardware_changes
            ]
            for change in factory_hardware_changes:
                hardware_changes.append({"factory_order": factory_order, **change})
            if identity_changed or factory_hardware_changes:
                actionable_factories.append({
                    **factory,
                    "change_type": "新增工厂单" if existing is None else "工厂单信息变化",
                    "hardware_changes": factory_hardware_changes,
                })
        material_changes = _server_material_change_rows(
            current, store.connection, order_id, folder_paths
        )
        orders.append({
            "order_id": order_id,
            "order_type": str(row[1] or ""),
            "source_folder": str(row[2] or ""),
            "validation_status": str(row[3] or ""),
            "validation_message": str(row[4] or ""),
            "material_status": str(row[5] or ""),
            "materials": materials_by_order.get(order_id, []),
            "material_changes": material_changes,
            "factories": actionable_factories,
            "excluded_factories": excluded_factories,
            "hardware_changes": hardware_changes,
            "source_paths": source_paths,
        })
    selected_source_paths = sorted({
        str(path)
        for path, source_folder, *_ in source_rows
        if _path_in_folders(str(source_folder or ""), folder_paths)
    })
    selected_factory_orders = sorted(selected_factories)

    def table_records(table: str, where: str, params: tuple = ()) -> list[dict]:
        """读取预览表的指定记录并转为字典；table 为表名，where 为筛选条件，params 为绑定参数。"""
        columns = [row[1] for row in store.connection.execute(f"pragma table_info({table})").fetchall()]
        if not columns:
            return []
        rows = store.connection.execute(
            f"select {','.join(columns)} from {table} where {where}", params
        ).fetchall()
        return [dict(zip(columns, row)) for row in rows]

    write_records = {
        "orders": table_records(
            "orders",
            "order_id in ({})".format(",".join("?" for _ in order_ids)) if order_ids else "0",
            tuple(sorted(order_ids)),
        ),
        "factory_orders": table_records(
            "factory_orders",
            "factory_order in ({})".format(",".join("?" for _ in selected_factory_orders))
            if selected_factory_orders else "0",
            tuple(selected_factory_orders),
        ),
        "material_items": table_records(
            "material_items",
            "source_path in ({})".format(",".join("?" for _ in selected_source_paths))
            if selected_source_paths else "0",
            tuple(selected_source_paths),
        ),
        "hardware_source_versions": table_records(
            "hardware_source_versions",
            "factory_order in ({})".format(",".join("?" for _ in selected_factory_orders))
            if selected_factory_orders else "0", tuple(selected_factory_orders),
        ),
        "hardware_items": table_records(
            "hardware_items",
            "factory_order in ({})".format(",".join("?" for _ in selected_factory_orders))
            if selected_factory_orders else "0",
            tuple(selected_factory_orders),
        ),
        "source_files": table_records(
            "source_files",
            "path in ({})".format(",".join("?" for _ in selected_source_paths))
            if selected_source_paths else "0",
            tuple(selected_source_paths),
        ),
        "optimization_artifacts": table_records(
            "optimization_artifacts",
            "factory_order in ({}) and order_id in ({})".format(
                ",".join("?" for _ in selected_factory_orders),
                ",".join("?" for _ in order_ids),
            ) if selected_factory_orders and order_ids else "0",
            tuple(selected_factory_orders) + tuple(sorted(order_ids))
            if selected_factory_orders and order_ids else (),
        ),
        "server_scan_xml_state": table_records(
            "server_scan_xml_state",
            "source_folder in ({})".format(",".join("?" for _ in folder_paths))
            if folder_paths else "0", tuple(folder_paths),
        ),
        "server_material_allocations": table_records(
            "server_material_allocations",
            "source_path in ({})".format(",".join("?" for _ in selected_source_paths))
            if selected_source_paths else "0",
            tuple(selected_source_paths),
        ),
    }
    for table in ("material_items", "server_material_allocations"):
        write_records[table] = [
            row for row in write_records[table]
            if str(row.get("order_id", "")).upper() not in aborted_orders
        ]
    no_change_revision = (
        _server_business_revision(current, sorted(order_ids))
        if _sqlite_table_exists(current, "orders") else ""
    )
    current.close()
    if owns_store:
        store.close()
    result = {
        "created_at": _now(),
        "include_hardware": include_hardware,
        "no_change_business_revision": no_change_revision,
        "source_folders": folder_paths,
        "materials": material_sources,
        "orders": orders,
        "has_business_changes": any(
            bool(order.get("material_changes"))
            or bool(order.get("factories"))
            or bool(order.get("hardware_changes"))
            for order in orders
        ),
        "write_records": write_records,
    }
    if token:
        result["token"] = token
    return result


def _server_preview_has_business_changes(payload: dict) -> bool:
    """判断预览内容 payload 是否包含实际业务资料增减变化。"""
    if "has_business_changes" in payload:
        return bool(payload.get("has_business_changes"))
    return any(
        bool(order.get("material_changes"))
        or bool(order.get("factories"))
        or bool(order.get("hardware_changes"))
        for order in payload.get("orders", [])
        if isinstance(order, dict)
    )


def _server_business_revision(connection: sqlite3.Connection, order_ids: list[str]) -> str:
    """计算订单事实版本以检测预览后的本地变化，不包括扫描基准。

    参数：connection 为数据库连接；order_ids 为订单范围。"""
    placeholders = ",".join("?" for _ in order_ids) or "NULL"
    state = {}
    for table in ("orders", "factory_orders", "material_items", "hardware_items"):
        cursor = connection.execute(
            f"select * from {table} where order_id in ({placeholders}) order by rowid",
            tuple(order_ids),
        )
        # 扫描和列表刷新即使事实未变也会更新记录时间，因此版本比较排除这些记账时间。
        columns = [column[0] for column in cursor.description]
        state[table] = [
            {name: value for name, value in zip(columns, row)
             if name not in {"updated_at", "last_seen", "last_server_seen", "last_aimes_seen",
                             "server_scan_policy_updated_at"}}
            for row in cursor.fetchall()
        ]
    state["hardware_source_decisions"] = connection.execute(
        "select * from hardware_source_decisions where factory_order in "
        f"(select factory_order from factory_orders where order_id in ({placeholders})) order by factory_order",
        tuple(order_ids),
    ).fetchall()
    return decision_revision(state)


def _server_preview_can_acknowledge(payload: dict) -> bool:
    """判断预览 payload 是否完整、无业务变化且满足仅确认扫描基准的条件。"""
    orders = payload.get("orders", [])
    return bool(
        orders and payload.get("source_folders") and payload.get("include_hardware")
        and payload.get("no_change_business_revision")
        and isinstance(payload.get("monitoring_xml_entries"), list)
        and payload.get("validation_recomputed")
        and all(order.get("validation_status") == "正常" for order in orders)
        and not any(order.get(key) for order in orders
                    for key in ("material_changes", "factories", "hardware_changes"))
        and not payload.get("has_business_changes")
        and not payload.get("hardware_mapping_requirements")
        and not payload.get("hardware_source_selection", {}).get("conflicts")
        and not any(decision_revision(value) != payload.get("hardware_source_decision_bases", {}).get(factory, "")
                    for factory, value in payload.get("hardware_source_decisions", {}).items())
    )


def acknowledge_server_preview_memory(config: Config, payload: dict, *, confirm_write: bool = False) -> dict:
    """确认完整且无变化的内存预览，只写其 XML 基准。

    参数：config 为配置；payload 为保留的预览；confirm_write 表示明确确认。"""
    if not confirm_write:
        raise RuleError("write_confirmation_required", "更新监控基线需要用户明确确认")
    _memory_preview_records(payload)
    if not _server_preview_can_acknowledge(payload):
        raise RuleError("server_preview_has_changes", "仍有待处理变化或未完成校验，请重新预览并确认写入")
    orders = sorted({str(order["order_id"]) for order in payload["orders"]})
    folders = [Path(folder) for folder in payload["source_folders"]]
    store = OrderIndexStore(config.workflow_database)
    try:
        store.connection.execute("begin immediate")
        if payload.get("no_change_business_revision") != _server_business_revision(store.connection, orders):
            raise RuleError("server_preview_stale", "本地订单事实已变化，请重新预览")
        confirmed_folders = set()
        for order_id in orders:
            row = store.connection.execute(
                "select source_folder from orders where order_id=? and coalesce((select v.status from temp.preview_validation v where v.order_id=orders.order_id),'正常')='正常' and exists (select 1 from material_items where order_id=orders.order_id and quantity>0)",
                (order_id,),
            ).fetchone()
            if row is None:
                raise RuleError("server_preview_unconfirmed", "订单尚无已确认的有效材料，不能确认无变化")
            confirmed_folders.add(Path(row[0]))
        if set(folders) != confirmed_folders:
            raise RuleError("server_preview_unconfirmed", "文件夹与已确认订单材料不一致，请重新预览")
        store.save_server_scan_xml_baseline(
            folders, payload["monitoring_xml_entries"], observed_at=_now(),
        )
        store.commit()
    except Exception:
        store.connection.rollback()
        raise
    finally:
        store.close()
    return {"server_no_changes_confirmed": True, "orders": orders,
            "source_folders": [str(folder) for folder in folders]}


def _server_preview_hardware_source_items(
    preview_store: OrderIndexStore,
    folder_paths: list[str],
    *,
    fittings_cache: dict | None = None,
) -> list[dict]:
    """提取解析后的五金来源事实，供后续内存 SKU 匹配。

    参数：preview_store 为预览库；folder_paths 为所选目录；fittings_cache 为可选解析缓存。"""
    from .order_workflow import parse_fittings_groups

    rows = preview_store.connection.execute(
        "select path, source_folder from source_files where kind='fittings' order by path"
    ).fetchall()
    scoped_rows = [
        (str(path or ""), str(source_folder or ""))
        for path, source_folder in rows
        if _path_in_folders(str(source_folder or ""), folder_paths)
        and str(path or "")
    ]
    selected_reports = _selected_hardware_reports(scoped_rows)
    result: list[dict] = []
    for path, source_folder in scoped_rows:
        path = str(path or "")
        if not path:
            continue
        try:
            groups = _preview_fittings_groups(Path(path), fittings_cache)
        except Exception:
            continue
        for factory_order, items in groups:
            locked = current_report_context()
            manual_locked = bool(
                locked
                and locked.locked_decisions.get(factory_order.upper(), {}).get("handling") == "manual"
            )
            has_automatic_hardware = bool(preview_store.connection.execute(
                "select 1 from hardware_items where factory_order=? and source_type='aicnc' limit 1",
                (factory_order.upper(),),
            ).fetchone())
            if locked and factory_order.upper() in locked.keep_factories and (manual_locked or has_automatic_hardware):
                continue
            source = selected_reports.get(factory_order.upper())
            if source is None or not same_selected_fittings_source(source, Path(path), items):
                continue
            factory = preview_store.connection.execute(
                "select order_id from factory_orders where factory_order=?",
                (str(factory_order).strip().upper(),),
            ).fetchone()
            if factory is None:
                continue
            result.append({
                "factory_order": str(factory_order).strip().upper(),
                "order_id": str(factory[0] or "").strip().upper(),
                "source_path": path,
                "items": [
                    {
                        "code": str(item.code or ""),
                        "name": str(item.name or ""),
                        "spec": str(item.size or ""),
                        "unit": str(item.unit or ""),
                        "quantity": float(item.quantity or 0),
                    }
                    for item in items
                ],
            })
    return result


@preview_read_session
def preview_server_changes(
    config: Config,
    selected_folders: list[Path],
    *,
    include_hardware: bool = True,
    hardware_source_choices: dict[str, str] | None = None,
) -> dict:
    """将所选 Server 目录解析到进程内预览，不在正式库写业务事实。

    参数：config 为配置；selected_folders 为所选目录；include_hardware 为是否包含五金；
    hardware_source_choices 为工厂单到所选来源标识的映射。
    预览以本地库为底本建立内存连接，不在状态目录落盘，也不返回令牌；调用方保留内容直至用户确认。"""
    if not selected_folders:
        raise ValueError("请先选择要预览的 Server 文件夹")
    from .aicnc_import import OPTIMIZATION_RE, preview as preview_optimization
    if any(OPTIMIZATION_RE.fullmatch(folder.name) for folder in selected_folders):
        if len(selected_folders) != 1:
            raise RuleError('aicnc_selection', '请一次选择一个优化文件夹进行分配和确认')
        return preview_optimization(config, selected_folders[0])
    timing_started = time.perf_counter()
    stage_started = timing_started
    timing_stages: list[dict[str, object]] = []

    def finish_timing_stage(stage: str, label: str) -> None:
        """结束并登记预览阶段耗时；stage 为阶段标识，label 为中文显示名称。"""
        nonlocal stage_started
        now = time.perf_counter()
        timing_stages.append({
            "stage": stage,
            "label": label,
            "duration_seconds": round(now - stage_started, 6),
        })
        stage_started = now

    fittings_cache: dict = {}
    normalized_folders = [folder.expanduser().resolve() for folder in selected_folders]
    _, normalized_folders = _server_folders_for_sync(config, None, selected_folders=normalized_folders)
    routing_store = OrderIndexStore(config.workflow_database)
    try:
        for folder in normalized_folders:
            if _server_folder_handling_mode(routing_store, folder) in {"supplemental", "external_manual"}:
                raise RuleError("server_folder_manual_only", f"{folder.name} 是独立人工处理文件夹；请在外部完成出库后登记“已人工处理”")
    finally:
        routing_store.close()
    if not isinstance(hardware_source_choices or {}, dict):
        raise ValueError("五金来源选择必须是工厂单到报表的映射")
    context = current_report_context()
    context.locked_decisions = load_source_decisions(config)
    progress("正在读取五金报表并检查来源冲突")
    selected_sources = {}
    if include_hardware:
        from .order_workflow import _fittings_report_is_empty
        paths = [path for folder in normalized_folders for path, kind in _report_files(folder)
                 if kind == "fittings"]
        try:
            selected_sources, _, _, _ = select_latest_fittings(paths, is_empty_report=_fittings_report_is_empty)
        except RuleError as exc:
            if exc.code == "fittings_selection_required":
                finish_timing_stage("source_selection", "检查五金来源")
                return {"operation_timing": {"total_seconds": round(time.perf_counter() - timing_started, 6), "stages": timing_stages},
                        "hardware_source_selection": {
                    "source_folders": [str(folder) for folder in normalized_folders],
                    "include_hardware": include_hardware,
                    "choices": hardware_source_choices or {},
                    "conflicts": exc.context["conflicts"],
                }}
            # 保留原有详细工作簿校验及错误展示。
    context.decisions_prepared = True
    finish_timing_stage("source_selection", "检查五金来源")
    # 影子库必须先包含当前商品目录，解析材料才能绑定 SKU 外键及业务属性；
    # 若备份后才导入商品，只有磁盘库更新，内存预览中的商品表仍可能为空。
    from .inventory import bootstrap_product_database
    bootstrap_product_database(config)
    memory = sqlite3.connect(":memory:")
    if config.workflow_database.is_file():
        source = sqlite3.connect(config.workflow_database)
        try:
            source.backup(memory)
        finally:
            source.close()
    stage_config = _preview_config(config, config.state_dir)
    stage_config.workflow_connection = memory
    preview_store = OrderIndexStore(config.workflow_database, connection=memory)
    try:
        # 发现快照与优化证据分别保存；部分优化目录可确认未变文件，但不能因此把其余工厂单标为优化，后续版本仍待处理。
        monitoring_xml_entries = _server_scan_xml_entries(normalized_folders)
        finish_timing_stage("preview_database", "复制中央数据库到内存预览")
        # 预览不执行临时出库或 Traveler 生成，这些属于单独批准的操作。
        progress("正在读取材料并核对数据库中的工厂单归属")
        sync_result = sync_order_index(
            stage_config,
            selected_folders=normalized_folders,
            process_temporary=False,
            include_hardware=include_hardware,
            full_refresh=False,
            validate_selected_orders=True,
            refresh_outbound_statuses=False,
            reconcile_outbound=False,
            fittings_cache=fittings_cache,
        )
        finish_timing_stage("server_parse", "读取、解析并校验 Server 文件")
        material_issues = preview_store.connection.execute(
            "select path, message from pending_issues where kind = 'material_validation' and status = 'open' order by path"
        ).fetchall()
        if material_issues:
            issue_details = [
                {"path": str(path or ""), "message": str(message or "")}
                for path, message in material_issues
                if _path_in_folders(str(path or ""), [str(folder) for folder in normalized_folders])
            ]
            if issue_details:
                summary = "；".join(
                    f"{item['path']}: {item['message']}" for item in issue_details
                )
                raise RuleError(
                    "material_validation",
                    f"材料文件尚未通过校验：{summary}。请处理上述映射或文件校验问题后重新预览",
                    issues=issue_details,
                )
        preview_store.connection.executemany(
            "insert or replace into server_material_preview_scopes(source_folder) values(?)",
            [(str(folder),) for folder in normalized_folders],
        )
        preview_store.commit()
        hardware_mapping_requirements = (
            _refresh_server_preview_hardware(
                config, None, [str(folder) for folder in normalized_folders],
                preview_store=preview_store, fittings_cache=fittings_cache,
            )
            if include_hardware else []
        )
        # 五金映射解决后再生成最终差异。
        progress("正在组装材料、五金及写入差异预览")
        payload = _server_preview_payload(
            config, None, "", normalized_folders, include_hardware,
            preview_store=preview_store,
        ) | {
            "validation_recomputed": True,
            "monitoring_xml_entries": monitoring_xml_entries,
            "hardware_source_decisions": context.decision_proposals,
            "hardware_source_decision_bases": {factory: decision_revision(value) for factory, value in context.locked_decisions.items()},
            "hardware_keep_factories": sorted(context.keep_factories),
            "hardware_source_choices": hardware_source_choices or {},
            "hardware_source_selection": {
                "source_folders": [str(folder) for folder in normalized_folders],
                "include_hardware": include_hardware,
                "choices": hardware_source_choices or {},
                "conflicts": list(current_report_context().source_conflicts.values()),
            },
            "hardware_selected_sources": [dict(factory_order=factory, **fittings_candidate(source))
                                          for factory, source in selected_sources.items()],
            "hardware_mapping_requirements": hardware_mapping_requirements,
            "hardware_source_items": _server_preview_hardware_source_items(
                preview_store, [str(folder) for folder in normalized_folders],
                fittings_cache=fittings_cache,
            ) if include_hardware else [],
        }
        if not payload["orders"]:
            raise ValueError("Server 文件夹中没有解析出可确认的订单和工厂单")
        payload["can_acknowledge_no_changes"] = _server_preview_can_acknowledge(payload)
        finish_timing_stage("preview_build", "生成材料、五金和写入差异预览")
        return {
            "server_write_preview": payload,
            "operation_timing": {
                "total_seconds": round(time.perf_counter() - timing_started, 6),
                "stages": timing_stages,
                "server_parse_phases": sync_result["index_stats"]["phase_durations"],
            },
        }
    finally:
        preview_store.close()
        memory.close()


def allocate_server_material(
    config: Config,
    token: str,
    material_id: int,
    order_id: str,
    quantity: float,
) -> dict:
    """在影子数据库中登记订单级材料分配。

    参数：config 为配置；token 为预览令牌；material_id 为来源材料编号；order_id 为目标订单；quantity 为分配数量。"""
    preview_path = _server_preview_path(config, token)
    order_id = str(order_id or "").strip().upper()
    try:
        quantity = float(quantity)
    except (TypeError, ValueError) as exc:
        raise ValueError("分配数量必须是数字") from exc
    if not order_id:
        raise ValueError("材料分配需要目标订单号")
    if not math.isfinite(quantity) or quantity <= MATERIAL_ALLOCATION_EPSILON:
        raise ValueError("分配数量必须大于 0")
    preview = OrderIndexStore(preview_path)
    try:
        if preview.connection.execute(
            "select 1 from orders where order_id = ?", (order_id,)
        ).fetchone() is None:
            raise ValueError("所选订单不在本次 Server 预览中")
        raw_row = preview.connection.execute(
            """
            select m.id, m.order_id, m.product_code,
                   p.material_kind, p.material_color, p.material_thickness,
                   m.quantity, p.unit,
                   case when p.material_kind='edge' then p.material_color else '' end,
                   m.source_path, m.source_fingerprint
            from material_items m join products p on p.code=m.product_code
            where m.id = ? and m.source_type = 'aihouse'
            """,
            (int(material_id),),
        ).fetchone()
        if raw_row is None:
            raise ValueError("所选材料明细不在本次 Server 预览中")
        row = dict(zip((
            "id", "order_id", "product_code", "material_type", "color",
            "thickness", "quantity", "unit", "edge", "source_path",
            "source_fingerprint",
        ), raw_row))
        source_quantity = float(row["quantity"] or 0)
        source_path = str(row["source_path"] or "")
        product_code = str(row["product_code"] or "").strip().upper()
        material_key = server_material_identity_key(source_path, product_code)
        allocation_rows = preview.connection.execute(
            """
            select id, order_id, allocated_quantity
            from server_material_allocations
            where source_path = ? and source_material_key = ?
            """,
            (source_path, material_key),
        ).fetchall()
        allocated = sum(float(item[2] or 0) for item in allocation_rows)
        remaining = source_quantity - float(allocated or 0)
        if quantity - remaining > MATERIAL_ALLOCATION_EPSILON:
            raise ValueError(
                f"分配数量超过剩余数量：剩余 {remaining:g} {row['unit'] or ''}，本次 {quantity:g}"
            )
        now = _now()
        existing = next(
            (item for item in allocation_rows if str(item[1]).upper() == order_id),
            None,
        )
        if existing is None:
            preview.connection.execute(
                """
                insert into server_material_allocations(
                    source_path, source_material_key, product_code,
                    source_quantity, order_id, allocated_quantity,
                    source_fingerprint, created_at, updated_at
                ) values(?,?,?,?,?,?,?,?,?)
                """,
                (
                    source_path, material_key, product_code, source_quantity,
                    order_id, quantity, str(row["source_fingerprint"] or ""),
                    now, now,
                ),
            )
        else:
            preview.connection.execute(
                """
                update server_material_allocations
                set allocated_quantity = ?, updated_at = ?
                where id = ?
                """,
                (float(existing[2]) + quantity, now, int(existing[0])),
            )
        preview.connection.commit()
        material = _server_material_preview_row(preview, row)
        return {
            "server_material_allocated": True,
            "material": material,
            "order_id": order_id,
        }
    finally:
        preview.close()


def _memory_preview_records(payload: dict) -> dict[str, list[dict]]:
    """校验并提取内存预览 payload 中按表分类的待写记录。"""
    records = payload.get("write_records")
    if not isinstance(records, dict):
        raise ValueError("Server 预览数据不完整，请重新读取文件夹")
    normalized: dict[str, list[dict]] = {}
    for table, rows in records.items():
        if not isinstance(rows, list):
            raise ValueError(f"Server 预览记录格式无效：{table}")
        normalized[table] = [row for row in rows if isinstance(row, dict)]
    return normalized


def _memory_factory_selection(payload: dict, order_id: str = "", factory_order: str = "") -> list[tuple[str, str]]:
    """提取内存预览的订单与工厂单选择集合；payload 为预览，order_id、factory_order 为可选选择限制。"""
    selected: set[tuple[str, str]] = set()
    wanted_order = str(order_id or "").strip().upper()
    wanted_factory = str(factory_order or "").strip().upper()
    payload_order_ids = {
        str(item.get("order_id", "")).strip().upper()
        for item in payload.get("orders", [])
        if isinstance(item, dict) and str(item.get("order_id", "")).strip()
    }
    if wanted_order:
        payload_order_ids.add(wanted_order)
    for order in payload.get("orders", []):
        if not isinstance(order, dict):
            continue
        current_order = str(order.get("order_id", "")).strip().upper()
        if wanted_order and current_order != wanted_order:
            continue
        for factory in order.get("factories", []):
            if not isinstance(factory, dict):
                continue
            current_factory = str(factory.get("factory_order", "")).strip().upper()
            if current_factory and (not wanted_factory or current_factory == wanted_factory):
                selected.add((current_factory, current_order))
    # 有新五金来源的工厂单即使身份字段未变、未出现在可视变化列表中，也必须保留可选资格，
    # 避免仅依据 AICNC 证据推导优化状态时绕过商品映射校验。
    for group in payload.get("hardware_source_items", []):
        if not isinstance(group, dict):
            continue
        current_order = str(group.get("order_id", "")).strip().upper()
        current_factory = str(group.get("factory_order", "")).strip().upper()
        if wanted_order and current_order != wanted_order:
            continue
        if current_factory and current_order and (not wanted_factory or current_factory == wanted_factory):
            selected.add((current_factory, current_order))
    for row in payload.get('write_records', {}).get('factory_orders', []):
        factory = str(row.get('factory_order', '')).upper()
        owner = str(row.get('order_id', '')).upper()
        if factory in payload.get('hardware_source_decisions', {}) and owner in payload_order_ids:
            if (not wanted_factory or factory == wanted_factory) and (not wanted_order or owner == wanted_order):
                selected.add((factory, owner))
    return sorted(selected)


def _server_preview_order_validation_errors(
    orders: Iterable[dict],
    selected_order_ids: set[str] | None = None,
    *,
    require_recomputed: bool = False,
) -> list[str]:
    """收集应阻止确认的订单校验错误。

    参数：orders 为预览订单；selected_order_ids 为可选确认范围；require_recomputed 决定是否要求重新计算过的校验结果。"""
    wanted = {
        str(order_id or "").strip().upper()
        for order_id in (selected_order_ids or set())
        if str(order_id or "").strip()
    }
    failures: list[str] = []
    for order in orders:
        if not isinstance(order, dict):
            continue
        order_id = str(order.get("order_id", "")).strip().upper()
        if not order_id or (wanted and order_id not in wanted):
            continue
        status = str(order.get("validation_status", "")).strip() or "待校验"
        message = str(order.get("validation_message", "")).strip()
        # 旧令牌式分配预览未运行所选订单校验，允许其旧约定中的默认待校验状态；
        # 内存目录预览设置 require_recomputed，必须拒绝未重新计算的结果。
        if not require_recomputed and status == "待同步" and not message:
            continue
        if status == "正常":
            continue
        failures.append(f"{order_id}：{status}" + (f"；{message}" if message else ""))
    return failures


def _require_valid_server_preview_orders(
    orders: Iterable[dict],
    selected_order_ids: set[str] | None = None,
    *,
    require_recomputed: bool = False,
) -> None:
    """检查预览订单并在存在阻断错误时抛出业务异常。

    参数：orders 为预览订单；selected_order_ids 为可选范围；require_recomputed 为重新计算要求。"""
    failures = _server_preview_order_validation_errors(
        orders,
        selected_order_ids,
        require_recomputed=require_recomputed,
    )
    if failures:
        raise RuleError(
            "order_validation",
            "以下订单未通过重新校验，不能确认写入：" + "；".join(failures),
            orders=failures,
        )


def _insert_memory_records(connection: sqlite3.Connection, table: str, rows: list[dict]) -> None:
    """按目标表实际字段插入内存预览记录；connection 为连接，table 为表名，rows 为记录列表。"""
    target_columns = {
        str(row[1]) for row in connection.execute(f"pragma table_info({table})").fetchall()
    }
    for row in rows:
        values = {key: value for key, value in row.items() if key in target_columns}
        if table in {"material_items", "hardware_items", "server_material_allocations", "optimization_artifacts"}:
            values.pop("id", None)
        if not values:
            continue
        columns = list(values)
        placeholders = ",".join("?" for _ in columns)
        connection.execute(
            f"insert or replace into {table}({','.join(columns)}) values({placeholders})",
            tuple(values[column] for column in columns),
        )


def _upsert_memory_optimization_artifacts(
    connection: sqlite3.Connection,
    rows: list[dict],
) -> None:
    """合并选中的优化证据而不替换其历史；connection 为连接，rows 为待合并证据记录。"""
    target_columns = {
        str(row[1])
        for row in connection.execute("pragma table_info(optimization_artifacts)").fetchall()
    }
    columns = [
        "source_path", "order_id", "factory_order", "file_modified_at",
        "file_created_at", "completed_at", "copied_at", "first_seen_at",
        "last_seen_at", "size",
    ]
    columns = [column for column in columns if column in target_columns]
    for row in rows:
        values = {column: row.get(column) for column in columns}
        if not values.get("source_path") or not values.get("factory_order"):
            continue
        placeholders = ",".join("?" for _ in columns)
        connection.execute(
            f"""
            insert into optimization_artifacts({','.join(columns)})
            values({placeholders})
            on conflict(source_path, file_modified_at, size, factory_order)
            do update set
                order_id=excluded.order_id,
                file_created_at=excluded.file_created_at,
                copied_at=excluded.copied_at,
                last_seen_at=case
                    when optimization_artifacts.last_seen_at > excluded.last_seen_at
                    then optimization_artifacts.last_seen_at
                    else excluded.last_seen_at
                end
            """,
            tuple(values[column] for column in columns),
        )


def _materialize_memory_hardware(
    config: Config,
    payload: dict,
    records: dict[str, list[dict]],
    selected_factory_ids: set[str],
    skipped_orders: set[str],
) -> None:
    """用已捕获五金事实匹配当前 SKU，不重开 Server 报表。

    参数：config 为配置；payload 为预览；records 为待写记录；selected_factory_ids 为所选工厂单；skipped_orders 为跳过订单。"""
    from .inventory import TravelerItem, resolve_inventory_items, resolved_product_code

    source_factories = {
        str(group.get("factory_order", "")).strip().upper()
        for group in payload.get("hardware_source_items", [])
        if isinstance(group, dict)
    }
    existing = [
        row for row in records.get("hardware_items", [])
        if (
            str(row.get("factory_order", "")).strip().upper() not in selected_factory_ids
            or str(row.get("factory_order", "")).strip().upper() not in source_factories
        )
    ]
    resolved_rows = list(existing)
    for group in payload.get("hardware_source_items", []):
        if not isinstance(group, dict):
            continue
        factory_order = str(group.get("factory_order", "")).strip().upper()
        order_id = str(group.get("order_id", "")).strip().upper()
        if factory_order not in selected_factory_ids or order_id in skipped_orders:
            continue
        items = group.get("items", [])
        pairs = [
            (
                TravelerItem(
                    row=index,
                    section="五金",
                    name=str(item.get("name", "")),
                    quantity=float(item.get("quantity", 0) or 0),
                    document_remark="",
                ),
                str(item.get("code", "")),
            )
            for index, item in enumerate(items, start=1)
            if isinstance(item, dict)
        ]
        resolution = resolve_inventory_items(config, pairs)
        if resolution.get("missing"):
            names = "、".join(
                str(item.get("name", "") or item.get("source_code", ""))
                for item in resolution["missing"]
            )
            raise RuleError(
                "hardware_mapping_required",
                f"订单 {order_id} 的五金存在未完成商品 SKU 处理：{names}",
                requirements=resolution["missing"],
            )
        ignored = {
            (
                str(item.get("name", "")).strip().casefold(),
                str(item.get("source_code", "")).strip().casefold(),
            )
            for item in resolution.get("ignored", [])
        }
        for index, item in enumerate(items):
            if not isinstance(item, dict):
                continue
            identity = (
                str(item.get("name", "")).strip().casefold(),
                str(item.get("code", "")).strip().casefold(),
            )
            if identity in ignored:
                continue
            product_code = resolved_product_code(resolution, index)
            resolved_rows.append({
                "order_id": order_id,
                "factory_order": factory_order,
                "scope": "factory_order",
                "product_code": product_code,
                "quantity": server_hardware_quantity(
                    product_code, item.get("quantity", 0), str(item.get("unit", "")),
                    factory_order=factory_order, name=str(item.get("name", "")),
                )["quantity"],
                "source_type": "aicnc",
                "source_path": str(group.get("source_path", "")),
                "remarks": "",
                "updated_at": _now(),
            })
    records["hardware_items"] = resolved_rows


def _validated_memory_allocations(payload: dict, records: dict) -> list[dict]:
    """在正式写入前核对所有材料类型的来源与 SKU 数量平衡；payload 为预览，records 为待写记录。"""
    totals: dict[tuple[str, str], float] = defaultdict(float)
    allocations: dict[tuple[str, str, str], float] = defaultdict(float)
    fingerprints = {}
    for row in payload.get('materials', []):
        key = (str(row.get('source_path', '')), str(row.get('product_code', '')).strip().upper())
        quantity = float(row.get('source_quantity', row.get('quantity', 0)) or 0)
        if not key[0] or not key[1] or not math.isfinite(quantity) or quantity < 0:
            raise RuleError('material_allocation', '来源材料身份或数量无效')
        totals[key] += quantity
        fingerprints[key] = str(row.get('source_fingerprint', ''))
    for row in records.get('material_items', []):
        if row.get('source_type') != 'aihouse':
            continue
        path = str(row.get('source_path', ''))
        code = str(row.get('product_code', '')).strip().upper()
        order = str(row.get('order_id', '')).strip().upper()
        quantity = float(row.get('quantity', 0) or 0)
        if not order or not math.isfinite(quantity) or quantity < 0:
            raise RuleError('material_allocation', '材料必须先分配到订单且数量有效')
        if (path, code) not in totals:
            raise RuleError('material_allocation', f'材料 {code} 缺少来源总量')
        allocations[(path, code, order)] += quantity
    for key, total in totals.items():
        assigned = sum(q for (path, code, _), q in allocations.items() if (path, code) == key)
        if abs(assigned - total) > MATERIAL_ALLOCATION_EPSILON:
            raise RuleError('material_allocation',
                f'材料 {key[1]} 分配不平衡：来源总量 {total:g}，已分配 {assigned:g}，差额 {total-assigned:g}')
    return [dict(source_path=path, source_material_key=server_material_identity_key(path, code),
                 product_code=code, source_quantity=totals[(path, code)], order_id=order,
                 allocated_quantity=quantity, source_fingerprint=fingerprints[(path, code)],
                 created_at=_now(), updated_at=_now())
            for (path, code, order), quantity in allocations.items()]


def _confirm_memory_preview(
    config: Config,
    payload: dict,
    *,
    order_id: str = "",
    factory_order: str = "",
    skip_hardware_order_ids: Iterable[str] = (),
    confirm_write: bool = False,
) -> dict:
    """只提交 App 保留的 JSON 预览，校验身份与数量后写入正式库。

    参数：config 为配置；payload 为预览；order_id、factory_order 为可选确认范围；
    skip_hardware_order_ids 为跳过五金的订单；confirm_write 为明确确认标志。
    不接受重新读取 Server 的路径或指纹输入；预览是本次确认依据，本地库为写入目标及写后校验来源。"""
    if not confirm_write:
        raise RuleError("write_confirmation_required", "写入 Server 事实需要用户明确确认")
    timing_started = time.perf_counter()
    records = _memory_preview_records(payload)
    allocations = _validated_memory_allocations(payload, records)
    selected_factories = _memory_factory_selection(payload, order_id, factory_order)
    if factory_order and not selected_factories:
        raise ValueError("所选工厂单不属于当前内存预览")
    if not factory_order:
        selected_factories = _memory_factory_selection(payload)
    selected_factory_ids = {factory for factory, _ in selected_factories}
    selected_order_ids = {
        current_order for _, current_order in selected_factories
    }
    if order_id:
        selected_order_ids.add(str(order_id).strip().upper())
    if not selected_order_ids:
        selected_order_ids = {
            str(item.get("order_id", "")).strip().upper()
            for item in payload.get("orders", [])
            if isinstance(item, dict) and str(item.get("order_id", "")).strip()
        }
    selected_sources = {row['source_path'] for row in allocations if row['order_id'] in selected_order_ids}
    shared_owners = {row['order_id'] for row in allocations if row['source_path'] in selected_sources}
    if not shared_owners.issubset(selected_order_ids):
        raise RuleError('material_allocation', '混单材料必须同时确认全部相关订单的分配，请使用整组确认')
    _require_valid_server_preview_orders(
        payload.get("orders", []),
        selected_order_ids,
        require_recomputed=bool(payload.get("validation_recomputed")),
    )
    skipped_orders = {
        str(value or "").strip().upper()
        for value in skip_hardware_order_ids
        if str(value or "").strip()
    }
    invalid_skips = skipped_orders - selected_order_ids
    if invalid_skips:
        raise RuleError(
            "invalid_hardware_selection",
            f"五金跳过选择包含本次预览之外的订单：{'、'.join(sorted(invalid_skips))}",
        )

    selected_evidence_pairs = {
        (
            str(row.get("factory_order", "")).strip().upper(),
            str(row.get("order_id", "")).strip().upper(),
        )
        for row in records.get("optimization_artifacts", [])
        if str(row.get("factory_order", "")).strip()
        and str(row.get("order_id", "")).strip().upper() in selected_order_ids
        and (not factory_order or str(row.get("factory_order", "")).strip().upper() == str(factory_order).strip().upper())
    }
    optimization_rows = [
        row for row in records.get("optimization_artifacts", [])
        if (
            str(row.get("factory_order", "")).strip().upper(),
            str(row.get("order_id", "")).strip().upper(),
        ) in selected_evidence_pairs
    ]

    validation_finished = time.perf_counter()

    if (
        not _server_preview_has_business_changes(payload)
        and not payload.get("hardware_mapping_requirements")
        and not any(decision_revision(value) != payload.get('hardware_source_decision_bases', {}).get(factory, '')
                    for factory, value in payload.get('hardware_source_decisions', {}).items())
    ):
        baseline_folders = [
            Path(str(folder))
            for folder in payload.get("source_folders", [])
            if str(folder).strip()
        ]
        baseline_entries = records.get("server_scan_xml_state", [])
        production = OrderIndexStore(config.workflow_database)
        try:
            production.connection.execute("begin")
            confirmed_orders = {row[0] for row in production.connection.execute(
                "select distinct order_id from material_items where quantity > 0")}
            optimization_rows = [row for row in optimization_rows if row["order_id"] in confirmed_orders]
            _upsert_memory_optimization_artifacts(production.connection, optimization_rows)
            production.save_server_scan_xml_baseline(
                _confirmed_material_folders(production, baseline_folders),
                baseline_entries,
                observed_at=_now(),
            )
            production.commit()
        except Exception:
            production.connection.rollback()
            raise
        finally:
            production.close()
        finished = time.perf_counter()
        return {
            "server_write_confirmed": True,
            "server_write_skipped": True,
            "server_write_skip_reason": (
                "板材、五金和工厂单信息没有实际变化，仅更新 Server XML 扫描基线"
                + ("并保存优化证据" if optimization_rows else "")
            ),
            "server_material_write_confirmed": False,
            "server_factory_hardware_write_confirmed": False,
            "orders": sorted(selected_order_ids),
            "factory_orders": sorted(selected_factory_ids),
            "optimization_artifact_count": len(optimization_rows),
            "hardware_count": 0,
            "hardware_skipped_orders": sorted(skipped_orders),
            "database": str(config.workflow_database),
            "operation_timing": {
                "total_seconds": round(finished - timing_started, 6),
                "stages": [
                    {
                        "stage": "validate_preview",
                        "label": "校验内存预览与五金映射",
                        "duration_seconds": round(validation_finished - timing_started, 6),
                    },
                    {
                        "stage": "scan_baseline_commit",
                        "label": "更新 Server XML 扫描基线",
                        "duration_seconds": round(finished - validation_finished, 6),
                    },
                ],
            },
        }

    _materialize_memory_hardware(
        config, payload, records, selected_factory_ids, skipped_orders
    )

    order_rows = [
        row for row in records.get("orders", [])
        if str(row.get("order_id", "")).strip().upper() in selected_order_ids
    ]
    material_rows = [
        row for row in records.get("material_items", [])
        if str(row.get("order_id", "")).strip().upper() in selected_order_ids
        and str(row.get("source_type", "")) == "aihouse"
    ]
    factory_rows = [
        row for row in records.get("factory_orders", [])
        if str(row.get("factory_order", "")).strip().upper() in selected_factory_ids
    ]
    hardware_rows = [
        row for row in records.get("hardware_items", [])
        if str(row.get("factory_order", "")).strip().upper() in selected_factory_ids
        and str(row.get("order_id", "")).strip().upper() not in skipped_orders
    ]
    if not order_rows and not factory_rows and not material_rows and not optimization_rows:
        raise ValueError("本次预览没有可写入的订单、材料或工厂单")

    production = OrderIndexStore(config.workflow_database)
    try:
        production.connection.execute("begin")
        commit_source_decisions(production.connection, payload, selected_factory_ids, skipped_orders)
        _insert_memory_records(production.connection, "orders", order_rows)

        material_attributes = {
            (
                str(item.get("source_order_id", "")).strip().upper(),
                str(item.get("source_path", "")),
                str(item.get("product_code", "")).strip().upper(),
            ): item
            for item in payload.get("materials", [])
            if isinstance(item, dict)
        }
        for row in material_rows:
            identity = (
                str(row.get("order_id", "")).strip().upper(),
                str(row.get("source_path", "")),
                str(row.get("product_code", "")).strip().upper(),
            )
            attributes = material_attributes.get(identity)
            if attributes is None:
                raise RuleError(
                    "server_material_identity",
                    f"材料 {identity[2] or '未知 SKU'} 的已验证商品属性缺失，请重新扫描",
                )
            # 删除来源行前先对照仍存在的正式事实校验；历史消耗和分配引用也要求 SKU 的业务属性保持稳定。
            confirm_product_material_attributes(
                production.connection,
                identity[2],
                str(attributes.get("material_type", "")),
                str(attributes.get("color", "")),
                str(attributes.get("thickness", "")),
            )

        material_paths_by_order: dict[str, set[str]] = defaultdict(set)
        for row in material_rows:
            material_paths_by_order[str(row.get("order_id", "")).strip().upper()].add(
                str(row.get("source_path", ""))
            )
        for current_order, paths in material_paths_by_order.items():
            for path in paths:
                production.connection.execute(
                    "delete from material_items where order_id=? and source_type='aihouse' and source_path=?",
                    (current_order, path),
                )
                production.connection.execute(
                    "delete from server_material_allocations where order_id=? and source_path=?",
                    (current_order, path),
                )
        _insert_memory_records(production.connection, "material_items", material_rows)
        selected_allocations = [row for row in allocations if row['order_id'] in selected_order_ids]
        for row in selected_allocations:
            production.connection.execute("""insert into server_material_allocations(
                source_path,source_material_key,product_code,source_quantity,order_id,
                allocated_quantity,source_fingerprint,created_at,updated_at)
                values(:source_path,:source_material_key,:product_code,:source_quantity,:order_id,
                :allocated_quantity,:source_fingerprint,:created_at,:updated_at)
                on conflict(source_path,source_material_key,order_id) do update set
                product_code=excluded.product_code,source_quantity=excluded.source_quantity,
                allocated_quantity=excluded.allocated_quantity,source_fingerprint=excluded.source_fingerprint,
                updated_at=excluded.updated_at""", row)


        for row in factory_rows:
            current_factory = str(row.get("factory_order", "")).strip().upper()
            current_order = str(row.get("order_id", "")).strip().upper()
            has_materials = production.connection.execute(
                "select 1 from material_items where order_id=? and quantity > 0 limit 1",
                (current_order,),
            ).fetchone() is not None
            if row.get("stage") == "已优化" and not has_materials:
                raise RuleError("missing_confirmed_material", "工厂单完成优化前必须先写入有效材料明细")
            _insert_memory_records(production.connection, "factory_orders", [row])
            preserve_confirmed_shipment(production.connection, current_factory)
            existing_automatic_hardware = production.connection.execute(
                "select 1 from hardware_items where factory_order=? and source_type='aicnc' limit 1",
                (current_factory,),
            ).fetchone()
            if current_order in skipped_orders or (
                current_factory in payload.get('hardware_keep_factories', [])
                and existing_automatic_hardware
            ):
                continue
            replace_factory_hardware(
                production.connection, current_factory,
                [item for item in hardware_rows
                 if str(item.get("factory_order", "")).strip().upper() == current_factory
                 and item.get("source_type") == "aicnc"],
                reason="确认 Server 五金预览",
                allow_empty=any(str(group.get("factory_order", "")).strip().upper() == current_factory
                    for group in payload.get("hardware_source_items", [])),
            )

        audit_hardware_integrity(production.connection)

        source_paths = {
            str(row.get("source_path", "")) for row in material_rows if row.get("source_path")
        }
        source_rows = []
        for row in records.get("source_files", []):
            path = str(row.get("path", ""))
            factory_tokens = {
                token.strip().upper()
                for token in str(row.get("factory_order", "")).split(",")
                if token.strip()
            }
            row_orders = {
                token.strip().upper()
                for token in str(row.get("order_id", "")).split("、")
                if token.strip()
            }
            if path in source_paths or factory_tokens.intersection(selected_factory_ids) or row_orders.intersection(selected_order_ids):
                source_rows.append(dict(row))
        source_order_index = next(
            (index for index, row in enumerate(
                production.connection.execute("pragma table_info(source_files)").fetchall()
            ) if row[1] == "order_id"),
            None,
        )
        _ = source_order_index
        for row in source_rows:
            path = str(row.get("path", ""))
            existing = production.connection.execute(
                "select order_id from source_files where path=?", (path,)
            ).fetchone()
            existing_orders = {
                token.strip().upper()
                for token in str(existing[0] if existing else "").split("、")
                if token.strip()
            }
            existing_orders.update(
                token.strip().upper()
                for token in str(row.get("order_id", "")).split("、")
                if token.strip()
            )
            row["order_id"] = "、".join(sorted(existing_orders))
            _insert_memory_records(production.connection, "source_files", [row])

        confirmed_orders = {row[0] for row in production.connection.execute(
            "select distinct order_id from material_items where quantity > 0")}
        optimization_rows = [row for row in optimization_rows if row["order_id"] in confirmed_orders]
        _upsert_memory_optimization_artifacts(production.connection, optimization_rows)
        baseline_folders = [
            Path(str(folder))
            for folder in payload.get("source_folders", [])
            if str(folder).strip()
        ]
        production.save_server_scan_xml_baseline(
            _confirmed_material_folders(production, baseline_folders),
            records.get("server_scan_xml_state", []),
            observed_at=_now(),
        )
        for summary in production.summaries(persist=False):
            if summary["order_id"] in selected_order_ids:
                production.connection.execute(
                    "update orders set stage=? where order_id=?",
                    (summary["stage"], summary["order_id"]),
                )
        production.connection.commit()
    except Exception:
        production.connection.rollback()
        raise
    finally:
        production.close()

    write_finished = time.perf_counter()

    return {
        "server_write_confirmed": True,
        "server_material_write_confirmed": bool(material_rows),
        "server_factory_hardware_write_confirmed": bool(factory_rows),
        "orders": sorted(selected_order_ids),
        "factory_orders": sorted(selected_factory_ids),
        "optimization_artifact_count": len(optimization_rows),
        "hardware_count": len(hardware_rows),
        "hardware_skipped_orders": sorted(skipped_orders),
        "database": str(config.workflow_database),
        "operation_timing": {
            "total_seconds": round(write_finished - timing_started, 6),
            "stages": [
                {
                    "stage": "validate_preview",
                    "label": "校验内存预览与五金映射",
                    "duration_seconds": round(validation_finished - timing_started, 6),
                },
                {
                    "stage": "database_commit",
                    "label": "写入本地数据库事务",
                    "duration_seconds": round(write_finished - validation_finished, 6),
                },
            ],
        },
    }


def confirm_server_preview_memory(
    config: Config,
    payload: dict,
    order_id: str,
    factory_order: str,
    *,
    confirm_write: bool = False,
) -> dict:
    """确认内存预览中指定订单和工厂单。

    参数：config 为配置；payload 为预览；order_id 为订单号；factory_order 为工厂单号；confirm_write 为明确确认标志。"""
    return _confirm_memory_preview(
        config,
        payload,
        order_id=order_id,
        factory_order=factory_order,
        confirm_write=confirm_write,
    )


def confirm_server_material_preview_memory(
    config: Config,
    payload: dict,
    *,
    confirm_write: bool = False,
    skip_hardware_order_ids: Iterable[str] = (),
) -> dict:
    """一并确认内存预览中的订单材料及已解析工厂单五金。

    参数：config 为配置；payload 为预览；confirm_write 为明确确认；skip_hardware_order_ids 为跳过五金的订单。"""
    result = _confirm_memory_preview(
        config,
        payload,
        skip_hardware_order_ids=skip_hardware_order_ids,
        confirm_write=confirm_write,
    )
    result["confirmation_mode"] = "order_materials_and_factory_hardware"
    result["factory_order_selection_required"] = False
    return result


def confirm_server_material_allocations(
    config: Config,
    token: str,
    *,
    confirm_write: bool = False,
    skip_hardware_order_ids: Iterable[str] = (),
) -> dict:
    """把已平衡的订单材料分配写入正式库。

    参数：config 为配置；token 为磁盘预览令牌；confirm_write 为明确确认；skip_hardware_order_ids 为跳过五金的订单。"""
    if not confirm_write:
        raise RuleError("write_confirmation_required", "材料分配写入需要用户明确确认")
    preview_path = _server_preview_path(config, token)
    preview = OrderIndexStore(preview_path)
    try:
        skipped_hardware_orders = {
            str(order_id or "").strip().upper()
            for order_id in skip_hardware_order_ids
            if str(order_id or "").strip()
        }
        if skipped_hardware_orders:
            order_types = {
                str(row[0]).strip().upper(): str(row[1] or "")
                for row in preview.connection.execute(
                    "select order_id, order_type from orders where order_id in ({})".format(
                        ",".join("?" for _ in skipped_hardware_orders)
                    ),
                    tuple(sorted(skipped_hardware_orders)),
                ).fetchall()
            }
            unknown_orders = skipped_hardware_orders - set(order_types)
            if unknown_orders:
                raise RuleError(
                    "invalid_hardware_selection",
                    f"五金写入选择包含本次预览之外的订单：{'、'.join(sorted(unknown_orders))}",
                    order_ids=sorted(unknown_orders),
                )
            invalid_orders = sorted(
                order_id for order_id, order_type in order_types.items()
                if order_type != "cutToSize"
            )
            if invalid_orders:
                raise RuleError(
                    "invalid_hardware_selection",
                    f"只有来料加工订单可以选择本次不写入五金：{'、'.join(invalid_orders)}",
                    order_ids=invalid_orders,
                )
        scope_paths = [
            str(row[0])
            for row in preview.connection.execute(
                "select source_folder from server_material_preview_scopes order by source_folder"
            ).fetchall()
        ]
        hardware_requirements = _refresh_server_preview_hardware(
            config,
            preview_path,
            scope_paths,
            skip_hardware_order_ids=skipped_hardware_orders,
        )
        if hardware_requirements:
            names = "、".join(item["name"] for item in hardware_requirements)
            raise RuleError(
                "hardware_mapping_required",
                f"五金存在未完成商品 SKU 处理：{names}；请在本次预览中设置映射或选择忽略后再确认写入",
                requirements=hardware_requirements,
            )
        preview_payload = _server_preview_payload(
            config,
            preview_path,
            token,
            [Path(path) for path in scope_paths],
            include_hardware=True,
        )
        _require_valid_server_preview_orders(
            preview_payload.get("orders", []),
            {
                str(order.get("order_id", "")).strip().upper()
                for order in preview_payload.get("orders", [])
                if isinstance(order, dict) and str(order.get("order_id", "")).strip()
            },
        )
        actionable_factories = [
            (str(factory["factory_order"]).upper(), str(order["order_id"]).upper())
            for order in preview_payload["orders"]
            for factory in order["factories"]
        ]
        material_rows = _server_material_source_rows(preview, scope_paths)
        if not material_rows and not actionable_factories:
            raise ValueError("本次预览没有可写入的板材、封边条或五金")
        allocations_by_material: dict[str, list[dict]] = defaultdict(list)
        for row in preview.connection.execute(
            """
            select id, source_path, source_material_key, product_code,
                   order_id, allocated_quantity
            from server_material_allocations
            order by source_path, order_id, id
            """
        ).fetchall():
            expected_key = server_material_identity_key(row[1], row[3])
            if str(row[2] or "") != expected_key:
                raise ValueError("Server 材料分配身份已过期，请重新扫描并分配")
            allocations_by_material[expected_key].append({
                "id": int(row[0]),
                "order_id": str(row[4]).upper(),
                "quantity": float(row[5] or 0),
                "product_code": str(row[3] or "").strip().upper(),
            })
        # 材料房间归属已由 Server 工作簿明确并在只读预览保存为 source_order_id；
        # 未分配数量默认归入该来源订单，不要求用户为订单级材料选择工厂单，已有人工分配保持原样。
        for row in material_rows:
            source_order_id = str(row["order_id"] or "").strip().upper()
            source_quantity = float(row["quantity"] or 0)
            source_path = str(row["source_path"] or "")
            product_code = str(row["product_code"] or "").strip().upper()
            source_key = server_material_identity_key(source_path, product_code)
            material_allocations = allocations_by_material[source_key]
            allocated_quantity = sum(
                float(item["quantity"] or 0) for item in material_allocations
            )
            remaining = source_quantity - allocated_quantity
            if remaining <= MATERIAL_ALLOCATION_EPSILON:
                continue
            if not source_order_id:
                raise ValueError(
                    f"材料 {row['color'] or row['material_type'] or product_code} 没有明确订单归属，不能自动确认"
                )
            now = _now()
            existing_index = next(
                (
                    index for index, item in enumerate(material_allocations)
                    if item["order_id"] == source_order_id
                ),
                None,
            )
            existing = (
                material_allocations[existing_index]
                if existing_index is not None else None
            )
            if existing is None:
                cursor = preview.connection.execute(
                    """
                    insert into server_material_allocations(
                        source_path, source_material_key, product_code,
                        source_quantity, order_id, allocated_quantity,
                        source_fingerprint, created_at, updated_at
                    ) values(?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        source_path, source_key, product_code, source_quantity,
                        source_order_id, remaining,
                        str(row["source_fingerprint"] or ""), now, now,
                    ),
                )
                material_allocations.append({
                    "id": int(cursor.lastrowid),
                    "order_id": source_order_id,
                    "quantity": remaining,
                    "product_code": product_code,
                })
            else:
                preview.connection.execute(
                    """
                    update server_material_allocations
                    set allocated_quantity = allocated_quantity + ?, updated_at = ?
                    where id = ?
                    """,
                    (remaining, now, int(existing["id"])),
                )
                existing["quantity"] += remaining
        for row in material_rows:
            source_quantity = float(row["quantity"] or 0)
            source_key = server_material_identity_key(
                row["source_path"], row["product_code"]
            )
            allocated_quantity = sum(
                float(item["quantity"] or 0) for item in allocations_by_material[source_key]
            )
            if abs(source_quantity - allocated_quantity) > MATERIAL_ALLOCATION_EPSILON:
                remaining = source_quantity - allocated_quantity
                raise ValueError(
                    f"材料尚未分配完成：{row['color'] or row['material_type'] or row['product_code']}，"
                    f"还差 {remaining:g} {row['unit'] or ''}"
                )
        material_orders = {
            str(item["order_id"]).upper()
            for values in allocations_by_material.values()
            for item in values
        }
        factory_orders = {order_id for _, order_id in actionable_factories}
        affected_orders = sorted(material_orders | factory_orders)
        if material_rows and not material_orders:
            raise ValueError("请先将板材和封边条分配到订单")
        source_paths = sorted({str(row["source_path"] or "") for row in material_rows if row["source_path"]})
        orders_by_source_path: dict[str, set[str]] = defaultdict(set)
        for row in material_rows:
            source_key = server_material_identity_key(
                row["source_path"], row["product_code"]
            )
            for allocation in allocations_by_material[source_key]:
                orders_by_source_path[str(row["source_path"] or "")].add(
                    str(allocation["order_id"]).upper()
                )

        factory_source_paths: set[str] = set()
        if actionable_factories:
            factory_numbers = {factory_order for factory_order, _ in actionable_factories}
            for path, source_folder, source_order, source_factory in preview.connection.execute(
                "select path, source_folder, order_id, factory_order from source_files"
            ).fetchall():
                if not _path_in_folders(str(source_folder or ""), scope_paths):
                    continue
                source_factory_numbers = {
                    value.strip().upper()
                    for value in str(source_factory or "").split(",")
                    if value.strip()
                }
                if factory_numbers.intersection(source_factory_numbers):
                    factory_source_paths.add(str(path))
        all_source_paths = sorted(set(source_paths) | factory_source_paths)
        production = OrderIndexStore(config.workflow_database)
        try:
            production.connection.execute("begin")
            for row in material_rows:
                confirm_product_material_attributes(
                    production.connection,
                    str(row["product_code"] or "").strip().upper(),
                    str(row["material_type"] or ""),
                    str(row["color"] or ""),
                    str(row["thickness"] or ""),
                )
            order_columns = [
                item[1]
                for item in preview.connection.execute("pragma table_info(orders)").fetchall()
            ]
            for order_id in affected_orders:
                order_row = preview.connection.execute(
                    "select * from orders where order_id = ?", (order_id,)
                ).fetchone()
                if order_row is None:
                    raise ValueError(f"目标订单不存在：{order_id}")
                placeholders = ",".join("?" for _ in order_columns)
                production.connection.execute(
                    f"insert or replace into orders({','.join(order_columns)}) values({placeholders})",
                    tuple(order_row),
                )
                for source_path in source_paths:
                    production.connection.execute(
                        """
                        delete from material_items
                        where order_id = ? and source_type = 'aihouse' and source_path = ?
                        """,
                        (order_id, source_path),
                    )

            material_columns = (
                "order_id", "product_code", "quantity", "source_type",
                "source_path", "source_fingerprint", "updated_at",
            )
            material_sql = f"""
                insert into material_items({','.join(material_columns)})
                values({','.join('?' for _ in material_columns)})
                on conflict(order_id, product_code, source_type, source_path)
                do update set
                    quantity = material_items.quantity + excluded.quantity,
                    source_fingerprint = excluded.source_fingerprint,
                    updated_at = excluded.updated_at
            """
            now = _now()
            for row in material_rows:
                source_key = server_material_identity_key(
                    row["source_path"], row["product_code"]
                )
                for allocation in allocations_by_material[source_key]:
                    production.connection.execute(
                        material_sql,
                        (
                            str(allocation["order_id"]).upper(),
                            str(row["product_code"] or "").strip().upper(),
                            float(allocation["quantity"] or 0), "aihouse",
                            str(row["source_path"] or ""),
                            str(row["source_fingerprint"] or ""), now,
                        ),
                    )

            factory_columns = [
                item[1]
                for item in preview.connection.execute(
                    "pragma table_info(factory_orders)"
                ).fetchall()
            ]
            factory_placeholders = ",".join("?" for _ in factory_columns)
            hardware_columns = [
                item[1]
                for item in preview.connection.execute(
                    "pragma table_info(hardware_items)"
                ).fetchall()
            ]
            hardware_placeholders = ",".join("?" for _ in hardware_columns)
            for factory_order, order_id in actionable_factories:
                preview_factory = preview.connection.execute(
                    "select * from factory_orders where factory_order=? and order_id=?",
                    (factory_order, order_id),
                ).fetchone()
                if preview_factory is None:
                    raise ValueError(f"预览中找不到工厂单：{factory_order}")
                production.connection.execute(
                    f"insert or replace into factory_orders({','.join(factory_columns)}) values({factory_placeholders})",
                    tuple(preview_factory),
                )
                preserve_confirmed_shipment(production.connection, factory_order)
                if order_id in skipped_hardware_orders:
                    # 订单级跳过选择意味着本次确认不改该订单任何工厂单的五金事实；身份和材料仍在同一事务提交。
                    continue
                cursor = preview.connection.execute(
                    "select * from hardware_items where factory_order=? and source_type='aicnc' order by id",
                    (factory_order,),
                )
                names = [column[0] for column in cursor.description]
                replace_factory_hardware(
                    production.connection, factory_order,
                    [dict(zip(names, row)) for row in cursor.fetchall()],
                    reason="确认 Server 五金预览",
                    allow_empty=bool(preview.connection.execute(
                        "select 1 from hardware_source_versions where factory_order=? and row_count=0",
                        (factory_order,),
                    ).fetchone()),
                )
            allocation_columns = [
                item[1]
                for item in preview.connection.execute(
                    "pragma table_info(server_material_allocations)"
                ).fetchall()
            ]
            allocation_insert_columns = [
                column for column in allocation_columns if column != "id"
            ]
            for source_path in source_paths:
                production.connection.execute(
                    "delete from server_material_allocations where source_path = ?",
                    (source_path,),
                )
            allocation_placeholders = ",".join("?" for _ in source_paths)
            allocation_rows = (
                preview.connection.execute(
                    f"select * from server_material_allocations where source_path in ({allocation_placeholders})",
                    tuple(source_paths),
                ).fetchall()
                if source_paths
                else []
            )
            if allocation_rows:
                id_index = allocation_columns.index("id")
                placeholders = ",".join("?" for _ in allocation_insert_columns)
                production.connection.executemany(
                    f"insert or replace into server_material_allocations({','.join(allocation_insert_columns)}) values({placeholders})",
                    [tuple(value for index, value in enumerate(row) if index != id_index) for row in allocation_rows],
                )

            source_columns = [
                item[1]
                for item in preview.connection.execute("pragma table_info(source_files)").fetchall()
            ]
            source_order_index = source_columns.index("order_id")
            for source_path in all_source_paths:
                source_row = preview.connection.execute(
                    "select * from source_files where path = ?", (source_path,)
                ).fetchone()
                if source_row is None:
                    continue
                values = list(source_row)
                existing_orders = {
                    value.strip().upper()
                    for value in str(values[source_order_index] or "").split("、")
                    if value.strip()
                }
                existing_orders.update(orders_by_source_path.get(source_path, set()))
                values[source_order_index] = "、".join(sorted(existing_orders))
                placeholders = ",".join("?" for _ in source_columns)
                production.connection.execute(
                    f"insert or replace into source_files({','.join(source_columns)}) values({placeholders})",
                    tuple(values),
                )

            production.connection.commit()
            # 事务成功还不足以让界面宣称完成；提交后须从正式库读回，并精确校验来源路径对应的数量。
            for order_id in affected_orders:
                expected = defaultdict(float)
                for row in material_rows:
                    source_key = server_material_identity_key(
                        row["source_path"], row["product_code"]
                    )
                    for allocation in allocations_by_material[source_key]:
                        if str(allocation["order_id"]).upper() != order_id:
                            continue
                        expected[str(row["product_code"] or "").strip().upper()] += float(
                            allocation["quantity"] or 0
                        )
                actual = {
                    str(row[0] or "").strip().upper(): float(row[1] or 0)
                    for row in production.connection.execute(
                        """
                        select product_code, sum(quantity)
                        from material_items
                        where order_id = ? and source_type = 'aihouse'
                          and source_path in ({})
                        group by product_code
                        """.format(",".join("?" for _ in source_paths)),
                        (order_id, *source_paths),
                    ).fetchall()
                }
                if set(expected) != set(actual) or any(
                    abs(expected[key] - actual.get(key, 0.0)) > MATERIAL_ALLOCATION_EPSILON
                    for key in expected
                ):
                    raise RuleError(
                        "server_material_persistence",
                        f"订单 {order_id} 的材料写入后回读数量不一致，已停止报告成功",
                        order_id=order_id,
                    )
            for factory_order, order_id in actionable_factories:
                if order_id in skipped_hardware_orders:
                    continue
                verified_factory = production.connection.execute(
                    "select order_id from factory_orders where factory_order=?",
                    (factory_order,),
                ).fetchone()
                if verified_factory is None or str(verified_factory[0] or "").upper() != order_id:
                    raise RuleError(
                        "server_factory_persistence",
                        f"工厂单 {factory_order} 写入后回读身份不一致，已停止报告成功",
                        factory_order=factory_order,
                        order_id=order_id,
                    )
        except Exception:
            production.connection.rollback()
            raise
        finally:
            production.close()
        return {
            "server_material_write_confirmed": bool(material_rows),
            "server_factory_hardware_write_confirmed": bool(actionable_factories),
            "orders": affected_orders,
            "material_count": len(material_rows),
            "factory_orders": [factory_order for factory_order, _ in actionable_factories],
            "hardware_count": sum(
                preview.connection.execute(
                    "select count(*) from hardware_items where factory_order=?",
                    (factory_order,),
                ).fetchone()[0]
                for factory_order, order_id in actionable_factories
                if order_id not in skipped_hardware_orders
            ),
            "hardware_skipped_orders": sorted(skipped_hardware_orders),
            "database": str(config.workflow_database),
        }
    finally:
        preview.close()


def confirm_server_material_preview(
    config: Config,
    token: str,
    *,
    confirm_write: bool = False,
    skip_hardware_order_ids: Iterable[str] = (),
) -> dict:
    """同时确认订单材料及已匹配工厂单五金。

    参数：config 为配置；token 为预览令牌；confirm_write 为明确确认；skip_hardware_order_ids 为跳过五金的订单。"""
    result = confirm_server_material_allocations(
        config,
        token,
        confirm_write=confirm_write,
        skip_hardware_order_ids=skip_hardware_order_ids,
    )
    result["confirmation_mode"] = "order_materials_and_factory_hardware"
    result["factory_order_selection_required"] = False
    return result


def confirm_server_preview(
    config: Config,
    token: str,
    order_id: str,
    factory_order: str,
    *,
    confirm_write: bool = False,
) -> dict:
    """仅将所选订单及工厂单证据合并到正式库。

    参数：config 为配置；token 为预览令牌；order_id 为订单号；factory_order 为工厂单号；confirm_write 为明确确认。"""
    if not confirm_write:
        raise RuleError("write_confirmation_required", "写入 Server 订单事实需要用户明确确认")
    preview_path = _server_preview_path(config, token)
    order_id = str(order_id or "").strip().upper()
    factory_order = str(factory_order or "").strip().upper()
    if not order_id or not factory_order:
        raise ValueError("确认写入需要订单号和工厂单号")
    preview = OrderIndexStore(preview_path)
    selected = preview.connection.execute(
        "select * from factory_orders where factory_order = ? and order_id = ?",
        (factory_order, order_id),
    ).fetchone()
    if selected is None:
        preview.close()
        raise ValueError("所选工厂单不属于该订单或已不在预览中，请重新扫描")
    production = OrderIndexStore(config.workflow_database)
    try:
        production.connection.execute("begin")
        order_row = preview.connection.execute("select * from orders where order_id = ?", (order_id,)).fetchone()
        if order_row is not None:
            columns = [row[1] for row in preview.connection.execute("pragma table_info(orders)").fetchall()]
            placeholders = ",".join("?" for _ in columns)
            production.connection.execute(
                f"insert or replace into orders({','.join(columns)}) values({placeholders})",
                tuple(order_row),
            )
        material_columns = [
            row[1] for row in preview.connection.execute("pragma table_info(material_items)").fetchall()
        ]
        material_rows = preview.connection.execute(
            "select * from material_items where order_id = ? and source_type = 'aihouse'",
            (order_id,),
        ).fetchall()
        material_id_index = material_columns.index("id")
        source_path_index = material_columns.index("source_path")
        material_insert_columns = [column for column in material_columns if column != "id"]
        material_source_paths = {
            str(row[source_path_index] or "") for row in material_rows if str(row[source_path_index] or "")
        }
        for source_path in material_source_paths:
            production.connection.execute(
                "delete from material_items where order_id = ? and source_type = 'aihouse' and source_path = ?",
                (order_id, source_path),
            )
        if material_rows:
            material_placeholders = ",".join("?" for _ in material_insert_columns)
            production.connection.executemany(
                f"insert or replace into material_items({','.join(material_insert_columns)}) values({material_placeholders})",
                [
                    tuple(value for index, value in enumerate(row) if index != material_id_index)
                    for row in material_rows
                ],
            )
        factory_columns = [row[1] for row in preview.connection.execute("pragma table_info(factory_orders)").fetchall()]
        production.connection.execute(
            f"insert or replace into factory_orders({','.join(factory_columns)}) values({','.join('?' for _ in factory_columns)})",
            tuple(selected),
        )
        for table, where, args in (
            ("hardware_items", "factory_order = ?", (factory_order,)),
        ):
            columns = [row[1] for row in preview.connection.execute(f"pragma table_info({table})").fetchall()]
            production.connection.execute(f"delete from {table} where {where}", args)
            rows = preview.connection.execute(
                f"select {','.join(columns)} from {table} where {where}", args
            ).fetchall()
            if rows:
                production.connection.executemany(
                    f"insert into {table}({','.join(columns)}) values({','.join('?' for _ in columns)})",
                    rows,
                )
        source_rows = preview.connection.execute(
            """
            select * from source_files
            where source_folder = ? or source_folder like ?
            """,
            (selected[7], str(selected[7]).rstrip("/") + "/%"),
        ).fetchall()
        source_columns = [row[1] for row in preview.connection.execute("pragma table_info(source_files)").fetchall()]
        for row in source_rows:
            values = tuple(row)
            source_order = str(values[source_columns.index("order_id")] or "").upper()
            source_factories = str(values[source_columns.index("factory_order")] or "").upper().split(",")
            if order_id not in source_order.split("、") and factory_order not in source_factories:
                continue
                production.connection.execute(
                    f"insert or replace into source_files({','.join(source_columns)}) values({','.join('?' for _ in source_columns)})",
                    values,
                )
        production.connection.commit()
    except Exception:
        production.connection.rollback()
        raise
    finally:
        preview.close()
        production.close()
    verification = sqlite3.connect(config.workflow_database)
    try:
        verified_order = verification.execute(
            "select 1 from orders where order_id = ?",
            (order_id,),
        ).fetchone()
        verified_factory = verification.execute(
            "select 1 from factory_orders where order_id = ? and factory_order = ?",
            (order_id, factory_order),
        ).fetchone()
    finally:
        verification.close()
    if verified_order is None or verified_factory is None:
        raise RuleError(
            "server_write_persistence",
            f"Server 确认事务已提交，但回读不到订单 {order_id} 或工厂单 {factory_order}",
            order_id=order_id,
            factory_order=factory_order,
        )
    return {
        "server_write_confirmed": True,
        "order_id": order_id,
        "factory_order": factory_order,
        "database": str(config.workflow_database),
    }


@pending_check_session
def process_server_changes(
    config: Config,
    selected_folders: list[Path] | None = None,
    *,
    include_hardware: bool = True,
) -> dict:
    """处理用户在 Server 提示中明确选择的变化。

    参数：config 为配置；selected_folders 为可选目录范围；include_hardware 为是否包含五金。"""
    return sync_order_index(
        config,
        selected_folders=selected_folders,
        process_temporary=True,
        include_hardware=include_hardware,
    )


def _confirm_current_factory_issue(
    store: OrderIndexStore,
    issue: dict,
    order_id: str,
    factory_name: str = "",
) -> None:
    """确认当前工厂单问题的订单归属及名称。

    参数：store 为索引库；issue 为问题记录；order_id 为确认订单号；factory_name 为可选工厂单名称。"""
    order_id = _valid_aimes_order_id(order_id)
    if not order_id:
        raise ValueError("确认归属的订单号必须是有效的 PP 四位数字或 CS 三位数字")
    factory_order = issue["factory_order"]
    existing = store.connection.execute(
        "select factory_name, source_folder from factory_orders where factory_order = ?",
        (factory_order,),
    ).fetchone()
    resolved_name = factory_name.strip() or (existing[0] if existing else "") or "人工确认"
    source_folder = issue["path"] or (existing[1] if existing else "")
    store.upsert_factory(
        factory_order,
        order_id=order_id,
        factory_name=resolved_name,
        sales_order_name=order_id,
        name_source="manual",
        source_folder=source_folder,
        report_state="已发现",
        ownership_status="已确认",
        server_seen=_now(),
    )
    store.upsert_order(order_id, source_folder=source_folder, server_seen=_now())
    store.resolve_active_issue(issue["issue_key"])
    store.add_change(
        severity="info",
        kind="factory_ownership_resolved",
        order_id=order_id,
        factory_order=factory_order,
        path=source_folder,
        message=f"已确认工厂单 {factory_order} 归属订单 {order_id}",
    )


@pending_check_session
def auto_resolve_current_issue(config: Config, issue_key: str) -> dict:
    """尝试自动解析指定待处理问题并更新结果；config 为配置，issue_key 为问题唯一键。"""
    store = OrderIndexStore(config.workflow_database)
    issue = store.current_issue(issue_key)
    if issue is None:
        store.close()
        raise ValueError("当前问题已解决或不存在，请刷新问题列表")
    if issue["kind"] != "factory_ownership":
        store.close()
        return recheck_current_issue(config, issue_key)

    order_id = ""
    factory_name = ""
    source_folder = Path(issue["path"]) if issue["path"] else None
    if source_folder and source_folder.is_dir():
        from .order_workflow import related_order_ids
        related = related_order_ids(source_folder)
        if len(related) == 1:
            order_id = related[0]
    if not order_id:
        from .core import lookup_aimes_names
        try:
            names = lookup_aimes_names(config, [issue["factory_order"]])
            factory_name = names.get(issue["factory_order"], "")
            order_id = _order_id_from_factory_name(factory_name)
        except Exception as exc:
            issue["message"] += f"；自动查询未完成：{exc}"
            store.upsert_active_issue(
                issue_key=issue_key,
                kind=issue["kind"],
                order_id=issue["order_id"],
                factory_order=issue["factory_order"],
                path=issue["path"],
                message=issue["message"],
            )
            store.commit()
            result = list_order_index(config)
            store.close()
            return result
    if not order_id:
        store.close()
        raise ValueError("系统无法从订单文件夹或 AIMES 名称确认归属，请输入订单号人工确认")
    _confirm_current_factory_issue(store, issue, order_id, factory_name)
    store.commit()
    result = list_order_index(config)
    store.close()
    return result


@pending_check_session
def resolve_current_issue(config: Config, issue_key: str, order_id: str = "", factory_name: str = "") -> dict:
    """按人工指定归属处理问题；config 为配置，issue_key 为问题键，order_id 为订单号，factory_name 为名称。"""
    store = OrderIndexStore(config.workflow_database)
    issue = store.current_issue(issue_key)
    if issue is None:
        store.close()
        raise ValueError("当前问题已解决或不存在，请刷新问题列表")
    if issue["kind"] == "factory_ownership":
        _confirm_current_factory_issue(store, issue, order_id, factory_name)
    else:
        store.close()
        return recheck_current_issue(config, issue_key)
    store.commit()
    result = list_order_index(config)
    store.close()
    return result


@pending_check_session
def recheck_current_issue(config: Config, issue_key: str) -> dict:
    """重新核对问题对应资料；校验成功才清除当前会话提示，不提交预览业务事实。"""
    store = OrderIndexStore(config.workflow_database)
    try:
        issue = store.current_issue(issue_key)
        if issue is None:
            raise ValueError("检查结果已过期，请重新扫描或预览")
        if issue["kind"] == "server_missing_report":
            if not issue["path"] or not Path(issue["path"]).is_dir():
                raise ValueError("文件夹无法访问，状态尚未确认，请恢复连接后重新检查")
            if not _report_files(Path(issue["path"])):
                raise ValueError("仍未找到可用报表，请补齐后重新检查")
        elif issue["kind"] in {"hardware_integrity", "outbound_hardware_difference"}:
            from .hardware_facts import hardware_integrity_findings
            if issue["kind"] == "hardware_integrity":
                findings = hardware_integrity_findings(store.connection, factory_orders=[issue["factory_order"]])
                if findings:
                    raise ValueError("；".join(row["message"] for row in findings))
            else:
                audit_factory_hardware(store.connection, issue["factory_order"])
                if store.current_issue(issue_key):
                    raise ValueError("当前五金与历史单据仍不一致，请核对后重新检查")
        elif issue["path"]:
            path = Path(issue["path"])
            folder = path if path.is_dir() else path.parent
            result = preview_server_changes(config, [folder])
            if result.get("hardware_source_selection"):
                raise ValueError("需要选择五金来源，请使用预览入口完成选择后继续检查")
        else:
            raise ValueError("缺少可检查的来源，请重新同步对应订单并核对详情")
        store.resolve_active_issue(issue_key)
        store.commit()
        result = list_order_index(config)
        result["current_issues"] = store.active_issues()
        result["checked_issue_key"] = issue_key
        return result
    finally:
        store.close()


def list_order_index(config: Config) -> dict:
    """读取并整理订单看板摘要及待处理信息；config 为配置，读取过程包含既有投影清理。"""
    store = OrderIndexStore(config.workflow_database)
    _reconcile_temporary_order_projections(store)
    cached_source_rows = load_aimes_order_cache(config)
    aimes_warnings = store.aimes_review_rows()
    result = {
        "orders": store.summaries(),
        "changes": store.latest_changes(),
        "current_issues": store.active_issues(),
        "sync": store.latest_sync(),
        "aimes_issues": [],
        "aimes_warnings": aimes_warnings,
        "ignored_aimes": store.ignored_aimes_factories(),
        "assigned_aimes": store.assigned_aimes_factories(),
        "database": str(store.path),
        "aimes_source_file": str(config.workflow_database),
        "operation_trace": {
            "aimes": _aimes_trace(
                config,
                source="cache",
                rows=cached_source_rows,
                wrote_cache=False,
            ),
        },
    }
    store.close()
    return result


def abort_order(config: Config, order_id: str, *, confirmed: bool = False) -> dict:
    """持久保存订单中止决定，不改工厂单事实；config 为配置，order_id 为订单号，confirmed 为明确确认标志。"""
    if not confirmed:
        raise RuleError("confirmation_required", "中止订单需要再次确认")
    order_id = str(order_id or "").strip().upper()
    store = OrderIndexStore(config.workflow_database)
    try:
        with store.connection:
            row = store.connection.execute(
                "select stage from orders where order_id=?", (order_id,)
            ).fetchone()
            if row is None:
                raise RuleError("order_not_found", "找不到要中止的订单，请刷新后重试")
            if row[0] != "已中止":
                store.connection.execute(
                    "update orders set stage='已中止', updated_at=? where order_id=?",
                    (_now(), order_id),
                )
        return {"order_id": order_id, "stage": "已中止", "orders": store.summaries()}
    finally:
        store.close()


def save_order_annotations(
    config: Config,
    order_id: str,
    *,
    user_note: str,
    planned_days: list[dict[str, str]],
    actual_days: list[dict[str, str]],
) -> dict:
    """保存人工备注和安装开始日期；config 为配置，order_id 为订单号，user_note 为备注，planned_days、actual_days 为日期记录。"""
    store = OrderIndexStore(config.workflow_database)
    try:
        return store.save_order_annotations(
            order_id,
            user_note=user_note,
            planned_days=planned_days,
            actual_days=actual_days,
        )
    finally:
        store.close()


@pending_check_session
def ignore_aimes_factories(config: Config, ignore_keys: list[str]) -> dict:
    """批量忽略 AIMES 待处理身份并提交；config 为配置，ignore_keys 为所选身份键列表。"""
    store = OrderIndexStore(config.workflow_database)
    _, cached_issues = _partition_aimes_rows(
        load_aimes_order_cache(config),
        store.ignored_aimes_keys(),
        store.aimes_assignments(),
    )
    issues_by_key = {issue["ignore_key"]: issue for issue in store.aimes_review_rows()}
    for issue in cached_issues:
        issues_by_key.setdefault(issue["ignore_key"], issue)
    issues = list(issues_by_key.values())
    by_key = {issue["ignore_key"]: issue for issue in issues}
    unknown = [key for key in ignore_keys if key not in by_key]
    if unknown:
        store.close()
        raise ValueError("所选 AIMES 工厂单已不在待确认清单中，请刷新后重试")
    for key in ignore_keys:
        store.ignore_aimes_factory(by_key[key])
    store.commit()
    store.close()
    return list_order_index(config)


def restore_aimes_factories(config: Config, ignore_keys: list[str]) -> dict:
    """批量取消 AIMES 忽略标记并提交；config 为配置，ignore_keys 为身份键列表。"""
    store = OrderIndexStore(config.workflow_database)
    for key in ignore_keys:
        store.restore_aimes_factory(key)
    store.commit()
    store.close()
    return list_order_index(config)


@pending_check_session
def assign_aimes_factory_order(config: Config, ignore_key: str, order_id: str) -> dict:
    """校验并保存 AIMES 工厂单的人工订单归属；config 为配置，ignore_key 为问题身份键，order_id 为目标订单号。"""
    order_id = _valid_aimes_order_id(order_id)
    if not order_id:
        raise ValueError("手工确认的订单号不符合当前订单规则，请使用 PP 加 4 位数字或 CS 加 3 位数字")
    store = OrderIndexStore(config.workflow_database)
    if ignore_key in store.ignored_aimes_keys():
        store.close()
        raise ValueError("该工厂单已经被忽略，请先恢复后再处理")
    issue = store.aimes_review_row(ignore_key)
    if issue is None:
        raw_rows = load_aimes_order_cache(config)
        raw = next((row for row in raw_rows if _aimes_ignore_key(row) == ignore_key), None)
        if raw is None:
            store.close()
            raise ValueError("所选 AIMES 异常记录已不在待处理清单中，请重新获取 AIMES 数据后重试")
        issue = _aimes_row_issue(raw)
    if issue is None:
        store.close()
        raise ValueError("所选 AIMES 工厂单已不需要人工处理，请刷新后重试")
    if not FACTORY_RE.fullmatch(issue["factory_order"]):
        store.close()
        raise ValueError("工厂单号不符合规则，无法自动归属")
    store.assign_aimes_factory(issue, order_id)
    seen_at = _now()
    store.upsert_order(order_id, aimes_seen=seen_at)
    store.upsert_aimes_factory(
        issue["factory_order"],
        order_id=order_id,
        factory_name=issue["factory_name"],
        sales_order_name=order_id,
        split_time=issue["split_time"],
        seen_at=seen_at,
    )
    store.add_change(
        severity="info",
        kind="aimes_order_assignment",
        order_id=order_id,
        factory_order=issue["factory_order"],
        message=f"已按工厂单名称确认归属：{issue['factory_order']} → {order_id}",
    )
    store.commit()
    store.close()
    return list_order_index(config)


def restore_aimes_order_assignment(config: Config, ignore_key: str) -> dict:
    """撤销人工 AIMES 订单归属；config 为配置，ignore_key 为身份键。"""
    store = OrderIndexStore(config.workflow_database)
    if ignore_key not in store.aimes_assignments():
        store.close()
        raise ValueError("该工厂单没有已确认的建议归属")
    store.restore_aimes_assignment(ignore_key)
    store.commit()
    store.close()
    return list_order_index(config)


def add_manual_factory(config: Config, order_id: str, factory_order: str, factory_name: str) -> dict:
    """校验后登记人工工厂单；config 为配置，order_id 为订单号，factory_order 为工厂单号，factory_name 为名称。"""
    order_id = order_id.upper().strip()
    factory_order = factory_order.upper().strip()
    factory_name = factory_name.strip()
    if not ORDER_FOLDER_RE.fullmatch(order_id):
        raise ValueError(f"订单号格式无效：{order_id}")
    if not FACTORY_RE.fullmatch(factory_order):
        raise ValueError(f"工厂单号格式无效：{factory_order}")
    store = OrderIndexStore(config.workflow_database)
    store.upsert_order(order_id, validation_status="正常", stage="已拆单")
    store.upsert_factory(
        factory_order,
        order_id=order_id,
        factory_name=factory_name,
        name_source="manual",
        ownership_status="已确认",
        report_state="手工添加",
    )
    store.add_change(
        severity="info",
        kind="manual_factory",
        order_id=order_id,
        factory_order=factory_order,
        message=f"手工添加工厂单：{factory_order} / {factory_name}",
    )
    store.commit()
    result = list_order_index(config)
    store.close()
    return result
