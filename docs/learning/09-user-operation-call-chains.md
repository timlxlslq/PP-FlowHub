# PP FlowHub 用户操作与业务调用链全解

> **学习快照（2026-09）**：本文依据阶段性源码整理调用链，行号和部分入口会变化；当前行为以 [系统架构](../architecture/system-architecture.md)、[业务规则](../business-rules.md) 和 [发布流程](../release-testing.md) 及当前源码为准，不把本文当作当前待办或授权。

本文回答一个固定问题：**用户在 App 里做了一件事后，代码从哪里开始、传入什么、下一步调用谁、最终读写什么？**

### 2026-09-18：展开订单为何不应拖慢消息区

订单中心由 `OrderDashboardView` 组合工具栏、`OrderDashboardActivityView` 和 `OrderDashboardListView`。展开订单、选中工厂单及订单弹窗状态归列表所有；详情仍经 `loadOrderDetailFromDatabase` → `runOrder(detail)` 读取本地数据库。消息视图不观察整个 `AppModel`，只接收 `OrderDashboardActivityInput` 值输入，并通过 `.equatable()` 在消息数据未变化时跳过 body 重算。该输入是临时传值，不是业务缓存；新消息、进度、失败和计时起点仍会改变输入。消息自己的悬停、宽度和计时更新仍正常工作。

`@State` 是视图自己的状态，`@ObservedObject` 会接收对象发布的变化。因此仅把一个长 body 拆成若干计算属性不能隔离更新；仅拆 View 但都观察大模型，也不能阻止无关字段通知。这里将局部状态下移，并为顶部建立明确的数据边界。SwiftUI 的 body 重算、布局和屏幕绘制是不同阶段，测试只对实际测到的阶段作结论。

另一个隐蔽问题是 `URL(fileURLWithPath:)` 可能为判断目录而查询文件系统。原来的消息文本和待处理分组仅需要文件名，却在主线程触发 Server 路径的 `lstat`。现在显示名称/父路径使用 `displayPathName`、`displayParentPath` 的字符串处理；真正打开、读取文件的动作仍使用文件 API。`OrderDashboardClickContainer` 保留 SwiftUI 内容，以不含子视图和尺寸约束的 `OrderDashboardClickReceiver` 接收单击/双击，避免在点击层嵌套 `NSHostingView`。

回归检查实际挂载消息视图，比较无关材料/选中订单变化前后的 body 计数，并验证真实进度和失败更新；安装版还需检查 PP0064 展开、收起、滚动、单/双击及系统布局异常。单纯编译通过不能证明现场卡顿或崩溃已经消失。

文档依据 2026-08-30 当前源码整理。函数级全集请配合以下自动生成文档：

- `05-file-map.md`：每个文件的中文职责。
- `06-python-symbol-reference.md`：全部一方 Python 类型、函数和方法。
- `07-swift-symbol-reference.md`：全部 App 类型、函数、方法和重要计算属性。
- `08-support-test-symbol-reference.md`：全部测试、脚本和工具过程。

## 1. 先理解三种证据

本文明确区分：

- **已确认事实**：当前源码中存在直接调用、参数、分支或测试契约。
- **静态分析结果**：生成器能看到直接调用，但动态类型、闭包和条件分支可能使运行路径不同。
- **运行时结果**：只有真实命令、操作日志、SQLite、Excel 或外部系统返回才能证明本次操作实际执行到哪一步。

因此，“函数 A 的源码里调用了函数 B”不等于每次都调用 B；必须继续看分支条件和本次输入。

## 2. 全项目统一入口

### 2.1 App 到业务引擎的主链

```text
用户点击/输入
  → macos/*.swift 的 View 按钮或 onAppear
  → macos/TravelerAssistant.swift: AppModel 某个操作函数
  → AppModel.runOrder / runInventory，或 AssistantView.executeAssistantTask
  → scripts/pp-flowhub
  → traveler_assistant/order_workflow.py: main
       或 traveler_assistant/inventory.py: inventory_main
       或 traveler_assistant/assistant_cli.py: main
  → 对应 Python 业务函数
  → workflow.sqlite3 / Excel / Server / AIMES / 金蝶云库存
  → stdout 最终 JSON + stderr 逐步 progress JSONL
  → Swift 解析并更新 @Published 页面状态
```

### 2.2 三个进程入口的参数合同

| App 入口 | 子进程参数 | Python 入口 | 标准输出 | 标准错误 |
| --- | --- | --- | --- | --- |
| `AppModel.runOrder(arguments,input,...)` | `pp-flowhub order <arguments>`；可把内存预览 JSON 写到 stdin | `order_workflow.main(argv)` | 最终结果对象；失败为 `fatal` | `progress` 事件和诊断 |
| `AppModel.runInventory(arguments,...)` | `pp-flowhub inventory <arguments>` | `inventory.inventory_main(argv)` | 最终结果对象；失败为 `fatal` | 浏览器实时页面动作、阶段进度和诊断 |
| `executeAssistantTask(task,approved)` | `pp-flowhub assistant <text> [--approve]` | `assistant_cli.main(argv)` | `status/result_type/preview/error/token_usage` | 助手后台诊断 |

三个入口都通过 `scripts/pp-flowhub` 完成同一件事：选择打包版或虚拟环境 Python，设置 `PYTHONPATH`，再以 `python -m` 启动模块。Shell 脚本本身不包含业务规则。

### 2.3 统一运行参数从哪里来

1. Swift `AppModel` 默认保存 `sourceRoot`、`orderRoot`、`backupRoot`、初始日期和账号名。
2. `AppModel.loadSettings()` 从 `~/Documents/pp-flowhub/data/settings.json` 读取本机配置。
3. `runOrder()` / `runInventory()` 通过 `environmentForOperation(operationID)` 传递当前操作编号与运行环境。
4. Python `Config.load_settings()` 再读取同一设置文件；CLI 显式参数优先覆盖设置。
5. `Config.prepare_storage()` 建立本机状态目录，并由 `ensure_schema()` 创建或事务升级中央 `workflow.sqlite3`；需要外键的应用连接在事务前开启约束。

密码边界：设置 JSON 只保存用户名；AIMES 和库存密码通过 macOS Keychain 读取，不能把明文密码写进日志或文档。

## 3. App 启动、页面与本地状态

### 3.1 App 启动

入口：`macos/TravelerAssistant.swift: TravelerAssistantApp`。

调用链：

```text
TravelerAssistantApp 创建 @StateObject AppModel
  → AppModel.init()
      → loadSettings()
      → OperationLogWriter.setEnabled(operationLogEnabled)
      → OperationLogWriter.record("app.started", ...)
      → loadTodoItems()
      → loadAssistantUsage()
  → WindowGroup 根据 AppSection 显示 AssistantView / OrderDashboardView / TodoView / SettingsView
```

输入：无显式业务参数；读取本机设置和待办文件。

副作用：记录 App 启动日志。启动本身不会自动写 Server、AIMES 或库存系统。订单看板出现后，`OrderDashboardView.onAppear` 才调用 `startOrderDashboard()`。

### 3.2 设置保存

入口：设置页按钮 → `AppModel.saveAllSettings()` / `saveSettings()`。

主要输入：

- `initialDate`
- `sourceRoot`
- `orderRoot`
- `backupRoot`
- `jdyUsername`
- `aimesUsername`
- `operationLogEnabled`
- 两套密码输入（分别走 Keychain）

调用链：

