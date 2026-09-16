# PP FlowHub Swift/macOS 全符号中文参考

> 本文件由 `tools/generate_code_reference.py` 生成。请不要手工修改。

## 如何阅读

- 范围：`macos/` App 生产代码，共登记 **790** 个类型、函数、方法、计算属性或脚本过程。
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
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1083` `OrderMaterialPreview`；`macos/TravelerAssistant.swift:1176` `OrderFactoryPreview`；`macos/TravelerAssistant.swift:1182` `OrderFittingPreview`

- **L91 · 类** `SpeechInputController` — 定义 `SpeechInputController` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L104 · 方法** `func beginPushToTalk()` — 封装 `beginPushToTalk` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:158` `SpeechInputController.requestAccessAndStart`

- **L113 · 方法** `func endPushToTalk(onComplete: @escaping (String) -> Void)` — 封装 `endPushToTalk` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`onComplete: @escaping (String) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:131` `SpeechInputController.stop`；`macos/AssistantView.swift:144` `SpeechInputController.completeRecognition`

- **L131 · 方法** `func stop()` — 封装 `stop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L144 · 方法** `private func completeRecognition()` — 封装 `completeRecognition` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L158 · 方法** `private func requestAccessAndStart()` — 封装 `requestAccessAndStart` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:177` `SpeechInputController.start`

- **L177 · 方法** `private func start()` — 启动与 `start` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:144` `SpeechInputController.completeRecognition`；`macos/AssistantView.swift:131` `SpeechInputController.stop`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L222 · 函数** `func isPushToTalkShortcut(keyCode: UInt16, modifiers: NSEvent.ModifierFlags) -> Bool` — 封装 `isPushToTalkShortcut` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`keyCode: UInt16`；`modifiers: NSEvent.ModifierFlags`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L227 · 类** `PushToTalkShortcutMonitor` — 定义 `PushToTalkShortcutMonitor` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L232 · 方法** `func install(onPress: @escaping () -> Void, onRelease: @escaping () -> Void)` — 封装 `install` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`onPress: @escaping () -> Void`；`onRelease: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:222` `isPushToTalkShortcut`

- **L250 · 方法** `func uninstall()` — 封装 `uninstall` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L259 · 结构体** `AssistantOrderPreviewView` — 定义与订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L262 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:358` `AssistantOrderPreviewView.metricCard`；`macos/AssistantView.swift:369` `AssistantOrderPreviewView.sectionTitle`；`macos/TravelerAssistant.swift:1109` `orderMaterialDisplayName`

- **L358 · 方法** `private func metricCard(_ title: String, _ value: String, _ icon: String) -> some View` — 封装 `metricCard` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ value: String`；`_ icon: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L369 · 方法** `private func sectionTitle(_ title: String, _ icon: String) -> some View` — 封装 `sectionTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ icon: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L374 · 结构体** `AssistantOrderListView` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L377 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1444` `appDisplayTimestamp`

- **L397 · 结构体** `AssistantStockComparisonView` — 定义 `AssistantStockComparisonView` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L402 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L462 · 函数** `func assistantTaskShowsHeaderCancel(_ status: String) -> Bool` — 封装 `assistantTaskShowsHeaderCancel` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L466 · 结构体** `AssistantCommandHintsContent` — 定义 `AssistantCommandHintsContent` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L467 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L480 · 扩展** `AppModel` — 定义 `AppModel` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L481 · 方法** `func loadAssistantUsage()` — 读取与 `loadAssistantUsage` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L507 · 方法** `func runAssistantCommand(approved: Bool = false)` — 把助手输入加入任务队列，并启动后续命令执行。
  - 输入：`approved: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/AssistantView.swift:549` `AppModel.executeAssistantTask`；`macos/TravelerAssistant.swift:1550` `AssistantTaskItem`；`macos/AssistantView.swift:542` `AppModel.processNextAssistantTask`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `executeAssistantTask`；是否真实写入仍取决于分支和参数。

- **L525 · 方法** `func cancelAssistantTask(_ id: UUID)` — 封装 `cancelAssistantTask` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ id: UUID`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/AssistantView.swift:542` `AppModel.processNextAssistantTask`

- **L542 · 方法** `func processNextAssistantTask()` — 处理与 `processNextAssistantTask` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:549` `AppModel.executeAssistantTask`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `executeAssistantTask`；是否真实写入仍取决于分支和参数。

- **L549 · 方法** `private func executeAssistantTask(_ task: AssistantTaskItem, approved: Bool)` — 启动助手子进程、消费输出并把结果映射为页面状态。
  - 输入：`_ task: AssistantTaskItem`；`approved: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2320` `AppModel.newOperationID`；`macos/TravelerAssistant.swift:2349` `AppModel.environmentForOperation`；`macos/AssistantView.swift:674` `AppModel.finishAssistantTask`；`macos/AssistantView.swift:36` `AssistantOrderResult`；`macos/TravelerAssistant.swift:1196` `OrderStockPreview`；`macos/TravelerAssistant.swift:85` `OrderFolderItem`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/AssistantView.swift:481` `AppModel.loadAssistantUsage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L674 · 方法** `private func finishAssistantTask(_ id: UUID, status: String)` — 结束并收口与 `finishAssistantTask` 对应的数据或步骤。
  - 输入：`_ id: UUID`；`status: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:542` `AppModel.processNextAssistantTask`

- **L684 · 枚举** `AssistantDashboardTypography` — 定义与看板相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L699 · 枚举** `AssistantProgressSegmentState` — 定义与进度相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L705 · 结构体** `AssistantView` — 定义 `AssistantView` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L716 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5824` `View.appPageFrame`；`macos/AssistantView.swift:9` `canonicalSpeechCommand`；`macos/TravelerAssistant.swift:2750` `AppModel.startOrderDashboard`；`macos/AssistantView.swift:232` `PushToTalkShortcutMonitor.install`；`macos/AssistantView.swift:104` `SpeechInputController.beginPushToTalk`；`macos/AssistantView.swift:1443` `AssistantView.finishPushToTalk`；`macos/AssistantView.swift:250` `PushToTalkShortcutMonitor.uninstall`；`macos/AssistantView.swift:131` `SpeechInputController.stop`

- **L755 · 计算属性** `private var commandStrip: some View` — 根据当前状态计算并返回`commandStrip` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:507` `AppModel.runAssistantCommand`；`macos/AssistantView.swift:1450` `AssistantView.beginCommandHintsAnchorHover`；`macos/AssistantView.swift:1465` `AssistantView.endCommandHintsAnchorHover`；`macos/AssistantView.swift:466` `AssistantCommandHintsContent`；`macos/AssistantView.swift:1471` `AssistantView.beginCommandHintsPanelHover`；`macos/AssistantView.swift:1477` `AssistantView.endCommandHintsPanelHover`；`macos/AssistantView.swift:104` `SpeechInputController.beginPushToTalk`；`macos/AssistantView.swift:1443` `AssistantView.finishPushToTalk`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5920` `AppStatusBadge`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L814 · 计算属性** `private var orderStatusBoard: some View` — 根据当前状态计算并返回订单、状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:857` `AssistantView.assistantMetric`；`macos/AssistantView.swift:903` `AssistantView.assistantOrderCard`

- **L857 · 方法** `private func assistantMetric(_ title: String, value: Int, symbol: String, color: Color) -> some View` — 封装 `assistantMetric` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`value: Int`；`symbol: String`；`color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L878 · 计算属性** `private var currentOperationSummary: some View` — 根据当前状态计算并返回操作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L903 · 方法** `private func assistantOrderCard(_ item: OrderDashboardItem) -> some View` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1207` `AssistantView.openOrderCenter`；`macos/AssistantView.swift:941` `AssistantView.assistantProgressRail`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderCenter`；是否真实写入仍取决于分支和参数。

- **L941 · 方法** `private func assistantProgressRail(_ item: OrderDashboardItem) -> some View` — 封装进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1124` `AssistantView.assistantProgressValue`；`macos/AssistantView.swift:1056` `AssistantView.assistantStageIcon`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `move`；是否真实写入仍取决于分支和参数。

- **L1056 · 方法** `private func assistantStageIcon( completed: Bool, current: Bool, fallbackSymbol: String ) -> some View` — 封装 `assistantStageIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`completed: Bool`；`current: Bool`；`fallbackSymbol: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1124 · 方法** `private func assistantProgressValue(_ value: String) -> String` — 封装进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1128 · 计算属性** `private var ongoingOrders: [OrderDashboardItem]` — 根据当前状态计算并返回`ongoingOrders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderDashboardItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1134 · 计算属性** `private var monthlyCompletedCount: Int` — 根据当前状态计算并返回`monthlyCompletedCount` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1466` `dashboardTimestamp`

- **L1140 · 计算属性** `private var effectiveOrders: [OrderDashboardItem]` — 根据当前状态计算并返回`effectiveOrders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderDashboardItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1144 · 计算属性** `private var showsAssistantWorkspace: Bool` — 根据当前状态计算并返回`showsAssistantWorkspace` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1152 · 计算属性** `private var currentAssistantOperation: (title: String, running: Bool)` — 根据当前状态计算并返回操作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`(title: String, running: Bool)`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:856` `dashboardMessageDetail`；`macos/OrderDashboardView.swift:863` `dashboardStatusIsInProgress`

- **L1168 · 方法** `private func assistantStageSummary(_ item: OrderDashboardItem) -> String` — 封装 `assistantStageSummary` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1182 · 方法** `private func assistantOrderDates(_ item: OrderDashboardItem) -> String` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1193` `AssistantView.assistantDate`

- **L1193 · 方法** `private func assistantDate(_ value: String) -> String` — 封装日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1448` `dashboardBusinessDate`；`macos/TravelerAssistant.swift:1444` `appDisplayTimestamp`

- **L1198 · 方法** `private func assistantStageKind(_ stage: String) -> AppStatusBadge.Kind` — 封装 `assistantStageKind` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stage: String`
  - 返回：`AppStatusBadge.Kind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1207 · 方法** `private func openOrderCenter(_ orderID: String?)` — 打开订单相关数据或步骤。
  - 输入：`_ orderID: String?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1212 · 计算属性** `private var commandCard: some View` — 根据当前状态计算并返回`commandCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:507` `AppModel.runAssistantCommand`；`macos/AssistantView.swift:1450` `AssistantView.beginCommandHintsAnchorHover`；`macos/AssistantView.swift:1465` `AssistantView.endCommandHintsAnchorHover`；`macos/AssistantView.swift:466` `AssistantCommandHintsContent`；`macos/AssistantView.swift:1471` `AssistantView.beginCommandHintsPanelHover`；`macos/AssistantView.swift:1477` `AssistantView.endCommandHintsPanelHover`；`macos/AssistantView.swift:104` `SpeechInputController.beginPushToTalk`；`macos/AssistantView.swift:1443` `AssistantView.finishPushToTalk`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/AssistantView.swift:1414` `AssistantView.flowStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L1293 · 计算属性** `private var workspaceCard: some View` — 根据当前状态计算并返回`workspaceCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/AssistantView.swift:1434` `AssistantView.badgeKind`；`macos/AssistantView.swift:462` `assistantTaskShowsHeaderCancel`；`macos/AssistantView.swift:525` `AppModel.cancelAssistantTask`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/AssistantView.swift:397` `AssistantStockComparisonView`；`macos/AssistantView.swift:259` `AssistantOrderPreviewView`；`macos/AssistantView.swift:374` `AssistantOrderListView`

- **L1336 · 计算属性** `private var approvalCard: some View` — 根据当前状态计算并返回`approvalCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/AssistantView.swift:525` `AppModel.cancelAssistantTask`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/AssistantView.swift:507` `AppModel.runAssistantCommand`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L1370 · 计算属性** `private var queueCard: some View` — 根据当前状态计算并返回`queueCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1524` `AssistantView.taskStatusColor`

- **L1400 · 计算属性** `private var usageCard: some View` — 根据当前状态计算并返回`usageCard` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1425` `AssistantView.statusLine`

- **L1414 · 方法** `private func flowStep(_ number: String, _ title: String, active: Bool) -> some View` — 封装 `flowStep` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ number: String`；`_ title: String`；`active: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1425 · 方法** `private func statusLine(_ label: String, _ value: String) -> some View` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ label: String`；`_ value: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1434 · 方法** `private func badgeKind(_ status: String) -> AppStatusBadge.Kind` — 封装 `badgeKind` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`AppStatusBadge.Kind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1443 · 方法** `private func finishPushToTalk()` — 结束并收口与 `finishPushToTalk` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:9` `canonicalSpeechCommand`；`macos/AssistantView.swift:507` `AppModel.runAssistantCommand`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runAssistantCommand`；是否真实写入仍取决于分支和参数。

- **L1450 · 方法** `private func beginCommandHintsAnchorHover()` — 封装 `beginCommandHintsAnchorHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1465 · 方法** `private func endCommandHintsAnchorHover()` — 封装 `endCommandHintsAnchorHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1483` `AssistantView.scheduleCommandHintsClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `scheduleCommandHintsClose`；是否真实写入仍取决于分支和参数。

- **L1471 · 方法** `private func beginCommandHintsPanelHover()` — 封装 `beginCommandHintsPanelHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1477 · 方法** `private func endCommandHintsPanelHover()` — 封装 `endCommandHintsPanelHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/AssistantView.swift:1483` `AssistantView.scheduleCommandHintsClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `scheduleCommandHintsClose`；是否真实写入仍取决于分支和参数。

- **L1483 · 方法** `private func scheduleCommandHintsClose()` — 封装 `scheduleCommandHintsClose` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1496 · 计算属性** `private var displayedTask: AssistantTaskItem?` — 根据当前状态计算并返回`displayedTask` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`AssistantTaskItem?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1504 · 计算属性** `private var queuedTaskCount: Int` — 根据当前状态计算并返回`queuedTaskCount` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1508 · 计算属性** `private var workspaceTitle: String` — 根据当前状态计算并返回`workspaceTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1516 · 计算属性** `private var workspaceIcon: String` — 根据当前状态计算并返回`workspaceIcon` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1524 · 方法** `private func taskStatusColor(_ status: String) -> Color` — 封装状态、颜色相关的辅助逻辑，供所属模块或类型复用。
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
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:272` `OperationLogWriter.redact`；`macos/OrderDashboardView.swift:1318` `Coordinator.close`
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
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`

- **L310 · 函数** `func sortedServerWriteMaterialChanges(_ changes: [ServerWriteMaterialChange]) -> [ServerWriteMaterialChange]` — 排序Server 数据、材料相关数据或步骤。
  - 输入：`_ changes: [ServerWriteMaterialChange]`
  - 返回：`[ServerWriteMaterialChange]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:293` `serverWriteMaterialTypeRank`；`macos/OrderDashboardView.swift:302` `serverWritePlywoodThicknessRank`；`macos/TravelerAssistant.swift:1410` `Double`
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
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1120` `orderedMaterialRows`

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
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:707` `orderDashboardIsCompleted`

- **L707 · 函数** `func orderDashboardIsCompleted(_ stage: String) -> Bool` — 封装订单、看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stage: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L711 · 函数** `func orderDashboardStatusHelp(status: String, validationMessage: String) -> String` — 封装订单、看板、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`status: String`；`validationMessage: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L719 · 函数** `func orderDashboardProgressFraction(completed: Int, total: Int) -> Double` — 封装订单、看板、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`completed: Int`；`total: Int`
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`

- **L724 · 函数** `func orderInstallationDisplayDate(_ value: String) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L734 · 函数** `func orderInstallationDateSummary(_ days: [OrderInstallationDay]) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ days: [OrderInstallationDay]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:724` `orderInstallationDisplayDate`

- **L739 · 函数** `func orderInstallationPlannedDateSummary(_ days: [OrderInstallationDay]) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ days: [OrderInstallationDay]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:724` `orderInstallationDisplayDate`

- **L744 · 函数** `func orderInstallationQuickSummaries( planned: [OrderInstallationDay], actual: [OrderInstallationDay] ) -> [String]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`planned: [OrderInstallationDay]`；`actual: [OrderInstallationDay]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:739` `orderInstallationPlannedDateSummary`；`macos/OrderDashboardView.swift:734` `orderInstallationDateSummary`

