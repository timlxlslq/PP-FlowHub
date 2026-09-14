# 数据库地图：当前文件、角色与字段入口

这份地图只介绍当前应用真正使用的两个 SQLite 文件，以及如何进入完整字段字典。它是静态学习资料，不会自动打开、查询或写入数据库。

## 两个正式运行库

| 文件 | 角色 | 当前结构 |
| --- | --- | ---: |
| `data/workflow.sqlite3` | 中央订单、材料、五金、生产、库存出库和同步事实 | 33 张表、307 个字段 |
| `data/assistant-runtime.sqlite3` | Agent 用量与已学习命令 | 2 张表、9 个字段 |

中央库路径由 [`core.py#L154`](../../traveler_assistant/core.py#L154) 的 `Config.workflow_database` 提供；schema 初始化由 [`database.py#L138`](../../traveler_assistant/database.py#L138) 的 `ensure_schema`、[`order_index.py#L703`](../../traveler_assistant/order_index.py#L703) 的 `OrderIndexStore` 和库存商品初始化共同负责。助手运行库路径由 [`runtime_store.py#L16`](../../traveler_assistant/runtime_store.py#L16) 返回。

## 快速入口

| 需要查什么 | 入口 |
| --- | --- |
| 当前两个正式运行库的完整字段、类型、可空、默认值、PK、唯一约束、外键和源码证据 | [`database-map/current-schema.md`](database-map/current-schema.md) |
| 连接、事务、路径、共享连接和外部数据隔离的学习说明 | [`11-database-guide.md`](11-database-guide.md) |

## 表的业务分层

订单与工厂单由 `orders`、`factory_orders` 保存；Server/AIMES 扫描、同步异常和来源文件由 `source_files`、`sync_runs`、`sync_changes`、`active_issues` 等表保存。订单材料进入 `material_items`，工厂单五金进入 `hardware_items`；`manual_production_*` 记录生产批次及生产材料消耗，不能把生产材料消耗当成工厂单已出货。

商品主数据在 `products`，名称到 SKU 的决定在 `inventory_resolution_rules`。库存成功单据在 `outbound_documents`，明确工厂单覆盖关系在 `outbound_document_factories`，出库范围人工决定在 `outbound_scope_decisions`。`inventory_operations` 只记录浏览器/库存操作意图、重试状态和结果，属于操作元数据，不等于出库事实。

`workflow_metadata` 和 `business_cache` 保存迁移标记、缓存值及更新时间；它们不是订单或库存事实。Server 预览使用工作副本和恢复材料，完整字段字典只列正式两个运行库。

## 如何按表查字段

1. 先在当前字段字典中按表名跳转。
2. 在字段表查看 SQLite 声明类型、可空、默认值、PK 位置、中文含义和源码证据。
3. 在字段表下方查看 SQLite schema 声明的唯一约束和 `REFERENCES` 外键。当前项目没有统一开启 `PRAGMA foreign_keys=ON`，因此声明关系不等于每个连接都会强制检查；`order_id`、`factory_order` 等仍需按应用层关联理解。
4. 对 `TEXT` 状态/类别和 JSON 字段，结合“已见值非穷举”及源码证据阅读；不要把当前调用点值当成完整协议。

## 快照口径

本地图基于 2026-09-12 22:37 PDT（America/Los_Angeles）当前 checkout 和实际 `data/workflow.sqlite3` 的 SQLite 元数据生成，未读取业务行。字段含义来自源码 CREATE/ALTER、读写、动态全字段恢复和序列化路径；源码或 schema 变化后需要重新核对。
