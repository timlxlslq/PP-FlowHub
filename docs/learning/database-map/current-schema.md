# 2026-09-12 数据库字段历史快照

本页是 2026-09-12 22:37 PDT（America/Los_Angeles）当时 checkout 与 `data/workflow.sqlite3` 的历史 schema 快照：中央业务库当时为 33 张表、307 个字段，助手运行库为 2 张表、9 个字段。它早于材料 SKU 外键迁移，不能作为当前 schema 或真实数据库已经迁移的证据；现行结构先看[数据模型](../../architecture/pp-flowhub-data-model.md)和[数据库地图](../12-database-map.md)，再以当前源码及迁移后数据库的 PRAGMA 结果核对。

字段证据来自采集时源码的 CREATE/ALTER、读写调用、动态全字段恢复和 SQLite 元数据。未把应用层关联误列为 schema 外键，也未读取业务行。

> 历史阅读说明：下文保留采集时的表项、源码行号和“当前”措辞，均只代表 2026-09-12 快照。本轮不手工把数百个字段改写成新结构，以免制造一份看似现行、实际无法重复生成的字典。

### 阅读约定

- “可空”按 SQLite `PRAGMA table_info` 的 `notnull` 解释；“是”表示该列未声明 `NOT NULL`，不代表业务上一定允许空值。
- `INTEGER PRIMARY KEY` 是 SQLite rowid 别名；插入 `NULL` 或省略值时由 SQLite 分配 rowid。普通 rowid 表中的 `TEXT PRIMARY KEY` 若没有另写 `NOT NULL`，PRAGMA 仍可能显示可空，不能把文本主键的唯一性误读成非空约束。
- 时间列按用途区分业务发生时间、外部系统同步/签发时间、本地记录创建时间和更新时间；不要用操作耗时替代业务事件时间。
- JSON 字段只说明快照源码已证明的外层用途；内部键可能扩展。状态/类别值列出当时已见值，除 SQLite CHECK 明确限制外均非穷举。SQLite schema 中的 `REFERENCES` 关系与应用层关联分开记录；“没有统一开启 `PRAGMA foreign_keys=ON`”是当时的连接现状，不是 SKU 迁移后的应用连接契约。

### 中央业务库表索引

