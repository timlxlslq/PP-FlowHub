# PP FlowHub Swift/macOS 全符号中文参考

> 本文件由 `tools/generate_code_reference.py` 生成。请不要手工修改。

## 如何阅读

- 范围：`macos/` App 生产代码，共登记 **729** 个类型、函数、方法、计算属性或脚本过程。
- “输入”来自静态签名；`self`/`cls` 不重复列出。未声明类型不代表运行时没有约束。
- “项目内下一跳”只表示源码中可静态确认的直接调用，不表示每个分支都会执行。
- `self.method()`、协议分发、闭包、Swift 重载和动态导入可能无法唯一解析；关键业务路径以 `09-user-operation-call-chains.md` 为准。
- “副作用提示”是保守提醒，不等于函数一定执行写入。确认真实行为时应继续阅读分支、日志和测试。

## `macos/AssistantView.swift`

助手页面、语音输入、任务队列和业务进度轨道。

- **L9 · 函数** `func canonicalSpeechCommand(_ text: String) -> String` — 封装 `canonicalSpeechCommand` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:22` `digits`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `replaceCharacters`；是否真实写入仍取决于分支和参数。

- **L22 · 函数** `func digits(at index: Int) -> String` — 封装 `digits` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`at index: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L36 · 结构体** `AssistantOrderResult` — 定义与订单、结果相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L46 · 初始化器** `init?(object: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`object: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:907` `OrderMaterialPreview`；`macos/TravelerAssistant.swift:1000` `OrderFactoryPreview`；`macos/TravelerAssistant.swift:1006` `OrderFittingPreview`

- **L90 · 类** `SpeechInputController` — 定义 `SpeechInputController` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L103 · 方法** `func beginPushToTalk()` — 封装 `beginPushToTalk` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:157` `SpeechInputController.requestAccessAndStart`

- **L112 · 方法** `func endPushToTalk(onComplete: @escaping (String) -> Void)` — 封装 `endPushToTalk` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`onComplete: @escaping (String) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:130` `SpeechInputController.stop`；`macos/AssistantView.swift:143` `SpeechInputController.completeRecognition`

- **L130 · 方法** `func stop()` — 封装 `stop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L143 · 方法** `private func completeRecognition()` — 封装 `completeRecognition` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L157 · 方法** `private func requestAccessAndStart()` — 封装 `requestAccessAndStart` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:176` `SpeechInputController.start`

- **L176 · 方法** `private func start()` — 启动与 `start` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:143` `SpeechInputController.completeRecognition`；`macos/AssistantView.swift:130` `SpeechInputController.stop`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L221 · 函数** `func isPushToTalkShortcut(keyCode: UInt16, modifiers: NSEvent.ModifierFlags) -> Bool` — 封装 `isPushToTalkShortcut` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`keyCode: UInt16`；`modifiers: NSEvent.ModifierFlags`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L226 · 类** `PushToTalkShortcutMonitor` — 定义 `PushToTalkShortcutMonitor` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L231 · 方法** `func install(onPress: @escaping () -> Void, onRelease: @escaping () -> Void)` — 封装 `install` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`onPress: @escaping () -> Void`；`onRelease: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:221` `isPushToTalkShortcut`

- **L249 · 方法** `func uninstall()` — 封装 `uninstall` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L258 · 结构体** `AssistantOrderPreviewView` — 定义与订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L261 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:356` `AssistantOrderPreviewView.metricCard`；`macos/AssistantView.swift:367` `AssistantOrderPreviewView.sectionTitle`；`macos/TravelerAssistant.swift:933` `orderMaterialDisplayName`

- **L356 · 方法** `private func metricCard(_ title: String, _ value: String, _ icon: String) -> some View` — 封装 `metricCard` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ value: String`；`_ icon: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L367 · 方法** `private func sectionTitle(_ title: String, _ icon: String) -> some View` — 封装 `sectionTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ icon: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L372 · 结构体** `AssistantOrderListView` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L375 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1263` `appDisplayTimestamp`

- **L395 · 结构体** `AssistantStockComparisonView` — 定义 `AssistantStockComparisonView` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L400 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L460 · 函数** `func assistantTaskShowsHeaderCancel(_ status: String) -> Bool` — 封装 `assistantTaskShowsHeaderCancel` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L464 · 结构体** `AssistantCommandHintsContent` — 定义 `AssistantCommandHintsContent` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L465 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L478 · 扩展** `AppModel` — 定义 `AppModel` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L479 · 方法** `func loadAssistantUsage()` — 读取与 `loadAssistantUsage` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L505 · 方法** `func runAssistantCommand(approved: Bool = false)` — 把助手输入加入任务队列，并启动后续命令执行。
  - 输入：`approved: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/AssistantView.swift:547` `AppModel.executeAssistantTask`；`macos/TravelerAssistant.swift:1369` `AssistantTaskItem`；`macos/AssistantView.swift:540` `AppModel.processNextAssistantTask`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `executeAssistantTask`；是否真实写入仍取决于分支和参数。

- **L523 · 方法** `func cancelAssistantTask(_ id: UUID)` — 封装 `cancelAssistantTask` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ id: UUID`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/AssistantView.swift:540` `AppModel.processNextAssistantTask`

- **L540 · 方法** `func processNextAssistantTask()` — 处理与 `processNextAssistantTask` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:547` `AppModel.executeAssistantTask`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `executeAssistantTask`；是否真实写入仍取决于分支和参数。

- **L547 · 方法** `private func executeAssistantTask(_ task: AssistantTaskItem, approved: Bool)` — 启动助手子进程、消费输出并把结果映射为页面状态。
  - 输入：`_ task: AssistantTaskItem`；`approved: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1801` `AppModel.newOperationID`；`macos/TravelerAssistant.swift:1830` `AppModel.environmentForOperation`；`macos/AssistantView.swift:672` `AppModel.finishAssistantTask`；`macos/AssistantView.swift:36` `AssistantOrderResult`；`macos/TravelerAssistant.swift:1019` `OrderStockPreview`；`macos/TravelerAssistant.swift:85` `OrderFolderItem`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/AssistantView.swift:479` `AppModel.loadAssistantUsage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L672 · 方法** `private func finishAssistantTask(_ id: UUID, status: String)` — 结束并收口与 `finishAssistantTask` 对应的数据或步骤。
  - 输入：`_ id: UUID`；`status: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:540` `AppModel.processNextAssistantTask`

- **L682 · 枚举** `AssistantDashboardTypography` — 定义与看板相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L696 · 结构体** `AssistantView` — 定义 `AssistantView` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L707 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5011` `View.appPageFrame`；`macos/AssistantView.swift:9` `canonicalSpeechCommand`；`macos/TravelerAssistant.swift:2158` `AppModel.startOrderDashboard`；`macos/AssistantView.swift:231` `PushToTalkShortcutMonitor.install`；`macos/AssistantView.swift:103` `SpeechInputController.beginPushToTalk`；`macos/AssistantView.swift:1366` `AssistantView.finishPushToTalk`；`macos/AssistantView.swift:249` `PushToTalkShortcutMonitor.uninstall`；`macos/AssistantView.swift:130` `SpeechInputController.stop`

- **L745 · 计算属性** `private var commandStrip: some View` — 根据当前状态计算并返回`commandStrip` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:505` `AppModel.runAssistantCommand`；`macos/AssistantView.swift:1373` `AssistantView.beginCommandHintsAnchorHover`；`macos/AssistantView.swift:1388` `AssistantView.endCommandHintsAnchorHover`；`macos/AssistantView.swift:464` `AssistantCommandHintsContent`；`macos/AssistantView.swift:1394` `AssistantView.beginCommandHintsPanelHover`；`macos/AssistantView.swift:1400` `AssistantView.endCommandHintsPanelHover`；`macos/AssistantView.swift:103` `SpeechInputController.beginPushToTalk`；`macos/AssistantView.swift:1366` `AssistantView.finishPushToTalk`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5107` `AppStatusBadge`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L807 · 计算属性** `private var orderStatusBoard: some View` — 根据当前状态计算并返回订单、状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:849` `AssistantView.assistantMetric`；`macos/AssistantView.swift:900` `AssistantView.assistantOrderCard`

- **L849 · 方法** `private func assistantMetric(_ title: String, value: Int, symbol: String, color: Color) -> some View` — 封装 `assistantMetric` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`value: Int`；`symbol: String`；`color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L870 · 计算属性** `private var currentOperationSummary: some View` — 根据当前状态计算并返回操作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L900 · 方法** `private func assistantOrderCard(_ item: OrderDashboardItem) -> some View` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1130` `AssistantView.openOrderCenter`；`macos/AssistantView.swift:937` `AssistantView.assistantProgressRail`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderCenter`；是否真实写入仍取决于分支和参数。

- **L937 · 方法** `private func assistantProgressRail(_ item: OrderDashboardItem) -> some View` — 封装进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1051` `AssistantView.assistantProgressValue`；`macos/AssistantView.swift:1013` `AssistantView.assistantStageIcon`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `move`；是否真实写入仍取决于分支和参数。

- **L1013 · 方法** `private func assistantStageIcon( completed: Bool, current: Bool, color: Color, symbol: String ) -> some View` — 封装 `assistantStageIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`completed: Bool`；`current: Bool`；`color: Color`；`symbol: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1051 · 方法** `private func assistantProgressValue(_ value: String) -> String` — 封装进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1055 · 计算属性** `private var ongoingOrders: [OrderDashboardItem]` — 根据当前状态计算并返回`ongoingOrders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderDashboardItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1061 · 计算属性** `private var monthlyCompletedCount: Int` — 根据当前状态计算并返回`monthlyCompletedCount` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1285` `dashboardTimestamp`

- **L1067 · 计算属性** `private var effectiveOrders: [OrderDashboardItem]` — 根据当前状态计算并返回`effectiveOrders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderDashboardItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1071 · 计算属性** `private var showsAssistantWorkspace: Bool` — 根据当前状态计算并返回`showsAssistantWorkspace` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1078 · 计算属性** `private var currentAssistantOperation: (title: String, detail: String, running: Bool)` — 根据当前状态计算并返回操作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`(title: String, detail: String, running: Bool)`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:859` `dashboardStatusIsInProgress`

- **L1091 · 方法** `private func assistantStageSummary(_ item: OrderDashboardItem) -> String` — 封装 `assistantStageSummary` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1105 · 方法** `private func assistantOrderDates(_ item: OrderDashboardItem) -> String` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1116` `AssistantView.assistantDate`

- **L1116 · 方法** `private func assistantDate(_ value: String) -> String` — 封装日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1267` `dashboardBusinessDate`；`macos/TravelerAssistant.swift:1263` `appDisplayTimestamp`

- **L1121 · 方法** `private func assistantStageKind(_ stage: String) -> AppStatusBadge.Kind` — 封装 `assistantStageKind` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stage: String`
  - 返回：`AppStatusBadge.Kind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1130 · 方法** `private func openOrderCenter(_ orderID: String?)` — 打开订单相关数据或步骤。
  - 输入：`_ orderID: String?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1135 · 计算属性** `private var commandCard: some View` — 根据当前状态计算并返回`commandCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:505` `AppModel.runAssistantCommand`；`macos/AssistantView.swift:1373` `AssistantView.beginCommandHintsAnchorHover`；`macos/AssistantView.swift:1388` `AssistantView.endCommandHintsAnchorHover`；`macos/AssistantView.swift:464` `AssistantCommandHintsContent`；`macos/AssistantView.swift:1394` `AssistantView.beginCommandHintsPanelHover`；`macos/AssistantView.swift:1400` `AssistantView.endCommandHintsPanelHover`；`macos/AssistantView.swift:103` `SpeechInputController.beginPushToTalk`；`macos/AssistantView.swift:1366` `AssistantView.finishPushToTalk`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/AssistantView.swift:1337` `AssistantView.flowStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L1216 · 计算属性** `private var workspaceCard: some View` — 根据当前状态计算并返回`workspaceCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/AssistantView.swift:1357` `AssistantView.badgeKind`；`macos/AssistantView.swift:460` `assistantTaskShowsHeaderCancel`；`macos/AssistantView.swift:523` `AppModel.cancelAssistantTask`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/AssistantView.swift:395` `AssistantStockComparisonView`；`macos/AssistantView.swift:258` `AssistantOrderPreviewView`；`macos/AssistantView.swift:372` `AssistantOrderListView`

- **L1259 · 计算属性** `private var approvalCard: some View` — 根据当前状态计算并返回`approvalCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/AssistantView.swift:523` `AppModel.cancelAssistantTask`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/AssistantView.swift:505` `AppModel.runAssistantCommand`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L1293 · 计算属性** `private var queueCard: some View` — 根据当前状态计算并返回`queueCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1447` `AssistantView.taskStatusColor`

- **L1323 · 计算属性** `private var usageCard: some View` — 根据当前状态计算并返回`usageCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1348` `AssistantView.statusLine`

- **L1337 · 方法** `private func flowStep(_ number: String, _ title: String, active: Bool) -> some View` — 封装 `flowStep` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ number: String`；`_ title: String`；`active: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1348 · 方法** `private func statusLine(_ label: String, _ value: String) -> some View` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ label: String`；`_ value: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1357 · 方法** `private func badgeKind(_ status: String) -> AppStatusBadge.Kind` — 封装 `badgeKind` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`AppStatusBadge.Kind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1366 · 方法** `private func finishPushToTalk()` — 结束并收口与 `finishPushToTalk` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:9` `canonicalSpeechCommand`；`macos/AssistantView.swift:505` `AppModel.runAssistantCommand`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L1373 · 方法** `private func beginCommandHintsAnchorHover()` — 封装 `beginCommandHintsAnchorHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1388 · 方法** `private func endCommandHintsAnchorHover()` — 封装 `endCommandHintsAnchorHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1406` `AssistantView.scheduleCommandHintsClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `scheduleCommandHintsClose`；是否真实写入仍取决于分支和参数。

- **L1394 · 方法** `private func beginCommandHintsPanelHover()` — 封装 `beginCommandHintsPanelHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1400 · 方法** `private func endCommandHintsPanelHover()` — 封装 `endCommandHintsPanelHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1406` `AssistantView.scheduleCommandHintsClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `scheduleCommandHintsClose`；是否真实写入仍取决于分支和参数。

- **L1406 · 方法** `private func scheduleCommandHintsClose()` — 封装 `scheduleCommandHintsClose` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1419 · 计算属性** `private var displayedTask: AssistantTaskItem?` — 根据当前状态计算并返回`displayedTask` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`AssistantTaskItem?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1427 · 计算属性** `private var queuedTaskCount: Int` — 根据当前状态计算并返回`queuedTaskCount` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1431 · 计算属性** `private var workspaceTitle: String` — 根据当前状态计算并返回`workspaceTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1439 · 计算属性** `private var workspaceIcon: String` — 根据当前状态计算并返回`workspaceIcon` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1447 · 方法** `private func taskStatusColor(_ status: String) -> Color` — 封装状态、颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `macos/OperationLog.swift`

App 端操作日志读取、展示、脱敏和清理。

- **L4 · 结构体** `OperationLogEntry` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L9 · 初始化器** `init(id: UUID = UUID(), timestamp: Date, operation: String)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`timestamp: Date`；`operation: String`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 计算属性** `var displayTime: String` — 根据当前状态计算并返回时间。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L28 · 结构体** `OperationLogTrimResult` — 定义与操作、日志、结果相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L34 · 枚举** `OperationLogMaintenanceError` — 定义与操作、日志相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L38 · 计算属性** `var errorDescription: String?` — 根据当前状态计算并返回`errorDescription` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L48 · 枚举** `OperationLogReader` — 定义与操作、日志相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L49 · 方法** `static func entries(from url: URL) -> [OperationLogEntry]` — 封装 `entries` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`from url: URL`
  - 返回：`[OperationLogEntry]`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:57` `OperationLogReader.parse`