- **L760 · 结构体** `OrderDashboardProgressBar` — 定义与订单、看板、进度相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L765 · 初始化器** `init(completed: Int, total: Int, accessibilityTitle: String = "优化进度")` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`completed: Int`；`total: Int`；`accessibilityTitle: String = "优化进度"`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L771 · 计算属性** `private var fraction: Double` — 根据当前状态计算并返回`fraction` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:719` `orderDashboardProgressFraction`

- **L775 · 计算属性** `private var progressColor: Color` — 根据当前状态计算并返回进度、颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L779 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L796 · 函数** `func shouldPresentPendingCenterAfterAimes( presentIfNeeded: Bool, pendingAimesReviews: [AimesReviewItem], aimesFormatWarnings: [AimesReviewItem] = [] ) -> Bool` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`presentIfNeeded: Bool`；`pendingAimesReviews: [AimesReviewItem]`；`aimesFormatWarnings: [AimesReviewItem] = []`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L804 · 结构体** `DashboardMessage` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L817 · 初始化器** `init( id: String, source: String, time: String, title: String, detail: String, state: String, manualPaths: [String] = [], operationDetails: [String] = [], contextDetails: [String] = [], duration: TimeInterval? = nil, operationDurations: [DashboardOperationDuration] = [] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`source: String`；`time: String`；`title: String`；`detail: String`；`state: String`；`manualPaths: [String] = []`；`operationDetails: [String] = []`；`contextDetails: [String] = []`；`duration: TimeInterval? = nil`；`operationDurations: [DashboardOperationDuration] = []`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L844 · 结构体** `DashboardOperationDisplay` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L849 · 函数** `func dashboardMessageState(_ text: String) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L856 · 函数** `func dashboardMessageDetail(_ text: String) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L863 · 函数** `func dashboardStatusIsInProgress(_ text: String) -> Bool` — 封装看板、状态、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:856` `dashboardMessageDetail`

- **L869 · 函数** `func dashboardMessageIsRunning(_ message: DashboardMessage) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: DashboardMessage`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:863` `dashboardStatusIsInProgress`

- **L884 · 函数** `func dashboardMessages( syncStatus: String, syncTime: String, inventoryStatus: String = "库存操作尚未执行", inventoryTime: String = "", aimesStatus: String, aimesTime: String, serverStatus: String, serverTime: String, activity: [InventoryStep], operationDetailsBySource: [String: [String]] = [:], manualPathsBySource: [String: [String]] = [:], contextDetailsBySource: [String: [String]] = [:], durationsBySource: [String: TimeInterval] = [:], operationDurationsBySource: [String: [DashboardOperationDuration]] = [:], sessionMessages: [DashboardMessage]? = nil ) -> [DashboardMessage]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`syncStatus: String`；`syncTime: String`；`inventoryStatus: String = "库存操作尚未执行"`；`inventoryTime: String = ""`；`aimesStatus: String`；`aimesTime: String`；`serverStatus: String`；`serverTime: String`；`activity: [InventoryStep]`；`operationDetailsBySource: [String: [String]] = [:]`；`manualPathsBySource: [String: [String]] = [:]`；`contextDetailsBySource: [String: [String]] = [:]`；`durationsBySource: [String: TimeInterval] = [:]`；`operationDurationsBySource: [String: [DashboardOperationDuration]] = [:]`；`sessionMessages: [DashboardMessage]? = nil`
  - 返回：`[DashboardMessage]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:856` `dashboardMessageDetail`；`macos/OrderDashboardView.swift:863` `dashboardStatusIsInProgress`；`macos/OrderDashboardView.swift:849` `dashboardMessageState`；`macos/OrderDashboardView.swift:804` `DashboardMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L963 · 函数** `func dashboardVisibleMessages(_ messages: [DashboardMessage], isRunning: Bool) -> [DashboardMessage]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ messages: [DashboardMessage]`；`isRunning: Bool`
  - 返回：`[DashboardMessage]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:869` `dashboardMessageIsRunning`

- **L968 · 函数** `func dashboardCurrentOperation( messages: [DashboardMessage], isRunning: Bool ) -> DashboardOperationDisplay?` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`messages: [DashboardMessage]`；`isRunning: Bool`
  - 返回：`DashboardOperationDisplay?`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:844` `DashboardOperationDisplay`

- **L982 · 函数** `func dashboardMessageScrollKey(_ messages: [DashboardMessage]) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ messages: [DashboardMessage]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L991 · 函数** `func dashboardMessageSupportsHoverDetail(_ message: DashboardMessage) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: DashboardMessage`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:869` `dashboardMessageIsRunning`

- **L1000 · 函数** `func dashboardMessageDetailText(_ message: DashboardMessage) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: DashboardMessage`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1363` `operationDurationText`

- **L1014 · 函数** `func dashboardMessageSummaryText(_ message: DashboardMessage, showsDuration: Bool = true) -> String` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: DashboardMessage`；`showsDuration: Bool = true`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1363` `operationDurationText`

- **L1022 · 函数** `func dashboardAimesReviewDetail(_ item: AimesReviewItem, status: String) -> String` — 封装看板、AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`status: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1033 · 函数** `func dashboardAimesActionDetails( pending: [AimesReviewItem], ignored: [AimesReviewItem], assigned: [AimesReviewItem] ) -> [String]` — 封装看板、AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`pending: [AimesReviewItem]`；`ignored: [AimesReviewItem]`；`assigned: [AimesReviewItem]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1022` `dashboardAimesReviewDetail`

- **L1054 · 函数** `func dashboardAimesWarningDetails(_ warnings: [[String: Any]]) -> [String]` — 封装看板、AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ warnings: [[String: Any]]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1070 · 结构体** `DashboardMessageTracePopover` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1073 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1000` `dashboardMessageDetailText`；`macos/OrderDashboardView.swift:1128` `DashboardMessageTracePopover.dashboardTraceBullet`；`macos/TravelerAssistant.swift:1363` `operationDurationText`

- **L1128 · 方法** `private func dashboardTraceBullet(_ text: String) -> some View` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1139 · 类** `DashboardMessageTraceTrackingView` — 定义与看板相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1143 · 方法** `override func updateTrackingAreas()` — 更新与 `updateTrackingAreas` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1156 · 方法** `override func mouseEntered(with event: NSEvent)` — 封装 `mouseEntered` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`with event: NSEvent`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1161 · 方法** `override func mouseExited(with event: NSEvent)` — 封装 `mouseExited` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`with event: NSEvent`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1167 · 结构体** `DashboardMessageTracePanelPresenter` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1173 · 方法** `func makeCoordinator() -> Coordinator` — 创建与 `makeCoordinator` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Coordinator`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1177 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1183 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update`；是否真实写入仍取决于分支和参数。

- **L1193 · 方法** `static func dismantleNSView(_ nsView: NSView, coordinator: Coordinator)` — 封装 `dismantleNSView` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ nsView: NSView`；`coordinator: Coordinator`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1318` `Coordinator.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close`；是否真实写入仍取决于分支和参数。

- **L1197 · 类** `Coordinator` — 定义 `Coordinator` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1206 · 方法** `func update( anchorView: NSView, message: DashboardMessage, isPresented: Bool, onPanelEntered: @escaping () -> Void, onPanelExited: @escaping () -> Void )` — 更新与 `update` 对应的数据或步骤。
  - 输入：`anchorView: NSView`；`message: DashboardMessage`；`isPresented: Bool`；`onPanelEntered: @escaping () -> Void`；`onPanelExited: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1318` `Coordinator.close`；`macos/OrderDashboardView.swift:1229` `Coordinator.presentIfNeeded`；`macos/OrderDashboardView.swift:1291` `Coordinator.updatePosition`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close`, `updatePosition`；是否真实写入仍取决于分支和参数。

- **L1229 · 方法** `private func presentIfNeeded()` — 封装 `presentIfNeeded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:336` `dashboardMessageHoverCanPresent`；`macos/OrderDashboardView.swift:1070` `DashboardMessageTracePopover`；`macos/OrderDashboardView.swift:1139` `DashboardMessageTraceTrackingView`；`macos/OrderDashboardView.swift:1291` `Coordinator.updatePosition`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setContentSize`, `updatePosition`；是否真实写入仍取决于分支和参数。

- **L1291 · 方法** `private func updatePosition()` — 更新与 `updatePosition` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setFrameOrigin`；是否真实写入仍取决于分支和参数。

- **L1318 · 方法** `func close()` — 关闭与 `close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1324 · 析构器** `deinit` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1318` `Coordinator.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close`；是否真实写入仍取决于分支和参数。

- **L1330 · 结构体** `DashboardMessageTraceHost<Content` — 定义与看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1339 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1369` `DashboardMessageTraceHost<Content.beginHover`；`macos/OrderDashboardView.swift:1388` `DashboardMessageTraceHost<Content.endHover`；`macos/OrderDashboardView.swift:1167` `DashboardMessageTracePanelPresenter`

- **L1369 · 方法** `private func beginHover()` — 封装 `beginHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1388 · 方法** `private func endHover()` — 封装 `endHover` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1395` `DashboardMessageTraceHost<Content.schedulePopoverClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `schedulePopoverClose`；是否真实写入仍取决于分支和参数。

- **L1395 · 方法** `private func schedulePopoverClose()` — 封装 `schedulePopoverClose` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1406 · 方法** `private func panelEntered()` — 封装 `panelEntered` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1413 · 方法** `private func panelExited()` — 封装 `panelExited` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1395` `DashboardMessageTraceHost<Content.schedulePopoverClose`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `schedulePopoverClose`；是否真实写入仍取决于分支和参数。

- **L1421 · 结构体** `OrderDashboardView` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1437 · 计算属性** `private var filteredOrders: [OrderDashboardItem]` — 根据当前状态计算并返回`filteredOrders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderDashboardItem]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:697` `orderDashboardStageMatchesFilter`

- **L1447 · 计算属性** `private var selectedFactory: OrderFactoryPreview?` — 选择工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`OrderFactoryPreview?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1451 · 计算属性** `private var availableHardwareFactoryOrders: Set<String>` — 根据当前状态计算并返回五金、工厂单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Set<String>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L1460 · 方法** `private func traceHost<Content: View>( for message: DashboardMessage, @ViewBuilder content: @escaping () -> Content ) -> some View` — 封装 `traceHost` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`for message: DashboardMessage`；`@ViewBuilder content: @escaping () -> Content`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:991` `dashboardMessageSupportsHoverDetail`

- **L1475 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5824` `View.appPageFrame`；`macos/TravelerAssistant.swift:2750` `AppModel.startOrderDashboard`；`macos/OrderDashboardView.swift:2109` `OrderDashboardView.openRequestedOrderIfAvailable`；`macos/OrderDashboardView.swift:2178` `OrderDashboardDetailPage`；`macos/OrderDashboardView.swift:2440` `OrderAnnotationsSheet`；`macos/OrderDashboardView.swift:3814` `OrderCostSheet`；`macos/OrderDashboardView.swift:4908` `FactoryStockComparisonSheet`；`macos/OrderDashboardView.swift:2883` `ProductionSheet`；`macos/OrderDashboardView.swift:3097` `OrderShipmentConfirmationSheet`；`macos/TravelerAssistant.swift:4004` `AppModel.startDirectOrderShipment`；`macos/OrderDashboardView.swift:3172` `OutboundScopeSheet`；`macos/TravelerAssistant.swift:3306` `AppModel.prepareSelectedServerFolder`；另有 1 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openRequestedOrderIfAvailable`, `OutboundScopeSheet`；是否真实写入仍取决于分支和参数。

- **L1567 · 计算属性** `private var dashboardSections: some View` — 根据当前状态计算并返回看板。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1576 · 计算属性** `private var toolbar: some View` — 根据当前状态计算并返回`toolbar` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2877` `AppModel.syncDashboardAimes`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:3050` `AppModel.scanDashboardServer`

- **L1637 · 计算属性** `private var dashboardActivityLog: some View` — 根据当前状态计算并返回看板、日志。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:700` `serverFolderChangeGroups`；`macos/OrderDashboardView.swift:863` `dashboardStatusIsInProgress`；`macos/OrderDashboardView.swift:1033` `dashboardAimesActionDetails`；`macos/OrderDashboardView.swift:1054` `dashboardAimesWarningDetails`；`macos/OrderDashboardView.swift:884` `dashboardMessages`；`macos/OrderDashboardView.swift:963` `dashboardVisibleMessages`；`macos/OrderDashboardView.swift:968` `dashboardCurrentOperation`；`macos/OrderDashboardView.swift:982` `dashboardMessageScrollKey`；`macos/OrderDashboardView.swift:1755` `OrderDashboardView.currentOperationRow`；`macos/OrderDashboardView.swift:1460` `OrderDashboardView.traceHost`；`macos/OrderDashboardView.swift:1818` `OrderDashboardView.activityIcon`；`macos/OrderDashboardView.swift:1827` `OrderDashboardView.activityColor`；另有 2 个直接调用

- **L1755 · 方法** `private func currentOperationRow(_ display: DashboardOperationDisplay?) -> some View` — 封装操作、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ display: DashboardOperationDisplay?`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1793` `OrderDashboardView.currentOperationIcon`；`macos/OrderDashboardView.swift:1014` `dashboardMessageSummaryText`；`macos/TravelerAssistant.swift:2678` `AppModel.dashboardElapsedTime`；`macos/TravelerAssistant.swift:1363` `operationDurationText`

- **L1793 · 方法** `private func currentOperationIcon(_ display: DashboardOperationDisplay) -> some View` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ display: DashboardOperationDisplay`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1818` `OrderDashboardView.activityIcon`；`macos/OrderDashboardView.swift:1827` `OrderDashboardView.activityColor`

- **L1811 · 方法** `private func scrollMessagesToBottom(_ proxy: ScrollViewProxy, messages: [DashboardMessage])` — 封装 `scrollMessagesToBottom` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ proxy: ScrollViewProxy`；`messages: [DashboardMessage]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1818 · 方法** `private func activityIcon(_ state: String) -> String` — 封装 `activityIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1827 · 方法** `private func activityColor(_ state: String) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1836 · 计算属性** `private var orderTable: some View` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:45` `OrderDashboardTableLayout`；`macos/OrderDashboardView.swift:1876` `OrderDashboardView.orderTableHeader`；`macos/OrderDashboardView.swift:1913` `OrderDashboardView.orderRow`

- **L1876 · 方法** `private func orderTableHeader(layout: OrderDashboardTableLayout) -> some View` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`layout: OrderDashboardTableLayout`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2121` `OrderDashboardView.tableHeader`

- **L1913 · 方法** `private func orderRow( _ item: OrderDashboardItem, isLastRow: Bool = false, layout: OrderDashboardTableLayout ) -> some View` — 封装订单、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`；`isLastRow: Bool = false`；`layout: OrderDashboardTableLayout`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2127` `OrderDashboardView.tableCell`；`macos/OrderDashboardView.swift:744` `orderInstallationQuickSummaries`；`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/OrderDashboardView.swift:2133` `OrderDashboardView.statusKind`；`macos/OrderDashboardView.swift:711` `orderDashboardStatusHelp`；`macos/OrderDashboardView.swift:760` `OrderDashboardProgressBar`；`macos/TravelerAssistant.swift:1444` `appDisplayTimestamp`；`macos/OrderDashboardView.swift:2097` `OrderDashboardView.toggleExpanded`；`macos/OrderDashboardView.swift:2104` `OrderDashboardView.openOrderDetail`；`macos/OrderDashboardView.swift:2680` `OrderDashboardDetailCard`；`macos/TravelerAssistant.swift:5486` `AppModel.checkSelectedOrderStock`；`macos/TravelerAssistant.swift:3831` `AppModel.loadProductionPreview`；另有 2 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderDetail`；是否真实写入仍取决于分支和参数。

- **L2089 · 方法** `private func prepareSelectedOrder(_ item: OrderDashboardItem)` — 准备并校验订单相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:707` `orderDashboardIsCompleted`；`macos/TravelerAssistant.swift:5272` `AppModel.loadOrderDetailFromDatabase`

- **L2097 · 方法** `private func toggleExpanded(_ item: OrderDashboardItem)` — 封装 `toggleExpanded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:563` `orderDashboardExpandedID`；`macos/OrderDashboardView.swift:2089` `OrderDashboardView.prepareSelectedOrder`

- **L2104 · 方法** `private func openOrderDetail(_ item: OrderDashboardItem)` — 打开订单相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2089` `OrderDashboardView.prepareSelectedOrder`

- **L2109 · 方法** `private func openRequestedOrderIfAvailable()` — 打开订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2121 · 方法** `private func tableHeader(_ title: String, width: CGFloat) -> some View` — 封装 `tableHeader` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`width: CGFloat`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2127 · 方法** `private func tableCell<Content: View>(width: CGFloat, @ViewBuilder content: () -> Content) -> some View` — 封装 `tableCell` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`width: CGFloat`；`@ViewBuilder content: () -> Content`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2133 · 方法** `private func statusKind(_ status: String) -> AppStatusBadge.Kind` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`AppStatusBadge.Kind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2143 · 结构体** `OrderShipmentRequest` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2149 · 结构体** `OrderDashboardMetricsView` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2152 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:553` `orderDashboardShortageCount`；`macos/OrderDashboardView.swift:2167` `OrderDashboardMetricsView.metric`；`macos/TravelerAssistant.swift:2750` `AppModel.startOrderDashboard`

- **L2167 · 方法** `private func metric(_ title: String, _ value: String, _ color: Color) -> some View` — 封装 `metric` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ value: String`；`_ color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2178 · 结构体** `OrderDashboardDetailPage` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2183 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5824` `View.appPageFrame`

- **L2219 · 计算属性** `private var orderIdentityCard: some View` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:5439` `AppModel.generateSelectedOrder`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`

- **L2240 · 计算属性** `private var boardAndEdgeSection: some View` — 根据当前状态计算并返回`boardAndEdgeSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2259` `OrderDashboardDetailPage.materialRow`；`macos/OrderDashboardView.swift:517` `orderDetailPlywoodRows`；`macos/OrderDashboardView.swift:521` `orderDetailPanelRows`

- **L2259 · 方法** `private func materialRow(title: String, rows: [OrderMaterialPreview]) -> some View` — 封装材料、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`rows: [OrderMaterialPreview]`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2357` `OrderDashboardDetailPage.orderDetailCard`；`macos/TravelerAssistant.swift:1109` `orderMaterialDisplayName`

- **L2283 · 计算属性** `@ViewBuilder private var edgeBandingRow: some View` — 根据当前状态计算并返回行数据。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:545` `orderDetailEdgeColors`；`macos/OrderDashboardView.swift:2357` `OrderDashboardDetailPage.orderDetailCard`

- **L2308 · 计算属性** `private var hardwareSection: some View` — 根据当前状态计算并返回五金。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2330` `OrderDashboardDetailPage.hardwareFactorySection`

- **L2330 · 方法** `private func hardwareFactorySection(title: String, rows: [OrderFittingPreview]) -> some View` — 封装五金、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`rows: [OrderFittingPreview]`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2357` `OrderDashboardDetailPage.orderDetailCard`

- **L2357 · 方法** `private func orderDetailCard( name: String, subtitle: String, value: String, panelMaterial: OrderMaterialPreview? = nil ) -> some View` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: String`；`subtitle: String`；`value: String`；`panelMaterial: OrderMaterialPreview? = nil`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2395 · 结构体** `OrderInstallationDraft` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2401 · 函数** `private func orderInstallationDateFormatter() -> DateFormatter` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`DateFormatter`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2410 · 函数** `private func orderInstallationDraftDate(_ value: String) -> Date` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`Date`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2401` `orderInstallationDateFormatter`

- **L2414 · 函数** `private func orderInstallationDraftValue(_ value: Date) -> String` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2401` `orderInstallationDateFormatter`

- **L2418 · 函数** `private func orderInstallationPickerDisplayDate(_ value: Date) -> String` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2427 · 函数** `private func orderInstallationInstallerSuggestions(from orders: [OrderDashboardItem]) -> [String]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from orders: [OrderDashboardItem]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L2440 · 结构体** `OrderAnnotationsSheet` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2444 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2457` `OrderAnnotationsEditor`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`

- **L2457 · 结构体** `OrderAnnotationsEditor` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2468 · 初始化器** `init(model: AppModel, order: OrderDashboardItem)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`order: OrderDashboardItem`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2395` `OrderInstallationDraft`；`macos/OrderDashboardView.swift:2410` `orderInstallationDraftDate`

- **L2481 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2542` `OrderAnnotationsEditor.installationRows`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/OrderDashboardView.swift:2650` `OrderAnnotationsEditor.save`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save`；是否真实写入仍取决于分支和参数。

- **L2542 · 方法** `private func installationRows( title: String, rows: Binding<[OrderInstallationDraft]> ) -> some View` — 封装 `installationRows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`rows: Binding<[OrderInstallationDraft]>`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2395` `OrderInstallationDraft`；`macos/OrderDashboardView.swift:2418` `orderInstallationPickerDisplayDate`；`macos/OrderDashboardView.swift:104` `AppGlassDatePickerCalendar`；`macos/OrderDashboardView.swift:272` `View.appGlassDatePickerPopoverSurface`；`macos/OrderDashboardView.swift:2427` `orderInstallationInstallerSuggestions`；`macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`macos/OrderDashboardView.swift:2414` `orderInstallationDraftValue`；`macos/OrderDashboardView.swift:724` `orderInstallationDisplayDate`

- **L2650 · 方法** `private func save()` — 保存与 `save` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`macos/OrderDashboardView.swift:2414` `orderInstallationDraftValue`；`macos/TravelerAssistant.swift:5360` `AppModel.saveOrderAnnotations`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveOrderAnnotations`；是否真实写入仍取决于分支和参数。

- **L2680 · 结构体** `OrderDashboardDetailCard` — 定义与订单、看板相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2692 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2701 · 计算属性** `private var detailActions: some View` — 根据当前状态计算并返回`detailActions` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:683` `orderDashboardOutboundActionTitle`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5528` `AppModel.calculateSelectedOrderCost`；`macos/OrderDashboardView.swift:676` `orderDashboardHasProducedSelection`；`macos/OrderDashboardView.swift:662` `orderDashboardHasShippedSelection`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderDashboardOutboundActionTitle`, `onOpenScope`, `onOpenProduction`, `onOpenOutbound`；是否真实写入仍取决于分支和参数。

- **L2765 · 计算属性** `private var panelColorsSummary: some View` — 根据当前状态计算并返回`panelColorsSummary` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:364` `orderDashboardPanelMaterials`

- **L2793 · 计算属性** `private var factoriesPanel: some View` — 根据当前状态计算并返回`factoriesPanel` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2799 · 计算属性** `private var factoryTable: some View` — 根据当前状态计算并返回工厂单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2831` `OrderDashboardDetailCard.factoryTableRow`；`macos/OrderDashboardView.swift:645` `toggledOrderFactorySelection`

- **L2831 · 方法** `private func factoryTableRow( isHeader: Bool, factory: OrderFactoryPreview? = nil, dashboardFactory: OrderDashboardFactory? = nil, selected: Bool = false ) -> some View` — 封装工厂单、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`isHeader: Bool`；`factory: OrderFactoryPreview? = nil`；`dashboardFactory: OrderDashboardFactory? = nil`；`selected: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:2872` `OrderDashboardDetailCard.factoryCell`；`macos/OrderDashboardView.swift:690` `orderDashboardOutboundDisplay`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderDashboardOutboundDisplay`；是否真实写入仍取决于分支和参数。

- **L2872 · 方法** `private func factoryCell(_ text: String, width: CGFloat? = nil, status: Bool = false) -> some View` — 封装工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ text: String`；`width: CGFloat? = nil`；`status: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2883 · 结构体** `ProductionSheet` — 定义与生产相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2893 · 枚举** `SheetOperationState` — 定义与操作相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2902 · 计算属性** `private var isProcessing: Bool` — 根据当前状态计算并返回`isProcessing` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2906 · 计算属性** `private var selectedQuantityCount: Int` — 选择数量相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`

- **L2910 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:168` `sortedProductionMaterialDrafts`；`macos/TravelerAssistant.swift:119` `productionMaterialTypeDisplayName`；`macos/TravelerAssistant.swift:128` `productionMaterialName`；`macos/OrderDashboardView.swift:3058` `ProductionSheet.submitProduction`；`macos/TravelerAssistant.swift:3831` `AppModel.loadProductionPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `onClose`；是否真实写入仍取决于分支和参数。

- **L3009 · 计算属性** `private var productionOperationBanner: some View` — 根据当前状态计算并返回生产、操作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3058 · 方法** `private func submitProduction()` — 封装生产相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3869` `AppModel.prepareProduction`；`macos/TravelerAssistant.swift:3886` `AppModel.startDirectProduction`

- **L3097 · 结构体** `OrderShipmentConfirmationSheet` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3104 · 计算属性** `private var fittings: [OrderFittingPreview]` — 根据当前状态计算并返回`fittings` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderFittingPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3108 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`

- **L3172 · 结构体** `OutboundScopeSheet` — 定义与出库、范围相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3186 · 计算属性** `private var incomingProcessing: Bool` — 根据当前状态计算并返回`incomingProcessing` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3187 · 计算属性** `private var noOutboundDecision: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3190 · 计算属性** `private var hardwareAvailable: Bool` — 根据当前状态计算并返回五金。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3192 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:3293` `OutboundScopeSheet.scopeSegment`；`macos/TravelerAssistant.swift:4106` `AppModel.saveOutboundScope`；`macos/OrderDashboardView.swift:3267` `OutboundScopeSheet.loadSavedScopeIfNeeded`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveOutboundScope`；是否真实写入仍取决于分支和参数。

- **L3267 · 方法** `private func loadSavedScopeIfNeeded()` — 读取范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4084` `AppModel.loadOutboundScope`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `loadOutboundScope`；是否真实写入仍取决于分支和参数。

- **L3293 · 方法** `private func scopeSegment(_ title: String, value: String, disabled: Bool = false) -> some View` — 封装范围相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`value: String`；`disabled: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3309 · 结构体** `FolderManualHandlingSheet` — 定义与文件夹相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3316 · 计算属性** `private var references: [String]` — 根据当前状态计算并返回`references` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `CharacterSet`；是否真实写入仍取决于分支和参数。

- **L3322 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3356` `AppModel.markTemporaryFolderManual`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`

- **L3358 · 结构体** `PendingCenterSheet` — 定义 `PendingCenterSheet` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3369 · 方法** `private func confirm(_ title: String, action: @escaping () -> Void)` — 封装 `confirm` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`action: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3375 · 计算属性** `private var items: [PendingCenterItem]` — 根据当前状态计算并返回`items` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3376 · 计算属性** `private var visibleItems: [PendingCenterItem]` — 根据当前状态计算并返回`visibleItems` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3383 · 计算属性** `private var selectedItem: PendingCenterItem?` — 选择项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`PendingCenterItem?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3387 · 方法** `private func reconcileSelection()` — 对账并重算与 `reconcileSelection` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3395 · 方法** `private func preview(_ item: PendingCenterItem)` — 预览预览相关数据或步骤。
  - 输入：`_ item: PendingCenterItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3312` `AppModel.processSelectedServerFolder`；`macos/TravelerAssistant.swift:69` `inventoryMappingSourceFolderPath`

- **L3404 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/OrderDashboardView.swift:3555` `PendingCenterSheet.queueRow`；`macos/OrderDashboardView.swift:3534` `PendingCenterSheet.detailTitle`；`macos/OrderDashboardView.swift:3543` `PendingCenterSheet.detailExplanation`；`macos/TravelerAssistant.swift:1713` `AppModel.pendingMappingResumeMessage`；`macos/OrderDashboardView.swift:3581` `PendingCenterSheet.pendingItemDetails`；`macos/TravelerAssistant.swift:2947` `AppModel.ignoreSelectedAimesFactories`；`macos/OrderDashboardView.swift:3395` `PendingCenterSheet.preview`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`；`macos/OrderDashboardView.swift:3309` `FolderManualHandlingSheet`；`macos/OrderDashboardView.swift:3387` `PendingCenterSheet.reconcileSelection`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L3528 · 计算属性** `private var postponeButton: some View` — 根据当前状态计算并返回`postponeButton` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3534 · 方法** `private func detailTitle(_ item: PendingCenterItem) -> String` — 封装 `detailTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: PendingCenterItem`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3543 · 方法** `private func detailExplanation(_ item: PendingCenterItem) -> String` — 封装 `detailExplanation` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: PendingCenterItem`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3555 · 方法** `private func queueRow(_ item: PendingCenterItem) -> some View` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: PendingCenterItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1444` `appDisplayTimestamp`

- **L3581 · 方法** `private func pendingItemDetails(_ item: PendingCenterItem) -> some View` — 封装项目相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: PendingCenterItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:3804` `PendingCenterSheet.changeTimeLabel`；`macos/OrderDashboardView.swift:3774` `PendingCenterSheet.changeTypeName`；`macos/OrderDashboardView.swift:3634` `PendingCenterSheet.issueDetails`；`macos/OrderDashboardView.swift:3689` `PendingCenterSheet.aimesDetails`；`macos/OrderDashboardView.swift:3720` `PendingCenterSheet.aimesFormatWarningDetails`

- **L3634 · 方法** `private func issueDetails(_ issue: CurrentIssue) -> some View` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:278` `currentIssueRequiresInventoryMapping`；`macos/TravelerAssistant.swift:5612` `AppModel.openDashboardLocation`；`macos/TravelerAssistant.swift:2844` `AppModel.autoResolveCurrentIssue`；`macos/TravelerAssistant.swift:2859` `AppModel.resolveCurrentIssue`；`macos/TravelerAssistant.swift:3431` `AppModel.requestInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openDashboardLocation`；是否真实写入仍取决于分支和参数。

- **L3689 · 方法** `private func aimesDetails(_ item: AimesReviewItem) -> some View` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2937` `AppModel.toggleAimesReviewSelection`；`macos/TravelerAssistant.swift:2993` `AppModel.assignAimesFactoryToSuggestedOrder`

- **L3720 · 方法** `private func aimesFormatWarningDetails(_ item: AimesReviewItem) -> some View` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2937` `AppModel.toggleAimesReviewSelection`；`macos/TravelerAssistant.swift:2998` `AppModel.assignAimesFactoryToOrder`

- **L3774 · 方法** `private func changeTypeName(_ type: String) -> String` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3784 · 方法** `private func changeIcon(_ type: String) -> String` — 封装 `changeIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3794 · 方法** `private func changeColor(_ type: String) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3804 · 方法** `private func changeTimeLabel(_ change: ServerChangePreview) -> String` — 封装时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ change: ServerChangePreview`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1444` `appDisplayTimestamp`

- **L3814 · 结构体** `OrderCostSheet` — 定义与订单、成本相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3821 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5528` `AppModel.calculateSelectedOrderCost`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/OrderDashboardView.swift:3914` `OrderCostSheet.costCard`；`macos/OrderDashboardView.swift:3941` `OrderCostSheet.costLine`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`

- **L3914 · 方法** `private func costCard(_ title: String, value: String, warning: Bool) -> some View` — 封装成本相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`value: String`；`warning: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3926 · 计算属性** `private var costLineHeader: some View` — 根据当前状态计算并返回成本。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3941 · 方法** `private func costLine(_ row: OrderCostLine) -> some View` — 封装成本相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderCostLine`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3973 · 计算属性** `private var orderCostSourceTotals: [OrderCostFactoryTotal]` — 根据当前状态计算并返回订单、成本、来源。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[OrderCostFactoryTotal]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:3988` `OrderCostSheet.sourceTotal`

- **L3988 · 方法** `private func sourceTotal( id: String, title: String, categories: [String] ) -> OrderCostFactoryTotal` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`id: String`；`title: String`；`categories: [String]`
  - 返回：`OrderCostFactoryTotal`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1223` `OrderCostFactoryTotal`

- **L4003 · 结构体** `ServerProcessingOptionsSheet` — 定义与Server 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4006 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:3312` `AppModel.processSelectedServerFolder`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`

- **L4045 · 结构体** `CurrentIssuesSheet` — 定义 `CurrentIssuesSheet` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4049 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:5612` `AppModel.openDashboardLocation`；`macos/TravelerAssistant.swift:2844` `AppModel.autoResolveCurrentIssue`；`macos/TravelerAssistant.swift:2859` `AppModel.resolveCurrentIssue`；`macos/OrderDashboardView.swift:278` `currentIssueRequiresInventoryMapping`；`macos/TravelerAssistant.swift:3431` `AppModel.requestInventoryMapping`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openDashboardLocation`；是否真实写入仍取决于分支和参数。

- **L4141 · 结构体** `ServerChangesSheet` — 定义与Server 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4145 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:700` `serverFolderChangeGroups`；`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:3093` `AppModel.clearServerFolderSelection`；`macos/TravelerAssistant.swift:3081` `AppModel.toggleServerFolderSelection`；`macos/TravelerAssistant.swift:1057` `serverChangeTypeName`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:3098` `AppModel.processPendingServerChanges`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`；`macos/OrderDashboardView.swift:3309` `FolderManualHandlingSheet`

- **L4258 · 方法** `private func changeIcon(_ type: String) -> String` — 封装 `changeIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4266 · 方法** `private func changeColor(_ type: String) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4275 · 结构体** `HardwareSourceSelectionSheet` — 定义与五金、来源相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4276 · 计算属性** `@ObservedObject var model: AppModel var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`AppModel var body: some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4307` `HardwareSourceSelectionSheet.sourceCard`；`macos/TravelerAssistant.swift:2575` `AppModel.confirmHardwareSourceSelection`

- **L4302 · 方法** `private func formatQuantity(_ value: Double) -> String` — 格式化数量相关数据或步骤。
  - 输入：`_ value: Double`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1411` `Double.rounded`

- **L4307 · 方法** `private func sourceCard(_ candidate: HardwareSourceCandidate, factoryOrder: String) -> some View` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ candidate: HardwareSourceCandidate`；`factoryOrder: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4366 · 结构体** `ServerWriteConfirmationSheet` — 定义与Server 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4367 · 计算属性** `@ObservedObject var model: AppModel @State private var mappingTarget: PendingInventoryMappingTarget? @State private var ignoreTarget: PendingInventoryMappingTarget? @State private var skippedHardwareOrderIDs: Set<String> = [] @State private var showWriteConfirmation = false private var canConfirmWrite: Bool` — 根据当前状态计算并返回`canConfirmWrite` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`AppModel @State private var mappingTarget: PendingInventoryMappingTarget? @State private var ignoreTarget: PendingInventoryMappingTarget? @State private var skippedHardwareOrderIDs: Set<String> = [] @State private var showWriteConfirmation = false private var canConfirmWrite: Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4376 · 计算属性** `private var orders: [ServerWriteOrderPreview]` — 根据当前状态计算并返回`orders` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[ServerWriteOrderPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4377 · 计算属性** `private var activeHardwareRequirements: [ServerHardwareMappingRequirement]` — 根据当前状态计算并返回五金。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[ServerHardwareMappingRequirement]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4384 · 计算属性** `private var invalidOrderValidations: [ServerWriteOrderPreview]` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[ServerWriteOrderPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4388 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/OrderDashboardView.swift:4608` `ServerWriteConfirmationSheet.orderPreviewCard`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`；`macos/TravelerAssistant.swift:3210` `AppModel.confirmServerMaterialPreview`；`macos/TravelerAssistant.swift:6799` `InventoryMappingSheet`；`macos/TravelerAssistant.swift:4465` `AppModel.saveServerHardwareMapping`；`macos/TravelerAssistant.swift:6983` `PendingInventoryIgnoreSheet`；`macos/TravelerAssistant.swift:4480` `AppModel.saveServerHardwareIgnoredMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveServerHardwareMapping`, `saveServerHardwareIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L4546 · 计算属性** `@ViewBuilder private var hardwareMappingSection: some View` — 根据当前状态计算并返回五金、映射。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6885` `PendingInventoryMappingTarget`

- **L4603 · 方法** `private func formatQuantity(_ value: Double) -> String` — 格式化数量相关数据或步骤。
  - 输入：`_ value: Double`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1411` `Double.rounded`

- **L4608 · 方法** `private func orderPreviewCard(_ order: ServerWriteOrderPreview) -> some View` — 封装订单、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ order: ServerWriteOrderPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/OrderDashboardView.swift:4746` `ServerWriteConfirmationSheet.cutToSizeHardwareChoice`；`macos/OrderDashboardView.swift:310` `sortedServerWriteMaterialChanges`；`macos/OrderDashboardView.swift:4806` `ServerWriteConfirmationSheet.materialChangeRow`；`macos/OrderDashboardView.swift:4850` `ServerWriteConfirmationSheet.hardwareChangeHeaderRow`；`macos/OrderDashboardView.swift:4824` `ServerWriteConfirmationSheet.hardwareChangeRow`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sortedServerWriteMaterialChanges`；是否真实写入仍取决于分支和参数。

- **L4746 · 方法** `private func cutToSizeHardwareChoice(for order: ServerWriteOrderPreview) -> some View` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`for order: ServerWriteOrderPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L4806 · 方法** `private func materialChangeRow(_ material: ServerWriteMaterialChange) -> some View` — 封装材料、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ServerWriteMaterialChange`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4824 · 方法** `private func hardwareChangeRow(_ hardware: ServerWriteHardwareChange) -> some View` — 封装五金、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ hardware: ServerWriteHardwareChange`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:4897` `serverHardwareUnitText`

- **L4850 · 方法** `private func hardwareChangeHeaderRow() -> some View` — 封装五金、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4863 · 方法** `private func materialPreviewRow(_ material: ServerWriteMaterialPreview) -> some View` — 封装材料、预览、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ServerWriteMaterialPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4897 · 函数** `func serverHardwareUnitText(_ unit: String) -> String` — 封装Server 数据、五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ unit: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4902 · 结构体** `ServerWriteSelectionRow` — 定义与Server 数据、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4908 · 结构体** `FactoryStockComparisonSheet` — 定义与工厂单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4912 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/OrderDashboardView.swift:4972` `FactoryStockComparisonSheet.stockRow`；`macos/TravelerAssistant.swift:5486` `AppModel.checkSelectedOrderStock`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`

- **L4958 · 计算属性** `private var stockHeader: some View` — 根据当前状态计算并返回`stockHeader` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4972 · 方法** `private func stockRow(_ row: OrderStockPreview) -> some View` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderStockPreview`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4995 · 结构体** `AimesHistorySheet` — 定义与AIMES 数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5003 · 方法** `private func confirm(_ title: String, action: @escaping () -> Void)` — 封装 `confirm` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`action: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5009 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`

- **L5040 · 计算属性** `@ViewBuilder private var aimesHistorySection: some View` — 根据当前状态计算并返回AIMES 数据。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:5088` `AimesHistorySheet.aimesHistoryRow`；`macos/TravelerAssistant.swift:3030` `AppModel.restoreAimesFactoryAssignment`；`macos/TravelerAssistant.swift:2973` `AppModel.restoreAimesFactory`

- **L5088 · 方法** `private func aimesHistoryRow( _ item: AimesReviewItem, title: String, action: @escaping () -> Void, actionTitle: @escaping () -> String ) -> some View` — 封装AIMES 数据、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`title: String`；`action: @escaping () -> Void`；`actionTitle: @escaping () -> String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5836` `View.appActionButton`

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
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`；`macos/TravelerAssistant.swift:1109` `orderMaterialDisplayName`；`macos/TravelerAssistant.swift:1083` `OrderMaterialPreview`

- **L151 · 函数** `private func productionMaterialTypeRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L160 · 函数** `private func productionMaterialPlywoodRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`

- **L168 · 函数** `func sortedProductionMaterialDrafts(_ materials: [ProductionMaterialDraft]) -> [ProductionMaterialDraft]` — 排序生产、材料相关数据或步骤。
  - 输入：`_ materials: [ProductionMaterialDraft]`
  - 返回：`[ProductionMaterialDraft]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:151` `productionMaterialTypeRank`；`macos/TravelerAssistant.swift:160` `productionMaterialPlywoodRank`；`macos/TravelerAssistant.swift:1410` `Double`；`macos/TravelerAssistant.swift:128` `productionMaterialName`

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

- **L269 · 初始化器** `init( id: String, changeType: String, kind: String, orderId: String, sourceFolder: String, path: String, oldPath: String = "", message: String, manualOnly: Bool, handlingMode: String = "", referenceOrderIDs: [String] = [], eventTime: String )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`changeType: String`；`kind: String`；`orderId: String`；`sourceFolder: String`；`path: String`；`oldPath: String = ""`；`message: String`；`manualOnly: Bool`；`handlingMode: String = ""`；`referenceOrderIDs: [String] = []`；`eventTime: String`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L298 · 结构体** `ServerWriteMaterialPreview` — 定义与Server 数据、材料、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L310 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L329 · 结构体** `ServerWriteHardwarePreview` — 定义与Server 数据、五金、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L338 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L352 · 结构体** `ServerWriteMaterialChange` — 定义与Server 数据、材料相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L364 · 初始化器** `init( id: String, changeType: String, materialType: String, color: String, thickness: String, edge: String, unit: String, oldQuantity: Double, newQuantity: Double, delta: Double )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`changeType: String`；`materialType: String`；`color: String`；`thickness: String`；`edge: String`；`unit: String`；`oldQuantity: Double`；`newQuantity: Double`；`delta: Double`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L388 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L403 · 方法** `static func aggregated(_ changes: [ServerWriteMaterialChange]) -> [ServerWriteMaterialChange]` — 封装 `aggregated` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerWriteMaterialChange]`
  - 返回：`[ServerWriteMaterialChange]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:352` `ServerWriteMaterialChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`；是否真实写入仍取决于分支和参数。

- **L432 · 结构体** `ServerWriteHardwareChange` — 定义与Server 数据、五金相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L445 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L464 · 结构体** `HardwareSourceItem` — 定义与五金、来源、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L471 · 初始化器** `init(_ value: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`_ value: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L480 · 结构体** `HardwareSourceCandidate` — 定义与五金、来源相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L485 · 初始化器** `init?(_ value: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`_ value: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L494 · 结构体** `HardwareSourceConflict` — 定义与五金、来源相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L497 · 初始化器** `init?(_ value: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`_ value: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L504 · 结构体** `ServerHardwareMappingRequirement` — 定义与Server 数据、五金、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L514 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L528 · 结构体** `ServerWriteFactoryPreview` — 定义与Server 数据、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L543 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:329` `ServerWriteHardwarePreview`；`macos/TravelerAssistant.swift:432` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteHardwarePreview`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L566 · 结构体** `ServerWriteOrderPreview` — 定义与Server 数据、订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L579 · 计算属性** `var existingHardwareChanges: [ServerWriteHardwareChange]` — 根据当前状态计算并返回五金。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[ServerWriteHardwareChange]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L584 · 初始化器** `init( id: String, orderID: String, orderType: String, sourceFolder: String, validationStatus: String, validationMessage: String, materials: [ServerWriteMaterialPreview], materialChanges: [ServerWriteMaterialChange], factories: [ServerWriteFactoryPreview], excludedFactories: [ServerWriteFactoryPreview], hardwareChanges: [ServerWriteHardwareChange] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`orderID: String`；`orderType: String`；`sourceFolder: String`；`validationStatus: String`；`validationMessage: String`；`materials: [ServerWriteMaterialPreview]`；`materialChanges: [ServerWriteMaterialChange]`；`factories: [ServerWriteFactoryPreview]`；`excludedFactories: [ServerWriteFactoryPreview]`；`hardwareChanges: [ServerWriteHardwareChange]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L610 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:298` `ServerWriteMaterialPreview`；`macos/TravelerAssistant.swift:403` `ServerWriteMaterialChange.aggregated`；`macos/TravelerAssistant.swift:352` `ServerWriteMaterialChange`；`macos/TravelerAssistant.swift:432` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`, `ServerWriteMaterialChange`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L635 · 结构体** `ServerWritePreview` — 定义与Server 数据、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L642 · 初始化器** `init(payload: [String: Any], sourceFolders: [String], materials: [ServerWriteMaterialPreview], orders: [ServerWriteOrderPreview], hardwareMappingRequirements: [ServerHardwareMappingRequirement] = [])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`payload: [String: Any]`；`sourceFolders: [String]`；`materials: [ServerWriteMaterialPreview]`；`orders: [ServerWriteOrderPreview]`；`hardwareMappingRequirements: [ServerHardwareMappingRequirement] = []`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L650 · 初始化器** `init?(object: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`object: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:298` `ServerWriteMaterialPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`；是否真实写入仍取决于分支和参数。

- **L667 · 结构体** `ServerFolderChangeGroup` — 定义与Server 数据、文件夹相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L675 · 计算属性** `var independentManual: Bool` — 根据当前状态计算并返回`independentManual` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L679 · 计算属性** `var referenceOrderIDs: [String]` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L681 · 计算属性** `var requiresManualReview: Bool` — 根据当前状态计算并返回`requiresManualReview` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L686 · 结构体** `PendingCenterItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L700 · 函数** `func serverFolderChangeGroups(_ changes: [ServerChangePreview]) -> [ServerFolderChangeGroup]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`
  - 返回：`[ServerFolderChangeGroup]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:667` `ServerFolderChangeGroup`

- **L719 · 函数** `func buildPendingCenterItems( serverChanges: [ServerChangePreview], currentIssues: [CurrentIssue], aimesReviews: [AimesReviewItem], aimesFormatWarnings: [AimesReviewItem] = [] ) -> [PendingCenterItem]` — 构建与 `buildPendingCenterItems` 对应的数据或步骤。
  - 输入：`serverChanges: [ServerChangePreview]`；`currentIssues: [CurrentIssue]`；`aimesReviews: [AimesReviewItem]`；`aimesFormatWarnings: [AimesReviewItem] = []`
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:700` `serverFolderChangeGroups`；`macos/TravelerAssistant.swift:730` `belongs`；`macos/OrderDashboardView.swift:278` `currentIssueRequiresInventoryMapping`；`macos/TravelerAssistant.swift:686` `PendingCenterItem`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `Set`；是否真实写入仍取决于分支和参数。

- **L730 · 函数** `func belongs(_ issue: CurrentIssue, to group: ServerFolderChangeGroup) -> Bool` — 封装 `belongs` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`；`to group: ServerFolderChangeGroup`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L831 · 结构体** `CurrentIssue` — 定义与待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L842 · 结构体** `AimesReviewItem` — 定义与AIMES 数据、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L854 · 函数** `func aimesReviewItems(_ object: [String: Any], key: String) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`key: String`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:842` `AimesReviewItem`

- **L871 · 函数** `func aimesReviewItemsFromWarnings(_ warnings: [[String: Any]]) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ warnings: [[String: Any]]`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:842` `AimesReviewItem`

- **L890 · 结构体** `DashboardAimesStatusUpdate` — 定义与看板、AIMES 数据、状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L895 · 函数** `func dashboardAimesStatusUpdate( attempted: Bool, succeeded: Bool, skippedToday: Bool, changed: Bool, count: Int, issueCount: Int, warningCount: Int, error: String ) -> DashboardAimesStatusUpdate` — 封装看板、AIMES 数据、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`attempted: Bool`；`succeeded: Bool`；`skippedToday: Bool`；`changed: Bool`；`count: Int`；`issueCount: Int`；`warningCount: Int`；`error: String`
  - 返回：`DashboardAimesStatusUpdate`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:890` `DashboardAimesStatusUpdate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `DashboardAimesStatusUpdate`；是否真实写入仍取决于分支和参数。

- **L948 · 函数** `func dashboardActivitySteps( _ object: [String: Any], includeChanges: Bool = true, sessionStartedAt: Date? = nil ) -> [InventoryStep]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`；`sessionStartedAt: Date? = nil`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1448` `dashboardBusinessDate`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1323` `InventoryStep`

- **L1008 · 函数** `func serverChangePreviews(_ rows: [[String: Any]]) -> [ServerChangePreview]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [[String: Any]]`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:255` `ServerChangePreview`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L1031 · 函数** `func serverChangesExcludingFolder( _ changes: [ServerChangePreview], folderPath: String ) -> [ServerChangePreview]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`；`folderPath: String`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1038` `serverChangesExcludingFolders`

- **L1038 · 函数** `func serverChangesExcludingFolders( _ changes: [ServerChangePreview], folderPaths: [String] ) -> [ServerChangePreview]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`；`folderPaths: [String]`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1057 · 函数** `func serverChangeTypeName(_ type: String) -> String` — 封装Server 数据、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1067 · 结构体** `OrderPreviewIssue` — 定义与订单、预览、待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1073 · 函数** `func orderPreviewIssues(_ object: [String: Any]) -> [OrderPreviewIssue]` — 封装订单、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`[OrderPreviewIssue]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1067` `OrderPreviewIssue`

- **L1083 · 结构体** `OrderMaterialPreview` — 定义与订单、材料、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1092 · 初始化器** `init( kind: String, thickness: Double, color: String, quantity: Double, productCode: String = "", brand: String = "" )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`kind: String`；`thickness: Double`；`color: String`；`quantity: Double`；`productCode: String = ""`；`brand: String = ""`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1109 · 函数** `func orderMaterialDisplayName(_ row: OrderMaterialPreview) -> String` — 封装订单、材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderMaterialPreview`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1120 · 函数** `func orderedMaterialRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`[OrderMaterialPreview]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:539` `orderDetailPanelThicknessRank`

- **L1151 · 函数** `func orderedEdgeColors(_ colors: [String], matching panels: [OrderMaterialPreview]) -> [String]` — 封装 `orderedEdgeColors` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ colors: [String]`；`matching panels: [OrderMaterialPreview]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1164 · 函数** `func panelColorsNeedingThicknessWarning(_ rows: [OrderMaterialPreview]) -> Set<String>` — 封装 `panelColorsNeedingThicknessWarning` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`Set<String>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L1176 · 结构体** `OrderFactoryPreview` — 定义与订单、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1182 · 结构体** `OrderFittingPreview` — 定义与订单、五金、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1196 · 结构体** `OrderStockPreview` — 定义与订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1208 · 结构体** `OrderCostLine` — 定义与订单、成本相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1223 · 结构体** `OrderCostFactoryTotal` — 定义与订单、成本、工厂单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1230 · 结构体** `InventoryTraveler` — 定义与库存、Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1240 · 函数** `func groupInventoryTravelersByNewest(_ travelers: [InventoryTraveler]) -> [(String, [InventoryTraveler])]` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ travelers: [InventoryTraveler]`
  - 返回：`[(String, [InventoryTraveler])]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1257 · 结构体** `InventoryPreviewRow` — 定义与库存、预览、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1268 · 函数** `func inventoryPreviewCategoryRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1277 · 函数** `func inventoryPreviewPlywoodRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1285 · 函数** `func sortedInventoryPreviewRows(_ rows: [InventoryPreviewRow]) -> [InventoryPreviewRow]` — 排序库存、预览相关数据或步骤。
  - 输入：`_ rows: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1268` `inventoryPreviewCategoryRank`；`macos/TravelerAssistant.swift:1277` `inventoryPreviewPlywoodRank`

- **L1301 · 结构体** `InventoryProductCandidate` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1310 · 结构体** `InventoryIgnoredMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1316 · 结构体** `InventoryManualMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1323 · 结构体** `InventoryStep` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1336 · 初始化器** `init( id: UUID = UUID(), time: String, title: String, detail: String, state: String, paths: [String] = [], operationDetails: [String] = [], contextDetails: [String] = [], startedAt: Date? = nil, duration: TimeInterval? = nil, sourceKey: String? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`time: String`；`title: String`；`detail: String`；`state: String`；`paths: [String] = []`；`operationDetails: [String] = []`；`contextDetails: [String] = []`；`startedAt: Date? = nil`；`duration: TimeInterval? = nil`；`sourceKey: String? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1363 · 函数** `func operationDurationText(_ duration: TimeInterval) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ duration: TimeInterval`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1411` `Double.rounded`

- **L1368 · 函数** `func inventoryFailureNeedsVerification(_ message: String) -> Bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1383 · 结构体** `DashboardOperationDuration` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1388 · 初始化器** `init(id: String? = nil, label: String, duration: TimeInterval)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String? = nil`；`label: String`；`duration: TimeInterval`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1395 · 函数** `func dashboardFlatOperationDurations(_ stages: [[String: Any]]) -> [DashboardOperationDuration]` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stages: [[String: Any]]`
  - 返回：`[DashboardOperationDuration]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1383` `DashboardOperationDuration`

- **L1405 · 结构体** `DashboardOperationStart` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1410 · 扩展** `Double` — 定义 `Double` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1411 · 方法** `func rounded(toPlaces places: Int) -> Double` — 封装 `rounded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`toPlaces places: Int`
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`

- **L1417 · 函数** `func dashboardClockTime(_ date: Date = Date()) -> String` — 封装看板、时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date = Date()`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1421 · 函数** `func dashboardInventoryProgressText(_ message: String) -> String` — 封装看板、库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1444 · 函数** `func appDisplayTimestamp(_ value: String) -> String` — 封装 `appDisplayTimestamp` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1448 · 函数** `func dashboardBusinessDate(_ value: String) -> Date?` — 封装看板、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`Date?`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:288` `ISO8601DateFormatter`

- **L1466 · 函数** `func dashboardTimestamp(_ value: String, isInSameMonthAs reference: Date, calendar: Calendar = .current) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`；`isInSameMonthAs reference: Date`；`calendar: Calendar = .current`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1448` `dashboardBusinessDate`

- **L1471 · 函数** `func updatingLatestRunningStep(_ steps: [InventoryStep], detail: String) -> [InventoryStep]?` — 封装 `updatingLatestRunningStep` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`detail: String`
  - 返回：`[InventoryStep]?`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1323` `InventoryStep`

- **L1490 · 函数** `func appendingInventoryProgressStep(_ steps: [InventoryStep], message: String) -> [InventoryStep]` — 封装库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`message: String`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1323` `InventoryStep`

- **L1519 · 函数** `func orderUpdateActionReady(existingTravelerPath: String, selectedOrderPath: String, selectedOrderId: String) -> Bool` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`；`selectedOrderPath: String`；`selectedOrderId: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1523 · 函数** `func orderTravelerOpenActionReady(existingTravelerPath: String) -> Bool` — 封装订单、Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1528 · 结构体** `TodoItem` — 定义与待办、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1535 · 初始化器** `init( id: UUID = UUID(), content: String, startedAt: Date = Date(), deadline: Date?, completedAt: Date? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`content: String`；`startedAt: Date = Date()`；`deadline: Date?`；`completedAt: Date? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1550 · 结构体** `AssistantTaskItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1556 · 类** `ResidentOrderServiceClient` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1566 · 初始化器** `init(onProgress: @escaping (String) -> Void)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`onProgress: @escaping (String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1570 · 方法** `func start(command: URL, environment: [String: String]) throws` — 启动与 `start` 对应的数据或步骤。
  - 输入：`command: URL`；`environment: [String: String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run`；是否真实写入仍取决于分支和参数。

- **L1590 · 方法** `func request(id: String, arguments: [String], inputData: Data?) throws -> Data` — 封装 `request` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`id: String`；`arguments: [String]`；`inputData: Data?`
  - 返回：`Data`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`；是否真实写入仍取决于分支和参数。

- **L1622 · 方法** `func stop()` — 封装 `stop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `closeFile`；是否真实写入仍取决于分支和参数。

- **L1642 · 类** `AppModel` — 定义 `AppModel` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1697 · 枚举** `PendingMappingResumeAction` — 定义与映射相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1702 · 结构体** `PendingMappingResumeState` — 定义与映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1709 · 方法** `func pendingMappingResumeState(for item: PendingCenterItem) -> PendingMappingResumeState?` — 封装映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`for item: PendingCenterItem`
  - 返回：`PendingMappingResumeState?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1713 · 方法** `func pendingMappingResumeMessage(for item: PendingCenterItem) -> String` — 封装映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`for item: PendingCenterItem`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1709` `AppModel.pendingMappingResumeState`

- **L1717 · 计算属性** `var activePendingMappingResumeState: PendingMappingResumeState?` — 根据当前状态计算并返回映射。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`PendingMappingResumeState?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1723 · 结构体** `PendingResumeContext` — 定义 `PendingResumeContext` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1864 · 方法** `private func appendNewDashboardActivityToSession(oldValue: [InventoryStep])` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`oldValue: [InventoryStep]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:804` `DashboardMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `insert`；是否真实写入仍取决于分支和参数。

- **L1889 · 计算属性** `var dashboardMessageOperationDetails: [String: [String]]` — 根据当前状态计算并返回看板、操作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[String: [String]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1901 · 方法** `private func dashboardSessionManualPaths(for source: String) -> [String]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`for source: String`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1914 · 方法** `private func dashboardSessionContextDetails(for source: String, status: String? = nil) -> [String]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`for source: String`；`status: String? = nil`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:1033` `dashboardAimesActionDetails`；`macos/OrderDashboardView.swift:1054` `dashboardAimesWarningDetails`；`macos/TravelerAssistant.swift:700` `serverFolderChangeGroups`

- **L1938 · 方法** `private func recordDashboardStatus(_ source: String, status: String, time: String)` — 记录记录、看板、状态相关数据或步骤。
  - 输入：`_ source: String`；`status: String`；`time: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1914` `AppModel.dashboardSessionContextDetails`；`macos/OrderDashboardView.swift:804` `DashboardMessage`；`macos/OrderDashboardView.swift:856` `dashboardMessageDetail`；`macos/OrderDashboardView.swift:849` `dashboardMessageState`；`macos/TravelerAssistant.swift:1901` `AppModel.dashboardSessionManualPaths`

- **L1978 · 方法** `private func recordDashboardStageCompletion( _ source: String, stage: String, label: String, duration: TimeInterval, time: String )` — 记录记录、看板相关数据或步骤。
  - 输入：`_ source: String`；`stage: String`；`label: String`；`duration: TimeInterval`；`time: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:804` `DashboardMessage`；`macos/TravelerAssistant.swift:1383` `DashboardOperationDuration`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L2015 · 计算属性** `var pendingCenterItems: [PendingCenterItem]` — 根据当前状态计算并返回`pendingCenterItems` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:719` `buildPendingCenterItems`

- **L2024 · 计算属性** `var hasAimesHistory: Bool` — 根据当前状态计算并返回AIMES 数据。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2028 · 计算属性** `var orderPreviewReady: Bool` — 根据当前状态计算并返回订单、预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2032 · 计算属性** `var orderCanGenerateTraveler: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2036 · 计算属性** `var orderTravelerOpenReady: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1523` `orderTravelerOpenActionReady`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L2040 · 计算属性** `var activeOwnedSourceRoot: String` — 根据当前状态计算并返回来源。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2044 · 计算属性** `var activeCutToSizeRoot: String` — 根据当前状态计算并返回`activeCutToSizeRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2050 · 计算属性** `var activeOrderRoot: String` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2054 · 计算属性** `var activeBackupRoot: String` — 根据当前状态计算并返回备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2058 · 计算属性** `var databaseBackupRoot: String` — 根据当前状态计算并返回数据库、备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2062 · 初始化器** `init()` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2214` `AppModel.loadSettings`；`macos/OperationLog.swift:186` `OperationLogWriter.setEnabled`；`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:2133` `AppModel.loadTodoItems`；`macos/AssistantView.swift:481` `AppModel.loadAssistantUsage`；`macos/TravelerAssistant.swift:2075` `AppModel.startResidentOrderService`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setEnabled`, `record`；是否真实写入仍取决于分支和参数。

- **L2075 · 方法** `private func startResidentOrderService()` — 启动订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4901` `AppModel.consumeOrderLogChunk`；`macos/TravelerAssistant.swift:1570` `ResidentOrderServiceClient.start`；`macos/TravelerAssistant.swift:2349` `AppModel.environmentForOperation`；`macos/TravelerAssistant.swift:2320` `AppModel.newOperationID`；`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2096 · 方法** `func checkBackupReminder()` — 检查备份相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2105 · 方法** `func performBackup()` — 执行手动/计划备份并把结果映射为 App 状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2123 · 计算属性** `private var settingsURL: URL` — 设置设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2128 · 计算属性** `var todoDataURL: URL` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2133 · 方法** `func loadTodoItems()` — 读取待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L2148 · 方法** `func addTodo(content: String, deadline: Date?)` — 新增待办相关数据或步骤。
  - 输入：`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:1528` `TodoItem`；`macos/TravelerAssistant.swift:2184` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L2159 · 方法** `func updateTodo(_ item: TodoItem, content: String, deadline: Date?)` — 更新待办相关数据或步骤。
  - 输入：`_ item: TodoItem`；`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2184` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L2171 · 方法** `func toggleTodoCompletion(_ item: TodoItem)` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2184` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L2178 · 方法** `func deleteTodo(_ item: TodoItem)` — 删除待办相关数据或步骤。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2184` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L2184 · 方法** `private func saveTodoItems()` — 保存待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L2214 · 方法** `func loadSettings() -> Bool` — 读取设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2233 · 方法** `func saveSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L2262 · 计算属性** `var operationLogURL: URL` — 根据当前状态计算并返回操作、日志。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2267 · 方法** `func setOperationLogEnabled(_ enabled: Bool)` — 设置操作、日志相关数据或步骤。
  - 输入：`_ enabled: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/OperationLog.swift:186` `OperationLogWriter.setEnabled`；`macos/TravelerAssistant.swift:2233` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`, `setEnabled`, `saveSettings`；是否真实写入仍取决于分支和参数。

- **L2289 · 方法** `func refreshOperationLogInfo()` — 刷新操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:78` `OperationLogReader.fileSizeText`

- **L2293 · 方法** `func trimOperationLog()` — 封装操作、日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:247` `OperationLogWriter.trimLogToRecentDays`；`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:2289` `AppModel.refreshOperationLogInfo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2316 · 方法** `func logUserAction(_ action: String, details: [String: Any] = [:])` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ action: String`；`details: [String: Any] = [:]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2320 · 方法** `func newOperationID(_ name: String, details: [String: Any] = [:]) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`details: [String: Any] = [:]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2331 · 方法** `private func finishOperationLog( _ operationID: String, name: String, startedAt: Date, exitStatus: Int32 )` — 结束并收口操作、日志相关数据或步骤。
  - 输入：`_ operationID: String`；`name: String`；`startedAt: Date`；`exitStatus: Int32`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2349 · 方法** `func environmentForOperation(_ operationID: String) -> [String: String]` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ operationID: String`
  - 返回：`[String: String]`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:257` `OperationLogWriter.environment`

- **L2357 · 方法** `func saveAllSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2233` `AppModel.saveSettings`；`macos/TravelerAssistant.swift:2381` `AppModel.saveJdyPassword`；`macos/TravelerAssistant.swift:2432` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `saveJdyPassword`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L2381 · 方法** `func saveJdyPassword()` — 保存与 `saveJdyPassword` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `SecItemDelete`, `SecItemUpdate`, `SecItemCopyMatching`；是否真实写入仍取决于分支和参数。

- **L2432 · 方法** `func saveAimesPassword()` — 保存AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2233` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `SecItemDelete`；是否真实写入仍取决于分支和参数。

- **L2453 · 方法** `private func applyDashboardObject(_ object: [String: Any], includeChanges: Bool = true)` — 应用看板相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2627` `AppModel.applyDashboardOperationTrace`；`macos/TravelerAssistant.swift:2610` `AppModel.applyCurrentIssues`；`macos/TravelerAssistant.swift:251` `dashboardOrderRows`；`macos/TravelerAssistant.swift:91` `OrderDashboardFactory`；`macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`macos/TravelerAssistant.swift:225` `OrderDashboardItem`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:948` `dashboardActivitySteps`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `insert`；是否真实写入仍取决于分支和参数。

- **L2538 · 方法** `private func presentServerWritePreview(_ object: [String: Any])` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2558` `AppModel.presentHardwareSourceSelection`；`macos/TravelerAssistant.swift:635` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2558 · 方法** `private func presentHardwareSourceSelection(_ request: [String: Any])` — 封装五金、来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ request: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2569 · 计算属性** `var canResumeHardwareSourcePreview: Bool` — 根据当前状态计算并返回五金、来源、预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2575 · 方法** `func confirmHardwareSourceSelection()` — 封装五金、来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2581 · 计算属性** `private var hardwareSourceChoiceArguments: [String]` — 根据当前状态计算并返回五金、来源。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2588 · 方法** `func hardwareSourceSelectionDidDismiss()` — 封装五金、来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:3431` `AppModel.requestInventoryMapping`；`macos/TravelerAssistant.swift:2538` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2610 · 方法** `private func applyCurrentIssues(from object: [String: Any])` — 应用与 `applyCurrentIssues` 对应的数据或步骤。
  - 输入：`from object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:831` `CurrentIssue`

- **L2627 · 方法** `private func applyDashboardOperationTrace(_ object: [String: Any])` — 应用看板、操作相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2639 · 方法** `private func applyAimesReviewObject(_ object: [String: Any], presentIfNeeded: Bool = true)` — 应用AIMES 数据相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:854` `aimesReviewItems`；`macos/TravelerAssistant.swift:871` `aimesReviewItemsFromWarnings`；`macos/OrderDashboardView.swift:796` `shouldPresentPendingCenterAfterAimes`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L2657 · 方法** `private func closePendingCenterIfEmpty()` — 关闭与 `closePendingCenterIfEmpty` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2663 · 方法** `private func beginDashboardOperation(_ source: String, label: String, continuing: Bool = false)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`；`label: String`；`continuing: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1405` `DashboardOperationStart`

- **L2678 · 方法** `func dashboardElapsedTime(_ source: String) -> TimeInterval?` — 封装看板、时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`
  - 返回：`TimeInterval?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2683 · 方法** `private func finishDashboardOperation(_ source: String)` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1383` `DashboardOperationDuration`

- **L2696 · 方法** `private func finishDashboardOperation( _ source: String, backendSeconds: Double, stages: [[String: Any]] )` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`backendSeconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1395` `dashboardFlatOperationDurations`；`macos/TravelerAssistant.swift:1383` `DashboardOperationDuration`

- **L2722 · 方法** `private func finishDashboardOperation(_ source: String, using object: [String: Any])` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`using object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2735 · 方法** `private func discardDashboardOperationTimer(_ source: String)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2739 · 方法** `private func applyAuthoritativeDashboardTiming( _ source: String, seconds: Double, stages: [[String: Any]] )` — 应用看板相关数据或步骤。
  - 输入：`_ source: String`；`seconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1395` `dashboardFlatOperationDurations`

- **L2750 · 方法** `func startOrderDashboard()` — 启动订单中心初始化链路，加载缓存并安排 AIMES/Server 刷新。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2756` `AppModel.loadOrderDashboardCache`

- **L2756 · 方法** `func loadOrderDashboardCache()` — 读取订单、看板、缓存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2639` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:2877` `AppModel.syncDashboardAimes`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2778 · 方法** `func refreshDashboardOrdersAfterOutbound()` — 刷新看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2797 · 方法** `private func startPendingDashboardOutboundRefreshIfNeeded()` — 启动看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2778` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L2805 · 方法** `private func runDailyBackupAfterLocalCache(completion: @escaping () -> Void)` — 执行备份、缓存相关数据或步骤。
  - 输入：`completion: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2844 · 方法** `func autoResolveCurrentIssue(_ issue: CurrentIssue)` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2657` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2859 · 方法** `func resolveCurrentIssue(_ issue: CurrentIssue, orderID: String)` — 解析并确定待处理问题相关数据或步骤。
  - 输入：`_ issue: CurrentIssue`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2657` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2877 · 方法** `func syncDashboardAimes(force: Bool, scanServerAfter: Bool = false)` — 从 App 发起 AIMES 同步，解析结果并衔接后续看板刷新。
  - 输入：`force: Bool`；`scanServerAfter: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:3050` `AppModel.scanDashboardServer`；`macos/TravelerAssistant.swift:2735` `AppModel.discardDashboardOperationTimer`；`macos/TravelerAssistant.swift:2739` `AppModel.applyAuthoritativeDashboardTiming`；`macos/TravelerAssistant.swift:2639` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:2627` `AppModel.applyDashboardOperationTrace`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:895` `dashboardAimesStatusUpdate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `dashboardAimesStatusUpdate`；是否真实写入仍取决于分支和参数。

- **L2937 · 方法** `func toggleAimesReviewSelection(_ item: AimesReviewItem)` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`

- **L2947 · 方法** `func ignoreSelectedAimesFactories()` — 忽略AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2639` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:2657` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2973 · 方法** `func restoreAimesFactory(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2639` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2993 · 方法** `func assignAimesFactoryToSuggestedOrder(_ item: AimesReviewItem)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2998` `AppModel.assignAimesFactoryToOrder`

- **L2998 · 方法** `func assignAimesFactoryToOrder(_ item: AimesReviewItem, orderID: String)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2639` `AppModel.applyAimesReviewObject`；`macos/TravelerAssistant.swift:2657` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L3030 · 方法** `func restoreAimesFactoryAssignment(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2639` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3050 · 方法** `func scanDashboardServer(background: Bool = false, presentIfNeeded: Bool = true)` — 从 App 发起 Server 扫描并把变化、问题和耗时写入看板状态。
  - 输入：`background: Bool = false`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2610` `AppModel.applyCurrentIssues`；`macos/TravelerAssistant.swift:2627` `AppModel.applyDashboardOperationTrace`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:1008` `serverChangePreviews`；`macos/TravelerAssistant.swift:2657` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L3081 · 方法** `func toggleServerFolderSelection(_ folderPath: String)` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folderPath: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:700` `serverFolderChangeGroups`

- **L3093 · 方法** `func clearServerFolderSelection()` — 清理Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`

- **L3098 · 方法** `func processPendingServerChanges()` — 按当前选择为 Server 变化生成业务预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:700` `serverFolderChangeGroups`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2538` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3131 · 方法** `func confirmServerWrite(orderID: String, factoryOrder: String)` — 确认并执行 Server 事实写入，然后只做所需的本地看板刷新。
  - 输入：`orderID: String`；`factoryOrder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:566` `ServerWriteOrderPreview`；`macos/TravelerAssistant.swift:635` `ServerWritePreview`；`macos/TravelerAssistant.swift:3278` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `ServerWriteOrderPreview`, `ServerWritePreview`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L3210 · 方法** `func confirmServerMaterialPreview(skipHardwareOrderIDs: Set<String> = [])` — 封装Server 数据、材料、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`skipHardwareOrderIDs: Set<String> = []`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1323` `InventoryStep`；`macos/TravelerAssistant.swift:1417` `dashboardClockTime`；`macos/TravelerAssistant.swift:3278` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L3278 · 方法** `func refreshDashboardAfterServerWrite(processedFolders: [String])` — 刷新看板、Server 数据相关数据或步骤。
  - 输入：`processedFolders: [String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:1038` `serverChangesExcludingFolders`；`macos/TravelerAssistant.swift:2657` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L3301 · 方法** `private func applyServerIndexResult(_ object: [String: Any])` — 应用Server 数据、结果相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:2639` `AppModel.applyAimesReviewObject`

- **L3306 · 方法** `func prepareSelectedServerFolder(_ folderURL: URL)` — 准备并校验Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3312 · 方法** `func processSelectedServerFolder(_ folderURL: URL, includeHardware: Bool)` — 处理Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`；`includeHardware: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:1323` `InventoryStep`；`macos/TravelerAssistant.swift:1417` `dashboardClockTime`；`macos/TravelerAssistant.swift:3431` `AppModel.requestInventoryMapping`；`macos/TravelerAssistant.swift:2538` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3356 · 方法** `func markTemporaryFolderManual(_ folderPath: String, referenceOrderIDs: [String], outboundDocument: String)` — 标记文件夹相关数据或步骤。
  - 输入：`_ folderPath: String`；`referenceOrderIDs: [String]`；`outboundDocument: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2610` `AppModel.applyCurrentIssues`；`macos/TravelerAssistant.swift:1031` `serverChangesExcludingFolder`；`macos/TravelerAssistant.swift:2657` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L3388 · 方法** `func loadInventory()` — 加载可处理的库存/Traveler 列表及目录状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1230` `InventoryTraveler`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:3577` `AppModel.activatePendingInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `Set`；是否真实写入仍取决于分支和参数。

- **L3431 · 方法** `func requestInventoryMapping(folderPath: String, message: String = "", includeHardware: Bool = true)` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folderPath: String`；`message: String = ""`；`includeHardware: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:69` `inventoryMappingSourceFolderPath`；`macos/TravelerAssistant.swift:1723` `PendingResumeContext`；`macos/TravelerAssistant.swift:1702` `PendingMappingResumeState`；`macos/TravelerAssistant.swift:3478` `AppModel.inventoryMappingNames`

- **L3468 · 方法** `func closeInventoryMappingWorkspace()` — 关闭库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3478 · 方法** `private func inventoryMappingNames(from message: String) -> [String]` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from message: String`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3489 · 方法** `private func rereadPendingSourceFolder()` — 封装来源、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3526` `AppModel.resumePendingMappingOperationAfterMapping`

- **L3494 · 方法** `private func failPendingResume(_ context: PendingResumeContext, message: String)` — 封装 `failPendingResume` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ context: PendingResumeContext`；`message: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3505 · 方法** `private func recordPendingMappingsSaved(_ names: [String], context: PendingResumeContext?)` — 记录记录相关数据或步骤。
  - 输入：`_ names: [String]`；`context: PendingResumeContext?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3518 · 方法** `func inventoryMappingWorkspaceDidDismiss()` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3468` `AppModel.closeInventoryMappingWorkspace`；`macos/TravelerAssistant.swift:2538` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryMappingWorkspace`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3526 · 方法** `private func resumePendingMappingOperationAfterMapping()` — 封装映射、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3757` `AppModel.previewSelectedInventory`；`macos/TravelerAssistant.swift:3494` `AppModel.failPendingResume`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:3478` `AppModel.inventoryMappingNames`；`macos/TravelerAssistant.swift:635` `ServerWritePreview`；`macos/TravelerAssistant.swift:69` `inventoryMappingSourceFolderPath`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3572 · 方法** `func retryPendingMappingPreview()` — 封装映射、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3526` `AppModel.resumePendingMappingOperationAfterMapping`

- **L3577 · 方法** `func activatePendingInventoryMapping()` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3757` `AppModel.previewSelectedInventory`

- **L3617 · 方法** `func openInventoryChrome()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3630 · 方法** `func updateInventoryCatalog()` — 更新库存、商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:5745` `inventoryCatalogUpdateFailureStatus`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `inventoryCatalogUpdateFailureStatus`, `inventoryCatalogUpdateSuccessStatus`；是否真实写入仍取决于分支和参数。

- **L3658 · 方法** `func closeInventoryChromeOnQuit()` — 关闭库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`, `record`；是否真实写入仍取决于分支和参数。

- **L3688 · 方法** `func refreshInventoryCatalogStatus()` — 刷新库存、商品目录、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3698 · 方法** `func refreshInventoryFolder(_ folder: String)` — 刷新库存、文件夹相关数据或步骤。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:3730` `AppModel.reloadInventoryFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3730 · 方法** `private func reloadInventoryFolder(_ folder: String)` — 封装库存、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1230` `InventoryTraveler`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3757 · 方法** `func previewSelectedInventory()` — 为当前选中对象串行生成库存需求和可用量预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:3790` `AppModel.previewOrderInventory`；`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4597` `AppModel.previewNext`

- **L3790 · 方法** `func previewOrderInventory( orderID: String, factoryOrderNames: [String], factoryOrders: [String] = [], productionBatchNumber: String = "", shipmentOnly: Bool = false )` — 预览预览、订单、库存相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrderNames: [String]`；`factoryOrders: [String] = []`；`productionBatchNumber: String = ""`；`shipmentOnly: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4585` `AppModel.applyInventoryPreviewObject`；`macos/TravelerAssistant.swift:4811` `AppModel.finishInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`；是否真实写入仍取决于分支和参数。

- **L3831 · 方法** `func loadProductionPreview(orderID: String, factoryOrders: [String], completion: @escaping (Bool) -> Void = { _ in })` — 读取当前选择的生产材料预览并填充编辑草稿。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:106` `ProductionMaterialDraft`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3869 · 方法** `func prepareProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], onResult completion: @escaping (String?, String?) -> Void )` — 从 App 提交生产准备参数并处理后端返回。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`onResult completion: @escaping (String?, String?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3886 · 方法** `func startDirectProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], batchNumber: String, completion: @escaping (ProductionOperationResult) -> Void = { _ in } )` — 执行用户确认后的生产完成流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`batchNumber: String`；`completion: @escaping (ProductionOperationResult) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`；`macos/TravelerAssistant.swift:206` `ProductionOperationResult`；`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:1323` `InventoryStep`；`macos/TravelerAssistant.swift:1417` `dashboardClockTime`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1368` `inventoryFailureNeedsVerification`；`macos/TravelerAssistant.swift:2778` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L4004 · 方法** `func startDirectOrderShipment(orderID: String, factoryOrders: [String])` — 执行用户确认后的订单出库流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2663` `AppModel.beginDashboardOperation`；`macos/TravelerAssistant.swift:1323` `InventoryStep`；`macos/TravelerAssistant.swift:1417` `dashboardClockTime`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:2778` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L4084 · 方法** `func loadOutboundScope( orderID: String, factoryOrders: [String], completion: @escaping ([String: Any]?) -> Void )` — 读取出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping ([String: Any]?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4106 · 方法** `func saveOutboundScope( orderID: String, scopeType: String, requirement: String, factoryOrder: String = "", reason: String, completion: @escaping (Bool) -> Void = { _ in } )` — 保存出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`scopeType: String`；`requirement: String`；`factoryOrder: String = ""`；`reason: String`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4135 · 方法** `func openAndFillSelectedInventory()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:4227` `AppModel.markInventoryTravelerSaved`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4227 · 方法** `private func markInventoryTravelerSaved(path: String, documentNumber: String)` — 标记库存、Traveler相关数据或步骤。
  - 输入：`path: String`；`documentNumber: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1230` `InventoryTraveler`

- **L4242 · 方法** `func setInventoryItemsIgnored(_ names: [String], ignored: Bool)` — 设置库存相关数据或步骤。
  - 输入：`_ names: [String]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3505` `AppModel.recordPendingMappingsSaved`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:3526` `AppModel.resumePendingMappingOperationAfterMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`, `recordPendingMappingsSaved`；是否真实写入仍取决于分支和参数。

- **L4277 · 方法** `func refreshInventoryMappings()` — 刷新库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1316` `InventoryManualMapping`；`macos/TravelerAssistant.swift:1310` `InventoryIgnoredMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4300 · 方法** `func saveSettingsManualMapping(name: String, productCode: String, displayName: String)` — 保存设置、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`；`displayName: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4317 · 方法** `func updateSettingsManualMapping(oldName: String, name: String, productCode: String, displayName: String)` — 更新设置、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`productCode: String`；`displayName: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4336 · 方法** `func removeSettingsManualMapping(name: String)` — 移除设置、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4346 · 方法** `func saveInventoryIgnoredMapping(name: String, reason: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3494` `AppModel.failPendingResume`；`macos/TravelerAssistant.swift:3505` `AppModel.recordPendingMappingsSaved`；`macos/TravelerAssistant.swift:3489` `AppModel.rereadPendingSourceFolder`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `recordPendingMappingsSaved`；是否真实写入仍取决于分支和参数。

- **L4379 · 方法** `func updateInventoryIgnoredMapping(oldName: String, name: String, reason: String)` — 更新库存、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4401 · 方法** `func removeInventoryIgnoredMapping(name: String)` — 移除库存、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4411 · 方法** `func searchInventoryProducts(_ query: String)` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ query: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:1301` `InventoryProductCandidate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4438 · 方法** `func saveInventoryMapping(travelerName: String, productCode: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`travelerName: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:3494` `AppModel.failPendingResume`；`macos/TravelerAssistant.swift:3505` `AppModel.recordPendingMappingsSaved`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:3526` `AppModel.resumePendingMappingOperationAfterMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `recordPendingMappingsSaved`；是否真实写入仍取决于分支和参数。

- **L4465 · 方法** `func saveServerHardwareMapping(name: String, productCode: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4495` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4480 · 方法** `func saveServerHardwareIgnoredMapping(name: String, reason: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4781` `AppModel.beginInventoryOperation`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4495` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4495 · 方法** `private func removeServerHardwareMappingRequirement(_ name: String)` — 移除Server 数据、五金、映射相关数据或步骤。
  - 输入：`_ name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:635` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L4510 · 方法** `private func consumeInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] ) -> [InventoryPreviewRow]` — 消费并转换库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1257` `InventoryPreviewRow`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`

- **L4585 · 方法** `private func applyInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] )` — 应用库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1285` `sortedInventoryPreviewRows`；`macos/TravelerAssistant.swift:4510` `AppModel.consumeInventoryPreviewObject`

- **L4597 · 方法** `private func previewNext( _ paths: [String], index: Int, selectedDocumentRemarks: Set<String> = [], accumulated: [InventoryPreviewRow] )` — 预览预览相关数据或步骤。
  - 输入：`_ paths: [String]`；`index: Int`；`selectedDocumentRemarks: Set<String> = []`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1285` `sortedInventoryPreviewRows`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:4635` `AppModel.runInventory`；`macos/TravelerAssistant.swift:4510` `AppModel.consumeInventoryPreviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4635 · 方法** `private func runInventory( _ arguments: [String], manageRunning: Bool = true, onFailure: ((String) -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动库存 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`manageRunning: Bool = true`；`onFailure: ((String) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:863` `dashboardStatusIsInProgress`；`macos/TravelerAssistant.swift:2320` `AppModel.newOperationID`；`macos/TravelerAssistant.swift:2349` `AppModel.environmentForOperation`；`macos/TravelerAssistant.swift:4830` `AppModel.consumeInventoryLogChunk`；`macos/TravelerAssistant.swift:2331` `AppModel.finishOperationLog`；`macos/TravelerAssistant.swift:4797` `AppModel.finishRunningInventoryStep`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L4781 · 方法** `private func beginInventoryOperation(_ title: String)` — 封装库存、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`

- **L4786 · 方法** `private func addInventoryStep(_ title: String, _ detail: String, _ state: String)` — 新增库存相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1323` `InventoryStep`；`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4797 · 方法** `private func finishRunningInventoryStep(_ detail: String, _ state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:4786` `AppModel.addInventoryStep`；`macos/TravelerAssistant.swift:1323` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4811 · 方法** `private func finishInventoryStep(named title: String, detail: String, state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`named title: String`；`detail: String`；`state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1323` `InventoryStep`

- **L4830 · 方法** `private func consumeInventoryLogChunk(_ chunk: String)` — 消费并转换库存、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1490` `appendingInventoryProgressStep`；`macos/TravelerAssistant.swift:1421` `dashboardInventoryProgressText`

- **L4851 · 方法** `private func addOrderStep(_ title: String, _ detail: String, _ state: String)` — 新增订单相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1323` `InventoryStep`；`macos/OperationLog.swift:198` `OperationLogWriter.record`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4870 · 方法** `private func finishOrderStep(_ detail: String, _ state: String)` — 结束并收口订单相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OperationLog.swift:198` `OperationLogWriter.record`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:1323` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4897 · 方法** `private func appendDashboardProgress(_ source: String, message: String)` — 封装看板、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`；`message: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4901 · 方法** `func consumeOrderLogChunk(_ chunk: String)` — 消费并转换订单、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4897` `AppModel.appendDashboardProgress`；`macos/TravelerAssistant.swift:1978` `AppModel.recordDashboardStageCompletion`；`macos/TravelerAssistant.swift:1417` `dashboardClockTime`；`macos/TravelerAssistant.swift:1421` `dashboardInventoryProgressText`；`macos/TravelerAssistant.swift:1471` `updatingLatestRunningStep`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `recordDashboardStageCompletion`；是否真实写入仍取决于分支和参数。

- **L4956 · 方法** `private func runOrder( _ arguments: [String], input: Data? = nil, failureStatus: String = "校验未通过", onFailure: (() -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动订单 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`input: Data? = nil`；`failureStatus: String = "校验未通过"`；`onFailure: (() -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2320` `AppModel.newOperationID`；`macos/TravelerAssistant.swift:4901` `AppModel.consumeOrderLogChunk`；`macos/TravelerAssistant.swift:1570` `ResidentOrderServiceClient.start`；`macos/TravelerAssistant.swift:2349` `AppModel.environmentForOperation`；`macos/TravelerAssistant.swift:1590` `ResidentOrderServiceClient.request`；`macos/TravelerAssistant.swift:2331` `AppModel.finishOperationLog`；`macos/TravelerAssistant.swift:2797` `AppModel.startPendingDashboardOutboundRefreshIfNeeded`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `startPendingDashboardOutboundRefreshIfNeeded`；是否真实写入仍取决于分支和参数。

- **L5064 · 方法** `func stopResidentOrderService()` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1622` `ResidentOrderServiceClient.stop`

- **L5069 · 方法** `func loadOrderFolders()` — 读取订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:85` `OrderFolderItem`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5107 · 方法** `func previewOrderFolder(_ item: OrderFolderItem, recordSelection: Bool = true)` — 预览预览、订单、文件夹相关数据或步骤。
  - 输入：`_ item: OrderFolderItem`；`recordSelection: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5183` `AppModel.findLocalOrderTraveler`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:1073` `orderPreviewIssues`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:5217` `AppModel.applyOrderPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5183 · 方法** `private func findLocalOrderTraveler(_ orderId: String) -> String` — 查找订单、Traveler相关数据或步骤。
  - 输入：`_ orderId: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5217 · 方法** `private func applyOrderPreview(_ object: [String: Any], targetOrderID: String? = nil)` — 应用订单、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`targetOrderID: String? = nil`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1083` `OrderMaterialPreview`；`macos/TravelerAssistant.swift:1176` `OrderFactoryPreview`；`macos/TravelerAssistant.swift:1182` `OrderFittingPreview`

- **L5272 · 方法** `func loadOrderDetailFromDatabase(_ item: OrderDashboardItem)` — 读取订单、数据库相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/OrderDashboardView.swift:707` `orderDashboardIsCompleted`；`macos/TravelerAssistant.swift:5342` `AppModel.schedulePendingOrderDetailRetry`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:1410` `Double`；`macos/TravelerAssistant.swift:5217` `AppModel.applyOrderPreview`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5342 · 方法** `private func schedulePendingOrderDetailRetry()` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5272` `AppModel.loadOrderDetailFromDatabase`

- **L5360 · 方法** `func saveOrderAnnotations( orderID: String, userNote: String, plannedDays: [OrderInstallationDay], actualDays: [OrderInstallationDay], onStatusChange: @escaping (String) -> Void = { _ in }, onSuccess: @escaping () -> Void = {} )` — 保存安装日期、安装人等订单人工备注并刷新详情。
  - 输入：`orderID: String`；`userNote: String`；`plannedDays: [OrderInstallationDay]`；`actualDays: [OrderInstallationDay]`；`onStatusChange: @escaping (String) -> Void = { _ in }`；`onSuccess: @escaping () -> Void = {}`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`macos/TravelerAssistant.swift:2453` `AppModel.applyDashboardObject`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5410 · 方法** `func setOrderFittingsIgnored(_ rows: [OrderFittingPreview], ignored: Bool)` — 设置订单相关数据或步骤。
  - 输入：`_ rows: [OrderFittingPreview]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:5107` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runOrder`；是否真实写入仍取决于分支和参数。

- **L5439 · 方法** `func generateSelectedOrder()` — 生成订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:5594` `AppModel.openSelectedOrderTraveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `openSelectedOrderTraveler`；是否真实写入仍取决于分支和参数。

- **L5463 · 方法** `func generateMissingMaterial()` — 生成材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`；`macos/TravelerAssistant.swift:5107` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5486 · 方法** `func checkSelectedOrderStock()` — 检查订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:1196` `OrderStockPreview`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5528 · 方法** `func calculateSelectedOrderCost(export: Bool = false)` — 计算订单、成本相关数据或步骤。
  - 输入：`export: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`；`macos/TravelerAssistant.swift:4956` `AppModel.runOrder`；`macos/TravelerAssistant.swift:5558` `AppModel.applyOrderCost`；`macos/TravelerAssistant.swift:4870` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `open`；是否真实写入仍取决于分支和参数。

- **L5558 · 方法** `private func applyOrderCost(_ object: [String: Any])` — 应用订单、成本相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1208` `OrderCostLine`；`macos/TravelerAssistant.swift:1223` `OrderCostFactoryTotal`

- **L5594 · 方法** `func openSelectedOrderTraveler()` — 打开订单、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:4851` `AppModel.addOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L5612 · 方法** `func openDashboardLocation(_ path: String)` — 打开看板相关数据或步骤。
  - 输入：`_ path: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L5625 · 计算属性** `var projectRoot: URL` — 根据当前状态计算并返回`projectRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5633 · 枚举** `AppLayout` — 定义 `AppLayout` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5682 · 结构体** `FixedWindowSizeController` — 定义 `FixedWindowSizeController` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5685 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5699` `FixedWindowSizeController.applyFixedSize`

- **L5693 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5699` `FixedWindowSizeController.applyFixedSize`

- **L5699 · 方法** `private func applyFixedSize(to window: NSWindow?)` — 应用与 `applyFixedSize` 对应的数据或步骤。
  - 输入：`to window: NSWindow?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setFrame`；是否真实写入仍取决于分支和参数。

- **L5713 · 函数** `func inventoryActionColumnCount(availableWidth: CGFloat) -> Int` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`availableWidth: CGFloat`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5718 · 枚举** `AppPalette` — 定义 `AppPalette` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5732 · 函数** `func inventoryCatalogUpdateSuccessStatus(_ count: Int) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5736 · 函数** `func inventoryCatalogUpdateSuccessStatus( _ count: Int, added: Int, updated: Int, removed: Int ) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`；`added: Int`；`updated: Int`；`removed: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5745 · 函数** `func inventoryCatalogUpdateFailureStatus(_ reason: String) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ reason: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5749 · 枚举** `SettingsStatusKind` — 定义与设置、状态相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5756 · 计算属性** `var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5766 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5777 · 函数** `func settingsStatusKind(_ status: String) -> SettingsStatusKind` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`SettingsStatusKind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5786 · 函数** `func settingsStatusDisplayText(_ status: String) -> String` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5792 · 结构体** `SettingsStatusBanner` — 定义与设置、状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5795 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5777` `settingsStatusKind`；`macos/TravelerAssistant.swift:5786` `settingsStatusDisplayText`

- **L5823 · 扩展** `View` — 定义 `View` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5824 · 方法** `func appPageFrame() -> some View` — 封装 `appPageFrame` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5852` `AppGlassGroupBoxStyle`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`

- **L5832 · 方法** `func appInputField(maxWidth: CGFloat? = nil) -> some View` — 封装 `appInputField` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`maxWidth: CGFloat? = nil`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5836 · 方法** `func appActionButton(minWidth: CGFloat = AppLayout.actionButtonWidth) -> some View` — 封装 `appActionButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.actionButtonWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5841 · 方法** `func inventoryActionButton(minWidth: CGFloat = AppLayout.inventoryActionMinWidth) -> some View` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.inventoryActionMinWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5852 · 结构体** `AppGlassGroupBoxStyle` — 定义 `AppGlassGroupBoxStyle` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5853 · 方法** `func makeBody(configuration: Configuration) -> some View` — 创建与 `makeBody` 对应的数据或步骤。
  - 输入：`configuration: Configuration`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5866 · 结构体** `AppSurfaceCard<Content` — 定义 `AppSurfaceCard<Content` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5870 · 初始化器** `init(padding: CGFloat = AppLayout.cardPadding, @ViewBuilder content: () -> Content)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`padding: CGFloat = AppLayout.cardPadding`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5875 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5885 · 结构体** `LiquidGlassPreviewBackdrop` — 定义与预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5886 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5920 · 结构体** `AppStatusBadge` — 定义与状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5921 · 枚举** `Kind` — 定义 `Kind` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5926 · 计算属性** `private var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5936 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5951 · 结构体** `WidthPreferenceKey` — 定义 `WidthPreferenceKey` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5954 · 方法** `static func reduce(value: inout CGFloat, nextValue: () -> CGFloat)` — 封装 `reduce` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: inout CGFloat`；`nextValue: () -> CGFloat`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5959 · 结构体** `ScrollingTextOnHover` — 定义 `ScrollingTextOnHover` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5970 · 计算属性** `private var overflow: CGFloat` — 根据当前状态计算并返回`overflow` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5974 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6009` `ScrollingTextOnHover.startScrolling`；`macos/TravelerAssistant.swift:6031` `ScrollingTextOnHover.stopScrolling`

- **L6009 · 方法** `private func startScrolling()` — 启动与 `startScrolling` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1410` `Double`

- **L6031 · 方法** `private func stopScrolling()` — 封装 `stopScrolling` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6038 · 结构体** `InventoryActionGrid<Content` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6042 · 初始化器** `init( minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6050 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6060 · 结构体** `AppPageHeader<Trailing` — 定义 `AppPageHeader<Trailing` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6066 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6071 · 结构体** `OperationLogCard` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6076 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6082 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6646` `SelectableOperationLogView`

- **L6092 · 结构体** `OrderWorkflowView` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6096 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:5069` `AppModel.loadOrderFolders`；`macos/TravelerAssistant.swift:5107` `AppModel.previewOrderFolder`；`macos/TravelerAssistant.swift:1444` `appDisplayTimestamp`；`macos/TravelerAssistant.swift:5486` `AppModel.checkSelectedOrderStock`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:6071` `OperationLogCard`；`macos/TravelerAssistant.swift:6485` `OrderWorkflowView.summaryCard`；`macos/TravelerAssistant.swift:6505` `OrderWorkflowView.subsectionTitle`；`macos/TravelerAssistant.swift:1164` `panelColorsNeedingThicknessWarning`；`macos/TravelerAssistant.swift:1120` `orderedMaterialRows`；`macos/TravelerAssistant.swift:1109` `orderMaterialDisplayName`；另有 4 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `setOrderFittingsIgnored`；是否真实写入仍取决于分支和参数。

- **L6485 · 方法** `private func summaryCard(title: String, value: String, detail: String, color: Color, warning: Bool = false) -> some View` — 封装 `summaryCard` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`value: String`；`detail: String`；`color: Color`；`warning: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6505 · 方法** `private func subsectionTitle(_ title: String, color: Color) -> some View` — 封装 `subsectionTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6512 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6522 · 结构体** `SettingsCard<Content` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6528 · 初始化器** `init( title: String, symbol: String, padding: CGFloat = 14, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`title: String`；`symbol: String`；`padding: CGFloat = 14`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6540 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6554 · 结构体** `InventoryStepRowView` — 定义与库存、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6558 · 初始化器** `init(step: InventoryStep, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`step: InventoryStep`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6563 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L6591 · 计算属性** `private var detailText: String` — 根据当前状态计算并返回`detailText` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1363` `operationDurationText`

- **L6597 · 计算属性** `@ViewBuilder private var icon: some View` — 根据当前状态计算并返回`icon` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6612 · 结构体** `InventoryOperationLogView` — 定义与库存、操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6615 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6646` `SelectableOperationLogView`

- **L6623 · 结构体** `OperationLogAutoScroller` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6626 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6630 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6646 · 结构体** `SelectableOperationLogView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6652 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6658 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:6732` `SelectableOperationLogView.copySelected`；`macos/TravelerAssistant.swift:6720` `SelectableOperationLogView.select`；`macos/TravelerAssistant.swift:6554` `InventoryStepRowView`；`macos/TravelerAssistant.swift:6623` `OperationLogAutoScroller`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copySelected`, `Set`；是否真实写入仍取决于分支和参数。

- **L6715 · 计算属性** `private var scrollRevision: String` — 根据当前状态计算并返回`scrollRevision` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6720 · 方法** `private func select(_ id: UUID)` — 选择与 `select` 对应的数据或步骤。
  - 输入：`_ id: UUID`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L6732 · 方法** `private func copySelected()` — 封装 `copySelected` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:1363` `operationDurationText`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L6752 · 结构体** `InventoryTravelerRowView` — 定义与库存、Traveler、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6758 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5959` `ScrollingTextOnHover`

- **L6789 · 计算属性** `private var statusColor: Color` — 根据当前状态计算并返回状态、颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6799 · 结构体** `InventoryMappingSheet` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6806 · 初始化器** `init( model: AppModel, travelerName: String, isPresented: Binding<Bool>, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`isPresented: Binding<Bool>`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6818 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5832` `View.appInputField`；`macos/TravelerAssistant.swift:4411` `AppModel.searchInventoryProducts`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:4438` `AppModel.saveInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryMapping`；是否真实写入仍取决于分支和参数。

- **L6885 · 结构体** `PendingInventoryMappingTarget` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6887 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6890 · 结构体** `PendingInventoryMappingWorkspace` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6895 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:6885` `PendingInventoryMappingTarget`；`macos/TravelerAssistant.swift:3572` `AppModel.retryPendingMappingPreview`；`macos/TravelerAssistant.swift:3468` `AppModel.closeInventoryMappingWorkspace`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`；`macos/TravelerAssistant.swift:6799` `InventoryMappingSheet`；`macos/TravelerAssistant.swift:6983` `PendingInventoryIgnoreSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryMappingWorkspace`；是否真实写入仍取决于分支和参数。

- **L6983 · 结构体** `PendingInventoryIgnoreSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6990 · 初始化器** `init( model: AppModel, travelerName: String, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7000 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5832` `View.appInputField`；`macos/TravelerAssistant.swift:4346` `AppModel.saveInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L7048 · 结构体** `InventoryView` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7059 · 初始化器** `init( model: AppModel, onClose: (() -> Void)? = nil, orderContextID: String = "", orderContextFactoryNames: [String] = [], orderContextFactoryOrders: [String] = [] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`onClose: (() -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7073 · 计算属性** `private var selectedTravelerCount: Int` — 选择Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7077 · 计算属性** `private var hasMappedOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7081 · 计算属性** `private var hasConfirmedNoOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7087 · 计算属性** `private var customerSuppliedOnly: Bool` — 根据当前状态计算并返回`customerSuppliedOnly` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L7094 · 计算属性** `private var confirmationTitle: String` — 根据当前状态计算并返回`confirmationTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7101 · 计算属性** `private var selectedTravelerDisplayName: String` — 选择Traveler、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7106 · 方法** `private func previewRowContent(_ row: InventoryPreviewRow) -> some View` — 预览预览、行数据相关数据或步骤。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7373` `InventoryView.previewStatusColor`

- **L7142 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:7350` `InventoryView.outboundStep`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:6071` `OperationLogCard`；`macos/TravelerAssistant.swift:7106` `InventoryView.previewRowContent`；`macos/TravelerAssistant.swift:5841` `View.inventoryActionButton`；`macos/TravelerAssistant.swift:3790` `AppModel.previewOrderInventory`；`macos/TravelerAssistant.swift:6799` `InventoryMappingSheet`；`macos/TravelerAssistant.swift:7364` `InventoryView.confirmationRow`；`macos/TravelerAssistant.swift:4135` `AppModel.openAndFillSelectedInventory`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outboundStep`, `onClose`, `openAndFillSelectedInventory`；是否真实写入仍取决于分支和参数。

- **L7341 · 方法** `private func statusColor(_ status: String) -> Color` — 封装状态、颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7350 · 方法** `private func outboundStep(_ number: Int, _ title: String, active: Bool) -> some View` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ number: Int`；`_ title: String`；`active: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7364 · 方法** `private func confirmationRow(_ label: String, _ value: String, valueColor: Color = .primary) -> some View` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ label: String`；`_ value: String`；`valueColor: Color = .primary`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7373 · 方法** `private func previewStatusColor(_ status: String) -> Color` — 预览预览、状态、颜色相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7382 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7392 · 方法** `private func stepIcon(_ state: String) -> some View` — 封装 `stepIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7406 · 结构体** `TodoView` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7415 · 计算属性** `private var sortedItems: [TodoItem]` — 排序与 `sortedItems` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[TodoItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7436 · 计算属性** `private var selectedItem: TodoItem?` — 选择项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`TodoItem?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7441 · 计算属性** `private var openCount: Int` — 打开与 `openCount` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7445 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:7597` `TodoView.todoRow`；`macos/TravelerAssistant.swift:2171` `AppModel.toggleTodoCompletion`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:7710` `TodoDeadlinePickerControl`；`macos/TravelerAssistant.swift:5824` `View.appPageFrame`；`macos/TravelerAssistant.swift:7763` `TodoEditorSheet`；`macos/TravelerAssistant.swift:2178` `AppModel.deleteTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `deleteTodo`；是否真实写入仍取决于分支和参数。

- **L7597 · 方法** `private func todoRow(_ item: TodoItem) -> some View` — 封装待办、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7670` `TodoView.deadlineText`；`macos/TravelerAssistant.swift:7690` `TodoView.deadlineColor`；`macos/TravelerAssistant.swift:7678` `TodoView.deadlineBadge`；`macos/TravelerAssistant.swift:2171` `AppModel.toggleTodoCompletion`

- **L7650 · 计算属性** `private var todoSelectionMessage: String?` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7655 · 计算属性** `private var deleteAlertBinding: Binding<Bool>` — 删除与 `deleteAlertBinding` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Binding<Bool>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7662 · 方法** `private func addTodo()` — 新增待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7670 · 方法** `private func deadlineText(_ date: Date?) -> String` — 封装 `deadlineText` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date?`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7678 · 方法** `private func deadlineBadge(_ item: TodoItem) -> String?` — 封装 `deadlineBadge` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7690 · 方法** `private func deadlineColor(_ item: TodoItem) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7702 · 函数** `func todoDeadlinePickerDisplay(_ date: Date) -> String` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7710 · 结构体** `TodoDeadlinePickerControl` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7714 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:7702` `todoDeadlinePickerDisplay`；`macos/OrderDashboardView.swift:104` `AppGlassDatePickerCalendar`；`macos/OrderDashboardView.swift:272` `View.appGlassDatePickerPopoverSurface`

- **L7763 · 结构体** `TodoEditorSheet` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7771 · 初始化器** `init(model: AppModel, item: TodoItem)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`item: TodoItem`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7783 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5832` `View.appInputField`；`macos/TravelerAssistant.swift:7710` `TodoDeadlinePickerControl`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:2159` `AppModel.updateTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateTodo`；是否真实写入仍取决于分支和参数。

- **L7812 · 结构体** `SettingsView` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7820 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`；`macos/TravelerAssistant.swift:8127` `SettingsView.compactStatus`；`macos/TravelerAssistant.swift:2357` `AppModel.saveAllSettings`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5824` `View.appPageFrame`；`macos/TravelerAssistant.swift:3688` `AppModel.refreshInventoryCatalogStatus`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`；`macos/TravelerAssistant.swift:2289` `AppModel.refreshOperationLogInfo`；`macos/OrderDashboardView.swift:4995` `AimesHistorySheet`；`macos/TravelerAssistant.swift:8340` `OperationLogViewerView`；`macos/TravelerAssistant.swift:8143` `InventoryIgnoredMappingsSheet`；`macos/TravelerAssistant.swift:8234` `InventoryManualMappingsSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAllSettings`；是否真实写入仍取决于分支和参数。

- **L7887 · 计算属性** `private var runAndFileSettingsCard: some View` — 执行文件、设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:8077` `SettingsView.settingsRowLabel`；`macos/TravelerAssistant.swift:8084` `SettingsView.settingsDateDisplay`；`macos/OrderDashboardView.swift:104` `AppGlassDatePickerCalendar`；`macos/OrderDashboardView.swift:272` `View.appGlassDatePickerPopoverSurface`；`macos/TravelerAssistant.swift:8093` `SettingsView.settingsFieldRow`

- **L7920 · 计算属性** `private var accountSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5832` `View.appInputField`；`macos/TravelerAssistant.swift:2381` `AppModel.saveJdyPassword`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:3617` `AppModel.openInventoryChrome`；`macos/TravelerAssistant.swift:2432` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveJdyPassword`, `openInventoryChrome`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L7973 · 计算属性** `private var inventorySettingsCard: some View` — 根据当前状态计算并返回库存、设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:8127` `SettingsView.compactStatus`；`macos/TravelerAssistant.swift:3630` `AppModel.updateInventoryCatalog`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:8106` `SettingsView.settingsManagementRow`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateInventoryCatalog`；是否真实写入仍取决于分支和参数。

- **L8005 · 计算属性** `private var maintenanceSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:2105` `AppModel.performBackup`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:8106` `SettingsView.settingsManagementRow`；`macos/TravelerAssistant.swift:2267` `AppModel.setOperationLogEnabled`；`macos/TravelerAssistant.swift:2316` `AppModel.logUserAction`；`macos/TravelerAssistant.swift:2293` `AppModel.trimOperationLog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setOperationLogEnabled`；是否真实写入仍取决于分支和参数。

- **L8077 · 方法** `private func settingsRowLabel(_ title: String) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8084 · 方法** `private func settingsDateDisplay(_ value: Date) -> String` — 设置设置、日期相关数据或步骤。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8093 · 方法** `private func settingsFieldRow( _ title: String, placeholder: String, text: Binding<String> ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`placeholder: String`；`text: Binding<String>`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:8077` `SettingsView.settingsRowLabel`；`macos/TravelerAssistant.swift:5832` `View.appInputField`

- **L8106 · 方法** `private func settingsManagementRow( _ title: String, count: Int, help: String, action: @escaping () -> Void ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`count: Int`；`help: String`；`action: @escaping () -> Void`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5836` `View.appActionButton`

- **L8127 · 方法** `private func compactStatus(_ status: String) -> some View` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5786` `settingsStatusDisplayText`；`macos/TravelerAssistant.swift:5777` `settingsStatusKind`

- **L8143 · 结构体** `InventoryIgnoredMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8150 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5832` `View.appInputField`；`macos/TravelerAssistant.swift:4346` `AppModel.saveInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:4379` `AppModel.updateInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:4401` `AppModel.removeInventoryIgnoredMapping`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryIgnoredMapping`, `updateInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L8227 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8234 · 结构体** `InventoryManualMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8242 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:5832` `View.appInputField`；`macos/TravelerAssistant.swift:4300` `AppModel.saveSettingsManualMapping`；`macos/TravelerAssistant.swift:4317` `AppModel.updateSettingsManualMapping`；`macos/TravelerAssistant.swift:4336` `AppModel.removeSettingsManualMapping`；`macos/TravelerAssistant.swift:4277` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettingsManualMapping`, `updateSettingsManualMapping`；是否真实写入仍取决于分支和参数。

- **L8332 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8340 · 结构体** `OperationLogViewerView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8345 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/OperationLog.swift:49` `OperationLogReader.entries`

- **L8411 · 枚举** `AppSection` — 定义 `AppSection` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8417 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8419 · 计算属性** `var title: String` — 根据当前状态计算并返回`title` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8428 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8437 · 计算属性** `var pageTitle: String` — 根据当前状态计算并返回`pageTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8446 · 计算属性** `var subtitle: String` — 根据当前状态计算并返回`subtitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8455 · 计算属性** `var isWorkSection: Bool` — 根据当前状态计算并返回`isWorkSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8464 · 结构体** `TopNavigationBar` — 定义 `TopNavigationBar` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8469 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:8584` `TopNavigationBar.navButton`；`macos/TravelerAssistant.swift:5836` `View.appActionButton`；`macos/TravelerAssistant.swift:8608` `TopNavigationBar.designNote`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`；`macos/OrderDashboardView.swift:3358` `PendingCenterSheet`；`macos/TravelerAssistant.swift:2588` `AppModel.hardwareSourceSelectionDidDismiss`；`macos/OrderDashboardView.swift:4275` `HardwareSourceSelectionSheet`；`macos/OrderDashboardView.swift:4366` `ServerWriteConfirmationSheet`；`macos/TravelerAssistant.swift:6890` `PendingInventoryMappingWorkspace`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteConfirmationSheet`；是否真实写入仍取决于分支和参数。

- **L8563 · 计算属性** `@ViewBuilder private var contextualStatus: some View` — 根据当前状态计算并返回状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:5920` `AppStatusBadge`

- **L8584 · 方法** `private func navButton(_ section: AppSection) -> some View` — 封装 `navButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ section: AppSection`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8608 · 方法** `private func designNote(_ title: String, _ text: String) -> some View` — 封装 `designNote` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ text: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8618 · 结构体** `TravelerAssistantApp` — 定义与Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8622 · 计算属性** `var body: some Scene` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some Scene`
  - 静态可确认的项目内下一跳：`macos/TravelerAssistant.swift:8464` `TopNavigationBar`；`macos/AssistantView.swift:705` `AssistantView`；`macos/OrderDashboardView.swift:1421` `OrderDashboardView`；`macos/TravelerAssistant.swift:7406` `TodoView`；`macos/TravelerAssistant.swift:7812` `SettingsView`；`macos/TravelerAssistant.swift:5852` `AppGlassGroupBoxStyle`；`macos/TravelerAssistant.swift:5885` `LiquidGlassPreviewBackdrop`；`macos/TravelerAssistant.swift:5682` `FixedWindowSizeController`；`macos/TravelerAssistant.swift:3658` `AppModel.closeInventoryChromeOnQuit`；`macos/TravelerAssistant.swift:5064` `AppModel.stopResidentOrderService`；`macos/TravelerAssistant.swift:2105` `AppModel.performBackup`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryChromeOnQuit`；是否真实写入仍取决于分支和参数。
