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

订单与工厂单由 `orders`、`factory_orders` 保存；Server/AIMES 扫描、同步异常和来源文件由 `source_files`、`sync_runs`、`sync_changes`、`active_issues` 等表保存。订单材料进入 `material_items`，工厂单五金进入 `hardware_items`；`manual_production_*` 记录生产批次及生产材料消耗，不能把生产材料消耗当成工厂单已出货。

商品主数据在 `products`：原始 `name/spec/category/unit` 保留库存目录证据，`material_kind/material_color/material_thickness` 是工作流读取的结构化材料属性，`catalog_present` 表示 SKU 是否仍出现在最新目录。名称到 SKU 的决定在 `inventory_resolution_rules`；mapping 行引用商品，ignore 行没有 SKU。

`material_items`、`manual_production_batch_materials` 和 `server_material_allocations` 都只保存 SKU、数量和各自必要身份；属性在读取时 JOIN `products`。`hardware_items` 同样以 SKU 引用商品，但额外保留来源名称、编码、规格和单位。库存成功单据在 `outbound_documents`，明确工厂单覆盖关系在 `outbound_document_factories`，出库范围人工决定在 `outbound_scope_decisions`。`inventory_operations` 只记录浏览器/库存操作意图、重试状态和结果，属于操作元数据，不等于出库事实。

`workflow_metadata` 和 `business_cache` 保存迁移标记、缓存值及更新时间；它们不是订单或库存事实。Server 预览使用工作副本和恢复材料。旧字段字典是迁移前快照，现行字段应从当前源码和已完成升级的隔离数据库核对。

## 如何按表查字段

1. 先在 `database.py` 和负责该表的模块中查看当前 `CREATE TABLE`、迁移和读写 SQL。
2. 对完成升级的隔离数据库运行 `PRAGMA table_info`、`index_list`/`index_info`、`foreign_key_list`，再执行 `PRAGMA foreign_key_check`；这些命令只读 schema/完整性，不需要读取业务行内容。
3. 五张 SKU 引用表应看到到 `products(code)` 的外键：`material_items`、`manual_production_batch_materials`、`server_material_allocations`、`hardware_items`、`inventory_resolution_rules`。参与这些表写入/事务的应用连接还必须在事务开始前确认 `PRAGMA foreign_keys=1`。
4. `order_id`、`factory_order` 等没有声明外键的字段仍按应用层关联理解。对 `TEXT` 状态/类别和 JSON 字段，不要把当前调用点值当成完整协议。

## 快照口径

[`database-map/current-schema.md`](database-map/current-schema.md) 基于 2026-09-12 22:37 PDT（America/Los_Angeles）的 checkout 和当时 `data/workflow.sqlite3` 元数据整理，未读取业务行。它早于材料 SKU 外键迁移，只能解释迁移前字段，不能证明当前真实库已升级。现行结论必须来自当前源码、迁移后的隔离/正式数据库 PRAGMA，以及本次实际执行记录；隔离副本通过不等于真实库已经迁移。