- **L57 · 方法** `static func parse(line: String) -> OperationLogEntry?` — 解析与 `parse` 对应的数据或步骤。
  - 输入：`line: String`
  - 返回：`OperationLogEntry?`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:71` `OperationLogReader.timestamp`；`macos/OperationLog.swift:161` `OperationLogReader.friendlyEvent`；`macos/OperationLog.swift:4` `OperationLogEntry`

- **L71 · 方法** `static func timestamp(from text: String) -> Date?` — 封装 `timestamp` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`from text: String`
  - 返回：`Date?`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:288` `ISO8601DateFormatter`

- **L78 · 方法** `static func fileSizeText(from url: URL) -> String` — 封装文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from url: URL`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L87 · 方法** `static func trim( toRecentDays days: Int, at url: URL, now: Date = Date(), calendar: Calendar = .current ) throws -> OperationLogTrimResult` — 封装 `trim` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`toRecentDays days: Int`；`at url: URL`；`now: Date = Date()`；`calendar: Calendar = .current`
  - 返回：`OperationLogTrimResult`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:28` `OperationLogTrimResult`；`macos/OperationLog.swift:71` `OperationLogReader.timestamp`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `setAttributes`, `replaceItemAt`；是否真实写入仍取决于分支和参数。

- **L161 · 方法** `private static func friendlyEvent(_ event: String) -> String` — 封装 `friendlyEvent` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ event: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L174 · 类** `OperationLogWriter` — 定义与操作、日志相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L181 · 计算属性** `private var logURL: URL` — 根据当前状态计算并返回日志。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L186 · 方法** `func setEnabled(_ value: Bool)` — 设置与 `setEnabled` 对应的数据或步骤。
  - 输入：`_ value: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L192 · 方法** `func isEnabled() -> Bool` — 封装 `isEnabled` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L198 · 方法** `func record( _ event: String, message: String, actor: String = "app", component: String = "swiftui", details: [String: Any] = [:], operationID: String? = nil, force: Bool = false )` — 记录记录相关数据或步骤。
  - 输入：`_ event: String`；`message: String`；`actor: String = "app"`；`component: String = "swiftui"`；`details: [String: Any] = [:]`；`operationID: String? = nil`；`force: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:272` `OperationLogWriter.redact`；`macos/OrderDashboardView.swift:1292` `Coordinator.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setAttributes`, `open`, `close`, `write`；是否真实写入仍取决于分支和参数。

- **L247 · 方法** `func trimLogToRecentDays( _ days: Int = 3, now: Date = Date(), calendar: Calendar = .current ) throws -> OperationLogTrimResult` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ days: Int = 3`；`now: Date = Date()`；`calendar: Calendar = .current`
  - 返回：`OperationLogTrimResult`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:87` `OperationLogReader.trim`

- **L257 · 方法** `func environment(operationID: String? = nil) -> [String: String]` — 封装 `environment` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`operationID: String? = nil`
  - 返回：`[String: String]`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:192` `OperationLogWriter.isEnabled`

- **L266 · 方法** `private static func sensitiveKey(_ key: String) -> Bool` — 封装 `sensitiveKey` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ key: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L272 · 方法** `private static func redact(_ value: Any, key: String? = nil) -> Any` — 封装 `redact` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: Any`；`key: String? = nil`
  - 返回：`Any`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:266` `OperationLogWriter.sensitiveKey`

- **L288 · 扩展** `ISO8601DateFormatter` — 定义与日期相关的扩展，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `macos/OrderDashboardView.swift`

订单看板、待处理中心、订单详情及生产/出库交互。

