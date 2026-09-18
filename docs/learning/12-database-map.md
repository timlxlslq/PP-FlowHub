# 数据库地图：当前文件、角色与 SKU 关系

这份地图只介绍当前应用真正使用的两个 SQLite 文件、SKU 关系，以及如何安全核对实际 schema。它是静态学习资料，不会自动打开、查询或写入数据库。

## 两个正式运行库

| 文件 | 角色 |
| --- | --- |
| `data/workflow.sqlite3` | 中央订单、商品、材料、五金、生产、库存出库和同步事实 |
| `data/assistant-runtime.sqlite3` | Agent 用量与已学习命令 |

中央库路径由 [`core.py`](../../traveler_assistant/core.py) 的 `Config.workflow_database` 提供；schema 初始化由 [`database.py`](../../traveler_assistant/database.py) 的 `ensure_schema`、[`order_index.py`](../../traveler_assistant/order_index.py) 的 `OrderIndexStore` 和库存商品初始化共同负责。助手运行库路径由 [`runtime_store.py`](../../traveler_assistant/runtime_store.py) 返回。

## 快速入口

| 需要查什么 | 入口 |
| --- | --- |
| 2026-09-12 迁移前两个运行库的完整字段快照 | [`database-map/current-schema.md`](database-map/current-schema.md)（历史参考，不能当作 SKU 迁移后的现行 schema） |
| 连接、事务、路径、共享连接和外部数据隔离的学习说明 | [`11-database-guide.md`](11-database-guide.md) |

## 表的业务分层

订单与工厂单由 `orders`、`factory_orders` 保存；Server/AIMES 扫描、同步异常和来源文件由 `source_files`、`sync_runs`、`sync_changes`、`active_issues` 等表保存。订单材料进入 `material_items`，工厂单五金进入 `hardware_items`；`production_records`、`production_materials` 记录实际生产及订单材料消耗，不能把生产材料消耗当成工厂单已出货。

商品主数据在 `products`：原始 `name/spec/category/unit` 保留库存目录证据，`material_kind/material_color/material_thickness` 是工作流读取的结构化材料属性，`catalog_present` 表示 SKU 是否仍出现在最新目录。名称到 SKU 的决定在 `inventory_resolution_rules`；mapping 行引用商品，ignore 行没有 SKU。

`material_items`、`production_materials` 和 `server_material_allocations` 都只保存 SKU、数量和各自必要身份；属性在读取时 JOIN `products`。`hardware_items` 同样只保存 SKU、数量与必要归属/来源身份，名称、规格和单位从商品表读取。库存成功单据在 `outbound_documents`，明确工厂单覆盖关系在 `outbound_document_factories`，出库范围人工决定在 `outbound_scope_decisions`。`inventory_operations` 只记录浏览器/库存操作意图、重试状态和结果，属于操作元数据，不等于出库事实。

`workflow_metadata` 和 `business_cache` 保存迁移标记、缓存值及更新时间；它们不是订单或库存事实。Server 预览使用工作副本和恢复材料。旧字段字典是迁移前快照，现行字段应从当前源码和已完成升级的隔离数据库核对。

## 如何按表查字段

1. 先在 `database.py` 和负责该表的模块中查看当前 `CREATE TABLE`、迁移和读写 SQL。
2. 对完成升级的隔离数据库运行 `PRAGMA table_info`、`index_list`/`index_info`、`foreign_key_list`，再执行 `PRAGMA foreign_key_check`；这些命令只读 schema/完整性，不需要读取业务行内容。
3. 五张 SKU 引用表应看到到 `products(code)` 的外键：`material_items`、`production_materials`、`server_material_allocations`、`hardware_items`、`inventory_resolution_rules`。参与这些表写入/事务的应用连接还必须在事务开始前确认 `PRAGMA foreign_keys=1`。
4. `order_id`、`factory_order` 等没有声明外键的字段仍按应用层关联理解。对 `TEXT` 状态/类别和 JSON 字段，不要把当前调用点值当成完整协议。

## 快照口径

[`database-map/current-schema.md`](database-map/current-schema.md) 基于 2026-09-12 22:37 PDT（America/Los_Angeles）的 checkout 和当时 `data/workflow.sqlite3` 元数据整理，未读取业务行。它早于材料 SKU 外键迁移，只能解释迁移前字段，不能证明当前真实库已升级。现行结论必须来自当前源码、迁移后的隔离/正式数据库 PRAGMA，以及本次实际执行记录；隔离副本通过不等于真实库已经迁移。

## 五金为什么只保存 SKU 与业务数量

当前需求不需要恢复历史报表，因此人工与自动五金都不复制报表代码、名称、规格或单位。`product_code` 是关联商品表的外键；读取时 JOIN `products` 获得名称、规格、单位。商品改名会随读取更新，不需要同步修改每条五金。已有五金引用的商品单位禁止静默更改，因为换单位可能改变数量的含义。

写入流程是：原始报表 → 校验左右轨数量 → 映射有效 SKU → 按 SKU 转换数量 → 保存事实。左右滑轨同区块数量相同只计一边；M1094–M1097 原始偶数数量除二。人工直接输入商品计量数量，读取、重复确认和旧库迁移都不能再次除二。未完成映射时事务拒绝写入，而不是先存原代码再补映射。

修改映射或忽略规则只影响后续原始输入，不能重新解释已确认 SKU。删除人工五金直接 DELETE，不保留 active=0 行；新增和删除在同一个事务中，任何失败一起回滚。工厂单是否有效仍来自独立的 factory_orders.aimes_status。

## 单一进度和明细关联

`factory_orders.stage` 是一个工厂单的进度；`orders.stage` 是多个有效工厂单的汇总。生产时间、材料量、出货单据是支撑进度的明细，并不因只用一个状态字段而删除。检查生产归属可连接 `factory_orders.production_record_id = production_records.batch_id`；检查消耗连接 `production_materials.batch_id`，再按 `order_id, product_code` 汇总。

一个生产记录包含多个工厂单，而一个工厂单只属于一次生产，这是“一对多”：把外键放在工厂单即可，不必再有独立关系表。生产材料则保留明细表，因为一次生产可以有多个订单及多个 SKU。材料分配表保存来源总数和各订单份额，用于数量守恒校验；生产材料表保存实际消耗，两者不可混用。