| 分类 | 表 |
| --- | --- |
| 订单索引 | [`orders`](#table-orders)、[`factory_orders`](#table-factory_orders)、[`source_files`](#table-source_files)、[`order_installation_days`](#table-order_installation_days) |
| 同步与问题证据 | [`sync_runs`](#table-sync_runs)、[`sync_changes`](#table-sync_changes)、[`active_issues`](#table-active_issues)、[`aimes_order_assignments`](#table-aimes_order_assignments)、[`aimes_review_rows`](#table-aimes_review_rows)、[`ignored_aimes_factory_orders`](#table-ignored_aimes_factory_orders)、[`server_scan_xml_state`](#table-server_scan_xml_state)、[`temporary_orders`](#table-temporary_orders) |
| 生产与来源证据 | [`production_batches`](#table-production_batches)、[`batch_evidence`](#table-batch_evidence)、[`optimization_artifacts`](#table-optimization_artifacts)、[`manual_production_batches`](#table-manual_production_batches)、[`manual_production_batch_factories`](#table-manual_production_batch_factories)、[`manual_production_batch_materials`](#table-manual_production_batch_materials) |
| 材料与五金事实 | [`material_items`](#table-material_items)、[`hardware_items`](#table-hardware_items)、[`hardware_source_decisions`](#table-hardware_source_decisions)、[`hardware_source_versions`](#table-hardware_source_versions)、[`server_material_allocations`](#table-server_material_allocations)、[`server_material_preview_scopes`](#table-server_material_preview_scopes) |
| 库存映射与出库事实 | [`products`](#table-products)、[`inventory_resolution_rules`](#table-inventory_resolution_rules)、[`outbound_scope_decisions`](#table-outbound_scope_decisions)、[`outbound_documents`](#table-outbound_documents)、[`outbound_document_factories`](#table-outbound_document_factories)、[`inventory_operations`](#table-inventory_operations) |
| 备份与工作流元数据 | [`backup_records`](#table-backup_records)、[`business_cache`](#table-business_cache)、[`workflow_metadata`](#table-workflow_metadata) |

### 助手运行库表索引

| 分类 | 表 |
| --- | --- |
| 助手运行库 | [`agent_usage`](#table-agent_usage)、[`learned_commands`](#table-learned_commands) |

## 中央业务库（workflow.sqlite3）

路径由 `Config.workflow_database` 得到，默认是 `state_dir/workflow.sqlite3`。当前业务表由 `ensure_schema`、`OrderIndexStore` 和库存商品初始化共同提供。

## `active_issues` {#table-active_issues}

用途：保存当前同步/解析/归属问题及其解决审计状态。

源码归属与读写：traveler_assistant/order_index.py#L871-882（ensure_schema 建表；status 默认 open，时间和 resolved_at 的空值约定可见。）; traveler_assistant/order_index.py#L1937-1997（add_change/upsert_active_issue 写入并按 open 查询。）; traveler_assistant/order_index.py#L2036-2083（resolve 和按范围解决把 status 写为 resolved，并写 resolved_at。）

Schema 定义：traveler_assistant/order_index.py#L871-882。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `issue_key` | `TEXT` | 是 | `无` | 1 | 问题记录的稳定键，用于 upsert、按键解决和路径范围解决；其内部拼接规则未在本次证据中完整确认。（部分确认） | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `kind` | `TEXT` | 否 | `无` | — | 问题类别；由 Server/AIMES 同步、报表读取、归属和临时订单流程写入。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 关联订单号；空字符串表示问题不归属于某订单或尚未解析。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 关联工厂单号；空字符串表示问题不归属于某工厂单。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `path` | `TEXT` | 否 | `''` | — | 触发问题的 Server 文件或文件夹路径；路径变更时会随迁移更新。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `message` | `TEXT` | 否 | `无` | — | 面向用户/审计的具体问题说明。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `'open'` | — | 问题生命周期状态；创建/重现为 open，解决流程写为 resolved。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `first_seen` | `TEXT` | 否 | `无` | — | 首次观察到该问题的时间戳（同步/操作观察时间）。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_seen` | `TEXT` | 否 | `无` | — | 最近一次观察到该问题的时间戳（同步观察时间）。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `resolved_at` | `TEXT` | 否 | `''` | — | 问题解决时间戳；未解决时为空字符串。 | traveler_assistant/order_index.py#L871-882（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_active_issues_1` → (issue_key)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`status`：open, resolved（完整；证据 traveler_assistant/order_index.py:1937-1997,2036-2083）；`kind`：batch_conflict, factory_ownership, hardware_integrity, hardware_mapping, hardware_selection, material_validation, order_validation, outbound_hardware_difference, report_error, server_missing_report, server_data, report_empty, source_removed, temporary_processing（当前已见值，非穷举；证据 traveler_assistant/order_index.py:5905-5910,6674-6686,6781-6793,6966-6976,7093-7103,7167-7177,7286-7296,7336-7347,7574-7583,2145-2150; traveler_assistant/hardware_facts.py:135-178）

## `aimes_order_assignments` {#table-aimes_order_assignments}

用途：保存用户确认的 AIMES 非标准行到本地订单的归属。

源码归属与读写：traveler_assistant/order_index.py#L1263-1389（读取字段、确认 upsert、恢复删除及其订单/工厂单关联。）

Schema 定义：traveler_assistant/order_index.py#L853-860。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `ignore_key` | `TEXT` | 是 | `无` | 1 | AIMES 非标准行的稳定键；同时作为该确认记录主键，内部生成规则未完整确认。（部分确认） | traveler_assistant/order_index.py#L853-860（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `无` | — | 被人工确认归属的 AIMES 工厂单号。 | traveler_assistant/order_index.py#L853-860（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_name` | `TEXT` | 否 | `''` | — | AIMES 工厂单名称快照。 | traveler_assistant/order_index.py#L853-860（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `original_sales_order_name` | `TEXT` | 否 | `''` | — | AIMES 原始销售订单名称快照；保留确认前来源值。 | traveler_assistant/order_index.py#L853-860（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `assigned_order_id` | `TEXT` | 否 | `无` | — | 用户确认归入的本地订单号。 | traveler_assistant/order_index.py#L853-860（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `confirmed_at` | `TEXT` | 否 | `无` | — | 用户确认归属的操作时间。 | traveler_assistant/order_index.py#L853-860（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_aimes_order_assignments_1` → (ignore_key)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `aimes_review_rows` {#table-aimes_review_rows}

用途：保存当前等待用户处理的非标准 AIMES 行。

源码归属与读写：traveler_assistant/order_index.py#L1294-1354（整表替换当前待复核行、读取和按键删除。）

Schema 定义：traveler_assistant/order_index.py#L861-870。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `ignore_key` | `TEXT` | 是 | `无` | 1 | 待人工处理 AIMES 行的稳定键，来自 issue 的 ignore_key/id。（部分确认） | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 待复核 AIMES 工厂单号。 | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_name` | `TEXT` | 否 | `''` | — | 待复核 AIMES 工厂单名称。 | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `sales_order_name` | `TEXT` | 否 | `''` | — | 待复核 AIMES 销售订单名称。 | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `reason` | `TEXT` | 否 | `''` | — | 该行进入待复核的原因。 | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `suggested_order_id` | `TEXT` | 否 | `''` | — | 代码推导的建议订单号；空字符串表示没有建议。 | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `split_time` | `TEXT` | 否 | `''` | — | AIMES 拆单时间快照；是业务事件时间，不是同步耗时。 | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_seen` | `TEXT` | 否 | `无` | — | 该待复核行最近一次被写入/观察的时间。 | traveler_assistant/order_index.py#L861-870（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_aimes_review_rows_1` → (ignore_key)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `backup_records` {#table-backup_records}

用途：保存中央 SQLite 备份文件及结果。

源码归属与读写：traveler_assistant/database.py#L326-336（ensure_schema 建表和 finished_at 索引。）; traveler_assistant/backup.py#L20-81（按 success 查询，备份完成后写 daily/success、指纹和完成时间。）

Schema 定义：traveler_assistant/database.py#L326-336。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 备份记录自增标识。 | traveler_assistant/database.py#L326-336（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `backup_path` | `TEXT` | 否 | `无` | — | 生成的 SQLite 备份文件路径。 | traveler_assistant/database.py#L326-336（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `backup_kind` | `TEXT` | 否 | `'daily'` | — | 备份类型；当前备份实现写入 daily。 | traveler_assistant/database.py#L326-336（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `started_at` | `TEXT` | 否 | `无` | — | 备份操作开始时间。 | traveler_assistant/database.py#L326-336（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `finished_at` | `TEXT` | 否 | `无` | — | 备份操作完成时间。 | traveler_assistant/database.py#L326-336（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `无` | — | 备份结果状态；成功路径写入 success，其他值由失败/后续流程决定，未穷举。（部分确认） | traveler_assistant/database.py#L326-336（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `database_fingerprint` | `TEXT` | 否 | `''` | — | 生成备份文件的内容指纹，用于识别备份版本；指纹算法值结构不在本表代码中展开。（部分确认） | traveler_assistant/database.py#L326-336（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`backup_kind`：daily（当前已见值，非穷举；证据 traveler_assistant/backup.py:74-75）；`status`：success（当前已见值，非穷举；证据 traveler_assistant/backup.py:30,75）

## `batch_evidence` {#table-batch_evidence}

用途：保存从 Server/优化证据观察到的工厂单-生产批次关系。

源码归属与读写：traveler_assistant/order_index.py#L905-932（建表、三列组合唯一约束和工厂单状态索引。）; traveler_assistant/order_index.py#L2104-2143（创建/更新 production_batches 与 batch_evidence，并按 observed 关联工厂单。）

Schema 定义：traveler_assistant/order_index.py#L905-915。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 批次证据自增标识。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `无` | — | 从来源证据解析出的工厂单号。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `batch_number` | `TEXT` | 否 | `无` | — | 来源文件中观察到的生产批次号。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_path` | `TEXT` | 否 | `无` | — | 批次证据所在的来源文件路径。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 批次证据关联的订单号；解析不到时为空字符串。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `first_seen` | `TEXT` | 否 | `无` | — | 首次观察到该工厂单/批次/路径组合的时间。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_seen` | `TEXT` | 否 | `无` | — | 最近观察到该组合的时间。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `'observed'` | — | 批次证据生命周期/观察状态；默认 observed，本次检索确认的读取路径只按 observed 使用。 | traveler_assistant/order_index.py#L905-915（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_batch_evidence_1` → (factory_order, batch_number, source_path)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`status`：observed（当前已见值，非穷举；证据 traveler_assistant/order_index.py:913,2132）

## `factory_orders` {#table-factory_orders}

用途：保存工厂单身份、来源、优化/生产/出库进度索引。

源码归属与读写：traveler_assistant/order_index.py#L757-776（核心工厂单表建表字段和默认状态。）; traveler_assistant/order_index.py#L953-1037（增加 sales/split、出库元数据、生产批次、AIMES 和优化/出库业务时间字段。）; traveler_assistant/order_index.py#L1633-1797（Server/general upsert 与 AIMES identity upsert 的字段保护和状态写入。）; traveler_assistant/order_index.py#L1799-1831（AIMES 删除保留事实并标记 deleted。）; traveler_assistant/order_index.py#L2301-2351（dashboard 读取工厂单及优化/出库时间，并仅读 active AIMES 身份。）; traveler_assistant/order_index.py#L3470-3585（出库状态刷新、业务出库完成时间和内容变化语义。）

优化聚合规则：`optimization_first_completed_at`/`optimization_latest_completed_at` 分别取关联优化证据 `completed_at` 的最小/最大值；`optimization_first_seen_at`/`optimization_latest_seen_at` 分别取 `first_seen_at`/`last_seen_at` 的最小/最大值；`optimization_source_path` 按 `completed_at` 最新、再按证据 `id` 最新选择。订单级展示计算须在所有预期子单完成后才取对应子单时间的最大值，否则为空。

Schema 定义：traveler_assistant/order_index.py#L757-776; traveler_assistant/order_index.py#L953-1037。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `factory_order` | `TEXT` | 是 | `无` | 1 | 工厂单号；表主键，也是工厂单事实的稳定身份。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 本地订单号；由 AIMES 或 Server 归属逻辑关联，空字符串表示尚未归属。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_name` | `TEXT` | 否 | `''` | — | 工厂单名称；优先保留来源名称。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `name_source` | `TEXT` | 否 | `''` | — | 名称/身份来源标记，例如 AIMES；其他值未穷举。（部分确认） | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_folder` | `TEXT` | 否 | `''` | — | Server 订单文件夹路径。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `report_state` | `TEXT` | 否 | `'未发现'` | — | Server 报表发现状态；用于区分未发现、已发现等。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `ownership_status` | `TEXT` | 否 | `'待确认'` | — | 订单归属确认状态；用于防止工厂单落入错误订单。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `has_hardware` | `INTEGER` | 否 | `0` | — | 是否存在当前有效五金事实的整数布尔标志（0/1）。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `optimized` | `INTEGER` | 否 | `0` | — | 是否有有效优化证据的整数布尔标志（0/1）。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_status` | `TEXT` | 否 | `'未查询'` | — | 该工厂单的库存出库状态；生产完成不等于此状态已出库。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_document` | `TEXT` | 否 | `''` | — | 出库单号或其他出库证据标识；空字符串表示没有本地单号。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_server_seen` | `TEXT` | 否 | `''` | — | 最近从 Server 观察到该工厂单的时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_aimes_seen` | `TEXT` | 否 | `''` | — | 最近从 AIMES 观察到该工厂单的时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 该工厂单索引事实最近被本地更新的时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `sales_order_name` | `TEXT` | 否 | `''` | — | AIMES 销售订单名称快照。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `split_time` | `TEXT` | 否 | `''` | — | AIMES 拆单业务事件时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `production_batch_id` | `INTEGER` | 是 | `无` | — | 关联生产批次的本地 batch_id；当前表无声明外键，关联由代码查询 production_batches 完成；空值表示无批次关联。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `aimes_status` | `TEXT` | 否 | `'active'` | — | AIMES 身份的活动状态；删除后保留记录并标为 deleted。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `aimes_deleted_at` | `TEXT` | 否 | `''` | — | AIMES 确认删除该工厂单的时间；未删除为空字符串。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `aimes_last_verified_at` | `TEXT` | 否 | `''` | — | 最近一次精确 AIMES 核验该身份的时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_mode` | `TEXT` | 否 | `''` | — | 出库方式/语义标记，例如库存出库、客户自供或无五金；值集合由库存流程维护，未穷举。（部分确认） | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_fingerprint` | `TEXT` | 否 | `''` | — | 出库事实/当前选择的指纹，用于检测出库内容变化；算法和 JSON 结构未在本次证据中展开。（部分确认） | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `optimization_first_completed_at` | `TEXT` | 否 | `''` | — | 该工厂单优化证据首次完成时间；来自 AICNC/XML 业务文件完成时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `optimization_latest_completed_at` | `TEXT` | 否 | `''` | — | 该工厂单最近一次优化证据完成时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `optimization_first_seen_at` | `TEXT` | 否 | `''` | — | 该优化证据首次被本地扫描/观察的时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `optimization_latest_seen_at` | `TEXT` | 否 | `''` | — | 该优化证据最近一次被本地扫描/观察的时间。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `optimization_source_path` | `TEXT` | 否 | `''` | — | 当前/代表性优化证据来源文件路径。 | traveler_assistant/order_index.py#L757-776（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L953-1037（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_completed_at` | `TEXT` | 否 | `''` | — | 正常重算取与当前出库单号匹配的同步时间（`synced_at`）最大值；没有匹配时间时保留原值。兼容恢复路径可从单据时间、本地记录时间或关联记录时间回填。 | traveler_assistant/order_index.py#L3552-3585<br>traveler_assistant/order_index.py#L1044-1061<br>traveler_assistant/hardware_facts.py#L184-194 |

唯一约束/索引：`sqlite_autoindex_factory_orders_1` → (factory_order)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`report_state`：未发现, 已发现, AIMES已发现, 手工添加（当前已见值，非穷举；证据 traveler_assistant/order_index.py:766,1760-1762,7388,10112-10113）；`ownership_status`：待确认, 已确认, 归属冲突（完整；证据 traveler_assistant/order_index.py:767,2847-2855）；`outbound_status`：未查询, 未出库, 已出库, 需要更新（当前已见值，非穷举；证据 traveler_assistant/order_index.py:770,3538,3574; traveler_assistant/production.py:516-526）；`aimes_status`：active, deleted（当前已见值，非穷举；证据 traveler_assistant/order_index.py:1025,1773-1774,1807-1809）；`outbound_mode`：customer_supplied, no_hardware, inventory（当前已见值，非穷举；证据 traveler_assistant/inventory.py:487-499,578-590; traveler_assistant/hardware_facts.py:192）

## `ignored_aimes_factory_orders` {#table-ignored_aimes_factory_orders}

用途：保存用户忽略的 AIMES 异常工厂单行。

源码归属与读写：traveler_assistant/order_index.py#L1234-1261（读取忽略记录并按 ignored_at 排序。）; traveler_assistant/order_index.py#L1396-1433（忽略/恢复写入或删除记录，并删除关联 factory_order。）

Schema 定义：traveler_assistant/order_index.py#L845-852。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `ignore_key` | `TEXT` | 是 | `无` | 1 | 被用户忽略的 AIMES 异常行稳定键；表主键。（部分确认） | traveler_assistant/order_index.py#L845-852（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 被忽略的 AIMES 工厂单号。 | traveler_assistant/order_index.py#L845-852（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_name` | `TEXT` | 否 | `''` | — | 被忽略行的工厂单名称快照。 | traveler_assistant/order_index.py#L845-852（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `sales_order_name` | `TEXT` | 否 | `''` | — | 被忽略行的销售订单名称快照。 | traveler_assistant/order_index.py#L845-852（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `reason` | `TEXT` | 否 | `''` | — | 用户/系统记录的忽略原因。 | traveler_assistant/order_index.py#L845-852（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `ignored_at` | `TEXT` | 否 | `无` | — | 执行忽略动作的时间。 | traveler_assistant/order_index.py#L845-852（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_ignored_aimes_factory_orders_1` → (ignore_key)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `optimization_artifacts` {#table-optimization_artifacts}

用途：保存 AICNC/XML 优化结果文件的来源与时间证据。

源码归属与读写：traveler_assistant/order_index.py#L916-932（建表、文件字段和四列组合唯一约束。）; traveler_assistant/order_index.py#L2960-3050（从优化结果文件解析工厂单，upsert 证据并更新 first/latest seen。）; traveler_assistant/order_index.py#L8967-9020（内存优化证据批量 upsert 的列映射。）

Schema 定义：traveler_assistant/order_index.py#L916-932。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 优化证据自增标识。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_path` | `TEXT` | 否 | `无` | — | AICNC 优化结果文件路径，作为证据来源。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 从优化证据解析出的订单号；解析不到时为空字符串。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `无` | — | 从 nesting_result.xml OrderID 等证据解析出的工厂单号。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `file_modified_at` | `REAL` | 否 | `无` | — | 来源文件的文件系统修改时间（扫描文件时间）。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `file_created_at` | `REAL` | 否 | `0` | — | 来源文件的文件系统创建时间；无法取得时默认 0。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `completed_at` | `TEXT` | 否 | `无` | — | 优化结果文件的文件系统修改时间（mtime）；不是本地扫描时间。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `copied_at` | `TEXT` | 否 | `''` | — | 优化证据文件的文件系统创建时间；未取得时为空字符串。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `first_seen_at` | `TEXT` | 否 | `无` | — | 该文件指纹首次被本地扫描记录的时间（扫描时 `_now`）。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_seen_at` | `TEXT` | 否 | `无` | — | 该文件指纹最近一次被本地扫描记录的时间（扫描时 `_now`）。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `size` | `INTEGER` | 否 | `0` | — | 来源文件大小（字节）。 | traveler_assistant/order_index.py#L916-932（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_optimization_artifacts_1` → (source_path, file_modified_at, size, factory_order)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `order_installation_days` {#table-order_installation_days}

用途：保存订单级计划/实际安装开始日期及安装人员。

源码归属与读写：traveler_assistant/order_index.py#L747-756（建表、planned/actual CHECK 和组合主键。）; traveler_assistant/order_index.py#L1547-1605（备注/安装日期保存；每种 date_type 最多一个开始日期并校验 YYYY-MM-DD。）; traveler_assistant/database.py#L481-520（兼容迁移只保留每订单最早 actual，并建立 actual 按订单唯一的部分索引。）

Schema 定义：traveler_assistant/order_index.py#L747-756; traveler_assistant/database.py#L481-520。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `order_id` | `TEXT` | 否 | `无` | 1 | 安装日期所属订单号；应用层关联 orders.order_id，数据库未声明外键。 | traveler_assistant/order_index.py#L747-756（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/database.py#L481-520（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `date_type` | `TEXT` | 否 | `无` | 2 | 安装日期类型；SQLite CHECK 只允许 planned（计划）或 actual（实际）。 | traveler_assistant/order_index.py#L747-756（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/database.py#L481-520（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `install_date` | `TEXT` | 否 | `无` | 3 | 安装开始日期，格式由保存逻辑校验为 YYYY-MM-DD。 | traveler_assistant/order_index.py#L747-756（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/database.py#L481-520（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `installer` | `TEXT` | 否 | `''` | — | 安装人员/安装组文本；可为空字符串。 | traveler_assistant/order_index.py#L747-756（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/database.py#L481-520（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 该安装日期事实最后保存时间。 | traveler_assistant/order_index.py#L747-756（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/database.py#L481-520（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`idx_order_installation_actual_start` → (order_id)；`sqlite_autoindex_order_installation_days_1` → (order_id, date_type, install_date)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`date_type`：planned, actual（完整；证据 traveler_assistant/order_index.py:749; database.py:497）

## `orders` {#table-orders}

用途：保存订单索引、校验、展示阶段、备注和 Server 扫描策略。

源码归属与读写：traveler_assistant/order_index.py#L729-746（建表字段和默认值。）; traveler_assistant/order_index.py#L972-992（迁移增加 validation_message、user_note 和 Server scan policy 四字段。）; traveler_assistant/order_index.py#L1435-1489（订单 upsert 保留既有状态、来源时间，并更新 Server/AIMES 观察时间。）; traveler_assistant/order_index.py#L1512-1537（读写 Server scan policy 及其指纹/观察截止时间。）; traveler_assistant/order_index.py#L2282-2467（dashboard 读取订单、安装日期，并根据工厂/生产/出库事实推导 stage。）

Schema 定义：traveler_assistant/order_index.py#L729-746; traveler_assistant/order_index.py#L972-992。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `order_id` | `TEXT` | 是 | `无` | 1 | 订单主键；正常订单为 PP/CS 等业务订单号，临时订单也可用此索引。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_type` | `TEXT` | 否 | `无` | — | 订单类型；代码区分 normal/temporary 等，值集合未穷举。（部分确认） | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_folder` | `TEXT` | 否 | `''` | — | 订单来源 Server 文件夹路径；临时订单路径也由 temporary_orders 独立保存。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_folder_mtime` | `REAL` | 是 | `无` | — | 订单来源文件夹的文件系统修改时间（REAL 秒值）；未知时 NULL。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `validation_status` | `TEXT` | 否 | `'待同步'` | — | 订单数据校验状态；与 derived stage 分开保存。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `stage` | `TEXT` | 否 | `'待拆单'` | — | 订单业务进度展示/缓存值，由订单及工厂单、生产、出库事实推导并持久化。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `material_status` | `TEXT` | 否 | `'待校验'` | — | 订单材料解析/准备状态摘要，例如待校验或板材 · 封边；值集合未穷举。（部分确认） | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_server_seen` | `TEXT` | 否 | `''` | — | 最近从 Server 观察该订单的时间。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_aimes_seen` | `TEXT` | 否 | `''` | — | 最近从 AIMES 观察该订单的时间。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 订单索引事实最近本地更新的时间。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `validation_message` | `TEXT` | 否 | `''` | — | 数据校验失败或提示的详细原因；正常时清空。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `user_note` | `TEXT` | 否 | `''` | — | 用户维护的订单备注；Server/AIMES upsert 不覆盖。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_scan_policy` | `TEXT` | 否 | `''` | — | 订单后续 Server 扫描策略，如 watching、permanent；值集合未穷举。（部分确认） | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_scan_aimes_fingerprint` | `TEXT` | 否 | `''` | — | 与扫描策略绑定的 AIMES 快照指纹；结构/算法未在本次证据中展开。（部分确认） | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_scan_watch_until` | `TEXT` | 否 | `''` | — | watching 观察期结束时间；非观察策略通常为空。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_scan_policy_updated_at` | `TEXT` | 否 | `''` | — | 扫描策略最后变更时间。 | traveler_assistant/order_index.py#L729-746（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L972-992（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_orders_1` → (order_id)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`order_type`：normal, temporary（当前已见值，非穷举；证据 traveler_assistant/order_index.py:2357,4588）；`validation_status`：待同步, 待校验, 正常, 数据异常（当前已见值，非穷举；证据 traveler_assistant/order_index.py:1454,6264-6270,8915-8924）；`stage`：待拆单, 已设计, 数据异常, 待确认, 已出货, 已拆单待优化, 部分优化, 部分生产，部分出货, 部分出货, 已生产, 部分生产, 已优化, 待人工处理（当前已见值，非穷举；证据 traveler_assistant/order_index.py:1063,2398-2427）；`material_status`：待校验, 板材 · 封边（当前已见值，非穷举；证据 traveler_assistant/order_index.py:737,6947,7050）；`server_scan_policy`：watching, permanent, legacy（当前已见值，非穷举；证据 traveler_assistant/order_index.py:4491,4506,3947）

## `production_batches` {#table-production_batches}

用途：保存生产批次索引。

源码归属与读写：traveler_assistant/database.py#L178-188（中心数据库建 production_batches；batch_number 唯一。）; traveler_assistant/database.py#L178-188（central database 建 production_batches；batch_number 唯一。）; traveler_assistant/order_index.py#L2104-2143（批次证据写入/更新时间和 factory_orders.production_batch_id 关联。）

Schema 定义：traveler_assistant/database.py#L178-188。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `batch_id` | `INTEGER` | 是 | `无` | 1 | 生产批次自增标识；被 factory_orders.production_batch_id 以应用层方式引用。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `batch_number` | `TEXT` | 否 | `无` | — | 生产批次号；唯一。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `production_date` | `TEXT` | 否 | `''` | — | 批次生产业务日期/时间文本；未提供时空字符串。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source` | `TEXT` | 否 | `''` | — | 批次来源标记；当前 Server 报表证据路径写入 server-report，其他来源未穷举。（部分确认） | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `'active'` | — | 批次证据状态；默认 active，批次关联查询还使用 completed。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `first_seen` | `TEXT` | 否 | `''` | — | 首次观察该批次的同步时间。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_seen` | `TEXT` | 否 | `''` | — | 最近观察该批次的同步时间。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 批次记录创建时间。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 批次记录最近更新时间。 | traveler_assistant/database.py#L178-188（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_production_batches_1` → (batch_number)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`source`：server-report（当前已见值，非穷举；证据 traveler_assistant/order_index.py:2111-2117）；`status`：active（当前已见值，非穷举；证据 traveler_assistant/database.py:178-188; no named update of production_batches.status found in current traveler_assistant source）

## `server_scan_xml_state` {#table-server_scan_xml_state}

用途：保存 XML/优化文件扫描基线。

源码归属与读写：traveler_assistant/order_index.py#L790-799（建表及 source_folder/kind 索引。）; traveler_assistant/order_index.py#L2214-2254（保存 XML baseline，按路径 upsert。）; traveler_assistant/order_index.py#L4660-4688（读取 XML 状态比较修改时间。）

Schema 定义：traveler_assistant/order_index.py#L790-799。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `path` | `TEXT` | 是 | `无` | 1 | Server XML/优化证据路径主键。 | traveler_assistant/order_index.py#L790-799（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_folder` | `TEXT` | 否 | `无` | — | 该 XML 文件所属的 Server 订单文件夹。 | traveler_assistant/order_index.py#L790-799（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `kind` | `TEXT` | 否 | `无` | — | 扫描对象类型；该表由 XML baseline 路径保存，当前调用使用 optimization_result。 | traveler_assistant/order_index.py#L790-799（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 从来源文件夹/文件解析出的订单号；未知时为空字符串。 | traveler_assistant/order_index.py#L790-799（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `modified_at` | `INTEGER` | 否 | `0` | — | XML 文件系统修改时间（整数时间值）。 | traveler_assistant/order_index.py#L790-799（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_seen` | `TEXT` | 否 | `无` | — | 最近一次扫描观察该 XML 文件的时间。 | traveler_assistant/order_index.py#L790-799（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_server_scan_xml_state_1` → (path)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`kind`：optimization_input, optimization_result（完整；证据 traveler_assistant/order_index.py:90,2228-2233）

## `source_files` {#table-source_files}

用途：保存 Server 来源路径、身份解析和增量扫描基线。

源码归属与读写：traveler_assistant/order_index.py#L778-789（建表字段；path 主键。）; traveler_assistant/order_index.py#L1009-1019（迁移增加 content_fingerprint 和 batch_number。）; traveler_assistant/order_index.py#L1836-1943（来源文件 upsert、变更记录和字段身份更新。）; traveler_assistant/order_index.py#L5740-5765（扫描基线读取路径、种类和修改时间。）

Schema 定义：traveler_assistant/order_index.py#L778-789; traveler_assistant/order_index.py#L1009-1019。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `path` | `TEXT` | 是 | `无` | 1 | Server 来源文件或文件夹路径主键。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_folder` | `TEXT` | 否 | `''` | — | 文件所属订单/临时文件夹路径。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `kind` | `TEXT` | 否 | `无` | — | 来源对象种类，如 folder、board、material、fittings 等；代码按 kind 分流。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 来源文件解析出的订单号；未解析时为空字符串。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 来源文件解析出的工厂单号；未解析时为空字符串。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `modified_at` | `REAL` | 否 | `0` | — | 来源文件系统修改时间（REAL 秒值）；旧版本纳秒值会被归一化。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `size` | `INTEGER` | 否 | `0` | — | 来源文件大小（字节）。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_seen` | `TEXT` | 否 | `无` | — | 最近扫描观察该路径的时间。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `content_fingerprint` | `TEXT` | 否 | `''` | — | 来源内容/解析基线指纹；用于判断内容是否变化，结构/算法未在本次证据中展开。（部分确认） | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `batch_number` | `TEXT` | 否 | `''` | — | 来源文件关联的生产批次号；无关联时为空字符串。 | traveler_assistant/order_index.py#L778-789（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L1009-1019（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_source_files_1` → (path)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`kind`：folder, board, material, fittings, optimization_result, temporary_processing（当前已见值，非穷举；证据 traveler_assistant/order_index.py:5479,6766,6827,7107,4669）

## `sync_changes` {#table-sync_changes}

用途：保存同步变化和问题解决事件。

源码归属与读写：traveler_assistant/database.py#L156-166（中心数据库最先创建同步变化表。）; traveler_assistant/order_index.py#L835-844（OrderIndexStore 建表字段。）; traveler_assistant/order_index.py#L1930-1943（add_change 将严重级别、类型、订单/工厂单/路径和消息写入。）; traveler_assistant/order_index.py#L2258-2272（按 id 或最近记录读取同步变化。）

Schema 定义：traveler_assistant/database.py#L156-165; traveler_assistant/order_index.py#L835-844。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 同步变化/审计事件自增标识。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `observed_at` | `TEXT` | 否 | `无` | — | 发现或记录该变化的操作/同步时间。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `severity` | `TEXT` | 否 | `无` | — | 事件严重级别；代码使用 info、warning、error。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `kind` | `TEXT` | 否 | `无` | — | 事件类型；由各同步、解决、迁移路径写入，非穷举。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 事件关联订单号；没有订单时为空字符串。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 事件关联工厂单号；没有工厂单时为空字符串。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `path` | `TEXT` | 否 | `''` | — | 事件关联 Server 文件/文件夹路径；没有路径时为空字符串。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `message` | `TEXT` | 否 | `无` | — | 事件的具体说明。 | traveler_assistant/database.py#L156-165（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L835-844（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`severity`：info, warning, error（完整；证据 traveler_assistant/order_index.py:1827,4311,6792,7573）；`kind`：aimes, aimes_deleted, aimes_order_assignment, factory_ownership, factory_ownership_resolved, folder_changed, hardware_mapping, hardware_selection, historical_outbound_confirmed, historical_validation_reconciled, issue_resolved, manual_factory, material_validation, material_validation_reconciled, order_validation, report_empty, report_error, server_data, server_folder_renamed, source_removed, temporary_manual_outbound_reconciled, temporary_processing（当前已见值，非穷举；证据 traveler_assistant/order_index.py:1826-1829,3859-3891,4089,4311,4855,5433,6519,6724,6792,7063,7243,7273,7346,7435,7573,10136-10190,10326-10367）

## `sync_runs` {#table-sync_runs}

用途：保存一次 AIMES/Server 同步运行的计数与错误。

源码归属与读写：traveler_assistant/order_index.py#L825-834（建表字段和计数默认值。）; traveler_assistant/order_index.py#L2155-2190（写入一次运行的起止时间、AIMES 成功计数、Server 文件夹数和错误，并读取最近运行。）

Schema 定义：traveler_assistant/order_index.py#L825-834。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 同步运行记录自增标识。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `started_at` | `TEXT` | 否 | `无` | — | 一次同步运行开始时间。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `finished_at` | `TEXT` | 否 | `无` | — | 一次同步运行完成时间。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `aimes_attempted` | `INTEGER` | 否 | `0` | — | 本次是否尝试 AIMES（整数布尔值 0/1）。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `aimes_succeeded` | `INTEGER` | 否 | `0` | — | 本次 AIMES 是否成功（整数布尔值 0/1）。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `aimes_count` | `INTEGER` | 否 | `0` | — | 本次 AIMES 成功返回/处理的数量。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_folder_count` | `INTEGER` | 否 | `0` | — | 本次扫描到的 Server 文件夹数量。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `error` | `TEXT` | 否 | `''` | — | 本次运行错误说明；正常时为空字符串。 | traveler_assistant/order_index.py#L825-834（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `temporary_orders` {#table-temporary_orders}

用途：保存非标准临时订单文件夹、Traveler 生成和出库处理状态。

源码归属与读写：traveler_assistant/order_index.py#L883-904（建表字段、source_folder 唯一和 Traveler/扫描策略默认值。）; traveler_assistant/order_index.py#L996-1007（迁移增加 Traveler 元数据和 Server scan policy 字段。）; traveler_assistant/order_index.py#L1127-1231（读取和按 source_folder upsert；空值保留既有 Traveler/出库/扫描元数据。）; traveler_assistant/order_index.py#L4725-5050（临时订单处理、Traveler 生成、人工完成和出库状态实际写入。）

Schema 定义：traveler_assistant/order_index.py#L883-904; traveler_assistant/order_index.py#L996-1007。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `temporary_id` | `TEXT` | 是 | `无` | 1 | 临时订单稳定标识/主键。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `folder_name` | `TEXT` | 否 | `无` | — | 临时订单文件夹名称。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `source_folder` | `TEXT` | 否 | `无` | — | 临时订单来源文件夹路径；唯一，作为 upsert 冲突键。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `folder_created_at` | `REAL` | 否 | `0` | — | 来源文件夹创建时间（REAL 秒值）。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `content_fingerprint` | `TEXT` | 否 | `''` | — | 临时订单来源内容指纹，用于判断 Traveler/处理结果是否仍可复用。（部分确认） | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `traveler_path` | `TEXT` | 否 | `''` | — | 生成的 Traveler 文件路径。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `processing_status` | `TEXT` | 否 | `'未处理'` | — | 临时订单处理状态，例如 未处理、处理中、Traveler 已生成、已人工处理、处理失败。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_status` | `TEXT` | 否 | `'未出库'` | — | 临时订单出库状态，例如 未出库、出库状态未知、已出库。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_document` | `TEXT` | 否 | `''` | — | 临时订单出库单号或证据标识。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `processed_at` | `TEXT` | 否 | `''` | — | 临时订单处理完成业务时间。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `outbound_at` | `TEXT` | 否 | `''` | — | 临时订单出库完成业务时间。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `last_error` | `TEXT` | 否 | `''` | — | 最近一次临时订单处理错误。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 临时订单记录最近本地更新时间。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `traveler_fingerprint` | `TEXT` | 否 | `''` | — | 生成 Traveler 时使用的来源指纹，用于重试时判断能否复用。（部分确认） | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `traveler_include_hardware` | `INTEGER` | 否 | `1` | — | 生成 Traveler 是否包含五金的整数布尔值（默认 1）。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `traveler_status` | `TEXT` | 否 | `'未生成'` | — | Traveler 生成状态；默认 未生成，成功路径写 已生成。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `traveler_generated_at` | `TEXT` | 否 | `''` | — | Traveler 生成完成时间。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_scan_policy` | `TEXT` | 否 | `''` | — | 临时文件夹后续 Server 扫描策略，如 watching、permanent；值集合未穷举。（部分确认） | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_scan_watch_until` | `TEXT` | 否 | `''` | — | watching 观察期结束时间。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |
| `server_scan_policy_updated_at` | `TEXT` | 否 | `''` | — | 临时文件夹扫描策略最后变更时间。 | traveler_assistant/order_index.py#L883-904（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方）<br>traveler_assistant/order_index.py#L996-1007（表级 schema 证据；字段列由该表 CREATE/ALTER 定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_temporary_orders_1` → (temporary_id)；`sqlite_autoindex_temporary_orders_2` → (source_folder)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。

已见类别/状态值：`processing_status`：未处理, 处理中, Traveler 已生成, 已人工处理, 处理失败（当前已见值，非穷举；证据 traveler_assistant/order_index.py:1167,4928,5012,4837,6667）；`outbound_status`：未出库, 出库状态未知, 已出库（当前已见值，非穷举；证据 traveler_assistant/order_index.py:1168,4929,5013,5044）；`traveler_status`：未生成, 已生成（完整；证据 traveler_assistant/order_index.py:892,5010,5041）；`server_scan_policy`：watching, permanent（当前已见值，非穷举；证据 traveler_assistant/order_index.py:4491,4506,4779）

## `business_cache` {#table-business_cache}

用途：通用业务缓存，按缓存名和固定 value key 保存 JSON。

源码归属与读写：traveler_assistant/database.py#L774-789、819-858；traveler_assistant/core.py#L262-301

Schema 定义：traveler_assistant/database.py#L166-177。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `cache_name` | `TEXT` | 否 | `无` | 1 | 缓存命名空间，例如 factory_names、aimes_orders、material_assignments。 | traveler_assistant/database.py#L166-177（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `cache_key` | `TEXT` | 否 | `无` | 2 | 命名空间内的键；当前通用写入固定为 value。 | traveler_assistant/database.py#L166-177（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `value_json` | `TEXT` | 否 | `无` | — | 缓存值的 JSON 文本；结构由 cache_name 决定。 | traveler_assistant/database.py#L166-177（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 缓存写入/更新时间（记录时间）。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L166-177（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_business_cache_1` → (cache_name, cache_key)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `hardware_items` {#table-hardware_items}

用途：工厂单级五金投影事实；AICNC 自动五金和人工五金共表，用 source_type 区分。

源码归属与读写：traveler_assistant/hardware_facts.py#L47-99（自动五金替换）；traveler_assistant/order_workflow.py#L2951-3010（人工五金）；traveler_assistant/inventory.py#L2171-2485（读取/人工修复）

Schema 定义：traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 五金投影行主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 所属工厂单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `scope` | `TEXT` | 否 | `'factory_order'` | — | 五金事实范围；当前替换逻辑固定 factory_order。（根据 schema 与调用上下文解释）；已见值非穷举。 | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `product_code` | `TEXT` | 否 | `''` | — | 库存商品 SKU/本地映射后的代码。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `name` | `TEXT` | 否 | `''` | — | 五金名称。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `spec` | `TEXT` | 否 | `''` | — | 五金规格/尺寸。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `quantity` | `REAL` | 否 | `0` | — | 五金数量。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `unit` | `TEXT` | 否 | `''` | — | 数量单位。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_type` | `TEXT` | 否 | `'aicnc'` | — | 来源类型；源码确认 aicnc（自动）与 manual（人工）。；已见值非穷举。 | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_path` | `TEXT` | 否 | `''` | — | 来源报表/文件路径。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `active` | `INTEGER` | 否 | `1` | — | 当前有效投影标志；源码写入 1。 | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `remarks` | `TEXT` | 否 | `''` | — | 备注/修复或人工说明。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 该投影行记录更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_code` | `TEXT` | 否 | `''` | — | 报表或来源系统中的原始五金代码；与 product_code 分开保存。 | traveler_assistant/database.py#L263-280（source_code 是兼容迁移列）；traveler_assistant/hardware_facts.py#L47-105（表级 schema 证据；字段列由该表定义，读写见本表上方） |

SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `hardware_source_decisions` {#table-hardware_source_decisions}

用途：用户确认后的五金来源选择/锁定记录，按工厂单一条。

源码归属与读写：traveler_assistant/hardware_source_decisions.py#L11-48（只读加载、确认写入）；traveler_assistant/order_index.py#L8701-8709（预览提案）

Schema 定义：traveler_assistant/database.py#L144-147。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `factory_order` | `TEXT` | 是 | `无` | 1 | 五金来源决定所属工厂单，主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L144-147（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `decision_json` | `TEXT` | 否 | `无` | — | 用户确认的五金来源决定 JSON；源码未约束内部键和值全集。 | traveler_assistant/database.py#L144-147（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_hardware_source_decisions_1` → (factory_order)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `hardware_source_versions` {#table-hardware_source_versions}

用途：每个工厂单当前自动五金投影的内容指纹、来源路径和行数版本。

源码归属与读写：traveler_assistant/hardware_facts.py#L74-98（比较、替换、写版本）；:144-162（row_count=0 语义）

Schema 定义：traveler_assistant/database.py#L148-155。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `factory_order` | `TEXT` | 是 | `无` | 1 | 当前自动五金版本所属工厂单，主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L148-155（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `无` | — | 工厂单所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L148-155（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `fingerprint` | `TEXT` | 否 | `无` | — | 自动五金业务字段集合的 SHA-256 内容指纹。 | traveler_assistant/database.py#L148-155（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_paths_json` | `TEXT` | 否 | `无` | — | 生成该版本的来源路径 JSON 数组。 | traveler_assistant/database.py#L148-155（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `row_count` | `INTEGER` | 否 | `无` | — | 该版本自动五金投影行数；0 表示已完成读取但没有自动五金。 | traveler_assistant/database.py#L148-155（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 版本记录更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L148-155（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_hardware_source_versions_1` → (factory_order)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `inventory_operations` {#table-inventory_operations}

用途：库存浏览器操作的意图/结果日志，属于操作元数据，不是生产或出库事实。

源码归属与读写：traveler_assistant/inventory.py#L2690-2817（prepare/update/JSON 解码）；:3914-3970（出库操作状态机）；:3088-3097（本地提交）

Schema 定义：traveler_assistant/database.py#L310-325。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `operation_id` | `TEXT` | 是 | `无` | 1 | 由操作类型、订单、工厂单集合和 payload 指纹计算的幂等操作 ID，主键。 | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `operation_kind` | `TEXT` | 否 | `无` | — | 操作种类；当前 production、shipment、outbound 已在调用点确认，非穷举。；已见值非穷举。 | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 操作所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `factory_orders_json` | `TEXT` | 否 | `'[]'` | — | 参与操作的工厂单号列表 JSON。（根据 schema 与调用上下文解释）；已见值非穷举。 | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `payload_json` | `TEXT` | 否 | `'{}'` | — | 操作意图/输入 payload JSON；生产草稿会剔除 batch_number/production_time 后参与身份指纹。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `payload_fingerprint` | `TEXT` | 否 | `无` | — | 规范化身份 payload 的 SHA-256 指纹。 | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `'prepared'` | — | 操作状态；当前调用点确认 prepared、external_confirmed、local_committed、verification_required、partial_external_confirmed 等，非穷举。；已见值非穷举。 | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `document_results_json` | `TEXT` | 否 | `'[]'` | — | 逐单外部结果列表 JSON；由 decoded_results 解码为字典列表。；已见值非穷举。 | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `attempt_count` | `INTEGER` | 否 | `0` | — | 浏览器/外部操作尝试次数；increment_attempt 时递增。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `last_error` | `TEXT` | 否 | `''` | — | 最近一次错误文本，空串表示没有记录错误。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 操作意图首次记录时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 操作日志最后更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L310-325（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_inventory_operations_1` → (operation_id)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `inventory_resolution_rules` {#table-inventory_resolution_rules}

用途：库存名称到 SKU 的持久化映射或全局忽略规则。

源码归属与读写：traveler_assistant/database.py#L539-640（旧 JSON 迁移）；traveler_assistant/inventory.py#L1800-2080、2500-2687（读取/写入映射和忽略）

Schema 定义：traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 映射/忽略规则主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `rule_type` | `TEXT` | 否 | `无` | — | 规则类别，仅 mapping 或 ignore。 | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_name` | `TEXT` | 否 | `无` | — | 来源材料/五金名称，保留用户或来源显示名。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `normalized_name` | `TEXT` | 否 | `无` | — | 去空白、连字符并大写后的唯一匹配名。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `product_code` | `TEXT` | 是 | `无` | — | mapping 对应库存 SKU；ignore 必须 NULL。 | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `reason` | `TEXT` | 否 | `''` | — | 忽略或人工决定的原因；非 required 决定通常必须填写。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 规则首次写入时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 规则最后更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `display_name` | `TEXT` | 否 | `''` | — | 用于界面的显示名；可与 normalized_name 不同。 | traveler_assistant/database.py#L337-354（含 CHECK 与 display_name 迁移）；traveler_assistant/inventory.py#L1595-1612（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_inventory_resolution_rules_1` → (normalized_name)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `manual_production_batch_factories` {#table-manual_production_batch_factories}

用途：人工生产批次与其工厂单的关联表。

源码归属与读写：traveler_assistant/production.py#L454-464、496-503；:530-547（生产写入与读取）

Schema 定义：traveler_assistant/database.py#L215-221。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `batch_id` | `INTEGER` | 否 | `无` | 1 | 关联的人工生产批次 ID，联合主键成员且外键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L215-221（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `无` | — | 工厂单所属订单号，冗余保存用于查询/校验。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L215-221（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `无` | 2 | 被该生产批次覆盖的工厂单号，联合主键成员。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L215-221（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_manual_production_batch_factories_1` → (batch_id, factory_order)
SQLite schema 声明的 REFERENCES 外键：`batch_id` → `manual_production_batches.batch_id`（on delete NO ACTION）。是否强制校验取决于连接的 PRAGMA foreign_keys；当前项目没有统一开启。


## `manual_production_batch_materials` {#table-manual_production_batch_materials}

用途：人工生产批次实际消耗的订单级材料明细。

源码归属与读写：traveler_assistant/production.py#L68-90、454-489；traveler_assistant/inventory.py#L653-668（按批次构建生产材料出库预览）

Schema 定义：traveler_assistant/database.py#L222-237。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `batch_id` | `INTEGER` | 否 | `无` | 1 | 所属人工生产批次 ID，联合主键成员且外键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `无` | — | 生产材料所属订单号，冗余保存。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `material_type` | `TEXT` | 否 | `''` | 2 | 材料类型；生产代码至少使用 plywood、panel、back、edge。（根据 schema 与调用上下文解释）；已见值非穷举。 | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `color` | `TEXT` | 否 | `''` | 3 | 材料颜色/名称。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `thickness` | `TEXT` | 否 | `''` | 4 | 材料厚度文本。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `edge` | `TEXT` | 否 | `''` | 5 | 封边信息；普通板材通常为空。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `unit` | `TEXT` | 否 | `''` | 6 | 数量单位。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `quantity` | `REAL` | 否 | `0` | — | 本批次实际生产/消耗数量。 | traveler_assistant/database.py#L222-237（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_manual_production_batch_materials_1` → (batch_id, material_type, color, thickness, edge, unit)
SQLite schema 声明的 REFERENCES 外键：`batch_id` → `manual_production_batches.batch_id`（on delete NO ACTION）。是否强制校验取决于连接的 PRAGMA foreign_keys；当前项目没有统一开启。


## `manual_production_batches` {#table-manual_production_batches}

用途：人工生产批次主记录及生产状态。

源码归属与读写：traveler_assistant/production.py#L334-503（校验、记录、完成）；:530-547（旧出库迁移）

Schema 定义：traveler_assistant/database.py#L205-214。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `batch_id` | `INTEGER` | 是 | `无` | 1 | 人工生产批次自增主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `batch_number` | `TEXT` | 否 | `无` | — | 用户或系统批次编号，唯一。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `无` | — | 批次所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `production_time` | `TEXT` | 否 | `''` | — | 业务生产发生时间；源码允许草稿值，记录完成时写入。 | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source` | `TEXT` | 否 | `'manual'` | — | 批次来源；源码确认 manual、legacy-outbound-migration，非穷举。（根据 schema 与调用上下文解释）；已见值非穷举。 | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `'prepared'` | — | 批次状态；源码确认 prepared、completed，非穷举。；已见值非穷举。 | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 批次记录创建时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 批次记录更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L205-214（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_manual_production_batches_1` → (batch_number)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `material_items` {#table-material_items}

用途：订单级板材/封边材料事实，按来源路径和指纹保留投影。

源码归属与读写：traveler_assistant/order_workflow.py#L1891-1948（解析预览写入）；traveler_assistant/order_index.py#L7870-7982（Server 预览读取/比较）；traveler_assistant/inventory.py#L277-302（库存需求读取）

Schema 定义：traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 材料投影行主键；Server 分配中仅作预览行 ID，不是稳定来源身份。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 材料所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `material_type` | `TEXT` | 否 | `''` | — | 材料类型；Server 排序/业务代码确认 plywood、panel、back、edge。（根据 schema 与调用上下文解释）；已见值非穷举。 | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `color` | `TEXT` | 否 | `''` | — | 板材颜色或封边颜色。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `thickness` | `TEXT` | 否 | `''` | — | 板材厚度文本；封边通常为空。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `quantity` | `REAL` | 否 | `0` | — | 材料数量。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `unit` | `TEXT` | 否 | `''` | — | 数量单位，如 pcs 或 m，具体值取来源。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `edge` | `TEXT` | 否 | `''` | — | 封边颜色/边缘信息，封边行写入颜色。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_type` | `TEXT` | 否 | `''` | — | 材料来源投影类型；源码确认 aihouse、derived，其他值未确认。；已见值非穷举。 | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_path` | `TEXT` | 否 | `''` | — | 来源文件路径。 | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_fingerprint` | `TEXT` | 否 | `''` | — | 来源内容指纹；当前部分写入路径为空，具体生成方非本表约束。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 材料投影更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L189-204；:390-426（旧 schema 迁移）（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_material_items_1` → (order_id, material_type, color, thickness, unit, edge, source_type, source_path)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `outbound_document_factories` {#table-outbound_document_factories}

用途：出库单据与明确工厂单身份的关联，支持一个订单级材料单覆盖选定工厂单。

源码归属与读写：traveler_assistant/database.py#L95-135（确保关联）；traveler_assistant/inventory.py#L3029-3084（成功保存写关联）；traveler_assistant/order_index.py#L3121-3143、3547-3550（读取和关系维护）

Schema 定义：traveler_assistant/database.py#L298-309。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 出库单-工厂单关联行主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L298-309（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `document_number` | `TEXT` | 否 | `无` | — | 关联的出库单号，外键指向 outbound_documents.document_number。 | traveler_assistant/database.py#L298-309（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 关联工厂单所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L298-309（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `无` | — | 明确覆盖的工厂单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L298-309（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 关联创建时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L298-309（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 关联更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L298-309（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_outbound_document_factories_1` → (document_number, factory_order)
SQLite schema 声明的 REFERENCES 外键：`document_number` → `outbound_documents.document_number`（on delete CASCADE）。是否强制校验取决于连接的 PRAGMA foreign_keys；当前项目没有统一开启。


## `outbound_documents` {#table-outbound_documents}

用途：库存系统成功出库单的本地审计事实及其材料明细快照。

源码归属与读写：traveler_assistant/inventory.py#L3012-3075（成功写入）；traveler_assistant/order_index.py#L3121-3173（读取）；traveler_assistant/production.py#L198-213（按 document_type/status 过滤）

Schema 定义：traveler_assistant/database.py#L281-297。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 出库审计记录自增主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `document_number` | `TEXT` | 否 | `无` | — | 库存系统出库单号，唯一；成功返回缺失时流程会阻止直接重试。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `document_type` | `TEXT` | 否 | `''` | — | 单据业务类型；确认 production_materials、hardware 等用途，全部枚举未确认。；已见值非穷举。 | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `''` | — | 单据所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 单据备注/默认关联的工厂单号或订单级标识；精确覆盖关系以关联表为准。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `'recorded'` | — | 库存单据状态；成功写入路径为 已出库，其他系统值未穷举。；已见值非穷举。 | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source` | `TEXT` | 否 | `''` | — | 单据事实来源；成功浏览器写入为 金蝶，旧迁移为 legacy-json，非穷举。（根据 schema 与调用上下文解释）；已见值非穷举。 | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `issued_at` | `TEXT` | 否 | `''` | — | 写入 `result.get("syncedAt", "")` 的结果时间；当前成功返回缺少该键时为空，不自动等于单据签发时间或本地确认时间；不可与本地 `updated_at` 混淆。 | traveler_assistant/inventory.py#L3053-3073<br>tools/jdy_inventory.mjs#L1561-1564 |
| `source_path` | `TEXT` | 否 | `''` | — | 生成该单据的 Traveler/来源文件路径。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 本地审计记录更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `document_url` | `TEXT` | 否 | `''` | — | 库存系统单据链接。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `items_json` | `TEXT` | 否 | `'[]'` | — | 出库单材料/五金明细快照 JSON 数组。 | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `raw_fingerprint` | `TEXT` | 否 | `''` | — | 原始 Traveler/材料内容指纹，用于检测源变化。 | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `mapped_fingerprint` | `TEXT` | 否 | `''` | — | 完成 SKU 映射后的内容指纹。 | traveler_assistant/database.py#L281-297（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_outbound_documents_1` → (document_number)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `outbound_scope_decisions` {#table-outbound_scope_decisions}

用途：来料加工订单的材料/五金出库范围决定。

源码归属与读写：traveler_assistant/inventory.py#L739-863（读取/校验/写入）；:866-1013（预览应用）

Schema 定义：traveler_assistant/database.py#L355-368。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 出库范围决定主键。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `无` | — | 决定所属订单号。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `scope_type` | `TEXT` | 否 | `无` | — | 范围层级，仅 material（订单材料）或 hardware（工厂单五金）。 | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `factory_order` | `TEXT` | 否 | `''` | — | 硬件范围的工厂单号；材料范围必须为空。 | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `requirement` | `TEXT` | 否 | `无` | — | 出库要求，仅 required、customer_supplied、remainder、not_required。 | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `reason` | `TEXT` | 否 | `''` | — | 非 required 的人工决定原因；源码要求 customer_supplied/remainder/not_required 必填。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_fingerprint` | `TEXT` | 否 | `''` | — | 决定所依据材料来源指纹；当前 set_outbound_scope 写入空串，实际绑定用途未在源码确认。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 决定首次写入时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 决定最后更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L355-368（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_outbound_scope_decisions_1` → (order_id, scope_type, factory_order)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `products` {#table-products}

用途：库存商品/SKU 本地主数据及归一化检索字段。

源码归属与读写：traveler_assistant/inventory.py#L1615-1735、1778-1850（读取/替换）；:2508-2687（SKU 映射查询）

Schema 定义：traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `category` | `TEXT` | 否 | `''` | — | 库存商品类别。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `code` | `TEXT` | 是 | `无` | 1 | 库存商品 SKU，主键。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `name` | `TEXT` | 否 | `''` | — | 库存商品名称。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `spec` | `TEXT` | 否 | `''` | — | 库存商品规格。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `status` | `TEXT` | 否 | `''` | — | 库存商品状态；迁移校验确认 启用 表示可用，其他值未穷举。；已见值非穷举。 | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `remark` | `TEXT` | 否 | `''` | — | 商品备注。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `unit` | `TEXT` | 否 | `''` | — | 商品单位。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `normalized_code` | `TEXT` | 否 | `无` | — | 归一化 SKU 检索键。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `normalized_name` | `TEXT` | 否 | `无` | — | 归一化名称检索键。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `normalized_spec` | `TEXT` | 否 | `无` | — | 归一化规格检索键。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `normalized_category` | `TEXT` | 否 | `无` | — | 归一化类别检索键。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `normalized_remark` | `TEXT` | 否 | `无` | — | 归一化备注检索键。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `cost_price` | `REAL` | 是 | `无` | — | 商品预计采购/成本价；允许 NULL 表示资料缺失，不应当作 0。 | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `brand` | `TEXT` | 否 | `''` | — | 商品品牌；后加列默认空串。（根据 schema 与调用上下文解释） | traveler_assistant/inventory.py#L1746-1775（建表、cost_price 兼容迁移）；traveler_assistant/database.py#L593-607（业务库校验）（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_products_1` → (code)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `server_material_allocations` {#table-server_material_allocations}

用途：Server 材料来源行到订单的分配记录，用于预览期余量和确认写回。

源码归属与读写：traveler_assistant/order_index.py#L7785-7830、8750-8833、9423-9605（读取/增量分配/确认）；:9766-9797（预览库写回生产库）

Schema 定义：traveler_assistant/database.py#L238-259。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | Server 材料分配行主键；不作为稳定来源身份。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_material_id` | `INTEGER` | 否 | `无` | — | 预览中对应 material_items 行 ID。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_path` | `TEXT` | 否 | `''` | — | Server 材料来源文件路径。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_material_key` | `TEXT` | 否 | `''` | — | 由来源路径和材料字段计算的稳定 v2 身份指纹。 | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `material_type` | `TEXT` | 否 | `''` | — | 来源材料类型。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `color` | `TEXT` | 否 | `''` | — | 来源材料颜色。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `thickness` | `TEXT` | 否 | `''` | — | 来源材料厚度。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `unit` | `TEXT` | 否 | `''` | — | 来源材料单位。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `edge` | `TEXT` | 否 | `''` | — | 来源封边信息。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_quantity` | `REAL` | 否 | `0` | — | 该来源材料行的总量。 | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `order_id` | `TEXT` | 否 | `无` | — | 分配到的订单号。 | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `allocated_quantity` | `REAL` | 否 | `0` | — | 已分配到该订单的数量。 | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `source_fingerprint` | `TEXT` | 否 | `''` | — | 来源材料内容指纹。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 分配记录创建时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 分配记录更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L238-259（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_server_material_allocations_1` → (source_path, source_material_key, order_id)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `server_material_preview_scopes` {#table-server_material_preview_scopes}

用途：本次 Server 材料预览覆盖的来源文件夹集合。

源码归属与读写：traveler_assistant/order_index.py#L8678-8686（预览写入）；:9468-9473（确认读取）

Schema 定义：traveler_assistant/database.py#L260-262。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `source_folder` | `TEXT` | 是 | `无` | 1 | 本次 Server 预览的来源文件夹路径，主键。 | traveler_assistant/database.py#L260-262（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_server_material_preview_scopes_1` → (source_folder)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `workflow_metadata` {#table-workflow_metadata}

用途：工作流级键值元数据，保存迁移标记和迁移摘要。

源码归属与读写：traveler_assistant/database.py#L539-640、697-800（迁移标记/摘要写入）；:555-566、736-739（读取/更新）

Schema 定义：traveler_assistant/database.py#L166-170。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `key` | `TEXT` | 是 | `无` | 1 | 工作流元数据键，主键。 | traveler_assistant/database.py#L166-170（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `value` | `TEXT` | 否 | `''` | — | 元数据字符串；当前迁移标记/摘要常编码为 JSON。 | traveler_assistant/database.py#L166-170（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `updated_at` | `TEXT` | 否 | `无` | — | 元数据更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/database.py#L166-170（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_workflow_metadata_1` → (key)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## 助手运行库（assistant-runtime.sqlite3）

运行库路径由 `runtime_database_path(state_dir)` 返回；`agent_usage` 和 `learned_commands` 只属于该运行库。本页不把它们归入中央业务库，也不把助手用量/命令记忆当作订单、生产或出库事实。

## `agent_usage` {#table-agent_usage}

用途：助手调用用量审计记录，不是订单或库存业务事实。

源码归属与读写：traveler_assistant/runtime_store.py#L63-68（写入）；:89-120（读取/汇总）

Schema 定义：traveler_assistant/runtime_store.py#L43-58。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `id` | `INTEGER` | 是 | `无` | 1 | 助手用量记录自增主键。（根据 schema 与调用上下文解释） | traveler_assistant/runtime_store.py#L43-58（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 助手用量记录产生时间（记录时间，不是业务事件时间）。 | traveler_assistant/runtime_store.py#L43-58（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `model` | `TEXT` | 否 | `无` | — | 产生该次用量的模型标识。（根据 schema 与调用上下文解释） | traveler_assistant/runtime_store.py#L43-58（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `input_tokens` | `INTEGER` | 否 | `无` | — | 该次调用输入 token 数；CHECK >= 0。 | traveler_assistant/runtime_store.py#L43-58（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `output_tokens` | `INTEGER` | 否 | `无` | — | 该次调用输出 token 数；CHECK >= 0。 | traveler_assistant/runtime_store.py#L43-58（表级 schema 证据；字段列由该表定义，读写见本表上方） |

SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。


## `learned_commands` {#table-learned_commands}

用途：助手对归一化自然语言命令的动作和参数记忆。

源码归属与读写：traveler_assistant/runtime_store.py#L70-97（写入/读取）

Schema 定义：traveler_assistant/runtime_store.py#L43-59。

| 字段 | SQLite 类型 | 可空 | 默认值 | PK 位置 | 中文含义 | 证据 |
| --- | --- | --- | --- | ---: | --- | --- |
| `normalized_text` | `TEXT` | 是 | `无` | 1 | 归一化后的用户命令文本，主键。（根据 schema 与调用上下文解释） | traveler_assistant/runtime_store.py#L43-59（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `action` | `TEXT` | 否 | `无` | — | 命令路由动作名。（根据 schema 与调用上下文解释） | traveler_assistant/runtime_store.py#L43-59（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `arguments_json` | `TEXT` | 否 | `无` | — | 动作参数字典 JSON。 | traveler_assistant/runtime_store.py#L43-59（表级 schema 证据；字段列由该表定义，读写见本表上方） |
| `created_at` | `TEXT` | 否 | `无` | — | 记忆命令写入/更新时间。（根据 schema 与调用上下文解释） | traveler_assistant/runtime_store.py#L43-59（表级 schema 证据；字段列由该表定义，读写见本表上方） |

唯一约束/索引：`sqlite_autoindex_learned_commands_1` → (normalized_text)
SQLite schema 声明外键：无；order_id/factory_order 等是应用层关联。当前项目没有统一开启 PRAGMA foreign_keys=ON。



## 维护边界

本字典是源码与当前实际 schema 的静态快照。新增列、ALTER、迁移、预览库恢复或 JSON 契约变化后，应重新读取 SQLite 元数据并补充源码证据；不要仅凭表名推断当前业务含义。