```text
SettingsView 按钮
  → AppModel.saveAllSettings()
      → saveSettings()
          → JSONSerialization.data(...)
          → Data.write(settingsURL, .atomic)
      → saveJdyPassword() / saveAimesPassword()
          → macOS Security/Keychain 命令
```

输出：页面 `settingsStatus`。设置文件写入是原子替换；密码不进入 JSON。

### 3.3 待办新增、修改、完成与删除

入口分别是 `addTodo(content,deadline)`、`updateTodo(item,content,deadline)`、`toggleTodoCompletion(item)`、`deleteTodo(item)`。

共同下一跳：`saveTodoItems()` → `JSONEncoder.encode(todoItems)` → 原子写入 `data/todo-items.json`。

业务规则：空内容不保存；完成状态通过 `completedAt` 是否为空表示；日期按 ISO 8601 编解码。

### 3.4 操作日志

App 侧入口：`OperationLogWriter.record()`；Python 侧入口：`configure_operation_log()` → `OperationLogger.event()`。

写入位置：`data/operation-log.jsonl`。每一行是独立 JSON，使用同一 `operation_id` 关联 Swift、Python 和浏览器阶段。

`OperationLog.swift` 和 `operation_log.py` 都执行敏感键/文本脱敏。关闭日志只影响后续普通记录；关闭动作本身使用强制记录留下审计事实。

### 3.5 数据库备份

入口：设置页“立即备份”或订单看板启动后的每日检查。

```text
AppModel.performBackup()
  → runOrder(["backup-now"])
  → scripts/pp-flowhub order backup-now
  → order_workflow.main()
  → backup.perform_backup(config)
      → database.ensure_schema(...)
      → SQLite backup 到临时文件
      → 计算 fingerprint
      → os.replace() 原子落盘
      → _apply_retention()
```

输入：`Config.workflow_database`、`Config.database_backup_root` 和当前日期。

输出：备份路径、指纹和状态。`backup_status()` 只检查最近成功证据；`perform_backup()` 才实际写文件。

## 4. 助手命令

### 4.1 从文字/语音到结构化动作

入口：`AssistantView` 的执行按钮或语音完成回调 → `AppModel.runAssistantCommand(approved:false)`。

输入：`assistantInput` 文本。语音文本先通过 `canonicalSpeechCommand(text)` 把“P P 三十五”等表达规范化为订单号。

```text
runAssistantCommand(false)
  → 把 AssistantTaskItem 加入队列
  → processNextAssistantTask()
  → executeAssistantTask(task,false)
  → Process: pp-flowhub assistant <task.text>
  → assistant_cli.main(argv)
      → command_router.parse_local_command(text)
      → 若返回 None：RuntimeStore.learned_command(normalized_text)
      → 仍未命中：agent_runner.route_with_agent(text)
      → tool_gateway.execute_local_command(config,command,approved=false)
```

本地解析器输入是原始文本，输出 `LocalCommand(action, arguments, requires_approval)`；它不读写业务系统。Agent 只负责理解模糊意图，最终动作仍必须进入 Gateway。

### 4.2 Gateway 的读写边界

`tool_gateway.execute_local_command(config,command,approved)` 支持：

| action | 关键参数 | 下一跳 | 是否写入 |
| --- | --- | --- | --- |
| `list_orders` | 无 | `order_workflow.list_order_folders(config)` | 否 |
| `preview_order` | `order_id` | `_order_folder()` → `preview_order()` → `preview_payload()` | 预览解析可持久化已验证中央事实；不生成 Traveler |
| `check_inventory_stock` | `order_id` | `inventory.check_database_stock()` | 只读库存查询，不出库 |
| `generate_traveler` | `order_id` | 首次只返回预览；批准后 `generate_order_traveler()` | 是，生成 Excel |
| `update_traveler` | `order_id` | 首次只返回预览；批准后 `update_order_traveler()` | 是，备份并更新 Excel |
| `add_manual_hardware` | `order_id/factory_name/product_code/quantity/remarks` | `preview_manual_hardware()`；批准后 `add_manual_hardware()` | 是，写中央 SQLite，存在 Traveler 时同步更新 |

第二次确认入口：`runAssistantCommand(approved:true)` → 相同任务文本加 `--approve` → Gateway 重新解析和校验，不能把第一次预览当作永久授权。

## 5. 订单看板启动链

入口：`OrderDashboardView.onAppear` → `AppModel.startOrderDashboard()`。

```text
startOrderDashboard()
  → loadOrderDashboardCache()
      → beginDashboardOperation("sync", "读取本地订单缓存")
      → runOrder(["list-index"])
      → order_workflow.main(command="list-index")
      → order_index.list_order_index(config)
      → OrderIndexStore.summaries()/active_issues()/...
  → applyDashboardObject(local cache)
  → runDailyBackupAfterLocalCache()
      → order backup-status
      → 必要时 order backup-now
  → syncDashboardAimes(force:false, scanServerAfter:true)
      → AIMES 完成或失败后 scanDashboardServer(background:true)
```

已确认边界：本地 `list-index` 只负责尽快显示已有事实；它不应伪装成 AIMES 或 Server 的最新结果。AIMES 与 Server 是后续两个独立阶段，分别记录耗时。

## 6. AIMES 同步

### 6.1 App 参数

- 自动启动检查：`syncDashboardAimes(force:false)` → `sync-aimes --aimes-if-needed`。
- 用户点击再次获取：`syncDashboardAimes(force:true)` → `sync-aimes --refresh-aimes`。

### 6.2 Python 调用链

```text
order_workflow.main(command="sync-aimes")
  → order_index.sync_aimes_index(config, force, if_needed)
      → reconcile_outbound_statuses(config, store)
      → load_aimes_order_cache(config)
      → 判断今天是否已成功同步
      → core.refresh_aimes_recent_orders(...)
          或 refresh_aimes_recent_orders_and_verify(...)
          → tools/aimes_lookup.mjs
          → Playwright/AIMES 页面
      → _partition_aimes_rows(...)
      → _persist_valid_aimes_mapping(...)
      → OrderIndexStore.upsert_order()/upsert_aimes_factory()
      → _verify_missing_aimes_factories(...)
      → OrderIndexStore.record_run()/commit()
```

输入：`force`、`if_needed`、AIMES 用户名、Keychain 密码、批量上限和当前缓存。

2026-09-17 核验范围：Python 先排除已关联 `completed` 生产批次的工厂单（按订单号和工厂单号共同匹配），浏览器再排除最近 50 条已读到的工厂单，仅对剩余未生产工厂单逐单查询。`NOT EXISTS` 表示“没有对应的已完成生产记录”；生产判断与看板相同，不用已出货文案或 Server 文件推断。删除结果落库前再次使用相同筛选，已生产记录保留本地事实。所有工厂单均已生产时仍读最近 50 条，以发现新增任务。

输出：`orders`、`aimes` 状态、warnings、ignored/assigned 列表、stage durations 和 operation trace。

关键边界：`sync_aimes_index()` 只刷新 AIMES 身份，不扫描 Server。格式异常行保存在 `aimes_review_rows`，并由读层投影为待人工确认的警告；它跳过有效业务写入。失败时可以返回缓存，但缓存不能表述成刚刚在线验证成功。

## 7. Server 扫描、预览与确认

### 7.1 扫描变化

入口：用户点击“扫描 Server”或 AIMES 启动链结束 → `scanDashboardServer(background)`。

