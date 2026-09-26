# PP FlowHub 数据模型与边界

## 系统边界

AIHouse 是设计源，AIMES 是拆单排产源，AICNC 报表是生产源，金蝶是库存余额源。PP FlowHub 只做汇总、查询、人工修正、同步证据和状态管理，不把 Traveler 当作生产事实。

当前完整操作端运行在 Mac；中央数据库先放在 Mac 本地。未来 Windows Server 运行后端服务时，SQLite 仍只放在 Windows 本机磁盘，Mac App 和只读网页通过 API 访问，不直接打开 SMB/UNC 上的 SQLite 文件。

## 中央 SQLite

正式业务数据库：`~/Documents/pp-flowhub/data/workflow.sqlite3`。

主要表按职责分组：订单索引与同步证据、`production_records` 实际生产记录、`material_items` 材料、`hardware_items` 五金、`outbound_documents` 出库单据、`products` 商品主资料、`backup_records` 备份记录。`products` 保存 SKU、原始名称/规格/单位、商品成本 `cost_price`，以及工作流使用的 `material_kind`、`material_color`、`material_thickness`；库存商品资料没有预计采购价时，`cost_price` 为 `NULL`。原始商品规格不改写：例如 `M0002`、`M0003` 的外部规格仍可为 5.2、15，而工作流名义厚度分别保存为 5.4、14.5。

订单材料、已完成生产材料和 Server 材料分配分别保存在 `material_items`、`production_materials`、`server_material_allocations`。三张表只保存 SKU、数量及各自必要的订单/批次/来源身份，不重复保存材料类型、颜色、厚度、单位或 `edge`；详情、生产、库存、成本和 Traveler 在读取时按 `product_code` 连接 `products` 投影这些属性。生产累计消耗也按 SKU 汇总，商品单位文字变化不能使已完成数量重新变成可用数量。

`material_items`、`production_materials`、`server_material_allocations`、`hardware_items` 和 `inventory_resolution_rules` 的 `product_code` 都声明到 `products(code)` 的外键；前四张事实表的新行必须有 SKU，映射规则必须有 SKU，忽略规则则必须为 `NULL`。SQLite 外键是每条连接的运行时开关，参与这五张表写入/事务的应用连接必须在事务开始前启用 `PRAGMA foreign_keys=ON`；已经进入事务后再执行不会补上本次约束。

AICNC 五金和人工五金在同一张表中，用 `source_type` 区分；`hardware_items.product_code` 是规范库存 SKU；名称、规格、单位连接 `products` 读取，不再复制来源代码与属性。AICNC 重同步只替换 AICNC 来源，不会覆盖 `manual`。

原始 Excel、XML、CSV 不复制进数据库，数据库保存路径、指纹、解析结果和同步时间。设置、待办、操作审计仍使用 JSON/JSONL，因为它们不是订单业务事实。

## 新版优化台账（显式批准迁移后启用）

普通启动不创建新版表。`tools/migrate_aicnc_import.py` 默认只读列出范围，明确批准后使用 `--apply --backup-dir …` 做 SQLite 在线备份，再原子添加以下四张表。原有表、字段、索引及业务数据不重建、不删除。

| 表 | 字段与约束 | 用途 |
| --- | --- | --- |
| `aicnc_import_settings` | `key` 主键、`value` 非空 | 启用时间与清理提醒关闭标记 |
| `aicnc_optimizations` | `optimization_id` 主键；`source_folder`、`status`、`plan_json`、`created_at`、`completed_at`；状态限 processing/completed/ignored | 优化编号去重、确认快照、外部恢复；已处理后不读文件 |
| `aicnc_material_allocations` | 联合主键：优化编号＋订单＋用途＋SKU；非负 `quantity`；用途 normal/rework；优化编号及 SKU 外键 | 混单及正常/返工的分配来源 |
| `aicnc_legacy_watch` | `path` 主键、`files_json`、`retired_at` | 切换时旧范围与原文件清单证据；退出后不再激活 |

