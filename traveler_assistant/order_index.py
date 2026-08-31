"""Order index, synchronization evidence, and pending-issue state.

This module connects external identity/report observations to the central
SQLite index.  It does not make Server file metadata into production facts:
source paths, fingerprints, AIMES identities, outbound evidence, and user
decisions remain distinguishable records.  The module is large because the
index is also the recovery point for dashboard status and pending work.
"""

from __future__ import annotations

import json
import hashlib
import os
import re
import sqlite3
import shutil
import time
import uuid
import xml.etree.ElementTree as ET
from collections import defaultdict
from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import Iterable

from .core import (
    AIMES_BULK_FETCH_LIMIT,
    Config,
    RuleError,
    factory_name_order_mismatch,
    load_aimes_order_cache,
    load_factory_name_cache,
    save_aimes_order_cache,
    save_factory_name_cache,
)
from .operation_log import log_database_statement
from .fittings import select_latest_fittings
from .database import (
    collapse_actual_installation_days,
    ensure_outbound_document_factory_links,
    ensure_schema,
)
from .inventory import InventoryMappings


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

# The resident order service installs one serialized SQLite connection for the
# central workflow database.  One-shot CLI/tests do not install it and keep
# the previous connection ownership behavior.
_SHARED_WORKFLOW_PATH: Path | None = None
_SHARED_WORKFLOW_CONNECTION: sqlite3.Connection | None = None


def install_shared_workflow_connection(path: Path, connection: sqlite3.Connection) -> None:
    global _SHARED_WORKFLOW_PATH, _SHARED_WORKFLOW_CONNECTION
    _SHARED_WORKFLOW_PATH = path.resolve()
    _SHARED_WORKFLOW_CONNECTION = connection


def clear_shared_workflow_connection() -> None:
    global _SHARED_WORKFLOW_PATH, _SHARED_WORKFLOW_CONNECTION
    _SHARED_WORKFLOW_PATH = None
    _SHARED_WORKFLOW_CONNECTION = None


def _shared_workflow_connection(path: Path) -> sqlite3.Connection | None:
    if _SHARED_WORKFLOW_PATH == path.resolve():
        return _SHARED_WORKFLOW_CONNECTION
    return None
SERVER_SHIPPED_WATCH_DAYS = 7
TEMPORARY_SHIPPED_WATCH_DAYS = 3
SERVER_SNAPSHOT_MAX_WORKERS = 4
SERVER_SCAN_SNAPSHOT_FILENAME = "server-scan-snapshot.json"
SERVER_SCAN_XML_KINDS = {"optimization_input", "optimization_result"}
BATCH_NUMBER_RE = re.compile(r"(PC\d{12,})", re.IGNORECASE)
MATERIAL_ALLOCATION_EPSILON = 0.01
TRAVELER_FILENAME_RE = re.compile(r"^Work Order Traveler\(.+\)\.xlsx$", re.IGNORECASE)


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def _order_id_from_factory_name(name: str) -> str:
    match = ORDER_ID_FROM_FACTORY_RE.match(str(name or "").strip())
    return match.group(1).upper() if match else ""


def _order_type(order_id: str) -> str:
    return "cutToSize" if order_id.upper().startswith("CS") else "owned"


def _batch_number_from_path(path: Path) -> str:
    """Extract a PC batch identifier from a report path as evidence only."""
    for part in reversed(path.parts):
        match = BATCH_NUMBER_RE.search(part)
        if match:
            return match.group(1).upper()
    return ""


def _server_root_candidates(config: Config) -> list[Path]:
    """Return both production Server roots in stable order.

    ``source_root`` remains the configured owned-order root for compatibility
    with existing settings.  The sibling root is always derived from it so
    dashboard refreshes and explicit Server processing share the same routing
    rule as the production-files page.
    """
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
    return [root for root in _server_root_candidates(config) if root.is_dir()]


def _server_root_order_type(root: Path) -> str:
    return "cutToSize" if root.name.casefold() == "cut to size" else "owned"


def _server_folder_matches_root(folder: Path, root: Path, order_ids: set[str]) -> bool:
    if not _is_standard_order_folder(folder.name):
        return True
    return (
        folder.name.upper() in order_ids
        and _order_type(folder.name) == _server_root_order_type(root)
    )


def _is_standard_order_folder(name: str) -> bool:
    """Recognize the two supported standard Server folder-name formats."""
    return bool(ORDER_FOLDER_RE.fullmatch(str(name or "")))


def _is_traveler_file(path: Path) -> bool:
    """Return whether a path has the production Work Order Traveler filename."""
    return bool(TRAVELER_FILENAME_RE.fullmatch(path.name))


def _folder_created_at(folder: Path) -> float:
    """Return creation time where the filesystem exposes it, with a safe fallback."""
    stat = folder.stat()
    return float(getattr(stat, "st_birthtime", stat.st_ctime))


def _path_created_at(path: Path, stat=None) -> float:
    """Return filesystem creation time with a portable ctime fallback."""
    stat = stat or path.stat()
    return float(getattr(stat, "st_birthtime", stat.st_ctime))


def _display_timestamp(value: float) -> str:
    return datetime.fromtimestamp(value).isoformat(timespec="seconds")


