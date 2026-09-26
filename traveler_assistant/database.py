"""中央工作流数据库及安全迁移辅助能力。

应用用一个本地 SQLite 文件保存业务事实；AIHouse、AIMES、AICNC 和金蝶来源仍在外部。
本模块保存看板所需的标准化事实、来源证据及用户修正。
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
    """在事务开始前启用连接 connection 的外键约束并返回该连接。

    SQLite 会忽略事务内启用外键的请求；若调用方过早开启事务则报错，避免共享连接看似受保护。"""
    enabled = int(connection.execute("pragma foreign_keys").fetchone()[0])
    if enabled:
        return connection
    if connection.in_transaction:
        raise RuntimeError("必须在事务开始前启用 SQLite foreign_keys")
    connection.execute("pragma foreign_keys=on")
    if int(connection.execute("pragma foreign_keys").fetchone()[0]) != 1:
        raise RuntimeError("无法启用 SQLite foreign_keys")
    return connection


def prepare_pending_session(connection: sqlite3.Connection) -> None:
    """创建仅属于连接的检查结果表；不迁移、读取或清理磁盘上的历史问题。"""
    connection.execute("""create temp table if not exists pending_issues(
        issue_key text primary key, kind text not null, order_id text not null default '',
        factory_order text not null default '', path text not null default '', message text not null,
        status text not null default 'open', first_seen text not null, last_seen text not null,
        resolved_at text not null default '')""")
    connection.execute("""create temp table if not exists pending_aimes_reviews(
        ignore_key text primary key, factory_order text not null, factory_name text not null default '',
        sales_order_name text not null default '', reason text not null default '',
        suggested_order_id text not null default '', split_time text not null default '',
        last_seen text not null)""")


def connect_database(path: Path, **kwargs: Any) -> sqlite3.Connection:
    """打开启用外键的 SQLite 连接；path 为数据库路径，kwargs 透传给 sqlite3.connect。"""
    connection = enable_foreign_keys(sqlite3.connect(path, **kwargs))
    prepare_pending_session(connection)
    return connection


def database_path(state_dir: Path) -> Path:
    """返回状态目录 state_dir 中唯一的中央业务数据库路径。"""
    return state_dir / "workflow.sqlite3"


def _now() -> str:
    """返回带本地时区、精确到秒的当前时间字符串；无参数。"""
    return datetime.now().astimezone().isoformat(timespec="seconds")


_OUTBOUND_FACTORY_SPLIT_RE = re.compile(r"[,，;；、|]+")
_PRODUCT_KEY_RE = re.compile(r"[\s_-]+")
_NUMBER_RE = re.compile(r"\d+(?:\.\d+)?")
_PLYWOOD_NOMINAL_THICKNESS = {
    "M0002": "5.4",
    "M0003": "14.5",
    "M0004": "18",
}
_SCHEMA_READY_MARKER = "ensure_schema_production_simplification_v1"


def _product_key(value: object) -> str:
    """移除 value 中的空白、下划线及连字符并转为大写，生成商品比较键。"""
    return _PRODUCT_KEY_RE.sub("", str(value or "")).upper()


def catalog_material_attributes(
    category: object, name: object, spec: object, code: object = "",
) -> tuple[str, str, str]:
    """从商品目录推导材料类型、颜色和厚度，不改动原始字段。

    参数：category 为类别；name 为名称；spec 为规格；code 为可选 SKU。
    夹板的业务标称厚度与供应商规格中的实际厚度分别保留。"""
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
            # 商品规格先写厚度（如 3/4 Board），后面还可能出现宽长分数（如 110-1/4）。
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
    """重建旧材料的匹配名称；material_type 为材料类型，color 为颜色，thickness 为厚度。"""
    kind = str(material_type or "").strip().casefold()
    color_text = str(color or "").strip()
    thickness_text = str(thickness or "").strip()
    if kind == "edge":
        return f"Edge banding--{color_text}"
    if kind == "plywood":
        return f"{float(thickness_text):g}mm--Plywood"
    return f"{float(thickness_text):g}mm--{color_text}"


def server_material_identity_key(source_path: object, product_code: object) -> str:
    """生成来源材料的稳定 v3 标识；source_path 为来源路径，product_code 为已确认 SKU。"""
    payload = "\x1f".join((
        str(source_path or "").strip().casefold(),
        str(product_code or "").strip().upper(),
    ))
    return "v3:" + hashlib.sha256(payload.encode()).hexdigest()


def _has_product_foreign_key(connection: sqlite3.Connection, table: str) -> bool:
    """检查 table 的 product_code 是否关联 products.code 且限制删除；connection 为数据库连接。"""
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
    """复用现行匹配规则解析旧材料 SKU，并返回诊断候选列表。

    参数：connection 为迁移事务连接；material_type、color、thickness 为旧材料类型、颜色和厚度。"""
    try:
        display_name = _legacy_material_name(material_type, color, thickness)
    except (TypeError, ValueError):
        return "", []

    # 复用运行时的权威材料匹配器；适配器使用当前迁移事务，避免另开连接被锁，
    # 也避免在迁移中维护另一套夹板、饰面板及封边别名。
    from .core import RuleError
    from .inventory import InventoryMappings, Product, TravelerItem, match_item

    class _MigrationCatalog:
        @staticmethod
        def _product(row: tuple) -> Product:
            """将数据库查询行 row 转为商品对象，保留缺失价格为 None。"""
            return Product(
                category=str(row[0] or ""), code=str(row[1] or ""),
                name=str(row[2] or ""), spec=str(row[3] or ""),
                status=str(row[4] or ""), brand=str(row[5] or ""),
                remark=str(row[6] or ""), unit=str(row[7] or ""),
                cost_price=None if row[8] is None else float(row[8]),
            )

        def require_code(self, code: str) -> Product:
            """在当前迁移事务中按 code 查询唯一可用商品；未匹配、多匹配或停用时抛出业务错误。"""
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
            """在当前迁移事务中筛选商品。

            参数：category 为类别；name 为完整名称；contains 为名称或备注包含词；spec_thickness 为厚度条件。"""
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
    """按常见中英文分隔符拆分工厂单字段 value，忽略空项。"""
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
    """依据出库单和本地归属解析明确的工厂单候选，不用生产消耗推断出货。

    参数：connection 为连接；document_number 为单据号；order_id 为订单号；factory_value 为原工厂单字段。"""
    document_number = str(document_number or "").strip()
    order_id = str(order_id or "").strip().upper()
    if not document_number or not order_id:
        return set()
    # 生产消耗不能证明工厂单已出货，启动时补齐旧单据关联也遵守此规则。
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
    # 独立出库台账可能没有订单索引表，无法解析工厂单身份；此时单据主行仍是有效的持久出库事实。
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
    """为出库单补充精确工厂单关联，返回新增关联数。

    参数：connection 为连接；document_number 为单据号；order_id 为订单号；factory_value 为原关联字段；
    updated_at 为可选记录时间。单据表保留一单一行，关联表表达多工厂单；仅有订单号时，
    只有唯一有效工厂单才能推导关联，分单场景必须提供明确身份。"""
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
    """逐条执行结构脚本，保留调用方的事务边界。

    参数：connection 为事务连接；script 为 SQL 脚本。避免 executescript 隐式提交已有事务，
    使建表、加列、复制数据和清理可以一起回滚；不完整语句会报错。"""
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


def _simplify_production_schema(connection: sqlite3.Connection) -> None:
    """通过事务连接 connection 迁移已确认生产记录、材料及工厂单关联，不推断新增数量。"""
    connection.execute('''create table if not exists production_records(
        batch_id integer primary key,
        production_time text not null default '',
        source text not null default 'manual',
        status text not null default 'completed',
        created_at text not null,
        updated_at text not null
    )''')
    connection.execute('''create table if not exists production_materials(
        batch_id integer not null references production_records(batch_id),
        order_id text not null,
        product_code text not null check(trim(product_code)<>''),
        quantity real not null check(quantity>=0),
        primary key(batch_id,order_id,product_code),
        foreign key(product_code) references products(code) on update cascade on delete restrict
    )''')
    links = connection.execute('select batch_id,order_id,factory_order from manual_production_batch_factories').fetchall()
    if len({r[2] for r in links}) != len(links):
        raise ValueError('生产迁移失败：一个工厂单存在多次生产记录，需先核对')
    factory_exists = connection.execute("select 1 from sqlite_master where type='table' and name='factory_orders'").fetchone()
    if links and not factory_exists:
        raise ValueError('生产迁移失败：缺少工厂单表')
    if factory_exists:
        columns = {r[1] for r in connection.execute('pragma table_info(factory_orders)')}
        if 'production_record_id' not in columns:
            connection.execute('alter table factory_orders add column production_record_id integer references production_records(batch_id)')
        for batch_id, order_id, factory in links:
            row = connection.execute('select order_id,production_record_id from factory_orders where factory_order=?',(factory,)).fetchone()
            if row is None or row[0] != order_id or row[1] not in (None,batch_id):
                raise ValueError(f'生产迁移失败：工厂单关联不一致 {factory}')
        if 'production_batch_id' in columns:
            connection.execute('alter table factory_orders drop column production_batch_id')
    connection.execute('''insert into production_records(batch_id,production_time,source,status,created_at,updated_at)
        select batch_id,production_time,source,status,created_at,updated_at from manual_production_batches''')
    connection.execute('''insert into production_materials(batch_id,order_id,product_code,quantity)
        select batch_id,order_id,product_code,quantity from manual_production_batch_materials''')
    for batch_id, order_id, factory in links:
        connection.execute('update factory_orders set production_record_id=? where factory_order=? and order_id=?',(batch_id,factory,order_id))
    if factory_exists:
        columns = {r[1] for r in connection.execute('pragma table_info(factory_orders)')}
        if 'stage' not in columns:
            connection.execute("alter table factory_orders add column stage text not null default '已拆单' check(stage in ('已拆单','已优化','已生产','已出货'))")
            shipped = "outbound_status" if "outbound_status" in columns else "'未出库'"
            optimized = "optimized" if "optimized" in columns else "0"
            connection.execute(f"""update factory_orders set stage=case
                when {shipped}='已出库' then '已出货'
                when exists(select 1 from production_records r where r.batch_id=production_record_id and r.status='completed') then '已生产'
                when {optimized}=1 then '已优化' else '已拆单' end""")
        for column in ('optimized','outbound_status'):
            if column in columns:
                connection.execute(f'alter table factory_orders drop column {column}')
    for table in ('manual_production_batch_factories','manual_production_batch_materials','manual_production_batches','batch_evidence','production_batches'):
        connection.execute(f'drop table if exists {table}')
    connection.execute('create index if not exists idx_production_material_order on production_materials(order_id,product_code)')
    if connection.execute("select 1 from sqlite_master where type='table' and name='orders'").fetchone():
        columns = {r[1] for r in connection.execute('pragma table_info(orders)')}
        for column in ('material_status','validation_status','validation_message'):
            if column in columns:
                connection.execute(f'alter table orders drop column {column}')

    if connection.execute("select 1 from sqlite_master where type='table' and name='source_files'").fetchone():
        if 'batch_number' in {r[1] for r in connection.execute('pragma table_info(source_files)')}:
            connection.execute('alter table source_files drop column batch_number')
    if connection.execute("select 1 from sqlite_master where type='table' and name='active_issues'").fetchone():
        connection.execute("delete from active_issues where kind='batch_conflict'")


def ensure_schema(path: Path) -> None:
    """检查或升级 path 指向的中央数据库结构；升级前保留备份，当前结构只补必要的缺失关联。"""
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
            # 当前结构的普通读取不应仅为重复检查就取得写锁；初始化后仍可能插入旧格式合并单据，
            # 因此只修补确实缺少标准化工厂单关联的单据。
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
        # 升级前保存独立于每日轮转策略的可恢复快照；成功前不修改业务行。
        if connection.execute("select 1 from sqlite_master where type='table' and name='manual_production_batches'").fetchone():
            backup_directory = path.parent / "schema-migration-backups"
            backup_directory.mkdir(parents=True, exist_ok=True)
            stamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
            backup_path = backup_directory / f"{path.stem}-before-production-v1-{stamp}.sqlite3"
            backup = sqlite3.connect(backup_path)
            try:
                connection.backup(backup)
                if backup.execute("pragma integrity_check").fetchone() != ("ok",):
                    raise ValueError("结构迁移前备份完整性检查失败")
            finally:
                backup.close()
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
                quantity real not null default 0,
                source_type text not null default 'aicnc',
                source_path text not null default '',
                remarks text not null default '',
                updated_at text not null,
                foreign key(product_code) references products(code)
                    on update cascade on delete restrict
            );
            create index if not exists idx_hardware_items_order on hardware_items(order_id, factory_order);
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
        if "active" in hardware_columns:
            # 与结构迁移共用事务，删表失败时也恢复已删除行；这里只识别人工删除标记。
            unexpected = connection.execute(
                "select count(*) from hardware_items where active<>1 and source_type<>'manual'"
            ).fetchone()[0]
            if unexpected:
                raise ValueError("存在失效的自动五金，请先核对来源后再迁移")
            connection.execute("delete from hardware_items where active<>1")
            connection.execute("drop index if exists idx_hardware_items_order")
            connection.execute("alter table hardware_items drop column active")
            connection.execute(
                "create index idx_hardware_items_order on hardware_items(order_id,factory_order)"
            )
        retired_hardware_columns = {"source_code", "name", "spec", "unit"} & hardware_columns
        if retired_hardware_columns:
            # 持久事实中的数量已标准化；迁移时不可再次合并导轨或执行支数转对数。
            for column in sorted(retired_hardware_columns):
                connection.execute(f"alter table hardware_items drop column {column}")
            from .hardware_facts import hardware_fingerprint
            for factory, in connection.execute("select factory_order from hardware_source_versions").fetchall():
                rows = [dict(zip(("order_id", "factory_order", "product_code", "quantity"), row))
                        for row in connection.execute(
                            "select order_id,factory_order,product_code,quantity from hardware_items "
                            "where factory_order=? and source_type='aicnc'", (factory,)).fetchall()]
                connection.execute("update hardware_source_versions set fingerprint=? where factory_order=?",
                                   (hardware_fingerprint(rows), factory))
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
            # 部分开发库可能同时保留 product_code 和旧描述列；收敛为仅以 SKU 标识的结构，不改批次数量。
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
                       quantity real not null default 0,
                       source_type text not null default 'aicnc',
                       source_path text not null default '',
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
                "create index idx_hardware_items_order on hardware_items(order_id,factory_order)"
            )

        connection.execute("""create trigger if not exists protect_hardware_product_unit
            before update of unit on products
            when new.unit <> old.unit and exists (
                select 1 from hardware_items where product_code=old.code
            )
            begin select raise(abort, 'hardware_product_unit_locked'); end""")

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
                        # 两个独立命令可能同时初始化新目录；另一个事务可能在读取结构后先添加该列，
                        # 这是并发初始化已成功，不是结构失败。
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
        _simplify_production_schema(connection)
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
    """每单只保留最早实际安装日期及该行安装人员，并建立唯一约束。

    参数：connection 为数据库连接。保留原日期类型表结构以兼容计划日期，返回删除行数。"""
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
    """标准化库存规则名称 value，去除空白、下划线及连字符并转大写。"""
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
    """将 state_dir 中的旧映射 JSON 一次性迁入中央库，事务提交后才归档原文件。

    归档只用于恢复切换前配置，运行时不再使用归档文件。"""
    central = database_path(state_dir)
    ensure_schema(central)
    source = state_dir / "inventory" / "mappings.json"
    connection = connect_database(central)
    try:
        # App 多个后台任务可能同时准备存储；串行执行一次性迁移，避免都读到缺失标记后争用元数据主键。
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

    # 旧库合并可能在首次结构检查后创建旧版工厂单表；再执行一次轻量迁移，
    # 使 OrderIndexStore 打开前的直接详情读取也能使用当前结构。
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
    """复制来源表结构及全部数据，会重建目标同名表。

    参数：source 为来源连接；target 为目标连接；table 为表名。来源表不存在时返回 False。"""
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
    """将 state_dir 中的旧本地事实幂等合并到中央库，提交后才把原文件移入带时间戳的归档。"""
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
                    # 保留已有中央表；依据稳定主键使用 INSERT OR IGNORE 合并记录。
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
                            # 新中央结构可能已移除历史列；原始来源仍保留在归档中。
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
    """读取指定缓存的全部键值并解码 JSON；path 为数据库路径，cache_name 为缓存名称。"""
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
    """读取已有业务缓存，必要时导入旧 JSON。

    参数：path 为数据库路径；cache_name 为缓存名称；legacy 为可选旧文件；default 为缺失或读取失败的默认值。"""
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
    """保存已有业务缓存并提交；path 为数据库路径，cache_name 为缓存名称，value 为可序列化的值。"""
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
