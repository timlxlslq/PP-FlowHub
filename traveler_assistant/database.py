"""Central workflow database and safe migration helpers.

The application owns one local SQLite file for business data.  Source files
from AIHouse/AIMES/AICNC/Kingdee remain external; this module stores the
normalized facts, provenance and user corrections needed by the dashboard.
"""

from __future__ import annotations

import json
import hashlib
import re
import shutil
import sqlite3
from datetime import datetime
from pathlib import Path
from typing import Any


def enable_foreign_keys(connection: sqlite3.Connection) -> sqlite3.Connection:
    """Enable SQLite foreign-key enforcement before the first transaction.

    SQLite silently ignores ``pragma foreign_keys=on`` inside a transaction.
    Failing loudly here prevents a borrowed/shared connection from appearing
    protected when its caller opened a transaction too early.
    """
    enabled = int(connection.execute("pragma foreign_keys").fetchone()[0])
    if enabled:
        return connection
    if connection.in_transaction:
        raise RuntimeError("必须在事务开始前启用 SQLite foreign_keys")
    connection.execute("pragma foreign_keys=on")
    if int(connection.execute("pragma foreign_keys").fetchone()[0]) != 1:
        raise RuntimeError("无法启用 SQLite foreign_keys")
    return connection


def connect_database(path: Path, **kwargs: Any) -> sqlite3.Connection:
    """Open an application SQLite connection with foreign keys enforced."""
    return enable_foreign_keys(sqlite3.connect(path, **kwargs))


def database_path(state_dir: Path) -> Path:
    """Return the single central SQLite path for an application state dir."""
    return state_dir / "workflow.sqlite3"


def _now() -> str:
    return datetime.now().astimezone().isoformat(timespec="seconds")


_OUTBOUND_FACTORY_SPLIT_RE = re.compile(r"[,，;；、|]+")
_PRODUCT_KEY_RE = re.compile(r"[\s_-]+")
_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
_PLYWOOD_NOMINAL_THICKNESS = {
    "M0002": "5.4",
    "M0003": "14.5",
    "M0004": "18",
}
_SCHEMA_READY_MARKER = "ensure_schema_material_sku_v1"


def _product_key(value: object) -> str:
    return _PRODUCT_KEY_RE.sub("", str(value or "")).upper()


def catalog_material_attributes(
    category: object, name: object, spec: object, code: object = "",
) -> tuple[str, str, str]:
    """Derive catalog-owned workflow attributes without changing raw fields.

    The plywood aliases are explicit workflow nominal sizes.  They deliberately
    remain separate from a supplier specification such as 5.2 or 15 mm.
    """
    category_text = str(category or "").strip()
    name_text = str(name or "").strip()
    spec_text = str(spec or "").strip()
    category_key = _product_key(category_text)
    name_key = _product_key(name_text)
    if "EDGEBAND" in category_key or "封边" in category_key:
        kind = "edge"
    elif "PLYWOOD" in category_key or "夹板" in category_key or "PLYWOOD" in name_key:
        kind = "plywood"
    elif "PANEL" in category_key or "板材" in category_key:
        kind = "panel"
    else:
        return "", "", ""

    if kind == "plywood":
        thickness = _PLYWOOD_NOMINAL_THICKNESS.get(str(code or "").strip().upper(), "")
        if not thickness:
            numbers = _NUMBER_RE.findall(spec_text)
            thickness = f"{float(numbers[0]):g}" if numbers else ""
        return kind, "", thickness
    if kind == "panel":
        fractions = re.findall(r"(?<!\d)(\d+)\s*/\s*(\d+)(?!\d)", spec_text)
        if fractions:
            # Product specs write thickness first (for example ``3/4 Board``)
            # and may contain later width/length fractions such as 110-1/4.
            numerator, denominator = fractions[0]
            thickness = f"{round(float(numerator) / float(denominator) * 25.4, 1):g}"
        else:
            numbers = [float(value) for value in _NUMBER_RE.findall(spec_text)]
            plausible = [value for value in numbers if 0 < value <= 50]
            thickness = f"{plausible[-1]:g}" if plausible else ""
        return kind, name_text, thickness

    color = re.sub(r"^\s*edge\s*banding\s*[-:–—]*\s*", "", name_text, flags=re.I)
    color = re.sub(
        r"\s+(?:abs\s+)?(?:edge\s+)?banding(?:\s*\d+(?:\.\d+)?\s*mm)?\s*$",
        "", color, flags=re.I,
    ).strip()
    return kind, color or name_text, ""


def _legacy_material_name(material_type: object, color: object, thickness: object) -> str:
    kind = str(material_type or "").strip().casefold()
    color_text = str(color or "").strip()
    thickness_text = str(thickness or "").strip()
    if kind == "edge":
        return f"Edge banding--{color_text}"
    if kind == "plywood":
        return f"{float(thickness_text):g}mm--Plywood"
    return f"{float(thickness_text):g}mm--{color_text}"


def server_material_identity_key(source_path: object, product_code: object) -> str:
    """Return the stable v3 identity for one source material SKU."""
    payload = "\x1f".join((
        str(source_path or "").strip().casefold(),
        str(product_code or "").strip().upper(),
    ))
    return "v3:" + hashlib.sha256(payload.encode()).hexdigest()


def _has_product_foreign_key(connection: sqlite3.Connection, table: str) -> bool:
    return any(
        str(row[2]) == "products" and str(row[3]) == "product_code"
        and str(row[4]) == "code" and str(row[6]).upper() == "RESTRICT"
        for row in connection.execute(f"pragma foreign_key_list({table})").fetchall()
    )


def _resolve_legacy_material_code(
    connection: sqlite3.Connection,
    material_type: object,
    color: object,
    thickness: object,
) -> tuple[str, list[str]]:
    """Resolve one legacy material identity, returning candidates for diagnostics."""
    try:
        display_name = _legacy_material_name(material_type, color, thickness)
    except (TypeError, ValueError):
        return "", []

    # Reuse the runtime's authoritative material matcher.  The small adapter
    # keeps it on this migration transaction instead of opening a second,
    # potentially locked connection or maintaining a subtly different set of
    # plywood/panel/edge aliases here.
    from .core import RuleError
    from .inventory import InventoryMappings, Product, TravelerItem, match_item

    class _MigrationCatalog:
        @staticmethod
        def _product(row: tuple) -> Product:
            return Product(
                category=str(row[0] or ""), code=str(row[1] or ""),
                name=str(row[2] or ""), spec=str(row[3] or ""),
                status=str(row[4] or ""), brand=str(row[5] or ""),
                remark=str(row[6] or ""), unit=str(row[7] or ""),
                cost_price=None if row[8] is None else float(row[8]),
            )

        def require_code(self, code: str) -> Product:
            rows = connection.execute(
                """select category,code,name,spec,status,brand,remark,unit,cost_price
                   from products where normalized_code=?""",
                (_product_key(code),),
            ).fetchall()
            if len(rows) != 1:
                raise RuleError("product_conflict", f"商品编号 {code} 匹配到 {len(rows)} 条记录")
            product = self._product(rows[0])
            if product.status and product.status != "启用":
                raise RuleError("product_disabled", f"商品已停用：{code} {product.name}")
            return product

        def find(self, *, category=None, name=None, contains=None, spec_thickness=None):
            products = [
                self._product(row) for row in connection.execute(
                    """select category,code,name,spec,status,brand,remark,unit,cost_price
                       from products where catalog_present=1 order by code"""
                ).fetchall()
            ]
            if category:
                products = [item for item in products if _product_key(item.category) == _product_key(category)]
            if name:
                products = [item for item in products if _product_key(item.name) == _product_key(name)]
            if contains:
                token = _product_key(contains)
                products = [item for item in products if token in _product_key(item.name) or token in _product_key(item.remark)]
            if spec_thickness is not None:
                aliases = {14.5: 15.0, 5.4: 5.2, 8.0: 9.0}
                requested = float(spec_thickness)
                expected = (8.0, 9.0) if requested in {8.0, 9.0} else (aliases.get(requested, requested),)
                products = [
                    item for item in products
                    if (numbers := _NUMBER_RE.findall(item.spec))
                    and any(abs(float(numbers[0]) - value) < 0.6 for value in expected)
                ]
            return products

    try:
        matched = match_item(
            _MigrationCatalog(),
            InventoryMappings(Path("migration.sqlite3"), connection=connection),
            TravelerItem(0, "板材与封边", display_name, 1),
        )
    except RuleError as exc:
        candidates = [str(item.get("code", "")) for item in exc.context.get("candidates", [])]
        return "", candidates
    candidates = sorted({str(item.product_code).strip().upper() for item in matched})
    return (candidates[0] if len(candidates) == 1 else ""), candidates