确认后材料写入既有 `material_items`，`source_type=aicnc_optimization`，实际来源目录保存在 `source_path`；完整原报表数量、工厂单身份及人工决策留在 `plan_json`。正常工厂单优化时间来自 AICNC 编号，记录到 `optimization_artifacts`。返工生产记录使用 `production_records.source=aicnc_rework`，只有材料消耗，不重新关联工厂单；补单使用 `outbound_documents.document_type=rework_materials`，不建立出货工厂单关联。库存操作日志使用 `aicnc_rework`，保存唯一备注、明细和返回单据号。

新分配表的 SKU 外键为更新级联、删除限制；普通生产累计出库排除已经独立扣库的返工消耗，订单总消耗仍包含返工。迁移验证原表逐行一致、完整性及外键；回滚须先停止 App，再恢复迁移前数据库和原 App，保留迁移后的库供核对。

## 优化状态与文件基线（文件基线部分仅适用于旧范围）

`material_items` 中已校验并确认写入的有效材料是完成优化的前提；`factory_orders.stage` 只将本次已确认材料覆盖且尚未生产/出货的工厂单推进为已优化，订单状态按有效工厂单汇总。仅有 `optimization_artifacts` 不能把订单推进为已优化。

`orders.stage = 已中止` 是二次确认的人工终态，优先于工厂单进度聚合；普通 upsert、列表重算及临时投影清理均保留此决定。中止只更新订单状态和更新时间，已有工厂单、材料、生产与出库事实不改动。命令为 `abort-order --order-id … --confirm-write`，无新增 schema 字段。

普通 Server 扫描不写 `optimization_artifacts`、工厂单优化时间或 `server_scan_xml_state`；磁盘扫描快照也不保留优化 XML 条目。内存预览可暂存这些记录，取消后不落入正式库。确认事务同时写材料、所选工厂单状态与其优化元数据；文件夹仍有未完成确认的工厂单时，不推进整个文件夹的 XML 基线。失败整体回滚。

对已有有效材料确认、材料/五金/工厂单均无差异的预览，专用 `acknowledge-server-preview-memory` 事务只替换 `server_scan_xml_state`，不写优化证据或业务表。事务内比较预览时的本地业务版本并检查文件夹确认条件；本地事实变化则拒绝，失败整体回滚。

XML 基线来自用户确认的预览版本，不在确认时重新读取最新文件来覆盖；这样预览后发生的修改仍会被下次扫描发现。已存在的历史扫描日志保留用于审计，不作为确认材料的证据。独立人工文件夹仍按下述人工登记规则维护观察基线。

## 独立文件夹人工任务

`temporary_orders` 按文件夹内部身份及来源路径保存普通临时任务和补单。`handling_mode` 区分 `supplemental`（已识别、待人工处理）与 `external_manual`（已确认采用外部人工处理）；`reference_order_ids` 是可空的 JSON 数组，不是正式订单外键。没有参考订单也能完成登记。

新增字段通过 `OrderIndexStore` 的增量 `ALTER TABLE` 补齐，保留已有台账和真实数据库。旧“已人工处理”记录继续采用独立人工路径，不要求重建或重新出库。

`processing_status`、`outbound_status`、`outbound_at`、可选 `outbound_document` 保存本次用户确认；扫描状态由 `watching` 转为 `manual_pending`（观察期发现 XML 变化）或 `permanent`（到期无变化）。已发现的待处理内容不能因旧观察期限到期而消失。重复确认原内容只更新用户参考信息，不延长完成时间和观察期；历次完成通过 `sync_changes` 保留操作证据。

人工登记是一个 SQLite 事务，只保存文件夹台账、基线和相关问题的处理结果，失败整体回滚；不调用库存系统、不更新正式订单汇总。

## 迁移与备份