```text
scanDashboardServer()
  → runOrder(["scan-server"])
  → order_workflow.main(command="scan-server")
  → order_index.scan_server_changes(config)
      → _clear_stale_server_pending_state(...)
      → _server_snapshot(config,store)
      → 比较 source_files 基线与当前目录/文件元数据
      → 未确认 XML 仅进入本次内存待处理结果
      → 不保存优化证据、优化时间或 XML 基线
      → 返回 changes / active issues / scan_stats / stage durations
```

输入：设置中的 Server 根目录、AIMES 当前工厂单范围、已出库状态和上次处理基线；普通临时及补单文件夹的人工处理通过独立的三天 XML 观察策略登记。

写入边界：扫描只做元数据发现，不解析 Excel、不保存优化 XML 信息、不推进状态或已处理基线；可清理失效待处理状态和维护扫描策略。材料与工厂单的确认结果及 XML 基线在后续确认事务中保存。

#### 现场案例：已优化但材料为空（2026-09-15，PP0086）

- 修复前 `order_index.py` 的优化证据扫描会依据 `optimization_artifacts` 更新 `factory_orders.stage`；看板再汇总该字段。因此，看到“已优化”不能证明 `material_items` 和 `hardware_items` 已确认写入。
- 本次修复前，PP0086 的两个工厂单都有优化 XML 证据，但材料和五金均为 0 条。现有日志有两次 Server 预览完成记录；预览中的写表日志也不能单独证明正式落库，须核对目标连接和中央数据库。
- 修复采用备份 → 单文件夹内存预览 → 检查归属、材料校验和五金映射 → `confirm-server-material-preview-memory --confirm-write` → 数据库及安装 App 详情回读。结果为 5 条材料、6 条五金，未新增人工生产批次或出库单。
- 不应仅把 `optimized` 改为 0 来补材料：保留的 XML 证据可能在下次扫描恢复该标记。材料缺失应走预览和确认写入流程。
- 后续按用户要求修改业务逻辑：扫描和取消预览不再保存优化文件信息；只有材料确认写入后，才设置对应工厂单的优化状态。XML 作为确认时的来源追溯信息，不能单独推动状态。实际规则见 [业务规则](../business-rules.md)。

### 7.2 选择文件夹并生成内存预览

入口：待处理中心“预览并逐单确认” → `processPendingServerChanges()`。

输入：选中的 `folderPath[]`，默认 `include_hardware=true`。

```text
processPendingServerChanges()
  → runOrder(["preview-server-changes", "--include-hardware", "true",
              "--server-folder", folder1, ...])
  → order_workflow.main()
  → order_index.preview_server_changes(config, selected_folders, include_hardware)
      → 复制 workflow.sqlite3 到 sqlite3 :memory:
      → inventory.bootstrap_product_database(stage_config)
      → sync_order_index(stage_config, selected_folders=..., validate_selected_orders=true)
      → _server_preview_payload(...)
      → _refresh_server_preview_hardware(...)
      → 返回 server_write_preview + operation_timing
  → AppModel.presentServerWritePreview(object)
```

已确认边界：正式数据库不会被预览污染。预览对象只保存在当前 App 内存；重新启动 App 后应重新预览。

五金变化展示：`_server_preview_payload()` 从正式数据库的 `hardware_items` 查询工厂单是否已有五金记录，返回 `has_existing_hardware`。Swift 的 `ServerWriteOrderPreview.existingHardwareChanges` 只展示这些工厂单的变化；首次写入仍展示上方五金明细。原始 `hardware_changes` 和 `write_records` 保持完整，因为“是否显示对比”和“是否需要写入”是不同判断，不能为隐藏界面差异而清空写入依据。

### 7.3 确认一个工厂单

入口：`confirmServerWrite(orderID,factoryOrder)`。

输入：内存 `preview.payload`、人工确认的 `orderID`、`factoryOrder`、`--confirm-write`。

```text
confirmServerWrite(...)
  → 把 payload 写入 runOrder(..., input: stdin JSON)
  → order confirm-server-preview-memory --order-id ... --factory-order ... --confirm-write
  → order_workflow.main() 读取 sys.stdin
  → order_index.confirm_server_preview_memory(...)
  → _confirm_memory_preview(...)
      → 重新校验 payload、订单/工厂单身份和写入授权
      → 同一事务写材料、所选工厂单状态、优化元数据和预览版本的 XML 基线
      → 按实际已确认工厂单重新汇总订单状态；失败全部回滚
  → App 从预览中移除已确认工厂单
  → 全部完成后 refreshDashboardAfterServerWrite()
  → order list-index（仅本地刷新）
```

### 7.4 确认订单级材料和工厂单五金

入口：`confirmServerMaterialPreview(skipHardwareOrderIDs)`。

参数：stdin 内存预览、`--confirm-write`，以及零个或多个 `--skip-hardware-order <order_id>`。

下一跳：`confirm_server_material_preview_memory()` → `_confirm_memory_preview()`。来源材料先解析为唯一、当前可写的商品 SKU，并把已确认的材料类型、颜色和名义厚度绑定到商品层；Server 分配以“来源路径 + SKU”作为来源材料身份，事务中的 `material_items` 再按“订单 + SKU + 来源类型 + 来源路径”聚合，只写 `product_code`、数量和来源身份。对应工厂单五金只保存规范 SKU、已换算数量和必要归属，商品资料在读取时关联。来料加工订单可在本次确认中显式跳过五金。确认之后修改名称映射不会重绑已有订单材料。

### 7.5 登记临时或补单文件夹已人工处理

入口：待处理中心 → “已人工处理” → `FolderManualHandlingSheet` → 确认已在外部出库。

```text
scan_server_changes
  → _server_folder_handling_mode：新文件夹 + 所有相关订单工厂单已出库
  → supplemental：独立补单待处理
FolderManualHandlingSheet
  → markTemporaryFolderManual(path, referenceOrderIDs, outboundDocument)
  → order mark-temporary-manual --folder <path>
      --reference-orders-json '[]' --outbound-document ''
  → mark_temporary_folder_manual
      → 再次验证分类，阻止新的 AIMES 工厂单被绕过
      → 一个事务保存 temporary_orders、报表/XML 基线、操作记录
      → Swift 只移除这个文件夹
```

这里要区分“身份”和“参考”：内部 `temporary_id` 确定是哪一个任务，参考订单只是标签。即使两批补件都写着 PP0008，也不能用 PP0008 作为任务主键；否则会覆盖彼此，更可能覆盖正式订单。没有参考订单仍能登记，体现的是“可选输入”，不是错误或缺失数据。

补单判定用的是最近同步的有效 AIMES/出库事实。正式混单的材料归属仍按订单处理；只有满足补单条件或普通临时任务才走独立人工登记。填写的参考订单不参与这个判定，也不能借修改参考标签把未出库正式混单改为补单。

相同报表/XML 内容再次点击，称为“幂等”：不会多扣一次库存，也不会把完成时间和观察期不断向后推。观察期发现 XML 变化后标记 `manual_pending`，待用户再次完成；正式订单的扫描期限不控制这条记录。

该入口只登记用户已经在外部完成的出库事实，不会打开库存系统或创建出库单。隔离验证见 `tests/test_folder_manual_handling.py`。

## 8. 待处理中心与人工归属

待处理中心由 `buildPendingCenterItems(serverChanges,currentIssues,aimesReviews)` 合并三个独立来源。

常见入口：