def _outbound_factory_tokens(value: object) -> list[str]:
    return [
        token.strip()
        for token in _OUTBOUND_FACTORY_SPLIT_RE.split(str(value or ""))
        if token.strip()
    ]


def _outbound_document_factory_candidates(
    connection: sqlite3.Connection,
    document_number: str,
    order_id: str,
    factory_value: str,
) -> set[str]:
    document_number = str(document_number or "").strip()
    order_id = str(order_id or "").strip().upper()
    if not document_number or not order_id:
        return set()
    # Production consumption never proves that a factory order was shipped,
    # including when startup backfills legacy document relationships.
    document = connection.execute(
        "select document_type from outbound_documents where document_number=?",
        (document_number,),
    ).fetchone()
    if document and document[0] == "production_materials":
        return set()
    if connection.execute(
        "select 1 from sqlite_master where type='table' and name='outbound_document_factories'"
    ).fetchone() is None:
        return set()
    # InventorySyncStore can also be exercised against the standalone
    # outbound ledger schema, where the order-index tables do not exist.  In
    # that case there is no factory identity to resolve; the header row is
    # still a valid durable outbound fact.
    if connection.execute(
        "select 1 from sqlite_master where type='table' and name='factory_orders'"
    ).fetchone() is None:
        return set()
    candidates: set[str] = set()
    for token in _outbound_factory_tokens(factory_value):
        rows = connection.execute(
            """
            select factory_order
            from factory_orders
            where order_id=? and (factory_order=? or factory_name=?)
            """,
            (order_id, token, token),
        ).fetchall()
        candidates.update(str(row[0]).strip() for row in rows if str(row[0]).strip())
    if not candidates:
        active = connection.execute(
            """
            select factory_order
            from factory_orders
            where order_id=? and aimes_status='active'
            order by factory_order
            """,
            (order_id,),
        ).fetchall()
        tokens = {
            re.sub(r"[\s_-]+", "", token).casefold()
            for token in _outbound_factory_tokens(factory_value)
        }
        order_aliases = {order_id}
        order_aliases.update(
            re.sub(r"[\s_-]+", "", str(row[0])).casefold()
            for row in connection.execute(
                "select distinct sales_order_name from factory_orders where order_id=?",
                (order_id,),
            ).fetchall()
            if str(row[0]).strip()
        )
        if len(active) == 1 and tokens.intersection(order_aliases):
            candidates.add(str(active[0][0]).strip())
    return candidates


def ensure_outbound_document_factory_links(
    connection: sqlite3.Connection,
    document_number: str,
    order_id: str,
    factory_value: str,
    *,
    updated_at: str | None = None,
) -> int:
    """Link one outbound document to its exact factory-order identities.

    The header table keeps one row per inventory document.  This relation
    table allows one document to cover multiple factory orders without
    encoding a list into the single-valued legacy ``factory_order`` column.
    An order-only value is linked only when the order has exactly one active
    factory order; split orders must provide exact factory identities.
    """
    document_number = str(document_number or "").strip()
    order_id = str(order_id or "").strip().upper()
    candidates = _outbound_document_factory_candidates(
        connection, document_number, order_id, factory_value
    )
    now = updated_at or _now()
    inserted = 0
    for factory_order in sorted(candidates):
        if connection.execute(
            """
            select 1 from outbound_document_factories
            where document_number=? and factory_order=?
            """,
            (document_number, factory_order),
        ).fetchone():
            continue
        cursor = connection.execute(
            """
            insert or ignore into outbound_document_factories(
                document_number, order_id, factory_order, created_at, updated_at
            ) values(?,?,?,?,?)
            """,
            (document_number, order_id, factory_order, now, now),
        )
        inserted += cursor.rowcount
    return inserted


def _execute_schema_statements(
    connection: sqlite3.Connection, script: str,
) -> None:
    """Execute a schema script without ``executescript``'s implicit commit.

    Python's ``sqlite3.Connection.executescript`` commits an already-open
    transaction before running the script.  Schema upgrades need their table
    creation, column additions, data copy, and cleanup to roll back together,
    so execute each complete statement inside the caller's transaction.
    """
    pending: list[str] = []
    for line in script.splitlines():
        pending.append(line)
        statement = "\n".join(pending)
        if not sqlite3.complete_statement(statement):
            continue
        if statement.strip():
            connection.execute(statement)
        pending = []
    if "\n".join(pending).strip():
        raise sqlite3.OperationalError("incomplete schema statement")