首次准备存储时，旧订单索引和业务缓存合并到中央数据库；商品主资料直接写入中央数据库，不再读取旧库存数据库。旧订单索引成功迁移后只读归档到 `migration-archives/`，不自动删除。数据库备份写入本机 `data/database-backups/`：App 每个自然日首次启动、完成本地订单缓存读取后自动执行一次；保留今天及前两个自然日的每日备份，并在滚动 30 天内每个自然周保留最新一份，其他文件删除。Traveler 文件备份目录与数据库备份目录分开管理。

旧材料属性结构升级时，先在同一事务内把每条旧材料、生产消耗和 Server 分配唯一解析为商品 SKU，再重建最终表形状；任一行缺少唯一匹配、五金/映射出现孤儿 SKU 或完整性检查失败时整体回滚并列出诊断，不能留下部分迁移。正式数据库迁移前还要创建可恢复备份，并在副本演练和正式迁移后分别检查行数、数量汇总、`foreign_key_check` 与关键订单读层。

商品目录更新不删除整张 `products` 表。当前导出中的 SKU 按编号更新或插入；本次目录缺少的旧 SKU 保留原行并标为 `catalog_present=0`，让历史材料、生产和详情仍可追溯，但不能用于新的映射、材料确认或库存写入。只要订单材料、生产消耗或 Server 分配任一表仍引用某 SKU，它的结构化材料属性就不能因后续名称映射改变而静默重绑。

## Traveler

Traveler 只按需从数据库和当前源文件生成到系统临时目录，用于查看或打印，使用后不写入订单目录。生产事实仍来自 AIMES、AICNC 和金蝶；历史详情依赖中央数据库保存的解析结果。

## 五金直接删除与来源字段（2026-09-17）

`hardware_items` 只保存当前五金行，不再有 `active` 字段。人工五金删除在确认保存的同一事务中执行 `DELETE`，新增或约束失败时整体回滚；迁移清理旧人工失效行并移除字段、更新索引，保留有效行的 ID、数量和其余字段。发现失效的自动来源时拒绝自动迁移，避免猜测其业务含义。工厂单自身的 AIMES/出库状态仍独立保留，已出库或失效工厂单禁止编辑人工五金。

SKU（`product_code`）是唯一商品身份。人工和自动五金均移除 `source_code/name/spec/unit`；保留数量、订单/工厂单、来源类型、文件定位、备注和时间。所有新写入在替换前校验有效商品 SKU，未映射或无效商品整体回滚；不从已确认事实反向恢复或重新映射报表。商品名称与规格读取当前资料，已被五金引用的商品单位由目录更新校验和 SQLite trigger 保护，避免改变数量含义。

迁移逐行保留已有 SKU、数量、ID 和归属，绝不再次执行报表换算。自动来源指纹按订单、工厂单和 SKU 汇总数量；迁移在同一事务中重算已有来源版本指纹，其他来源版本字段和出库单据不变。正式升级先做 SQLite Online Backup，在副本核对保留字段、其他业务表、完整性和外键；失败整体回滚。

## 生产与状态精简（2026-09-18）

正式订单移除 `validation_status`、`validation_message`、`material_status`。导入校验在本次连接的 `TEMP preview_validation` 中保留，连接关闭即消失，预览 payload 携带结果；确认仍检查结果、SKU、数量和归属。TEMP 对象不是正式 schema 或新的业务表；列表材料说明从明细计算。订单 `stage` 由同一汇总逻辑从有效工厂单计算，不能被一次导入失败覆盖。

工厂单仅用 `stage` 保存主流程：已拆单、已优化、已生产、已出货。保留 AIMES 有效性、归属、文件证据、时间及单据，因它们不是同一进度。API 的 `optimized`、`outbound_status` 是旧界面所需的读层投影，不再是持久列；历史已出货可跳过缺失的早期证据，不补造优化时间或材料。