| UI 动作 | CLI | Python 下一跳 | 写入 |
| --- | --- | --- | --- |
| 自动处理当前问题 | `order auto-resolve-issue --issue-key` | `auto_resolve_current_issue()` | 视问题类型更新 SQLite |
| 人工确认订单归属 | `order resolve-issue --issue-key [--order-id]` | `resolve_current_issue()` | 是 |
| 忽略 AIMES 记录 | `order ignore-aimes --ignore-key ...` | `ignore_aimes_factories()` | 是 |
| 恢复 AIMES 忽略 | `order restore-aimes-ignore --ignore-key ...` | `restore_aimes_factories()` | 是 |
| 把 AIMES 工厂单指派给订单 | `order assign-aimes-order --ignore-key X --order-id Y` | `assign_aimes_factory_order()` | 是 |
| 撤销 AIMES 指派 | `order restore-aimes-assignment --ignore-key X` | `restore_aimes_order_assignment()` | 是 |

所有人工身份写入都以当前 `issue_key/ignore_key` 为定位证据；不能只凭页面显示文本猜测数据库行。

## 9. 订单详情、安装安排和成本

### 9.1 读取订单详情

入口：点击看板订单 → `loadOrderDetailFromDatabase(item)`。

参数：`item.orderId`。

```text
loadOrderDetailFromDatabase(item)
  → order detail --order-id <id>
  → order_workflow.main()
  → order_details.order_detail(config,order_id)
      → 查询 workflow.sqlite3 的订单、工厂单、material_items、hardware_items 等事实
      → material_items 按 product_code JOIN products，投影材料类型、颜色、名义厚度和单位
      → _panel_products_by_name()/产品图片映射
  → Swift applyOrderPreview(...) 组装详情页模型
```

这里读取的是中央事实，不重新解析 Server 文件，也不把 Traveler 当事实源。材料表中的 SKU 是已确认身份；商品 JOIN 是属性投影，不是再次按名称做映射。

### 9.2 保存备注和安装日期

入口：`saveOrderAnnotations(orderID,userNote,plannedDays,actualDays)`。

输入：订单号、备注、计划安装日数组、实际安装日数组；每个日期项包含 `date` 和 `installer`。

下一跳：`order save-order-annotations` → `order_index.save_order_annotations()` → `OrderIndexStore.save_order_annotations()` → SQLite commit → 返回更新后的 `list_order_index()` payload。

### 9.3 计算与导出成本

入口：`calculateSelectedOrderCost(export)`。

```text
export=false → order cost --order-id
export=true  → order cost-export --order-id
  → order_workflow.main()
  → costing.calculate_order_cost(config,order_id)
      → 读取中央材料/五金事实；材料按 product_code JOIN products
      → ProductDatabase / cost_price（SKU 是成本身份）
      → _aggregate_material_rows()
      → _display_cost_lines()（仅展示排序/聚合投影）
  → export 时继续 export_order_cost()
      → _excel_row() / _style_rows()
      → 保存并返回 export_path
```

原始成本 `lines` 和 App 展示用 `factory_lines` 是不同合同；不要为了 UI 排序改乱 Excel 需要的原始明细。

## 10. 生产流程

### 10.1 生产预览

入口：`loadProductionPreview(orderID,factoryOrders)`。

CLI 参数：`order production-preview --order-id <id> --factory-orders-json '[...]'`。

下一跳：`production.production_preview(config,order_id,factory_orders)` → `_selected_factory_rows()`、`_order_material_rows()`、`cumulative_production_materials()` → 返回每个 SKU 的总量、已消耗量和剩余量，再从 `products` 投影显示属性。`production_materials` 按 `product_code` 保存和累计历史消耗，因此商品单位、显示名或颜色文字后来变化都不会把已完成数量漏掉。

### 10.2 准备生产批次

入口：`prepareProduction(orderID,factoryOrders,materials,onResult)`。

输入：工厂单数组；材料数组只传 `{key,quantity}`。下一跳：`order prepare-production` → `production.prepare_production()` → 校验工厂单、数量、剩余量并返回内存草稿和 `request_id`，此时不写入生产记录。

准备成功不等于库存已扣，也不等于生产已完成。

### 10.3 确认生产并扣减库存

入口：`startDirectProduction(orderID,factoryOrders,materials,batchNumber)`。

```text
startDirectProduction(...)
  → inventory outbound --order-id ... --production-batch ...
      --production-materials-json [...] --factory-order ... --confirm-save
  → inventory_main()
  → inventory.run_jdy(action="outbound", production_materials=...)
      → production.cumulative_production_materials(...)
      → build_database_preview(...)
      → InventoryOperationJournal.prepare(kind="production", ...)
      → tools/jdy_inventory.mjs（逐单打开、填写、保存）
      → _persist_single_outbound_result()（每个已确认单据立即落本地）
      → InventorySyncStore.save_success(..., production_draft=...)
      → production.record_completed_production()/相关数据库事务
      → reconcile_outbound_statuses(config)
  → Swift 刷新本地订单列表
```

外部保存成功和本地生产记录成功是两个证据。若外部结果不确定，Journal 标记 `verification_required`，后续重试必须先查历史，避免重复出库。

App 的生产材料 `key` 就是已确认商品 SKU。Python 的 `production_material_code()` 在累计校验和完成写入时统一读取 `key` / `product_code`，两者同时存在但不同则报错。不能只在库存累计预览中补全 SKU，却把原始草稿的空 `product_code` 写入生产表。恢复时保留原 Journal 载荷与指纹，使用已确认单据补交本地事务；不按显示名称重新匹配，也不重新扣库存。

## 11. 出货流程

入口：订单看板“直接出货” → `startDirectOrderShipment(orderID,factoryOrders)`。

参数：订单号、选择的工厂单；CLI 增加 `--shipment-only --confirm-save`。

```text
startDirectOrderShipment(...)
  → inventory_main(action="outbound")
  → run_jdy(..., shipment_only=true)
      → build_database_preview(order_id, selected_factory_orders, shipment_only=true)
      → assert_shipment_allowed(config,order_id,factory_orders)
      → 无五金：mark_no_hardware_outbound()，只更新状态
      → 有五金：InventoryOperationJournal.prepare(kind="shipment")
      → jdy_inventory.mjs 逐单保存
      → _persist_single_outbound_result()
      → InventorySyncStore.save_success()
      → reconcile_outbound_statuses()
      → record_standard_outbound_baseline()
  → refreshDashboardOrdersAfterOutbound()
  → order list-index
```

`shipment-only` 不再扣订单材料；生产材料应在生产流程中处理。无五金工厂单不会创建空库存单，但会保存明确的本地出货状态事实。

## 12. 库存页、商品目录和映射

### 12.1 轻量加载 Traveler 列表

入口：`loadInventory()` → `inventory list-names` → `list_traveler_names(config)`。

只枚举符合名称规则的 Traveler 路径、mtime 和已有同步状态，不立即打开所有 Excel。点击文件后才调用预览。

### 12.2 Traveler 库存预览

入口：`previewSelectedInventory()`。

参数：选择的 Traveler 路径数组和可选 `document_remark`。每个文件串行调用：

```text
inventory preview --traveler <path>
  → build_preview(traveler_path, product_database, workflow_database)
      → parse_traveler(path)
      → order_stock_requirements()/stock_requirements()
      → InventoryMappings
      → match_item()/resolve_inventory_items()
      → InventoryPreview.payload()
```

预览不会写库存系统。缺失或歧义映射使 `ready=false`，必须先处理后才能出库。

### 12.3 数据库订单预览

入口：`previewOrderInventory(orderID,factoryOrderNames,factoryOrders,productionBatchNumber,shipmentOnly)`。

