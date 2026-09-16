# PP FlowHub 数据模型与边界

## 系统边界

AIHouse 是设计源，AIMES 是拆单排产源，AICNC 报表是生产源，金蝶是库存余额源。PP FlowHub 只做汇总、查询、人工修正、同步证据和状态管理，不把 Traveler 当作生产事实。

当前完整操作端运行在 Mac；中央数据库先放在 Mac 本地。未来 Windows Server 运行后端服务时，SQLite 仍只放在 Windows 本机磁盘，Mac App 和只读网页通过 API 访问，不直接打开 SMB/UNC 上的 SQLite 文件。

## 中央 SQLite

正式业务数据库：`~/Documents/pp-flowhub/data/workflow.sqlite3`。

主要表按职责分组：订单索引与同步证据、`production_batches`/`batch_evidence` 批次、`material_items` 材料、`hardware_items` 五金、`outbound_documents` 出库单据、`products` 商品主资料、`backup_records` 备份记录。`products` 保存 SKU、原始名称/规格/单位、商品成本 `cost_price`，以及工作流使用的 `material_kind`、`material_color`、`material_thickness`；库存商品资料没有预计采购价时，`cost_price` 为 `NULL`。原始商品规格不改写：例如 `M0002`、`M0003` 的外部规格仍可为 5.2、15，而工作流名义厚度分别保存为 5.4、14.5。

订单材料、已完成生产材料和 Server 材料分配分别保存在 `material_items`、`manual_production_batch_materials`、`server_material_allocations`。三张表只保存 SKU、数量及各自必要的订单/批次/来源身份，不重复保存材料类型、颜色、厚度、单位或 `edge`；详情、生产、库存、成本和 Traveler 在读取时按 `product_code` 连接 `products` 投影这些属性。生产累计消耗也按 SKU 汇总，商品单位文字变化不能使已完成数量重新变成可用数量。

`material_items`、`manual_production_batch_materials`、`server_material_allocations`、`hardware_items` 和 `inventory_resolution_rules` 的 `product_code` 都声明到 `products(code)` 的外键；前四张事实表的新行必须有 SKU，映射规则必须有 SKU，忽略规则则必须为 `NULL`。SQLite 外键是每条连接的运行时开关，参与这五张表写入/事务的应用连接必须在事务开始前启用 `PRAGMA foreign_keys=ON`；已经进入事务后再执行不会补上本次约束。

AICNC 五金和人工五金在同一张表中，用 `source_type` 区分；`hardware_items.product_code` 是规范库存 SKU，`name`、`source_code`、`spec` 和 `unit` 继续保留来源证据。AICNC 重同步只替换 AICNC 来源，不会覆盖 `manual`。

原始 Excel、XML、CSV 不复制进数据库，数据库保存路径、指纹、解析结果和同步时间。设置、待办、操作审计仍使用 JSON/JSONL，因为它们不是订单业务事实。

## 优化状态与文件基线

`material_items` 中已校验并确认写入的有效材料是完成优化的前提；`factory_orders.optimized` 只标记本次已确认材料覆盖的工厂单，订单状态按有效工厂单汇总。仅有 `optimization_artifacts` 不能把订单推进为已优化。

普通 Server 扫描不写 `optimization_artifacts`、工厂单优化时间或 `server_scan_xml_state`；磁盘扫描快照也不保留优化 XML 条目。内存预览可暂存这些记录，取消后不落入正式库。确认事务同时写材料、所选工厂单状态与其优化元数据；文件夹仍有未完成确认的工厂单时，不推进整个文件夹的 XML 基线。失败整体回滚。

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