`production_records(batch_id, production_time, source, status, created_at, updated_at)` 不绑定单一订单、不保存 MP 编号。`factory_orders.production_record_id` 外键直接关联记录，一个工厂单最多一次；原 `manual_production_batch_factories` 移除。`production_materials` 主键为 `(batch_id, order_id, product_code)`，可保存跨订单同 SKU，不能将订单材料强行分摊给各工厂单。现有 App 的生产选择入口仍以当前订单为上下文，跨订单共享记录的存储/事务合同已支持，不代表新增了跨订单批量库存操作界面。

`production_batches`、`batch_evidence`、`factory_orders.production_batch_id`、`source_files.batch_number` 移除；文件路径、指纹、优化元数据和分配表仍保留。旧唯一来源批次冲突已不适用。

迁移保留生产记录 ID、历史空时间、来源、状态、材料数量及工厂单归属；重复关联或孤儿身份拒绝迁移并回滚。历史 `CS002/M0041` 的 manual 板材事实保留，不因当前仅允许人工五金而删除。首次升级在 `data/schema-migration-backups/` 创建 SQLite Online Backup 并校验完整性，成功后才开始结构迁移事务；原业务表及删除字段可从该备份追溯。

## 订单筛选与内部初始值（2026-09-18）

订单中心不再提供已设计、待人工处理、待确认、数据异常四个筛选项。菜单选项不作为数据库枚举约束；`orders.stage` 仍保留未关联工厂单时的内部初始值及既有迁移，列表按有效工厂单汇总显示。当前库只读核对四类订单均为零，本次不改 schema、不更新或删除订单。归属确认、临时任务及校验结果各自保留。

### 临时文件夹永久忽略

`server_folder_ignores(path PRIMARY KEY, ignored_at)` 保存用户明确确认的文件夹忽略决定。`path` 使用配置的 Server 根目录路径形式，不关联出库或订单状态，没有观察期限/指纹字段。重复请求保留首次时间；记录、操作日志与路径内问题关闭在同一事务中提交。自动扫描、自动同步及扫描快照复用均先排除忽略路径；旧 `ignored_server_folders` 的月度观察表仍按历史迁移移除，不复用旧含义。


### 五金人工处理版本合同（2026-09-21）

不新增表/字段/索引。`hardware_source_decisions.decision_json` 在既有 selected/observed_contents 基础上支持 `handling: manual`、`report_versions: {报表路径: SHA-256}`；对应 `hardware_source_versions` 保留空投影指纹及 row_count=0。人工决定、空投影版本、自动五金清理及索引版本在确认事务中写入，手工五金与生产/出货事实不变。变版来源需重新确认，不能将旧 manual 标志带入新来源决定。维护审计比较本地索引版本；实时文件变化由报表读取/预览识别。

### 当前检查结果与恢复记录（2026-09-24）

`pending_issues`、`pending_aimes_reviews` 是 SQLite 连接内的 TEMP 表，不存在于磁盘主库 schema。常驻订单服务在会话内共享；一次性命令只在该命令及其嵌套调用期间共享。连接关闭后结果丢弃。历史主库 `active_issues` 和 `aimes_review_rows` 保留，不参与当前待办投影，不执行删表或清空迁移。订单详情不读取历史问题。

`inventory_operations` 保持原有结构；`submitting`、`verification_required`、`external_confirmed`、`partial_external_confirmed` 投影为库存恢复项，`local_committed` 不再显示。原有 `payload_json` 内附带来源上下文，原始 documents 和 production_draft 用于恢复；来源上下文不参与操作幂等身份。外部返回先保存操作结果，再提交本地业务事务，关闭程序后仍可核对。普通检查结果不能代替外部操作记录，也不能修改历史出库事实。

### 零材料消耗生产（2026-09-24）

不新增或改变任何数据库结构。使用现有 `production_records` 保存生产时间，`factory_orders.production_record_id` 关联所选工厂单；本次全零时不新增 `production_materials`，原订单材料与历史消耗不变。没有生产方式或原因字段，事务与生产一次性约束沿用现有实现。实施状态见 [零消耗生产计划](../plans/remainder-production.md)。