下一跳：`inventory order-preview` → `build_database_preview()`。材料、五金和出库范围直接来自 `workflow.sqlite3`；Traveler 不是这个路径的事实来源。

### 12.4 商品目录更新

入口：`updateInventoryCatalog()` → `inventory update-products`。

```text
inventory.update_catalog_online(config)
  → run_jdy(config,"exportProducts",download_path)
  → tools/jdy_inventory.mjs 导出商品 Excel
  → ProductCatalog(download)
  → _catalog_change_summary(old,new)
  → import_catalog(config,download)
      → 校验临时 Excel
      → _replace_product_database(...)（名称保留，实际按 SKU upsert）
      → os.replace() 安装当前目录
```

数据库更新先把旧行标记为不在本次目录，再把当前 SKU 更新/插入并设为 `catalog_present=1`。未出现在新导出中的历史 SKU 不物理删除，因此外键引用和历史详情仍可读取；但商品查找、映射、材料确认和新的库存操作会阻断 `catalog_present=0` 的商品。`current-products.xlsx` 的原始文件替换与 SQLite 商品事务是两个需要分别验证的结果。

### 12.5 打开库存专用 Chrome

入口：`openInventoryChrome()` → `inventory open-chrome` → `open_inventory_chrome(config)`。

参数来自 CDP endpoint、专用 profile 路径和 Chrome 可执行文件。已存在合格登录页面时复用；存在登录页时等待用户完成登录；否则启动带专用 `--user-data-dir` 和远程调试端口的 Chrome。

### 12.6 人工映射和全局忽略

| 动作 | CLI | Python 函数 | 事实表/结果 |
| --- | --- | --- | --- |
| 搜索商品 | `search-products --query` | `search_inventory_products()` | 只读商品库 |
| 新增映射 | `set-mapping --item-name --product-code` | `save_manual_mapping()` | `inventory_resolution_rules` |
| 修改映射 | `update-mapping --old-name --item-name --product-code` | `update_manual_mapping()` | 同上 |
| 删除映射 | `remove-mapping --item-name` | `remove_manual_mapping()` | 同上 |
| 加入忽略 | `ignore-item --item-name [--reason]` | `set_ignored_mapping(...,True)` | 同上，rule_type=ignore |
| 修改忽略 | `update-ignore --old-name --name --ignored true` | `update_ignored_mapping()` | 同上 |
| 恢复忽略 | `unignore-item --item-name` | `set_ignored_mapping(...,False)` | 删除忽略规则 |

映射是业务事实，不应靠模糊名称自动写入。所有保存操作都在成功后重新预览当前对象。对尚未确认 SKU 的来源项目，当前名称映射和全局忽略仍决定它能否进入预览；一旦材料已经以 `product_code` 写入中央事实，数据库预览和库存需求就使用该显式 SKU，不会因后来修改同名 mapping 或 ignore 而重绑或移除。这里不绕过显式的 `outbound_scope_decisions`：客户提供、余料生产或不需要出库等范围决定仍按订单规则生效。

`TravelerItem.product_code` 保存运行时 canonical 身份，`source_snapshot()` 则固定只序列化历史的 `row/section/name/quantity/document_remark` 五个来源字段。这样数据库路径可以按 SKU 匹配和比较实际出库内容，同时旧 raw fingerprint 与待恢复 `inventory_operations` journal 的 payload 形状不漂移；SKU 和数量的真实变化仍由映射后指纹识别。

## 13. 生产文件与 Traveler

### 13.1 列出源订单文件夹

入口：`loadOrderFolders()` → `order list --source-root <path>` → `list_order_folders(config)` → `resolve_source_root()`。

输入源根目录由页面的 owned/cut-to-size 选择决定。输出包括订单号、路径和修改时间。

### 13.2 预览源订单

入口：`previewOrderFolder(item)` → `order preview-related --folder <path>`。

```text
preview_related_orders(config,folder)
  → related_order_ids(folder)
  → 对每个 order_id 调 preview_order(config,folder,order_id)
      → 选择/校验 material 文件
      → parse_order_materials()/parse_material_room_rows()
      → _choose_fittings() → core.parse_fittings_groups()
      → _factory_names() → 板材清单/缓存/AIMES fallback
      → _normalize_fittings()
      → resolve_inventory_items()
      → persist_preview() 写入已验证中央事实
  → preview_payload()
```

关键参数：`folder`、可选 `order_id`、`include_hardware`、临时订单身份。返回材料、封边、工厂单、五金、warnings 和已有 Traveler 路径。

### 13.3 自动生成缺失 material

入口：`generateMissingMaterial()` → `order generate-material --folder --order-id` → `generate_material_from_reports()` → 写入新 material 工作簿 → `_record_generated_material_baseline()` 保存生成证据 → 重新预览订单。

### 13.4 从中央数据库生成 Traveler

入口：`generateSelectedOrder()` → `order generate-db --order-id`。

```text
generate_database_order_traveler(config,order_id)
  → 从 workflow.sqlite3 读取材料、五金、工厂单
  → 材料按 product_code JOIN products，得到类型、颜色、名义厚度和单位
  → 组装 OrderPreview/FactoryPreview
  → generate_order_traveler(config,preview)
      → 复制模板到临时工作簿
      → _prepare_picking_list()
      → _prepare_purchase_list()
      → _fill_usage_list()/相关写入函数
      → 保存临时文件并重新打开校验
      → 原子替换目标
```

Traveler 使用已确认 SKU 对应的商品业务属性，不重新依据当前名称映射选择 SKU。Plywood 的工作流名义厚度（例如 5.4、14.5）与商品原始规格（例如 5.2、15）分别保留，避免改变 Usage List 分类。

### 13.5 更新旧 Traveler

入口：CLI `order update --folder` 或助手 `update_traveler`。

`update_order_traveler()` 会先解析当前源事实、备份旧 Traveler、补齐/恢复模板工作表、保留允许保留的人工五金，再原子替换。备份成功、工作簿保存成功和重新打开校验成功分别是不同证据。

### 13.6 人工五金

入口：`order add-hardware` 或助手 `add_manual_hardware`。

参数：`order_id`、完整 `factory_name`、`product_code`、正数 `quantity`、可选 `remarks`。第一次 `preview_manual_hardware()` 只返回预览；`--confirm-write` 后 `add_manual_hardware()` 写中央 SQLite，并在存在 Traveler 时备份、同步 Excel。

## 14. 全部 Order CLI 命令对照

以下表覆盖 `order_workflow.main()` 当前 `choices`。它用于定位入口，不替代上面的业务解释。