- **L45 · 结构体** `OrderDashboardTableLayout` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L50 · 初始化器** `init(totalWidth: CGFloat)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`totalWidth: CGFloat`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L67 · 计算属性** `var dataWidth: CGFloat` — 根据当前状态计算并返回`dataWidth` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L71 · 计算属性** `var trailingSpacerWidth: CGFloat` — 根据当前状态计算并返回`trailingSpacerWidth` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L75 · 计算属性** `var columns: [GridItem]` — 根据当前状态计算并返回`columns` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[GridItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L90 · 计算属性** `var dataColumns: [GridItem]` — 根据当前状态计算并返回`dataColumns` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[GridItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L104 · 结构体** `AppGlassDatePickerCalendar` — 定义与日期相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L111 · 初始化器** `init(selection: Binding<Date>, compact: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`selection: Binding<Date>`；`compact: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L117 · 计算属性** `private var daySize: CGFloat` — 根据当前状态计算并返回`daySize` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L118 · 计算属性** `private var gridSpacing: CGFloat` — 根据当前状态计算并返回`gridSpacing` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L119 · 计算属性** `private var columns: [GridItem]` — 根据当前状态计算并返回`columns` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[GridItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L123 · 计算属性** `private var calendar: Calendar` — 根据当前状态计算并返回`calendar` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Calendar`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L131 · 计算属性** `private var gridDates: [Date]` — 根据当前状态计算并返回`gridDates` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[Date]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L141 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:263` `appGlassDatePickerMonthTitle`；`macos/OrderDashboardView.swift:188` `AppGlassDatePickerCalendar.monthButton`；`macos/OrderDashboardView.swift:204` `AppGlassDatePickerCalendar.dayButton`

- **L188 · 方法** `private func monthButton(symbol: String, delta: Int, label: String) -> some View` — 封装 `monthButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`symbol: String`；`delta: Int`；`label: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L204 · 方法** `private func dayButton(_ date: Date) -> some View` — 封装 `dayButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:240` `appGlassDatePickerDate`；`macos/OrderDashboardView.swift:255` `appGlassDatePickerDisplayDate`

- **L240 · 函数** `func appGlassDatePickerDate(_ date: Date, preservingTimeFrom original: Date, calendar: Calendar) -> Date` — 封装日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`；`preservingTimeFrom original: Date`；`calendar: Calendar`
  - 返回：`Date`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L255 · 函数** `private func appGlassDatePickerDisplayDate(_ date: Date) -> String` — 封装日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L263 · 函数** `private func appGlassDatePickerMonthTitle(_ date: Date) -> String` — 封装日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L271 · 扩展** `View` — 定义 `View` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L272 · 方法** `func appGlassDatePickerPopoverSurface() -> some View` — 封装日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L278 · 函数** `func currentIssueRequiresInventoryMapping(_ issue: CurrentIssue) -> Bool` — 封装待处理问题、库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L293 · 函数** `private func serverWriteMaterialTypeRank(_ materialType: String) -> Int` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ materialType: String`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L302 · 函数** `private func serverWritePlywoodThicknessRank(_ thickness: String) -> Int` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ thickness: String`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`

- **L310 · 函数** `func sortedServerWriteMaterialChanges(_ changes: [ServerWriteMaterialChange]) -> [ServerWriteMaterialChange]` — 排序Server 数据、材料相关数据或步骤。
  - 输入：`_ changes: [ServerWriteMaterialChange]`
  - 返回：`[ServerWriteMaterialChange]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:293` `serverWriteMaterialTypeRank`；`macos/OrderDashboardView.swift:302` `serverWritePlywoodThicknessRank`；`macos/TravelerAssistant.swift:1229` `Double`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `serverWriteMaterialTypeRank`, `serverWritePlywoodThicknessRank`；是否真实写入仍取决于分支和参数。

- **L336 · 函数** `func dashboardMessageHoverCanPresent(appIsActive: Bool, mainWindowIsFrontmost: Bool) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`appIsActive: Bool`；`mainWindowIsFrontmost: Bool`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L348 · 函数** `func orderDashboardMetricsFit(width: CGFloat, horizontalPadding: CGFloat) -> Bool` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`width: CGFloat`；`horizontalPadding: CGFloat`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L354 · 函数** `func orderDashboardPanelColors(_ materials: [OrderMaterialPreview]) -> [String]` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ materials: [OrderMaterialPreview]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L364 · 函数** `func orderDashboardPanelMaterials(_ materials: [OrderMaterialPreview]) -> [OrderMaterialPreview]` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ materials: [OrderMaterialPreview]`
  - 返回：`[OrderMaterialPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L377 · 函数** `func panelMaterialImageURL(productCode: String) -> URL?` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`productCode: String`
  - 返回：`URL?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L393 · 类** `PanelMaterialHoverTrackingView` — 定义与材料相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L397 · 方法** `override func updateTrackingAreas()` — 更新与 `updateTrackingAreas` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L410 · 方法** `override func mouseEntered(with event: NSEvent)` — 封装 `mouseEntered` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`with event: NSEvent`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L415 · 方法** `override func mouseExited(with event: NSEvent)` — 封装 `mouseExited` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`with event: NSEvent`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L421 · 结构体** `PanelMaterialHoverTracking` — 定义与材料相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L425 · 方法** `func makeNSView(context: Context) -> PanelMaterialHoverTrackingView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`PanelMaterialHoverTrackingView`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:393` `PanelMaterialHoverTrackingView`

- **L432 · 方法** `func updateNSView(_ nsView: PanelMaterialHoverTrackingView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: PanelMaterialHoverTrackingView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L438 · 结构体** `PanelMaterialHoverPreview<Content` — 定义与材料相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L445 · 初始化器** `init(material: OrderMaterialPreview, @ViewBuilder content: () -> Content)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`material: OrderMaterialPreview`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L450 · 计算属性** `private var imageURL: URL?` — 根据当前状态计算并返回`imageURL` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL?`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:377` `panelMaterialImageURL`

- **L454 · 计算属性** `private var previewImage: NSImage?` — 预览预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`NSImage?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L458 · 计算属性** `private var previewImageWidth: CGFloat` — 预览预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L465 · 计算属性** `private var panelDisplayName: String` — 根据当前状态计算并返回名称。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L471 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:421` `PanelMaterialHoverTracking`

- **L517 · 函数** `func orderDetailPlywoodRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`[OrderMaterialPreview]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:944` `orderedMaterialRows`

- **L521 · 函数** `func orderDetailPanelRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`[OrderMaterialPreview]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:539` `orderDetailPanelThicknessRank`

- **L539 · 函数** `func orderDetailPanelThicknessRank(_ thickness: Double) -> Int` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ thickness: Double`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L545 · 函数** `func orderDetailEdgeColors(_ colors: [String]) -> [String]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ colors: [String]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L553 · 函数** `func orderDashboardShortageCount(_ rows: [OrderStockPreview]) -> Int` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderStockPreview]`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L557 · 函数** `func orderDashboardStatus(previewValidated: Bool, hasError: Bool, isExistingTraveler: Bool) -> String` — 封装订单、看板、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`previewValidated: Bool`；`hasError: Bool`；`isExistingTraveler: Bool`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L563 · 函数** `func orderDashboardExpandedID(current: String?, tapped: String, forceOpen: Bool = false) -> String?` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`current: String?`；`tapped: String`；`forceOpen: Bool = false`
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L568 · 结构体** `OrderDashboardClickContainer<Content` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L573 · 初始化器** `init( onSingleClick: @escaping () -> Void, onDoubleClick: @escaping () -> Void, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`onSingleClick: @escaping () -> Void`；`onDoubleClick: @escaping () -> Void`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L583 · 方法** `func makeCoordinator() -> Coordinator` — 创建与 `makeCoordinator` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Coordinator`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L587 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L616 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L624 · 类** `Coordinator` — 定义 `Coordinator` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L628 · 初始化器** `init(onSingleClick: @escaping () -> Void, onDoubleClick: @escaping () -> Void)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`onSingleClick: @escaping () -> Void`；`onDoubleClick: @escaping () -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L633 · 方法** `func gestureRecognizer(_ gestureRecognizer: NSGestureRecognizer, shouldRequireFailureOf otherGestureRecognizer: NSGestureRecognizer) -> Bool` — 封装 `gestureRecognizer` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ gestureRecognizer: NSGestureRecognizer`；`shouldRequireFailureOf otherGestureRecognizer: NSGestureRecognizer`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L645 · 函数** `func toggledOrderFactorySelection(_ selected: Set<String>, factoryOrder: String) -> Set<String>` — 封装订单、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ selected: Set<String>`；`factoryOrder: String`
  - 返回：`Set<String>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L655 · 函数** `func selectedOrderFactoryNames(_ factories: [OrderFactoryPreview], selected: Set<String>) -> [String]` — 选择订单、工厂单相关数据或步骤。
  - 输入：`_ factories: [OrderFactoryPreview]`；`selected: Set<String>`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L662 · 函数** `func orderDashboardHasShippedSelection( _ selected: Set<String>, statuses: [String: String] ) -> Bool` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ selected: Set<String>`；`statuses: [String: String]`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L669 · 函数** `func orderDashboardNeedsOutboundUpdateSelection( _ selected: Set<String>, statuses: [String: String] ) -> Bool` — 封装订单、看板、出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ selected: Set<String>`；`statuses: [String: String]`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L676 · 函数** `func orderDashboardHasProducedSelection( _ selected: Set<String>, produced: [String: Bool] ) -> Bool` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ selected: Set<String>`；`produced: [String: Bool]`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L683 · 函数** `func orderDashboardOutboundActionTitle( _ selected: Set<String>, statuses: [String: String] ) -> String` — 封装订单、看板、出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ selected: Set<String>`；`statuses: [String: String]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L690 · 函数** `func orderDashboardOutboundDisplay(status: String, documentNumber: String) -> String` — 封装订单、看板、出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`status: String`；`documentNumber: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L697 · 函数** `func orderDashboardStageMatchesFilter(_ stage: String, statusFilter: String) -> Bool` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stage: String`；`statusFilter: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:704` `orderDashboardIsCompleted`

- **L704 · 函数** `func orderDashboardIsCompleted(_ stage: String) -> Bool` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stage: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L708 · 函数** `func orderDashboardStatusHelp(status: String, validationMessage: String) -> String` — 封装订单、看板、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`status: String`；`validationMessage: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L716 · 函数** `func orderDashboardProgressFraction(completed: Int, total: Int) -> Double` — 封装订单、看板、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`completed: Int`；`total: Int`
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`

- **L721 · 函数** `func orderInstallationDisplayDate(_ value: String) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L731 · 函数** `func orderInstallationDateSummary(_ days: [OrderInstallationDay]) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ days: [OrderInstallationDay]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:721` `orderInstallationDisplayDate`

- **L736 · 函数** `func orderInstallationPlannedDateSummary(_ days: [OrderInstallationDay]) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ days: [OrderInstallationDay]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:721` `orderInstallationDisplayDate`

- **L741 · 函数** `func orderInstallationQuickSummaries( planned: [OrderInstallationDay], actual: [OrderInstallationDay] ) -> [String]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`planned: [OrderInstallationDay]`；`actual: [OrderInstallationDay]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:736` `orderInstallationPlannedDateSummary`；`macos/OrderDashboardView.swift:731` `orderInstallationDateSummary`

- **L757 · 结构体** `OrderDashboardProgressBar` — 定义与订单、看板、进度相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L762 · 初始化器** `init(completed: Int, total: Int, accessibilityTitle: String = "优化进度")` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`completed: Int`；`total: Int`；`accessibilityTitle: String = "优化进度"`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L768 · 计算属性** `private var fraction: Double` — 根据当前状态计算并返回`fraction` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:716` `orderDashboardProgressFraction`

- **L772 · 计算属性** `private var progressColor: Color` — 根据当前状态计算并返回进度、颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L776 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L793 · 函数** `func shouldPresentPendingCenterAfterAimes( presentIfNeeded: Bool, pendingAimesReviews: [AimesReviewItem] ) -> Bool` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`presentIfNeeded: Bool`；`pendingAimesReviews: [AimesReviewItem]`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L800 · 结构体** `DashboardMessage` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L813 · 初始化器** `init( id: String, source: String, time: String, title: String, detail: String, state: String, manualPaths: [String] = [], operationDetails: [String] = [], contextDetails: [String] = [], duration: TimeInterval? = nil, operationDurations: [DashboardOperationDuration] = [] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`source: String`；`time: String`；`title: String`；`detail: String`；`state: String`；`manualPaths: [String] = []`；`operationDetails: [String] = []`；`contextDetails: [String] = []`；`duration: TimeInterval? = nil`；`operationDurations: [DashboardOperationDuration] = []`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L840 · 结构体** `DashboardOperationDisplay` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L845 · 函数** `func dashboardMessageState(_ text: String) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L852 · 函数** `func dashboardMessageDetail(_ text: String) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L859 · 函数** `func dashboardStatusIsInProgress(_ text: String) -> Bool` — 封装看板、状态、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:852` `dashboardMessageDetail`

- **L864 · 函数** `func dashboardMessages( syncStatus: String, syncTime: String, inventoryStatus: String = "库存操作尚未执行", inventoryTime: String = "", aimesStatus: String, aimesTime: String, serverStatus: String, serverTime: String, activity: [InventoryStep], operationDetailsBySource: [String: [String]] = [:], manualPathsBySource: [String: [String]] = [:], contextDetailsBySource: [String: [String]] = [:], durationsBySource: [String: TimeInterval] = [:], operationDurationsBySource: [String: [DashboardOperationDuration]] = [:] ) -> [DashboardMessage]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`syncStatus: String`；`syncTime: String`；`inventoryStatus: String = "库存操作尚未执行"`；`inventoryTime: String = ""`；`aimesStatus: String`；`aimesTime: String`；`serverStatus: String`；`serverTime: String`；`activity: [InventoryStep]`；`operationDetailsBySource: [String: [String]] = [:]`；`manualPathsBySource: [String: [String]] = [:]`；`contextDetailsBySource: [String: [String]] = [:]`；`durationsBySource: [String: TimeInterval] = [:]`；`operationDurationsBySource: [String: [DashboardOperationDuration]] = [:]`
  - 返回：`[DashboardMessage]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:852` `dashboardMessageDetail`；`macos/OrderDashboardView.swift:800` `DashboardMessage`；`macos/OrderDashboardView.swift:845` `dashboardMessageState`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L937 · 函数** `func dashboardVisibleMessages(_ messages: [DashboardMessage], isRunning: Bool) -> [DashboardMessage]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ messages: [DashboardMessage]`；`isRunning: Bool`
  - 返回：`[DashboardMessage]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:859` `dashboardStatusIsInProgress`

- **L942 · 函数** `func dashboardCurrentOperation( messages: [DashboardMessage], isRunning: Bool ) -> DashboardOperationDisplay?` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`messages: [DashboardMessage]`；`isRunning: Bool`
  - 返回：`DashboardOperationDisplay?`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:859` `dashboardStatusIsInProgress`；`macos/OrderDashboardView.swift:840` `DashboardOperationDisplay`

- **L956 · 函数** `func dashboardMessageScrollKey(_ messages: [DashboardMessage]) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ messages: [DashboardMessage]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L965 · 函数** `func dashboardMessageSupportsHoverDetail(_ message: DashboardMessage) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: DashboardMessage`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:859` `dashboardStatusIsInProgress`

- **L974 · 函数** `func dashboardMessageDetailText(_ message: DashboardMessage) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: DashboardMessage`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1182` `operationDurationText`

- **L988 · 函数** `func dashboardMessageSummaryText(_ message: DashboardMessage, showsDuration: Bool = true) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: DashboardMessage`；`showsDuration: Bool = true`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1182` `operationDurationText`

- **L996 · 函数** `func dashboardAimesReviewDetail(_ item: AimesReviewItem, status: String) -> String` — 封装看板、AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`status: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1007 · 函数** `func dashboardAimesActionDetails( pending: [AimesReviewItem], ignored: [AimesReviewItem], assigned: [AimesReviewItem] ) -> [String]` — 封装看板、AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`pending: [AimesReviewItem]`；`ignored: [AimesReviewItem]`；`assigned: [AimesReviewItem]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:996` `dashboardAimesReviewDetail`

- **L1028 · 函数** `func dashboardAimesWarningDetails(_ warnings: [[String: Any]]) -> [String]` — 封装看板、AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ warnings: [[String: Any]]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1044 · 结构体** `DashboardMessageTracePopover` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1047 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:974` `dashboardMessageDetailText`；`macos/OrderDashboardView.swift:1102` `DashboardMessageTracePopover.dashboardTraceBullet`；`macos/TravelerAssistant.swift:1182` `operationDurationText`

- **L1102 · 方法** `private func dashboardTraceBullet(_ text: String) -> some View` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1113 · 类** `DashboardMessageTraceTrackingView` — 定义与看板相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1117 · 方法** `override func updateTrackingAreas()` — 更新与 `updateTrackingAreas` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1130 · 方法** `override func mouseEntered(with event: NSEvent)` — 封装 `mouseEntered` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`with event: NSEvent`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1135 · 方法** `override func mouseExited(with event: NSEvent)` — 封装 `mouseExited` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`with event: NSEvent`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1141 · 结构体** `DashboardMessageTracePanelPresenter` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1147 · 方法** `func makeCoordinator() -> Coordinator` — 创建与 `makeCoordinator` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Coordinator`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1151 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1157 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update`；是否真实写入仍取决于分支和参数。

- **L1167 · 方法** `static func dismantleNSView(_ nsView: NSView, coordinator: Coordinator)` — 封装 `dismantleNSView` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ nsView: NSView`；`coordinator: Coordinator`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1292` `Coordinator.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close`；是否真实写入仍取决于分支和参数。

- **L1171 · 类** `Coordinator` — 定义 `Coordinator` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1180 · 方法** `func update( anchorView: NSView, message: DashboardMessage, isPresented: Bool, onPanelEntered: @escaping () -> Void, onPanelExited: @escaping () -> Void )` — 更新与 `update` 对应的数据或步骤。
  - 输入：`anchorView: NSView`；`message: DashboardMessage`；`isPresented: Bool`；`onPanelEntered: @escaping () -> Void`；`onPanelExited: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1292` `Coordinator.close`；`macos/OrderDashboardView.swift:1203` `Coordinator.presentIfNeeded`；`macos/OrderDashboardView.swift:1265` `Coordinator.updatePosition`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close`, `updatePosition`；是否真实写入仍取决于分支和参数。

- **L1203 · 方法** `private func presentIfNeeded()` — 封装 `presentIfNeeded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:336` `dashboardMessageHoverCanPresent`；`macos/OrderDashboardView.swift:1044` `DashboardMessageTracePopover`；`macos/OrderDashboardView.swift:1113` `DashboardMessageTraceTrackingView`；`macos/OrderDashboardView.swift:1265` `Coordinator.updatePosition`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setContentSize`, `updatePosition`；是否真实写入仍取决于分支和参数。

- **L1265 · 方法** `private func updatePosition()` — 更新与 `updatePosition` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setFrameOrigin`；是否真实写入仍取决于分支和参数。

- **L1292 · 方法** `func close()` — 关闭与 `close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1298 · 析构器** `deinit` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1292` `Coordinator.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close`；是否真实写入仍取决于分支和参数。

- **L1304 · 结构体** `DashboardMessageTraceHost<Content` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1313 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1343` `DashboardMessageTraceHost<Content.beginHover`；`macos/OrderDashboardView.swift:1362` `DashboardMessageTraceHost<Content.endHover`；`macos/OrderDashboardView.swift:1141` `DashboardMessageTracePanelPresenter`

- **L1343 · 方法** `private func beginHover()` — 封装 `beginHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1362 · 方法** `private func endHover()` — 封装 `endHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1369` `DashboardMessageTraceHost<Content.schedulePopoverClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `schedulePopoverClose`；是否真实写入仍取决于分支和参数。

- **L1369 · 方法** `private func schedulePopoverClose()` — 封装 `schedulePopoverClose` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1380 · 方法** `private func panelEntered()` — 封装 `panelEntered` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1387 · 方法** `private func panelExited()` — 封装 `panelExited` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1369` `DashboardMessageTraceHost<Content.schedulePopoverClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `schedulePopoverClose`；是否真实写入仍取决于分支和参数。

- **L1395 · 结构体** `OrderDashboardView` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1411 · 计算属性** `private var filteredOrders: [OrderDashboardItem]` — 根据当前状态计算并返回`filteredOrders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderDashboardItem]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:697` `orderDashboardStageMatchesFilter`

- **L1421 · 计算属性** `private var selectedFactory: OrderFactoryPreview?` — 选择工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`OrderFactoryPreview?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1425 · 计算属性** `private var availableHardwareFactoryOrders: Set<String>` — 根据当前状态计算并返回五金、工厂单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Set<String>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L1434 · 方法** `private func traceHost<Content: View>( for message: DashboardMessage, @ViewBuilder content: @escaping () -> Content ) -> some View` — 封装 `traceHost` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`for message: DashboardMessage`；`@ViewBuilder content: @escaping () -> Content`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:965` `dashboardMessageSupportsHoverDetail`

- **L1449 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5011` `View.appPageFrame`；`macos/TravelerAssistant.swift:2158` `AppModel.startOrderDashboard`；`macos/OrderDashboardView.swift:2084` `OrderDashboardView.openRequestedOrderIfAvailable`；`macos/OrderDashboardView.swift:2153` `OrderDashboardDetailPage`；`macos/OrderDashboardView.swift:2413` `OrderAnnotationsSheet`；`macos/OrderDashboardView.swift:3571` `OrderCostSheet`；`macos/OrderDashboardView.swift:4771` `FactoryStockComparisonSheet`；`macos/OrderDashboardView.swift:2845` `ProductionSheet`；`macos/OrderDashboardView.swift:3059` `OrderShipmentConfirmationSheet`；`macos/TravelerAssistant.swift:3312` `AppModel.startDirectOrderShipment`；`macos/OrderDashboardView.swift:3132` `OutboundScopeSheet`；`macos/TravelerAssistant.swift:2704` `AppModel.prepareSelectedServerFolder`；另有 1 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openRequestedOrderIfAvailable`, `OutboundScopeSheet`；是否真实写入仍取决于分支和参数。

- **L1541 · 计算属性** `private var dashboardSections: some View` — 根据当前状态计算并返回看板。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1550 · 计算属性** `private var toolbar: some View` — 根据当前状态计算并返回`toolbar` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2271` `AppModel.syncDashboardAimes`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:2445` `AppModel.scanDashboardServer`

- **L1621 · 计算属性** `private var dashboardActivityLog: some View` — 根据当前状态计算并返回看板、日志。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:635` `serverFolderChangeGroups`；`macos/OrderDashboardView.swift:859` `dashboardStatusIsInProgress`；`macos/OrderDashboardView.swift:1007` `dashboardAimesActionDetails`；`macos/OrderDashboardView.swift:1028` `dashboardAimesWarningDetails`；`macos/OrderDashboardView.swift:864` `dashboardMessages`；`macos/OrderDashboardView.swift:937` `dashboardVisibleMessages`；`macos/OrderDashboardView.swift:942` `dashboardCurrentOperation`；`macos/OrderDashboardView.swift:956` `dashboardMessageScrollKey`；`macos/OrderDashboardView.swift:1738` `OrderDashboardView.currentOperationRow`；`macos/OrderDashboardView.swift:1434` `OrderDashboardView.traceHost`；`macos/OrderDashboardView.swift:1793` `OrderDashboardView.activityIcon`；`macos/OrderDashboardView.swift:1802` `OrderDashboardView.activityColor`；另有 2 个直接调用

- **L1738 · 方法** `private func currentOperationRow(_ display: DashboardOperationDisplay?) -> some View` — 封装操作、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ display: DashboardOperationDisplay?`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1768` `OrderDashboardView.currentOperationIcon`；`macos/OrderDashboardView.swift:988` `dashboardMessageSummaryText`

- **L1768 · 方法** `private func currentOperationIcon(_ display: DashboardOperationDisplay) -> some View` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ display: DashboardOperationDisplay`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1793` `OrderDashboardView.activityIcon`；`macos/OrderDashboardView.swift:1802` `OrderDashboardView.activityColor`

- **L1786 · 方法** `private func scrollMessagesToBottom(_ proxy: ScrollViewProxy, messages: [DashboardMessage])` — 封装 `scrollMessagesToBottom` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ proxy: ScrollViewProxy`；`messages: [DashboardMessage]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1793 · 方法** `private func activityIcon(_ state: String) -> String` — 封装 `activityIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1802 · 方法** `private func activityColor(_ state: String) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1811 · 计算属性** `private var orderTable: some View` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:45` `OrderDashboardTableLayout`；`macos/OrderDashboardView.swift:1851` `OrderDashboardView.orderTableHeader`；`macos/OrderDashboardView.swift:1888` `OrderDashboardView.orderRow`

- **L1851 · 方法** `private func orderTableHeader(layout: OrderDashboardTableLayout) -> some View` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`layout: OrderDashboardTableLayout`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2096` `OrderDashboardView.tableHeader`

- **L1888 · 方法** `private func orderRow( _ item: OrderDashboardItem, isLastRow: Bool = false, layout: OrderDashboardTableLayout ) -> some View` — 封装订单、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`；`isLastRow: Bool = false`；`layout: OrderDashboardTableLayout`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2102` `OrderDashboardView.tableCell`；`macos/OrderDashboardView.swift:741` `orderInstallationQuickSummaries`；`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/OrderDashboardView.swift:2108` `OrderDashboardView.statusKind`；`macos/OrderDashboardView.swift:708` `orderDashboardStatusHelp`；`macos/OrderDashboardView.swift:757` `OrderDashboardProgressBar`；`macos/TravelerAssistant.swift:1263` `appDisplayTimestamp`；`macos/OrderDashboardView.swift:2072` `OrderDashboardView.toggleExpanded`；`macos/OrderDashboardView.swift:2079` `OrderDashboardView.openOrderDetail`；`macos/OrderDashboardView.swift:2642` `OrderDashboardDetailCard`；`macos/TravelerAssistant.swift:4702` `AppModel.checkSelectedOrderStock`；`macos/TravelerAssistant.swift:3139` `AppModel.loadProductionPreview`；另有 2 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderDetail`；是否真实写入仍取决于分支和参数。

- **L2064 · 方法** `private func prepareSelectedOrder(_ item: OrderDashboardItem)` — 准备并校验订单相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:704` `orderDashboardIsCompleted`；`macos/TravelerAssistant.swift:4491` `AppModel.loadOrderDetailFromDatabase`

- **L2072 · 方法** `private func toggleExpanded(_ item: OrderDashboardItem)` — 封装 `toggleExpanded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:563` `orderDashboardExpandedID`；`macos/OrderDashboardView.swift:2064` `OrderDashboardView.prepareSelectedOrder`

- **L2079 · 方法** `private func openOrderDetail(_ item: OrderDashboardItem)` — 打开订单相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2064` `OrderDashboardView.prepareSelectedOrder`

- **L2084 · 方法** `private func openRequestedOrderIfAvailable()` — 打开订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2096 · 方法** `private func tableHeader(_ title: String, width: CGFloat) -> some View` — 封装 `tableHeader` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`width: CGFloat`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2102 · 方法** `private func tableCell<Content: View>(width: CGFloat, @ViewBuilder content: () -> Content) -> some View` — 封装 `tableCell` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`width: CGFloat`；`@ViewBuilder content: () -> Content`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2108 · 方法** `private func statusKind(_ status: String) -> AppStatusBadge.Kind` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`AppStatusBadge.Kind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2118 · 结构体** `OrderShipmentRequest` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2124 · 结构体** `OrderDashboardMetricsView` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2127 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:553` `orderDashboardShortageCount`；`macos/OrderDashboardView.swift:2142` `OrderDashboardMetricsView.metric`；`macos/TravelerAssistant.swift:2158` `AppModel.startOrderDashboard`

- **L2142 · 方法** `private func metric(_ title: String, _ value: String, _ color: Color) -> some View` — 封装 `metric` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ value: String`；`_ color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2153 · 结构体** `OrderDashboardDetailPage` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2158 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5011` `View.appPageFrame`

- **L2194 · 计算属性** `private var orderIdentityCard: some View` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:4655` `AppModel.generateSelectedOrder`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`

- **L2215 · 计算属性** `private var boardAndEdgeSection: some View` — 根据当前状态计算并返回`boardAndEdgeSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2234` `OrderDashboardDetailPage.materialRow`；`macos/OrderDashboardView.swift:517` `orderDetailPlywoodRows`；`macos/OrderDashboardView.swift:521` `orderDetailPanelRows`

- **L2234 · 方法** `private func materialRow(title: String, rows: [OrderMaterialPreview]) -> some View` — 封装材料、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`rows: [OrderMaterialPreview]`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2330` `OrderDashboardDetailPage.orderDetailCard`；`macos/TravelerAssistant.swift:933` `orderMaterialDisplayName`

- **L2258 · 计算属性** `@ViewBuilder private var edgeBandingRow: some View` — 根据当前状态计算并返回行数据。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:545` `orderDetailEdgeColors`；`macos/OrderDashboardView.swift:2330` `OrderDashboardDetailPage.orderDetailCard`

- **L2283 · 计算属性** `private var hardwareSection: some View` — 根据当前状态计算并返回五金。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2305` `OrderDashboardDetailPage.hardwareFactorySection`

- **L2305 · 方法** `private func hardwareFactorySection(title: String, rows: [OrderFittingPreview]) -> some View` — 封装五金、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`rows: [OrderFittingPreview]`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2330` `OrderDashboardDetailPage.orderDetailCard`

- **L2330 · 方法** `private func orderDetailCard( name: String, subtitle: String, value: String, panelMaterial: OrderMaterialPreview? = nil ) -> some View` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: String`；`subtitle: String`；`value: String`；`panelMaterial: OrderMaterialPreview? = nil`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2368 · 结构体** `OrderInstallationDraft` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2374 · 函数** `private func orderInstallationDateFormatter() -> DateFormatter` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`DateFormatter`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2383 · 函数** `private func orderInstallationDraftDate(_ value: String) -> Date` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`Date`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2374` `orderInstallationDateFormatter`

- **L2387 · 函数** `private func orderInstallationDraftValue(_ value: Date) -> String` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2374` `orderInstallationDateFormatter`

- **L2391 · 函数** `private func orderInstallationPickerDisplayDate(_ value: Date) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2400 · 函数** `private func orderInstallationInstallerSuggestions(from orders: [OrderDashboardItem]) -> [String]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from orders: [OrderDashboardItem]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L2413 · 结构体** `OrderAnnotationsSheet` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2418 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/OrderDashboardView.swift:2442` `OrderAnnotationsEditor`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L2442 · 结构体** `OrderAnnotationsEditor` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2451 · 初始化器** `init(model: AppModel, order: OrderDashboardItem)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`order: OrderDashboardItem`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2368` `OrderInstallationDraft`；`macos/OrderDashboardView.swift:2383` `orderInstallationDraftDate`

- **L2464 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2508` `OrderAnnotationsEditor.installationRows`；`macos/OrderDashboardView.swift:2616` `OrderAnnotationsEditor.save`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save`；是否真实写入仍取决于分支和参数。

- **L2508 · 方法** `private func installationRows( title: String, rows: Binding<[OrderInstallationDraft]> ) -> some View` — 封装 `installationRows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`rows: Binding<[OrderInstallationDraft]>`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2368` `OrderInstallationDraft`；`macos/OrderDashboardView.swift:2391` `orderInstallationPickerDisplayDate`；`macos/OrderDashboardView.swift:104` `AppGlassDatePickerCalendar`；`macos/OrderDashboardView.swift:272` `View.appGlassDatePickerPopoverSurface`；`macos/OrderDashboardView.swift:2400` `orderInstallationInstallerSuggestions`；`macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`macos/OrderDashboardView.swift:2387` `orderInstallationDraftValue`；`macos/OrderDashboardView.swift:721` `orderInstallationDisplayDate`

- **L2616 · 方法** `private func save()` — 保存与 `save` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`macos/OrderDashboardView.swift:2387` `orderInstallationDraftValue`；`macos/TravelerAssistant.swift:4578` `AppModel.saveOrderAnnotations`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveOrderAnnotations`；是否真实写入仍取决于分支和参数。

- **L2642 · 结构体** `OrderDashboardDetailCard` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2654 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2663 · 计算属性** `private var detailActions: some View` — 根据当前状态计算并返回`detailActions` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:683` `orderDashboardOutboundActionTitle`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:4744` `AppModel.calculateSelectedOrderCost`；`macos/OrderDashboardView.swift:676` `orderDashboardHasProducedSelection`；`macos/OrderDashboardView.swift:662` `orderDashboardHasShippedSelection`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderDashboardOutboundActionTitle`, `onOpenScope`, `onOpenProduction`, `onOpenOutbound`；是否真实写入仍取决于分支和参数。

- **L2727 · 计算属性** `private var panelColorsSummary: some View` — 根据当前状态计算并返回`panelColorsSummary` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:364` `orderDashboardPanelMaterials`

- **L2755 · 计算属性** `private var factoriesPanel: some View` — 根据当前状态计算并返回`factoriesPanel` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2761 · 计算属性** `private var factoryTable: some View` — 根据当前状态计算并返回工厂单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2793` `OrderDashboardDetailCard.factoryTableRow`；`macos/OrderDashboardView.swift:645` `toggledOrderFactorySelection`

- **L2793 · 方法** `private func factoryTableRow( isHeader: Bool, factory: OrderFactoryPreview? = nil, dashboardFactory: OrderDashboardFactory? = nil, selected: Bool = false ) -> some View` — 封装工厂单、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`isHeader: Bool`；`factory: OrderFactoryPreview? = nil`；`dashboardFactory: OrderDashboardFactory? = nil`；`selected: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2834` `OrderDashboardDetailCard.factoryCell`；`macos/OrderDashboardView.swift:690` `orderDashboardOutboundDisplay`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderDashboardOutboundDisplay`；是否真实写入仍取决于分支和参数。

- **L2834 · 方法** `private func factoryCell(_ text: String, width: CGFloat? = nil, status: Bool = false) -> some View` — 封装工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`；`width: CGFloat? = nil`；`status: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2845 · 结构体** `ProductionSheet` — 定义与生产相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2855 · 枚举** `SheetOperationState` — 定义与操作相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2864 · 计算属性** `private var isProcessing: Bool` — 根据当前状态计算并返回`isProcessing` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2868 · 计算属性** `private var selectedQuantityCount: Int` — 选择数量相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`

- **L2872 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:168` `sortedProductionMaterialDrafts`；`macos/TravelerAssistant.swift:119` `productionMaterialTypeDisplayName`；`macos/TravelerAssistant.swift:128` `productionMaterialName`；`macos/OrderDashboardView.swift:3020` `ProductionSheet.submitProduction`；`macos/TravelerAssistant.swift:3139` `AppModel.loadProductionPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `onClose`；是否真实写入仍取决于分支和参数。

- **L2971 · 计算属性** `private var productionOperationBanner: some View` — 根据当前状态计算并返回生产、操作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3020 · 方法** `private func submitProduction()` — 封装生产相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3177` `AppModel.prepareProduction`；`macos/TravelerAssistant.swift:3194` `AppModel.startDirectProduction`

- **L3059 · 结构体** `OrderShipmentConfirmationSheet` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3066 · 计算属性** `private var fittings: [OrderFittingPreview]` — 根据当前状态计算并返回`fittings` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderFittingPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3070 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`

- **L3132 · 结构体** `OutboundScopeSheet` — 定义与出库、范围相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3146 · 计算属性** `private var incomingProcessing: Bool` — 根据当前状态计算并返回`incomingProcessing` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3147 · 计算属性** `private var noOutboundDecision: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3150 · 计算属性** `private var hardwareAvailable: Bool` — 根据当前状态计算并返回五金。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3152 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:3253` `OutboundScopeSheet.scopeSegment`；`macos/TravelerAssistant.swift:3414` `AppModel.saveOutboundScope`；`macos/OrderDashboardView.swift:3227` `OutboundScopeSheet.loadSavedScopeIfNeeded`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveOutboundScope`；是否真实写入仍取决于分支和参数。

- **L3227 · 方法** `private func loadSavedScopeIfNeeded()` — 读取范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3392` `AppModel.loadOutboundScope`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `loadOutboundScope`；是否真实写入仍取决于分支和参数。

- **L3253 · 方法** `private func scopeSegment(_ title: String, value: String, disabled: Bool = false) -> some View` — 封装范围相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`value: String`；`disabled: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3269 · 结构体** `PendingCenterSheet` — 定义 `PendingCenterSheet` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3274 · 计算属性** `private var items: [PendingCenterItem]` — 根据当前状态计算并返回`items` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3275 · 计算属性** `private var serverItems: [PendingCenterItem]` — 根据当前状态计算并返回Server 数据。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3276 · 计算属性** `private var selectedServerCount: Int` — 选择Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3282 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/OrderDashboardView.swift:3341` `PendingCenterSheet.pendingItemRow`；`macos/TravelerAssistant.swift:2341` `AppModel.ignoreSelectedAimesFactories`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:2506` `AppModel.processPendingServerChanges`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L3341 · 方法** `private func pendingItemRow(_ item: PendingCenterItem) -> some View` — 封装项目、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: PendingCenterItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2481` `AppModel.toggleServerFolderSelection`；`macos/OrderDashboardView.swift:3401` `PendingCenterSheet.pendingItemDetails`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L3401 · 方法** `private func pendingItemDetails(_ item: PendingCenterItem) -> some View` — 封装项目相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: PendingCenterItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:3561` `PendingCenterSheet.changeTimeLabel`；`macos/OrderDashboardView.swift:3531` `PendingCenterSheet.changeTypeName`；`macos/TravelerAssistant.swift:2748` `AppModel.markTemporaryFolderManual`；`macos/OrderDashboardView.swift:3450` `PendingCenterSheet.issueDetails`；`macos/OrderDashboardView.swift:3502` `PendingCenterSheet.aimesDetails`

- **L3450 · 方法** `private func issueDetails(_ issue: CurrentIssue) -> some View` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:278` `currentIssueRequiresInventoryMapping`；`macos/TravelerAssistant.swift:4828` `AppModel.openDashboardLocation`；`macos/TravelerAssistant.swift:2238` `AppModel.autoResolveCurrentIssue`；`macos/TravelerAssistant.swift:2253` `AppModel.resolveCurrentIssue`；`macos/TravelerAssistant.swift:2818` `AppModel.requestInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openDashboardLocation`；是否真实写入仍取决于分支和参数。

- **L3502 · 方法** `private func aimesDetails(_ item: AimesReviewItem) -> some View` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2332` `AppModel.toggleAimesReviewSelection`；`macos/TravelerAssistant.swift:2387` `AppModel.assignAimesFactoryToSuggestedOrder`

- **L3531 · 方法** `private func changeTypeName(_ type: String) -> String` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3541 · 方法** `private func changeIcon(_ type: String) -> String` — 封装 `changeIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3551 · 方法** `private func changeColor(_ type: String) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3561 · 方法** `private func changeTimeLabel(_ change: ServerChangePreview) -> String` — 封装时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ change: ServerChangePreview`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1263` `appDisplayTimestamp`

- **L3571 · 结构体** `OrderCostSheet` — 定义与订单、成本相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3578 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4744` `AppModel.calculateSelectedOrderCost`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/OrderDashboardView.swift:3671` `OrderCostSheet.costCard`；`macos/OrderDashboardView.swift:3698` `OrderCostSheet.costLine`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L3671 · 方法** `private func costCard(_ title: String, value: String, warning: Bool) -> some View` — 封装成本相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`value: String`；`warning: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3683 · 计算属性** `private var costLineHeader: some View` — 根据当前状态计算并返回成本。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3698 · 方法** `private func costLine(_ row: OrderCostLine) -> some View` — 封装成本相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderCostLine`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3730 · 计算属性** `private var orderCostSourceTotals: [OrderCostFactoryTotal]` — 根据当前状态计算并返回订单、成本、来源。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderCostFactoryTotal]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:3745` `OrderCostSheet.sourceTotal`

- **L3745 · 方法** `private func sourceTotal( id: String, title: String, categories: [String] ) -> OrderCostFactoryTotal` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`id: String`；`title: String`；`categories: [String]`
  - 返回：`OrderCostFactoryTotal`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1046` `OrderCostFactoryTotal`

- **L3760 · 结构体** `ServerProcessingOptionsSheet` — 定义与Server 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3763 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:2710` `AppModel.processSelectedServerFolder`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L3802 · 结构体** `AimesReviewSheet` — 定义与AIMES 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3806 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:2341` `AppModel.ignoreSelectedAimesFactories`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L3852 · 计算属性** `@ViewBuilder private var formatWarningSection: some View` — 格式化与 `formatWarningSection` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4002` `AimesReviewSheet.aimesIdentity`；`macos/TravelerAssistant.swift:2392` `AppModel.assignAimesFactoryToOrder`

- **L3902 · 计算属性** `@ViewBuilder private var pendingSection: some View` — 根据当前状态计算并返回`pendingSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2332` `AppModel.toggleAimesReviewSelection`；`macos/OrderDashboardView.swift:4002` `AimesReviewSheet.aimesIdentity`；`macos/TravelerAssistant.swift:2387` `AppModel.assignAimesFactoryToSuggestedOrder`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L3956 · 计算属性** `@ViewBuilder private var assignedSection: some View` — 根据当前状态计算并返回`assignedSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4002` `AimesReviewSheet.aimesIdentity`；`macos/TravelerAssistant.swift:2425` `AppModel.restoreAimesFactoryAssignment`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`

- **L3979 · 计算属性** `@ViewBuilder private var ignoredSection: some View` — 忽略与 `ignoredSection` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4002` `AimesReviewSheet.aimesIdentity`；`macos/TravelerAssistant.swift:2367` `AppModel.restoreAimesFactory`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`

- **L4002 · 方法** `private func aimesIdentity(_ item: AimesReviewItem, timestampLabel: String? = nil) -> some View` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`timestampLabel: String? = nil`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1263` `appDisplayTimestamp`

- **L4024 · 结构体** `CurrentIssuesSheet` — 定义 `CurrentIssuesSheet` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4028 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:4828` `AppModel.openDashboardLocation`；`macos/TravelerAssistant.swift:2238` `AppModel.autoResolveCurrentIssue`；`macos/TravelerAssistant.swift:2253` `AppModel.resolveCurrentIssue`；`macos/OrderDashboardView.swift:278` `currentIssueRequiresInventoryMapping`；`macos/TravelerAssistant.swift:2818` `AppModel.requestInventoryMapping`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openDashboardLocation`；是否真实写入仍取决于分支和参数。

- **L4120 · 结构体** `ServerChangesSheet` — 定义与Server 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4123 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:635` `serverFolderChangeGroups`；`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:2492` `AppModel.selectAllServerFolders`；`macos/TravelerAssistant.swift:2501` `AppModel.clearServerFolderSelection`；`macos/TravelerAssistant.swift:2481` `AppModel.toggleServerFolderSelection`；`macos/TravelerAssistant.swift:881` `serverChangeTypeName`；`macos/TravelerAssistant.swift:2748` `AppModel.markTemporaryFolderManual`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:2506` `AppModel.processPendingServerChanges`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L4236 · 方法** `private func changeIcon(_ type: String) -> String` — 封装 `changeIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4244 · 方法** `private func changeColor(_ type: String) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4253 · 结构体** `ServerWriteConfirmationSheet` — 定义与Server 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4254 · 计算属性** `@ObservedObject var model: AppModel @State private var mappingTarget: PendingInventoryMappingTarget? @State private var ignoreTarget: PendingInventoryMappingTarget? @State private var skippedHardwareOrderIDs: Set<String> = [] private var orders: [ServerWriteOrderPreview]` — 根据当前状态计算并返回`orders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`AppModel @State private var mappingTarget: PendingInventoryMappingTarget? @State private var ignoreTarget: PendingInventoryMappingTarget? @State private var skippedHardwareOrderIDs: Set<String> = [] private var orders: [ServerWriteOrderPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4259 · 计算属性** `private var activeHardwareRequirements: [ServerHardwareMappingRequirement]` — 根据当前状态计算并返回五金。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[ServerHardwareMappingRequirement]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4266 · 计算属性** `private var invalidOrderValidations: [ServerWriteOrderPreview]` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[ServerWriteOrderPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4270 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/OrderDashboardView.swift:4473` `ServerWriteConfirmationSheet.orderPreviewCard`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:2617` `AppModel.confirmServerMaterialPreview`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`；`macos/TravelerAssistant.swift:5986` `InventoryMappingSheet`；`macos/TravelerAssistant.swift:3742` `AppModel.saveServerHardwareMapping`；`macos/TravelerAssistant.swift:6165` `PendingInventoryIgnoreSheet`；`macos/TravelerAssistant.swift:3757` `AppModel.saveServerHardwareIgnoredMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveServerHardwareMapping`, `saveServerHardwareIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L4411 · 计算属性** `@ViewBuilder private var hardwareMappingSection: some View` — 根据当前状态计算并返回五金、映射。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6072` `PendingInventoryMappingTarget`

- **L4468 · 方法** `private func formatQuantity(_ value: Double) -> String` — 格式化数量相关数据或步骤。
  - 输入：`_ value: Double`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1230` `Double.rounded`

- **L4473 · 方法** `private func orderPreviewCard(_ order: ServerWriteOrderPreview) -> some View` — 封装订单、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ order: ServerWriteOrderPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/OrderDashboardView.swift:4611` `ServerWriteConfirmationSheet.cutToSizeHardwareChoice`；`macos/OrderDashboardView.swift:310` `sortedServerWriteMaterialChanges`；`macos/OrderDashboardView.swift:4671` `ServerWriteConfirmationSheet.materialChangeRow`；`macos/OrderDashboardView.swift:4468` `ServerWriteConfirmationSheet.formatQuantity`；`macos/OrderDashboardView.swift:4713` `ServerWriteConfirmationSheet.hardwareChangeHeaderRow`；`macos/OrderDashboardView.swift:4689` `ServerWriteConfirmationSheet.hardwareChangeRow`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sortedServerWriteMaterialChanges`；是否真实写入仍取决于分支和参数。

- **L4611 · 方法** `private func cutToSizeHardwareChoice(for order: ServerWriteOrderPreview) -> some View` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`for order: ServerWriteOrderPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L4671 · 方法** `private func materialChangeRow(_ material: ServerWriteMaterialChange) -> some View` — 封装材料、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ServerWriteMaterialChange`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4468` `ServerWriteConfirmationSheet.formatQuantity`

- **L4689 · 方法** `private func hardwareChangeRow(_ hardware: ServerWriteHardwareChange) -> some View` — 封装五金、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ hardware: ServerWriteHardwareChange`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4760` `serverHardwareUnitText`；`macos/OrderDashboardView.swift:4468` `ServerWriteConfirmationSheet.formatQuantity`

- **L4713 · 方法** `private func hardwareChangeHeaderRow() -> some View` — 封装五金、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4726 · 方法** `private func materialPreviewRow(_ material: ServerWriteMaterialPreview) -> some View` — 封装材料、预览、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ServerWriteMaterialPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4468` `ServerWriteConfirmationSheet.formatQuantity`

- **L4760 · 函数** `func serverHardwareUnitText(_ unit: String) -> String` — 封装Server 数据、五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ unit: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4765 · 结构体** `ServerWriteSelectionRow` — 定义与Server 数据、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4771 · 结构体** `FactoryStockComparisonSheet` — 定义与工厂单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4775 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/OrderDashboardView.swift:4835` `FactoryStockComparisonSheet.stockRow`；`macos/TravelerAssistant.swift:4702` `AppModel.checkSelectedOrderStock`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L4821 · 计算属性** `private var stockHeader: some View` — 根据当前状态计算并返回`stockHeader` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4835 · 方法** `private func stockRow(_ row: OrderStockPreview) -> some View` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderStockPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `macos/TravelerAssistant.swift`

App 入口与 AppModel：全局状态、页面、子进程和业务编排。

- **L12 · 扩展** `Notification.Name` — 定义 `Notification.Name` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L18 · 函数** `func businessFriendlyMessage(_ raw: String, operation: String) -> String` — 封装 `businessFriendlyMessage` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ raw: String`；`operation: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L69 · 函数** `func inventoryMappingSourceFolderPath(_ path: String) -> String` — 封装库存、映射、来源、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ path: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L80 · 函数** `func dashboardFailureMessage(_ failureStatus: String, rawError: String, operation: String) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ failureStatus: String`；`rawError: String`；`operation: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L85 · 结构体** `OrderFolderItem` — 定义与订单、文件夹、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L91 · 结构体** `OrderDashboardFactory` — 定义与订单、看板、工厂单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L106 · 结构体** `ProductionMaterialDraft` — 定义与生产、材料相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L119 · 函数** `func productionMaterialTypeDisplayName(_ material: ProductionMaterialDraft) -> String` — 封装生产、材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L128 · 函数** `func productionMaterialName(_ material: ProductionMaterialDraft) -> String` — 封装生产、材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`；`macos/TravelerAssistant.swift:933` `orderMaterialDisplayName`；`macos/TravelerAssistant.swift:907` `OrderMaterialPreview`

- **L151 · 函数** `private func productionMaterialTypeRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L160 · 函数** `private func productionMaterialPlywoodRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`

- **L168 · 函数** `func sortedProductionMaterialDrafts(_ materials: [ProductionMaterialDraft]) -> [ProductionMaterialDraft]` — 排序生产、材料相关数据或步骤。
  - 输入：`_ materials: [ProductionMaterialDraft]`
  - 返回：`[ProductionMaterialDraft]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:151` `productionMaterialTypeRank`；`macos/TravelerAssistant.swift:160` `productionMaterialPlywoodRank`；`macos/TravelerAssistant.swift:1229` `Double`；`macos/TravelerAssistant.swift:128` `productionMaterialName`

- **L200 · 枚举** `ProductionOperationState` — 定义与生产、操作相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L206 · 结构体** `ProductionOperationResult` — 定义与生产、操作、结果相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L213 · 结构体** `OrderInstallationDay` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L218 · 初始化器** `init(date: String, installer: String)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`date: String`；`installer: String`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L225 · 结构体** `OrderDashboardItem` — 定义与订单、看板、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L251 · 函数** `func dashboardOrderRows(from object: [String: Any]) -> [[String: Any]]?` — 封装看板、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from object: [String: Any]`
  - 返回：`[[String: Any]]?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L255 · 结构体** `ServerChangePreview` — 定义与Server 数据、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L267 · 初始化器** `init( id: String, changeType: String, kind: String, orderId: String, sourceFolder: String, path: String, oldPath: String = "", message: String, manualOnly: Bool, eventTime: String )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`changeType: String`；`kind: String`；`orderId: String`；`sourceFolder: String`；`path: String`；`oldPath: String = ""`；`message: String`；`manualOnly: Bool`；`eventTime: String`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L292 · 结构体** `ServerWriteMaterialPreview` — 定义与Server 数据、材料、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L304 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L323 · 结构体** `ServerWriteHardwarePreview` — 定义与Server 数据、五金、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L331 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L344 · 结构体** `ServerWriteMaterialChange` — 定义与Server 数据、材料相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L356 · 初始化器** `init( id: String, changeType: String, materialType: String, color: String, thickness: String, edge: String, unit: String, oldQuantity: Double, newQuantity: Double, delta: Double )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`changeType: String`；`materialType: String`；`color: String`；`thickness: String`；`edge: String`；`unit: String`；`oldQuantity: Double`；`newQuantity: Double`；`delta: Double`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L380 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L395 · 方法** `static func aggregated(_ changes: [ServerWriteMaterialChange]) -> [ServerWriteMaterialChange]` — 封装 `aggregated` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerWriteMaterialChange]`
  - 返回：`[ServerWriteMaterialChange]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:344` `ServerWriteMaterialChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`；是否真实写入仍取决于分支和参数。

- **L424 · 结构体** `ServerWriteHardwareChange` — 定义与Server 数据、五金相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L436 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L453 · 结构体** `ServerHardwareMappingRequirement` — 定义与Server 数据、五金、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L463 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L477 · 结构体** `ServerWriteFactoryPreview` — 定义与Server 数据、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L491 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:323` `ServerWriteHardwarePreview`；`macos/TravelerAssistant.swift:424` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteHardwarePreview`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L513 · 结构体** `ServerWriteOrderPreview` — 定义与Server 数据、订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L526 · 初始化器** `init( id: String, orderID: String, orderType: String, sourceFolder: String, validationStatus: String, validationMessage: String, materials: [ServerWriteMaterialPreview], materialChanges: [ServerWriteMaterialChange], factories: [ServerWriteFactoryPreview], excludedFactories: [ServerWriteFactoryPreview], hardwareChanges: [ServerWriteHardwareChange] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`orderID: String`；`orderType: String`；`sourceFolder: String`；`validationStatus: String`；`validationMessage: String`；`materials: [ServerWriteMaterialPreview]`；`materialChanges: [ServerWriteMaterialChange]`；`factories: [ServerWriteFactoryPreview]`；`excludedFactories: [ServerWriteFactoryPreview]`；`hardwareChanges: [ServerWriteHardwareChange]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L552 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:292` `ServerWriteMaterialPreview`；`macos/TravelerAssistant.swift:395` `ServerWriteMaterialChange.aggregated`；`macos/TravelerAssistant.swift:344` `ServerWriteMaterialChange`；`macos/TravelerAssistant.swift:424` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`, `ServerWriteMaterialChange`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L577 · 结构体** `ServerWritePreview` — 定义与Server 数据、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L584 · 初始化器** `init(payload: [String: Any], sourceFolders: [String], materials: [ServerWriteMaterialPreview], orders: [ServerWriteOrderPreview], hardwareMappingRequirements: [ServerHardwareMappingRequirement] = [])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`payload: [String: Any]`；`sourceFolders: [String]`；`materials: [ServerWriteMaterialPreview]`；`orders: [ServerWriteOrderPreview]`；`hardwareMappingRequirements: [ServerHardwareMappingRequirement] = []`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L592 · 初始化器** `init?(object: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`object: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:292` `ServerWriteMaterialPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`；是否真实写入仍取决于分支和参数。

- **L609 · 结构体** `ServerFolderChangeGroup` — 定义与Server 数据、文件夹相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L617 · 计算属性** `var requiresManualReview: Bool` — 根据当前状态计算并返回`requiresManualReview` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L622 · 结构体** `PendingCenterItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L635 · 函数** `func serverFolderChangeGroups(_ changes: [ServerChangePreview]) -> [ServerFolderChangeGroup]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`
  - 返回：`[ServerFolderChangeGroup]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:609` `ServerFolderChangeGroup`

- **L654 · 函数** `func buildPendingCenterItems( serverChanges: [ServerChangePreview], currentIssues: [CurrentIssue], aimesReviews: [AimesReviewItem] ) -> [PendingCenterItem]` — 构建与 `buildPendingCenterItems` 对应的数据或步骤。
  - 输入：`serverChanges: [ServerChangePreview]`；`currentIssues: [CurrentIssue]`；`aimesReviews: [AimesReviewItem]`
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:635` `serverFolderChangeGroups`；`macos/TravelerAssistant.swift:664` `belongs`；`macos/TravelerAssistant.swift:622` `PendingCenterItem`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `Set`；是否真实写入仍取决于分支和参数。

- **L664 · 函数** `func belongs(_ issue: CurrentIssue, to group: ServerFolderChangeGroup) -> Bool` — 封装 `belongs` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`；`to group: ServerFolderChangeGroup`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L741 · 结构体** `CurrentIssue` — 定义与待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L752 · 结构体** `AimesReviewItem` — 定义与AIMES 数据、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L764 · 函数** `func aimesReviewItems(_ object: [String: Any], key: String) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`key: String`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:752` `AimesReviewItem`

- **L781 · 函数** `func aimesReviewItemsFromWarnings(_ warnings: [[String: Any]]) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ warnings: [[String: Any]]`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:752` `AimesReviewItem`

- **L800 · 函数** `func dashboardActivitySteps(_ object: [String: Any], includeChanges: Bool = true) -> [InventoryStep]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1145` `InventoryStep`

- **L844 · 函数** `func serverChangePreviews(_ rows: [[String: Any]]) -> [ServerChangePreview]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [[String: Any]]`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:255` `ServerChangePreview`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L865 · 函数** `func serverChangesExcludingFolder( _ changes: [ServerChangePreview], folderPath: String ) -> [ServerChangePreview]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`；`folderPath: String`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L881 · 函数** `func serverChangeTypeName(_ type: String) -> String` — 封装Server 数据、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L891 · 结构体** `OrderPreviewIssue` — 定义与订单、预览、待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L897 · 函数** `func orderPreviewIssues(_ object: [String: Any]) -> [OrderPreviewIssue]` — 封装订单、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`[OrderPreviewIssue]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:891` `OrderPreviewIssue`

- **L907 · 结构体** `OrderMaterialPreview` — 定义与订单、材料、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L916 · 初始化器** `init( kind: String, thickness: Double, color: String, quantity: Double, productCode: String = "", brand: String = "" )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`kind: String`；`thickness: Double`；`color: String`；`quantity: Double`；`productCode: String = ""`；`brand: String = ""`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L933 · 函数** `func orderMaterialDisplayName(_ row: OrderMaterialPreview) -> String` — 封装订单、材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderMaterialPreview`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L944 · 函数** `func orderedMaterialRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`[OrderMaterialPreview]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:539` `orderDetailPanelThicknessRank`

- **L975 · 函数** `func orderedEdgeColors(_ colors: [String], matching panels: [OrderMaterialPreview]) -> [String]` — 封装 `orderedEdgeColors` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ colors: [String]`；`matching panels: [OrderMaterialPreview]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L988 · 函数** `func panelColorsNeedingThicknessWarning(_ rows: [OrderMaterialPreview]) -> Set<String>` — 封装 `panelColorsNeedingThicknessWarning` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`Set<String>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L1000 · 结构体** `OrderFactoryPreview` — 定义与订单、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1006 · 结构体** `OrderFittingPreview` — 定义与订单、五金、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1019 · 结构体** `OrderStockPreview` — 定义与订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1031 · 结构体** `OrderCostLine` — 定义与订单、成本相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1046 · 结构体** `OrderCostFactoryTotal` — 定义与订单、成本、工厂单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1053 · 结构体** `InventoryTraveler` — 定义与库存、Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1063 · 函数** `func groupInventoryTravelersByNewest(_ travelers: [InventoryTraveler]) -> [(String, [InventoryTraveler])]` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ travelers: [InventoryTraveler]`
  - 返回：`[(String, [InventoryTraveler])]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1080 · 结构体** `InventoryPreviewRow` — 定义与库存、预览、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1091 · 函数** `func inventoryPreviewCategoryRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1100 · 函数** `func inventoryPreviewPlywoodRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1108 · 函数** `func sortedInventoryPreviewRows(_ rows: [InventoryPreviewRow]) -> [InventoryPreviewRow]` — 排序库存、预览相关数据或步骤。
  - 输入：`_ rows: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1091` `inventoryPreviewCategoryRank`；`macos/TravelerAssistant.swift:1100` `inventoryPreviewPlywoodRank`

- **L1124 · 结构体** `InventoryProductCandidate` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1133 · 结构体** `InventoryIgnoredMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1139 · 结构体** `InventoryManualMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1145 · 结构体** `InventoryStep` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1157 · 初始化器** `init( id: UUID = UUID(), time: String, title: String, detail: String, state: String, paths: [String] = [], operationDetails: [String] = [], contextDetails: [String] = [], startedAt: Date? = nil, duration: TimeInterval? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`time: String`；`title: String`；`detail: String`；`state: String`；`paths: [String] = []`；`operationDetails: [String] = []`；`contextDetails: [String] = []`；`startedAt: Date? = nil`；`duration: TimeInterval? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1182 · 函数** `func operationDurationText(_ duration: TimeInterval) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ duration: TimeInterval`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1230` `Double.rounded`

- **L1187 · 函数** `func inventoryFailureNeedsVerification(_ message: String) -> Bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1202 · 结构体** `DashboardOperationDuration` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1207 · 初始化器** `init(id: String? = nil, label: String, duration: TimeInterval)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String? = nil`；`label: String`；`duration: TimeInterval`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1214 · 函数** `func dashboardFlatOperationDurations(_ stages: [[String: Any]]) -> [DashboardOperationDuration]` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stages: [[String: Any]]`
  - 返回：`[DashboardOperationDuration]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1202` `DashboardOperationDuration`

- **L1224 · 结构体** `DashboardOperationStart` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1229 · 扩展** `Double` — 定义 `Double` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1230 · 方法** `func rounded(toPlaces places: Int) -> Double` — 封装 `rounded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`toPlaces places: Int`
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`

- **L1236 · 函数** `func dashboardClockTime(_ date: Date = Date()) -> String` — 封装看板、时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date = Date()`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1240 · 函数** `func dashboardInventoryProgressText(_ message: String) -> String` — 封装看板、库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1263 · 函数** `func appDisplayTimestamp(_ value: String) -> String` — 封装 `appDisplayTimestamp` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1267 · 函数** `func dashboardBusinessDate(_ value: String) -> Date?` — 封装看板、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`Date?`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:288` `ISO8601DateFormatter`

- **L1285 · 函数** `func dashboardTimestamp(_ value: String, isInSameMonthAs reference: Date, calendar: Calendar = .current) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`；`isInSameMonthAs reference: Date`；`calendar: Calendar = .current`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1267` `dashboardBusinessDate`

- **L1290 · 函数** `func updatingLatestRunningStep(_ steps: [InventoryStep], detail: String) -> [InventoryStep]?` — 封装 `updatingLatestRunningStep` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`detail: String`
  - 返回：`[InventoryStep]?`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1145` `InventoryStep`

- **L1309 · 函数** `func appendingInventoryProgressStep(_ steps: [InventoryStep], message: String) -> [InventoryStep]` — 封装库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`message: String`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1145` `InventoryStep`

- **L1338 · 函数** `func orderUpdateActionReady(existingTravelerPath: String, selectedOrderPath: String, selectedOrderId: String) -> Bool` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`；`selectedOrderPath: String`；`selectedOrderId: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1342 · 函数** `func orderTravelerOpenActionReady(existingTravelerPath: String) -> Bool` — 封装订单、Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1347 · 结构体** `TodoItem` — 定义与待办、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1354 · 初始化器** `init( id: UUID = UUID(), content: String, startedAt: Date = Date(), deadline: Date?, completedAt: Date? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`content: String`；`startedAt: Date = Date()`；`deadline: Date?`；`completedAt: Date? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1369 · 结构体** `AssistantTaskItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1375 · 类** `AppModel` — 定义 `AppModel` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1523 · 计算属性** `var pendingCenterItems: [PendingCenterItem]` — 根据当前状态计算并返回`pendingCenterItems` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:654` `buildPendingCenterItems`

- **L1531 · 计算属性** `var orderPreviewReady: Bool` — 根据当前状态计算并返回订单、预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1535 · 计算属性** `var orderCanGenerateTraveler: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1539 · 计算属性** `var orderTravelerOpenReady: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1342` `orderTravelerOpenActionReady`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L1543 · 计算属性** `var activeOwnedSourceRoot: String` — 根据当前状态计算并返回来源。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1547 · 计算属性** `var activeCutToSizeRoot: String` — 根据当前状态计算并返回`activeCutToSizeRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1553 · 计算属性** `var activeOrderRoot: String` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1557 · 计算属性** `var activeBackupRoot: String` — 根据当前状态计算并返回备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1561 · 计算属性** `var databaseBackupRoot: String` — 根据当前状态计算并返回数据库、备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1565 · 初始化器** `init()` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1695` `AppModel.loadSettings`；`macos/OperationLog.swift:186` `OperationLogWriter.setEnabled`；`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:1614` `AppModel.loadTodoItems`；`macos/AssistantView.swift:479` `AppModel.loadAssistantUsage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setEnabled`, `record`；是否真实写入仍取决于分支和参数。

- **L1577 · 方法** `func checkBackupReminder()` — 检查备份相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L1586 · 方法** `func performBackup()` — 执行手动/计划备份并把结果映射为 App 状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L1604 · 计算属性** `private var settingsURL: URL` — 设置设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1609 · 计算属性** `var todoDataURL: URL` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1614 · 方法** `func loadTodoItems()` — 读取待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L1629 · 方法** `func addTodo(content: String, deadline: Date?)` — 新增待办相关数据或步骤。
  - 输入：`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1347` `TodoItem`；`macos/TravelerAssistant.swift:1665` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1640 · 方法** `func updateTodo(_ item: TodoItem, content: String, deadline: Date?)` — 更新待办相关数据或步骤。
  - 输入：`_ item: TodoItem`；`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1665` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1652 · 方法** `func toggleTodoCompletion(_ item: TodoItem)` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1665` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1659 · 方法** `func deleteTodo(_ item: TodoItem)` — 删除待办相关数据或步骤。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1665` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1665 · 方法** `private func saveTodoItems()` — 保存待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L1695 · 方法** `func loadSettings() -> Bool` — 读取设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1714 · 方法** `func saveSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L1743 · 计算属性** `var operationLogURL: URL` — 根据当前状态计算并返回操作、日志。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1748 · 方法** `func setOperationLogEnabled(_ enabled: Bool)` — 设置操作、日志相关数据或步骤。
  - 输入：`_ enabled: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/OperationLog.swift:186` `OperationLogWriter.setEnabled`；`macos/TravelerAssistant.swift:1714` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`, `setEnabled`, `saveSettings`；是否真实写入仍取决于分支和参数。

- **L1770 · 方法** `func refreshOperationLogInfo()` — 刷新操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:78` `OperationLogReader.fileSizeText`

- **L1774 · 方法** `func trimOperationLog()` — 封装操作、日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:247` `OperationLogWriter.trimLogToRecentDays`；`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:1770` `AppModel.refreshOperationLogInfo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1797 · 方法** `func logUserAction(_ action: String, details: [String: Any] = [:])` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ action: String`；`details: [String: Any] = [:]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1801 · 方法** `func newOperationID(_ name: String, details: [String: Any] = [:]) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`details: [String: Any] = [:]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1812 · 方法** `private func finishOperationLog( _ operationID: String, name: String, startedAt: Date, exitStatus: Int32 )` — 结束并收口操作、日志相关数据或步骤。
  - 输入：`_ operationID: String`；`name: String`；`startedAt: Date`；`exitStatus: Int32`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1830 · 方法** `func environmentForOperation(_ operationID: String) -> [String: String]` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ operationID: String`
  - 返回：`[String: String]`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:257` `OperationLogWriter.environment`

- **L1838 · 方法** `func saveAllSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1714` `AppModel.saveSettings`；`macos/TravelerAssistant.swift:1862` `AppModel.saveJdyPassword`；`macos/TravelerAssistant.swift:1913` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `saveJdyPassword`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L1862 · 方法** `func saveJdyPassword()` — 保存与 `saveJdyPassword` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `SecItemDelete`, `SecItemUpdate`, `SecItemCopyMatching`；是否真实写入仍取决于分支和参数。

- **L1913 · 方法** `func saveAimesPassword()` — 保存AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1714` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `SecItemDelete`；是否真实写入仍取决于分支和参数。

- **L1934 · 方法** `private func applyDashboardObject(_ object: [String: Any], includeChanges: Bool = true)` — 应用看板相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2043` `AppModel.applyDashboardOperationTrace`；`macos/TravelerAssistant.swift:2026` `AppModel.applyCurrentIssues`；`macos/TravelerAssistant.swift:251` `dashboardOrderRows`；`macos/TravelerAssistant.swift:91` `OrderDashboardFactory`；`macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`macos/TravelerAssistant.swift:225` `OrderDashboardItem`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:800` `dashboardActivitySteps`

- **L2010 · 方法** `private func presentServerWritePreview(_ object: [String: Any])` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:577` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2026 · 方法** `private func applyCurrentIssues(from object: [String: Any])` — 应用与 `applyCurrentIssues` 对应的数据或步骤。
  - 输入：`from object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:741` `CurrentIssue`

- **L2043 · 方法** `private func applyDashboardOperationTrace(_ object: [String: Any])` — 应用看板、操作相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2055 · 方法** `private func applyAimesReviewObject(_ object: [String: Any], presentIfNeeded: Bool = true)` — 应用AIMES 数据相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:764` `aimesReviewItems`；`macos/TravelerAssistant.swift:781` `aimesReviewItemsFromWarnings`；`macos/OrderDashboardView.swift:793` `shouldPresentPendingCenterAfterAimes`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L2073 · 方法** `private func closePendingCenterIfEmpty()` — 关闭与 `closePendingCenterIfEmpty` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2079 · 方法** `private func beginDashboardOperation(_ source: String, label: String, continuing: Bool = false)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`；`label: String`；`continuing: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1224` `DashboardOperationStart`

- **L2091 · 方法** `private func finishDashboardOperation(_ source: String)` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1202` `DashboardOperationDuration`

- **L2104 · 方法** `private func finishDashboardOperation( _ source: String, backendSeconds: Double, stages: [[String: Any]] )` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`backendSeconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1214` `dashboardFlatOperationDurations`；`macos/TravelerAssistant.swift:1202` `DashboardOperationDuration`

- **L2130 · 方法** `private func finishDashboardOperation(_ source: String, using object: [String: Any])` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`using object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2143 · 方法** `private func discardDashboardOperationTimer(_ source: String)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2147 · 方法** `private func applyAuthoritativeDashboardTiming( _ source: String, seconds: Double, stages: [[String: Any]] )` — 应用看板相关数据或步骤。
  - 输入：`_ source: String`；`seconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1214` `dashboardFlatOperationDurations`

- **L2158 · 方法** `func startOrderDashboard()` — 启动订单中心初始化链路，加载缓存并安排 AIMES/Server 刷新。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2164` `AppModel.loadOrderDashboardCache`

- **L2164 · 方法** `func loadOrderDashboardCache()` — 读取订单、看板、缓存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2055` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:2271` `AppModel.syncDashboardAimes`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2186 · 方法** `func refreshDashboardOrdersAfterOutbound()` — 刷新看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2205 · 方法** `private func startPendingDashboardOutboundRefreshIfNeeded()` — 启动看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2186` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L2213 · 方法** `private func runDailyBackupAfterLocalCache(completion: @escaping () -> Void)` — 执行备份、缓存相关数据或步骤。
  - 输入：`completion: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2238 · 方法** `func autoResolveCurrentIssue(_ issue: CurrentIssue)` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2073` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2253 · 方法** `func resolveCurrentIssue(_ issue: CurrentIssue, orderID: String)` — 解析并确定待处理问题相关数据或步骤。
  - 输入：`_ issue: CurrentIssue`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2073` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2271 · 方法** `func syncDashboardAimes(force: Bool, scanServerAfter: Bool = false)` — 从 App 发起 AIMES 同步，解析结果并衔接后续看板刷新。
  - 输入：`force: Bool`；`scanServerAfter: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2445` `AppModel.scanDashboardServer`；`macos/TravelerAssistant.swift:2143` `AppModel.discardDashboardOperationTimer`；`macos/TravelerAssistant.swift:2147` `AppModel.applyAuthoritativeDashboardTiming`；`macos/TravelerAssistant.swift:2055` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2332 · 方法** `func toggleAimesReviewSelection(_ item: AimesReviewItem)` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L2341 · 方法** `func ignoreSelectedAimesFactories()` — 忽略AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2055` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:2073` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2367 · 方法** `func restoreAimesFactory(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2055` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2387 · 方法** `func assignAimesFactoryToSuggestedOrder(_ item: AimesReviewItem)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2392` `AppModel.assignAimesFactoryToOrder`

- **L2392 · 方法** `func assignAimesFactoryToOrder(_ item: AimesReviewItem, orderID: String)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2055` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:2073` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2425 · 方法** `func restoreAimesFactoryAssignment(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2055` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2445 · 方法** `func scanDashboardServer(background: Bool = false, presentIfNeeded: Bool = true)` — 从 App 发起 Server 扫描并把变化、问题和耗时写入看板状态。
  - 输入：`background: Bool = false`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2026` `AppModel.applyCurrentIssues`；`macos/TravelerAssistant.swift:2043` `AppModel.applyDashboardOperationTrace`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:844` `serverChangePreviews`；`macos/TravelerAssistant.swift:2073` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2481 · 方法** `func toggleServerFolderSelection(_ folderPath: String)` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folderPath: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:635` `serverFolderChangeGroups`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L2492 · 方法** `func selectAllServerFolders()` — 选择Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:635` `serverFolderChangeGroups`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L2501 · 方法** `func clearServerFolderSelection()` — 清理Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`

- **L2506 · 方法** `func processPendingServerChanges()` — 按当前选择为 Server 变化生成业务预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:635` `serverFolderChangeGroups`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2010` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2538 · 方法** `func confirmServerWrite(orderID: String, factoryOrder: String)` — 确认并执行 Server 事实写入，然后只做所需的本地看板刷新。
  - 输入：`orderID: String`；`factoryOrder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:513` `ServerWriteOrderPreview`；`macos/TravelerAssistant.swift:577` `ServerWritePreview`；`macos/TravelerAssistant.swift:2685` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `ServerWriteOrderPreview`, `ServerWritePreview`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L2617 · 方法** `func confirmServerMaterialPreview(skipHardwareOrderIDs: Set<String> = [])` — 封装Server 数据、材料、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`skipHardwareOrderIDs: Set<String> = []`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1145` `InventoryStep`；`macos/TravelerAssistant.swift:1236` `dashboardClockTime`；`macos/TravelerAssistant.swift:2685` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L2685 · 方法** `func refreshDashboardAfterServerWrite()` — 刷新看板、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2699 · 方法** `private func applyServerIndexResult(_ object: [String: Any])` — 应用Server 数据、结果相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2055` `AppModel.applyAimesReviewObject`

- **L2704 · 方法** `func prepareSelectedServerFolder(_ folderURL: URL)` — 准备并校验Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2710 · 方法** `func processSelectedServerFolder(_ folderURL: URL, includeHardware: Bool)` — 处理Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`；`includeHardware: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:1145` `InventoryStep`；`macos/TravelerAssistant.swift:1236` `dashboardClockTime`；`macos/TravelerAssistant.swift:2010` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2748 · 方法** `func markTemporaryFolderManual(_ folderPath: String)` — 标记文件夹相关数据或步骤。
  - 输入：`_ folderPath: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2026` `AppModel.applyCurrentIssues`；`macos/TravelerAssistant.swift:865` `serverChangesExcludingFolder`；`macos/TravelerAssistant.swift:2073` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2775 · 方法** `func loadInventory()` — 加载可处理的库存/Traveler 列表及目录状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1053` `InventoryTraveler`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:2885` `AppModel.activatePendingInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `Set`；是否真实写入仍取决于分支和参数。

- **L2818 · 方法** `func requestInventoryMapping(folderPath: String, message: String = "")` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folderPath: String`；`message: String = ""`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:69` `inventoryMappingSourceFolderPath`；`macos/TravelerAssistant.swift:2840` `AppModel.inventoryMappingNames`

- **L2833 · 方法** `func closeInventoryMappingWorkspace()` — 关闭库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2840 · 方法** `private func inventoryMappingNames(from message: String) -> [String]` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from message: String`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2850 · 方法** `private func rereadPendingSourceFolder()` — 封装来源、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2869` `AppModel.refreshDashboardOrdersAfterInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2869 · 方法** `private func refreshDashboardOrdersAfterInventoryMapping()` — 刷新看板、库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2073` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2885 · 方法** `func activatePendingInventoryMapping()` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3065` `AppModel.previewSelectedInventory`

- **L2925 · 方法** `func openInventoryChrome()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L2938 · 方法** `func updateInventoryCatalog()` — 更新库存、商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4932` `inventoryCatalogUpdateFailureStatus`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `inventoryCatalogUpdateFailureStatus`, `inventoryCatalogUpdateSuccessStatus`；是否真实写入仍取决于分支和参数。

- **L2966 · 方法** `func closeInventoryChromeOnQuit()` — 关闭库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`, `record`；是否真实写入仍取决于分支和参数。

- **L2996 · 方法** `func refreshInventoryCatalogStatus()` — 刷新库存、商品目录、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3006 · 方法** `func refreshInventoryFolder(_ folder: String)` — 刷新库存、文件夹相关数据或步骤。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:3038` `AppModel.reloadInventoryFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3038 · 方法** `private func reloadInventoryFolder(_ folder: String)` — 封装库存、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1053` `InventoryTraveler`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3065 · 方法** `func previewSelectedInventory()` — 为当前选中对象串行生成库存需求和可用量预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3098` `AppModel.previewOrderInventory`；`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3874` `AppModel.previewNext`

- **L3098 · 方法** `func previewOrderInventory( orderID: String, factoryOrderNames: [String], factoryOrders: [String] = [], productionBatchNumber: String = "", shipmentOnly: Bool = false )` — 预览预览、订单、库存相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrderNames: [String]`；`factoryOrders: [String] = []`；`productionBatchNumber: String = ""`；`shipmentOnly: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3862` `AppModel.applyInventoryPreviewObject`；`macos/TravelerAssistant.swift:4074` `AppModel.finishInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`；是否真实写入仍取决于分支和参数。

- **L3139 · 方法** `func loadProductionPreview(orderID: String, factoryOrders: [String], completion: @escaping (Bool) -> Void = { _ in })` — 读取当前选择的生产材料预览并填充编辑草稿。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:106` `ProductionMaterialDraft`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3177 · 方法** `func prepareProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], onResult completion: @escaping (String?, String?) -> Void )` — 从 App 提交生产准备参数并处理后端返回。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`onResult completion: @escaping (String?, String?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3194 · 方法** `func startDirectProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], batchNumber: String, completion: @escaping (ProductionOperationResult) -> Void = { _ in } )` — 执行用户确认后的生产完成流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`batchNumber: String`；`completion: @escaping (ProductionOperationResult) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`；`macos/TravelerAssistant.swift:206` `ProductionOperationResult`；`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:1145` `InventoryStep`；`macos/TravelerAssistant.swift:1236` `dashboardClockTime`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1187` `inventoryFailureNeedsVerification`；`macos/TravelerAssistant.swift:2186` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L3312 · 方法** `func startDirectOrderShipment(orderID: String, factoryOrders: [String])` — 执行用户确认后的订单出库流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2079` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:1145` `InventoryStep`；`macos/TravelerAssistant.swift:1236` `dashboardClockTime`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:2186` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L3392 · 方法** `func loadOutboundScope( orderID: String, factoryOrders: [String], completion: @escaping ([String: Any]?) -> Void )` — 读取出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping ([String: Any]?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3414 · 方法** `func saveOutboundScope( orderID: String, scopeType: String, requirement: String, factoryOrder: String = "", reason: String, completion: @escaping (Bool) -> Void = { _ in } )` — 保存出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`scopeType: String`；`requirement: String`；`factoryOrder: String = ""`；`reason: String`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3443 · 方法** `func openAndFillSelectedInventory()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:3535` `AppModel.markInventoryTravelerSaved`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3535 · 方法** `private func markInventoryTravelerSaved(path: String, documentNumber: String)` — 标记库存、Traveler相关数据或步骤。
  - 输入：`path: String`；`documentNumber: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1053` `InventoryTraveler`

- **L3550 · 方法** `func setInventoryItemsIgnored(_ names: [String], ignored: Bool)` — 设置库存相关数据或步骤。
  - 输入：`_ names: [String]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3065` `AppModel.previewSelectedInventory`；`macos/TravelerAssistant.swift:2850` `AppModel.rereadPendingSourceFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`；是否真实写入仍取决于分支和参数。

- **L3576 · 方法** `func refreshInventoryMappings()` — 刷新库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1139` `InventoryManualMapping`；`macos/TravelerAssistant.swift:1133` `InventoryIgnoredMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3597 · 方法** `func saveSettingsManualMapping(name: String, productCode: String)` — 保存设置、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3611 · 方法** `func updateSettingsManualMapping(oldName: String, name: String, productCode: String)` — 更新设置、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3629 · 方法** `func removeSettingsManualMapping(name: String)` — 移除设置、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3639 · 方法** `func saveInventoryIgnoredMapping(name: String, reason: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:2850` `AppModel.rereadPendingSourceFolder`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3664 · 方法** `func updateInventoryIgnoredMapping(oldName: String, name: String, reason: String)` — 更新库存、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3686 · 方法** `func removeInventoryIgnoredMapping(name: String)` — 移除库存、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3696 · 方法** `func searchInventoryProducts(_ query: String)` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ query: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1124` `InventoryProductCandidate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3723 · 方法** `func saveInventoryMapping(travelerName: String, productCode: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`travelerName: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:3065` `AppModel.previewSelectedInventory`；`macos/TravelerAssistant.swift:2850` `AppModel.rereadPendingSourceFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3742 · 方法** `func saveServerHardwareMapping(name: String, productCode: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3772` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3757 · 方法** `func saveServerHardwareIgnoredMapping(name: String, reason: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4044` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3772` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3772 · 方法** `private func removeServerHardwareMappingRequirement(_ name: String)` — 移除Server 数据、五金、映射相关数据或步骤。
  - 输入：`_ name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:577` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3787 · 方法** `private func consumeInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] ) -> [InventoryPreviewRow]` — 消费并转换库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1080` `InventoryPreviewRow`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`

- **L3862 · 方法** `private func applyInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] )` — 应用库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1108` `sortedInventoryPreviewRows`；`macos/TravelerAssistant.swift:3787` `AppModel.consumeInventoryPreviewObject`

- **L3874 · 方法** `private func previewNext( _ paths: [String], index: Int, selectedDocumentRemarks: Set<String> = [], accumulated: [InventoryPreviewRow] )` — 预览预览相关数据或步骤。
  - 输入：`_ paths: [String]`；`index: Int`；`selectedDocumentRemarks: Set<String> = []`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1108` `sortedInventoryPreviewRows`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3912` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3787` `AppModel.consumeInventoryPreviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3912 · 方法** `private func runInventory( _ arguments: [String], manageRunning: Bool = true, onFailure: ((String) -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动库存 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`manageRunning: Bool = true`；`onFailure: ((String) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:859` `dashboardStatusIsInProgress`；`macos/TravelerAssistant.swift:1801` `AppModel.newOperationID`；`macos/TravelerAssistant.swift:1830` `AppModel.environmentForOperation`；`macos/TravelerAssistant.swift:4093` `AppModel.consumeInventoryLogChunk`；`macos/TravelerAssistant.swift:1812` `AppModel.finishOperationLog`；`macos/TravelerAssistant.swift:4060` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L4044 · 方法** `private func beginInventoryOperation(_ title: String)` — 封装库存、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`

- **L4049 · 方法** `private func addInventoryStep(_ title: String, _ detail: String, _ state: String)` — 新增库存相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1145` `InventoryStep`；`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4060 · 方法** `private func finishRunningInventoryStep(_ detail: String, _ state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:4049` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:1145` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4074 · 方法** `private func finishInventoryStep(named title: String, detail: String, state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`named title: String`；`detail: String`；`state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1145` `InventoryStep`

- **L4093 · 方法** `private func consumeInventoryLogChunk(_ chunk: String)` — 消费并转换库存、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1309` `appendingInventoryProgressStep`；`macos/TravelerAssistant.swift:1240` `dashboardInventoryProgressText`

- **L4114 · 方法** `private func addOrderStep(_ title: String, _ detail: String, _ state: String)` — 新增订单相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1145` `InventoryStep`；`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4133 · 方法** `private func finishOrderStep(_ detail: String, _ state: String)` — 结束并收口订单相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:1145` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4160 · 方法** `private func consumeOrderLogChunk(_ chunk: String)` — 消费并转换订单、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1290` `updatingLatestRunningStep`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`

- **L4180 · 方法** `private func runOrder( _ arguments: [String], input: Data? = nil, failureStatus: String = "校验未通过", onFailure: (() -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动订单 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`input: Data? = nil`；`failureStatus: String = "校验未通过"`；`onFailure: (() -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1801` `AppModel.newOperationID`；`macos/TravelerAssistant.swift:1830` `AppModel.environmentForOperation`；`macos/TravelerAssistant.swift:4160` `AppModel.consumeOrderLogChunk`；`macos/TravelerAssistant.swift:1812` `AppModel.finishOperationLog`；`macos/TravelerAssistant.swift:2205` `AppModel.startPendingDashboardOutboundRefreshIfNeeded`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`, `write`, `closeFile`, `startPendingDashboardOutboundRefreshIfNeeded`；是否真实写入仍取决于分支和参数。

- **L4289 · 方法** `func loadOrderFolders()` — 读取订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:85` `OrderFolderItem`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4327 · 方法** `func previewOrderFolder(_ item: OrderFolderItem, recordSelection: Bool = true)` — 预览预览、订单、文件夹相关数据或步骤。
  - 输入：`_ item: OrderFolderItem`；`recordSelection: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4403` `AppModel.findLocalOrderTraveler`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:897` `orderPreviewIssues`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:4437` `AppModel.applyOrderPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4403 · 方法** `private func findLocalOrderTraveler(_ orderId: String) -> String` — 查找订单、Traveler相关数据或步骤。
  - 输入：`_ orderId: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4437 · 方法** `private func applyOrderPreview(_ object: [String: Any], targetOrderID: String? = nil)` — 应用订单、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`targetOrderID: String? = nil`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:907` `OrderMaterialPreview`；`macos/TravelerAssistant.swift:1000` `OrderFactoryPreview`；`macos/TravelerAssistant.swift:1006` `OrderFittingPreview`

- **L4491 · 方法** `func loadOrderDetailFromDatabase(_ item: OrderDashboardItem)` — 读取订单、数据库相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:704` `orderDashboardIsCompleted`；`macos/TravelerAssistant.swift:4560` `AppModel.schedulePendingOrderDetailRetry`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:1229` `Double`；`macos/TravelerAssistant.swift:4437` `AppModel.applyOrderPreview`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4560 · 方法** `private func schedulePendingOrderDetailRetry()` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4491` `AppModel.loadOrderDetailFromDatabase`

- **L4578 · 方法** `func saveOrderAnnotations( orderID: String, userNote: String, plannedDays: [OrderInstallationDay], actualDays: [OrderInstallationDay], onStatusChange: @escaping (String) -> Void = { _ in } )` — 保存安装日期、安装人等订单人工备注并刷新详情。
  - 输入：`orderID: String`；`userNote: String`；`plannedDays: [OrderInstallationDay]`；`actualDays: [OrderInstallationDay]`；`onStatusChange: @escaping (String) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1934` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4626 · 方法** `func setOrderFittingsIgnored(_ rows: [OrderFittingPreview], ignored: Bool)` — 设置订单相关数据或步骤。
  - 输入：`_ rows: [OrderFittingPreview]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:4327` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runOrder`；是否真实写入仍取决于分支和参数。

- **L4655 · 方法** `func generateSelectedOrder()` — 生成订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:4810` `AppModel.openSelectedOrderTraveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `openSelectedOrderTraveler`；是否真实写入仍取决于分支和参数。

- **L4679 · 方法** `func generateMissingMaterial()` — 生成材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:4327` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4702 · 方法** `func checkSelectedOrderStock()` — 检查订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:1019` `OrderStockPreview`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4744 · 方法** `func calculateSelectedOrderCost(export: Bool = false)` — 计算订单、成本相关数据或步骤。
  - 输入：`export: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4180` `AppModel.runOrder`；`macos/TravelerAssistant.swift:4774` `AppModel.applyOrderCost`；`macos/TravelerAssistant.swift:4133` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `open`；是否真实写入仍取决于分支和参数。

- **L4774 · 方法** `private func applyOrderCost(_ object: [String: Any])` — 应用订单、成本相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1031` `OrderCostLine`；`macos/TravelerAssistant.swift:1046` `OrderCostFactoryTotal`

- **L4810 · 方法** `func openSelectedOrderTraveler()` — 打开订单、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4114` `AppModel.addOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L4828 · 方法** `func openDashboardLocation(_ path: String)` — 打开看板相关数据或步骤。
  - 输入：`_ path: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L4841 · 计算属性** `var projectRoot: URL` — 根据当前状态计算并返回`projectRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4849 · 枚举** `AppLayout` — 定义 `AppLayout` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4900 · 函数** `func inventoryActionColumnCount(availableWidth: CGFloat) -> Int` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`availableWidth: CGFloat`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4905 · 枚举** `AppPalette` — 定义 `AppPalette` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4919 · 函数** `func inventoryCatalogUpdateSuccessStatus(_ count: Int) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4923 · 函数** `func inventoryCatalogUpdateSuccessStatus( _ count: Int, added: Int, updated: Int, removed: Int ) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`；`added: Int`；`updated: Int`；`removed: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4932 · 函数** `func inventoryCatalogUpdateFailureStatus(_ reason: String) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ reason: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4936 · 枚举** `SettingsStatusKind` — 定义与设置、状态相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4943 · 计算属性** `var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4953 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4964 · 函数** `func settingsStatusKind(_ status: String) -> SettingsStatusKind` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`SettingsStatusKind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4973 · 函数** `func settingsStatusDisplayText(_ status: String) -> String` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4979 · 结构体** `SettingsStatusBanner` — 定义与设置、状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4982 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4964` `settingsStatusKind`；`macos/TravelerAssistant.swift:4973` `settingsStatusDisplayText`

- **L5010 · 扩展** `View` — 定义 `View` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5011 · 方法** `func appPageFrame() -> some View` — 封装 `appPageFrame` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5039` `AppGlassGroupBoxStyle`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`

- **L5019 · 方法** `func appInputField(maxWidth: CGFloat? = nil) -> some View` — 封装 `appInputField` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`maxWidth: CGFloat? = nil`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5023 · 方法** `func appActionButton(minWidth: CGFloat = AppLayout.actionButtonWidth) -> some View` — 封装 `appActionButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.actionButtonWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5028 · 方法** `func inventoryActionButton(minWidth: CGFloat = AppLayout.inventoryActionMinWidth) -> some View` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.inventoryActionMinWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5039 · 结构体** `AppGlassGroupBoxStyle` — 定义 `AppGlassGroupBoxStyle` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5040 · 方法** `func makeBody(configuration: Configuration) -> some View` — 创建与 `makeBody` 对应的数据或步骤。
  - 输入：`configuration: Configuration`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5053 · 结构体** `AppSurfaceCard<Content` — 定义 `AppSurfaceCard<Content` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5057 · 初始化器** `init(padding: CGFloat = AppLayout.cardPadding, @ViewBuilder content: () -> Content)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`padding: CGFloat = AppLayout.cardPadding`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5062 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5072 · 结构体** `LiquidGlassPreviewBackdrop` — 定义与预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5073 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5107 · 结构体** `AppStatusBadge` — 定义与状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5108 · 枚举** `Kind` — 定义 `Kind` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5113 · 计算属性** `private var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5123 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5138 · 结构体** `WidthPreferenceKey` — 定义 `WidthPreferenceKey` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5141 · 方法** `static func reduce(value: inout CGFloat, nextValue: () -> CGFloat)` — 封装 `reduce` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: inout CGFloat`；`nextValue: () -> CGFloat`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5146 · 结构体** `ScrollingTextOnHover` — 定义 `ScrollingTextOnHover` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5157 · 计算属性** `private var overflow: CGFloat` — 根据当前状态计算并返回`overflow` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5161 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5196` `ScrollingTextOnHover.startScrolling`；`macos/TravelerAssistant.swift:5218` `ScrollingTextOnHover.stopScrolling`

- **L5196 · 方法** `private func startScrolling()` — 启动与 `startScrolling` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1229` `Double`

- **L5218 · 方法** `private func stopScrolling()` — 封装 `stopScrolling` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5225 · 结构体** `InventoryActionGrid<Content` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5229 · 初始化器** `init( minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5237 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5247 · 结构体** `AppPageHeader<Trailing` — 定义 `AppPageHeader<Trailing` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5253 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5258 · 结构体** `OperationLogCard` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5263 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5269 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5833` `SelectableOperationLogView`

- **L5279 · 结构体** `OrderWorkflowView` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5283 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:4289` `AppModel.loadOrderFolders`；`macos/TravelerAssistant.swift:4327` `AppModel.previewOrderFolder`；`macos/TravelerAssistant.swift:1263` `appDisplayTimestamp`；`macos/TravelerAssistant.swift:4702` `AppModel.checkSelectedOrderStock`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5258` `OperationLogCard`；`macos/TravelerAssistant.swift:5672` `OrderWorkflowView.summaryCard`；`macos/TravelerAssistant.swift:5692` `OrderWorkflowView.subsectionTitle`；`macos/TravelerAssistant.swift:988` `panelColorsNeedingThicknessWarning`；`macos/TravelerAssistant.swift:944` `orderedMaterialRows`；`macos/TravelerAssistant.swift:933` `orderMaterialDisplayName`；另有 4 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `setOrderFittingsIgnored`；是否真实写入仍取决于分支和参数。

- **L5672 · 方法** `private func summaryCard(title: String, value: String, detail: String, color: Color, warning: Bool = false) -> some View` — 封装 `summaryCard` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`value: String`；`detail: String`；`color: Color`；`warning: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5692 · 方法** `private func subsectionTitle(_ title: String, color: Color) -> some View` — 封装 `subsectionTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5699 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5709 · 结构体** `SettingsCard<Content` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5715 · 初始化器** `init( title: String, symbol: String, padding: CGFloat = 14, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`title: String`；`symbol: String`；`padding: CGFloat = 14`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5727 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5741 · 结构体** `InventoryStepRowView` — 定义与库存、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5745 · 初始化器** `init(step: InventoryStep, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`step: InventoryStep`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5750 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L5778 · 计算属性** `private var detailText: String` — 根据当前状态计算并返回`detailText` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1182` `operationDurationText`

- **L5784 · 计算属性** `@ViewBuilder private var icon: some View` — 根据当前状态计算并返回`icon` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5799 · 结构体** `InventoryOperationLogView` — 定义与库存、操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5802 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5833` `SelectableOperationLogView`

- **L5810 · 结构体** `OperationLogAutoScroller` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5813 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5817 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5833 · 结构体** `SelectableOperationLogView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5839 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5845 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5919` `SelectableOperationLogView.copySelected`；`macos/TravelerAssistant.swift:5907` `SelectableOperationLogView.select`；`macos/TravelerAssistant.swift:5741` `InventoryStepRowView`；`macos/TravelerAssistant.swift:5810` `OperationLogAutoScroller`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copySelected`, `Set`；是否真实写入仍取决于分支和参数。

- **L5902 · 计算属性** `private var scrollRevision: String` — 根据当前状态计算并返回`scrollRevision` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5907 · 方法** `private func select(_ id: UUID)` — 选择与 `select` 对应的数据或步骤。
  - 输入：`_ id: UUID`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L5919 · 方法** `private func copySelected()` — 封装 `copySelected` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1182` `operationDurationText`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L5939 · 结构体** `InventoryTravelerRowView` — 定义与库存、Traveler、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5945 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5146` `ScrollingTextOnHover`

- **L5976 · 计算属性** `private var statusColor: Color` — 根据当前状态计算并返回状态、颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5986 · 结构体** `InventoryMappingSheet` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5993 · 初始化器** `init( model: AppModel, travelerName: String, isPresented: Binding<Bool>, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`isPresented: Binding<Bool>`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6005 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5019` `View.appInputField`；`macos/TravelerAssistant.swift:3696` `AppModel.searchInventoryProducts`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:3723` `AppModel.saveInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryMapping`；是否真实写入仍取决于分支和参数。

- **L6072 · 结构体** `PendingInventoryMappingTarget` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6074 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6077 · 结构体** `PendingInventoryMappingWorkspace` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6082 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:6072` `PendingInventoryMappingTarget`；`macos/TravelerAssistant.swift:2833` `AppModel.closeInventoryMappingWorkspace`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`；`macos/TravelerAssistant.swift:5986` `InventoryMappingSheet`；`macos/TravelerAssistant.swift:6165` `PendingInventoryIgnoreSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryMappingWorkspace`；是否真实写入仍取决于分支和参数。

- **L6165 · 结构体** `PendingInventoryIgnoreSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6172 · 初始化器** `init( model: AppModel, travelerName: String, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6182 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5019` `View.appInputField`；`macos/TravelerAssistant.swift:3639` `AppModel.saveInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L6230 · 结构体** `InventoryView` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6241 · 初始化器** `init( model: AppModel, onClose: (() -> Void)? = nil, orderContextID: String = "", orderContextFactoryNames: [String] = [], orderContextFactoryOrders: [String] = [] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`onClose: (() -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6255 · 计算属性** `private var selectedTravelerCount: Int` — 选择Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6259 · 计算属性** `private var hasMappedOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6263 · 计算属性** `private var hasConfirmedNoOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6269 · 计算属性** `private var customerSuppliedOnly: Bool` — 根据当前状态计算并返回`customerSuppliedOnly` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L6276 · 计算属性** `private var confirmationTitle: String` — 根据当前状态计算并返回`confirmationTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6283 · 计算属性** `private var selectedTravelerDisplayName: String` — 选择Traveler、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6288 · 方法** `private func previewRowContent(_ row: InventoryPreviewRow) -> some View` — 预览预览、行数据相关数据或步骤。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6555` `InventoryView.previewStatusColor`

- **L6324 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:6532` `InventoryView.outboundStep`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5258` `OperationLogCard`；`macos/TravelerAssistant.swift:6288` `InventoryView.previewRowContent`；`macos/TravelerAssistant.swift:5028` `View.inventoryActionButton`；`macos/TravelerAssistant.swift:3098` `AppModel.previewOrderInventory`；`macos/TravelerAssistant.swift:5986` `InventoryMappingSheet`；`macos/TravelerAssistant.swift:6546` `InventoryView.confirmationRow`；`macos/TravelerAssistant.swift:3443` `AppModel.openAndFillSelectedInventory`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outboundStep`, `onClose`, `openAndFillSelectedInventory`；是否真实写入仍取决于分支和参数。

- **L6523 · 方法** `private func statusColor(_ status: String) -> Color` — 封装状态、颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6532 · 方法** `private func outboundStep(_ number: Int, _ title: String, active: Bool) -> some View` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ number: Int`；`_ title: String`；`active: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6546 · 方法** `private func confirmationRow(_ label: String, _ value: String, valueColor: Color = .primary) -> some View` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ label: String`；`_ value: String`；`valueColor: Color = .primary`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6555 · 方法** `private func previewStatusColor(_ status: String) -> Color` — 预览预览、状态、颜色相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6564 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6574 · 方法** `private func stepIcon(_ state: String) -> some View` — 封装 `stepIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6588 · 结构体** `TodoView` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6597 · 计算属性** `private var sortedItems: [TodoItem]` — 排序与 `sortedItems` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[TodoItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6618 · 计算属性** `private var selectedItem: TodoItem?` — 选择项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`TodoItem?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6623 · 计算属性** `private var openCount: Int` — 打开与 `openCount` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6627 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:6779` `TodoView.todoRow`；`macos/TravelerAssistant.swift:1652` `AppModel.toggleTodoCompletion`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:6892` `TodoDeadlinePickerControl`；`macos/TravelerAssistant.swift:5011` `View.appPageFrame`；`macos/TravelerAssistant.swift:6945` `TodoEditorSheet`；`macos/TravelerAssistant.swift:1659` `AppModel.deleteTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `deleteTodo`；是否真实写入仍取决于分支和参数。

- **L6779 · 方法** `private func todoRow(_ item: TodoItem) -> some View` — 封装待办、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6852` `TodoView.deadlineText`；`macos/TravelerAssistant.swift:6872` `TodoView.deadlineColor`；`macos/TravelerAssistant.swift:6860` `TodoView.deadlineBadge`；`macos/TravelerAssistant.swift:1652` `AppModel.toggleTodoCompletion`

- **L6832 · 计算属性** `private var todoSelectionMessage: String?` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6837 · 计算属性** `private var deleteAlertBinding: Binding<Bool>` — 删除与 `deleteAlertBinding` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Binding<Bool>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6844 · 方法** `private func addTodo()` — 新增待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6852 · 方法** `private func deadlineText(_ date: Date?) -> String` — 封装 `deadlineText` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date?`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6860 · 方法** `private func deadlineBadge(_ item: TodoItem) -> String?` — 封装 `deadlineBadge` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6872 · 方法** `private func deadlineColor(_ item: TodoItem) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6884 · 函数** `func todoDeadlinePickerDisplay(_ date: Date) -> String` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6892 · 结构体** `TodoDeadlinePickerControl` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6896 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6884` `todoDeadlinePickerDisplay`；`macos/OrderDashboardView.swift:104` `AppGlassDatePickerCalendar`；`macos/OrderDashboardView.swift:272` `View.appGlassDatePickerPopoverSurface`

- **L6945 · 结构体** `TodoEditorSheet` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6953 · 初始化器** `init(model: AppModel, item: TodoItem)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`item: TodoItem`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6965 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5019` `View.appInputField`；`macos/TravelerAssistant.swift:6892` `TodoDeadlinePickerControl`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:1640` `AppModel.updateTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateTodo`；是否真实写入仍取决于分支和参数。

- **L6994 · 结构体** `SettingsView` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7001 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`；`macos/TravelerAssistant.swift:7299` `SettingsView.compactStatus`；`macos/TravelerAssistant.swift:1838` `AppModel.saveAllSettings`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5011` `View.appPageFrame`；`macos/TravelerAssistant.swift:2996` `AppModel.refreshInventoryCatalogStatus`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`；`macos/TravelerAssistant.swift:1770` `AppModel.refreshOperationLogInfo`；`macos/TravelerAssistant.swift:7501` `OperationLogViewerView`；`macos/TravelerAssistant.swift:7315` `InventoryIgnoredMappingsSheet`；`macos/TravelerAssistant.swift:7406` `InventoryManualMappingsSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAllSettings`；是否真实写入仍取决于分支和参数。

- **L7065 · 计算属性** `private var runAndFileSettingsCard: some View` — 执行文件、设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7249` `SettingsView.settingsRowLabel`；`macos/TravelerAssistant.swift:7256` `SettingsView.settingsDateDisplay`；`macos/OrderDashboardView.swift:104` `AppGlassDatePickerCalendar`；`macos/OrderDashboardView.swift:272` `View.appGlassDatePickerPopoverSurface`；`macos/TravelerAssistant.swift:7265` `SettingsView.settingsFieldRow`

- **L7098 · 计算属性** `private var accountSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5019` `View.appInputField`；`macos/TravelerAssistant.swift:1862` `AppModel.saveJdyPassword`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:2925` `AppModel.openInventoryChrome`；`macos/TravelerAssistant.swift:1913` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveJdyPassword`, `openInventoryChrome`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L7151 · 计算属性** `private var inventorySettingsCard: some View` — 根据当前状态计算并返回库存、设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7299` `SettingsView.compactStatus`；`macos/TravelerAssistant.swift:2938` `AppModel.updateInventoryCatalog`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:7278` `SettingsView.settingsManagementRow`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateInventoryCatalog`；是否真实写入仍取决于分支和参数。

- **L7183 · 计算属性** `private var maintenanceSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1586` `AppModel.performBackup`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:1748` `AppModel.setOperationLogEnabled`；`macos/TravelerAssistant.swift:1797` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1774` `AppModel.trimOperationLog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setOperationLogEnabled`；是否真实写入仍取决于分支和参数。

- **L7249 · 方法** `private func settingsRowLabel(_ title: String) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7256 · 方法** `private func settingsDateDisplay(_ value: Date) -> String` — 设置设置、日期相关数据或步骤。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7265 · 方法** `private func settingsFieldRow( _ title: String, placeholder: String, text: Binding<String> ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`placeholder: String`；`text: Binding<String>`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7249` `SettingsView.settingsRowLabel`；`macos/TravelerAssistant.swift:5019` `View.appInputField`

- **L7278 · 方法** `private func settingsManagementRow( _ title: String, count: Int, help: String, action: @escaping () -> Void ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`count: Int`；`help: String`；`action: @escaping () -> Void`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5023` `View.appActionButton`

- **L7299 · 方法** `private func compactStatus(_ status: String) -> some View` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4973` `settingsStatusDisplayText`；`macos/TravelerAssistant.swift:4964` `settingsStatusKind`

- **L7315 · 结构体** `InventoryIgnoredMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7322 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5019` `View.appInputField`；`macos/TravelerAssistant.swift:3639` `AppModel.saveInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:3664` `AppModel.updateInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:3686` `AppModel.removeInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryIgnoredMapping`, `updateInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L7399 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7406 · 结构体** `InventoryManualMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7413 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:5019` `View.appInputField`；`macos/TravelerAssistant.swift:3597` `AppModel.saveSettingsManualMapping`；`macos/TravelerAssistant.swift:3611` `AppModel.updateSettingsManualMapping`；`macos/TravelerAssistant.swift:3629` `AppModel.removeSettingsManualMapping`；`macos/TravelerAssistant.swift:3576` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettingsManualMapping`, `updateSettingsManualMapping`；是否真实写入仍取决于分支和参数。

- **L7494 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7501 · 结构体** `OperationLogViewerView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7506 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/OperationLog.swift:49` `OperationLogReader.entries`

- **L7572 · 枚举** `AppSection` — 定义 `AppSection` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7578 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7580 · 计算属性** `var title: String` — 根据当前状态计算并返回`title` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7589 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7598 · 计算属性** `var pageTitle: String` — 根据当前状态计算并返回`pageTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7607 · 计算属性** `var subtitle: String` — 根据当前状态计算并返回`subtitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7616 · 计算属性** `var isWorkSection: Bool` — 根据当前状态计算并返回`isWorkSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7625 · 结构体** `TopNavigationBar` — 定义 `TopNavigationBar` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7630 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7742` `TopNavigationBar.navButton`；`macos/TravelerAssistant.swift:5023` `View.appActionButton`；`macos/TravelerAssistant.swift:7766` `TopNavigationBar.designNote`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`；`macos/OrderDashboardView.swift:3269` `PendingCenterSheet`；`macos/OrderDashboardView.swift:4253` `ServerWriteConfirmationSheet`；`macos/TravelerAssistant.swift:6077` `PendingInventoryMappingWorkspace`；`macos/OrderDashboardView.swift:3802` `AimesReviewSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteConfirmationSheet`；是否真实写入仍取决于分支和参数。

- **L7721 · 计算属性** `@ViewBuilder private var contextualStatus: some View` — 根据当前状态计算并返回状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5107` `AppStatusBadge`

- **L7742 · 方法** `private func navButton(_ section: AppSection) -> some View` — 封装 `navButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ section: AppSection`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7766 · 方法** `private func designNote(_ title: String, _ text: String) -> some View` — 封装 `designNote` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ text: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7776 · 结构体** `TravelerAssistantApp` — 定义与Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7780 · 计算属性** `var body: some Scene` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some Scene`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7625` `TopNavigationBar`；`macos/AssistantView.swift:696` `AssistantView`；`macos/OrderDashboardView.swift:1395` `OrderDashboardView`；`macos/TravelerAssistant.swift:6588` `TodoView`；`macos/TravelerAssistant.swift:6994` `SettingsView`；`macos/TravelerAssistant.swift:5039` `AppGlassGroupBoxStyle`；`macos/TravelerAssistant.swift:5072` `LiquidGlassPreviewBackdrop`；`macos/TravelerAssistant.swift:2966` `AppModel.closeInventoryChromeOnQuit`；`macos/TravelerAssistant.swift:1586` `AppModel.performBackup`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryChromeOnQuit`；是否真实写入仍取决于分支和参数。