def _mtime_marker(stat) -> int:
    """Return a SQLite-safe millisecond modification-time marker.

    Storing nanoseconds in SQLite's REAL-affinity column loses the lowest bits
    when converted to IEEE-754 float. That made an unchanged file look
    modified on the next sync. Millisecond precision still compares mtime and
    size, while remaining exactly representable at current dates.
    """
    return int(stat.st_mtime_ns // 1_000_000)


def _file_content_fingerprint(path: Path) -> str:
    """Return a stable SHA-256 fingerprint for a readable Server report."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _material_source_fingerprint(store: "OrderIndexStore", path: Path) -> str:
    """Return the current material workbook identity for audit and dedupe."""
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


def _replace_server_material_facts(
    store: "OrderIndexStore",
    order_id: str,
    path: Path,
    parsed_materials: list,
    parsed_edges: dict[str, float],
    mappings: InventoryMappings,
    observed_at: str,
) -> None:
    """Replace one order's Server material facts as a single source set."""
    normalized_order_id = order_id.upper()
    # A base material workbook is a complete replacement for the base set,
    # but nested ``*-recut`` board reports are additive sources.  Deleting all
    # rows here used to erase a recut's newly inserted 18mm plywood whenever
    # the root workbook happened to be visited later in the same scan.
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
    """Insert one source-scoped Server material fact set."""
    from .order_workflow import _material_inventory_name

    normalized_order_id = order_id.upper()
    source_fingerprint = _material_source_fingerprint(store, path)
    for item in parsed_materials:
        if mappings.ignored_reason(_material_inventory_name(item.kind, item.thickness, item.color)) is not None:
            continue
        store.connection.execute(
            """insert or replace into material_items(
                order_id,material_type,color,thickness,quantity,unit,edge,
                source_type,source_path,source_fingerprint,updated_at
            ) values(?,?,?,?,?,?,?,?,?,?,?)""",
            (normalized_order_id, item.kind, item.color, str(item.thickness),
             float(item.quantity), "pcs", "", "aihouse", str(path),
             source_fingerprint, observed_at),
        )
    for color, quantity in parsed_edges.items():
        if mappings.ignored_reason(f"Edge banding--{color}") is not None:
            continue
        store.connection.execute(
            """insert or replace into material_items(
                order_id,material_type,color,thickness,quantity,unit,edge,
                source_type,source_path,source_fingerprint,updated_at
            ) values(?,?,?,?,?,?,?,?,?,?,?)""",
            (normalized_order_id, "edge", color, "", float(quantity), "m", color,
             "aihouse", str(path), source_fingerprint, observed_at),
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
    """Replace one incremental Server report without replacing the base order set."""
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
    try:
        return datetime.fromisoformat(config.server_scan_baseline_at).timestamp()
    except ValueError:
        return 0.0


def _valid_aimes_order_id(value: str) -> str:
    order_id = str(value or "").upper().strip()
    if not AIMES_ORDER_RE.fullmatch(order_id):
        return ""
    return order_id


def _normalize_split_time(value: str) -> str:
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
    """Extract the YYMMDD date embedded in a dated AIMES factory number."""
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
    """Return whether a factory order predates the configured first scan date.

    Dated factory numbers are the authoritative source for the historical rows
    in question.  For other factory-number formats, use split_time when it is
    available; malformed or missing dates are kept for normal review.
    """
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
    """Return a stable fingerprint of one order's persisted AIMES identity.

    The fingerprint deliberately excludes the local source label.  A
    Server-derived factory row becoming AIMES-confirmed is not an AIMES
    business change when the factory identity itself is unchanged.
    """
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
    """Use factory-order dates first and folder creation as the fallback."""
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
    """Use the latest known shipment time, falling back to policy creation."""
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
    """Parse naive or timezone-aware ISO text into one comparable instant."""
    return datetime.fromisoformat(str(value or "").strip()).timestamp()


def _visible_aimes_row(row: dict) -> dict | None:
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
) -> list[dict]:
    """Combine the recent page with exact rows found outside that page.

    AIMES returns recent-page rows and exact-verification rows separately.  A
    verified row is still authoritative identity data and must be persisted;
    it is not only evidence that the factory order was not deleted.
    """
    merged: dict[str, dict] = {}
    for row in recent_rows:
        factory_order = str(row.get("factory_order", "")).upper().strip()
        if factory_order:
            merged[factory_order] = row
    for row in (verification_result or {}).get("rows", []):
        if not isinstance(row, dict):
            continue
        factory_order = str(row.get("factory_order", "")).upper().strip()
        if factory_order and factory_order not in merged:
            merged[factory_order] = row
    return list(merged.values())


def _business_validation_message(exc: Exception) -> str:
    """Convert parser/runtime failures into an actionable order explanation."""
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
    message = str(exc).strip().casefold()
    if any(word in message for word in ("password", "credential", "账号", "密码", "登录")):
        return "AIMES 登录未成功。请在设置中确认用户名和密码后重新获取。"
    if any(word in message for word in ("timeout", "timed out", "network", "connection", "网络")):
        return "AIMES 暂时没有响应。请确认网络连接正常，稍后重新获取。"
    return "AIMES 数据获取未完成。请确认网络、账号密码和 AIMES 可用状态后重新获取。"


def _business_server_message(exc: Exception) -> str:
    message = str(exc).strip().casefold()
    if "所选文件夹" in message or "订单文件夹" in message:
        return str(exc).strip()
    if any(word in message for word in ("permission", "not permitted", "权限")):
        return "App 没有访问 Server 订单目录的权限。请确认 Server 已挂载并允许 App 访问后重新扫描。"
    return "Server 订单目录当前无法访问。请确认已连接公司网络并挂载 Server，然后重新扫描。"


def _business_report_message(kind: str, path: Path) -> str:
    report_name = "板材清单" if kind == "board" else "Fittingslist"
    return f"{report_name} {path.name} 无法读取。请确认文件完整、未被占用且格式正确，修正后重新扫描 Server。"


def _source_path_in_dashboard_scope(root: Path, value: str) -> bool:
    """Return whether an indexed server path belongs to a dashboard folder we scan."""
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


class OrderIndexStore:
    """Persistent order/factory/source index used by the order dashboard."""

    def __init__(self, path: Path, *, connection: sqlite3.Connection | None = None):
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
            self.connection = sqlite3.connect(path)
        else:
            self.connection = connection
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
                validation_status text not null default '待同步',
                validation_message text not null default '',
                stage text not null default '已设计',
                material_status text not null default '待校验',
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
                production_batch_id integer,
                factory_name text not null default '',
                sales_order_name text not null default '',
                split_time text not null default '',
                name_source text not null default '',
                source_folder text not null default '',
                report_state text not null default '未发现',
                ownership_status text not null default '待确认',
                has_hardware integer not null default 0,
                optimized integer not null default 0,
                outbound_status text not null default '未查询',
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
                batch_number text not null default '',
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
                source_material_id integer not null,
                source_path text not null default '',
                source_material_key text not null default '',
                material_type text not null default '',
                color text not null default '',
                thickness text not null default '',
                unit text not null default '',
                edge text not null default '',
                source_quantity real not null default 0,
                order_id text not null,
                allocated_quantity real not null default 0,
                source_fingerprint text not null default '',
                created_at text not null,
                updated_at text not null,
                unique(source_path, source_material_key, order_id)
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
            create table if not exists batch_evidence(
                id integer primary key,
                factory_order text not null,
                batch_number text not null,
                source_path text not null,
                order_id text not null default '',
                first_seen text not null,
                last_seen text not null,
                status text not null default 'observed',
                unique(factory_order, batch_number, source_path)
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
            create index if not exists idx_batch_evidence_factory on batch_evidence(factory_order, status);
            create index if not exists idx_factory_order_id on factory_orders(order_id);
            create index if not exists idx_sync_changes_observed on sync_changes(observed_at desc);
            create index if not exists idx_active_issues_status on active_issues(status, last_seen desc);
            """
        )
        # The old one-month folder-ignore feature was removed. Drop its
        # obsolete table from databases created by earlier App versions.
        self.connection.execute("drop table if exists ignored_server_folders")
        collapse_actual_installation_days(self.connection)
        # Versions before the incremental index stored nanoseconds in the
        # REAL-affinity column. Normalize those old values once so installing
        # the optimization does not force every existing report through a
        # needless full reparse on the first refresh.
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
        if "validation_message" not in order_columns:
            self.connection.execute(
                "alter table orders add column validation_message text not null default ''"
            )
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
        if "batch_number" not in source_columns:
            self.connection.execute(
                "alter table source_files add column batch_number text not null default ''"
            )
        if "production_batch_id" not in factory_columns:
            self.connection.execute(
                "alter table factory_orders add column production_batch_id integer"
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
            # Existing outbound rows already carry the inventory-system issue
            # time. Backfill once so the dashboard's monthly completion count
            # is based on the last factory shipment, not a later index refresh.
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
                where outbound_status = '已出库'
                  and outbound_completed_at = ''
                """
            )
        self.connection.execute("update orders set stage = '已设计' where stage = '待拆单'")
        # Current issues are created by the config-aware sync path below.  Do
        # not reconstruct them from every unresolved factory row while merely
        # opening the database: that would revive historical rows which are
        # outside the user's configured initial scan date.
        if version < 7:
            # Repair the historical false warning created before the server
            # report parser passed the unique order-folder hint into fittings
            # candidates.  A real PP/CS folder is an unambiguous owner, so it
            # is safe to confirm it without waiting for another full scan.
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
        if self._owns_connection:
            self.connection.close()

    def temporary_order(self, source_folder: str) -> dict | None:
        row = self.connection.execute(
            """
            select temporary_id, folder_name, source_folder, folder_created_at,
                   content_fingerprint, traveler_path, traveler_fingerprint,
                   traveler_include_hardware, traveler_status, traveler_generated_at,
                   processing_status,
                   outbound_status, outbound_document, processed_at,
                   outbound_at, last_error, server_scan_policy,
                   server_scan_watch_until, server_scan_policy_updated_at, updated_at
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
        )
        return dict(zip(keys, row))

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
    ) -> None:
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
                server_scan_policy_updated_at, updated_at
            ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
            on conflict(source_folder) do update set
                temporary_id=excluded.temporary_id,
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
            ),
        )

    def ignored_aimes_keys(self) -> set[str]:
        return {
            row[0]
            for row in self.connection.execute(
                "select ignore_key from ignored_aimes_factory_orders"
            ).fetchall()
        }

    def ignored_aimes_factories(self) -> list[dict]:
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
        return {
            row[0]: row[1]
            for row in self.connection.execute(
                "select ignore_key, assigned_order_id from aimes_order_assignments"
            ).fetchall()
        }

    def assigned_aimes_factories(self) -> list[dict]:
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
        """Persist the current non-standard AIMES rows for temporary matching."""
        self.connection.execute("delete from aimes_review_rows")
        self.connection.executemany(
            """
            insert into aimes_review_rows(
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

    def assign_aimes_factory(self, issue: dict, order_id: str) -> None:
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

    def restore_aimes_assignment(self, ignore_key: str) -> None:
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

    def restore_aimes_factory(self, ignore_key: str) -> None:
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
        material_status: str | None = None,
        server_seen: str = "",
        aimes_seen: str = "",
        ) -> None:
        order_id = order_id.upper()
        current = self.connection.execute(
            "select validation_status, stage, material_status, order_type from orders where order_id = ?",
            (order_id,),
        ).fetchone()
        values = (
            validation_status or (current[0] if current else "待同步"),
            stage or (current[1] if current else "已设计"),
            material_status or (current[2] if current else "待校验"),
        )
        resolved_order_type = order_type or (current[3] if current else _order_type(order_id))
        self.connection.execute(
            """
            insert into orders(
                order_id, order_type, source_folder, source_folder_mtime,
                validation_status, stage, material_status,
                last_server_seen, last_aimes_seen, updated_at
            ) values(?,?,?,?,?,?,?,?,?,?)
            on conflict(order_id) do update set
                order_type=excluded.order_type,
                source_folder=case when excluded.source_folder <> '' then excluded.source_folder else orders.source_folder end,
                source_folder_mtime=coalesce(excluded.source_folder_mtime, orders.source_folder_mtime),
                validation_status=excluded.validation_status,
                stage=excluded.stage,
                material_status=excluded.material_status,
                last_server_seen=case when excluded.last_server_seen <> '' then excluded.last_server_seen else orders.last_server_seen end,
                last_aimes_seen=case when excluded.last_aimes_seen <> '' then excluded.last_aimes_seen else orders.last_aimes_seen end,
                updated_at=excluded.updated_at
            """,
            (
                order_id,
                resolved_order_type,
                source_folder,
                source_folder_mtime,
                values[0],
                values[1],
                values[2],
                server_seen,
                aimes_seen,
                _now(),
            ),
        )

    def server_scan_policy(self, order_id: str) -> dict | None:
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
        """Save user-maintained order note and single-day installation facts.

        Server/AIMES upserts never touch these fields.  Both planned and actual
        installation are represented by at most one start-date row.
        """
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
        # The SwiftUI dashboard applies this response to its full in-memory
        # order snapshot.  Return the complete summaries so saving an
        # order-level annotation cannot be mistaken for a partial dashboard
        # response and clear every other row.
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
        factory_order = factory_order.upper()
        current = self.connection.execute(
            """
            select report_state, ownership_status, has_hardware, optimized,
                   outbound_status, outbound_document, outbound_mode, outbound_fingerprint
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
                report_state, ownership_status, has_hardware, optimized,
                outbound_status, outbound_document, outbound_mode, outbound_fingerprint, last_server_seen,
                last_aimes_seen, updated_at
            ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
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
                optimized=excluded.optimized,
                outbound_status=excluded.outbound_status,
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
                int(resolved_optimized),
                resolved_outbound_status,
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
        """Update AIMES-owned identity fields without erasing Server-derived state."""
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
                split_time=excluded.split_time,
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
        """Retain a deleted AIMES identity for audit, while making it inactive."""
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
            update active_issues
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
        if metadata is None:
            stat = path.stat()
            modified_at = float(_mtime_marker(stat))
            size = stat.st_size
        else:
            modified_at = float(metadata["modified_at"])
            size = int(metadata["size"])
        batch_number = _batch_number_from_path(path)
        previous = self.connection.execute(
            """
            select modified_at, size, source_folder, kind, order_id, factory_order,
                   content_fingerprint, batch_number
            from source_files where path = ?
            """,
            (str(path),),
        ).fetchone()
        # A directory mtime is filesystem bookkeeping, not a source-data
        # change.  Keep the folder row for discovery, grouping, and deletion
        # detection, but do not advance its business baseline on mtime-only
        # changes.  Recognized workbooks retain the normal mtime/size check.
        metadata_changed = (
            previous is None
            if kind == "folder"
            else previous is None or previous[:2] != (modified_at, size)
        )
        content_fingerprint = str(previous[6] if previous is not None else "")
        if not batch_number and previous is not None:
            batch_number = str(previous[7] or "")
        if kind != "folder" and metadata_changed:
            try:
                current_fingerprint = _file_content_fingerprint(path)
            except OSError:
                # A report which cannot be read must remain a change so the
                # normal parser/error path can ask the user to repair it.
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
            # ``last_seen`` is diagnostic-only. Avoid a network-triggered
            # SQLite upsert for an unchanged source entry; the scan result
            # itself now reports the current scope and counts.
            return ""
        change_type = "added" if previous is None else ("modified" if changed else "")
        self.connection.execute(
            """
            insert into source_files(
                path, source_folder, kind, order_id, factory_order, batch_number, modified_at, size,
                content_fingerprint, last_seen
            ) values(?,?,?,?,?,?,?,?,?,?)
            on conflict(path) do update set
                source_folder=excluded.source_folder,
                kind=excluded.kind,
                order_id=case when excluded.order_id <> '' then excluded.order_id else source_files.order_id end,
                factory_order=case when excluded.factory_order <> '' then excluded.factory_order else source_files.factory_order end,
                batch_number=case when excluded.batch_number <> '' then excluded.batch_number else source_files.batch_number end,
                modified_at=excluded.modified_at,
                size=excluded.size,
                content_fingerprint=excluded.content_fingerprint,
                last_seen=excluded.last_seen
            """,
            (
                str(path), str(source_folder), kind, order_id.upper(), factory_order.upper(), batch_number,
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
        seen_at = seen_at or _now()
        self.connection.execute(
            """
            insert into active_issues(
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
        rows = self.connection.execute(
            """
            select issue_key, kind, order_id, factory_order, path, message,
                   status, first_seen, last_seen, resolved_at
            from active_issues
            where status = 'open'
            order by last_seen desc, issue_key
            """
        ).fetchall()
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
        ]

    def delete_stale_factory_ownership_issues(self, initial_date: str) -> int:
        """Delete open ownership issues for factory orders before initial_date."""
        rows = self.connection.execute(
            """
            select active_issues.issue_key, active_issues.factory_order,
                   coalesce(factory_orders.split_time, '')
            from active_issues
            left join factory_orders
              on factory_orders.factory_order = active_issues.factory_order
            where active_issues.kind = 'factory_ownership'
              and active_issues.status = 'open'
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
            f"delete from active_issues where issue_key in ({placeholders})",
            stale_keys,
        )
        return len(stale_keys)

    def resolve_active_issue(self, issue_key: str, *, resolved_at: str | None = None) -> None:
        self.connection.execute(
            "update active_issues set status = 'resolved', resolved_at = ? where issue_key = ?",
            (resolved_at or _now(), issue_key),
        )

    def resolve_active_issues_not_in(
        self,
        issue_keys: set[str],
        *,
        scoped_folders: set[str] | None = None,
    ) -> None:
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
            sql = f"update active_issues set status = 'resolved', resolved_at = ? where status = 'open' and issue_key not in ({placeholders}){scope_sql}"
            self.connection.execute(sql, (_now(), *sorted(issue_keys), *scope_args))
        else:
            sql = f"update active_issues set status = 'resolved', resolved_at = ? where status = 'open'{scope_sql}"
            self.connection.execute(sql, (_now(), *scope_args))

    def clear_server_folder_pending_records(self, folders: set[str]) -> None:
        """Remove stale lightweight baselines and close issues for excluded folders."""
        for folder in sorted(path.rstrip("/") for path in folders if path):
            prefix = folder + "/%"
            self.connection.execute(
                "delete from source_files where source_folder = ? or source_folder like ?",
                (folder, prefix),
            )
            self.connection.execute(
                """
                update active_issues
                set status = 'resolved', resolved_at = ?
                where status = 'open' and (path = ? or path like ?)
                """,
                (_now(), folder, prefix),
            )

    def current_issue(self, issue_key: str) -> dict | None:
        return next((issue for issue in self.active_issues() if issue["issue_key"] == issue_key), None)

    def update_source_file_identity(
        self,
        path: Path,
        *,
        order_id: str = "",
        factory_order: str = "",
    ) -> None:
        self.connection.execute(
            "update source_files set order_id = ?, factory_order = ?, batch_number = case when batch_number <> '' then batch_number else ? end where path = ?",
            (order_id.upper(), factory_order.upper(), _batch_number_from_path(path), str(path)),
        )
        batch_number = _batch_number_from_path(path)
        for factory in [item.strip().upper() for item in factory_order.split(",") if item.strip()]:
            if batch_number:
                self.record_batch_evidence(factory, batch_number, path, order_id)

    def record_batch_evidence(
        self, factory_order: str, batch_number: str, source_path: Path, order_id: str = ""
    ) -> None:
        """Record evidence and enforce one effective batch per factory order."""
        factory_order = factory_order.upper().strip()
        batch_number = batch_number.upper().strip()
        if not factory_order or not batch_number:
            return
        observed = _now()
        self.connection.execute(
            """
            insert into production_batches(batch_number, source, first_seen, last_seen, created_at, updated_at)
            values(?, 'server-report', ?, ?, ?, ?)
            on conflict(batch_number) do update set last_seen=excluded.last_seen, updated_at=excluded.updated_at
            """,
            (batch_number, observed, observed, observed, observed),
        )
        self.connection.execute(
            """
            insert into batch_evidence(factory_order,batch_number,source_path,order_id,first_seen,last_seen,status)
            values(?,?,?,?,?,?, 'observed')
            on conflict(factory_order,batch_number,source_path) do update set last_seen=excluded.last_seen
            """,
            (factory_order, batch_number, str(source_path), order_id.upper(), observed, observed),
        )
        self.connection.execute(
            "insert or ignore into factory_orders(factory_order, order_id, updated_at) values(?,?,?)",
            (factory_order, order_id.upper(), observed),
        )
        rows = self.connection.execute(
            "select distinct batch_number from batch_evidence where factory_order=? and status='observed'",
            (factory_order,),
        ).fetchall()
        if len(rows) == 1:
            self.connection.execute(
                "update factory_orders set production_batch_id=(select batch_id from production_batches where batch_number=?), updated_at=? where factory_order=?",
                (batch_number, observed, factory_order),
            )
        else:
            self.connection.execute(
                "update factory_orders set production_batch_id=null, updated_at=? where factory_order=?",
                (observed, factory_order),
            )
            self.upsert_active_issue(
                issue_key=f"batch_conflict:{factory_order}",
                kind="batch_conflict",
                order_id=order_id,
                factory_order=factory_order,
                path=str(source_path),
                message=f"工厂单 {factory_order} 发现多个批次证据：{', '.join(sorted(row[0] for row in rows))}。请手工确认唯一有效批次。",
                seen_at=observed,
            )

    def record_run(self, started: str, finished: str, *, aimes_attempted: bool, aimes_succeeded: bool,
                   aimes_count: int, server_folder_count: int, error: str = "") -> None:
        self.connection.execute(
            """
            insert into sync_runs(started_at, finished_at, aimes_attempted, aimes_succeeded, aimes_count, server_folder_count, error)
            values(?,?,?,?,?,?,?)
            """,
            (started, finished, int(aimes_attempted), int(aimes_succeeded), aimes_count, server_folder_count, error),
        )

    def commit(self) -> None:
        self.connection.commit()

    def latest_sync(self) -> dict:
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
        row = self.connection.execute(
            "select 1 from sync_runs where aimes_succeeded = 1 and finished_at like ? limit 1",
            (f"{day}%",),
        ).fetchone()
        return row is not None

    def latest_change_id(self) -> int:
        return int(self.connection.execute("select coalesce(max(id), 0) from sync_changes").fetchone()[0])

    def server_scan_xml_state(self) -> list[dict[str, object]]:
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
        """Replace XML scan baselines for explicitly completed folders only."""
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

    def summaries(self) -> list[dict]:
        orders = self.connection.execute(
            "select order_id, order_type, source_folder, source_folder_mtime, validation_status, stage, material_status, last_server_seen, last_aimes_seen, updated_at, validation_message, user_note from orders order by order_id"
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
                      ownership_status, has_hardware, optimized, outbound_status,
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
               from manual_production_batch_factories f
               join manual_production_batches b on b.batch_id=f.batch_id
               where b.status='completed'
               group by f.order_id, f.factory_order"""
        ).fetchall() if self.connection.execute(
            "select 1 from sqlite_master where type='table' and name='manual_production_batches'"
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
            if not children and not is_temporary:
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
            if is_temporary:
                if row[4] == "数据异常":
                    stage = "数据异常"
                elif expected and shipped == expected:
                    # A temporary folder can still represent a completed
                    # order after manual processing.  Outbound facts are the
                    # terminal business state; do not keep such an order in
                    # the default unfinished list merely because its source
                    # folder was non-standard.
                    stage = "已出货"
                else:
                    stage = "待人工处理"
            elif row[4] == "数据异常" or unresolved:
                stage = "数据异常" if row[4] == "数据异常" else "待确认"
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
            # Keep the separately persisted validation failure stage intact;
            # the dashboard still presents ``数据异常`` from validation_status.
            # For normal rows, persist the derived business stage so restart
            # and direct SQLite reads agree with the factory-order evidence.
            if row[4] != "数据异常" and row[5] != stage:
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
    result = []
    for path in folder.rglob("*.xlsx"):
        if path.name.startswith("~$"):
            continue
        lowered = path.name.lower()
        if lowered.startswith("fittingslist"):
            result.append((path, "fittings"))
        elif "板材清单" in path.name:
            result.append((path, "board"))
        elif "material" in lowered and not lowered.startswith("panelmaterial"):
            result.append((path, "material"))
    return result


def _is_recut_material_source(path: Path) -> bool:
    """Return whether a material source path is inside a recut scope."""
    return any(
        part.casefold() == "recut" or part.casefold().endswith("-recut")
        for part in path.expanduser().resolve().parts[:-1]
    )


def _is_recut_server_report(path: Path, source_folder: Path) -> bool:
    """Return whether a recognized report belongs to a nested recut scope."""
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


def _delete_server_material_source_facts(
    store: "OrderIndexStore",
    source_path: str,
) -> None:
    """Remove all derived Server material facts for one obsolete workbook."""
    normalized_path = str(source_path or "")
    if not normalized_path:
        return
    store.connection.execute(
        "delete from server_material_allocations where source_path = ?",
        (normalized_path,),
    )
    store.connection.execute(
        "delete from material_items where source_type='aihouse' and source_path = ?",
        (normalized_path,),
    )


def _reconcile_authoritative_server_material_sources(
    store: "OrderIndexStore",
    folders_by_order: dict[str, set[str]],
) -> set[str]:
    """Keep only current Server-folder material sources for scanned orders.

    ``material_items`` deliberately includes ``source_path`` in its identity
    so a path migration cannot overwrite a newer source accidentally.  That
    safety property also means an old source root must be explicitly retired;
    otherwise identical workbooks from the old and new roots are summed by
    production and inventory calculations.
    """
    removed_orders: set[str] = set()
    for raw_order_id, raw_folders in folders_by_order.items():
        order_id = str(raw_order_id or "").strip().upper()
        folders = sorted({str(folder) for folder in raw_folders if str(folder)})
        if not order_id or not folders:
            continue
        material_paths = [
            str(row[0] or "")
            for row in store.connection.execute(
                "select distinct source_path from material_items "
                "where order_id=? and source_type='aihouse'",
                (order_id,),
            ).fetchall()
        ]
        for source_path in material_paths:
            if not _path_in_folders(source_path, folders):
                _delete_server_material_source_facts(store, source_path)
                removed_orders.add(order_id)

        source_rows = store.connection.execute(
            "select path, source_folder, order_id from source_files"
        ).fetchall()
        for path, source_folder, source_order in source_rows:
            source_order_ids = {
                token.strip().upper()
                for token in str(source_order or "").split("、")
                if token.strip()
            }
            if order_id not in source_order_ids:
                continue
            if not any(_path_in_folders(str(source_folder or ""), [folder]) for folder in folders):
                store.connection.execute("delete from source_files where path=?", (str(path),))
    return removed_orders


def _hardware_report_paths(
    paths: Iterable[Path],
    source_folder: Path,
) -> list[Path]:
    """Exclude nested recut Fittingslists when a base report exists."""
    all_paths = sorted({Path(path) for path in paths}, key=lambda item: str(item).casefold())
    base_paths = [
        path for path in all_paths
        if not _is_recut_server_report(path, source_folder)
    ]
    return base_paths or all_paths


def _selected_hardware_report_paths(
    source_rows: Iterable[tuple[str, str]],
) -> set[str]:
    """Select one non-recut Fittingslist block per factory and folder."""
    grouped: dict[str, list[Path]] = defaultdict(list)
    for path, source_folder in source_rows:
        if path and source_folder:
            grouped[str(source_folder)].append(Path(path))
    selected_paths: set[str] = set()
    for source_folder, paths in grouped.items():
        candidates = _hardware_report_paths(paths, Path(source_folder))
        try:
            selected, _, _, _ = select_latest_fittings(candidates)
        except RuleError:
            # The normal sync pass records the detailed report error. Keep the
            # candidate paths here so the preview does not silently erase all
            # hardware while that error is being shown.
            selected_paths.update(str(path) for path in candidates)
        else:
            selected_paths.update(str(item.path) for item in selected.values())
    return selected_paths


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
    """Return marker files from the known AICNC layouts without file recursion.

    An order folder may contain several AICNC workspaces, but each workspace
    is either the order folder itself or one of its direct children.  The
    marker files then live at one of the known relative paths below that
    workspace.  Keeping discovery to these paths avoids walking PNG/NC/CSV
    outputs on the network Server while still supporting the current New
    Nesting and old Auo-Label-CNC layouts.
    """
    scopes = [folder]
    scan_complete = True
    try:
        scopes.extend(
            sorted(
                (path for path in folder.iterdir() if path.is_dir()),
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
    """Return recognizable CNC optimization outputs under known layouts."""
    artifacts, _ = _optimization_artifact_paths(folder)
    return artifacts


def _optimization_result_artifacts(folder: Path) -> list[Path]:
    """Return AICNC nesting results that carry exact factory-order identity."""
    return [path for path in _optimization_artifacts(folder) if path.name.casefold() == "nesting_result.xml"]


def _optimization_result_artifacts_checked(folder: Path) -> tuple[list[Path], bool]:
    """Return result files plus whether fixed-path discovery completed."""
    artifacts, scan_complete = _optimization_artifact_paths(folder)
    return [
        path for path in artifacts
        if path.name.casefold() == "nesting_result.xml"
    ], scan_complete


def _server_optimization_monitor_files(folder: Path) -> list[tuple[Path, str]]:
    """Return the two XML files used as the lightweight Server change marker."""
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
    """Read factory order ids embedded by AICNC without loading the XML at once."""
    factory_orders: set[str] = set()
    for _, element in ET.iterparse(path, events=("start",)):
        factory_order = str(element.attrib.get("OrderID", "")).upper().strip()
        if FACTORY_RE.fullmatch(factory_order):
            factory_orders.add(factory_order)
        element.clear()
    return factory_orders


def _file_timestamp(value: float) -> str:
    return datetime.fromtimestamp(value).isoformat(timespec="seconds") if value else ""


def _canonical_source_folder(source_root: Path, folder_name: str) -> Path:
    """Return the existing Server child using its filesystem spelling.

    macOS commonly treats Server paths as case-insensitive while SQLite keys
    remain case-sensitive.  Reusing the actual directory entry prevents a
    manual outbound from creating a second temporary-order row whose only
    difference is path casing.
    """
    root = source_root if source_root.is_absolute() else source_root.resolve()
    try:
        for candidate in root.iterdir():
            if candidate.is_dir() and candidate.name.casefold() == folder_name.casefold():
                return candidate
    except OSError:
        pass
    return root / folder_name


def _record_server_baseline(store: OrderIndexStore, folder: Path, *, order_id: str = "") -> None:
    """Record the current Server metadata after a successful manual outbound."""
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
    """Record the current standard-order Server reports after outbound sync."""
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
    """Register an App-created material file without accepting other changes."""
    # Preserve the caller's path spelling.  The Server snapshot uses the
    # spelling returned by directory enumeration; resolving only here can
    # turn /var into /private/var on macOS and create a false mismatch.
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
    """Return recognized reports directly inside a folder, not child folders."""
    return [(path, kind) for path, kind in _report_files(folder) if path.parent == folder]


def _merge_candidate(candidates: dict[str, dict], factory_order: str, *, name: str = "", source: str,
                     order_id: str = "", sales_order_name: str = "", split_time: str = "",
                     folder: str = "", has_hardware: bool = False,
                     derive_order_from_name: bool = True, optimized: bool = False) -> None:
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
    aimes_names = sorted(candidate["names"].get("aimes", set()))
    exact_aimes_names = sorted(candidate["names"].get("aimes_exact", set()))
    server_names = sorted(candidate["names"].get("server", set()))
    factory_name = aimes_names[0] if aimes_names else (
        exact_aimes_names[0] if exact_aimes_names else (server_names[0] if server_names else "")
    )
    aimes_orders = {_valid_aimes_order_id(name) for name in candidate.get("sales_orders", set())}
    aimes_orders.discard("")
    if len(aimes_orders) == 1:
        # AIMES is the authority for the factory-order name and owner. A
        # stale/mixed server report must not turn an AIMES-confirmed factory
        # into a false ownership conflict.
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
    """Reuse the indexed identity for an unchanged board/fittings report.

    ``source_files`` already stores the factory-order identity discovered by
    the previous parse.  The corresponding ``factory_orders`` row stores the
    remaining candidate facts, so reopening an unchanged workbook is not
    necessary.  Return whether a usable cached identity was found; callers
    use a false result as the safe fallback to the normal parser.
    """
    row = store.connection.execute(
        "select order_id, factory_order from source_files where path = ?",
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
                   name_source, has_hardware, optimized
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


def _refresh_cached_optimization_artifacts(
    store: OrderIndexStore,
    validation_rows: list[tuple[str, str]],
    *,
    timing_sink: list[dict[str, object]] | None = None,
) -> int:
    """Persist exact AICNC optimization evidence and refresh factory state.

    ``nesting_result.xml`` embeds the AIMES factory order in ``OrderID``.
    Its modification time is the AICNC generation time; filesystem birth time
    is only the later copy-to-Server time.  Keeping both plus first-seen time
    prevents an index refresh timestamp from masquerading as a business event.
    """
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
                where order_id = ? and aimes_status = 'active' and ownership_status = '已确认'
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
            for factory_order in sorted(artifact_factory_orders):
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
        # A complete readable scan may correct the historical blanket status.
        # Previously observed evidence remains durable even if an old Server
        # file is later archived, while a newly added AIMES factory starts at 0.
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
            optimized = bool(evidence and evidence[1])
            current = store.connection.execute(
                """
                select optimized, optimization_first_completed_at,
                       optimization_latest_completed_at, optimization_first_seen_at,
                       optimization_latest_seen_at, optimization_source_path
                from factory_orders where factory_order=?
                """,
                (factory_order,),
            ).fetchone()
            desired = (
                int(optimized),
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
                    optimized=?,
                    optimization_first_completed_at=?,
                    optimization_latest_completed_at=?,
                    optimization_first_seen_at=?,
                    optimization_latest_seen_at=?,
                    optimization_source_path=?,
                    report_state=case when ? then '已发现' else report_state end,
                    updated_at=?
                where factory_order=? and order_id=?
                """,
                desired + (int(optimized), observed_at, factory_order, order_id),
            )
            refreshed += 1
    return refreshed


def _load_outbound_records(config: Config) -> list[dict]:
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
                        # ``remark`` identifies the exact factory for status
                        # matching; the header value identifies the source
                        # document (for example, an order-level materials
                        # document whose relation covers one factory).
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
    # The storage cutover intentionally has no JSON fallback.  A missing
    # central database means there is no authoritative outbound fact to use.
    return []


def _outbound_key(value: object) -> str:
    return re.sub(r"[\s_-]+", "", str(value or "")).casefold()


def _outbound_exact_aliases(factory: dict) -> set[str]:
    """Return identities that can safely identify one factory order."""
    return {
        _outbound_key(factory.get("factory_name")),
        _outbound_key(factory.get("factory_order")),
    } - {""}


def _outbound_record_matches_factory(record: dict, factory: dict, *, allow_order_alias: bool) -> bool:
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
    """Return whether a shipped hardware document is scoped to this factory."""
    return any(
        str(record.get("kind", "")).strip().casefold() == "hardware"
        and str(record.get("status", "")).strip() == "已出库"
        and _outbound_record_matches_factory(record, factory, allow_order_alias=False)
        for record in records
    )


def _factory_outbound_metadata(config: Config, factory: dict) -> tuple[str, str]:
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
    """Read the local outbound audit records without querying or writing JDY."""
    if not factory["order_id"] or not factory["factory_name"]:
        return "未查询", ""
    records = _load_outbound_records(config) if records is None else records
    outbound_mode, stored_fingerprint = _factory_outbound_metadata(config, factory)
    allow_order_alias = bool(factory_group and len(factory_group) == 1)
    production_document_numbers = {
        str(record.get("document_number", "")).strip()
        for record in records
        if str(record.get("kind", "")).strip().casefold() == "production_materials"
        and str(record.get("document_number", "")).strip()
    }
    exact_records = []
    order_alias_records = []
    exact_aliases = _outbound_exact_aliases(factory)
    for record in records:
        if _outbound_key(record.get("order_id")) != _outbound_key(factory.get("order_id")):
            continue
        if (
            str(record.get("kind", "")).strip().casefold() == "production_materials"
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
    # Prefer a factory-specific hardware document over an order-level
    # materials document when both exist.  Otherwise the earlier materials
    # number can mask the actual factory outbound document in the dashboard.
    matching_records = exact_records + order_alias_records
    # A split factory can have both the historical order-level materials
    # document and a newer factory-scoped hardware document.  The material
    # document must not make the factory look stale after the hardware was
    # successfully shipped; once a hardware record exists, reconcile only
    # factory-scoped hardware records for this factory.
    hardware_records = [
        record for record in matching_records
        if str(record.get("kind", "")).strip().casefold() == "hardware"
    ]
    if hardware_records:
        matching_records = hardware_records
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
                    # Order-center material previews use the central SQLite
                    # database as their source path.  If the document is no
                    # longer present in the current database, do not pass
                    # that SQLite path to ``parse_traveler``; an absent
                    # document is a valid changed/removed-source case and is
                    # compared as an empty item list below.
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
                        # Standard order outbound records may retain the
                        # material source workbook as ``traveler_path`` for a
                        # room-level document. It is not a Traveler and its
                        # sheet layout is intentionally different. Without a
                        # matching database document, do not infer a changed
                        # outbound document from an incompatible source file.
                        if document_number:
                            document_numbers.append(document_number)
                        continue
                    if InventorySyncStore.raw_document_fingerprint(current_items) != recorded_raw:
                        document_numbers.append(document_number)
                        return "需要更新", "、".join(filter(None, document_numbers))
                except (OSError, KeyError, TypeError, ValueError, RuleError):
                    # Keep the last confirmed shipped state when the current
                    # Traveler cannot be read; the inventory workflow will
                    # surface the concrete parse/read error on retry.
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
    """Enforce the standard-order outbound gate from persisted SQLite state.

    A previously shipped factory order remains blocked unless the current
    mapped source data has changed and the caller explicitly lists that
    factory order in ``changed_factory_orders``.
    """
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
        # Refresh the derived status first so a changed Traveler/report is
        # represented as 可更新 rather than being treated as a duplicate.
        reconcile_outbound_statuses(config, store)
        placeholders = ",".join("?" for _ in selected)
        rows = store.connection.execute(
            f"""
            select factory_order, order_id, outbound_status, outbound_document
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
) -> int:
    """Reconcile successful inventory records into persisted factory status.

    The inventory audit file is the local evidence of a successful outbound.
    A record whose remark is only the order id is assigned only when that
    order currently has one factory order; this prevents one outbound record
    from incorrectly marking several split factory orders as shipped.
    """
    owns_store = store is None
    store = store or OrderIndexStore(config.workflow_database)
    records = _load_outbound_records(config)
    rows = store.connection.execute(
        """
        select factory_order, order_id, factory_name, sales_order_name,
               outbound_status, outbound_document, outbound_mode, outbound_fingerprint,
               outbound_completed_at
        from factory_orders
        where order_id <> '' and aimes_status = 'active'
        """
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

    updated = 0
    for factory in factories:
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
            if str(record.get("kind", "")).strip().casefold() == "production_materials"
            and str(record.get("document_number", "")).strip()
        }
        stale_production_status = (
            status == "未出库"
            and str(factory.get("outbound_document", "")).strip() in production_document_numbers
        )
        # Legacy migration records prior hardware shipment separately from
        # the old combined material document.  Do not let the old material
        # fingerprint turn that historical shipment back into "需要更新".
        legacy_production = store.connection.execute(
            """select 1 from manual_production_batch_factories f
               join manual_production_batches b on b.batch_id=f.batch_id
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
            set outbound_status = ?, outbound_document = ?, outbound_mode = ?,
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
    resolved_issues = _resolve_fully_shipped_server_issues(config, store)
    if updated or resolved_issues:
        store.commit()
    if owns_store:
        store.close()
    return updated


def _orders_requiring_server_scan(
    config: Config,
    store: OrderIndexStore,
    aimes_rows: list[dict] | None = None,
) -> set[str]:
    """Return AIMES orders whose factory work is not completely shipped.

    The database keeps historical AIMES sightings.  The optional current rows
    are merged in memory so a newly split factory order can trigger a Server
    scan before the next index write.
    """
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
            # Outbound status is maintained transactionally when the inventory
            # operation succeeds. A normal AIMES/Server scan consumes that
            # fact; it does not reopen every outbound document to prove it.
            statuses = {str(item.get("outbound_status") or "未查询") for item in items}
        if not statuses or statuses != {"已出库"}:
            result.add(order_id)
    return result


def _aimes_factory_records(
    store: OrderIndexStore,
    aimes_rows: list[dict] | None = None,
) -> dict[str, dict]:
    """Return active AIMES factory facts, optionally merged with fresh rows."""
    factories: dict[str, dict] = {}
    for row in store.connection.execute(
        """
        select factory_order, order_id, factory_name, sales_order_name,
               split_time, outbound_status, outbound_document, outbound_mode,
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
    """Return whether one order should remain in the automatic Server scan."""
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
        # The changed AIMES identity is itself a scan trigger.  The baseline
        # is updated only after the folder has actually been included in a
        # scan, so a failed/unavailable scan cannot silently consume a change.
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
            # A malformed or missing watch deadline is repaired conservatively
            # by starting a fresh seven-day observation window.
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
    """Apply per-order historical and seven-day Server scan policies."""
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
    """Commit AIMES baselines after the corresponding folders were scanned."""
    requires_scan = _orders_requiring_server_scan(config, store)
    for folder in folders:
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
    """Apply the user's historical shipment confirmation before scanning."""
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
                "select validation_status from orders where order_id = ?",
                (order_id,),
            ).fetchone()
            if stale_validation and stale_validation[0] == "数据异常":
                # Historical folders are intentionally not re-read after the
                # initial date. Keep material validation honest as pending,
                # but do not let an old missing-report error override the
                # user-confirmed shipped business stage.
                store.connection.execute(
                    "update orders set validation_status = '待校验', validation_message = '', updated_at = ? where order_id = ?",
                    (now, order_id),
                )
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
                select factory_order, outbound_status, outbound_document, outbound_mode
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
                    set outbound_status = ?, outbound_mode = ?, updated_at = ?
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
    """Return order ids represented by a standard or mixed Server folder."""
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
    """Return whether every known order in a standard/mixed folder is shipped.

    An order without an active AIMES mapping is deliberately not considered
    shipped: the scanner must keep the folder eligible until its identity is
    known.  Fresh AIMES rows are merged in memory so a newly discovered factory
    order can reopen a folder during the same sync.
    """
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
        # Historical folders confirmed as shipped by the user are allowed to
        # remain permanently outside the ordinary AIMES mapping set.  A later
        # AIMES row changes the fingerprint and reopens the folder through the
        # dedicated scan-policy path.
        if not all(
            (store.server_scan_policy(order_id) or {}).get("policy") in {"legacy", "permanent"}
            for order_id in unmapped
        ):
            return False
    return not (order_ids & _orders_requiring_server_scan(config, store, aimes_rows))


def _server_folder_for_issue(issue_path: str) -> Path | None:
    """Find the standard/mixed Server folder containing an issue path."""
    path = Path(issue_path).expanduser()
    # Some issues point at the offending file, while folder-level issues such
    # as hardware selection point directly at the order folder.  Include the
    # path itself so both forms resolve to the same Server-order boundary.
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
) -> int:
    """Close stale Server issues once every order in their folder shipped.

    Material validation and hardware selection issues can be created before
    the outbound workflow finishes.  Automatic scans correctly stop selecting
    a fully shipped folder, so those old issues otherwise have no later
    validation pass that could close them.  Keep the historical sync_changes
    rows, but remove the stale open items.
    """
    # A validation error can remain open after the order has been completely
    # shipped (for example, a transient AIMES credential failure during a
    # later index refresh).  Once every known factory order in the folder has
    # a confirmed outbound record, the folder is intentionally excluded from
    # automatic Server scans, so that stale order-level validation issue must
    # be closed here as well.  Keep the historical sync_changes row intact.
    resolvable_kinds = {
        "material_validation",
        "hardware_selection",
        "order_validation",
    }
    resolved = 0
    for issue in store.active_issues():
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


def _aimes_row_signature(rows: list[dict]) -> list[tuple[str, str, str, str]]:
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
    """Persist only validated AIMES mapping rows.

    Invalid rows are returned to the caller as one-operation warnings. They
    are deliberately absent from both the source cache and the factory-name
    cache so a malformed AIMES sales-order name cannot become business data.
    """
    # The online endpoint intentionally returns only a recent page.  Keep the
    # local cache as a cumulative identity cache as well, so a later 50-row
    # fetch cannot make older, still-valid AIMES facts disappear locally.
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
    return [
        str(row[0]).upper()
        for row in store.connection.execute(
            """
            select factory_order
            from factory_orders
            where aimes_status='active'
              and factory_order like 'F%'
              and (order_id like 'PP%' or order_id like 'CS%')
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
    """Exact-check local active factories absent from the recent AIMES page.

    Absence from a 50-row snapshot is not deletion evidence by itself. Only
    an explicit AIMES query returning no matching row can transition a record
    to the inactive audit state.
    """
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


def sync_aimes_index(config: Config, *, force: bool = False, if_needed: bool = False) -> dict:
    """Refresh only AIMES identity data; never scan or parse Server files.

    Keeping this boundary separate from Server scanning matters for both
    performance and diagnosis: an AIMES refresh can update factory identity
    evidence without implying that a Server report changed.
    """
    from .core import refresh_aimes_recent_orders

    operation_started = time.perf_counter()
    started = _now()
    store = OrderIndexStore(config.workflow_database)
    if config.reconcile_outbound_on_read:
        reconcile_outbound_statuses(config, store)
    today = date.today().isoformat()
    cached_source_rows = load_aimes_order_cache(config)
    cached_rows, cached_issues = _partition_aimes_rows(
        cached_source_rows,
        store.ignored_aimes_keys(),
        store.aimes_assignments(),
    )
    # Format-invalid rows are transient fetch warnings, not persistent review
    # records. Clear rows written by older versions before returning anything.
    store.replace_aimes_review_rows([])
    store.commit()
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
                "warning_count": 0,
                "duration_seconds": round(time.perf_counter() - operation_started, 2),
                "error": "",
            },
            "aimes_issues": [],
            "aimes_warnings": [],
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
            fetched = _merge_aimes_recent_and_verified_rows(fetched, verification_result)
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
                "warning_count": 0,
                "duration_seconds": round(time.perf_counter() - operation_started, 2),
                "error": message,
            },
            "aimes_issues": [],
            "aimes_warnings": [],
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
    store.replace_aimes_review_rows([])
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


def _temporary_folder_is_candidate(config: Config, store: OrderIndexStore, folder: Path) -> bool:
    """Select eligible recent or never-processed non-standard folders for review."""
    try:
        created_at = _folder_created_at(folder)
    except OSError:
        return False
    baseline = _server_scan_baseline(config)

    # Ordinary old temporary folders are excluded before any recursive report
    # enumeration.  This is intentionally before the fingerprint call above:
    # the age check is the inexpensive guard on a network-mounted Server.
    if created_at < baseline:
        return False

    existing = store.temporary_order(str(folder))
    if existing and existing.get("outbound_status") == "已出库":
        # A processed temporary folder gets the same lightweight XML watch as
        # a shipped standard order, but the watch is only three days. Excel
        # reports are intentionally not consulted after processing.
        policy = str(existing.get("server_scan_policy") or "").strip()
        if policy == "permanent":
            return False
        marker_files = _server_optimization_monitor_files(folder)
        if not marker_files:
            # Without either approved XML marker there is no safe signal for
            # the three-day observation window. Preserve the legacy shipped
            # behavior instead of recursively reading report workbooks.
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
    """Find existing non-standard folders that must no longer remain pending."""
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
    """Clear persisted pending state for old non-standard Server folders."""
    roots = _available_server_roots(config)
    if not roots:
        return None
    stale_folders: set[str] = set()
    for root in roots:
        stale_folders.update(_temporary_folders_before_server_baseline(config, root))
    if stale_folders:
        store.clear_server_folder_pending_records(stale_folders)
        store.commit()
    return roots[0]


def _folder_order_ids(folder: Path) -> list[str]:
    """Return complete order ids encoded by a Server folder and its reports."""
    from .order_workflow import related_order_ids

    return list(dict.fromkeys(order_id.upper() for order_id in related_order_ids(folder) if order_id))


def _temporary_order_id(folder: Path) -> str:
    """Return a stable internal key for one temporary source folder."""
    stat = folder.stat()
    identity = f"{folder.resolve()}\n{getattr(stat, 'st_ino', 0)}\n{_folder_created_at(folder):.6f}"
    return "TMP:" + hashlib.sha256(identity.encode("utf-8")).hexdigest()[:24]


def _reconcile_temporary_order_projections(store: OrderIndexStore) -> int:
    """Remove the old temporary-folder projection from the formal order table.

    Temporary/rework folders are identified by their source path and live in
    ``temporary_orders``.  Older sync code also inserted their parsed order
    number into ``orders``; because ``orders.order_id`` is the formal-order
    primary key, that projection could overwrite the formal order's type and
    source folder.  Keep a formal row when AIMES confirms the order, otherwise
    remove the orphan projection so the task is represented only by the
    pending-center ledger.
    """
    rows = store.connection.execute(
        "select order_id, source_folder from orders where order_type = 'temporary'"
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
    """Fingerprint the folder's relevant workbooks for duplicate-outbound protection."""
    entries = []
    for path in sorted(folder.rglob("*.xlsx"), key=lambda item: str(item).casefold()):
        if path.name.startswith("~$") or not path.is_file():
            continue
        # A material workbook generated by the app is an output of this
        # processing run, not a new source change.  Otherwise the next scan
        # would see its own generated file and schedule a duplicate outbound.
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
    """Return whether a processed temporary folder still has its XML baseline."""
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
    """Match a non-standard folder name to one unique AIMES factory name."""
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
    """A non-standard name containing two order ids is a shared/mixed order.

    This helper is used by the lightweight scan, so it intentionally inspects
    only the folder name. Report contents are parsed later, after approval.
    """
    name_order_ids = {
        match.group(1).upper()
        for match in ORDER_TOKEN_RE.finditer(folder.name)
    }
    return (
        not _is_standard_order_folder(folder.name)
        and len(name_order_ids) >= 2
    )


def _temporary_folder_layout_error(folder: Path) -> str:
    """Validate only the workbooks needed to prepare a temporary order.

    Production folders often contain auxiliary Excel exports (door lists,
    packing lists, CNC lists).  They are not input reports and must not block
    a temporary order when the required material/board source is present.
    """
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
    """Mirror a successful manual outbound into the temporary-order ledger."""
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


def mark_temporary_folder_manual(config: Config, folder: Path) -> dict:
    """Record a temporary Server folder that was completed outside the App.

    Manual handling is an outbound fact and starts the three-day XML-only
    watch. It is not a reminder-suppression action.
    """
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
    if _is_standard_order_folder(selected.name) or _is_mixed_order_folder(selected):
        raise ValueError("已人工处理只适用于普通临时文件夹")

    marker_files = _server_optimization_monitor_files(selected)
    if not marker_files:
        raise ValueError("该临时文件夹没有 Optimize file.xml 或 nesting_result.xml，无法建立三天 XML 观察基线")

    now = _now()
    watch_until = (
        datetime.fromisoformat(now) + timedelta(days=TEMPORARY_SHIPPED_WATCH_DAYS)
    ).isoformat(timespec="seconds")
    store = OrderIndexStore(config.workflow_database)
    try:
        path = str(selected)
        previous = store.temporary_order(path) or {}
        fingerprint = _temporary_folder_fingerprint(selected)
        store.upsert_temporary_order(
            temporary_id=previous.get("temporary_id") or _temporary_order_id(selected),
            folder_name=selected.name,
            source_folder=path,
            folder_created_at=_folder_created_at(selected),
            content_fingerprint=fingerprint,
            traveler_path=previous.get("traveler_path", ""),
            traveler_fingerprint=previous.get("traveler_fingerprint", ""),
            traveler_include_hardware=previous.get("traveler_include_hardware"),
            traveler_status=previous.get("traveler_status", ""),
            traveler_generated_at=previous.get("traveler_generated_at", ""),
            processing_status="已人工处理",
            outbound_status="已出库",
            outbound_document=previous.get("outbound_document", ""),
            processed_at=previous.get("processed_at", "") or now,
            outbound_at=now,
            last_error="",
            server_scan_policy="watching",
            server_scan_watch_until=watch_until,
            server_scan_policy_updated_at=now,
        )
        _record_server_baseline(store, selected, order_id=selected.name.upper())
        store.save_server_scan_xml_baseline(
            [selected], _server_scan_xml_entries([selected]), observed_at=now
        )
        store.resolve_active_issue(f"temporary_processing:{selected}")
        store.resolve_active_issue(f"server_missing_report:{selected}")
        store.add_change(
            severity="info",
            kind="temporary_manual_outbound_reconciled",
            path=path,
            message=(
                f"用户确认临时文件夹 {selected.name} 已人工处理并出库；"
                "已记录当前文件基线，未来三天只观察两个 XML 文件"
            ),
            observed_at=now,
        )
        store.commit()
        return {
            "ok": True,
            "temporary_manual_handled": path,
            "outbound_status": "已出库",
            "server_scan_policy": "watching",
            "server_scan_watch_until": watch_until,
            "pending_server_changes": [],
            "current_issues": store.active_issues(),
        }
    finally:
        store.close()


def _temporary_order_ids(folder: Path) -> list[str]:
    order_ids = _folder_order_ids(folder)
    # A temporary folder may intentionally have no PP/CS order number.  Its
    # folder name is the user-visible temporary order identity and is written
    # to Traveler/Usage List and the outbound remark.
    return order_ids or [folder.name.strip()]


def _process_temporary_folder(
    config: Config,
    folder: Path,
    *,
    store: OrderIndexStore,
    include_hardware: bool = True,
) -> dict:
    """Validate, prepare Travelers, and perform the requested temporary outbound."""
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
                # A rework/replacement task is tracked by temporary_orders and
                # the pending center. Its materials must not overwrite the
                # formal order's central material/hardware facts.
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
    """Build one read-only Server folder snapshot without touching SQLite."""
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
    # Standard AICNC order folders use the two XML markers as their complete
    # change signal. Temporary and mixed folders do not have that contract:
    # their Excel reports are the only way to discover/ retry the manual
    # workflow, so retain the legacy report metadata scan for those folders.
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
        # ``duration_seconds`` is the accounted folder total shown to the
        # user: it is deliberately the exact sum of the per-file timings.
        # Keep the wall-clock measurement separately because folder.stat(),
        # directory iteration, and thread scheduling are not file processing.
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
    # Automatic scans apply the persisted per-order policy: historical orders
    # are skipped unless AIMES changes, while a newly fully-shipped order is
    # watched for seven days before it becomes permanent. Manual folder
    # selection does not use this snapshot path and remains an explicit
    # override.
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
            is_order_folder = _is_standard_order_folder(folder.name)
            if is_order_folder:
                if _order_type(folder.name) != _server_root_order_type(server_root):
                    continue
                if not _server_folder_scan_allowed(config, store, folder):
                    continue
            if (
                not is_order_folder
                and _is_mixed_order_folder(folder)
                and not _server_folder_scan_allowed(config, store, folder)
            ):
                continue
            if not is_order_folder and not _is_mixed_order_folder(folder) and not _temporary_folder_is_candidate(config, store, folder):
                continue
            folders.append(folder)

    snapshot: dict[str, dict] = {}
    if not folders:
        return root, snapshot
    xml_only_folders = {
        str(folder)
        for folder in folders
        if not _is_standard_order_folder(folder.name)
        and (store.temporary_order(str(folder)) or {}).get("server_scan_policy") == "watching"
    }
    scan_targets = [
        (folder, str(folder) in xml_only_folders)
        for folder in folders
    ]
    worker_count = min(SERVER_SNAPSHOT_MAX_WORKERS, len(scan_targets))
    with ThreadPoolExecutor(max_workers=worker_count) as executor:
        for folder_snapshot, folder_timing in executor.map(_server_snapshot_folder, scan_targets):
            snapshot.update(folder_snapshot)
            if timing_sink is not None:
                timing_sink.append(folder_timing)
    return root, snapshot


def _server_scan_xml_entries(folders: Iterable[Path]) -> list[dict[str, object]]:
    """Read the current XML marker metadata for completed Server scopes."""
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
    return config.state_dir / SERVER_SCAN_SNAPSHOT_FILENAME


def _write_server_scan_snapshot(
    config: Config,
    *,
    root: Path,
    roots: list[Path],
    scanned_at: str,
    entries: dict[str, dict],
) -> Path:
    """Persist the read-only scan result for the immediately following index update."""
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
    """Load a scan snapshot only when it still matches the configured roots."""
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
    """Match a renamed folder only when its recognized reports are identical.

    The match is deliberately conservative: same parent, non-empty identical
    report metadata, and exactly one candidate with the same order identity.
    Ambiguous or content-changing folders remain ordinary add/remove changes.
    """
    def folders(entries: dict[str, dict], previous_entries: bool) -> dict[str, set[str]]:
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
    """Move indexed source paths after a confirmed folder rename."""
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
                "update active_issues set path=? where path=? or path like ?",
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
    return {
        "board": "板材信息",
        "fittings": "五金信息",
        "folder": "工厂单文件夹和报表目录",
        "optimization_input": "优化输入 XML",
        "optimization_result": "优化结果 XML",
    }.get(kind, "报表数据")


def _summarize_server_read_items(items: list[tuple[str, str, str]]) -> str:
    """Summarize indexed Server reads without exposing every absolute path.

    ``items`` contains ``(path, source_folder, kind)`` entries.  The complete
    paths remain in the index and error records; this display-only summary is
    intentionally short enough for the dashboard hover panel.
    """
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
    """Return distinct order and factory-order counts for an operation trace."""
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
    """Keep only non-overlapping AIMES stages in the display contract."""
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
    """Make the flat stage list account for backend-only preparation/cleanup."""
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
        f"解析并校验变化材料文件 {float(stats.get('material_validation_seconds', 0)):.2f} 秒；"
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


def _validate_materials_during_server_scan(
    config: Config,
    folders: list[Path],
    seen_at: str,
) -> None:
    """Validate changed material workbooks in an isolated preview database.

    Server scanning must not write order or factory facts, but it should still
    tell the user that a material workbook needs manual correction before the
    preview/confirmation step becomes available.
    """
    if not folders:
        return
    store = OrderIndexStore(config.workflow_database)
    try:
        for folder in folders:
            folder_path = str(folder)
            order_ids = _server_folder_order_ids(folder)
            display_order_id = "、".join(sorted(order_ids))
            try:
                preview_server_changes(config, [folder])
            except RuleError as exc:
                if exc.code != "material_validation":
                    continue
                issue_rows = exc.context.get("issues") or []
                if not issue_rows:
                    issue_rows = [{"path": folder_path, "message": str(exc)}]
                for issue in issue_rows:
                    path = str(issue.get("path") or folder_path)
                    message = f"material 文件校验未通过：{issue.get('message') or str(exc)}"
                    issue_key = f"material_validation:{display_order_id}:{path}"
                    store.upsert_active_issue(
                        issue_key=issue_key,
                        kind="material_validation",
                        order_id=display_order_id,
                        path=path,
                        message=message,
                        seen_at=seen_at,
                    )
                    store.add_change(
                        severity="warning",
                        kind="material_validation",
                        order_id=display_order_id,
                        message=message,
                        path=path,
                        observed_at=seen_at,
                    )
            except (OSError, ValueError):
                # The metadata scan remains useful even when an isolated
                # preview cannot be assembled for a folder without enough
                # order evidence. The actionable material parser errors are
                # returned as RuleError above.
                continue
            else:
                for issue in store.active_issues():
                    if issue.get("kind") != "material_validation":
                        continue
                    if _path_in_folders(str(issue.get("path") or ""), [folder_path]):
                        store.resolve_active_issue(issue["issue_key"])
        store.commit()
    finally:
        store.close()


def scan_server_changes(config: Config) -> dict:
    """Compare Server metadata without advancing the processed baseline.

    The scan may clean stale pending state for folders excluded by the configured
    baseline; it never marks currently visible material/report files as processed.
    AICNC ``nesting_result.xml`` is a separately approved, read-only status
    source, so the scan may persist its exact factory-order optimization evidence.
    """
    scanned_at = _now()
    scan_started = time.perf_counter()
    store = OrderIndexStore(config.workflow_database)
    server_folder_timings: list[dict[str, object]] = []
    optimization_file_timings: list[dict[str, object]] = []
    _clear_stale_server_pending_state(config, store)
    root, current = _server_snapshot(
        config,
        store,
        timing_sink=server_folder_timings,
    )
    _resolve_fully_shipped_server_issues(config, store)
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
        and (store.temporary_order(str(item.get("source_folder") or "")) or {}).get("server_scan_policy") == "watching"
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
    # Existing processed folders already have a folder baseline in source_files.
    # Seed the new XML-only baseline for those folders without turning the first
    # post-migration scan into a false batch of new changes.
    known_folders = {
        str(row[0])
        for row in store.connection.execute(
            "select path from source_files where kind = 'folder'"
        ).fetchall()
    }
    bootstrap_folders = {
        folder for folder in current_folders
        if folder in known_folders
        and not any(item.get("source_folder") == folder for item in previous_all.values())
    }
    bootstrap_entries = [
        dict(item, path=path)
        for path, item in current_xml.items()
        if item.get("source_folder") in bootstrap_folders
    ]
    if bootstrap_folders:
        store.save_server_scan_xml_baseline(
            [Path(folder) for folder in bootstrap_folders],
            bootstrap_entries,
            observed_at=scanned_at,
        )
        store.commit()
        previous_all.update({
            str(item["path"]): {
                "source_folder": str(item["source_folder"]),
                "kind": str(item["kind"]),
                "order_id": str(item.get("order_id") or ""),
                "modified_at": int(item.get("modified_at") or 0),
                "size": 0,
                "manual_only": False,
                "mixed_order": False,
            }
            for item in bootstrap_entries
        })
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
    # Temporary and mixed folders retain the report-metadata workflow. Their
    # reports are deliberately outside the XML-only standard-order contract.
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
    # A mixed-order folder is recognized from its name before report parsing.
    # Keep it actionable when no usable report exists, but leave the actual
    # workbook parsing to the explicit preview/processing step.
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
    # A failed temporary-order processing run must remain actionable, but it
    # must not erase the metadata baseline.  Keep the original source paths as
    # the comparison baseline and surface a virtual pending change from the
    # active issue instead.  This prevents an unchanged retry from being
    # mislabeled as a newly discovered order.
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
    order_folder_count = sum(item["kind"] == "folder" for item in current.values())
    related_xml_count = len(current_xml)
    related_legacy_count = sum(item["kind"] != "folder" for item in current_legacy.values())
    metadata_finished = time.perf_counter()
    scan_stats: dict[str, int | float] = {
        # Keep this distinct from the full scan total below.  The Server scan
        # also parses changed material workbooks for validation, so reporting
        # only the metadata traversal as the total was misleading.
        "metadata_scan_seconds": round(metadata_finished - scan_started, 6),
        "order_folder_count": order_folder_count,
        # The current scanner checks only the two optimization XML markers in
        # each included folder. Report workbooks are parsed later only when a
        # user opens the preview.
        "quick_checked_file_count": related_xml_count + related_legacy_count,
        "reused_folder_count": 0,
        "deep_scanned_folder_count": order_folder_count,
        "related_xml_count": related_xml_count,
        # Keep the old key for clients that decode older scan payloads. It no
        # longer represents the files considered by this Server scan.
        "related_excel_count": related_legacy_count,
        "added_count": sum(item["change_type"] == "added" for item in changes),
        "modified_count": sum(item["change_type"] == "modified" for item in changes),
        "deleted_count": sum(item["change_type"] == "removed" for item in changes),
        "renamed_count": sum(item["change_type"] == "renamed" for item in changes),
    }
    store.commit()
    store.close()
    validation_started = time.perf_counter()
    validation_finished = time.perf_counter()
    store = OrderIndexStore(config.workflow_database)
    optimization_started = time.perf_counter()
    optimization_rows = store.connection.execute(
        """
        select distinct orders.order_id, orders.source_folder
        from orders
        join factory_orders on factory_orders.order_id = orders.order_id
        where orders.source_folder <> ''
          and factory_orders.aimes_status = 'active'
          and exists (
              select 1 from factory_orders pending
              where pending.order_id = orders.order_id
                and pending.aimes_status = 'active'
                and pending.outbound_status <> '已出库'
          )
        """
    ).fetchall()
    optimization_refreshed = _refresh_cached_optimization_artifacts(
        store,
        optimization_rows,
        timing_sink=optimization_file_timings,
    )
    folder_timing_by_path = {
        str(item.get("source_folder") or ""): item
        for item in server_folder_timings
        if item.get("source_folder")
    }
    for item in optimization_file_timings:
        folder_path = str(item.get("source_folder") or "")
        if not folder_path:
            continue
        folder = folder_timing_by_path.setdefault(
            folder_path,
            {
                "source_folder": folder_path,
                "duration_seconds": 0.0,
                "files": [],
                "error": "",
            },
        )
        files = folder.setdefault("files", [])
        existing = next(
            (
                value for value in files
                if isinstance(value, dict)
                and str(value.get("path") or "") == str(item.get("path") or "")
            ),
            None,
        )
        if existing is None:
            files.append(item)
        else:
            existing["duration_seconds"] = round(
                float(existing.get("duration_seconds", 0) or 0)
                + float(item.get("duration_seconds", 0) or 0),
                6,
            )
            if item.get("error"):
                existing["error"] = item["error"]
        # Recalculate from the final file list so rounding and same-path
        # aggregation cannot make the folder total differ from its files.
        folder["duration_seconds"] = round(
            sum(
                float(value.get("duration_seconds", 0) or 0)
                for value in folder.get("files", [])
                if isinstance(value, dict)
            ),
            6,
        )
    for folder in folder_timing_by_path.values():
        folder["duration_seconds"] = round(
            sum(
                float(value.get("duration_seconds", 0) or 0)
                for value in folder.get("files", [])
                if isinstance(value, dict)
            ),
            6,
        )
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
    optimization_finished = time.perf_counter()
    snapshot_path = ""
    try:
        snapshot_path = str(
            _write_server_scan_snapshot(
                config,
                root=root,
                roots=_available_server_roots(config),
                scanned_at=scanned_at,
                entries=current,
            )
        )
    except OSError:
        # The next sync can safely fall back to its own read-only traversal.
        snapshot_path = ""
    completed = time.perf_counter()
    scan_stats["material_validation_seconds"] = round(validation_finished - validation_started, 6)
    scan_stats["optimization_evidence_seconds"] = round(optimization_finished - optimization_started, 6)
    scan_stats["optimization_artifact_refresh_count"] = optimization_refreshed
    scan_stats["finalize_seconds"] = round(completed - optimization_finished, 6)
    scan_stats["duration_seconds"] = round(completed - scan_started, 6)
    timing_stages = [
        {
            "stage": "server_metadata",
            "label": "读取并比对 Server 文件",
            "duration_seconds": scan_stats["metadata_scan_seconds"],
        },
        {
            "stage": "material_validation",
            "label": "解析并校验变化材料文件",
            "duration_seconds": scan_stats["material_validation_seconds"],
        },
        {
            "stage": "optimization_evidence",
            "label": "读取 AICNC 优化证据",
            "duration_seconds": scan_stats["optimization_evidence_seconds"],
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
    roots = _available_server_roots(config)
    if not roots:
        from .order_workflow import resolve_source_root
        resolve_source_root(config.source_root)
    root = roots[0]

    def containing_root(candidate: Path) -> Path | None:
        return next((server_root for server_root in roots if _path_is_within(candidate, server_root)), None)

    if selected_folders is not None:
        folders = []
        for selected in selected_folders:
            candidate = selected.expanduser().resolve()
            if not candidate.is_dir() or containing_root(candidate) is None:
                raise RuleError("server_folder_invalid", f"所选 Server 文件夹无法访问或不在 Server 根目录内：{selected}")
            if not _is_standard_order_folder(candidate.name) and not _direct_report_files(candidate) and not _report_files(candidate):
                raise RuleError(
                    "server_folder_invalid",
                    "选错了文件夹：请选择订单文件夹，或选择包含 material、板材清单或 Fittingslist 的临时订单文件夹。",
                )
            folders.append(candidate)
        return root, list(dict.fromkeys(folders))

    if selected_folder is None:
        if store is None:
            store = OrderIndexStore(config.workflow_database)
            close_store = True
        else:
            close_store = False
        folders = []
        for server_root in roots:
            folders.extend(
                folder
                for folder in server_root.iterdir()
                if folder.is_dir()
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
    if not selected.is_dir() or containing_root(selected) is None:
        raise RuleError("server_folder_invalid", "所选文件夹无法访问，请重新选择 Server 订单文件夹。")
    if _is_standard_order_folder(selected.name):
        return selected, [selected]
    if _direct_report_files(selected):
        # A non-standard folder containing recognized Server reports is a
        # temporary or mixed order. Keep the folder itself as the processing scope;
        # never expand it into child order folders.
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
    """Clear an old SKU validation error after its mapping is now resolved."""
    cleared = 0
    for order_id in sorted({value.upper() for value in order_ids if value}):
        mapping_prefixes = (
            f"material_mapping:{order_id}:",
            f"hardware_mapping:{order_id}:",
        )
        if any(key.startswith(mapping_prefixes) for key in current_issue_keys):
            continue
        row = store.connection.execute(
            "select validation_status, validation_message from orders where order_id = ?",
            (order_id,),
        ).fetchone()
        if not row or row[0] != "数据异常" or "未完成商品 SKU 处理" not in (row[1] or ""):
            continue
        store.connection.execute(
            "update orders set validation_status = '正常', validation_message = '', updated_at = ? where order_id = ?",
            (seen_at, order_id),
        )
        cleared += 1
    return cleared


def _exact_resolve_unowned_factories(config: Config, candidates: dict[str, dict]) -> str:
    """Use exact AIMES lookups only for factory orders absent from local DB.

    The local factory-order table is the durable identity index. A Server
    report may be re-read with only a partial name, so callers hydrate
    candidates from that table before considering an online exact lookup.
    Exact lookup is reserved for a genuinely new factory order that has no
    local identity.
    """
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
    """Reuse durable factory identity before any exact AIMES lookup."""
    if not candidates:
        return set()
    placeholders = ",".join("?" for _ in candidates)
    rows = store.connection.execute(
        f"""
        select factory_order, order_id, factory_name, sales_order_name,
               split_time, name_source, has_hardware, optimized
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
) -> dict:
    """Refresh AIMES/Server facts into the local order index and return summaries.

    Normal dashboard refreshes are incremental: unchanged report metadata is
    reused from SQLite and only orders touched by a Server report change are
    previewed again.  ``full_refresh`` remains available for an explicit
    integrity refresh or troubleshooting.
    """
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
        nonlocal phase_started
        now = time.perf_counter()
        phase_durations[name] = round(now - phase_started, 3)
        phase_started = now

    inventory_mappings = (
        InventoryMappings(config.workflow_database, connection=config.workflow_connection)
        if config.storage_prepared else None
    )
    # InventoryMappings opens short-lived read connections to the same
    # workflow database.  Initialize it before OrderIndexStore starts its
    # schema transaction, and reuse it throughout this sync.
    store = OrderIndexStore(config.workflow_database, connection=config.workflow_connection)
    _mark_initial_orders_shipped(config, store)
    _reconcile_temporary_order_projections(store)
    if reconcile_outbound:
        reconcile_outbound_statuses(config, store)
    _clear_stale_server_pending_state(config, store)
    store.delete_stale_factory_ownership_issues(config.initial_date)
    changes_before = store.latest_change_id()
    today = date.today().isoformat()
    cached_aimes_source_rows = load_aimes_order_cache(config)
    cached_aimes_rows, _cached_aimes_warnings = _partition_aimes_rows(
        cached_aimes_source_rows,
        store.ignored_aimes_keys(),
        store.aimes_assignments(),
    )
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
        aimes_warnings = []
    store.replace_aimes_review_rows([])
    finish_phase("load_aimes_and_local_state")

    snapshot_data = None
    if selected_folder is None and selected_folders is None:
        snapshot_data = _load_server_scan_snapshot(config, server_snapshot_path)
    server_snapshot_entries: dict[str, dict] | None = None
    server_snapshot_reused = snapshot_data is not None
    if snapshot_data is not None:
        root, server_folders, server_snapshot_entries = snapshot_data
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
            manual_folder = not (standard_folder or mixed_folder)
            folder_metadata = (
                server_snapshot_entries.get(str(folder))
                if server_snapshot_entries is not None
                else None
            )
            if manual_folder and process_temporary:
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
                        # A standard or mixed Server folder is authoritative
                        # evidence that a previously temporary-looking order
                        # is now a normal owned/cut-to-size order.
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
                # The lightweight scan snapshot intentionally contains only
                # the XML change markers. Explicit preview/confirmation still
                # needs the current Excel reports, so discover those files
                # only after the user has selected the folder for processing.
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
                    # A changed workbook must not fall back to the previous
                    # identity if parsing it fails; unchanged workbooks may
                    # safely retain their cached identity for reuse.
                    store.connection.execute(
                        "update source_files set order_id = '', factory_order = '' where path = ?",
                        (str(path),),
                    )
                seen_source_paths.add(str(path))
                # Temporary/rework reports are actionable only through the
                # pending-center approval flow. Keep their metadata baseline,
                # but never parse or project business facts into the formal
                # order index during this sync.
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
                # Fittings are optional user input.  When the user chose not
                # to include hardware, do not parse or validate the report at
                # all.  A non-standard temporary folder is also parsed only
                # during the approved processing step, where its AIMES match
                # (or lack of one) selects strict versus unscoped rules.
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
                        # Room-level allocation is used to preserve factory
                        # ownership, but it must not bypass the order-level
                        # material workbook checks. In particular, a standard
                        # single-order folder with explicit room rows would
                        # otherwise go straight to _select_room_materials()
                        # and skip Color/Color Table validation entirely.
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
                        # resolve_inventory_items reads mapping rules through a
                        # separate SQLite connection. Commit the source-file
                        # metadata update before opening that reader.
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
                                "update orders set material_status = '板材 · 封边', updated_at = ? where order_id = ?",
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
                                "update orders set material_status='板材 · 封边', updated_at=? where order_id=?",
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
                    except Exception:
                        issue_key = f"report_error:{path}"
                        issue_message = _business_report_message("board", path)
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
                    # Keep the folder-derived order hint available to both
                    # the successful parser path and every error path.  A
                    # malformed Fittingslist must report its own file, not
                    # raise a secondary UnboundLocalError for order_hint.
                    order_hint = folder_order_ids[0] if len(folder_order_ids) == 1 else ""
                    try:
                        groups = parse_fittings_groups(path)
                        factory_orders = [factory_order for factory_order, _ in groups]
                        server_factory_orders.update(factory_order.upper() for factory_order in factory_orders)
                        selected_groups = [
                            (factory_order, items)
                            for factory_order, items in groups
                            if (
                                selected_fittings.get(factory_order.upper()) is not None
                                and selected_fittings[factory_order.upper()].path.resolve() == path.resolve()
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
                                store.commit()
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
                                # Replace this source only after parsing and
                                # resolving every selected item successfully.
                                # Unchanged reports take the cached branch
                                # above and therefore retain their facts; a
                                # mapping failure must also retain the prior
                                # valid projection instead of deleting it.
                                store.connection.execute(
                                    "delete from hardware_items where source_type='aicnc' and source_path=?",
                                    (str(path),),
                                )
                                accepted_index = 0
                                for factory_order, items in selected_groups:
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
                                    for item in items:
                                        accepted = resolution.get("accepted", [])[accepted_index] if accepted_index < len(resolution.get("accepted", [])) else {}
                                        accepted_index += 1
                                        if ignored_hardware_reason(mappings, item.name, item.code) is not None:
                                            continue
                                        product_code = resolved_product_code(resolution, accepted_index - 1, item.code)
                                        store.connection.execute(
                                            """insert into hardware_items(
                                                order_id,factory_order,scope,product_code,source_code,name,spec,quantity,unit,
                                                source_type,source_path,remarks,updated_at
                                            ) values(?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                                            (hardware_order_id, factory_order.upper(), "factory_order", product_code, item.code, item.name,
                                             item.size, float(item.quantity), item.unit, "aicnc", str(path), "", server_seen),
                                        )
                                resolved_mapping_order_ids.add(order_hint.upper())
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
                    except Exception:
                        if _fittings_report_is_empty(path):
                            store.add_change(
                                severity="info",
                                kind="report_empty",
                                order_id=order_hint,
                                message=f"五金报表 {path.name} 没有内容，已按无五金处理",
                                path=str(path),
                            )
                        else:
                            issue_key = f"report_error:{path}"
                            issue_message = _business_report_message("fittings", path)
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
                # An order-level material source can change independently of
                # a factory-scoped hardware shipment.  Do not reopen that
                # factory's shipped status when its hardware document is
                # still confirmed locally.
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
            if kind == "material":
                _delete_server_material_source_facts(store, old_path)
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
    # A manually selected Server folder is an explicit request to recheck the
    # contained order.  Do not let the candidate-resolution phase's temporary
    # ``Server`` identity prevent that order from entering validation; doing
    # so would leave the previous validation_status/validation_message in the
    # preview database and make a repaired report look broken forever.
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
    artifact_refreshed = _refresh_cached_optimization_artifacts(store, all_validation_rows)
    finish_phase("optimization_artifact_check")

    # Validate the current source against each logical order. A successful
    # preview is the existing, auditable material/factory evidence for the
    # dashboard's “已优化” count; it is not a claim about CNC production.
    # ``preview_order`` also persists its normalized facts. Commit the report
    # parsing transaction first so its separate SQLite connection cannot be
    # blocked by this index connection's pending writes.
    store.commit()
    store.close()
    store = OrderIndexStore(config.workflow_database, connection=config.workflow_connection)
    for order in validation_rows:
        order_id, source_folder = order
        try:
            # Validation must not overwrite the source-scoped Server facts
            # just parsed above.  ``preview_order`` historically persisted
            # the root material workbook and would erase recut increments
            # before the confirmation payload was built.
            preview = preview_order(
                config, Path(source_folder), order_id, persist_facts=False
            )
            factory_ids = {factory.factory_order for factory in preview.factories}
            if not factory_ids:
                # CUT TO SIZE previews intentionally omit hardware/factory
                # blocks. A successful board/material preview still proves
                # the indexed factory orders for that order are optimized.
                factory_ids = {
                    row[0]
                    for row in store.connection.execute(
                        "select factory_order from factory_orders where order_id = ? and aimes_status = 'active' and ownership_status = '已确认'",
                        (order_id,),
                    ).fetchall()
                }
            store.connection.execute(
                "update orders set validation_status = ?, validation_message = '', material_status = ?, updated_at = ? where order_id = ?",
                ("正常", "板材 · 封边", _now(), order_id),
            )
            for factory_order in factory_ids:
                store.connection.execute(
                    "update factory_orders set report_state = '已发现', updated_at = ? where factory_order = ? and order_id = ?",
                    (_now(), factory_order, order_id),
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
                # Some CUT TO SIZE exports contain only the production reports
                # and CNC nesting output, without a generated material workbook.
                # The optimization artifact is sufficient for the optimization
                # column; keep material validation visibly pending.
                store.connection.execute(
                    "update orders set validation_status = ?, validation_message = ?, material_status = ?, updated_at = ? where order_id = ?",
                    (
                        "待校验",
                        f"已发现优化产物：{optimization_outputs[0].name}；material 尚未生成，材料数据仍待校验",
                        "待校验",
                        _now(),
                        order_id,
                    ),
                )
                continue
            store.connection.execute(
                "update orders set validation_status = ?, validation_message = ?, material_status = ?, updated_at = ? where order_id = ?",
                ("数据异常", validation_message, "待校验", _now(), order_id),
            )
            store.add_change(
                severity="warning",
                kind="order_validation",
                order_id=order_id,
                message=f"订单校验未完成：{validation_message}",
                path=source_folder,
            )
            issue_key = f"order_validation:{order_id}"
            current_issue_keys.add(issue_key)
            store.upsert_active_issue(
                issue_key=issue_key,
                kind="order_validation",
                order_id=order_id,
                path=source_folder,
                message=f"订单校验未完成：{validation_message}",
                seen_at=server_seen,
            )
        store.commit()

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
                server_folders,
                _server_scan_xml_entries(server_folders),
                observed_at=server_seen,
            )
        except OSError:
            # The business sync can still complete when a network folder
            # disappears during this optional scan-baseline refresh.
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
        reconcile_outbound_statuses(config, store)
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
    """Parse one user-selected Server folder using the normal index update path."""
    # Validate before opening/updating the index.  This command is the explicit
    # folder picker flow, so an invalid selection must be a fatal user-facing
    # error rather than an ordinary sync warning that looks successful in the UI.
    _server_folders_for_sync(config, folder)
    return sync_order_index(
        config,
        selected_folder=folder,
        process_temporary=process_temporary,
        include_hardware=include_hardware,
    )


def _server_preview_directory(config: Config) -> Path:
    directory = config.state_dir / "server-previews"
    directory.mkdir(parents=True, exist_ok=True)
    return directory


def _server_preview_path(config: Config, token: str) -> Path:
    token = str(token or "").strip()
    if not re.fullmatch(r"[0-9a-f]{32}", token):
        raise ValueError("Server 预览标识无效，请重新扫描")
    path = _server_preview_directory(config) / token / "workflow.sqlite3"
    if not path.is_file():
        raise ValueError("Server 预览已失效，请重新扫描")
    return path


def _clone_workflow_database(config: Config, destination: Path) -> None:
    """Clone the production index without copying its WAL files by hand."""
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
    rows = store.connection.execute(
        """
        select order_id, allocated_quantity, material_type, color,
               thickness, unit, edge
        from server_material_allocations
        where source_path = ?
        order by order_id
        """,
        (source_path,),
    ).fetchall()
    return [
        {
            "order_id": str(row[0]).upper(),
            "quantity": float(row[1] or 0),
        }
        for row in rows
        if _server_material_identity_key(
            source_path, row[2], row[3], row[4], row[5], row[6]
        ) == material_key
    ]


def _server_material_identity_key(
    source_path: str,
    material_type: str,
    color: str,
    thickness: str,
    unit: str,
    edge: str,
) -> str:
    """Return a stable identity for one parsed Server material fact.

    ``material_items.id`` is an SQLite row id and changes whenever a source
    workbook is refreshed.  Allocation records must therefore use the source
    path and normalized material fields instead of that transient id.
    """
    values = [
        str(value or "").strip().casefold()
        for value in (source_path, material_type, color, thickness, unit, edge)
    ]
    return "v2:" + hashlib.sha256("\x1f".join(values).encode()).hexdigest()


def _server_material_preview_row(store: OrderIndexStore, row: tuple) -> dict:
    (
        material_id,
        provisional_order_id,
        material_type,
        color,
        thickness,
        quantity,
        unit,
        edge,
        source_path,
        source_fingerprint,
    ) = row
    source_quantity = float(quantity or 0)
    material_key = _server_material_identity_key(
        str(source_path or ""), material_type, color, thickness, unit, edge
    )
    allocations = _server_material_allocation_rows(store, str(source_path or ""), material_key)
    allocated_quantity = sum(item["quantity"] for item in allocations)
    return {
        "material_id": int(material_id),
        "source_order_id": str(provisional_order_id or "").upper(),
        "material_type": str(material_type or ""),
        "color": str(color or ""),
        "thickness": str(thickness or ""),
        "quantity": source_quantity,
        "source_quantity": source_quantity,
        "allocated_quantity": allocated_quantity,
        "remaining_quantity": max(0.0, source_quantity - allocated_quantity),
        "unit": str(unit or ""),
        "edge": str(edge or ""),
        "source_path": str(source_path or ""),
        "source_fingerprint": str(source_fingerprint or ""),
        "allocations": allocations,
    }


def _server_material_source_rows(
    store: OrderIndexStore | sqlite3.Connection,
    folder_paths: list[str],
) -> list[tuple]:
    connection = store.connection if isinstance(store, OrderIndexStore) else store
    rows = connection.execute(
        """
        select id, order_id, material_type, color, thickness, quantity,
               unit, edge, source_path, source_fingerprint
        from material_items
        where source_type = 'aihouse'
        order by source_path, id
        """
    ).fetchall()
    return [row for row in rows if _path_in_folders(str(row[8] or ""), folder_paths)]


def _server_material_sort_key(item: dict) -> tuple:
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
    return tuple(str(value or "").strip().casefold() for value in values)


def _sqlite_table_exists(connection: sqlite3.Connection, table_name: str) -> bool:
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
    """Compare order-level material facts, aggregating duplicate source rows."""
    def grouped(connection: sqlite3.Connection, source_paths: list[str]) -> dict[tuple[str, ...], dict]:
        if not _sqlite_table_exists(connection, "material_items"):
            return {}
        params: list[object] = [order_id]
        path_clause = ""
        if source_paths:
            path_clause = " and source_path in (" + ",".join("?" for _ in source_paths) + ")"
            params.extend(source_paths)
        rows = connection.execute(
            f"""select material_type, color, thickness, unit, edge, sum(quantity)
                from material_items
                where order_id=? and source_type='aihouse'{path_clause}
                group by material_type, color, thickness, unit, edge""",
            params,
        ).fetchall()
        return {
            _server_change_key(row[0], row[1], row[2], row[3], row[4]): {
                "material_type": str(row[0] or ""),
                "color": str(row[1] or ""),
                "thickness": str(row[2] or ""),
                "unit": str(row[3] or ""),
                "edge": str(row[4] or ""),
                "quantity": float(row[5] or 0),
            }
            for row in rows
        }

    preview_rows = _server_material_source_rows(preview, folder_paths)
    source_paths = sorted({str(row[8] or "") for row in preview_rows if str(row[8] or "")})
    current_rows = grouped(current, source_paths)
    preview_values: dict[tuple[str, ...], dict] = {}
    for row in preview_rows:
        if str(row[1] or "").strip().upper() != order_id:
            continue
        key = _server_change_key(row[2], row[3], row[4], row[6], row[7])
        item = preview_values.setdefault(key, {
            "material_type": str(row[2] or ""), "color": str(row[3] or ""),
            "thickness": str(row[4] or ""), "unit": str(row[6] or ""),
            "edge": str(row[7] or ""), "quantity": 0.0,
        })
        item["quantity"] += float(row[5] or 0)
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
    def grouped(connection: sqlite3.Connection) -> dict[tuple[str, ...], dict]:
        if not _sqlite_table_exists(connection, "hardware_items"):
            return {}
        rows = connection.execute(
            """select product_code, name, spec, unit, sum(quantity)
               from hardware_items where factory_order=? and active=1
               group by product_code, name, spec, unit""",
            (factory_order,),
        ).fetchall()
        grouped_rows: dict[tuple[str, ...], dict] = {}
        for row in rows:
            # SKU is the stable business identity.  Source labels such as
            # ``Hinge`` and ``TestFullHinge`` may vary between exports, while
            # report specs and units may be absent or localized (``pcs`` vs
            # ``Piece``); comparing those presentation fields creates false
            # delete/add pairs in the preview.
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
) -> list[dict]:
    """Rebuild preview hardware with the current SKU rules.

    Server confirmation is allowed to resolve a hardware mapping after the
    read-only preview was opened.  The preview database is therefore rebuilt
    from the source Fittingslist files immediately before payload generation
    and again immediately before the final write.  Production facts remain
    untouched until the user confirms the combined write.
    """
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
        paths = sorted(_selected_hardware_report_paths(scoped_rows))
        selected_factory_orders: set[str] = set()
        for path in paths:
            try:
                groups = parse_fittings_groups(Path(path))
            except Exception:
                continue
            for factory_order, _ in groups:
                normalized_factory = str(factory_order).strip().upper()
                owner = preview.connection.execute(
                    "select order_id from factory_orders where factory_order=?",
                    (normalized_factory,),
                ).fetchone()
                if owner is not None and str(owner[0] or "").strip().upper() in skipped_orders:
                    continue
                selected_factory_orders.add(normalized_factory)
        if selected_factory_orders:
            placeholders = ",".join("?" for _ in selected_factory_orders)
            preview.connection.execute(
                f"delete from hardware_items where source_type='aicnc' and factory_order in ({placeholders})",
                tuple(sorted(selected_factory_orders)),
            )
        for path in paths:
            try:
                groups = parse_fittings_groups(Path(path))
            except Exception:
                # The regular Server parser already records malformed report
                # issues.  This helper only owns SKU resolution.
                continue

            group_rows = []
            file_missing: list[dict] = []
            for factory_order, items in groups:
                factory = preview.connection.execute(
                    """select order_id, outbound_status from factory_orders
                       where factory_order=? and aimes_status='active'""",
                    (str(factory_order).strip().upper(),),
                ).fetchone()
                if factory is None or str(factory[1] or "") == "已出库":
                    continue
                order_id = str(factory[0] or "").strip().upper()
                if order_id in skipped_orders:
                    # The user selected the decision at order level for a
                    # cut-to-size order.  Do not require SKU resolution for
                    # this order, and do not rebuild its preview hardware.
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

            # Do not leave a partially rebuilt Fittingslist in the preview.
            # The whole source file is blocked until every item is mapped or
            # explicitly ignored.
            if file_missing:
                continue
            preview.connection.execute(
                "delete from hardware_items where source_type='aicnc' and source_path=?",
                (path,),
            )
            for factory_order, order_id, items, resolution in group_rows:
                if resolution is None:
                    continue
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
                    product_code = resolved_product_code(resolution, index, str(item.code or ""))
                    preview.connection.execute(
                        """insert into hardware_items(
                            order_id, factory_order, scope, product_code, source_code, name, spec,
                            quantity, unit, source_type, source_path, active, updated_at
                        ) values(?,?,?,?,?,?,?,?,?,?,?,1,?)""",
                        (
                            order_id,
                            factory_order,
                            "factory_order",
                            product_code,
                            str(item.code or ""),
                            str(item.name or ""),
                            str(item.size or ""),
                            float(item.quantity or 0),
                            str(item.unit or ""),
                            "aicnc",
                            path,
                            _now(),
                        ),
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
    owns_store = preview_store is None
    store = preview_store or OrderIndexStore(preview_path)
    current = sqlite3.connect(config.workflow_database)
    from .inventory import InventoryMappings
    display_mappings = InventoryMappings(config.workflow_database, connection=current)
    folder_paths = [str(folder) for folder in folders]
    order_ids: set[str] = set()
    source_rows = store.connection.execute(
        "select path, source_folder, kind, order_id, factory_order, batch_number from source_files"
    ).fetchall()
    for path, source_folder, kind, order_id, factory_order, batch_number in source_rows:
        if not _path_in_folders(str(source_folder), folder_paths):
            continue
        order_ids.update(
            value.strip().upper()
            for value in str(order_id or "").split("、")
            if value.strip()
        )

    material_source_rows = _server_material_source_rows(store, folder_paths)
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
               has_hardware, optimized, outbound_status, outbound_document,
               production_batch_id
        from factory_orders
        where order_id <> ''
        order by order_id, factory_order
        """
    ).fetchall()
    factories_by_order: dict[str, list[dict]] = defaultdict(list)
    selected_factories: set[str] = set()
    for row in factory_rows:
        factory_order, order_id = str(row[0]), str(row[1]).upper()
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
                    select product_code, name, spec, quantity, unit, source_path
                    from hardware_items
                    where factory_order = ?
                    order by id
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
            "production_batch_id": row[13],
            "hardware": hardware,
        })

    orders = []
    for order_id in sorted(order_ids):
        row = store.connection.execute(
            "select order_id, order_type, source_folder, validation_status, validation_message, material_status from orders where order_id = ?",
            (order_id,),
        ).fetchone()
        if row is None:
            continue
        source_paths = sorted({
            str(path)
            for path, source_folder, kind, source_order_id, factory_order, batch_number in source_rows
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
                              report_state, ownership_status, has_hardware, optimized,
                              outbound_status, outbound_document
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
        "batch_evidence": table_records(
            "batch_evidence",
            "factory_order in ({})".format(",".join("?" for _ in selected_factory_orders))
            if selected_factory_orders else "0",
            tuple(selected_factory_orders),
        ),
        "production_batches": table_records(
            "production_batches",
            "batch_number in (select batch_number from batch_evidence where factory_order in ({}))".format(
                ",".join("?" for _ in selected_factory_orders)
            ) if selected_factory_orders else "0",
            tuple(selected_factory_orders),
        ),
        "server_material_allocations": table_records(
            "server_material_allocations",
            "source_path in ({})".format(",".join("?" for _ in selected_source_paths))
            if selected_source_paths else "0",
            tuple(selected_source_paths),
        ),
    }
    current.close()
    if owns_store:
        store.close()
    result = {
        "created_at": _now(),
        "include_hardware": include_hardware,
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
    """Return whether a Server preview contains a real business delta."""
    if "has_business_changes" in payload:
        return bool(payload.get("has_business_changes"))
    return any(
        bool(order.get("material_changes"))
        or bool(order.get("factories"))
        or bool(order.get("hardware_changes"))
        for order in payload.get("orders", [])
        if isinstance(order, dict)
    )


def _server_preview_hardware_source_items(
    preview_store: OrderIndexStore,
    folder_paths: list[str],
) -> list[dict]:
    """Capture parsed Fittingslist facts for later in-memory SKU resolution."""
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
    selected_paths = _selected_hardware_report_paths(scoped_rows)
    result: list[dict] = []
    for path, source_folder in scoped_rows:
        path = str(path or "")
        if not path or path not in selected_paths:
            continue
        try:
            groups = parse_fittings_groups(Path(path))
        except Exception:
            continue
        for factory_order, items in groups:
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


def preview_server_changes(
    config: Config,
    selected_folders: list[Path],
    *,
    include_hardware: bool = True,
) -> dict:
    """Parse selected Server folders into a process-local preview.

    The preview database is an in-memory working connection backed by the
    local production database. Nothing is written under ``state_dir`` and no
    token is returned. The caller must retain the returned payload until the
    user confirms it.
    """
    if not selected_folders:
        raise ValueError("请先选择要预览的 Server 文件夹")
    timing_started = time.perf_counter()
    stage_started = timing_started
    timing_stages: list[dict[str, object]] = []

    def finish_timing_stage(stage: str, label: str) -> None:
        nonlocal stage_started
        now = time.perf_counter()
        timing_stages.append({
            "stage": stage,
            "label": label,
            "duration_seconds": round(now - stage_started, 6),
        })
        stage_started = now

    normalized_folders = [folder.expanduser().resolve() for folder in selected_folders]
    _server_folders_for_sync(config, None, selected_folders=normalized_folders)
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
        # Product mappings and the order index share the central SQLite file;
        # create the shadow product tables before opening OrderIndexStore so
        # the preview never tries to migrate the same file while it is locked.
        from .inventory import bootstrap_product_database
        bootstrap_product_database(stage_config)
        finish_timing_stage("preview_database", "复制中央数据库到内存预览")
        # The preview intentionally never runs temporary-order outbound or
        # traveler generation. Those are separate user-approved operations.
        sync_order_index(
            stage_config,
            selected_folders=normalized_folders,
            process_temporary=False,
            include_hardware=include_hardware,
            full_refresh=False,
            validate_selected_orders=True,
            refresh_outbound_statuses=False,
            reconcile_outbound=False,
        )
        finish_timing_stage("server_parse", "读取、解析并校验 Server 文件")
        material_issues = preview_store.connection.execute(
            "select path, message from active_issues where kind = 'material_validation' and status = 'open' order by path"
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
                    f"材料文件尚未通过校验：{summary}。请手工修正 Room/section 后重新扫描 Server",
                    issues=issue_details,
                )
        preview_store.connection.executemany(
            "insert or replace into server_material_preview_scopes(source_folder) values(?)",
            [(str(folder),) for folder in normalized_folders],
        )
        preview_store.commit()
        payload = _server_preview_payload(
            config, None, "", normalized_folders, include_hardware,
            preview_store=preview_store,
        )
        payload["hardware_mapping_requirements"] = (
            _refresh_server_preview_hardware(
                config, None, [str(folder) for folder in normalized_folders],
                preview_store=preview_store,
            )
            if include_hardware else []
        )
        # Hardware rows are rebuilt after the mapping check, so regenerate the
        # diff payload once more to include the resolved factory-order facts.
        payload = _server_preview_payload(
            config, None, "", normalized_folders, include_hardware,
            preview_store=preview_store,
        ) | {
            "validation_recomputed": True,
            "hardware_mapping_requirements": payload["hardware_mapping_requirements"],
            "hardware_source_items": _server_preview_hardware_source_items(
                preview_store, [str(folder) for folder in normalized_folders]
            ) if include_hardware else [],
        }
        if not payload["orders"]:
            raise ValueError("Server 文件夹中没有解析出可确认的订单和工厂单")
        finish_timing_stage("preview_build", "生成材料、五金和写入差异预览")
        return {
            "server_write_preview": payload,
            "operation_timing": {
                "total_seconds": round(time.perf_counter() - timing_started, 6),
                "stages": timing_stages,
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
    """Record one order-level material allocation in the shadow database."""
    preview_path = _server_preview_path(config, token)
    order_id = str(order_id or "").strip().upper()
    try:
        quantity = float(quantity)
    except (TypeError, ValueError) as exc:
        raise ValueError("分配数量必须是数字") from exc
    if not order_id:
        raise ValueError("材料分配需要目标订单号")
    if quantity <= MATERIAL_ALLOCATION_EPSILON:
        raise ValueError("分配数量必须大于 0")
    preview = OrderIndexStore(preview_path)
    try:
        if preview.connection.execute(
            "select 1 from orders where order_id = ?", (order_id,)
        ).fetchone() is None:
            raise ValueError("所选订单不在本次 Server 预览中")
        row = preview.connection.execute(
            """
            select id, order_id, material_type, color, thickness, quantity,
                   unit, edge, source_path, source_fingerprint
            from material_items
            where id = ? and source_type = 'aihouse'
            """,
            (int(material_id),),
        ).fetchone()
        if row is None:
            raise ValueError("所选材料明细不在本次 Server 预览中")
        source_quantity = float(row[5] or 0)
        source_path = str(row[8] or "")
        material_key = _server_material_identity_key(
            source_path, row[2], row[3], row[4], row[6], row[7]
        )
        allocation_rows = preview.connection.execute(
            """
            select id, order_id, allocated_quantity, material_type, color,
                   thickness, unit, edge
            from server_material_allocations
            where source_path = ?
            """,
            (source_path,),
        ).fetchall()
        matching_allocations = [
            item for item in allocation_rows
            if _server_material_identity_key(
                source_path, item[3], item[4], item[5], item[6], item[7]
            ) == material_key
        ]
        allocated = sum(float(item[2] or 0) for item in matching_allocations)
        remaining = source_quantity - float(allocated or 0)
        if quantity - remaining > MATERIAL_ALLOCATION_EPSILON:
            raise ValueError(
                f"分配数量超过剩余数量：剩余 {remaining:g} {row[6] or ''}，本次 {quantity:g}"
            )
        now = _now()
        existing = next(
            (item for item in matching_allocations if str(item[1]).upper() == order_id),
            None,
        )
        source_key = material_key
        if existing is None:
            preview.connection.execute(
                """
                insert into server_material_allocations(
                    source_material_id, source_path, source_material_key,
                    material_type, color, thickness, unit, edge,
                    source_quantity, order_id, allocated_quantity,
                    source_fingerprint, created_at, updated_at
                ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                """,
                (
                    int(material_id), source_path, source_key,
                    str(row[2] or ""), str(row[3] or ""), str(row[4] or ""),
                    str(row[6] or ""), str(row[7] or ""), source_quantity,
                    order_id, quantity, str(row[9] or ""), now, now,
                ),
            )
        else:
            preview.connection.execute(
                """
                update server_material_allocations
                set allocated_quantity = ?, updated_at = ?
                where id = ?
                """,
                (float(existing[1]) + quantity, now, int(existing[0])),
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
    selected: set[tuple[str, str]] = set()
    wanted_order = str(order_id or "").strip().upper()
    wanted_factory = str(factory_order or "").strip().upper()
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
    # A factory with a new fittings source must remain selectable even when
    # its identity fields are otherwise unchanged and therefore omitted from
    # the visual "factory changes" list. This also keeps mapping validation
    # from being bypassed when optimization state is derived only from AICNC
    # evidence rather than a successful report preview.
    for group in payload.get("hardware_source_items", []):
        if not isinstance(group, dict):
            continue
        current_order = str(group.get("order_id", "")).strip().upper()
        current_factory = str(group.get("factory_order", "")).strip().upper()
        if wanted_order and current_order != wanted_order:
            continue
        if current_factory and current_order and (not wanted_factory or current_factory == wanted_factory):
            selected.add((current_factory, current_order))
    return sorted(selected)


def _server_preview_order_validation_errors(
    orders: Iterable[dict],
    selected_order_ids: set[str] | None = None,
    *,
    require_recomputed: bool = False,
) -> list[str]:
    """Return validation failures that must block a Server confirmation."""
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
        # Older token-based material-allocation previews did not run the
        # selected-order validation pass and therefore carry the schema
        # default ``待同步`` without an error message. Preserve that legacy
        # contract; the in-memory Server folder flow sets
        # ``require_recomputed`` and rejects it instead.
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
    target_columns = {
        str(row[1]) for row in connection.execute(f"pragma table_info({table})").fetchall()
    }
    for row in rows:
        values = {key: value for key, value in row.items() if key in target_columns}
        if table in {"material_items", "hardware_items", "batch_evidence", "server_material_allocations"}:
            values.pop("id", None)
        if not values:
            continue
        columns = list(values)
        placeholders = ",".join("?" for _ in columns)
        connection.execute(
            f"insert or replace into {table}({','.join(columns)}) values({placeholders})",
            tuple(values[column] for column in columns),
        )


def _materialize_memory_hardware(
    config: Config,
    payload: dict,
    records: dict[str, list[dict]],
    selected_factory_ids: set[str],
    skipped_orders: set[str],
) -> None:
    """Resolve mappings from captured fittings facts without reopening Server."""
    from .inventory import TravelerItem, resolve_inventory_items, resolved_product_code

    existing = [
        row for row in records.get("hardware_items", [])
        if str(row.get("factory_order", "")).strip().upper() not in selected_factory_ids
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
            resolved_rows.append({
                "order_id": order_id,
                "factory_order": factory_order,
                "scope": "factory_order",
                "product_code": resolved_product_code(resolution, index, str(item.get("code", ""))),
                "source_code": str(item.get("code", "")),
                "name": str(item.get("name", "")),
                "spec": str(item.get("spec", "")),
                "quantity": float(item.get("quantity", 0) or 0),
                "unit": str(item.get("unit", "")),
                "source_type": "aicnc",
                "source_path": str(group.get("source_path", "")),
                "active": 1,
                "remarks": "",
                "updated_at": _now(),
            })
    records["hardware_items"] = resolved_rows


def _confirm_memory_preview(
    config: Config,
    payload: dict,
    *,
    order_id: str = "",
    factory_order: str = "",
    skip_hardware_order_ids: Iterable[str] = (),
    confirm_write: bool = False,
) -> dict:
    """Commit only the JSON preview retained by the App.

    This function deliberately has no Server path or fingerprint input.  The
    preview is the authority for this confirmation transaction; the local
    database is only the destination and post-write verification source.
    """
    if not confirm_write:
        raise RuleError("write_confirmation_required", "写入 Server 事实需要用户明确确认")
    timing_started = time.perf_counter()
    records = _memory_preview_records(payload)
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

    validation_finished = time.perf_counter()

    if (
        not _server_preview_has_business_changes(payload)
        and not payload.get("hardware_mapping_requirements")
    ):
        baseline_folders = [
            Path(str(folder))
            for folder in payload.get("source_folders", [])
            if str(folder).strip()
        ]
        baseline_entries = _server_scan_xml_entries(baseline_folders)
        production = OrderIndexStore(config.workflow_database)
        try:
            production.save_server_scan_xml_baseline(
                baseline_folders,
                baseline_entries,
                observed_at=_now(),
            )
            production.commit()
        finally:
            production.close()
        finished = time.perf_counter()
        return {
            "server_write_confirmed": True,
            "server_write_skipped": True,
            "server_write_skip_reason": "板材、五金和工厂单信息没有实际变化，仅更新 Server XML 扫描基线",
            "server_material_write_confirmed": False,
            "server_factory_hardware_write_confirmed": False,
            "orders": sorted(selected_order_ids),
            "factory_orders": sorted(selected_factory_ids),
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
    if not order_rows and not factory_rows and not material_rows:
        raise ValueError("本次预览没有可写入的订单、材料或工厂单")

    production = OrderIndexStore(config.workflow_database)
    try:
        production.connection.execute("begin")
        _insert_memory_records(production.connection, "orders", order_rows)

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
        _insert_memory_records(production.connection, "material_items", material_rows)

        for row in factory_rows:
            current_factory = str(row.get("factory_order", "")).strip().upper()
            current_order = str(row.get("order_id", "")).strip().upper()
            _insert_memory_records(production.connection, "factory_orders", [row])
            if current_order in skipped_orders:
                continue
            production.connection.execute(
                "delete from hardware_items where factory_order=?",
                (current_factory,),
            )
            _insert_memory_records(
                production.connection,
                "hardware_items",
                [item for item in hardware_rows if str(item.get("factory_order", "")).strip().upper() == current_factory],
            )

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

        selected_batches = [
            row for row in records.get("batch_evidence", [])
            if str(row.get("factory_order", "")).strip().upper() in selected_factory_ids
        ]
        _insert_memory_records(production.connection, "batch_evidence", selected_batches)
        batch_numbers = {str(row.get("batch_number", "")) for row in selected_batches}
        _insert_memory_records(
            production.connection,
            "production_batches",
            [row for row in records.get("production_batches", []) if str(row.get("batch_number", "")) in batch_numbers],
        )
        baseline_folders = [
            Path(str(folder))
            for folder in payload.get("source_folders", [])
            if str(folder).strip()
        ]
        production.save_server_scan_xml_baseline(
            baseline_folders,
            _server_scan_xml_entries(baseline_folders),
            observed_at=_now(),
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
    """Write balanced order-level material allocations to production."""
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
        allocations_by_material: dict[str, list[tuple]] = defaultdict(list)
        for row in preview.connection.execute(
            """
            select id, source_path, order_id, allocated_quantity,
                   material_type, color, thickness, unit, edge
            from server_material_allocations
            order by source_path, order_id, id
            """
        ).fetchall():
            allocation_key = _server_material_identity_key(
                row[1], row[4], row[5], row[6], row[7], row[8]
            )
            allocations_by_material[allocation_key].append(
                (int(row[0]), str(row[2]).upper(), float(row[3] or 0))
            )
        # Material room ownership is already explicit in the Server workbook
        # and is persisted as source_order_id during the read-only preview.
        # Default unallocated quantity to that source order so confirmation
        # never asks the user to select a factory order for order-level
        # material facts. Existing manual splits remain untouched.
        for row in material_rows:
            source_order_id = str(row[1] or "").strip().upper()
            source_quantity = float(row[5] or 0)
            source_path = str(row[8] or "")
            source_key = _server_material_identity_key(
                source_path, row[2], row[3], row[4], row[6], row[7]
            )
            material_allocations = allocations_by_material[source_key]
            allocated_quantity = sum(
                float(item[2] or 0) for item in material_allocations
            )
            remaining = source_quantity - allocated_quantity
            if remaining <= MATERIAL_ALLOCATION_EPSILON:
                continue
            if not source_order_id:
                raise ValueError(
                    f"材料 {row[3] or row[2] or '未命名'} 没有明确订单归属，不能自动确认"
                )
            now = _now()
            existing_index = next(
                (
                    index for index, item in enumerate(material_allocations)
                    if item[1] == source_order_id
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
                        source_material_id, source_path, source_material_key,
                        material_type, color, thickness, unit, edge,
                        source_quantity, order_id, allocated_quantity,
                        source_fingerprint, created_at, updated_at
                    ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    """,
                    (
                        int(row[0]), source_path, source_key,
                        str(row[2] or ""), str(row[3] or ""), str(row[4] or ""),
                        str(row[6] or ""), str(row[7] or ""), source_quantity,
                        source_order_id, remaining, str(row[9] or ""), now, now,
                    ),
                )
                material_allocations.append(
                    (int(cursor.lastrowid), source_order_id, remaining)
                )
            else:
                preview.connection.execute(
                    """
                    update server_material_allocations
                    set allocated_quantity = allocated_quantity + ?, updated_at = ?
                    where id = ?
                    """,
                    (remaining, now, int(existing[0])),
                )
                material_allocations[existing_index] = (
                    existing[0], existing[1], existing[2] + remaining
                )
        for row in material_rows:
            source_quantity = float(row[5] or 0)
            source_key = _server_material_identity_key(
                str(row[8] or ""), row[2], row[3], row[4], row[6], row[7]
            )
            allocated_quantity = sum(
                float(item[2] or 0) for item in allocations_by_material[source_key]
            )
            if abs(source_quantity - allocated_quantity) > MATERIAL_ALLOCATION_EPSILON:
                remaining = source_quantity - allocated_quantity
                raise ValueError(
                    f"材料尚未分配完成：{row[3] or row[2] or '未命名'}，"
                    f"还差 {remaining:g} {row[6] or ''}"
                )
        material_orders = {
            str(item[1]).upper()
            for values in allocations_by_material.values()
            for item in values
        }
        factory_orders = {order_id for _, order_id in actionable_factories}
        affected_orders = sorted(material_orders | factory_orders)
        if material_rows and not material_orders:
            raise ValueError("请先将板材和封边条分配到订单")
        source_paths = sorted({str(row[8] or "") for row in material_rows if row[8]})
        orders_by_source_path: dict[str, set[str]] = defaultdict(set)
        for row in material_rows:
            source_key = _server_material_identity_key(
                str(row[8] or ""), row[2], row[3], row[4], row[6], row[7]
            )
            for allocation in allocations_by_material[source_key]:
                orders_by_source_path[str(row[8] or "")].add(str(allocation[1]).upper())

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
                "order_id", "material_type", "color", "thickness", "quantity",
                "unit", "edge", "source_type", "source_path", "source_fingerprint", "updated_at",
            )
            material_sql = f"""
                insert into material_items({','.join(material_columns)})
                values({','.join('?' for _ in material_columns)})
                on conflict(order_id, material_type, color, thickness, unit, edge, source_type, source_path)
                do update set
                    quantity = material_items.quantity + excluded.quantity,
                    source_fingerprint = excluded.source_fingerprint,
                    updated_at = excluded.updated_at
            """
            now = _now()
            for row in material_rows:
                source_key = _server_material_identity_key(
                    str(row[8] or ""), row[2], row[3], row[4], row[6], row[7]
                )
                for allocation in allocations_by_material[source_key]:
                    production.connection.execute(
                        material_sql,
                        (
                            str(allocation[1]).upper(), str(row[2] or ""), str(row[3] or ""),
                            str(row[4] or ""), float(allocation[2] or 0), str(row[6] or ""),
                            str(row[7] or ""), "aihouse", str(row[8] or ""),
                            str(row[9] or ""), now,
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
            batch_tables = ("production_batches", "batch_evidence")
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
                if order_id in skipped_hardware_orders:
                    # The order-level choice means this Server confirmation
                    # must not change hardware facts for any factory order in
                    # the order.  The factory identity/material facts still
                    # commit in the same transaction.
                    continue
                production.connection.execute(
                    "delete from hardware_items where factory_order=?",
                    (factory_order,),
                )
                preview_hardware = preview.connection.execute(
                    "select * from hardware_items where factory_order=? and active=1 order by id",
                    (factory_order,),
                ).fetchall()
                if preview_hardware:
                    production.connection.executemany(
                        f"insert into hardware_items({','.join(hardware_columns)}) values({hardware_placeholders})",
                        [tuple(row) for row in preview_hardware],
                    )
                for table in batch_tables:
                    columns = [
                        item[1]
                        for item in preview.connection.execute(
                            f"pragma table_info({table})"
                        ).fetchall()
                    ]
                    if not columns:
                        continue
                    rows = preview.connection.execute(
                        f"select {','.join(columns)} from {table} "
                        + (
                            "where factory_order=?"
                            if table == "batch_evidence"
                            else "where batch_number in (select batch_number from batch_evidence where factory_order=?)"
                        ),
                        (factory_order,),
                    ).fetchall()
                    if rows:
                        placeholders = ",".join("?" for _ in columns)
                        production.connection.executemany(
                            f"insert or replace into {table}({','.join(columns)}) values({placeholders})",
                            [tuple(row) for row in rows],
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
            # A successful transaction is not enough for the UI to claim
            # completion. Read the committed rows back from the production
            # database and verify the exact source-path quantities.
            for order_id in affected_orders:
                expected = defaultdict(float)
                for row in material_rows:
                    source_key = _server_material_identity_key(
                        str(row[8] or ""), row[2], row[3], row[4], row[6], row[7]
                    )
                    for allocation in allocations_by_material[source_key]:
                        if str(allocation[1]).upper() != order_id:
                            continue
                        expected[
                            (
                                str(row[2] or ""), str(row[3] or ""),
                                str(row[4] or ""), str(row[6] or ""), str(row[7] or ""),
                            )
                        ] += float(allocation[2] or 0)
                actual = {
                    (
                        str(row[0] or ""), str(row[1] or ""),
                        str(row[2] or ""), str(row[3] or ""), str(row[4] or ""),
                    ): float(row[5] or 0)
                    for row in production.connection.execute(
                        """
                        select material_type, color, thickness, unit, edge,
                               sum(quantity)
                        from material_items
                        where order_id = ? and source_type = 'aihouse'
                          and source_path in ({})
                        group by material_type, color, thickness, unit, edge
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
                    "select count(*) from hardware_items where factory_order=? and active=1",
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
    """Confirm order materials and resolved factory-order hardware together."""
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
    """Merge only the selected order/factory evidence into production."""
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
        for table, predicate in (
            ("production_batches", "batch_number in (select batch_number from batch_evidence where factory_order = ?)"),
            ("batch_evidence", "factory_order = ?"),
        ):
            columns = [row[1] for row in preview.connection.execute(f"pragma table_info({table})").fetchall()]
            rows = preview.connection.execute(
                f"select {','.join(columns)} from {table} where {predicate}",
                (factory_order,),
            ).fetchall()
            if rows:
                production.connection.executemany(
                    f"insert or replace into {table}({','.join(columns)}) values({','.join('?' for _ in columns)})",
                    rows,
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


def process_server_changes(
    config: Config,
    selected_folders: list[Path] | None = None,
    *,
    include_hardware: bool = True,
) -> dict:
    """Process the changes explicitly approved in the Server prompt."""
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


def auto_resolve_current_issue(config: Config, issue_key: str) -> dict:
    store = OrderIndexStore(config.workflow_database)
    issue = store.current_issue(issue_key)
    if issue is None:
        store.close()
        raise ValueError("当前问题已解决或不存在，请刷新问题列表")
    if issue["kind"] != "factory_ownership":
        store.resolve_active_issue(issue_key)
        store.add_change(severity="info", kind="issue_resolved", message=f"已标记问题为已处理：{issue['message']}", path=issue["path"])
        store.commit()
        result = list_order_index(config)
        store.close()
        return result

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


def resolve_current_issue(config: Config, issue_key: str, order_id: str = "", factory_name: str = "") -> dict:
    store = OrderIndexStore(config.workflow_database)
    issue = store.current_issue(issue_key)
    if issue is None:
        store.close()
        raise ValueError("当前问题已解决或不存在，请刷新问题列表")
    if issue["kind"] == "factory_ownership":
        _confirm_current_factory_issue(store, issue, order_id, factory_name)
    else:
        store.resolve_active_issue(issue_key)
        store.add_change(severity="info", kind="issue_resolved", message=f"已标记问题为已处理：{issue['message']}", path=issue["path"])
    store.commit()
    result = list_order_index(config)
    store.close()
    return result


def list_order_index(config: Config) -> dict:
    store = OrderIndexStore(config.workflow_database)
    _reconcile_temporary_order_projections(store)
    if config.reconcile_outbound_on_read:
        reconcile_outbound_statuses(config, store)
    cached_source_rows = load_aimes_order_cache(config)
    _, aimes_warnings = _partition_aimes_rows(
        cached_source_rows,
        store.ignored_aimes_keys(),
        store.aimes_assignments(),
    )
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


def save_order_annotations(
    config: Config,
    order_id: str,
    *,
    user_note: str,
    planned_days: list[dict[str, str]],
    actual_days: list[dict[str, str]],
) -> dict:
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


def ignore_aimes_factories(config: Config, ignore_keys: list[str]) -> dict:
    store = OrderIndexStore(config.workflow_database)
    _, issues = _partition_aimes_rows(
        load_aimes_order_cache(config),
        store.ignored_aimes_keys(),
        store.aimes_assignments(),
    )
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
    store = OrderIndexStore(config.workflow_database)
    for key in ignore_keys:
        store.restore_aimes_factory(key)
    store.commit()
    store.close()
    return list_order_index(config)


def assign_aimes_factory_order(config: Config, ignore_key: str, order_id: str) -> dict:
    order_id = _valid_aimes_order_id(order_id)
    if not order_id:
        raise ValueError("手工确认的订单号不符合当前订单规则，请使用 PP 加 4 位数字或 CS 加 3 位数字")
    raw_rows = load_aimes_order_cache(config)
    raw = next((row for row in raw_rows if _aimes_ignore_key(row) == ignore_key), None)
    issue = _aimes_row_issue(raw or {})
    if issue is None:
        raise ValueError("所选 AIMES 工厂单已不需要人工处理，请刷新后重试")
    if not FACTORY_RE.fullmatch(issue["factory_order"]):
        raise ValueError("工厂单号不符合规则，无法自动归属")

    store = OrderIndexStore(config.workflow_database)
    if ignore_key in store.ignored_aimes_keys():
        store.close()
        raise ValueError("该工厂单已经被忽略，请先恢复后再处理")
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
    store = OrderIndexStore(config.workflow_database)
    if ignore_key not in store.aimes_assignments():
        store.close()
        raise ValueError("该工厂单没有已确认的建议归属")
    store.restore_aimes_assignment(ignore_key)
    store.commit()
    store.close()
    return list_order_index(config)


def add_manual_factory(config: Config, order_id: str, factory_order: str, factory_name: str) -> dict:
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