| command | 必要/关键参数 | 直接分发函数 | 读写性质 |
| --- | --- | --- | --- |
| `list` | `--source-root` 可选 | `list_order_folders()` | 只读目录 |
| `list-index` | 无 | `order_index.list_order_index()` | 只读中央事实（会执行必要 schema 准备） |
| `detail` | `--order-id` | `order_details.order_detail()` | 只读 |
| `cost` | `--order-id` | `costing.calculate_order_cost()` | 只读 |
| `cost-export` | `--order-id` | `costing.export_order_cost()` | 写 Excel |
| `backup-status` | 无 | `backup.backup_status()` | 检查 |
| `backup-now` | 无 | `backup.perform_backup()` | 写备份 |
| `sync-index` | refresh/full/snapshot 选项 | `order_index.sync_order_index()` | 按参数同步 SQLite |
| `process-server-changes` | `--server-folder*`、`--include-hardware` | `process_server_changes()` | 兼容处理路径，会写事实 |
| `process-server-folder` | `--folder` | `process_server_folder()` | 解析并写事实 |
| `preview-server-changes` | `--server-folder*` | `preview_server_changes()` | 内存预览 |
| `confirm-server-preview` | token/order/factory | `confirm_server_preview()` | `--confirm-write` 后写入 |
| `confirm-server-material-preview` | token | `confirm_server_material_preview()` | `--confirm-write` 后写入 |
| `confirm-server-preview-memory` | stdin/order/factory | `confirm_server_preview_memory()` | `--confirm-write` 后写入 |
| `confirm-server-material-preview-memory` | stdin/skip list | `confirm_server_material_preview_memory()` | `--confirm-write` 后写入 |
| `sync-aimes` | `--refresh-aimes` 或 `--aimes-if-needed` | `sync_aimes_index()` | 读取 AIMES并写身份事实 |
| `scan-server` | 无 | `scan_server_changes()` | 发现变化；普通报表不确认写入 |
| `ignore-aimes` | `--ignore-key*` | `ignore_aimes_factories()` | 写 |
| `restore-aimes-ignore` | `--ignore-key*` | `restore_aimes_factories()` | 写 |
| `assign-aimes-order` | 单个 key + order | `assign_aimes_factory_order()` | 写 |
| `restore-aimes-assignment` | 单个 key | `restore_aimes_order_assignment()` | 写 |
| `auto-resolve-issue` | `--issue-key` | `auto_resolve_current_issue()` | 视问题写入 |
| `resolve-issue` | `--issue-key` | `resolve_current_issue()` | 写 |
| `save-order-annotations` | order/note/date JSON | `save_order_annotations()` | 写 |
| `production-preview` | order/factory JSON | `production_preview()` | 只读 |
| `prepare-production` | order/factory/material JSON | `prepare_production()` | 写 prepared batch |
| `migrate-production-state` | 无 | `migrate_legacy_production_state()` | 数据迁移 |
| `preview` | `--folder` | `preview_order()` + `preview_payload()` | 解析并持久化已验证事实 |
| `preview-related` | `--folder` | `preview_related_orders()` | 同上，按关联订单拆分 |
| `refresh-aimes` | 无 | `sync_aimes_index(force=True)` | 在线同步身份 |
| `stock-check` | `--folder` | `inventory.check_order_stock()` | 外部库存只读 |
| `set-ignore` | `--name* --ignored` | `order_workflow.set_ignored()` | 写全局忽略规则 |
| `generate` | `--folder` | `generate_order_traveler()` | 写 Excel |
| `generate-db` | `--order-id` | `generate_database_order_traveler()` | 写 Excel |
| `temporary` | `--folder` | `generate_temporary_traveler()` | 写临时 Excel |
| `generate-material` | folder/order | `generate_material_from_reports()` | 写 Excel和基线 |
| `generate-material-from-travelers` | folder/order | `generate_material_from_travelers()` | 先预览，确认后写 |
| `update` | `--folder` | `update_order_traveler()` | 备份并写 Excel |
| `update-related` | `--folder` | `update_related_orders()` | 多订单写 Excel |
| `add-hardware` | order/factory/code/quantity | `preview_manual_hardware()` / `add_manual_hardware()` | 确认后写 |
| `add-factory` | order/factory/name | `add_manual_factory()` | 写身份事实 |
| `assign-material` | folder/order/material file | `save_material_assignment()` | 写选择事实 |
| `create-test-data` | `--target-root` | `test_data.create_local_test_source()` | 仅写测试目录 |

## 15. 全部 Inventory CLI 命令对照

| action | 必要/关键参数 | 直接分发函数 | 读写性质 |
| --- | --- | --- | --- |
| `list` | `--include-history` 可选 | `list_travelers()` | 打开 Traveler 读取 |
| `list-names` | 无 | `list_traveler_names()` | 只枚举文件名/mtime |
| `preview` | `--traveler` | `build_preview()` | 只读预览 |
| `order-preview` | `--order-id`、factory/batch 选项 | `build_database_preview()` | 只读预览 |
| `get-outbound-scope` | order/factory | `outbound_scope_decisions()` | 只读 |
| `set-outbound-scope` | order/type/requirement | `set_outbound_scope()` | 写范围决定 |
| `import-products` | `--source` | `import_catalog()` | 写本地商品库 |
| `update-products` | 无 | `update_catalog_online()` | 读外部、写本地商品库 |
| `open-chrome` | 无 | `open_inventory_chrome()` | 启动专用 Chrome |
| `close-chrome` | 无 | `close_inventory_chrome()` | 关闭专用 Chrome |
| `preflight` | 无 | `run_jdy("preflight")` | 外部只读/登录检查 |
| `stock-check` | traveler/hardware 选项 | `check_stock()` | 外部只读库存 |
| `find-outbound` | `--order-name` | `run_jdy("findOutbound")` | 查询外部历史 |
| `reconcile-folder` | `--folder` | `reconcile_folder_status()` | 对账并更新本地状态 |
| `search-products` | `--query` | `search_inventory_products()` | 只读商品库 |
| `set-mapping` | item/code | `save_manual_mapping()` | 写映射 |
| `update-mapping` | old/item/code | `update_manual_mapping()` | 写映射 |
| `remove-mapping` | item | `remove_manual_mapping()` | 删除映射 |
| `list-mappings` | 无 | `list_inventory_mappings()` | 只读 |
| `update-ignore` | old/name/ignored/reason | `update_ignored_mapping()` | 写忽略规则 |
| `ignore-item` | item/reason | `set_ignored_mapping(...,True)` | 写忽略规则 |
| `unignore-item` | item | `set_ignored_mapping(...,False)` | 删除忽略规则 |
| `outbound` | order 或 traveler；确认时 `--confirm-save` | `run_jdy("outbound",...)` | 外部和本地写入 |

## 16. 如何沿调用链自己调试

针对一个具体操作，建议固定做六步：

1. 在 App 页面找到按钮绑定的 Swift 函数。
2. 看该函数传给 `runOrder` / `runInventory` 的**完整 arguments 数组**。
3. 在 `order_workflow.main()` 或 `inventory_main()` 找对应 command/action 分支。
4. 跳到分支调用的业务函数，先读输入校验、返回结构和副作用，再读私有辅助函数。
5. 用同一参数直接运行 `./scripts/pp-flowhub ...`，只在安全的只读命令上这样做；写操作要保留预览/确认边界。
6. 用相同 `operation_id` 对照 `operation-log.jsonl`、SQLite 行、Excel 或外部单据号，确认本次真实执行结果。

不要只看页面最终一句状态，也不要只看一个函数名就推断整条链已经执行。

## 17. 推荐学习顺序

### 第一阶段：一周内建立全局地图

1. 读 `00-architecture-overview.md` 和本文第 1～5 节。
2. 在 App 里只观察一次订单看板启动，画出“本地缓存 → 备份 → AIMES → Server”的四段时间线。
3. 对照 `TravelerAssistant.swift: runOrder()` 和 `order_workflow.py: main()`，理解跨进程 JSON 合同。

### 第二阶段：按业务场景跟读

建议顺序：订单详情 → Server 预览/确认 → 生产 → 出货 → Traveler。每次只跟一条链，并为每个函数记五件事：输入、返回、事实源、副作用、不变量。

### 第三阶段：从测试反推规则

在 `08-support-test-symbol-reference.md` 搜索目标函数名，再读对应测试。测试名称通常比实现代码更接近业务语言，并能告诉你哪些边界不允许破坏。