def ensure_schema(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    connection = connect_database(path)
    try:
        metadata_exists = connection.execute(
            "select 1 from sqlite_master where type='table' and name='workflow_metadata'"
        ).fetchone()
        if metadata_exists and connection.execute(
            "select 1 from workflow_metadata where key=? and value='ready'",
            (_SCHEMA_READY_MARKER,),
        ).fetchone():
            # Normal reads must not take a write lock merely to re-check an
            # already-current schema.  A legacy/grouped outbound document can
            # still be inserted after initialization, however, so repair only
            # documents that demonstrably lack their normalized factory links.
            required_tables = {
                str(row[0]) for row in connection.execute(
                    """select name from sqlite_master
                       where type='table' and name in (
                           'outbound_documents','outbound_document_factories','factory_orders'
                       )"""
                ).fetchall()
            }
            pending_documents = []
            if required_tables == {
                "outbound_documents", "outbound_document_factories", "factory_orders",
            }:
                pending_documents = connection.execute(
                    """select document_number,order_id,factory_order,updated_at
                       from outbound_documents d
                       where trim(factory_order)<>''
                         and not exists (
                             select 1 from outbound_document_factories f
                             where f.document_number=d.document_number
                         )"""
                ).fetchall()
                pending_documents = [
                    row for row in pending_documents
                    if _outbound_document_factory_candidates(
                        connection, row[0], row[1], row[2]
                    )
                ]
            if not pending_documents:
                return
            connection.execute("begin immediate")
            for document_number, order_id, factory_value, updated_at in pending_documents:
                ensure_outbound_document_factory_links(
                    connection,
                    document_number,
                    order_id,
                    factory_value,
                    updated_at=updated_at or _now(),
                )
            connection.commit()
            return
        connection.execute("begin immediate")
        _execute_schema_statements(
            connection,
            """
            create table if not exists hardware_source_decisions(
                factory_order text primary key,
                decision_json text not null
            );
            create table if not exists hardware_source_versions(
                factory_order text primary key,
                order_id text not null,
                fingerprint text not null,
                source_paths_json text not null,
                row_count integer not null,
                updated_at text not null
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
            create table if not exists workflow_metadata(
                key text primary key,
                value text not null default '',
                updated_at text not null
            );
            create table if not exists business_cache(
                cache_name text not null,
                cache_key text not null,
                value_json text not null,
                updated_at text not null,
                primary key(cache_name, cache_key)
            );
            create table if not exists production_batches(
                batch_id integer primary key,
                batch_number text not null unique,
                production_date text not null default '',
                source text not null default '',
                status text not null default 'active',
                first_seen text not null default '',
                last_seen text not null default '',
                created_at text not null,
                updated_at text not null
            );
            create table if not exists products(
                category text not null default '',
                code text primary key,
                name text not null default '',
                spec text not null default '',
                status text not null default '',
                brand text not null default '',
                remark text not null default '',
                unit text not null default '',
                cost_price real,
                normalized_code text not null default '',
                normalized_name text not null default '',
                normalized_spec text not null default '',
                normalized_category text not null default '',
                normalized_remark text not null default '',
                material_kind text not null default '',
                material_color text not null default '',
                material_thickness text not null default '',
                catalog_present integer not null default 1
            );
            create table if not exists material_items(
                id integer primary key,
                order_id text not null default '',
                product_code text not null check(trim(product_code) <> ''),
                quantity real not null default 0,
                source_type text not null default '',
                source_path text not null default '',
                source_fingerprint text not null default '',
                updated_at text not null,
                unique(order_id, product_code, source_type, source_path),
                foreign key(product_code) references products(code)
                    on update cascade on delete restrict
            );
            create index if not exists idx_material_items_order on material_items(order_id);
            create table if not exists manual_production_batches(
                batch_id integer primary key,
                batch_number text not null unique,
                order_id text not null,
                production_time text not null default '',
                source text not null default 'manual',
                status text not null default 'prepared',
                created_at text not null,
                updated_at text not null
            );
            create table if not exists manual_production_batch_factories(
                batch_id integer not null,
                order_id text not null,
                factory_order text not null,
                primary key(batch_id, factory_order),
                foreign key(batch_id) references manual_production_batches(batch_id)
            );
            create table if not exists manual_production_batch_materials(
                batch_id integer not null,
                order_id text not null,
                product_code text not null check(trim(product_code) <> ''),
                quantity real not null default 0,
                primary key(batch_id, product_code),
                foreign key(batch_id) references manual_production_batches(batch_id),
                foreign key(product_code) references products(code)
                    on update cascade on delete restrict
            );
            create index if not exists idx_manual_production_factory
                on manual_production_batch_factories(order_id, factory_order);
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
            create table if not exists hardware_items(
                id integer primary key,
                order_id text not null default '',
                factory_order text not null default '',
                scope text not null default 'factory_order',
                product_code text not null check(trim(product_code) <> ''),
                source_code text not null default '',
                name text not null default '',
                spec text not null default '',
                quantity real not null default 0,
                unit text not null default '',
                source_type text not null default 'aicnc',
                source_path text not null default '',
                active integer not null default 1,
                remarks text not null default '',
                updated_at text not null,
                foreign key(product_code) references products(code)
                    on update cascade on delete restrict
            );
            create index if not exists idx_hardware_items_order on hardware_items(order_id, factory_order, active);
            create table if not exists outbound_documents(
                id integer primary key,
                document_number text not null unique,
                document_type text not null default '',
                order_id text not null default '',
                factory_order text not null default '',
                status text not null default 'recorded',
                source text not null default '',
                issued_at text not null default '',
                source_path text not null default '',
                document_url text not null default '',
                items_json text not null default '[]',
                raw_fingerprint text not null default '',
                mapped_fingerprint text not null default '',
                updated_at text not null
            );
            create index if not exists idx_outbound_documents_order on outbound_documents(order_id, factory_order);
            create table if not exists outbound_document_factories(
                id integer primary key,
                document_number text not null,
                order_id text not null default '',
                factory_order text not null,
                created_at text not null,
                updated_at text not null,
                unique(document_number, factory_order),
                foreign key(document_number) references outbound_documents(document_number) on delete cascade
            );
            create index if not exists idx_outbound_document_factories_factory
                on outbound_document_factories(order_id, factory_order);
            create table if not exists inventory_operations(
                operation_id text primary key,
                operation_kind text not null,
                order_id text not null default '',
                factory_orders_json text not null default '[]',
                payload_json text not null default '{}',
                payload_fingerprint text not null,
                status text not null default 'prepared',
                document_results_json text not null default '[]',
                attempt_count integer not null default 0,
                last_error text not null default '',
                created_at text not null,
                updated_at text not null
            );
            create index if not exists idx_inventory_operations_lookup
                on inventory_operations(operation_kind, order_id, payload_fingerprint, updated_at desc);
            create table if not exists backup_records(
                id integer primary key,
                backup_path text not null,
                backup_kind text not null default 'daily',
                started_at text not null,
                finished_at text not null,
                status text not null,
                database_fingerprint text not null default ''
            );
            create index if not exists idx_backup_records_finished on backup_records(finished_at desc);
            create table if not exists inventory_resolution_rules(
                id integer primary key,
                rule_type text not null check(rule_type in ('mapping', 'ignore')),
                source_name text not null,
                normalized_name text not null unique,
                product_code text,
                display_name text not null default '',
                reason text not null default '',
                created_at text not null,
                updated_at text not null,
                check(
                    (rule_type = 'mapping' and product_code is not null and trim(product_code) <> '')
                    or
                    (rule_type = 'ignore' and product_code is null)
                ),
                foreign key(product_code) references products(code)
                    on update cascade on delete restrict
            );
            create index if not exists idx_inventory_rules_type
                on inventory_resolution_rules(rule_type, normalized_name);
            create table if not exists outbound_scope_decisions(
                id integer primary key,
                order_id text not null,
                scope_type text not null check(scope_type in ('material', 'hardware')),
                factory_order text not null default '',
                requirement text not null check(requirement in ('required', 'customer_supplied', 'remainder', 'not_required')),
                reason text not null default '',
                source_fingerprint text not null default '',
                created_at text not null,
                updated_at text not null,
                unique(order_id, scope_type, factory_order)
            );
            create index if not exists idx_outbound_scope_order
                on outbound_scope_decisions(order_id, scope_type, factory_order);
            """
        )
        product_columns = {
            row[1] for row in connection.execute("pragma table_info(products)").fetchall()
        }
        added_product_material_columns = not {
            "material_kind", "material_color", "material_thickness", "catalog_present"
        }.issubset(product_columns)
        for column, definition in (
            ("category", "text not null default ''"),
            ("name", "text not null default ''"),
            ("spec", "text not null default ''"),
            ("status", "text not null default ''"),
            ("brand", "text not null default ''"),
            ("remark", "text not null default ''"),
            ("unit", "text not null default ''"),
            ("cost_price", "real"),
            ("normalized_code", "text not null default ''"),
            ("normalized_name", "text not null default ''"),
            ("normalized_spec", "text not null default ''"),
            ("normalized_category", "text not null default ''"),
            ("normalized_remark", "text not null default ''"),
            ("material_kind", "text not null default ''"),
            ("material_color", "text not null default ''"),
            ("material_thickness", "text not null default ''"),
            ("catalog_present", "integer not null default 1"),
        ):
            if column not in product_columns:
                connection.execute(f"alter table products add column {column} {definition}")
        material_columns = {
            row[1] for row in connection.execute("pragma table_info(material_items)").fetchall()
        }
        if added_product_material_columns or "product_code" not in material_columns:
            product_rows = connection.execute(
                "select code, category, name, spec, remark from products"
            ).fetchall()
            for code, category, name, spec, remark in product_rows:
                kind, color, thickness = catalog_material_attributes(category, name, spec, code)
                connection.execute(
                    """update products
                       set normalized_code=?, normalized_name=?, normalized_spec=?,
                           normalized_category=?, normalized_remark=?,
                           material_kind=?, material_color=?, material_thickness=?
                       where code=?""",
                    (
                        _product_key(code), _product_key(name), _product_key(spec),
                        _product_key(category), _product_key(remark),
                        kind, color, thickness, code,
                    ),
                )
        hardware_columns = {
            row[1] for row in connection.execute("pragma table_info(hardware_items)").fetchall()
        }
        if "source_code" not in hardware_columns:
            connection.execute(
                "alter table hardware_items add column source_code text not null default ''"
            )
        inventory_rule_columns = {
            row[1] for row in connection.execute(
                "pragma table_info(inventory_resolution_rules)"
            ).fetchall()
        }
        if "display_name" not in inventory_rule_columns:
            connection.execute(
                "alter table inventory_resolution_rules add column display_name text not null default ''"
            )
        if "product_code" not in material_columns:
            legacy_rows = connection.execute(
                "select * from material_items"
            ).fetchall()
            legacy_names = [
                str(row[1]) for row in connection.execute("pragma table_info(material_items)")
            ]
            legacy_materials = [dict(zip(legacy_names, row)) for row in legacy_rows]
            selected_materials = [
                row for row in legacy_materials
                if not str(row.get("factory_order", "") or "").strip()
                and str(row.get("scope", "") or "").strip() in {"", "order"}
            ]
            material_codes: dict[tuple[str, str, str, str, str, str], str] = {}
            product_business_attributes: dict[str, dict[str, list[str]]] = {}
            unresolved: list[str] = []
            for row in selected_materials:
                code, candidates = _resolve_legacy_material_code(
                    connection, row.get("material_type"), row.get("color"), row.get("thickness")
                )
                if not code:
                    unresolved.append(
                        f"id={row.get('id')} order={row.get('order_id')} "
                        f"material={row.get('material_type')}/{row.get('color')}/{row.get('thickness')} "
                        f"candidates={','.join(candidates) or '-'}"
                    )
                    continue
                identity = (
                    str(row.get("order_id", "")).upper(),
                    str(row.get("material_type", "")), str(row.get("color", "")),
                    str(row.get("thickness", "")), str(row.get("edge", "")),
                    str(row.get("unit", "")),
                )
                previous = material_codes.get(identity)
                if previous and previous != code:
                    unresolved.append(
                        f"order={identity[0]} material={'/'.join(identity[1:])} "
                        f"conflicting_skus={previous},{code}"
                    )
                material_codes[identity] = code
                attributes = product_business_attributes.setdefault(
                    code, {"kind": [], "color": [], "thickness": []}
                )
                attributes["kind"].append(str(row.get("material_type", "")).strip().casefold())
                if str(row.get("color", "") or "").strip():
                    attributes["color"].append(str(row.get("color", "")).strip())
                if str(row.get("thickness", "") or "").strip():
                    attributes["thickness"].append(str(row.get("thickness", "")).strip())

            production_columns = {
                row[1] for row in connection.execute(
                    "pragma table_info(manual_production_batch_materials)"
                ).fetchall()
            }
            legacy_production: list[dict[str, Any]] = []
            if production_columns and "product_code" not in production_columns:
                production_names = [
                    str(row[1]) for row in connection.execute(
                        "pragma table_info(manual_production_batch_materials)"
                    )
                ]
                legacy_production = [
                    dict(zip(production_names, row))
                    for row in connection.execute(
                        "select * from manual_production_batch_materials"
                    ).fetchall()
                ]
                for row in legacy_production:
                    identity = (
                        str(row.get("order_id", "")).upper(),
                        str(row.get("material_type", "")), str(row.get("color", "")),
                        str(row.get("thickness", "")), str(row.get("edge", "")),
                        str(row.get("unit", "")),
                    )
                    code = material_codes.get(identity, "")
                    if not code:
                        code, candidates = _resolve_legacy_material_code(
                            connection, row.get("material_type"), row.get("color"), row.get("thickness")
                        )
                        if not code:
                            unresolved.append(
                                f"production batch={row.get('batch_id')} order={row.get('order_id')} "
                                f"material={row.get('material_type')}/{row.get('color')}/{row.get('thickness')} "
                                f"candidates={','.join(candidates) or '-'}"
                            )
                    row["product_code"] = code
            if unresolved:
                raise ValueError(
                    "旧材料无法唯一迁移到商品 SKU；数据库未修改：\n" + "\n".join(unresolved)
                )

            for code, values in sorted(product_business_attributes.items()):
                kinds = {value for value in values["kind"] if value}
                color_groups: dict[str, list[str]] = {}
                for value in values["color"]:
                    color_groups.setdefault(_product_key(value), []).append(value)
                thicknesses = {
                    f"{float(value):g}" for value in values["thickness"] if value
                }
                if len(kinds) != 1 or len(color_groups) > 1 or len(thicknesses) > 1:
                    raise ValueError(
                        f"商品 {code} 的历史材料属性冲突："
                        f"type={sorted(kinds)} color={sorted(color_groups)} "
                        f"thickness={sorted(thicknesses)}"
                    )
                kind = next(iter(kinds))
                color = ""
                if color_groups:
                    variants = next(iter(color_groups.values()))
                    counts: dict[str, int] = {}
                    for value in variants:
                        counts[value] = counts.get(value, 0) + 1
                    color = sorted(counts, key=lambda value: (-counts[value], value.casefold()))[0]
                thickness = next(iter(thicknesses), "")
                connection.execute(
                    """update products
                       set material_kind=?, material_color=?, material_thickness=?
                       where code=?""",
                    (kind, color, thickness, code),
                )

            connection.execute("drop index if exists idx_material_items_order")
            connection.execute("alter table material_items rename to material_items_legacy")
            connection.execute(
                """
                create table material_items(
                    id integer primary key,
                    order_id text not null default '',
                    product_code text not null check(trim(product_code) <> ''),
                    quantity real not null default 0,
                    source_type text not null default '',
                    source_path text not null default '',
                    source_fingerprint text not null default '',
                    updated_at text not null,
                    unique(order_id, product_code, source_type, source_path),
                    foreign key(product_code) references products(code)
                        on update cascade on delete restrict
                )
                """
            )
            aggregated: dict[tuple[str, str, str, str], dict[str, Any]] = {}
            for row in selected_materials:
                identity = (
                    str(row.get("order_id", "")).upper(),
                    str(row.get("material_type", "")), str(row.get("color", "")),
                    str(row.get("thickness", "")), str(row.get("edge", "")),
                    str(row.get("unit", "")),
                )
                code = material_codes[identity]
                key = (
                    identity[0], code, str(row.get("source_type", "")),
                    str(row.get("source_path", "")),
                )
                target = aggregated.setdefault(key, {
                    "id": int(row.get("id", 0) or 0),
                    "quantity": 0.0,
                    "source_fingerprint": str(row.get("source_fingerprint", "") or ""),
                    "updated_at": str(row.get("updated_at", "") or ""),
                })
                target["quantity"] += float(row.get("quantity", 0) or 0)
                if int(row.get("id", 0) or 0) and (
                    not target["id"] or int(row.get("id", 0)) < target["id"]
                ):
                    target["id"] = int(row["id"])
                if str(row.get("updated_at", "") or "") >= target["updated_at"]:
                    target["updated_at"] = str(row.get("updated_at", "") or "")
                    target["source_fingerprint"] = str(row.get("source_fingerprint", "") or "")
            for key, value in aggregated.items():
                connection.execute(
                    """insert into material_items(
                           id, order_id, product_code, quantity, source_type, source_path,
                           source_fingerprint, updated_at
                       ) values(?,?,?,?,?,?,?,?)""",
                    (value["id"] or None, key[0], key[1], value["quantity"], key[2], key[3],
                     value["source_fingerprint"], value["updated_at"]),
                )
            connection.execute("drop table material_items_legacy")
            connection.execute("create index idx_material_items_order on material_items(order_id)")
            if production_columns and "product_code" not in production_columns:
                connection.execute(
                    "alter table manual_production_batch_materials rename to manual_production_batch_materials_legacy"
                )
                connection.execute(
                    """create table manual_production_batch_materials(
                           batch_id integer not null,
                           order_id text not null,
                           product_code text not null check(trim(product_code) <> ''),
                           quantity real not null default 0,
                           primary key(batch_id, product_code),
                           foreign key(batch_id) references manual_production_batches(batch_id),
                           foreign key(product_code) references products(code)
                               on update cascade on delete restrict
                       )"""
                )
                grouped_production: dict[tuple[int, str], dict[str, Any]] = {}
                for row in legacy_production:
                    key = (int(row["batch_id"]), str(row["product_code"]))
                    if key in grouped_production:
                        target = grouped_production[key]
                        target["quantity"] = float(target.get("quantity", 0) or 0) + float(row.get("quantity", 0) or 0)
                    else:
                        grouped_production[key] = dict(row)
                connection.executemany(
                    """insert into manual_production_batch_materials(
                           batch_id, order_id, product_code, quantity
                       ) values(?,?,?,?)""",
                    [(
                        row["batch_id"], row["order_id"], row["product_code"],
                        row.get("quantity", 0),
                    ) for row in grouped_production.values()],
                )
                connection.execute("drop table manual_production_batch_materials_legacy")
                connection.execute(
                    "create index idx_manual_production_material on manual_production_batch_materials(order_id, product_code)"
                )

        production_material_columns = {
            row[1] for row in connection.execute(
                "pragma table_info(manual_production_batch_materials)"
            ).fetchall()
        }
        if production_material_columns and (
            production_material_columns != {"batch_id", "order_id", "product_code", "quantity"}
            or not _has_product_foreign_key(connection, "manual_production_batch_materials")
        ):
            # A partial development database may already carry product_code
            # together with the legacy descriptive columns.  Collapse it to
            # the final SKU-only shape without changing batch quantities.
            if "product_code" in production_material_columns:
                rows = connection.execute(
                    "select batch_id,order_id,product_code,quantity from manual_production_batch_materials"
                ).fetchall()
            else:
                legacy_names = [
                    str(row[1]) for row in connection.execute(
                        "pragma table_info(manual_production_batch_materials)"
                    )
                ]
                legacy_rows = [
                    dict(zip(legacy_names, row))
                    for row in connection.execute(
                        "select * from manual_production_batch_materials"
                    ).fetchall()
                ]
                unresolved_production: list[str] = []
                rows = []
                for row in legacy_rows:
                    code, candidates = _resolve_legacy_material_code(
                        connection,
                        row.get("material_type"),
                        row.get("color"),
                        row.get("thickness"),
                    )
                    if not code:
                        unresolved_production.append(
                            f"batch={row.get('batch_id')} order={row.get('order_id')} "
                            f"candidates={','.join(candidates) or '-'}"
                        )
                        continue
                    rows.append((
                        row.get("batch_id"), row.get("order_id"), code,
                        row.get("quantity", 0),
                    ))
                if unresolved_production:
                    raise ValueError(
                        "旧生产材料无法唯一迁移到商品 SKU：\n"
                        + "\n".join(unresolved_production)
                    )
            invalid = [str(row[2] or "") for row in rows if not connection.execute(
                "select 1 from products where code=?", (str(row[2] or "").strip().upper(),)
            ).fetchone()]
            if invalid:
                raise ValueError("生产材料包含不存在的商品 SKU：" + "、".join(sorted(set(invalid))))
            connection.execute("drop index if exists idx_manual_production_material")
            connection.execute(
                "alter table manual_production_batch_materials rename to manual_production_batch_materials_legacy_shape"
            )
            connection.execute(
                """create table manual_production_batch_materials(
                       batch_id integer not null,
                       order_id text not null,
                       product_code text not null check(trim(product_code) <> ''),
                       quantity real not null default 0,
                       primary key(batch_id, product_code),
                       foreign key(batch_id) references manual_production_batches(batch_id),
                       foreign key(product_code) references products(code)
                           on update cascade on delete restrict
                   )"""
            )
            connection.executemany(
                """insert into manual_production_batch_materials(
                       batch_id,order_id,product_code,quantity
                   ) values(?,?,?,?)
                   on conflict(batch_id,product_code) do update set
                       quantity=manual_production_batch_materials.quantity+excluded.quantity""",
                [(row[0], row[1], str(row[2]).strip().upper(), row[3]) for row in rows],
            )
            connection.execute("drop table manual_production_batch_materials_legacy_shape")
            connection.execute(
                "create index idx_manual_production_material on manual_production_batch_materials(order_id,product_code)"
            )

        allocation_columns = {
            row[1] for row in connection.execute(
                "pragma table_info(server_material_allocations)"
            ).fetchall()
        }
        allocation_target_columns = {
            "id", "source_path", "source_material_key", "product_code",
            "source_quantity", "order_id", "allocated_quantity",
            "source_fingerprint", "created_at", "updated_at",
        }
        if allocation_columns and (
            allocation_columns != allocation_target_columns
            or not _has_product_foreign_key(connection, "server_material_allocations")
        ):
            names = [
                str(row[1]) for row in connection.execute(
                    "pragma table_info(server_material_allocations)"
                )
            ]
            old_allocations = [
                dict(zip(names, row))
                for row in connection.execute("select * from server_material_allocations").fetchall()
            ]
            allocation_errors: list[str] = []
            for row in old_allocations:
                code = str(row.get("product_code", "") or "").strip().upper()
                if not code and {"material_type", "color", "thickness"}.issubset(row):
                    code, candidates = _resolve_legacy_material_code(
                        connection, row.get("material_type"), row.get("color"), row.get("thickness")
                    )
                else:
                    candidates = [code] if code else []
                if not code or connection.execute(
                    "select 1 from products where code=?", (code,)
                ).fetchone() is None:
                    allocation_errors.append(
                        f"id={row.get('id')} path={row.get('source_path')} "
                        f"candidates={','.join(candidates) or '-'}"
                    )
                row["product_code"] = code
            if allocation_errors:
                raise ValueError(
                    "Server 材料分配无法唯一迁移到商品 SKU：\n" + "\n".join(allocation_errors)
                )
            connection.execute("drop index if exists idx_server_material_allocations_source")
            connection.execute("drop index if exists idx_server_material_allocations_order")
            connection.execute(
                "alter table server_material_allocations rename to server_material_allocations_legacy"
            )
            connection.execute(
                """create table server_material_allocations(
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
                   )"""
            )
            connection.executemany(
                """insert into server_material_allocations(
                       id,source_path,source_material_key,product_code,source_quantity,
                       order_id,allocated_quantity,source_fingerprint,created_at,updated_at
                   ) values(?,?,?,?,?,?,?,?,?,?)""",
                [(
                    row.get("id"), row.get("source_path", ""),
                    server_material_identity_key(row.get("source_path"), row["product_code"]),
                    row["product_code"], row.get("source_quantity", 0),
                    row.get("order_id", ""), row.get("allocated_quantity", 0),
                    row.get("source_fingerprint", ""), row.get("created_at", ""),
                    row.get("updated_at", ""),
                ) for row in old_allocations],
            )
            connection.execute("drop table server_material_allocations_legacy")
            connection.execute(
                "create index idx_server_material_allocations_source on server_material_allocations(source_path,source_material_key)"
            )
            connection.execute(
                "create index idx_server_material_allocations_order on server_material_allocations(order_id)"
            )

        if not _has_product_foreign_key(connection, "hardware_items"):
            hardware_names = [
                str(row[1]) for row in connection.execute("pragma table_info(hardware_items)")
            ]
            hardware_rows = connection.execute(
                f"select {','.join(hardware_names)} from hardware_items"
            ).fetchall()
            invalid_hardware = sorted({
                str(row[hardware_names.index("product_code")] or "").strip().upper()
                for row in hardware_rows
                if connection.execute(
                    "select 1 from products where code=?",
                    (str(row[hardware_names.index("product_code")] or "").strip().upper(),),
                ).fetchone() is None
            })
            if invalid_hardware:
                raise ValueError("五金事实包含不存在的商品 SKU：" + "、".join(invalid_hardware))
            connection.execute("drop index if exists idx_hardware_items_order")
            connection.execute("alter table hardware_items rename to hardware_items_legacy")
            connection.execute(
                """create table hardware_items(
                       id integer primary key,
                       order_id text not null default '',
                       factory_order text not null default '',
                       scope text not null default 'factory_order',
                       product_code text not null check(trim(product_code) <> ''),
                       source_code text not null default '',
                       name text not null default '',
                       spec text not null default '',
                       quantity real not null default 0,
                       unit text not null default '',
                       source_type text not null default 'aicnc',
                       source_path text not null default '',
                       active integer not null default 1,
                       remarks text not null default '',
                       updated_at text not null,
                       foreign key(product_code) references products(code)
                           on update cascade on delete restrict
                   )"""
            )
            connection.executemany(
                f"insert into hardware_items({','.join(hardware_names)}) values({','.join('?' for _ in hardware_names)})",
                hardware_rows,
            )
            connection.execute("drop table hardware_items_legacy")
            connection.execute(
                "create index idx_hardware_items_order on hardware_items(order_id,factory_order,active)"
            )

        if not _has_product_foreign_key(connection, "inventory_resolution_rules"):
            rule_names = [
                str(row[1]) for row in connection.execute(
                    "pragma table_info(inventory_resolution_rules)"
                )
            ]
            rule_rows = connection.execute(
                f"select {','.join(rule_names)} from inventory_resolution_rules"
            ).fetchall()
            code_index = rule_names.index("product_code")
            invalid_rules = sorted({
                str(row[code_index] or "").strip().upper()
                for row in rule_rows if row[code_index] and connection.execute(
                    "select 1 from products where code=?", (str(row[code_index]).strip().upper(),)
                ).fetchone() is None
            })
            if invalid_rules:
                raise ValueError("库存映射包含不存在的商品 SKU：" + "、".join(invalid_rules))
            connection.execute("drop index if exists idx_inventory_rules_type")
            connection.execute(
                "alter table inventory_resolution_rules rename to inventory_resolution_rules_legacy"
            )
            connection.execute(
                """create table inventory_resolution_rules(
                       id integer primary key,
                       rule_type text not null check(rule_type in ('mapping','ignore')),
                       source_name text not null,
                       normalized_name text not null unique,
                       product_code text,
                       display_name text not null default '',
                       reason text not null default '',
                       created_at text not null,
                       updated_at text not null,
                       check(
                           (rule_type='mapping' and product_code is not null and trim(product_code)<>'')
                           or (rule_type='ignore' and product_code is null)
                       ),
                       foreign key(product_code) references products(code)
                           on update cascade on delete restrict
                   )"""
            )
            connection.executemany(
                f"insert into inventory_resolution_rules({','.join(rule_names)}) values({','.join('?' for _ in rule_names)})",
                rule_rows,
            )
            connection.execute("drop table inventory_resolution_rules_legacy")
            connection.execute(
                "create index idx_inventory_rules_type on inventory_resolution_rules(rule_type,normalized_name)"
            )
        connection.execute(
            "create index if not exists idx_products_name on products(normalized_name)"
        )
        connection.execute(
            "create index if not exists idx_products_category on products(normalized_category)"
        )
        connection.execute(
            "create index if not exists idx_manual_production_material "
            "on manual_production_batch_materials(order_id,product_code)"
        )
        connection.execute("drop table if exists material_allocations")
        factory_table = connection.execute(
            "select 1 from sqlite_master where type='table' and name='factory_orders'"
        ).fetchone()
        if factory_table is not None:
            outbound_columns = {
                row[1] for row in connection.execute("pragma table_info(outbound_documents)").fetchall()
            }
            for column, definition in (
                ("document_url", "text not null default ''"),
                ("items_json", "text not null default '[]'"),
                ("raw_fingerprint", "text not null default ''"),
                ("mapped_fingerprint", "text not null default ''"),
            ):
                if column not in outbound_columns:
                    connection.execute(
                        f"alter table outbound_documents add column {column} {definition}"
                    )
            factory_columns = {
                row[1] for row in connection.execute("pragma table_info(factory_orders)").fetchall()
            }
            for column, definition in (
                ("aimes_status", "text not null default 'active'"),
                ("aimes_deleted_at", "text not null default ''"),
                ("aimes_last_verified_at", "text not null default ''"),
            ):
                if column not in factory_columns:
                    try:
                        connection.execute(
                            f"alter table factory_orders add column {column} {definition}"
                        )
                    except sqlite3.OperationalError as exc:
                        # Two independent one-shot commands can prepare the
                        # same fresh state directory concurrently.  The first
                        # transaction may add the column after this caller's
                        # pragma snapshot; that is a successful race, not a
                        # schema failure.
                        if "duplicate column name" not in str(exc).lower():
                            raise
            for document_number, order_id, factory_value, updated_at in connection.execute(
                "select document_number, order_id, factory_order, updated_at from outbound_documents"
            ).fetchall():
                ensure_outbound_document_factory_links(
                    connection,
                    document_number,
                    order_id,
                    factory_value,
                    updated_at=updated_at or _now(),
                )
        integrity_rows = connection.execute("pragma integrity_check").fetchall()
        if integrity_rows != [("ok",)]:
            raise ValueError(
                "数据库结构迁移完整性检查失败："
                + "；".join(str(row[0]) for row in integrity_rows)
            )
        foreign_key_rows = connection.execute("pragma foreign_key_check").fetchall()
        if foreign_key_rows:
            details = "；".join(
                f"{row[0]} rowid={row[1]} parent={row[2]}"
                for row in foreign_key_rows[:20]
            )
            raise ValueError("数据库结构迁移外键检查失败：" + details)
        connection.execute(
            """insert into workflow_metadata(key,value,updated_at) values(?,?,?)
               on conflict(key) do update set
                   value=excluded.value, updated_at=excluded.updated_at""",
            (_SCHEMA_READY_MARKER, "ready", _now()),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def collapse_actual_installation_days(connection: sqlite3.Connection) -> int:
    """Keep only the earliest actual installation date for each order.

    The table remains date-type based for compatibility with existing
    databases and the planned start-date row.  Actual installation is now an
    order-level start date, so older rows after the earliest date are removed
    while the installer attached to the earliest row is preserved.
    """
    table = connection.execute(
        "select 1 from sqlite_master where type='table' and name='order_installation_days'"
    ).fetchone()
    if table is None:
        return 0
    cursor = connection.execute(
        """
        delete from order_installation_days
        where date_type = 'actual'
          and exists (
              select 1
              from order_installation_days earliest
              where earliest.order_id = order_installation_days.order_id
                and earliest.date_type = 'actual'
                and (
                    earliest.install_date < order_installation_days.install_date
                    or (
                        earliest.install_date = order_installation_days.install_date
                        and earliest.rowid < order_installation_days.rowid
                    )
                )
          )
        """
    )
    connection.execute(
        """
        create unique index if not exists idx_order_installation_actual_start
        on order_installation_days(order_id)
        where date_type = 'actual'
        """
    )
    return max(cursor.rowcount, 0)


def _normalize_inventory_rule_name(value: str) -> str:
    return re.sub(r"[\s_-]+", "", str(value)).upper()


_LEGACY_MAPPING_DISPLAY_NAMES = {
    "EDGEBANDINGWOODLINE4": "Edge banding--Woodline 4",
    "ADJUSTABLESHELFHOLDER": "Adjustable shelf holder",
    "EDGEBANDINGPENELOPEFA44": "Edge banding--Penelope FA44",
    "19.1MMPENELOPEFA44": "19.1mm--Penelope FA44",
    "8MMWOODLINE3": "8mm--Woodline 3",
    "19.1MMWALNUT": "19.1mm--Walnut",
    "EDGEBANDINGWALNUT": "Edge banding--Walnut",
    "CLOTHRODBRACKETFITTING": "Cloth rod bracket - Fitting",
}


def migrate_inventory_mapping_file(state_dir: Path) -> dict[str, Any]:
    """Move the legacy mapping JSON into the central database once.

    The JSON is archived only after the transaction commits.  Runtime code
    does not use the archived file; it exists solely as a recoverable record
    of the pre-database configuration.
    """
    central = database_path(state_dir)
    ensure_schema(central)
    source = state_dir / "inventory" / "mappings.json"
    connection = connect_database(central)
    try:
        # App startup can prepare storage from more than one background task.
        # Serialize this one-time migration so two callers cannot both observe
        # a missing marker and then race on workflow_metadata's primary key.
        connection.execute("begin immediate")
        marker = connection.execute(
            "select value from workflow_metadata where key='inventory_mapping_migration_v1'"
        ).fetchone()
        if marker is not None:
            return {"status": "already_migrated", "central": str(central)}
        if not source.is_file():
            connection.execute(
                "insert into workflow_metadata(key,value,updated_at) values(?,?,?)",
                ("inventory_mapping_migration_v1", json.dumps({"manual": 0, "ignored": 0}), _now()),
            )
            connection.commit()
            return {"status": "no_legacy_file", "central": str(central)}
        try:
            payload = json.loads(source.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError) as exc:
            raise ValueError(f"库存映射文件无法读取：{source}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"库存映射文件格式无效：{source}")
        manual = payload.get("manual", {})
        ignored = payload.get("ignored", {})
        if not isinstance(manual, dict) or not isinstance(ignored, dict):
            raise ValueError(f"库存映射文件缺少 manual/ignored 对象：{source}")

        rows: list[tuple[str, str, str | None, str]] = []
        for raw_name, raw_code in manual.items():
            normalized = _normalize_inventory_rule_name(raw_name)
            code = str(raw_code or "").strip().upper()
            if not normalized or not code:
                raise ValueError(f"库存映射文件包含空名称或空 SKU：{raw_name}")
            display_name = _LEGACY_MAPPING_DISPLAY_NAMES.get(normalized, str(raw_name).strip())
            rows.append(("mapping", display_name, code, ""))
        for raw_name, raw_reason in ignored.items():
            normalized = _normalize_inventory_rule_name(raw_name)
            if not normalized:
                raise ValueError(f"库存忽略文件包含空名称：{raw_name}")
            display_name = _LEGACY_MAPPING_DISPLAY_NAMES.get(normalized, str(raw_name).strip())
            rows.append(("ignore", display_name, None, str(raw_reason or "").strip() or "用户确认全局忽略"))

        has_products = connection.execute(
            "select 1 from sqlite_master where type='table' and name='products'"
        ).fetchone() is not None
        if has_products and connection.execute("select count(*) from products").fetchone()[0]:
            for rule_type, display_name, product_code, _ in rows:
                if rule_type != "mapping":
                    continue
                product = connection.execute(
                    "select code, status from products where normalized_code=?",
                    (_normalize_inventory_rule_name(product_code or ""),),
                ).fetchall()
                if len(product) != 1:
                    raise ValueError(f"库存映射的 SKU 不存在或不唯一：{display_name} → {product_code}")
                if product[0][1] and product[0][1] != "启用":
                    raise ValueError(f"库存映射的商品已停用：{display_name} → {product_code}")

        now = _now()
        for rule_type, display_name, product_code, reason in rows:
            normalized = _normalize_inventory_rule_name(display_name)
            existing = connection.execute(
                "select rule_type, product_code from inventory_resolution_rules where normalized_name=?",
                (normalized,),
            ).fetchone()
            if existing is not None:
                if existing[0] != rule_type or (product_code and existing[1] != product_code):
                    raise ValueError(f"库存映射规则冲突：{display_name}")
                continue
            connection.execute(
                """insert into inventory_resolution_rules(
                    rule_type, source_name, normalized_name, product_code, reason, created_at, updated_at
                ) values(?,?,?,?,?,?,?)""",
                (rule_type, display_name, normalized, product_code, reason, now, now),
            )
        connection.execute(
            "insert into workflow_metadata(key,value,updated_at) values(?,?,?)",
            ("inventory_mapping_migration_v1", json.dumps({"manual": len(manual), "ignored": len(ignored)}, ensure_ascii=False), now),
        )
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()

    # The legacy merge can create a central factory_orders table from an old
    # schema after the first ensure_schema call. Run the lightweight migration
    # once more so direct detail reads are safe before OrderIndexStore opens.
    ensure_schema(central)

    archive = state_dir / "migration-archives" / datetime.now().strftime("%Y%m%d-%H%M%S")
    archive.mkdir(parents=True, exist_ok=True)
    destination = archive / source.name
    if not destination.exists():
        shutil.move(str(source), str(destination))
    return {
        "status": "completed",
        "central": str(central),
        "source": str(source),
        "archived": str(destination),
        "manual": len(manual),
        "ignored": len(ignored),
    }


def _copy_table(source: sqlite3.Connection, target: sqlite3.Connection, table: str) -> bool:
    exists = source.execute(
        "select sql from sqlite_master where type='table' and name=?", (table,)
    ).fetchone()
    if exists is None:
        return False
    target.execute(f"drop table if exists {table}")
    target.execute(exists[0])
    columns = [row[1] for row in source.execute(f"pragma table_info({table})").fetchall()]
    if columns:
        names = ",".join('"' + column.replace('"', '""') + '"' for column in columns)
        target.executemany(
            f"insert into {table}({names}) values({','.join('?' for _ in columns)})",
            source.execute(f"select {names} from {table}").fetchall(),
        )
    return True


def migrate_legacy_databases(state_dir: Path) -> dict[str, Any]:
    """Merge old local facts into the central DB and archive source files.

    The operation is idempotent. Legacy files are moved to a timestamped
    archive only after their data has been committed to the central database;
    runtime code therefore has one canonical storage path after cutover.
    """
    central = database_path(state_dir)
    ensure_schema(central)
    legacy_paths = [state_dir / "order-index.sqlite3"]
    existing = [path for path in legacy_paths if path.is_file() and path != central]
    outbound_json = state_dir / "inventory-outbound-records.json"
    cache_sources = {
        "aimes_orders": state_dir / "aimes-orders.json",
        "factory_names": state_dir / "factory-names.json",
    }
    if not existing and not outbound_json.is_file() and not any(path.is_file() for path in cache_sources.values()):
        return {"central": str(central), "migrated": [], "status": "no_legacy_files"}

    connection = connect_database(central)
    migrated: list[str] = []
    try:
        for legacy in existing:
            source = sqlite3.connect(legacy)
            try:
                tables = [
                    "orders", "factory_orders", "source_files", "sync_runs", "sync_changes",
                    "ignored_aimes_factory_orders", "aimes_order_assignments", "aimes_review_rows",
                    "active_issues", "temporary_orders",
                ]
                for table in tables:
                    # Existing central tables are preserved; row-level merge is
                    # handled by INSERT OR IGNORE for stable primary keys.
                    sql = source.execute(
                        "select sql from sqlite_master where type='table' and name=?", (table,)
                    ).fetchone()
                    if sql is None:
                        continue
                    columns = [row[1] for row in source.execute(f"pragma table_info({table})").fetchall()]
                    if not columns:
                        continue
                    target_exists = connection.execute(
                        "select 1 from sqlite_master where type='table' and name=?", (table,)
                    ).fetchone()
                    if target_exists is None:
                        connection.execute(sql[0])
                    names = ",".join('"' + column.replace('"', '""') + '"' for column in columns)
                    rows = source.execute(f"select {names} from {table}").fetchall()
                    placeholders = ",".join("?" for _ in columns)
                    for row in rows:
                        try:
                            connection.execute(
                                f"insert or ignore into {table}({names}) values({placeholders})", row
                            )
                        except sqlite3.Error:
                            # A newer central schema may intentionally omit a
                            # historical column. The source remains archived.
                            continue
                migrated.append(str(legacy))
            finally:
                source.close()
        connection.execute(
            "insert into workflow_metadata(key,value,updated_at) values('legacy_migration',?,?) "
            "on conflict(key) do update set value=excluded.value, updated_at=excluded.updated_at",
            (json.dumps(migrated, ensure_ascii=False), _now()),
        )
        if outbound_json.is_file():
            try:
                payload = json.loads(outbound_json.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                payload = {}
            records = payload.get("records", {}) if isinstance(payload, dict) else {}
            for record in records.values() if isinstance(records, dict) else []:
                document = str(record.get("document_number", "")).strip()
                if not document:
                    continue
                connection.execute(
                    """insert into outbound_documents(
                        document_number,document_type,order_id,factory_order,status,source,issued_at,source_path,
                        document_url,items_json,raw_fingerprint,mapped_fingerprint,updated_at
                    ) values(?,?,?,?,?,?,?,?,?,?,?,?,?)
                    on conflict(document_number) do update set
                        document_type=case when excluded.document_type <> '' then excluded.document_type else outbound_documents.document_type end,
                        order_id=case when excluded.order_id <> '' then excluded.order_id else outbound_documents.order_id end,
                        factory_order=case when excluded.factory_order <> '' then excluded.factory_order else outbound_documents.factory_order end,
                        status=case when excluded.status <> '' then excluded.status else outbound_documents.status end,
                        issued_at=case when excluded.issued_at <> '' then excluded.issued_at else outbound_documents.issued_at end,
                        source_path=case when excluded.source_path <> '' then excluded.source_path else outbound_documents.source_path end,
                        document_url=case when excluded.document_url <> '' then excluded.document_url else outbound_documents.document_url end,
                        items_json=case when excluded.items_json <> '[]' then excluded.items_json else outbound_documents.items_json end,
                        raw_fingerprint=case when excluded.raw_fingerprint <> '' then excluded.raw_fingerprint else outbound_documents.raw_fingerprint end,
                        mapped_fingerprint=case when excluded.mapped_fingerprint <> '' then excluded.mapped_fingerprint else outbound_documents.mapped_fingerprint end,
                        updated_at=excluded.updated_at""",
                    (document, str(record.get("kind", "")), str(record.get("order_id", "")),
                     str(record.get("remark", "")), str(record.get("status", "已出库")), "legacy-json",
                     str(record.get("synced_at", "")), str(record.get("traveler_path", "")),
                     str(record.get("document_url", "")), json.dumps(record.get("items", []), ensure_ascii=False, separators=(",", ":")),
                     str(record.get("raw_fingerprint", "")), str(record.get("mapped_fingerprint", "")), _now()),
                )
        for cache_name, source_path in cache_sources.items():
            if not source_path.is_file():
                continue
            try:
                value = json.loads(source_path.read_text(encoding="utf-8"))
            except (OSError, json.JSONDecodeError):
                continue
            encoded = json.dumps(value, ensure_ascii=False, sort_keys=True)
            connection.execute(
                """insert into business_cache(cache_name,cache_key,value_json,updated_at)
                   values(?,?,?,?)
                   on conflict(cache_name,cache_key) do update set
                     value_json=case when business_cache.value_json in ('', 'null', '{}', '[]') then excluded.value_json else business_cache.value_json end,
                     updated_at=excluded.updated_at""",
                (cache_name, "value", encoded, _now()),
            )
        for document_number, order_id, factory_value, updated_at in connection.execute(
            "select document_number, order_id, factory_order, updated_at from outbound_documents"
        ).fetchall():
            ensure_outbound_document_factory_links(
                connection,
                document_number,
                order_id,
                factory_value,
                updated_at=updated_at or _now(),
            )
        connection.commit()
    finally:
        connection.close()

    archive = state_dir / "migration-archives" / datetime.now().strftime("%Y%m%d-%H%M%S")
    archive.mkdir(parents=True, exist_ok=True)
    archived: list[str] = []
    archive_sources = [*existing]
    if outbound_json.is_file():
        archive_sources.append(outbound_json)
    archive_sources.extend(path for path in cache_sources.values() if path.is_file())
    for legacy in archive_sources:
        destination = archive / legacy.name
        if not destination.exists():
            shutil.move(str(legacy), str(destination))
            archived.append(str(destination))
    return {"central": str(central), "migrated": migrated, "archived": archived, "status": "completed"}


def _cache_rows(path: Path, cache_name: str) -> dict[str, Any]:
    ensure_schema(path)
    connection = connect_database(path)
    try:
        return {
            row[0]: json.loads(row[1])
            for row in connection.execute(
                "select cache_key,value_json from business_cache where cache_name=?", (cache_name,)
            ).fetchall()
        }
    finally:
        connection.close()


def read_cache(path: Path, cache_name: str, legacy: Path | None = None, default: Any = None) -> Any:
    values = _cache_rows(path, cache_name)
    if values:
        return values.get("value", default)
    if legacy and legacy.is_file():
        try:
            value = json.loads(legacy.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return default
        write_cache(path, cache_name, value)
        return value
    return default


def write_cache(path: Path, cache_name: str, value: Any) -> None:
    ensure_schema(path)
    connection = connect_database(path)
    try:
        connection.execute(
            "insert into business_cache(cache_name,cache_key,value_json,updated_at) values(?,?,?,?) "
            "on conflict(cache_name,cache_key) do update set value_json=excluded.value_json, updated_at=excluded.updated_at",
            (cache_name, "value", json.dumps(value, ensure_ascii=False, sort_keys=True), _now()),
        )
        connection.commit()
    finally:
        connection.close()