### 第四阶段：做低风险练习

1. 只修改一个纯展示字段，并更新对应 Swift 契约测试。
2. 给一个只读 Python 函数新增返回字段，并更新 CLI 测试。
3. 在隔离临时目录中修改 Traveler 模板写入逻辑，验证工作表、合并单元格和重新打开结果。
4. 最后再接触 Server 确认、生产完成或库存出库等真实写入路径。

## 18. 文档维护规则

代码变化后运行：

```bash
PYTHONDONTWRITEBYTECODE=1 python3 tools/generate_code_reference.py
```

生成器负责文件和符号全集；本文必须人工维护，因为业务意图、审批边界和动态调用不能仅靠静态扫描可靠推断。新增用户可见操作时，应同时补充：

- Swift 页面入口和传参；
- CLI command/action；
- Python 业务入口与下一跳；
- 读取事实源；
- 写入副作用；
- 返回合同；
- 失败或不确定结果的恢复方式；
- 对应测试。

### Server 确认页内的五金映射刷新

`saveServerHardwareMapping` / `saveServerHardwareIgnoredMapping` 保存规则后，调用 `refreshServerHardwarePreview`，以当前预览的文件夹和 `hardware_source_choices` 再运行 `preview-server-changes`。成功返回后同时替换展示模型与确认 payload，不能只删除待映射提示。刷新中或失败时由 `serverWritePreviewNeedsRefresh` 阻止确认，失败可重试；五金来源冲突需重新打开文件夹预览处理。来料加工订单的跳过选择留在原 Sheet 中。此步骤只重建预览，正式材料和五金仍由用户最终确认写入。

Swift 回归 `testServerHardwareMappingRefresh` 覆盖映射后明细与 payload 更新、来源保留、失败/无效返回阻止确认、重试和忽略后的刷新。

### 已确认材料与 Server 来源变化

订单材料 `material_items` 是需求事实，生产批次材料是消耗事实，出库单是库存操作证据。生产完成应计算需求减消耗，不删除需求；订单材料按订单与 SKU 保存，不按每个工厂单各存一份。

Server 文件夹变化或材料文件消失只更新发现信息，不能据此清空需求或历史分配。`_reconcile_authoritative_server_material_sources` 仅在当前文件夹已有完整且逐 SKU 数量一致的材料集时清理旧路径重复事实，删除范围限定同一订单。不同数量必须经材料预览与确认处理。回归见 `test_order_index.py` 的 material_scope 测试及 `test_confirmed_material_optimization.py` 的文件缺失测试。

### material 封边的公式结果与显示数量

Excel 将公式计算结果和数字格式分别保存。例如 Color Table 的封边公式结果为 `319.64`，整数格式 `0` 显示为 `320`。`parse_order_materials` 以汇总单元格的显示数量作为业务数量：有公式缓存时读取缓存并应用 `_display_number`；没有缓存时先按颜色合计原始明细，再应用汇总格格式，不能逐房间取整后相加。`Total Qty` 的封边校验也使用该格显示数量；真实合计不一致仍阻止写入。`General` 或保留小数的格式不强制取整数。

读取只在内存计算，不保存 Excel，不更新正式材料。Server 确认页比较的是已确认数据库数量与本次解析结果；预览修正后仍需用户确认才能写入。回归覆盖公式缓存有/无、汇总后取整、整数/小数格式、真实不一致，以及源文件字节不变。

### 订单中心表头与操作时间对齐

表头的 `offset` 只移动文字显示位置，不改变表头和数据行共享的列宽；本次所有标题在原位置左移 5pt。消息列表的滚动条可能占用横向空间，`onGeometryChange` 读取列表内容的实际宽度，顶部当前操作/最近结果使用同一宽度及 12pt 内边距，使右侧时间对齐，并随窗口宽度变化更新。

### Server 材料确认页的列表布局

`ServerWriteConfirmationSheet` 将材料类型与颜色／规格分列，变化标签与数量变化共用固定列宽，表头和数据行采用相同间距。表头的 `offset(x: 10)` / `offset(x: -5)` 只微调材料类型和数量变化标题，不影响数据列。颜色与封边描述完全相同时仅在显示层去重，原始字段与确认 payload 不变。

五金按订单与工厂单组合标识保存展开状态，默认展开，可单独折叠；商品名称、SKU、数量、商品单位各占一列，空单位显示“—”。首次写入仍只显示五金明细，已有事实的比较继续由 `existingHardwareChanges` 提供。布局不修改 SKU 校验、来料加工订单跳过选择、刷新失败阻断和最终确认写入入口。

## Server 预览的“确认无变化”（2026-09-16）

调用链：`ServerWriteConfirmationSheet` → `AppModel.acknowledgeServerPreview()` → `acknowledge-server-preview-memory` → `acknowledge_server_preview_memory()`。前端根据完整预览显示按钮；后端重新检查差异、校验、五金来源和已确认材料，不能只信任界面的按钮状态。

这里的“监控基线”是下次扫描用于比较的 XML 文件版本，不是材料或优化完成的业务事实。它保存预览时的版本，不重新读取点击时的新文件，因此预览后文件变化不会被悄悄忽略。事务只更新 `server_scan_xml_state`；预览时记录本地业务数据的指纹，确认时在同一写事务中比较，发现旧预览便要求重读。成功后关闭预览并刷新待处理列表，失败则留在原界面。

## 订单中心：人工五金编辑

入口在订单展开后的「计算成本」右侧。「人工五金」打开 `ManualHardwareSheet`，通过 `manual-hardware --order-id` 读取本订单人工记录和工厂单；`search-hardware-products --query` 复用商品目录的 SKU/名称检索。列表按工厂单分组，不提供备注输入。

新增和删除先保存在 SwiftUI 的弹窗状态中，不调用写库。删除可撤销，关闭含更改的弹窗需确认放弃。点击「保存更改」后，App 把版本、待新增记录和待删除 ID 作为 JSON 发送到 `save-manual-hardware --confirm-write`。`traveler_assistant/manual_hardware.py` 在同一个 SQLite 事务内校验工厂单归属、启用商品、正整数数量、全局忽略规则和编辑基线，再保存全部更改；任何错误整体回滚。

`version` 是已读人工记录和工厂单状态的摘要，用来发现并发变化和阻止同一草稿重复新增，并非新的持久缓存。每条新增必须绑定本订单有效且未出库的工厂单；删除只允许当前订单的有效 manual 记录，保存时直接删除对应行。自动五金不变，不写 Traveler 或外部库存。保存后重新读取订单列表和详情。

学习点：界面草稿解决“取消编辑”，数据库事务解决“保存一半”，版本校验解决“编辑期间别人已修改”；三者分别负责不同的错误边界。回归见 `tests/test_manual_hardware.py` 和 `testManualHardwareEditorContract()`。

### 订单安排表单与按钮布局（2026-09-17）

订单中心“订单安排”仍进入 `OrderAnnotationsSheet` → `OrderAnnotationsEditor`。方案一只调整 SwiftUI：上方订单说明，下方按“安排类型 / 开始日期 / 安装人”对齐的两行；日期用中性输入外观，月历与历史安装人菜单沿用原实现。未填写时点击“选择日期”创建本地草稿并打开月历，清除只移除草稿，点击保存才进入原 `saveOrderAnnotations` 调用链。实际安装仍只保存开始日期；没有新增字段或修改 SQLite 保存协议。

按钮外部 `.frame(minWidth:)` 只扩大布局占位，不一定扩大按钮可见背景。要让不同字数的按钮边缘等距，应把统一宽度放到 `Button` 的 `label` 内，再用 `HStack(spacing: 8)` 排列。详情工具栏与工厂单表格间距从 12 改为 7，减少 5 个 SwiftUI 逻辑点；Retina 截图像素会随显示缩放变化。

安装版验收补充：`ForEach(rows) { $day in ... }` 中的 `$day` 是指向数组元素的绑定。清除动作如果先从数组删除元素，再读取 `day.id`，会触发数组越界；应在修改数组前把 `day.id` 复制到局部常量，先处理弹窗状态，再按该标识删除。此问题已由 2026-09-17 安装版崩溃堆栈中的 `Array._checkSubscript` / `Binding.subscript.getter` 直接确认；修复后的真实点击须重新安装验证。

### 助手看板：分批推进的阶段连接线（2026-09-17）

`dashboardOrders` → `AssistantView.assistantProgressRail` → `assistantProgressSegmentState`。拆单、优化、生产、出货分别使用自己的完成数量与工厂单总数：零完成或总数为零显示灰色，部分完成显示绿色流动虚线，全部完成显示绿色实线；节点图标复用相同判断，部分完成和全部完成均标绿。减少动态效果开启时，部分完成的虚线保持静止。

不要用“第一个未全部完成的阶段”锁住后续阶段：例如 PP0064 的 27 个工厂单中，3 个已优化且已生产，优化和生产应同时显示部分完成。这个函数只把已有数量转换为显示状态，不修改订单汇总阶段、生产或库存事实。回归比较生产数量从 0 变成 3 前后的阶段数组，确保前一阶段未完成不会阻止后一阶段更新。

## 订单中止（2026-09-18）

订单详情“中止” → SwiftUI 二次确认 → `AppModel.abortOrder` → `order-service` 的 `abort-order --confirm-write` → `order_index.abort_order` → SQLite `orders.stage = 已中止`。取消确认不会调用后台。

普通进度由工厂单汇总，中止是人工终态：`upsert_order` 和 `summaries` 都保留它，否则下一次刷新就会丢失。生产选择校验及库存出库入口再次检查中止状态，防止旧预览绕过按钮禁用。历史事实的对账保存不受此限制，避免外部已经成功的单据丢失。隔离回归见 `tests/test_order_abort.py`。

订单动作按钮宽度补记：生产、出货、中止统一使用 67 pt 的标签宽度（原生产标签为 72 pt，减 5），同用 regular controlSize 与 glassProminent 样式，使按钮包含系统内边距后的实际宽度一致。不要只给整个 Button 设置 minWidth：那是最小布局宽度，不保证可见按钮等宽。本次按用户要求不运行测试。

订单动作按钮再次微调：三个标签由 67 pt 改为 57 pt，按钮 HStack 的 spacing 保持 8，不调整其他按钮宽度。

订单状态筛选只读核对：当前 `OrderIndexStore.summaries` 不产生“待确认”或“数据异常”订单 stage；Swift 直接读取 stage，未用 validation_status 替换。`orderDashboardStatus` 仍能返回数据异常，但产品调用链未使用，仅回归测试引用。“待人工处理”仍在 temporary 分支，正常 list-index 先清理/转正旧临时订单投影，临时任务走 temporary_orders 与待处理中心。三个筛选项属于待清理的旧显示逻辑；归属确认和校验功能本身仍有用。本次只回答状态用途，没有删除选项或调整业务逻辑。

状态筛选清理已实施：从 `orderDashboardStatuses` 移除已设计、待人工处理、待确认、数据异常，并同步 Swift 筛选断言。仅收窄用户可选菜单，不改变 summaries、后台初始值、归属确认、异常校验或真实数据库。菜单集合与数据库业务状态集合不是同一个概念。按用户此前要求未执行测试。

成本按钮材料门槛：`canCalculateOrderCost` 从当前详情的正数量材料和读取状态派生，同时用于按钮禁用及计算入口守卫。切换订单在请求排队之前清空材料；详情响应校验订单身份，避免旧材料串到新订单。无需新增缓存或数据库字段。三个动作标签宽度由 57 pt 再减 20 到 37 pt，操作间距仍为 8。用户本次恢复正常测试，执行完整发布门禁。

### 待处理中心提醒与执行状态（2026-09-18）

`scanDashboardServer` 完成后留下“请在待处理中心预览并逐单确认写入”；“稍后处理”只关闭弹窗，不启动后台任务。订单中心的 `OrderDashboardActivityInput.operationRunning` 与助手的 `currentAssistantOperation` 都使用 `dashboardStatusIsInProgress`。该判断在匹配“正在 / 处理中”前剔除界面名称“待处理中心”，避免名称中的“处理中”触发虚假动画；“正在读取待处理中心”仍算真实执行状态。无需清空提醒或修改待处理业务事实。Swift 回归覆盖弹窗显示/关闭、助手共用条件以及真实执行提示。

本次验证：普通环境 `test-release` 全部通过（Python 401 项、跳过 1；Swift UI、AIMES 离线、PP0067 workbook 通过），串行 `build-app` 成功。首次沙箱运行被 SwiftUI 宏插件限制阻断，非源码编译缺陷。旧安装版实测两页均误显示进行中；新安装版尚未验收：后台无有效签名 identity，Computer Use 明确禁止操作 Terminal，未尝试绕过或降级签名。未签名产物保留于 `/tmp/pp-flowhub-build/PP FlowHub.app`，需普通 Terminal 执行项目 `scripts/install-app` 后复测启动弹窗 → 稍后处理 → 切换助手（无同步图标或忙指示器）。


### 材料确认预览与主界面密度（2026-09-18）

`TopNavigationBar` 中材料确认 sheet 从 820 收至 720 pt，保持 650 pt 高度；`ServerWriteConfirmationSheet` 五金编码、数量、单位列统一为 100/56/40 pt，表头和内容采用相同列宽及 10 pt 间距，名称列弹性布局并允许换行。材料变化表同步收紧固定列，为颜色规格保留空间。删除界面设计说明按钮、状态与弹窗后，待处理按钮成为右侧末项。

历史消息行的最小高度从 74 改为 59 pt，三行视口从 222 改为 177 pt；订单列表自动获得释放的 45 pt。SwiftUI 使用逻辑点（pt），Retina 屏幕上的物理像素由系统缩放。较长的阶段耗时消息仍可自然换行，避免裁掉文字。此调整不改变消息来源、预览确认和 SKU 校验逻辑。

发布验证：完整 `test-release` 在普通执行环境通过（Python 401 项，跳过 1；Swift UI、AIMES 离线、PP0067 workbook 均通过）。一次串行构建成功；Computer Use 禁止操作 Terminal，但普通执行环境能访问有效 Apple Development identity，直接执行现有 `scripts/install-app` 成功完成签名、helper 验证及正式替换。安装版 0.4.1 (5) 的 SHA-256 为 `c2c0055e79b35018455ff3c91e26ce248bd58559dd10cc25e4b686c21727fbb6`。退出旧进程重开后，主界面已确认说明按钮消失、待处理入口移到右侧，三行历史消息和更多订单同时可见。

现场预览验收限制：安装版选择 PP0064 只读预览后，等待超过 127 秒仍停在读取材料/核对工厂单阶段；尚未取得新预览截图，列间距、长名称和底部按钮的视觉验收未完成，详见根目录 design-qa.md。未执行 SKU 映射、忽略或最终业务写入。
