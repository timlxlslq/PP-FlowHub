# PP FlowHub 测试、脚本与工具全符号中文参考

> 本文件由 `tools/generate_code_reference.py` 生成。请不要手工修改。

## 如何阅读

- 范围：`tests/`、`scripts/`、`tools/` 和 `outputs/` 中的一方辅助代码，共登记 **1505** 个类型、函数、方法、计算属性或脚本过程。
- “输入”来自静态签名；`self`/`cls` 不重复列出。未声明类型不代表运行时没有约束。
- “项目内下一跳”只表示源码中可静态确认的直接调用，不表示每个分支都会执行。
- `self.method()`、协议分发、闭包、Swift 重载和动态导入可能无法唯一解析；关键业务路径以 `09-user-operation-call-chains.md` 为准。
- “副作用提示”是保守提醒，不等于函数一定执行写入。确认真实行为时应继续阅读分支、日志和测试。

## `.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift`

Swift/macOS 源码或测试辅助文件。

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
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

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
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:982` `orderMaterialDisplayName`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:956` `OrderMaterialPreview`

- **L151 · 函数** `private func productionMaterialTypeRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L160 · 函数** `private func productionMaterialPlywoodRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`

- **L168 · 函数** `func sortedProductionMaterialDrafts(_ materials: [ProductionMaterialDraft]) -> [ProductionMaterialDraft]` — 排序生产、材料相关数据或步骤。
  - 输入：`_ materials: [ProductionMaterialDraft]`
  - 返回：`[ProductionMaterialDraft]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:151` `productionMaterialTypeRank`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:160` `productionMaterialPlywoodRank`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:128` `productionMaterialName`

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

- **L332 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L346 · 结构体** `ServerWriteMaterialChange` — 定义与Server 数据、材料相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L358 · 初始化器** `init( id: String, changeType: String, materialType: String, color: String, thickness: String, edge: String, unit: String, oldQuantity: Double, newQuantity: Double, delta: Double )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`changeType: String`；`materialType: String`；`color: String`；`thickness: String`；`edge: String`；`unit: String`；`oldQuantity: Double`；`newQuantity: Double`；`delta: Double`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L382 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L397 · 方法** `static func aggregated(_ changes: [ServerWriteMaterialChange]) -> [ServerWriteMaterialChange]` — 封装 `aggregated` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerWriteMaterialChange]`
  - 返回：`[ServerWriteMaterialChange]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:346` `ServerWriteMaterialChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`；是否真实写入仍取决于分支和参数。

- **L426 · 结构体** `ServerWriteHardwareChange` — 定义与Server 数据、五金相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L439 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L457 · 结构体** `ServerHardwareMappingRequirement` — 定义与Server 数据、五金、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L467 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L481 · 结构体** `ServerWriteFactoryPreview` — 定义与Server 数据、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L495 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:323` `ServerWriteHardwarePreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:426` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteHardwarePreview`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L517 · 结构体** `ServerWriteOrderPreview` — 定义与Server 数据、订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L530 · 初始化器** `init( id: String, orderID: String, orderType: String, sourceFolder: String, validationStatus: String, validationMessage: String, materials: [ServerWriteMaterialPreview], materialChanges: [ServerWriteMaterialChange], factories: [ServerWriteFactoryPreview], excludedFactories: [ServerWriteFactoryPreview], hardwareChanges: [ServerWriteHardwareChange] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`orderID: String`；`orderType: String`；`sourceFolder: String`；`validationStatus: String`；`validationMessage: String`；`materials: [ServerWriteMaterialPreview]`；`materialChanges: [ServerWriteMaterialChange]`；`factories: [ServerWriteFactoryPreview]`；`excludedFactories: [ServerWriteFactoryPreview]`；`hardwareChanges: [ServerWriteHardwareChange]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L556 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:292` `ServerWriteMaterialPreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:397` `ServerWriteMaterialChange.aggregated`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:346` `ServerWriteMaterialChange`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:426` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`, `ServerWriteMaterialChange`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L581 · 结构体** `ServerWritePreview` — 定义与Server 数据、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L588 · 初始化器** `init(payload: [String: Any], sourceFolders: [String], materials: [ServerWriteMaterialPreview], orders: [ServerWriteOrderPreview], hardwareMappingRequirements: [ServerHardwareMappingRequirement] = [])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`payload: [String: Any]`；`sourceFolders: [String]`；`materials: [ServerWriteMaterialPreview]`；`orders: [ServerWriteOrderPreview]`；`hardwareMappingRequirements: [ServerHardwareMappingRequirement] = []`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L596 · 初始化器** `init?(object: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`object: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:292` `ServerWriteMaterialPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`；是否真实写入仍取决于分支和参数。

- **L613 · 结构体** `ServerFolderChangeGroup` — 定义与Server 数据、文件夹相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L621 · 计算属性** `var requiresManualReview: Bool` — 根据当前状态计算并返回`requiresManualReview` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L626 · 结构体** `PendingCenterItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L640 · 函数** `func serverFolderChangeGroups(_ changes: [ServerChangePreview]) -> [ServerFolderChangeGroup]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`
  - 返回：`[ServerFolderChangeGroup]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:613` `ServerFolderChangeGroup`

- **L659 · 函数** `func buildPendingCenterItems( serverChanges: [ServerChangePreview], currentIssues: [CurrentIssue], aimesReviews: [AimesReviewItem], aimesFormatWarnings: [AimesReviewItem] = [] ) -> [PendingCenterItem]` — 构建与 `buildPendingCenterItems` 对应的数据或步骤。
  - 输入：`serverChanges: [ServerChangePreview]`；`currentIssues: [CurrentIssue]`；`aimesReviews: [AimesReviewItem]`；`aimesFormatWarnings: [AimesReviewItem] = []`
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:640` `serverFolderChangeGroups`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:670` `belongs`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:626` `PendingCenterItem`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `Set`；是否真实写入仍取决于分支和参数。

- **L670 · 函数** `func belongs(_ issue: CurrentIssue, to group: ServerFolderChangeGroup) -> Bool` — 封装 `belongs` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`；`to group: ServerFolderChangeGroup`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L771 · 结构体** `CurrentIssue` — 定义与待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L782 · 结构体** `AimesReviewItem` — 定义与AIMES 数据、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L794 · 函数** `func aimesReviewItems(_ object: [String: Any], key: String) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`key: String`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:782` `AimesReviewItem`

- **L811 · 函数** `func aimesReviewItemsFromWarnings(_ warnings: [[String: Any]]) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ warnings: [[String: Any]]`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:782` `AimesReviewItem`

- **L830 · 函数** `func dashboardActivitySteps( _ object: [String: Any], includeChanges: Bool = true, sessionStartedAt: Date? = nil ) -> [InventoryStep]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`；`sessionStartedAt: Date? = nil`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1318` `dashboardBusinessDate`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L883 · 函数** `func serverChangePreviews(_ rows: [[String: Any]]) -> [ServerChangePreview]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [[String: Any]]`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:255` `ServerChangePreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L904 · 函数** `func serverChangesExcludingFolder( _ changes: [ServerChangePreview], folderPath: String ) -> [ServerChangePreview]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`；`folderPath: String`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:911` `serverChangesExcludingFolders`

- **L911 · 函数** `func serverChangesExcludingFolders( _ changes: [ServerChangePreview], folderPaths: [String] ) -> [ServerChangePreview]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`；`folderPaths: [String]`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L930 · 函数** `func serverChangeTypeName(_ type: String) -> String` — 封装Server 数据、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L940 · 结构体** `OrderPreviewIssue` — 定义与订单、预览、待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L946 · 函数** `func orderPreviewIssues(_ object: [String: Any]) -> [OrderPreviewIssue]` — 封装订单、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`[OrderPreviewIssue]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:940` `OrderPreviewIssue`

- **L956 · 结构体** `OrderMaterialPreview` — 定义与订单、材料、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L965 · 初始化器** `init( kind: String, thickness: Double, color: String, quantity: Double, productCode: String = "", brand: String = "" )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`kind: String`；`thickness: Double`；`color: String`；`quantity: Double`；`productCode: String = ""`；`brand: String = ""`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L982 · 函数** `func orderMaterialDisplayName(_ row: OrderMaterialPreview) -> String` — 封装订单、材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderMaterialPreview`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L993 · 函数** `func orderedMaterialRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`[OrderMaterialPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1024 · 函数** `func orderedEdgeColors(_ colors: [String], matching panels: [OrderMaterialPreview]) -> [String]` — 封装 `orderedEdgeColors` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ colors: [String]`；`matching panels: [OrderMaterialPreview]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1037 · 函数** `func panelColorsNeedingThicknessWarning(_ rows: [OrderMaterialPreview]) -> Set<String>` — 封装 `panelColorsNeedingThicknessWarning` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`Set<String>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L1049 · 结构体** `OrderFactoryPreview` — 定义与订单、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1055 · 结构体** `OrderFittingPreview` — 定义与订单、五金、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1069 · 结构体** `OrderStockPreview` — 定义与订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1081 · 结构体** `OrderCostLine` — 定义与订单、成本相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1096 · 结构体** `OrderCostFactoryTotal` — 定义与订单、成本、工厂单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1103 · 结构体** `InventoryTraveler` — 定义与库存、Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1113 · 函数** `func groupInventoryTravelersByNewest(_ travelers: [InventoryTraveler]) -> [(String, [InventoryTraveler])]` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ travelers: [InventoryTraveler]`
  - 返回：`[(String, [InventoryTraveler])]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1130 · 结构体** `InventoryPreviewRow` — 定义与库存、预览、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1141 · 函数** `func inventoryPreviewCategoryRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1150 · 函数** `func inventoryPreviewPlywoodRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1158 · 函数** `func sortedInventoryPreviewRows(_ rows: [InventoryPreviewRow]) -> [InventoryPreviewRow]` — 排序库存、预览相关数据或步骤。
  - 输入：`_ rows: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1141` `inventoryPreviewCategoryRank`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1150` `inventoryPreviewPlywoodRank`

- **L1174 · 结构体** `InventoryProductCandidate` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1183 · 结构体** `InventoryIgnoredMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1189 · 结构体** `InventoryManualMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1196 · 结构体** `InventoryStep` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1208 · 初始化器** `init( id: UUID = UUID(), time: String, title: String, detail: String, state: String, paths: [String] = [], operationDetails: [String] = [], contextDetails: [String] = [], startedAt: Date? = nil, duration: TimeInterval? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`time: String`；`title: String`；`detail: String`；`state: String`；`paths: [String] = []`；`operationDetails: [String] = []`；`contextDetails: [String] = []`；`startedAt: Date? = nil`；`duration: TimeInterval? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1233 · 函数** `func operationDurationText(_ duration: TimeInterval) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ duration: TimeInterval`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1281` `Double.rounded`

- **L1238 · 函数** `func inventoryFailureNeedsVerification(_ message: String) -> Bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1253 · 结构体** `DashboardOperationDuration` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1258 · 初始化器** `init(id: String? = nil, label: String, duration: TimeInterval)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String? = nil`；`label: String`；`duration: TimeInterval`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1265 · 函数** `func dashboardFlatOperationDurations(_ stages: [[String: Any]]) -> [DashboardOperationDuration]` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stages: [[String: Any]]`
  - 返回：`[DashboardOperationDuration]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1253` `DashboardOperationDuration`

- **L1275 · 结构体** `DashboardOperationStart` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1280 · 扩展** `Double` — 定义 `Double` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1281 · 方法** `func rounded(toPlaces places: Int) -> Double` — 封装 `rounded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`toPlaces places: Int`
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`

- **L1287 · 函数** `func dashboardClockTime(_ date: Date = Date()) -> String` — 封装看板、时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date = Date()`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1291 · 函数** `func dashboardInventoryProgressText(_ message: String) -> String` — 封装看板、库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1314 · 函数** `func appDisplayTimestamp(_ value: String) -> String` — 封装 `appDisplayTimestamp` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1318 · 函数** `func dashboardBusinessDate(_ value: String) -> Date?` — 封装看板、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`Date?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1336 · 函数** `func dashboardTimestamp(_ value: String, isInSameMonthAs reference: Date, calendar: Calendar = .current) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`；`isInSameMonthAs reference: Date`；`calendar: Calendar = .current`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1318` `dashboardBusinessDate`

- **L1341 · 函数** `func updatingLatestRunningStep(_ steps: [InventoryStep], detail: String) -> [InventoryStep]?` — 封装 `updatingLatestRunningStep` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`detail: String`
  - 返回：`[InventoryStep]?`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L1360 · 函数** `func appendingInventoryProgressStep(_ steps: [InventoryStep], message: String) -> [InventoryStep]` — 封装库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`message: String`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L1389 · 函数** `func orderUpdateActionReady(existingTravelerPath: String, selectedOrderPath: String, selectedOrderId: String) -> Bool` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`；`selectedOrderPath: String`；`selectedOrderId: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1393 · 函数** `func orderTravelerOpenActionReady(existingTravelerPath: String) -> Bool` — 封装订单、Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1398 · 结构体** `TodoItem` — 定义与待办、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1405 · 初始化器** `init( id: UUID = UUID(), content: String, startedAt: Date = Date(), deadline: Date?, completedAt: Date? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`content: String`；`startedAt: Date = Date()`；`deadline: Date?`；`completedAt: Date? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1420 · 结构体** `AssistantTaskItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1426 · 类** `ResidentOrderServiceClient` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1436 · 初始化器** `init(onProgress: @escaping (String) -> Void)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`onProgress: @escaping (String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1440 · 方法** `func start(command: URL, environment: [String: String]) throws` — 启动与 `start` 对应的数据或步骤。
  - 输入：`command: URL`；`environment: [String: String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run`；是否真实写入仍取决于分支和参数。

- **L1460 · 方法** `func request(id: String, arguments: [String], inputData: Data?) throws -> Data` — 封装 `request` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`id: String`；`arguments: [String]`；`inputData: Data?`
  - 返回：`Data`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`；是否真实写入仍取决于分支和参数。

- **L1492 · 方法** `func stop()` — 封装 `stop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `closeFile`；是否真实写入仍取决于分支和参数。

- **L1512 · 类** `AppModel` — 定义 `AppModel` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1567 · 枚举** `PendingMappingResumeAction` — 定义与映射相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1668 · 计算属性** `var pendingCenterItems: [PendingCenterItem]` — 根据当前状态计算并返回`pendingCenterItems` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:659` `buildPendingCenterItems`

- **L1677 · 计算属性** `var hasAimesHistory: Bool` — 根据当前状态计算并返回AIMES 数据。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1681 · 计算属性** `var orderPreviewReady: Bool` — 根据当前状态计算并返回订单、预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1685 · 计算属性** `var orderCanGenerateTraveler: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1689 · 计算属性** `var orderTravelerOpenReady: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1393` `orderTravelerOpenActionReady`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L1693 · 计算属性** `var activeOwnedSourceRoot: String` — 根据当前状态计算并返回来源。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1697 · 计算属性** `var activeCutToSizeRoot: String` — 根据当前状态计算并返回`activeCutToSizeRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1703 · 计算属性** `var activeOrderRoot: String` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1707 · 计算属性** `var activeBackupRoot: String` — 根据当前状态计算并返回备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1711 · 计算属性** `var databaseBackupRoot: String` — 根据当前状态计算并返回数据库、备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1715 · 初始化器** `init()` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1867` `AppModel.loadSettings`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1786` `AppModel.loadTodoItems`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1728` `AppModel.startResidentOrderService`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setEnabled`, `record`；是否真实写入仍取决于分支和参数。

- **L1728 · 方法** `private func startResidentOrderService()` — 启动订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4360` `AppModel.consumeOrderLogChunk`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1440` `ResidentOrderServiceClient.start`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2002` `AppModel.environmentForOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1973` `AppModel.newOperationID`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1749 · 方法** `func checkBackupReminder()` — 检查备份相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L1758 · 方法** `func performBackup()` — 执行手动/计划备份并把结果映射为 App 状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L1776 · 计算属性** `private var settingsURL: URL` — 设置设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1781 · 计算属性** `var todoDataURL: URL` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1786 · 方法** `func loadTodoItems()` — 读取待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L1801 · 方法** `func addTodo(content: String, deadline: Date?)` — 新增待办相关数据或步骤。
  - 输入：`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1398` `TodoItem`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1837` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1812 · 方法** `func updateTodo(_ item: TodoItem, content: String, deadline: Date?)` — 更新待办相关数据或步骤。
  - 输入：`_ item: TodoItem`；`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1837` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1824 · 方法** `func toggleTodoCompletion(_ item: TodoItem)` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1837` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1831 · 方法** `func deleteTodo(_ item: TodoItem)` — 删除待办相关数据或步骤。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1837` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1837 · 方法** `private func saveTodoItems()` — 保存待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L1867 · 方法** `func loadSettings() -> Bool` — 读取设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1886 · 方法** `func saveSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`tests/test_inventory.py:75` `_FakeNodeInput.write`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L1915 · 计算属性** `var operationLogURL: URL` — 根据当前状态计算并返回操作、日志。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1920 · 方法** `func setOperationLogEnabled(_ enabled: Bool)` — 设置操作、日志相关数据或步骤。
  - 输入：`_ enabled: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1886` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`, `setEnabled`, `saveSettings`；是否真实写入仍取决于分支和参数。

- **L1942 · 方法** `func refreshOperationLogInfo()` — 刷新操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1946 · 方法** `func trimOperationLog()` — 封装操作、日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1942` `AppModel.refreshOperationLogInfo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1969 · 方法** `func logUserAction(_ action: String, details: [String: Any] = [:])` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ action: String`；`details: [String: Any] = [:]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1973 · 方法** `func newOperationID(_ name: String, details: [String: Any] = [:]) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`details: [String: Any] = [:]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1984 · 方法** `private func finishOperationLog( _ operationID: String, name: String, startedAt: Date, exitStatus: Int32 )` — 结束并收口操作、日志相关数据或步骤。
  - 输入：`_ operationID: String`；`name: String`；`startedAt: Date`；`exitStatus: Int32`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2002 · 方法** `func environmentForOperation(_ operationID: String) -> [String: String]` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ operationID: String`
  - 返回：`[String: String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2010 · 方法** `func saveAllSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1886` `AppModel.saveSettings`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2034` `AppModel.saveJdyPassword`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2085` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `saveJdyPassword`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L2034 · 方法** `func saveJdyPassword()` — 保存与 `saveJdyPassword` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `SecItemDelete`, `SecItemUpdate`, `SecItemCopyMatching`；是否真实写入仍取决于分支和参数。

- **L2085 · 方法** `func saveAimesPassword()` — 保存AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1886` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `SecItemDelete`；是否真实写入仍取决于分支和参数。

- **L2106 · 方法** `private func applyDashboardObject(_ object: [String: Any], includeChanges: Bool = true)` — 应用看板相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2218` `AppModel.applyDashboardOperationTrace`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2201` `AppModel.applyCurrentIssues`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:251` `dashboardOrderRows`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:91` `OrderDashboardFactory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:225` `OrderDashboardItem`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:830` `dashboardActivitySteps`

- **L2185 · 方法** `private func presentServerWritePreview(_ object: [String: Any])` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:581` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2201 · 方法** `private func applyCurrentIssues(from object: [String: Any])` — 应用与 `applyCurrentIssues` 对应的数据或步骤。
  - 输入：`from object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:771` `CurrentIssue`

- **L2218 · 方法** `private func applyDashboardOperationTrace(_ object: [String: Any])` — 应用看板、操作相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2230 · 方法** `private func applyAimesReviewObject(_ object: [String: Any], presentIfNeeded: Bool = true)` — 应用AIMES 数据相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:794` `aimesReviewItems`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:811` `aimesReviewItemsFromWarnings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L2248 · 方法** `private func closePendingCenterIfEmpty()` — 关闭与 `closePendingCenterIfEmpty` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2254 · 方法** `private func beginDashboardOperation(_ source: String, label: String, continuing: Bool = false)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`；`label: String`；`continuing: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1275` `DashboardOperationStart`

- **L2266 · 方法** `private func finishDashboardOperation(_ source: String)` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1253` `DashboardOperationDuration`

- **L2279 · 方法** `private func finishDashboardOperation( _ source: String, backendSeconds: Double, stages: [[String: Any]] )` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`backendSeconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1265` `dashboardFlatOperationDurations`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1253` `DashboardOperationDuration`

- **L2305 · 方法** `private func finishDashboardOperation(_ source: String, using object: [String: Any])` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`using object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2318 · 方法** `private func discardDashboardOperationTimer(_ source: String)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2322 · 方法** `private func applyAuthoritativeDashboardTiming( _ source: String, seconds: Double, stages: [[String: Any]] )` — 应用看板相关数据或步骤。
  - 输入：`_ source: String`；`seconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1265` `dashboardFlatOperationDurations`

- **L2333 · 方法** `func startOrderDashboard()` — 启动订单中心初始化链路，加载缓存并安排 AIMES/Server 刷新。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2339` `AppModel.loadOrderDashboardCache`

- **L2339 · 方法** `func loadOrderDashboardCache()` — 读取订单、看板、缓存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2230` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2446` `AppModel.syncDashboardAimes`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2361 · 方法** `func refreshDashboardOrdersAfterOutbound()` — 刷新看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2380 · 方法** `private func startPendingDashboardOutboundRefreshIfNeeded()` — 启动看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2361` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L2388 · 方法** `private func runDailyBackupAfterLocalCache(completion: @escaping () -> Void)` — 执行备份、缓存相关数据或步骤。
  - 输入：`completion: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2413 · 方法** `func autoResolveCurrentIssue(_ issue: CurrentIssue)` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2428 · 方法** `func resolveCurrentIssue(_ issue: CurrentIssue, orderID: String)` — 解析并确定待处理问题相关数据或步骤。
  - 输入：`_ issue: CurrentIssue`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2446 · 方法** `func syncDashboardAimes(force: Bool, scanServerAfter: Bool = false)` — 从 App 发起 AIMES 同步，解析结果并衔接后续看板刷新。
  - 输入：`force: Bool`；`scanServerAfter: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2620` `AppModel.scanDashboardServer`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2318` `AppModel.discardDashboardOperationTimer`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2322` `AppModel.applyAuthoritativeDashboardTiming`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2230` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2507 · 方法** `func toggleAimesReviewSelection(_ item: AimesReviewItem)` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`

- **L2517 · 方法** `func ignoreSelectedAimesFactories()` — 忽略AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2230` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2543 · 方法** `func restoreAimesFactory(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2230` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2563 · 方法** `func assignAimesFactoryToSuggestedOrder(_ item: AimesReviewItem)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2568` `AppModel.assignAimesFactoryToOrder`

- **L2568 · 方法** `func assignAimesFactoryToOrder(_ item: AimesReviewItem, orderID: String)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2230` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2600 · 方法** `func restoreAimesFactoryAssignment(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2230` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2620 · 方法** `func scanDashboardServer(background: Bool = false, presentIfNeeded: Bool = true)` — 从 App 发起 Server 扫描并把变化、问题和耗时写入看板状态。
  - 输入：`background: Bool = false`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2201` `AppModel.applyCurrentIssues`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2218` `AppModel.applyDashboardOperationTrace`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:883` `serverChangePreviews`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2656 · 方法** `func toggleServerFolderSelection(_ folderPath: String)` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folderPath: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:640` `serverFolderChangeGroups`

- **L2668 · 方法** `func clearServerFolderSelection()` — 清理Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`

- **L2673 · 方法** `func processPendingServerChanges()` — 按当前选择为 Server 变化生成业务预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:640` `serverFolderChangeGroups`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2185` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2705 · 方法** `func confirmServerWrite(orderID: String, factoryOrder: String)` — 确认并执行 Server 事实写入，然后只做所需的本地看板刷新。
  - 输入：`orderID: String`；`factoryOrder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:517` `ServerWriteOrderPreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:581` `ServerWritePreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2852` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `ServerWriteOrderPreview`, `ServerWritePreview`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L2784 · 方法** `func confirmServerMaterialPreview(skipHardwareOrderIDs: Set<String> = [])` — 封装Server 数据、材料、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`skipHardwareOrderIDs: Set<String> = []`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2852` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L2852 · 方法** `func refreshDashboardAfterServerWrite(processedFolders: [String])` — 刷新看板、Server 数据相关数据或步骤。
  - 输入：`processedFolders: [String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:911` `serverChangesExcludingFolders`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2875 · 方法** `private func applyServerIndexResult(_ object: [String: Any])` — 应用Server 数据、结果相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2230` `AppModel.applyAimesReviewObject`

- **L2880 · 方法** `func prepareSelectedServerFolder(_ folderURL: URL)` — 准备并校验Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2886 · 方法** `func processSelectedServerFolder(_ folderURL: URL, includeHardware: Bool)` — 处理Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`；`includeHardware: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2185` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2924 · 方法** `func markTemporaryFolderManual(_ folderPath: String)` — 标记文件夹相关数据或步骤。
  - 输入：`_ folderPath: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2201` `AppModel.applyCurrentIssues`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:904` `serverChangesExcludingFolder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2951 · 方法** `func loadInventory()` — 加载可处理的库存/Traveler 列表及目录状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1103` `InventoryTraveler`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3077` `AppModel.activatePendingInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `Set`；是否真实写入仍取决于分支和参数。

- **L2994 · 方法** `func requestInventoryMapping(folderPath: String, message: String = "")` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folderPath: String`；`message: String = ""`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:69` `inventoryMappingSourceFolderPath`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3018` `AppModel.inventoryMappingNames`

- **L3010 · 方法** `func closeInventoryMappingWorkspace()` — 关闭库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3018 · 方法** `private func inventoryMappingNames(from message: String) -> [String]` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from message: String`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3028 · 方法** `private func rereadPendingSourceFolder()` — 封装来源、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3048` `AppModel.refreshDashboardOrdersAfterInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3048 · 方法** `private func refreshDashboardOrdersAfterInventoryMapping()` — 刷新看板、库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2248` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L3072 · 方法** `private func resumePendingMappingOperationAfterMapping()` — 封装映射、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3028` `AppModel.rereadPendingSourceFolder`

- **L3077 · 方法** `func activatePendingInventoryMapping()` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3257` `AppModel.previewSelectedInventory`

- **L3117 · 方法** `func openInventoryChrome()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3130 · 方法** `func updateInventoryCatalog()` — 更新库存、商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5154` `inventoryCatalogUpdateFailureStatus`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `inventoryCatalogUpdateFailureStatus`, `inventoryCatalogUpdateSuccessStatus`；是否真实写入仍取决于分支和参数。

- **L3158 · 方法** `func closeInventoryChromeOnQuit()` — 关闭库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`, `record`；是否真实写入仍取决于分支和参数。

- **L3188 · 方法** `func refreshInventoryCatalogStatus()` — 刷新库存、商品目录、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3198 · 方法** `func refreshInventoryFolder(_ folder: String)` — 刷新库存、文件夹相关数据或步骤。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3230` `AppModel.reloadInventoryFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3230 · 方法** `private func reloadInventoryFolder(_ folder: String)` — 封装库存、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1103` `InventoryTraveler`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3257 · 方法** `func previewSelectedInventory()` — 为当前选中对象串行生成库存需求和可用量预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3290` `AppModel.previewOrderInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4074` `AppModel.previewNext`

- **L3290 · 方法** `func previewOrderInventory( orderID: String, factoryOrderNames: [String], factoryOrders: [String] = [], productionBatchNumber: String = "", shipmentOnly: Bool = false )` — 预览预览、订单、库存相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrderNames: [String]`；`factoryOrders: [String] = []`；`productionBatchNumber: String = ""`；`shipmentOnly: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4062` `AppModel.applyInventoryPreviewObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4274` `AppModel.finishInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`；是否真实写入仍取决于分支和参数。

- **L3331 · 方法** `func loadProductionPreview(orderID: String, factoryOrders: [String], completion: @escaping (Bool) -> Void = { _ in })` — 读取当前选择的生产材料预览并填充编辑草稿。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:106` `ProductionMaterialDraft`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3369 · 方法** `func prepareProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], onResult completion: @escaping (String?, String?) -> Void )` — 从 App 提交生产准备参数并处理后端返回。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`onResult completion: @escaping (String?, String?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3386 · 方法** `func startDirectProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], batchNumber: String, completion: @escaping (ProductionOperationResult) -> Void = { _ in } )` — 执行用户确认后的生产完成流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`batchNumber: String`；`completion: @escaping (ProductionOperationResult) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:206` `ProductionOperationResult`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1238` `inventoryFailureNeedsVerification`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2361` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L3504 · 方法** `func startDirectOrderShipment(orderID: String, factoryOrders: [String])` — 执行用户确认后的订单出库流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2254` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2361` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L3584 · 方法** `func loadOutboundScope( orderID: String, factoryOrders: [String], completion: @escaping ([String: Any]?) -> Void )` — 读取出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping ([String: Any]?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3606 · 方法** `func saveOutboundScope( orderID: String, scopeType: String, requirement: String, factoryOrder: String = "", reason: String, completion: @escaping (Bool) -> Void = { _ in } )` — 保存出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`scopeType: String`；`requirement: String`；`factoryOrder: String = ""`；`reason: String`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3635 · 方法** `func openAndFillSelectedInventory()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3727` `AppModel.markInventoryTravelerSaved`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3727 · 方法** `private func markInventoryTravelerSaved(path: String, documentNumber: String)` — 标记库存、Traveler相关数据或步骤。
  - 输入：`path: String`；`documentNumber: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1103` `InventoryTraveler`

- **L3742 · 方法** `func setInventoryItemsIgnored(_ names: [String], ignored: Bool)` — 设置库存相关数据或步骤。
  - 输入：`_ names: [String]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3257` `AppModel.previewSelectedInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3028` `AppModel.rereadPendingSourceFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`；是否真实写入仍取决于分支和参数。

- **L3768 · 方法** `func refreshInventoryMappings()` — 刷新库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1189` `InventoryManualMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1183` `InventoryIgnoredMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3791 · 方法** `func saveSettingsManualMapping(name: String, productCode: String, displayName: String)` — 保存设置、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`；`displayName: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3808 · 方法** `func updateSettingsManualMapping(oldName: String, name: String, productCode: String, displayName: String)` — 更新设置、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`productCode: String`；`displayName: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3827 · 方法** `func removeSettingsManualMapping(name: String)` — 移除设置、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3837 · 方法** `func saveInventoryIgnoredMapping(name: String, reason: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3028` `AppModel.rereadPendingSourceFolder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3862 · 方法** `func updateInventoryIgnoredMapping(oldName: String, name: String, reason: String)` — 更新库存、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3884 · 方法** `func removeInventoryIgnoredMapping(name: String)` — 移除库存、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3894 · 方法** `func searchInventoryProducts(_ query: String)` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ query: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1174` `InventoryProductCandidate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3921 · 方法** `func saveInventoryMapping(travelerName: String, productCode: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`travelerName: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3072` `AppModel.resumePendingMappingOperationAfterMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3942 · 方法** `func saveServerHardwareMapping(name: String, productCode: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3972` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3957 · 方法** `func saveServerHardwareIgnoredMapping(name: String, reason: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4244` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3972` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3972 · 方法** `private func removeServerHardwareMappingRequirement(_ name: String)` — 移除Server 数据、五金、映射相关数据或步骤。
  - 输入：`_ name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:581` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3987 · 方法** `private func consumeInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] ) -> [InventoryPreviewRow]` — 消费并转换库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1130` `InventoryPreviewRow`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`

- **L4062 · 方法** `private func applyInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] )` — 应用库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1158` `sortedInventoryPreviewRows`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3987` `AppModel.consumeInventoryPreviewObject`

- **L4074 · 方法** `private func previewNext( _ paths: [String], index: Int, selectedDocumentRemarks: Set<String> = [], accumulated: [InventoryPreviewRow] )` — 预览预览相关数据或步骤。
  - 输入：`_ paths: [String]`；`index: Int`；`selectedDocumentRemarks: Set<String> = []`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1158` `sortedInventoryPreviewRows`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4112` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3987` `AppModel.consumeInventoryPreviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4112 · 方法** `private func runInventory( _ arguments: [String], manageRunning: Bool = true, onFailure: ((String) -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动库存 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`manageRunning: Bool = true`；`onFailure: ((String) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1973` `AppModel.newOperationID`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2002` `AppModel.environmentForOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4293` `AppModel.consumeInventoryLogChunk`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1984` `AppModel.finishOperationLog`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4260` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L4244 · 方法** `private func beginInventoryOperation(_ title: String)` — 封装库存、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`

- **L4249 · 方法** `private func addInventoryStep(_ title: String, _ detail: String, _ state: String)` — 新增库存相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4260 · 方法** `private func finishRunningInventoryStep(_ detail: String, _ state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4249` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4274 · 方法** `private func finishInventoryStep(named title: String, detail: String, state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`named title: String`；`detail: String`；`state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L4293 · 方法** `private func consumeInventoryLogChunk(_ chunk: String)` — 消费并转换库存、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1360` `appendingInventoryProgressStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1291` `dashboardInventoryProgressText`

- **L4314 · 方法** `private func addOrderStep(_ title: String, _ detail: String, _ state: String)` — 新增订单相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4333 · 方法** `private func finishOrderStep(_ detail: String, _ state: String)` — 结束并收口订单相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4360 · 方法** `private func consumeOrderLogChunk(_ chunk: String)` — 消费并转换订单、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1341` `updatingLatestRunningStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`

- **L4380 · 方法** `private func runOrder( _ arguments: [String], input: Data? = nil, failureStatus: String = "校验未通过", onFailure: (() -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动订单 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`input: Data? = nil`；`failureStatus: String = "校验未通过"`；`onFailure: (() -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1973` `AppModel.newOperationID`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4360` `AppModel.consumeOrderLogChunk`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1440` `ResidentOrderServiceClient.start`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2002` `AppModel.environmentForOperation`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1460` `ResidentOrderServiceClient.request`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1984` `AppModel.finishOperationLog`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2380` `AppModel.startPendingDashboardOutboundRefreshIfNeeded`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `startPendingDashboardOutboundRefreshIfNeeded`；是否真实写入仍取决于分支和参数。

- **L4475 · 方法** `func stopResidentOrderService()` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1492` `ResidentOrderServiceClient.stop`

- **L4480 · 方法** `func loadOrderFolders()` — 读取订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:85` `OrderFolderItem`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4518 · 方法** `func previewOrderFolder(_ item: OrderFolderItem, recordSelection: Bool = true)` — 预览预览、订单、文件夹相关数据或步骤。
  - 输入：`_ item: OrderFolderItem`；`recordSelection: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4594` `AppModel.findLocalOrderTraveler`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:946` `orderPreviewIssues`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4628` `AppModel.applyOrderPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4594 · 方法** `private func findLocalOrderTraveler(_ orderId: String) -> String` — 查找订单、Traveler相关数据或步骤。
  - 输入：`_ orderId: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4628 · 方法** `private func applyOrderPreview(_ object: [String: Any], targetOrderID: String? = nil)` — 应用订单、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`targetOrderID: String? = nil`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:956` `OrderMaterialPreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1049` `OrderFactoryPreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1055` `OrderFittingPreview`

- **L4683 · 方法** `func loadOrderDetailFromDatabase(_ item: OrderDashboardItem)` — 读取订单、数据库相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4753` `AppModel.schedulePendingOrderDetailRetry`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4628` `AppModel.applyOrderPreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4753 · 方法** `private func schedulePendingOrderDetailRetry()` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4683` `AppModel.loadOrderDetailFromDatabase`

- **L4771 · 方法** `func saveOrderAnnotations( orderID: String, userNote: String, plannedDays: [OrderInstallationDay], actualDays: [OrderInstallationDay], onStatusChange: @escaping (String) -> Void = { _ in } )` — 保存安装日期、安装人等订单人工备注并刷新详情。
  - 输入：`orderID: String`；`userNote: String`；`plannedDays: [OrderInstallationDay]`；`actualDays: [OrderInstallationDay]`；`onStatusChange: @escaping (String) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2106` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4819 · 方法** `func setOrderFittingsIgnored(_ rows: [OrderFittingPreview], ignored: Bool)` — 设置订单相关数据或步骤。
  - 输入：`_ rows: [OrderFittingPreview]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4518` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runOrder`；是否真实写入仍取决于分支和参数。

- **L4848 · 方法** `func generateSelectedOrder()` — 生成订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5003` `AppModel.openSelectedOrderTraveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `openSelectedOrderTraveler`；是否真实写入仍取决于分支和参数。

- **L4872 · 方法** `func generateMissingMaterial()` — 生成材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4518` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4895 · 方法** `func checkSelectedOrderStock()` — 检查订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1069` `OrderStockPreview`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4937 · 方法** `func calculateSelectedOrderCost(export: Bool = false)` — 计算订单、成本相关数据或步骤。
  - 输入：`export: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4380` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4967` `AppModel.applyOrderCost`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4333` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `open`；是否真实写入仍取决于分支和参数。

- **L4967 · 方法** `private func applyOrderCost(_ object: [String: Any])` — 应用订单、成本相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1081` `OrderCostLine`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1096` `OrderCostFactoryTotal`

- **L5003 · 方法** `func openSelectedOrderTraveler()` — 打开订单、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4314` `AppModel.addOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L5021 · 方法** `func openDashboardLocation(_ path: String)` — 打开看板相关数据或步骤。
  - 输入：`_ path: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L5034 · 计算属性** `var projectRoot: URL` — 根据当前状态计算并返回`projectRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5042 · 枚举** `AppLayout` — 定义 `AppLayout` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5091 · 结构体** `FixedWindowSizeController` — 定义 `FixedWindowSizeController` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5094 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5108` `FixedWindowSizeController.applyFixedSize`

- **L5102 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5108` `FixedWindowSizeController.applyFixedSize`

- **L5108 · 方法** `private func applyFixedSize(to window: NSWindow?)` — 应用与 `applyFixedSize` 对应的数据或步骤。
  - 输入：`to window: NSWindow?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setFrame`；是否真实写入仍取决于分支和参数。

- **L5122 · 函数** `func inventoryActionColumnCount(availableWidth: CGFloat) -> Int` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`availableWidth: CGFloat`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5127 · 枚举** `AppPalette` — 定义 `AppPalette` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5141 · 函数** `func inventoryCatalogUpdateSuccessStatus(_ count: Int) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5145 · 函数** `func inventoryCatalogUpdateSuccessStatus( _ count: Int, added: Int, updated: Int, removed: Int ) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`；`added: Int`；`updated: Int`；`removed: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5154 · 函数** `func inventoryCatalogUpdateFailureStatus(_ reason: String) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ reason: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5158 · 枚举** `SettingsStatusKind` — 定义与设置、状态相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5165 · 计算属性** `var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5175 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5186 · 函数** `func settingsStatusKind(_ status: String) -> SettingsStatusKind` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`SettingsStatusKind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5195 · 函数** `func settingsStatusDisplayText(_ status: String) -> String` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5201 · 结构体** `SettingsStatusBanner` — 定义与设置、状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5204 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5186` `settingsStatusKind`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5195` `settingsStatusDisplayText`

- **L5232 · 扩展** `View` — 定义 `View` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5233 · 方法** `func appPageFrame() -> some View` — 封装 `appPageFrame` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5261` `AppGlassGroupBoxStyle`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5294` `LiquidGlassPreviewBackdrop`

- **L5241 · 方法** `func appInputField(maxWidth: CGFloat? = nil) -> some View` — 封装 `appInputField` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`maxWidth: CGFloat? = nil`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5245 · 方法** `func appActionButton(minWidth: CGFloat = AppLayout.actionButtonWidth) -> some View` — 封装 `appActionButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.actionButtonWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5250 · 方法** `func inventoryActionButton(minWidth: CGFloat = AppLayout.inventoryActionMinWidth) -> some View` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.inventoryActionMinWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5261 · 结构体** `AppGlassGroupBoxStyle` — 定义 `AppGlassGroupBoxStyle` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5262 · 方法** `func makeBody(configuration: Configuration) -> some View` — 创建与 `makeBody` 对应的数据或步骤。
  - 输入：`configuration: Configuration`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5275 · 结构体** `AppSurfaceCard<Content` — 定义 `AppSurfaceCard<Content` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5279 · 初始化器** `init(padding: CGFloat = AppLayout.cardPadding, @ViewBuilder content: () -> Content)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`padding: CGFloat = AppLayout.cardPadding`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5284 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5294 · 结构体** `LiquidGlassPreviewBackdrop` — 定义与预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5295 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5329 · 结构体** `AppStatusBadge` — 定义与状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5330 · 枚举** `Kind` — 定义 `Kind` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5335 · 计算属性** `private var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5345 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5360 · 结构体** `WidthPreferenceKey` — 定义 `WidthPreferenceKey` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5363 · 方法** `static func reduce(value: inout CGFloat, nextValue: () -> CGFloat)` — 封装 `reduce` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: inout CGFloat`；`nextValue: () -> CGFloat`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5368 · 结构体** `ScrollingTextOnHover` — 定义 `ScrollingTextOnHover` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5379 · 计算属性** `private var overflow: CGFloat` — 根据当前状态计算并返回`overflow` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5383 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5418` `ScrollingTextOnHover.startScrolling`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5440` `ScrollingTextOnHover.stopScrolling`

- **L5418 · 方法** `private func startScrolling()` — 启动与 `startScrolling` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1280` `Double`

- **L5440 · 方法** `private func stopScrolling()` — 封装 `stopScrolling` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5447 · 结构体** `InventoryActionGrid<Content` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5451 · 初始化器** `init( minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5459 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5469 · 结构体** `AppPageHeader<Trailing` — 定义 `AppPageHeader<Trailing` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5475 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5480 · 结构体** `OperationLogCard` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5485 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5491 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6055` `SelectableOperationLogView`

- **L5501 · 结构体** `OrderWorkflowView` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5505 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5329` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4480` `AppModel.loadOrderFolders`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4518` `AppModel.previewOrderFolder`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1314` `appDisplayTimestamp`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4895` `AppModel.checkSelectedOrderStock`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5480` `OperationLogCard`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5894` `OrderWorkflowView.summaryCard`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5914` `OrderWorkflowView.subsectionTitle`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1037` `panelColorsNeedingThicknessWarning`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:993` `orderedMaterialRows`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:982` `orderMaterialDisplayName`；另有 4 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `setOrderFittingsIgnored`；是否真实写入仍取决于分支和参数。

- **L5894 · 方法** `private func summaryCard(title: String, value: String, detail: String, color: Color, warning: Bool = false) -> some View` — 封装 `summaryCard` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`value: String`；`detail: String`；`color: Color`；`warning: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5914 · 方法** `private func subsectionTitle(_ title: String, color: Color) -> some View` — 封装 `subsectionTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5921 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5931 · 结构体** `SettingsCard<Content` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5937 · 初始化器** `init( title: String, symbol: String, padding: CGFloat = 14, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`title: String`；`symbol: String`；`padding: CGFloat = 14`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5949 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5963 · 结构体** `InventoryStepRowView` — 定义与库存、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5967 · 初始化器** `init(step: InventoryStep, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`step: InventoryStep`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5972 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L6000 · 计算属性** `private var detailText: String` — 根据当前状态计算并返回`detailText` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1233` `operationDurationText`

- **L6006 · 计算属性** `@ViewBuilder private var icon: some View` — 根据当前状态计算并返回`icon` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6021 · 结构体** `InventoryOperationLogView` — 定义与库存、操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6024 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6055` `SelectableOperationLogView`

- **L6032 · 结构体** `OperationLogAutoScroller` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6035 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6039 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6055 · 结构体** `SelectableOperationLogView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6061 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6067 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6141` `SelectableOperationLogView.copySelected`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6129` `SelectableOperationLogView.select`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5963` `InventoryStepRowView`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6032` `OperationLogAutoScroller`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copySelected`, `Set`；是否真实写入仍取决于分支和参数。

- **L6124 · 计算属性** `private var scrollRevision: String` — 根据当前状态计算并返回`scrollRevision` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6129 · 方法** `private func select(_ id: UUID)` — 选择与 `select` 对应的数据或步骤。
  - 输入：`_ id: UUID`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L6141 · 方法** `private func copySelected()` — 封装 `copySelected` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1233` `operationDurationText`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L6161 · 结构体** `InventoryTravelerRowView` — 定义与库存、Traveler、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6167 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5368` `ScrollingTextOnHover`

- **L6198 · 计算属性** `private var statusColor: Color` — 根据当前状态计算并返回状态、颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6208 · 结构体** `InventoryMappingSheet` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6215 · 初始化器** `init( model: AppModel, travelerName: String, isPresented: Binding<Bool>, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`isPresented: Binding<Bool>`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6227 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5241` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3894` `AppModel.searchInventoryProducts`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3921` `AppModel.saveInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryMapping`；是否真实写入仍取决于分支和参数。

- **L6294 · 结构体** `PendingInventoryMappingTarget` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6296 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6299 · 结构体** `PendingInventoryMappingWorkspace` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6304 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5329` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6294` `PendingInventoryMappingTarget`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3010` `AppModel.closeInventoryMappingWorkspace`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5294` `LiquidGlassPreviewBackdrop`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6208` `InventoryMappingSheet`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6387` `PendingInventoryIgnoreSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryMappingWorkspace`；是否真实写入仍取决于分支和参数。

- **L6387 · 结构体** `PendingInventoryIgnoreSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6394 · 初始化器** `init( model: AppModel, travelerName: String, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6404 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5241` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3837` `AppModel.saveInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5294` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L6452 · 结构体** `InventoryView` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6463 · 初始化器** `init( model: AppModel, onClose: (() -> Void)? = nil, orderContextID: String = "", orderContextFactoryNames: [String] = [], orderContextFactoryOrders: [String] = [] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`onClose: (() -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6477 · 计算属性** `private var selectedTravelerCount: Int` — 选择Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6481 · 计算属性** `private var hasMappedOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6485 · 计算属性** `private var hasConfirmedNoOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6491 · 计算属性** `private var customerSuppliedOnly: Bool` — 根据当前状态计算并返回`customerSuppliedOnly` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L6498 · 计算属性** `private var confirmationTitle: String` — 根据当前状态计算并返回`confirmationTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6505 · 计算属性** `private var selectedTravelerDisplayName: String` — 选择Traveler、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6510 · 方法** `private func previewRowContent(_ row: InventoryPreviewRow) -> some View` — 预览预览、行数据相关数据或步骤。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6777` `InventoryView.previewStatusColor`

- **L6546 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5329` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6754` `InventoryView.outboundStep`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5480` `OperationLogCard`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6510` `InventoryView.previewRowContent`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5250` `View.inventoryActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3290` `AppModel.previewOrderInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6208` `InventoryMappingSheet`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6768` `InventoryView.confirmationRow`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3635` `AppModel.openAndFillSelectedInventory`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5294` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outboundStep`, `onClose`, `openAndFillSelectedInventory`；是否真实写入仍取决于分支和参数。

- **L6745 · 方法** `private func statusColor(_ status: String) -> Color` — 封装状态、颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6754 · 方法** `private func outboundStep(_ number: Int, _ title: String, active: Bool) -> some View` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ number: Int`；`_ title: String`；`active: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6768 · 方法** `private func confirmationRow(_ label: String, _ value: String, valueColor: Color = .primary) -> some View` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ label: String`；`_ value: String`；`valueColor: Color = .primary`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6777 · 方法** `private func previewStatusColor(_ status: String) -> Color` — 预览预览、状态、颜色相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6786 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6796 · 方法** `private func stepIcon(_ state: String) -> some View` — 封装 `stepIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6810 · 结构体** `TodoView` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6819 · 计算属性** `private var sortedItems: [TodoItem]` — 排序与 `sortedItems` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[TodoItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6840 · 计算属性** `private var selectedItem: TodoItem?` — 选择项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`TodoItem?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6845 · 计算属性** `private var openCount: Int` — 打开与 `openCount` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6849 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5329` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7001` `TodoView.todoRow`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1824` `AppModel.toggleTodoCompletion`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7114` `TodoDeadlinePickerControl`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5233` `View.appPageFrame`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7167` `TodoEditorSheet`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1831` `AppModel.deleteTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `deleteTodo`；是否真实写入仍取决于分支和参数。

- **L7001 · 方法** `private func todoRow(_ item: TodoItem) -> some View` — 封装待办、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7074` `TodoView.deadlineText`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7094` `TodoView.deadlineColor`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7082` `TodoView.deadlineBadge`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1824` `AppModel.toggleTodoCompletion`

- **L7054 · 计算属性** `private var todoSelectionMessage: String?` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7059 · 计算属性** `private var deleteAlertBinding: Binding<Bool>` — 删除与 `deleteAlertBinding` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Binding<Bool>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7066 · 方法** `private func addTodo()` — 新增待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7074 · 方法** `private func deadlineText(_ date: Date?) -> String` — 封装 `deadlineText` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date?`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7082 · 方法** `private func deadlineBadge(_ item: TodoItem) -> String?` — 封装 `deadlineBadge` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7094 · 方法** `private func deadlineColor(_ item: TodoItem) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7106 · 函数** `func todoDeadlinePickerDisplay(_ date: Date) -> String` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7114 · 结构体** `TodoDeadlinePickerControl` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7118 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7106` `todoDeadlinePickerDisplay`

- **L7167 · 结构体** `TodoEditorSheet` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7175 · 初始化器** `init(model: AppModel, item: TodoItem)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`item: TodoItem`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7187 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5241` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7114` `TodoDeadlinePickerControl`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1812` `AppModel.updateTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateTodo`；是否真实写入仍取决于分支和参数。

- **L7216 · 结构体** `SettingsView` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7223 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5329` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7521` `SettingsView.compactStatus`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2010` `AppModel.saveAllSettings`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5233` `View.appPageFrame`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3188` `AppModel.refreshInventoryCatalogStatus`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1942` `AppModel.refreshOperationLogInfo`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7734` `OperationLogViewerView`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7537` `InventoryIgnoredMappingsSheet`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7628` `InventoryManualMappingsSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAllSettings`；是否真实写入仍取决于分支和参数。

- **L7287 · 计算属性** `private var runAndFileSettingsCard: some View` — 执行文件、设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7471` `SettingsView.settingsRowLabel`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7478` `SettingsView.settingsDateDisplay`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7487` `SettingsView.settingsFieldRow`

- **L7320 · 计算属性** `private var accountSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5241` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2034` `AppModel.saveJdyPassword`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3117` `AppModel.openInventoryChrome`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:2085` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveJdyPassword`, `openInventoryChrome`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L7373 · 计算属性** `private var inventorySettingsCard: some View` — 根据当前状态计算并返回库存、设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7521` `SettingsView.compactStatus`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3130` `AppModel.updateInventoryCatalog`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7500` `SettingsView.settingsManagementRow`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateInventoryCatalog`；是否真实写入仍取决于分支和参数。

- **L7405 · 计算属性** `private var maintenanceSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1758` `AppModel.performBackup`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1920` `AppModel.setOperationLogEnabled`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1969` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1946` `AppModel.trimOperationLog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setOperationLogEnabled`；是否真实写入仍取决于分支和参数。

- **L7471 · 方法** `private func settingsRowLabel(_ title: String) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7478 · 方法** `private func settingsDateDisplay(_ value: Date) -> String` — 设置设置、日期相关数据或步骤。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7487 · 方法** `private func settingsFieldRow( _ title: String, placeholder: String, text: Binding<String> ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`placeholder: String`；`text: Binding<String>`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7471` `SettingsView.settingsRowLabel`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5241` `View.appInputField`

- **L7500 · 方法** `private func settingsManagementRow( _ title: String, count: Int, help: String, action: @escaping () -> Void ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`count: Int`；`help: String`；`action: @escaping () -> Void`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`

- **L7521 · 方法** `private func compactStatus(_ status: String) -> some View` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5195` `settingsStatusDisplayText`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5186` `settingsStatusKind`

- **L7537 · 结构体** `InventoryIgnoredMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7544 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5241` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3837` `AppModel.saveInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3862` `AppModel.updateInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3884` `AppModel.removeInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryIgnoredMapping`, `updateInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L7621 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7628 · 结构体** `InventoryManualMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7636 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5241` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3791` `AppModel.saveSettingsManualMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3808` `AppModel.updateSettingsManualMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3827` `AppModel.removeSettingsManualMapping`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3768` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettingsManualMapping`, `updateSettingsManualMapping`；是否真实写入仍取决于分支和参数。

- **L7726 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7734 · 结构体** `OperationLogViewerView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7739 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`

- **L7805 · 枚举** `AppSection` — 定义 `AppSection` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7811 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7813 · 计算属性** `var title: String` — 根据当前状态计算并返回`title` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7822 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7831 · 计算属性** `var pageTitle: String` — 根据当前状态计算并返回`pageTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7840 · 计算属性** `var subtitle: String` — 根据当前状态计算并返回`subtitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7849 · 计算属性** `var isWorkSection: Bool` — 根据当前状态计算并返回`isWorkSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7858 · 结构体** `TopNavigationBar` — 定义 `TopNavigationBar` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7863 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7975` `TopNavigationBar.navButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5245` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7999` `TopNavigationBar.designNote`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5294` `LiquidGlassPreviewBackdrop`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6299` `PendingInventoryMappingWorkspace`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteConfirmationSheet`；是否真实写入仍取决于分支和参数。

- **L7954 · 计算属性** `@ViewBuilder private var contextualStatus: some View` — 根据当前状态计算并返回状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5329` `AppStatusBadge`

- **L7975 · 方法** `private func navButton(_ section: AppSection) -> some View` — 封装 `navButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ section: AppSection`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7999 · 方法** `private func designNote(_ title: String, _ text: String) -> some View` — 封装 `designNote` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ text: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8009 · 结构体** `TravelerAssistantApp` — 定义与Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8013 · 计算属性** `var body: some Scene` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some Scene`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7858` `TopNavigationBar`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:6810` `TodoView`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:7216` `SettingsView`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5261` `AppGlassGroupBoxStyle`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5294` `LiquidGlassPreviewBackdrop`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:5091` `FixedWindowSizeController`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:3158` `AppModel.closeInventoryChromeOnQuit`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:4475` `AppModel.stopResidentOrderService`；`.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift:1758` `AppModel.performBackup`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryChromeOnQuit`；是否真实写入仍取决于分支和参数。

## `.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift`

Swift/macOS 源码或测试辅助文件。

- **L4 · 类** `OperationLogHarnessModel` — 定义与操作、日志相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7 · 初始化器** `init(steps: [InventoryStep])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L12 · 结构体** `OperationLogHarnessView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 类** `HeaderBoundaryProbeBox` — 定义 `HeaderBoundaryProbeBox` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L25 · 结构体** `HeaderBoundaryProbe` — 定义 `HeaderBoundaryProbe` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L28 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L34 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L39 · 结构体** `PageLayoutHarness` — 定义 `PageLayoutHarness` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L43 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:25` `HeaderBoundaryProbe`

- **L64 · 结构体** `MacOSUIRegressionTests` — 定义 `MacOSUIRegressionTests` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L65 · 方法** `static func main()` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:1326` `MacOSUIRegressionTests.testInventoryTravelerNewestFirst`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:109` `MacOSUIRegressionTests.testPushToTalkShortcut`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:115` `MacOSUIRegressionTests.testSpeechCommandCanonicalization`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:121` `MacOSUIRegressionTests.testAssistantOrderResultParsing`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:142` `MacOSUIRegressionTests.testAssistantCompactHelpAndCancelRules`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:150` `MacOSUIRegressionTests.testMaterialDisplayNames`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:222` `MacOSUIRegressionTests.testOrderDetailMaterialRows`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:250` `MacOSUIRegressionTests.testOrderDashboardRules`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:1031` `MacOSUIRegressionTests.testDashboardActivityIsScopedToAppSession`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:1058` `MacOSUIRegressionTests.testPendingServerSelectionAndRefreshContract`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:1087` `MacOSUIRegressionTests.testPendingInventorySourceFolderPath`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:1105` `MacOSUIRegressionTests.testPendingMaterialMappingIssueRoute`；另有 28 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `testOrderOutboundFactorySelection`, `testServerWriteMaterialPreviewOrdering`, `testServerWriteHardwareChangeLayout`；是否真实写入仍取决于分支和参数。

- **L109 · 方法** `private static func testPushToTalkShortcut()` — 验证与 `testPushToTalkShortcut` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L115 · 方法** `private static func testSpeechCommandCanonicalization()` — 验证与 `testSpeechCommandCanonicalization` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L121 · 方法** `private static func testAssistantOrderResultParsing()` — 验证订单、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L142 · 方法** `private static func testAssistantCompactHelpAndCancelRules()` — 验证与 `testAssistantCompactHelpAndCancelRules` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L150 · 方法** `private static func testMaterialDisplayNames()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:187` `MacOSUIRegressionTests.material`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `inventoryCatalogUpdateSuccessStatus`, `inventoryCatalogUpdateFailureStatus`, `Set`；是否真实写入仍取决于分支和参数。

- **L187 · 方法** `func material(_ kind: String, _ thickness: Double, _ color: String = "") -> OrderMaterialPreview` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ kind: String`；`_ thickness: Double`；`_ color: String = ""`
  - 返回：`OrderMaterialPreview`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L222 · 方法** `private static func testOrderDetailMaterialRows()` — 验证订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L250 · 方法** `private static func testOrderDashboardRules()` — 验证订单、看板相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openRequestedOrderIfAvailable`, `openOrderDetail`, `Set`；是否真实写入仍取决于分支和参数。

- **L1031 · 方法** `private static func testDashboardActivityIsScopedToAppSession()` — 验证看板相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1058 · 方法** `private static func testPendingServerSelectionAndRefreshContract()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardAfterServerWrite`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L1087 · 方法** `private static func testPendingInventorySourceFolderPath()` — 验证库存、来源、文件夹、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1105 · 方法** `private static func testPendingMaterialMappingIssueRoute()` — 验证材料、映射、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1137 · 方法** `private static func testPendingInventoryMappingResumeContract()` — 验证库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryMapping`；是否真实写入仍取决于分支和参数。

- **L1175 · 方法** `private static func testOrderOutboundFactorySelection()` — 验证订单、出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `orderDashboardOutboundDisplay`, `orderDashboardNeedsOutboundUpdateSelection`, `orderDashboardOutboundActionTitle`；是否真实写入仍取决于分支和参数。

- **L1227 · 方法** `private static func testProductionFeedbackAndDashboardProgress()` — 验证生产、看板、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L1326 · 方法** `private static func testInventoryTravelerNewestFirst()` — 验证库存、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2071` `MacOSUIRegressionTests.traveler`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1339 · 方法** `private static func testSharedPageHeaderHeight()` — 验证与 `testSharedPageHeaderHeight` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1363 · 方法** `private static func testAssistantOrderTimelineContract()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderCenter`；是否真实写入仍取决于分支和参数。

- **L1523 · 方法** `private static func testAssistantStageIconAssets()` — 验证与 `testAssistantStageIconAssets` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1538 · 方法** `private static func testGlassDatePickerContract()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1582 · 方法** `private static func testTodoTableHeaderRoundedCorners()` — 验证待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1605 · 方法** `private static func testSettingsDefaultWindowLayoutContract()` — 验证设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1695 · 方法** `private static func testFixedWindowSizeContract()` — 验证与 `testFixedWindowSizeContract` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1716 · 方法** `private static func testInventoryActionLayoutRules()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:1732` `MacOSUIRegressionTests.preview`

- **L1732 · 方法** `func preview(_ name: String, _ section: String) -> InventoryPreviewRow` — 预览预览相关数据或步骤。
  - 输入：`_ name: String`；`_ section: String`
  - 返回：`InventoryPreviewRow`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1761 · 方法** `private static func testRunningProgressReusesOperationRow()` — 验证进度、操作、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2103` `MacOSUIRegressionTests.fail`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1775 · 方法** `private static func testDashboardInventoryProgressText()` — 验证看板、库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1797 · 方法** `private static func testInventoryProgressKeepsStageHistory()` — 验证库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1808 · 方法** `private static func testDashboardSeparatesInventoryAndRefreshTiming()` — 验证看板、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1834 · 方法** `private static func testOrderOperationDurationFormatting()` — 验证订单、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1839 · 方法** `private static func testServerWriteMaterialPreviewOrdering()` — 验证Server 数据、材料、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`, `sortedServerWriteMaterialChanges`；是否真实写入仍取决于分支和参数。

- **L1856 · 方法** `private static func testServerWriteHardwareChangeLayout()` — 验证Server 数据、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1862 · 方法** `private static func testProductionOrderPaths()` — 验证生产、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1873 · 方法** `private static func testStockFailureKeepsManualRetryEnabled()` — 验证与 `testStockFailureKeepsManualRetryEnabled` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1888 · 方法** `private static func testExistingTravelerCanBeUpdatedAfterPreviewFailure()` — 验证Traveler、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderUpdateActionReady`；是否真实写入仍取决于分支和参数。

- **L1903 · 方法** `private static func testDashboardTravelerActionsUseDatabaseFacts()` — 验证看板、Traveler、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L1916 · 方法** `private static func testRelatedPreviewMissingMaterialIssue()` — 验证预览、材料、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1932 · 方法** `private static func testPP0067MissingMaterialShowsPrompt()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2103` `MacOSUIRegressionTests.fail`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2095` `MacOSUIRegressionTests.pumpRunLoop`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`；是否真实写入仍取决于分支和参数。

- **L1953 · 方法** `private static func testFullPageHeaderBoundaryAlignment()` — 验证与 `testFullPageHeaderBoundaryAlignment` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:1962` `MacOSUIRegressionTests.headerBoundaryY`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L1962 · 方法** `private static func headerBoundaryY(flexibleContent: Bool) -> CGFloat` — 封装 `headerBoundaryY` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`flexibleContent: Bool`
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:21` `HeaderBoundaryProbeBox`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:39` `PageLayoutHarness`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2095` `MacOSUIRegressionTests.pumpRunLoop`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2103` `MacOSUIRegressionTests.fail`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L1981 · 方法** `private static func testOperationLogScrollsAfterAppending()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2083` `MacOSUIRegressionTests.step`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:4` `OperationLogHarnessModel`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:12` `OperationLogHarnessView`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2095` `MacOSUIRegressionTests.pumpRunLoop`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2087` `MacOSUIRegressionTests.firstScrollView`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2103` `MacOSUIRegressionTests.fail`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L2032 · 方法** `private static func testOperationLogReader()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`

- **L2042 · 方法** `private static func testOperationLogMaintenance()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`；`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2099` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`；是否真实写入仍取决于分支和参数。

- **L2071 · 方法** `private static func traveler(_ name: String, folder: String, modifiedAt: String) -> InventoryTraveler` — 封装Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`folder: String`；`modifiedAt: String`
  - 返回：`InventoryTraveler`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2083 · 方法** `private static func step(_ index: Int) -> InventoryStep` — 封装 `step` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ index: Int`
  - 返回：`InventoryStep`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2087 · 方法** `private static func firstScrollView(in view: NSView) -> NSScrollView?` — 封装 `firstScrollView` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`in view: NSView`
  - 返回：`NSScrollView?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2095 · 方法** `private static func pumpRunLoop(for seconds: TimeInterval)` — 封装 `pumpRunLoop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`for seconds: TimeInterval`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run`；是否真实写入仍取决于分支和参数。

- **L2099 · 方法** `private static func require(_ condition: @autoclosure () -> Bool, _ message: String)` — 封装 `require` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ condition: @autoclosure () -> Bool`；`_ message: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift:2103` `MacOSUIRegressionTests.fail`

- **L2103 · 方法** `private static func fail(_ message: String) -> Never` — 封装 `fail` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Never`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift`

Swift/macOS 源码或测试辅助文件。

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
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

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
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:982` `orderMaterialDisplayName`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:956` `OrderMaterialPreview`

- **L151 · 函数** `private func productionMaterialTypeRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L160 · 函数** `private func productionMaterialPlywoodRank(_ material: ProductionMaterialDraft) -> Int` — 封装生产、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ material: ProductionMaterialDraft`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`

- **L168 · 函数** `func sortedProductionMaterialDrafts(_ materials: [ProductionMaterialDraft]) -> [ProductionMaterialDraft]` — 排序生产、材料相关数据或步骤。
  - 输入：`_ materials: [ProductionMaterialDraft]`
  - 返回：`[ProductionMaterialDraft]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:151` `productionMaterialTypeRank`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:160` `productionMaterialPlywoodRank`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:128` `productionMaterialName`

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

- **L332 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L346 · 结构体** `ServerWriteMaterialChange` — 定义与Server 数据、材料相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L358 · 初始化器** `init( id: String, changeType: String, materialType: String, color: String, thickness: String, edge: String, unit: String, oldQuantity: Double, newQuantity: Double, delta: Double )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`changeType: String`；`materialType: String`；`color: String`；`thickness: String`；`edge: String`；`unit: String`；`oldQuantity: Double`；`newQuantity: Double`；`delta: Double`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L382 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L397 · 方法** `static func aggregated(_ changes: [ServerWriteMaterialChange]) -> [ServerWriteMaterialChange]` — 封装 `aggregated` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerWriteMaterialChange]`
  - 返回：`[ServerWriteMaterialChange]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:346` `ServerWriteMaterialChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`；是否真实写入仍取决于分支和参数。

- **L426 · 结构体** `ServerWriteHardwareChange` — 定义与Server 数据、五金相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L439 · 初始化器** `init?(row: [String: Any], index: Int)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`；`index: Int`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L457 · 结构体** `ServerHardwareMappingRequirement` — 定义与Server 数据、五金、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L467 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L481 · 结构体** `ServerWriteFactoryPreview` — 定义与Server 数据、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L495 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:323` `ServerWriteHardwarePreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:426` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteHardwarePreview`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L517 · 结构体** `ServerWriteOrderPreview` — 定义与Server 数据、订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L530 · 初始化器** `init( id: String, orderID: String, orderType: String, sourceFolder: String, validationStatus: String, validationMessage: String, materials: [ServerWriteMaterialPreview], materialChanges: [ServerWriteMaterialChange], factories: [ServerWriteFactoryPreview], excludedFactories: [ServerWriteFactoryPreview], hardwareChanges: [ServerWriteHardwareChange] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String`；`orderID: String`；`orderType: String`；`sourceFolder: String`；`validationStatus: String`；`validationMessage: String`；`materials: [ServerWriteMaterialPreview]`；`materialChanges: [ServerWriteMaterialChange]`；`factories: [ServerWriteFactoryPreview]`；`excludedFactories: [ServerWriteFactoryPreview]`；`hardwareChanges: [ServerWriteHardwareChange]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L556 · 初始化器** `init?(row: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`row: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:292` `ServerWriteMaterialPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:397` `ServerWriteMaterialChange.aggregated`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:346` `ServerWriteMaterialChange`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:426` `ServerWriteHardwareChange`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`, `ServerWriteMaterialChange`, `ServerWriteHardwareChange`；是否真实写入仍取决于分支和参数。

- **L581 · 结构体** `ServerWritePreview` — 定义与Server 数据、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L588 · 初始化器** `init(payload: [String: Any], sourceFolders: [String], materials: [ServerWriteMaterialPreview], orders: [ServerWriteOrderPreview], hardwareMappingRequirements: [ServerHardwareMappingRequirement] = [])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`payload: [String: Any]`；`sourceFolders: [String]`；`materials: [ServerWriteMaterialPreview]`；`orders: [ServerWriteOrderPreview]`；`hardwareMappingRequirements: [ServerHardwareMappingRequirement] = []`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L596 · 初始化器** `init?(object: [String: Any])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`object: [String: Any]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:292` `ServerWriteMaterialPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialPreview`；是否真实写入仍取决于分支和参数。

- **L613 · 结构体** `ServerFolderChangeGroup` — 定义与Server 数据、文件夹相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L621 · 计算属性** `var requiresManualReview: Bool` — 根据当前状态计算并返回`requiresManualReview` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L626 · 结构体** `PendingCenterItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L640 · 函数** `func serverFolderChangeGroups(_ changes: [ServerChangePreview]) -> [ServerFolderChangeGroup]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`
  - 返回：`[ServerFolderChangeGroup]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:613` `ServerFolderChangeGroup`

- **L659 · 函数** `func buildPendingCenterItems( serverChanges: [ServerChangePreview], currentIssues: [CurrentIssue], aimesReviews: [AimesReviewItem], aimesFormatWarnings: [AimesReviewItem] = [] ) -> [PendingCenterItem]` — 构建与 `buildPendingCenterItems` 对应的数据或步骤。
  - 输入：`serverChanges: [ServerChangePreview]`；`currentIssues: [CurrentIssue]`；`aimesReviews: [AimesReviewItem]`；`aimesFormatWarnings: [AimesReviewItem] = []`
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:640` `serverFolderChangeGroups`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:670` `belongs`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:626` `PendingCenterItem`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `Set`；是否真实写入仍取决于分支和参数。

- **L670 · 函数** `func belongs(_ issue: CurrentIssue, to group: ServerFolderChangeGroup) -> Bool` — 封装 `belongs` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`；`to group: ServerFolderChangeGroup`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L771 · 结构体** `CurrentIssue` — 定义与待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L782 · 结构体** `AimesReviewItem` — 定义与AIMES 数据、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L794 · 函数** `func aimesReviewItems(_ object: [String: Any], key: String) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`key: String`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:782` `AimesReviewItem`

- **L811 · 函数** `func aimesReviewItemsFromWarnings(_ warnings: [[String: Any]]) -> [AimesReviewItem]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ warnings: [[String: Any]]`
  - 返回：`[AimesReviewItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:782` `AimesReviewItem`

- **L830 · 函数** `func dashboardActivitySteps( _ object: [String: Any], includeChanges: Bool = true, sessionStartedAt: Date? = nil ) -> [InventoryStep]` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`；`sessionStartedAt: Date? = nil`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1318` `dashboardBusinessDate`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L883 · 函数** `func serverChangePreviews(_ rows: [[String: Any]]) -> [ServerChangePreview]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [[String: Any]]`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:255` `ServerChangePreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L904 · 函数** `func serverChangesExcludingFolder( _ changes: [ServerChangePreview], folderPath: String ) -> [ServerChangePreview]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`；`folderPath: String`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:911` `serverChangesExcludingFolders`

- **L911 · 函数** `func serverChangesExcludingFolders( _ changes: [ServerChangePreview], folderPaths: [String] ) -> [ServerChangePreview]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ changes: [ServerChangePreview]`；`folderPaths: [String]`
  - 返回：`[ServerChangePreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L930 · 函数** `func serverChangeTypeName(_ type: String) -> String` — 封装Server 数据、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ type: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L940 · 结构体** `OrderPreviewIssue` — 定义与订单、预览、待处理问题相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L946 · 函数** `func orderPreviewIssues(_ object: [String: Any]) -> [OrderPreviewIssue]` — 封装订单、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`[OrderPreviewIssue]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:940` `OrderPreviewIssue`

- **L956 · 结构体** `OrderMaterialPreview` — 定义与订单、材料、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L965 · 初始化器** `init( kind: String, thickness: Double, color: String, quantity: Double, productCode: String = "", brand: String = "" )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`kind: String`；`thickness: Double`；`color: String`；`quantity: Double`；`productCode: String = ""`；`brand: String = ""`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L982 · 函数** `func orderMaterialDisplayName(_ row: OrderMaterialPreview) -> String` — 封装订单、材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: OrderMaterialPreview`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L993 · 函数** `func orderedMaterialRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`[OrderMaterialPreview]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1024 · 函数** `func orderedEdgeColors(_ colors: [String], matching panels: [OrderMaterialPreview]) -> [String]` — 封装 `orderedEdgeColors` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ colors: [String]`；`matching panels: [OrderMaterialPreview]`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1037 · 函数** `func panelColorsNeedingThicknessWarning(_ rows: [OrderMaterialPreview]) -> Set<String>` — 封装 `panelColorsNeedingThicknessWarning` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ rows: [OrderMaterialPreview]`
  - 返回：`Set<String>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L1049 · 结构体** `OrderFactoryPreview` — 定义与订单、工厂单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1055 · 结构体** `OrderFittingPreview` — 定义与订单、五金、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1069 · 结构体** `OrderStockPreview` — 定义与订单、预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1081 · 结构体** `OrderCostLine` — 定义与订单、成本相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1096 · 结构体** `OrderCostFactoryTotal` — 定义与订单、成本、工厂单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1103 · 结构体** `InventoryTraveler` — 定义与库存、Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1113 · 函数** `func groupInventoryTravelersByNewest(_ travelers: [InventoryTraveler]) -> [(String, [InventoryTraveler])]` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ travelers: [InventoryTraveler]`
  - 返回：`[(String, [InventoryTraveler])]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1130 · 结构体** `InventoryPreviewRow` — 定义与库存、预览、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1141 · 函数** `func inventoryPreviewCategoryRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1150 · 函数** `func inventoryPreviewPlywoodRank(_ row: InventoryPreviewRow) -> Int` — 封装库存、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1158 · 函数** `func sortedInventoryPreviewRows(_ rows: [InventoryPreviewRow]) -> [InventoryPreviewRow]` — 排序库存、预览相关数据或步骤。
  - 输入：`_ rows: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1141` `inventoryPreviewCategoryRank`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1150` `inventoryPreviewPlywoodRank`

- **L1174 · 结构体** `InventoryProductCandidate` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1183 · 结构体** `InventoryIgnoredMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1189 · 结构体** `InventoryManualMapping` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1196 · 结构体** `InventoryStep` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1208 · 初始化器** `init( id: UUID = UUID(), time: String, title: String, detail: String, state: String, paths: [String] = [], operationDetails: [String] = [], contextDetails: [String] = [], startedAt: Date? = nil, duration: TimeInterval? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`time: String`；`title: String`；`detail: String`；`state: String`；`paths: [String] = []`；`operationDetails: [String] = []`；`contextDetails: [String] = []`；`startedAt: Date? = nil`；`duration: TimeInterval? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1233 · 函数** `func operationDurationText(_ duration: TimeInterval) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ duration: TimeInterval`
  - 返回：`String`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1281` `Double.rounded`

- **L1238 · 函数** `func inventoryFailureNeedsVerification(_ message: String) -> Bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1253 · 结构体** `DashboardOperationDuration` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1258 · 初始化器** `init(id: String? = nil, label: String, duration: TimeInterval)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: String? = nil`；`label: String`；`duration: TimeInterval`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1265 · 函数** `func dashboardFlatOperationDurations(_ stages: [[String: Any]]) -> [DashboardOperationDuration]` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ stages: [[String: Any]]`
  - 返回：`[DashboardOperationDuration]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1253` `DashboardOperationDuration`

- **L1275 · 结构体** `DashboardOperationStart` — 定义与看板、操作相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1280 · 扩展** `Double` — 定义 `Double` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1281 · 方法** `func rounded(toPlaces places: Int) -> Double` — 封装 `rounded` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`toPlaces places: Int`
  - 返回：`Double`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`

- **L1287 · 函数** `func dashboardClockTime(_ date: Date = Date()) -> String` — 封装看板、时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date = Date()`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1291 · 函数** `func dashboardInventoryProgressText(_ message: String) -> String` — 封装看板、库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1314 · 函数** `func appDisplayTimestamp(_ value: String) -> String` — 封装 `appDisplayTimestamp` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1318 · 函数** `func dashboardBusinessDate(_ value: String) -> Date?` — 封装看板、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`
  - 返回：`Date?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1336 · 函数** `func dashboardTimestamp(_ value: String, isInSameMonthAs reference: Date, calendar: Calendar = .current) -> Bool` — 封装看板相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ value: String`；`isInSameMonthAs reference: Date`；`calendar: Calendar = .current`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1318` `dashboardBusinessDate`

- **L1341 · 函数** `func updatingLatestRunningStep(_ steps: [InventoryStep], detail: String) -> [InventoryStep]?` — 封装 `updatingLatestRunningStep` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`detail: String`
  - 返回：`[InventoryStep]?`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L1360 · 函数** `func appendingInventoryProgressStep(_ steps: [InventoryStep], message: String) -> [InventoryStep]` — 封装库存、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ steps: [InventoryStep]`；`message: String`
  - 返回：`[InventoryStep]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L1389 · 函数** `func orderUpdateActionReady(existingTravelerPath: String, selectedOrderPath: String, selectedOrderId: String) -> Bool` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`；`selectedOrderPath: String`；`selectedOrderId: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1393 · 函数** `func orderTravelerOpenActionReady(existingTravelerPath: String) -> Bool` — 封装订单、Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`existingTravelerPath: String`
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1398 · 结构体** `TodoItem` — 定义与待办、项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1405 · 初始化器** `init( id: UUID = UUID(), content: String, startedAt: Date = Date(), deadline: Date?, completedAt: Date? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`id: UUID = UUID()`；`content: String`；`startedAt: Date = Date()`；`deadline: Date?`；`completedAt: Date? = nil`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1420 · 结构体** `AssistantTaskItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1426 · 类** `ResidentOrderServiceClient` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1436 · 初始化器** `init(onProgress: @escaping (String) -> Void)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`onProgress: @escaping (String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1440 · 方法** `func start(command: URL, environment: [String: String]) throws` — 启动与 `start` 对应的数据或步骤。
  - 输入：`command: URL`；`environment: [String: String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run`；是否真实写入仍取决于分支和参数。

- **L1460 · 方法** `func request(id: String, arguments: [String], inputData: Data?) throws -> Data` — 封装 `request` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`id: String`；`arguments: [String]`；`inputData: Data?`
  - 返回：`Data`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`；是否真实写入仍取决于分支和参数。

- **L1492 · 方法** `func stop()` — 封装 `stop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `closeFile`；是否真实写入仍取决于分支和参数。

- **L1512 · 类** `AppModel` — 定义 `AppModel` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1567 · 枚举** `PendingMappingResumeAction` — 定义与映射相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1573 · 结构体** `PendingResumeContext` — 定义 `PendingResumeContext` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1684 · 计算属性** `var pendingCenterItems: [PendingCenterItem]` — 根据当前状态计算并返回`pendingCenterItems` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingCenterItem]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:659` `buildPendingCenterItems`

- **L1693 · 计算属性** `var hasAimesHistory: Bool` — 根据当前状态计算并返回AIMES 数据。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1697 · 计算属性** `var orderPreviewReady: Bool` — 根据当前状态计算并返回订单、预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1701 · 计算属性** `var orderCanGenerateTraveler: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1705 · 计算属性** `var orderTravelerOpenReady: Bool` — 根据当前状态计算并返回订单、Traveler。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1393` `orderTravelerOpenActionReady`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L1709 · 计算属性** `var activeOwnedSourceRoot: String` — 根据当前状态计算并返回来源。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1713 · 计算属性** `var activeCutToSizeRoot: String` — 根据当前状态计算并返回`activeCutToSizeRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1719 · 计算属性** `var activeOrderRoot: String` — 根据当前状态计算并返回订单。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1723 · 计算属性** `var activeBackupRoot: String` — 根据当前状态计算并返回备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1727 · 计算属性** `var databaseBackupRoot: String` — 根据当前状态计算并返回数据库、备份。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1731 · 初始化器** `init()` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1883` `AppModel.loadSettings`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1802` `AppModel.loadTodoItems`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1744` `AppModel.startResidentOrderService`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setEnabled`, `record`；是否真实写入仍取决于分支和参数。

- **L1744 · 方法** `private func startResidentOrderService()` — 启动订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4452` `AppModel.consumeOrderLogChunk`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1440` `ResidentOrderServiceClient.start`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2018` `AppModel.environmentForOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1989` `AppModel.newOperationID`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1765 · 方法** `func checkBackupReminder()` — 检查备份相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L1774 · 方法** `func performBackup()` — 执行手动/计划备份并把结果映射为 App 状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L1792 · 计算属性** `private var settingsURL: URL` — 设置设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1797 · 计算属性** `var todoDataURL: URL` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1802 · 方法** `func loadTodoItems()` — 读取待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`

- **L1817 · 方法** `func addTodo(content: String, deadline: Date?)` — 新增待办相关数据或步骤。
  - 输入：`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1398` `TodoItem`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1853` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1828 · 方法** `func updateTodo(_ item: TodoItem, content: String, deadline: Date?)` — 更新待办相关数据或步骤。
  - 输入：`_ item: TodoItem`；`content: String`；`deadline: Date?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1853` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1840 · 方法** `func toggleTodoCompletion(_ item: TodoItem)` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1853` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1847 · 方法** `func deleteTodo(_ item: TodoItem)` — 删除待办相关数据或步骤。
  - 输入：`_ item: TodoItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1853` `AppModel.saveTodoItems`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveTodoItems`；是否真实写入仍取决于分支和参数。

- **L1853 · 方法** `private func saveTodoItems()` — 保存待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L1883 · 方法** `func loadSettings() -> Bool` — 读取设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1902 · 方法** `func saveSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`tests/test_inventory.py:75` `_FakeNodeInput.write`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`, `record`；是否真实写入仍取决于分支和参数。

- **L1931 · 计算属性** `var operationLogURL: URL` — 根据当前状态计算并返回操作、日志。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1936 · 方法** `func setOperationLogEnabled(_ enabled: Bool)` — 设置操作、日志相关数据或步骤。
  - 输入：`_ enabled: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1902` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`, `setEnabled`, `saveSettings`；是否真实写入仍取决于分支和参数。

- **L1958 · 方法** `func refreshOperationLogInfo()` — 刷新操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1962 · 方法** `func trimOperationLog()` — 封装操作、日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1958` `AppModel.refreshOperationLogInfo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1985 · 方法** `func logUserAction(_ action: String, details: [String: Any] = [:])` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ action: String`；`details: [String: Any] = [:]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L1989 · 方法** `func newOperationID(_ name: String, details: [String: Any] = [:]) -> String` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`details: [String: Any] = [:]`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2000 · 方法** `private func finishOperationLog( _ operationID: String, name: String, startedAt: Date, exitStatus: Int32 )` — 结束并收口操作、日志相关数据或步骤。
  - 输入：`_ operationID: String`；`name: String`；`startedAt: Date`；`exitStatus: Int32`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L2018 · 方法** `func environmentForOperation(_ operationID: String) -> [String: String]` — 封装操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ operationID: String`
  - 返回：`[String: String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2026 · 方法** `func saveAllSettings()` — 保存设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1902` `AppModel.saveSettings`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2050` `AppModel.saveJdyPassword`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2101` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `saveJdyPassword`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L2050 · 方法** `func saveJdyPassword()` — 保存与 `saveJdyPassword` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `SecItemDelete`, `SecItemUpdate`, `SecItemCopyMatching`；是否真实写入仍取决于分支和参数。

- **L2101 · 方法** `func saveAimesPassword()` — 保存AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1902` `AppModel.saveSettings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettings`, `SecItemDelete`；是否真实写入仍取决于分支和参数。

- **L2122 · 方法** `private func applyDashboardObject(_ object: [String: Any], includeChanges: Bool = true)` — 应用看板相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`includeChanges: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2234` `AppModel.applyDashboardOperationTrace`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2217` `AppModel.applyCurrentIssues`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:251` `dashboardOrderRows`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:91` `OrderDashboardFactory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:213` `OrderInstallationDay`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:225` `OrderDashboardItem`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:830` `dashboardActivitySteps`

- **L2201 · 方法** `private func presentServerWritePreview(_ object: [String: Any])` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:581` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2217 · 方法** `private func applyCurrentIssues(from object: [String: Any])` — 应用与 `applyCurrentIssues` 对应的数据或步骤。
  - 输入：`from object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:771` `CurrentIssue`

- **L2234 · 方法** `private func applyDashboardOperationTrace(_ object: [String: Any])` — 应用看板、操作相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2246 · 方法** `private func applyAimesReviewObject(_ object: [String: Any], presentIfNeeded: Bool = true)` — 应用AIMES 数据相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:794` `aimesReviewItems`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:811` `aimesReviewItemsFromWarnings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L2264 · 方法** `private func closePendingCenterIfEmpty()` — 关闭与 `closePendingCenterIfEmpty` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2270 · 方法** `private func beginDashboardOperation(_ source: String, label: String, continuing: Bool = false)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`；`label: String`；`continuing: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1275` `DashboardOperationStart`

- **L2282 · 方法** `private func finishDashboardOperation(_ source: String)` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1253` `DashboardOperationDuration`

- **L2295 · 方法** `private func finishDashboardOperation( _ source: String, backendSeconds: Double, stages: [[String: Any]] )` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`backendSeconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1265` `dashboardFlatOperationDurations`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1253` `DashboardOperationDuration`

- **L2321 · 方法** `private func finishDashboardOperation(_ source: String, using object: [String: Any])` — 结束并收口看板、操作相关数据或步骤。
  - 输入：`_ source: String`；`using object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2334 · 方法** `private func discardDashboardOperationTimer(_ source: String)` — 封装看板、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ source: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2338 · 方法** `private func applyAuthoritativeDashboardTiming( _ source: String, seconds: Double, stages: [[String: Any]] )` — 应用看板相关数据或步骤。
  - 输入：`_ source: String`；`seconds: Double`；`stages: [[String: Any]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1265` `dashboardFlatOperationDurations`

- **L2349 · 方法** `func startOrderDashboard()` — 启动订单中心初始化链路，加载缓存并安排 AIMES/Server 刷新。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2355` `AppModel.loadOrderDashboardCache`

- **L2355 · 方法** `func loadOrderDashboardCache()` — 读取订单、看板、缓存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2246` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2462` `AppModel.syncDashboardAimes`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2377 · 方法** `func refreshDashboardOrdersAfterOutbound()` — 刷新看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2396 · 方法** `private func startPendingDashboardOutboundRefreshIfNeeded()` — 启动看板、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2377` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L2404 · 方法** `private func runDailyBackupAfterLocalCache(completion: @escaping () -> Void)` — 执行备份、缓存相关数据或步骤。
  - 输入：`completion: @escaping () -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2429 · 方法** `func autoResolveCurrentIssue(_ issue: CurrentIssue)` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ issue: CurrentIssue`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2264` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2444 · 方法** `func resolveCurrentIssue(_ issue: CurrentIssue, orderID: String)` — 解析并确定待处理问题相关数据或步骤。
  - 输入：`_ issue: CurrentIssue`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2264` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2462 · 方法** `func syncDashboardAimes(force: Bool, scanServerAfter: Bool = false)` — 从 App 发起 AIMES 同步，解析结果并衔接后续看板刷新。
  - 输入：`force: Bool`；`scanServerAfter: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2636` `AppModel.scanDashboardServer`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2334` `AppModel.discardDashboardOperationTimer`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2338` `AppModel.applyAuthoritativeDashboardTiming`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2246` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2523 · 方法** `func toggleAimesReviewSelection(_ item: AimesReviewItem)` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`

- **L2533 · 方法** `func ignoreSelectedAimesFactories()` — 忽略AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2246` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2264` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2559 · 方法** `func restoreAimesFactory(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2246` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2579 · 方法** `func assignAimesFactoryToSuggestedOrder(_ item: AimesReviewItem)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2584` `AppModel.assignAimesFactoryToOrder`

- **L2584 · 方法** `func assignAimesFactoryToOrder(_ item: AimesReviewItem, orderID: String)` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: AimesReviewItem`；`orderID: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2246` `AppModel.applyAimesReviewObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2264` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2616 · 方法** `func restoreAimesFactoryAssignment(_ item: AimesReviewItem)` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`_ item: AimesReviewItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2246` `AppModel.applyAimesReviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L2636 · 方法** `func scanDashboardServer(background: Bool = false, presentIfNeeded: Bool = true)` — 从 App 发起 Server 扫描并把变化、问题和耗时写入看板状态。
  - 输入：`background: Bool = false`；`presentIfNeeded: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2217` `AppModel.applyCurrentIssues`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2234` `AppModel.applyDashboardOperationTrace`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:883` `serverChangePreviews`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2264` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2672 · 方法** `func toggleServerFolderSelection(_ folderPath: String)` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folderPath: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:640` `serverFolderChangeGroups`

- **L2684 · 方法** `func clearServerFolderSelection()` — 清理Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`

- **L2689 · 方法** `func processPendingServerChanges()` — 按当前选择为 Server 变化生成业务预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:640` `serverFolderChangeGroups`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2201` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2721 · 方法** `func confirmServerWrite(orderID: String, factoryOrder: String)` — 确认并执行 Server 事实写入，然后只做所需的本地看板刷新。
  - 输入：`orderID: String`；`factoryOrder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:517` `ServerWriteOrderPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:581` `ServerWritePreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2868` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `ServerWriteOrderPreview`, `ServerWritePreview`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L2800 · 方法** `func confirmServerMaterialPreview(skipHardwareOrderIDs: Set<String> = [])` — 封装Server 数据、材料、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`skipHardwareOrderIDs: Set<String> = []`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2868` `AppModel.refreshDashboardAfterServerWrite`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L2868 · 方法** `func refreshDashboardAfterServerWrite(processedFolders: [String])` — 刷新看板、Server 数据相关数据或步骤。
  - 输入：`processedFolders: [String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:911` `serverChangesExcludingFolders`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2264` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2891 · 方法** `private func applyServerIndexResult(_ object: [String: Any])` — 应用Server 数据、结果相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2246` `AppModel.applyAimesReviewObject`

- **L2896 · 方法** `func prepareSelectedServerFolder(_ folderURL: URL)` — 准备并校验Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2902 · 方法** `func processSelectedServerFolder(_ folderURL: URL, includeHardware: Bool)` — 处理Server 数据、文件夹相关数据或步骤。
  - 输入：`_ folderURL: URL`；`includeHardware: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2201` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `insert`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L2940 · 方法** `func markTemporaryFolderManual(_ folderPath: String)` — 标记文件夹相关数据或步骤。
  - 输入：`_ folderPath: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2217` `AppModel.applyCurrentIssues`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:904` `serverChangesExcludingFolder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2264` `AppModel.closePendingCenterIfEmpty`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L2967 · 方法** `func loadInventory()` — 加载可处理的库存/Traveler 列表及目录状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1103` `InventoryTraveler`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3137` `AppModel.activatePendingInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `Set`；是否真实写入仍取决于分支和参数。

- **L3010 · 方法** `func requestInventoryMapping(folderPath: String, message: String = "")` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folderPath: String`；`message: String = ""`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:69` `inventoryMappingSourceFolderPath`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1573` `PendingResumeContext`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3044` `AppModel.inventoryMappingNames`

- **L3034 · 方法** `func closeInventoryMappingWorkspace()` — 关闭库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3044 · 方法** `private func inventoryMappingNames(from message: String) -> [String]` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`from message: String`
  - 返回：`[String]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3055 · 方法** `private func rereadPendingSourceFolder()` — 封装来源、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3100` `AppModel.resumePendingMappingOperationAfterMapping`

- **L3060 · 方法** `private func failPendingResume(_ context: PendingResumeContext, message: String)` — 封装 `failPendingResume` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ context: PendingResumeContext`；`message: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3069 · 方法** `private func refreshDashboardOrdersAfterInventoryMapping(_ context: PendingResumeContext, preview: [String: Any])` — 刷新看板、库存、映射相关数据或步骤。
  - 输入：`_ context: PendingResumeContext`；`preview: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3060` `AppModel.failPendingResume`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2217` `AppModel.applyCurrentIssues`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3092 · 方法** `func inventoryMappingWorkspaceDidDismiss()` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3034` `AppModel.closeInventoryMappingWorkspace`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2201` `AppModel.presentServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryMappingWorkspace`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3100 · 方法** `private func resumePendingMappingOperationAfterMapping()` — 封装映射、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3317` `AppModel.previewSelectedInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3060` `AppModel.failPendingResume`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:581` `ServerWritePreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:69` `inventoryMappingSourceFolderPath`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3069` `AppModel.refreshDashboardOrdersAfterInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L3132 · 方法** `func retryPendingMappingPreview()` — 封装映射、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3100` `AppModel.resumePendingMappingOperationAfterMapping`

- **L3137 · 方法** `func activatePendingInventoryMapping()` — 封装库存、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3317` `AppModel.previewSelectedInventory`

- **L3177 · 方法** `func openInventoryChrome()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3190 · 方法** `func updateInventoryCatalog()` — 更新库存、商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5259` `inventoryCatalogUpdateFailureStatus`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`, `inventoryCatalogUpdateFailureStatus`, `inventoryCatalogUpdateSuccessStatus`；是否真实写入仍取决于分支和参数。

- **L3218 · 方法** `func closeInventoryChromeOnQuit()` — 关闭库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`, `record`；是否真实写入仍取决于分支和参数。

- **L3248 · 方法** `func refreshInventoryCatalogStatus()` — 刷新库存、商品目录、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3258 · 方法** `func refreshInventoryFolder(_ folder: String)` — 刷新库存、文件夹相关数据或步骤。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3290` `AppModel.reloadInventoryFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3290 · 方法** `private func reloadInventoryFolder(_ folder: String)` — 封装库存、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ folder: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1103` `InventoryTraveler`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3317 · 方法** `func previewSelectedInventory()` — 为当前选中对象串行生成库存需求和可用量预览。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3350` `AppModel.previewOrderInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4152` `AppModel.previewNext`

- **L3350 · 方法** `func previewOrderInventory( orderID: String, factoryOrderNames: [String], factoryOrders: [String] = [], productionBatchNumber: String = "", shipmentOnly: Bool = false )` — 预览预览、订单、库存相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrderNames: [String]`；`factoryOrders: [String] = []`；`productionBatchNumber: String = ""`；`shipmentOnly: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4140` `AppModel.applyInventoryPreviewObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4366` `AppModel.finishInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`；是否真实写入仍取决于分支和参数。

- **L3391 · 方法** `func loadProductionPreview(orderID: String, factoryOrders: [String], completion: @escaping (Bool) -> Void = { _ in })` — 读取当前选择的生产材料预览并填充编辑草稿。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:106` `ProductionMaterialDraft`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3429 · 方法** `func prepareProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], onResult completion: @escaping (String?, String?) -> Void )` — 从 App 提交生产准备参数并处理后端返回。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`onResult completion: @escaping (String?, String?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L3446 · 方法** `func startDirectProduction( orderID: String, factoryOrders: [String], materials: [ProductionMaterialDraft], batchNumber: String, completion: @escaping (ProductionOperationResult) -> Void = { _ in } )` — 执行用户确认后的生产完成流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`materials: [ProductionMaterialDraft]`；`batchNumber: String`；`completion: @escaping (ProductionOperationResult) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:206` `ProductionOperationResult`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1238` `inventoryFailureNeedsVerification`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2377` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L3564 · 方法** `func startDirectOrderShipment(orderID: String, factoryOrders: [String])` — 执行用户确认后的订单出库流程。
  - 输入：`orderID: String`；`factoryOrders: [String]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2270` `AppModel.beginDashboardOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1287` `dashboardClockTime`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2377` `AppModel.refreshDashboardOrdersAfterOutbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `runInventory`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L3644 · 方法** `func loadOutboundScope( orderID: String, factoryOrders: [String], completion: @escaping ([String: Any]?) -> Void )` — 读取出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`factoryOrders: [String]`；`completion: @escaping ([String: Any]?) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3666 · 方法** `func saveOutboundScope( orderID: String, scopeType: String, requirement: String, factoryOrder: String = "", reason: String, completion: @escaping (Bool) -> Void = { _ in } )` — 保存出库、范围相关数据或步骤。
  - 输入：`orderID: String`；`scopeType: String`；`requirement: String`；`factoryOrder: String = ""`；`reason: String`；`completion: @escaping (Bool) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3695 · 方法** `func openAndFillSelectedInventory()` — 打开库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3787` `AppModel.markInventoryTravelerSaved`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3787 · 方法** `private func markInventoryTravelerSaved(path: String, documentNumber: String)` — 标记库存、Traveler相关数据或步骤。
  - 输入：`path: String`；`documentNumber: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1103` `InventoryTraveler`

- **L3802 · 方法** `func setInventoryItemsIgnored(_ names: [String], ignored: Bool)` — 设置库存相关数据或步骤。
  - 输入：`_ names: [String]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3100` `AppModel.resumePendingMappingOperationAfterMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runInventory`；是否真实写入仍取决于分支和参数。

- **L3835 · 方法** `func refreshInventoryMappings()` — 刷新库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1189` `InventoryManualMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1183` `InventoryIgnoredMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3858 · 方法** `func saveSettingsManualMapping(name: String, productCode: String, displayName: String)` — 保存设置、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`；`displayName: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3875 · 方法** `func updateSettingsManualMapping(oldName: String, name: String, productCode: String, displayName: String)` — 更新设置、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`productCode: String`；`displayName: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3894 · 方法** `func removeSettingsManualMapping(name: String)` — 移除设置、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3904 · 方法** `func saveInventoryIgnoredMapping(name: String, reason: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3060` `AppModel.failPendingResume`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3055` `AppModel.rereadPendingSourceFolder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3935 · 方法** `func updateInventoryIgnoredMapping(oldName: String, name: String, reason: String)` — 更新库存、映射相关数据或步骤。
  - 输入：`oldName: String`；`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3957 · 方法** `func removeInventoryIgnoredMapping(name: String)` — 移除库存、映射相关数据或步骤。
  - 输入：`name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3967 · 方法** `func searchInventoryProducts(_ query: String)` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ query: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1174` `InventoryProductCandidate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L3994 · 方法** `func saveInventoryMapping(travelerName: String, productCode: String)` — 保存库存、映射相关数据或步骤。
  - 输入：`travelerName: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3060` `AppModel.failPendingResume`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3100` `AppModel.resumePendingMappingOperationAfterMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4020 · 方法** `func saveServerHardwareMapping(name: String, productCode: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`productCode: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4050` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4035 · 方法** `func saveServerHardwareIgnoredMapping(name: String, reason: String)` — 保存Server 数据、五金、映射相关数据或步骤。
  - 输入：`name: String`；`reason: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4336` `AppModel.beginInventoryOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4050` `AppModel.removeServerHardwareMappingRequirement`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4050 · 方法** `private func removeServerHardwareMappingRequirement(_ name: String)` — 移除Server 数据、五金、映射相关数据或步骤。
  - 输入：`_ name: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:581` `ServerWritePreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L4065 · 方法** `private func consumeInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] ) -> [InventoryPreviewRow]` — 消费并转换库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`[InventoryPreviewRow]`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1130` `InventoryPreviewRow`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`

- **L4140 · 方法** `private func applyInventoryPreviewObject( _ object: [String: Any], accumulated: [InventoryPreviewRow] )` — 应用库存、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1158` `sortedInventoryPreviewRows`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4065` `AppModel.consumeInventoryPreviewObject`

- **L4152 · 方法** `private func previewNext( _ paths: [String], index: Int, selectedDocumentRemarks: Set<String> = [], accumulated: [InventoryPreviewRow] )` — 预览预览相关数据或步骤。
  - 输入：`_ paths: [String]`；`index: Int`；`selectedDocumentRemarks: Set<String> = []`；`accumulated: [InventoryPreviewRow]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1158` `sortedInventoryPreviewRows`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4190` `AppModel.runInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4065` `AppModel.consumeInventoryPreviewObject`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runInventory`；是否真实写入仍取决于分支和参数。

- **L4190 · 方法** `private func runInventory( _ arguments: [String], manageRunning: Bool = true, onFailure: ((String) -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动库存 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`manageRunning: Bool = true`；`onFailure: ((String) -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1989` `AppModel.newOperationID`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2018` `AppModel.environmentForOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4385` `AppModel.consumeInventoryLogChunk`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2000` `AppModel.finishOperationLog`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4352` `AppModel.finishRunningInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Process`, `run`；是否真实写入仍取决于分支和参数。

- **L4336 · 方法** `private func beginInventoryOperation(_ title: String)` — 封装库存、操作相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`

- **L4341 · 方法** `private func addInventoryStep(_ title: String, _ detail: String, _ state: String)` — 新增库存相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4352 · 方法** `private func finishRunningInventoryStep(_ detail: String, _ state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4341` `AppModel.addInventoryStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4366 · 方法** `private func finishInventoryStep(named title: String, detail: String, state: String)` — 结束并收口库存相关数据或步骤。
  - 输入：`named title: String`；`detail: String`；`state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`

- **L4385 · 方法** `private func consumeInventoryLogChunk(_ chunk: String)` — 消费并转换库存、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1360` `appendingInventoryProgressStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1291` `dashboardInventoryProgressText`

- **L4406 · 方法** `private func addOrderStep(_ title: String, _ detail: String, _ state: String)` — 新增订单相关数据或步骤。
  - 输入：`_ title: String`；`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4425 · 方法** `private func finishOrderStep(_ detail: String, _ state: String)` — 结束并收口订单相关数据或步骤。
  - 输入：`_ detail: String`；`_ state: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1196` `InventoryStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record`；是否真实写入仍取决于分支和参数。

- **L4452 · 方法** `private func consumeOrderLogChunk(_ chunk: String)` — 消费并转换订单、日志相关数据或步骤。
  - 输入：`_ chunk: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1341` `updatingLatestRunningStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`

- **L4472 · 方法** `private func runOrder( _ arguments: [String], input: Data? = nil, failureStatus: String = "校验未通过", onFailure: (() -> Void)? = nil, completion: @escaping ([String: Any]) -> Void )` — 启动订单 CLI 子进程，持续消费进度和最终 JSON。
  - 输入：`_ arguments: [String]`；`input: Data? = nil`；`failureStatus: String = "校验未通过"`；`onFailure: (() -> Void`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1989` `AppModel.newOperationID`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4452` `AppModel.consumeOrderLogChunk`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1440` `ResidentOrderServiceClient.start`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2018` `AppModel.environmentForOperation`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1460` `ResidentOrderServiceClient.request`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2000` `AppModel.finishOperationLog`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2396` `AppModel.startPendingDashboardOutboundRefreshIfNeeded`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `startPendingDashboardOutboundRefreshIfNeeded`；是否真实写入仍取决于分支和参数。

- **L4580 · 方法** `func stopResidentOrderService()` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1492` `ResidentOrderServiceClient.stop`

- **L4585 · 方法** `func loadOrderFolders()` — 读取订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:85` `OrderFolderItem`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4623 · 方法** `func previewOrderFolder(_ item: OrderFolderItem, recordSelection: Bool = true)` — 预览预览、订单、文件夹相关数据或步骤。
  - 输入：`_ item: OrderFolderItem`；`recordSelection: Bool = true`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4699` `AppModel.findLocalOrderTraveler`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:946` `orderPreviewIssues`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4733` `AppModel.applyOrderPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4699 · 方法** `private func findLocalOrderTraveler(_ orderId: String) -> String` — 查找订单、Traveler相关数据或步骤。
  - 输入：`_ orderId: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4733 · 方法** `private func applyOrderPreview(_ object: [String: Any], targetOrderID: String? = nil)` — 应用订单、预览相关数据或步骤。
  - 输入：`_ object: [String: Any]`；`targetOrderID: String? = nil`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:956` `OrderMaterialPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1049` `OrderFactoryPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1055` `OrderFittingPreview`

- **L4788 · 方法** `func loadOrderDetailFromDatabase(_ item: OrderDashboardItem)` — 读取订单、数据库相关数据或步骤。
  - 输入：`_ item: OrderDashboardItem`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4858` `AppModel.schedulePendingOrderDetailRetry`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4733` `AppModel.applyOrderPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4858 · 方法** `private func schedulePendingOrderDetailRetry()` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4788` `AppModel.loadOrderDetailFromDatabase`

- **L4876 · 方法** `func saveOrderAnnotations( orderID: String, userNote: String, plannedDays: [OrderInstallationDay], actualDays: [OrderInstallationDay], onStatusChange: @escaping (String) -> Void = { _ in } )` — 保存安装日期、安装人等订单人工备注并刷新详情。
  - 输入：`orderID: String`；`userNote: String`；`plannedDays: [OrderInstallationDay]`；`actualDays: [OrderInstallationDay]`；`onStatusChange: @escaping (String) -> Void = { _ in }`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:18` `businessFriendlyMessage`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2122` `AppModel.applyDashboardObject`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L4924 · 方法** `func setOrderFittingsIgnored(_ rows: [OrderFittingPreview], ignored: Bool)` — 设置订单相关数据或步骤。
  - 输入：`_ rows: [OrderFittingPreview]`；`ignored: Bool`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4623` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `runOrder`；是否真实写入仍取决于分支和参数。

- **L4953 · 方法** `func generateSelectedOrder()` — 生成订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5108` `AppModel.openSelectedOrderTraveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `openSelectedOrderTraveler`；是否真实写入仍取决于分支和参数。

- **L4977 · 方法** `func generateMissingMaterial()` — 生成材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4623` `AppModel.previewOrderFolder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5000 · 方法** `func checkSelectedOrderStock()` — 检查订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1069` `OrderStockPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`；是否真实写入仍取决于分支和参数。

- **L5042 · 方法** `func calculateSelectedOrderCost(export: Bool = false)` — 计算订单、成本相关数据或步骤。
  - 输入：`export: Bool = false`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4472` `AppModel.runOrder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5072` `AppModel.applyOrderCost`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4425` `AppModel.finishOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `runOrder`, `open`；是否真实写入仍取决于分支和参数。

- **L5072 · 方法** `private func applyOrderCost(_ object: [String: Any])` — 应用订单、成本相关数据或步骤。
  - 输入：`_ object: [String: Any]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1081` `OrderCostLine`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1096` `OrderCostFactoryTotal`

- **L5108 · 方法** `func openSelectedOrderTraveler()` — 打开订单、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4406` `AppModel.addOrderStep`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L5126 · 方法** `func openDashboardLocation(_ path: String)` — 打开看板相关数据或步骤。
  - 输入：`_ path: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open`；是否真实写入仍取决于分支和参数。

- **L5139 · 计算属性** `var projectRoot: URL` — 根据当前状态计算并返回`projectRoot` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`URL`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5147 · 枚举** `AppLayout` — 定义 `AppLayout` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5196 · 结构体** `FixedWindowSizeController` — 定义 `FixedWindowSizeController` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5199 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5213` `FixedWindowSizeController.applyFixedSize`

- **L5207 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5213` `FixedWindowSizeController.applyFixedSize`

- **L5213 · 方法** `private func applyFixedSize(to window: NSWindow?)` — 应用与 `applyFixedSize` 对应的数据或步骤。
  - 输入：`to window: NSWindow?`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setFrame`；是否真实写入仍取决于分支和参数。

- **L5227 · 函数** `func inventoryActionColumnCount(availableWidth: CGFloat) -> Int` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`availableWidth: CGFloat`
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5232 · 枚举** `AppPalette` — 定义 `AppPalette` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5246 · 函数** `func inventoryCatalogUpdateSuccessStatus(_ count: Int) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5250 · 函数** `func inventoryCatalogUpdateSuccessStatus( _ count: Int, added: Int, updated: Int, removed: Int ) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ count: Int`；`added: Int`；`updated: Int`；`removed: Int`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5259 · 函数** `func inventoryCatalogUpdateFailureStatus(_ reason: String) -> String` — 封装库存、商品目录、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ reason: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5263 · 枚举** `SettingsStatusKind` — 定义与设置、状态相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5270 · 计算属性** `var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5280 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5291 · 函数** `func settingsStatusKind(_ status: String) -> SettingsStatusKind` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`SettingsStatusKind`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5300 · 函数** `func settingsStatusDisplayText(_ status: String) -> String` — 设置设置、状态相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5306 · 结构体** `SettingsStatusBanner` — 定义与设置、状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5309 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5291` `settingsStatusKind`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5300` `settingsStatusDisplayText`

- **L5337 · 扩展** `View` — 定义 `View` 扩展，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5338 · 方法** `func appPageFrame() -> some View` — 封装 `appPageFrame` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5366` `AppGlassGroupBoxStyle`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5399` `LiquidGlassPreviewBackdrop`

- **L5346 · 方法** `func appInputField(maxWidth: CGFloat? = nil) -> some View` — 封装 `appInputField` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`maxWidth: CGFloat? = nil`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5350 · 方法** `func appActionButton(minWidth: CGFloat = AppLayout.actionButtonWidth) -> some View` — 封装 `appActionButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.actionButtonWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5355 · 方法** `func inventoryActionButton(minWidth: CGFloat = AppLayout.inventoryActionMinWidth) -> some View` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`minWidth: CGFloat = AppLayout.inventoryActionMinWidth`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5366 · 结构体** `AppGlassGroupBoxStyle` — 定义 `AppGlassGroupBoxStyle` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5367 · 方法** `func makeBody(configuration: Configuration) -> some View` — 创建与 `makeBody` 对应的数据或步骤。
  - 输入：`configuration: Configuration`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5380 · 结构体** `AppSurfaceCard<Content` — 定义 `AppSurfaceCard<Content` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5384 · 初始化器** `init(padding: CGFloat = AppLayout.cardPadding, @ViewBuilder content: () -> Content)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`padding: CGFloat = AppLayout.cardPadding`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5389 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5399 · 结构体** `LiquidGlassPreviewBackdrop` — 定义与预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5400 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5434 · 结构体** `AppStatusBadge` — 定义与状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5435 · 枚举** `Kind` — 定义 `Kind` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5440 · 计算属性** `private var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5450 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5465 · 结构体** `WidthPreferenceKey` — 定义 `WidthPreferenceKey` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5468 · 方法** `static func reduce(value: inout CGFloat, nextValue: () -> CGFloat)` — 封装 `reduce` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: inout CGFloat`；`nextValue: () -> CGFloat`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5473 · 结构体** `ScrollingTextOnHover` — 定义 `ScrollingTextOnHover` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5484 · 计算属性** `private var overflow: CGFloat` — 根据当前状态计算并返回`overflow` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5488 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5523` `ScrollingTextOnHover.startScrolling`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5545` `ScrollingTextOnHover.stopScrolling`

- **L5523 · 方法** `private func startScrolling()` — 启动与 `startScrolling` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1280` `Double`

- **L5545 · 方法** `private func stopScrolling()` — 封装 `stopScrolling` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5552 · 结构体** `InventoryActionGrid<Content` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5556 · 初始化器** `init( minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`minColumnWidth: CGFloat = AppLayout.inventoryActionMinWidth`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5564 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5574 · 结构体** `AppPageHeader<Trailing` — 定义 `AppPageHeader<Trailing` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5580 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5585 · 结构体** `OperationLogCard` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5590 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5596 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6160` `SelectableOperationLogView`

- **L5606 · 结构体** `OrderWorkflowView` — 定义与订单相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5610 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5434` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4585` `AppModel.loadOrderFolders`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4623` `AppModel.previewOrderFolder`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1314` `appDisplayTimestamp`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5000` `AppModel.checkSelectedOrderStock`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5585` `OperationLogCard`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5999` `OrderWorkflowView.summaryCard`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6019` `OrderWorkflowView.subsectionTitle`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1037` `panelColorsNeedingThicknessWarning`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:993` `orderedMaterialRows`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:982` `orderMaterialDisplayName`；另有 4 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `setOrderFittingsIgnored`；是否真实写入仍取决于分支和参数。

- **L5999 · 方法** `private func summaryCard(title: String, value: String, detail: String, color: Color, warning: Bool = false) -> some View` — 封装 `summaryCard` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: String`；`value: String`；`detail: String`；`color: Color`；`warning: Bool = false`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6019 · 方法** `private func subsectionTitle(_ title: String, color: Color) -> some View` — 封装 `subsectionTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`color: Color`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6026 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6036 · 结构体** `SettingsCard<Content` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6042 · 初始化器** `init( title: String, symbol: String, padding: CGFloat = 14, @ViewBuilder content: () -> Content )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`title: String`；`symbol: String`；`padding: CGFloat = 14`；`@ViewBuilder content: () -> Content`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6054 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6068 · 结构体** `InventoryStepRowView` — 定义与库存、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6072 · 初始化器** `init(step: InventoryStep, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`step: InventoryStep`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6077 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L6105 · 计算属性** `private var detailText: String` — 根据当前状态计算并返回`detailText` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1233` `operationDurationText`

- **L6111 · 计算属性** `@ViewBuilder private var icon: some View` — 根据当前状态计算并返回`icon` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6126 · 结构体** `InventoryOperationLogView` — 定义与库存、操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6129 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6160` `SelectableOperationLogView`

- **L6137 · 结构体** `OperationLogAutoScroller` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6140 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6144 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6160 · 结构体** `SelectableOperationLogView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6166 · 初始化器** `init(steps: [InventoryStep], emptyText: String, showsDuration: Bool = false)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`；`emptyText: String`；`showsDuration: Bool = false`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6172 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6246` `SelectableOperationLogView.copySelected`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6234` `SelectableOperationLogView.select`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6068` `InventoryStepRowView`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6137` `OperationLogAutoScroller`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copySelected`, `Set`；是否真实写入仍取决于分支和参数。

- **L6229 · 计算属性** `private var scrollRevision: String` — 根据当前状态计算并返回`scrollRevision` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6234 · 方法** `private func select(_ id: UUID)` — 选择与 `select` 对应的数据或步骤。
  - 输入：`_ id: UUID`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`；是否真实写入仍取决于分支和参数。

- **L6246 · 方法** `private func copySelected()` — 封装 `copySelected` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1233` `operationDurationText`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setString`；是否真实写入仍取决于分支和参数。

- **L6266 · 结构体** `InventoryTravelerRowView` — 定义与库存、Traveler、行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6272 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5473` `ScrollingTextOnHover`

- **L6303 · 计算属性** `private var statusColor: Color` — 根据当前状态计算并返回状态、颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6313 · 结构体** `InventoryMappingSheet` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6320 · 初始化器** `init( model: AppModel, travelerName: String, isPresented: Binding<Bool>, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`isPresented: Binding<Bool>`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6332 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5346` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3967` `AppModel.searchInventoryProducts`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3994` `AppModel.saveInventoryMapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryMapping`；是否真实写入仍取决于分支和参数。

- **L6399 · 结构体** `PendingInventoryMappingTarget` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6401 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6404 · 结构体** `PendingInventoryMappingWorkspace` — 定义与库存、映射相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6409 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5434` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6399` `PendingInventoryMappingTarget`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3132` `AppModel.retryPendingMappingPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3034` `AppModel.closeInventoryMappingWorkspace`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5399` `LiquidGlassPreviewBackdrop`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6313` `InventoryMappingSheet`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6495` `PendingInventoryIgnoreSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryMappingWorkspace`；是否真实写入仍取决于分支和参数。

- **L6495 · 结构体** `PendingInventoryIgnoreSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6502 · 初始化器** `init( model: AppModel, travelerName: String, saveAction: ((String, String) -> Void)? = nil )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`travelerName: String`；`saveAction: ((String, String) -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6512 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5346` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3904` `AppModel.saveInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5399` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAction`, `saveInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L6560 · 结构体** `InventoryView` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6571 · 初始化器** `init( model: AppModel, onClose: (() -> Void)? = nil, orderContextID: String = "", orderContextFactoryNames: [String] = [], orderContextFactoryOrders: [String] = [] )` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`onClose: (() -> Void`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6585 · 计算属性** `private var selectedTravelerCount: Int` — 选择Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6589 · 计算属性** `private var hasMappedOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6593 · 计算属性** `private var hasConfirmedNoOutboundRows: Bool` — 根据当前状态计算并返回出库。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6599 · 计算属性** `private var customerSuppliedOnly: Bool` — 根据当前状态计算并返回`customerSuppliedOnly` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L6606 · 计算属性** `private var confirmationTitle: String` — 根据当前状态计算并返回`confirmationTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6613 · 计算属性** `private var selectedTravelerDisplayName: String` — 选择Traveler、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6618 · 方法** `private func previewRowContent(_ row: InventoryPreviewRow) -> some View` — 预览预览、行数据相关数据或步骤。
  - 输入：`_ row: InventoryPreviewRow`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6885` `InventoryView.previewStatusColor`

- **L6654 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5434` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6862` `InventoryView.outboundStep`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5585` `OperationLogCard`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6618` `InventoryView.previewRowContent`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5355` `View.inventoryActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3350` `AppModel.previewOrderInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6313` `InventoryMappingSheet`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6876` `InventoryView.confirmationRow`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3695` `AppModel.openAndFillSelectedInventory`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5399` `LiquidGlassPreviewBackdrop`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outboundStep`, `onClose`, `openAndFillSelectedInventory`；是否真实写入仍取决于分支和参数。

- **L6853 · 方法** `private func statusColor(_ status: String) -> Color` — 封装状态、颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6862 · 方法** `private func outboundStep(_ number: Int, _ title: String, active: Bool) -> some View` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ number: Int`；`_ title: String`；`active: Bool`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6876 · 方法** `private func confirmationRow(_ label: String, _ value: String, valueColor: Color = .primary) -> some View` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ label: String`；`_ value: String`；`valueColor: Color = .primary`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6885 · 方法** `private func previewStatusColor(_ status: String) -> Color` — 预览预览、状态、颜色相关数据或步骤。
  - 输入：`_ status: String`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6894 · 方法** `private func centeredTitle(_ title: String, systemImage: String) -> some View` — 封装 `centeredTitle` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`systemImage: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6904 · 方法** `private func stepIcon(_ state: String) -> some View` — 封装 `stepIcon` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ state: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6918 · 结构体** `TodoView` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6927 · 计算属性** `private var sortedItems: [TodoItem]` — 排序与 `sortedItems` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[TodoItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6948 · 计算属性** `private var selectedItem: TodoItem?` — 选择项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`TodoItem?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6953 · 计算属性** `private var openCount: Int` — 打开与 `openCount` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6957 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5434` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7109` `TodoView.todoRow`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1840` `AppModel.toggleTodoCompletion`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7222` `TodoDeadlinePickerControl`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5338` `View.appPageFrame`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7275` `TodoEditorSheet`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1847` `AppModel.deleteTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `deleteTodo`；是否真实写入仍取决于分支和参数。

- **L7109 · 方法** `private func todoRow(_ item: TodoItem) -> some View` — 封装待办、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7182` `TodoView.deadlineText`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7202` `TodoView.deadlineColor`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7190` `TodoView.deadlineBadge`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1840` `AppModel.toggleTodoCompletion`

- **L7162 · 计算属性** `private var todoSelectionMessage: String?` — 根据当前状态计算并返回待办。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7167 · 计算属性** `private var deleteAlertBinding: Binding<Bool>` — 删除与 `deleteAlertBinding` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Binding<Bool>`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7174 · 方法** `private func addTodo()` — 新增待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7182 · 方法** `private func deadlineText(_ date: Date?) -> String` — 封装 `deadlineText` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date?`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7190 · 方法** `private func deadlineBadge(_ item: TodoItem) -> String?` — 封装 `deadlineBadge` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`String?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7202 · 方法** `private func deadlineColor(_ item: TodoItem) -> Color` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ item: TodoItem`
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7214 · 函数** `func todoDeadlinePickerDisplay(_ date: Date) -> String` — 封装待办相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ date: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7222 · 结构体** `TodoDeadlinePickerControl` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7226 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7214` `todoDeadlinePickerDisplay`

- **L7275 · 结构体** `TodoEditorSheet` — 定义与待办相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7283 · 初始化器** `init(model: AppModel, item: TodoItem)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`model: AppModel`；`item: TodoItem`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7295 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5346` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7222` `TodoDeadlinePickerControl`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1828` `AppModel.updateTodo`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateTodo`；是否真实写入仍取决于分支和参数。

- **L7324 · 结构体** `SettingsView` — 定义与设置相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7331 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5434` `AppStatusBadge`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7629` `SettingsView.compactStatus`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2026` `AppModel.saveAllSettings`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5338` `View.appPageFrame`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3248` `AppModel.refreshInventoryCatalogStatus`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1958` `AppModel.refreshOperationLogInfo`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7842` `OperationLogViewerView`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7645` `InventoryIgnoredMappingsSheet`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7736` `InventoryManualMappingsSheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveAllSettings`；是否真实写入仍取决于分支和参数。

- **L7395 · 计算属性** `private var runAndFileSettingsCard: some View` — 执行文件、设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7579` `SettingsView.settingsRowLabel`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7586` `SettingsView.settingsDateDisplay`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7595` `SettingsView.settingsFieldRow`

- **L7428 · 计算属性** `private var accountSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5346` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2050` `AppModel.saveJdyPassword`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3177` `AppModel.openInventoryChrome`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:2101` `AppModel.saveAimesPassword`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveJdyPassword`, `openInventoryChrome`, `saveAimesPassword`；是否真实写入仍取决于分支和参数。

- **L7481 · 计算属性** `private var inventorySettingsCard: some View` — 根据当前状态计算并返回库存、设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7629` `SettingsView.compactStatus`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3190` `AppModel.updateInventoryCatalog`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7608` `SettingsView.settingsManagementRow`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `updateInventoryCatalog`；是否真实写入仍取决于分支和参数。

- **L7513 · 计算属性** `private var maintenanceSettingsCard: some View` — 根据当前状态计算并返回设置。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1774` `AppModel.performBackup`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1936` `AppModel.setOperationLogEnabled`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1985` `AppModel.logUserAction`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1962` `AppModel.trimOperationLog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setOperationLogEnabled`；是否真实写入仍取决于分支和参数。

- **L7579 · 方法** `private func settingsRowLabel(_ title: String) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7586 · 方法** `private func settingsDateDisplay(_ value: Date) -> String` — 设置设置、日期相关数据或步骤。
  - 输入：`_ value: Date`
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7595 · 方法** `private func settingsFieldRow( _ title: String, placeholder: String, text: Binding<String> ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`placeholder: String`；`text: Binding<String>`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7579` `SettingsView.settingsRowLabel`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5346` `View.appInputField`

- **L7608 · 方法** `private func settingsManagementRow( _ title: String, count: Int, help: String, action: @escaping () -> Void ) -> some View` — 设置设置、行数据相关数据或步骤。
  - 输入：`_ title: String`；`count: Int`；`help: String`；`action: @escaping () -> Void`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`

- **L7629 · 方法** `private func compactStatus(_ status: String) -> some View` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ status: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5300` `settingsStatusDisplayText`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5291` `settingsStatusKind`

- **L7645 · 结构体** `InventoryIgnoredMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7652 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5346` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3904` `AppModel.saveInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3935` `AppModel.updateInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3957` `AppModel.removeInventoryIgnoredMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryIgnoredMapping`, `updateInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L7729 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7736 · 结构体** `InventoryManualMappingsSheet` — 定义与库存相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7744 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5346` `View.appInputField`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3858` `AppModel.saveSettingsManualMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3875` `AppModel.updateSettingsManualMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3894` `AppModel.removeSettingsManualMapping`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3835` `AppModel.refreshInventoryMappings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveSettingsManualMapping`, `updateSettingsManualMapping`；是否真实写入仍取决于分支和参数。

- **L7834 · 方法** `private func clearEditor()` — 清理与 `clearEditor` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7842 · 结构体** `OperationLogViewerView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7847 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`

- **L7913 · 枚举** `AppSection` — 定义 `AppSection` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7919 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7921 · 计算属性** `var title: String` — 根据当前状态计算并返回`title` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7930 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7939 · 计算属性** `var pageTitle: String` — 根据当前状态计算并返回`pageTitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7948 · 计算属性** `var subtitle: String` — 根据当前状态计算并返回`subtitle` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7957 · 计算属性** `var isWorkSection: Bool` — 根据当前状态计算并返回`isWorkSection` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7966 · 结构体** `TopNavigationBar` — 定义 `TopNavigationBar` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7971 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:8083` `TopNavigationBar.navButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5350` `View.appActionButton`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:8107` `TopNavigationBar.designNote`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5399` `LiquidGlassPreviewBackdrop`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6404` `PendingInventoryMappingWorkspace`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteConfirmationSheet`；是否真实写入仍取决于分支和参数。

- **L8062 · 计算属性** `@ViewBuilder private var contextualStatus: some View` — 根据当前状态计算并返回状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5434` `AppStatusBadge`

- **L8083 · 方法** `private func navButton(_ section: AppSection) -> some View` — 封装 `navButton` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ section: AppSection`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8107 · 方法** `private func designNote(_ title: String, _ text: String) -> some View` — 封装 `designNote` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ title: String`；`_ text: String`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8117 · 结构体** `TravelerAssistantApp` — 定义与Traveler相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8121 · 计算属性** `var body: some Scene` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some Scene`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7966` `TopNavigationBar`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:6918` `TodoView`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:7324` `SettingsView`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5366` `AppGlassGroupBoxStyle`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5399` `LiquidGlassPreviewBackdrop`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:5196` `FixedWindowSizeController`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3218` `AppModel.closeInventoryChromeOnQuit`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:4580` `AppModel.stopResidentOrderService`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:1774` `AppModel.performBackup`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `closeInventoryChromeOnQuit`；是否真实写入仍取决于分支和参数。

## `.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift`

Swift/macOS 源码或测试辅助文件。

- **L4 · 类** `OperationLogHarnessModel` — 定义与操作、日志相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7 · 初始化器** `init(steps: [InventoryStep])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L12 · 结构体** `OperationLogHarnessView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 类** `HeaderBoundaryProbeBox` — 定义 `HeaderBoundaryProbeBox` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L25 · 结构体** `HeaderBoundaryProbe` — 定义 `HeaderBoundaryProbe` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L28 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L34 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L39 · 结构体** `PageLayoutHarness` — 定义 `PageLayoutHarness` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L43 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:25` `HeaderBoundaryProbe`

- **L64 · 结构体** `MacOSUIRegressionTests` — 定义 `MacOSUIRegressionTests` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L65 · 方法** `static func main()` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:1448` `MacOSUIRegressionTests.testInventoryTravelerNewestFirst`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:111` `MacOSUIRegressionTests.testPushToTalkShortcut`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:117` `MacOSUIRegressionTests.testSpeechCommandCanonicalization`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:123` `MacOSUIRegressionTests.testAssistantOrderResultParsing`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:144` `MacOSUIRegressionTests.testAssistantCompactHelpAndCancelRules`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:152` `MacOSUIRegressionTests.testMaterialDisplayNames`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:224` `MacOSUIRegressionTests.testOrderDetailMaterialRows`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:252` `MacOSUIRegressionTests.testOrderDashboardRules`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:1044` `MacOSUIRegressionTests.testDashboardActivityIsScopedToAppSession`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:1071` `MacOSUIRegressionTests.testPendingServerSelectionAndRefreshContract`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:1100` `MacOSUIRegressionTests.testPendingInventorySourceFolderPath`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:1118` `MacOSUIRegressionTests.testPendingMaterialMappingIssueRoute`；另有 30 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `testOrderOutboundFactorySelection`, `testServerWriteMaterialPreviewOrdering`, `testServerWriteHardwareChangeLayout`；是否真实写入仍取决于分支和参数。

- **L111 · 方法** `private static func testPushToTalkShortcut()` — 验证与 `testPushToTalkShortcut` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L117 · 方法** `private static func testSpeechCommandCanonicalization()` — 验证与 `testSpeechCommandCanonicalization` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L123 · 方法** `private static func testAssistantOrderResultParsing()` — 验证订单、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L144 · 方法** `private static func testAssistantCompactHelpAndCancelRules()` — 验证与 `testAssistantCompactHelpAndCancelRules` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L152 · 方法** `private static func testMaterialDisplayNames()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:189` `MacOSUIRegressionTests.material`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `inventoryCatalogUpdateSuccessStatus`, `inventoryCatalogUpdateFailureStatus`, `Set`；是否真实写入仍取决于分支和参数。

- **L189 · 方法** `func material(_ kind: String, _ thickness: Double, _ color: String = "") -> OrderMaterialPreview` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ kind: String`；`_ thickness: Double`；`_ color: String = ""`
  - 返回：`OrderMaterialPreview`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L224 · 方法** `private static func testOrderDetailMaterialRows()` — 验证订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L252 · 方法** `private static func testOrderDashboardRules()` — 验证订单、看板相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openRequestedOrderIfAvailable`, `openOrderDetail`, `Set`；是否真实写入仍取决于分支和参数。

- **L1044 · 方法** `private static func testDashboardActivityIsScopedToAppSession()` — 验证看板相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1071 · 方法** `private static func testPendingServerSelectionAndRefreshContract()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardAfterServerWrite`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L1100 · 方法** `private static func testPendingInventorySourceFolderPath()` — 验证库存、来源、文件夹、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1118 · 方法** `private static func testPendingMaterialMappingIssueRoute()` — 验证材料、映射、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1150 · 方法** `private static func testPendingInventoryMappingResumeContract()` — 验证库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryMapping`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L1188 · 方法** `private static func testPendingCenterWorkflowUIContract()` — 验证与 `testPendingCenterWorkflowUIContract` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1204 · 方法** `private static func testPendingMappingCallbacks()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3132` `AppModel.retryPendingMappingPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3092` `AppModel.inventoryMappingWorkspaceDidDismiss`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryMapping`, `closeInventoryMappingWorkspace`, `saveInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L1297 · 方法** `private static func testOrderOutboundFactorySelection()` — 验证订单、出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `orderDashboardOutboundDisplay`, `orderDashboardNeedsOutboundUpdateSelection`, `orderDashboardOutboundActionTitle`；是否真实写入仍取决于分支和参数。

- **L1349 · 方法** `private static func testProductionFeedbackAndDashboardProgress()` — 验证生产、看板、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L1448 · 方法** `private static func testInventoryTravelerNewestFirst()` — 验证库存、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2193` `MacOSUIRegressionTests.traveler`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1461 · 方法** `private static func testSharedPageHeaderHeight()` — 验证与 `testSharedPageHeaderHeight` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1485 · 方法** `private static func testAssistantOrderTimelineContract()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderCenter`；是否真实写入仍取决于分支和参数。

- **L1645 · 方法** `private static func testAssistantStageIconAssets()` — 验证与 `testAssistantStageIconAssets` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1660 · 方法** `private static func testGlassDatePickerContract()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1704 · 方法** `private static func testTodoTableHeaderRoundedCorners()` — 验证待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1727 · 方法** `private static func testSettingsDefaultWindowLayoutContract()` — 验证设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1817 · 方法** `private static func testFixedWindowSizeContract()` — 验证与 `testFixedWindowSizeContract` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1838 · 方法** `private static func testInventoryActionLayoutRules()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:1854` `MacOSUIRegressionTests.preview`

- **L1854 · 方法** `func preview(_ name: String, _ section: String) -> InventoryPreviewRow` — 预览预览相关数据或步骤。
  - 输入：`_ name: String`；`_ section: String`
  - 返回：`InventoryPreviewRow`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1883 · 方法** `private static func testRunningProgressReusesOperationRow()` — 验证进度、操作、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2225` `MacOSUIRegressionTests.fail`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1897 · 方法** `private static func testDashboardInventoryProgressText()` — 验证看板、库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1919 · 方法** `private static func testInventoryProgressKeepsStageHistory()` — 验证库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1930 · 方法** `private static func testDashboardSeparatesInventoryAndRefreshTiming()` — 验证看板、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1956 · 方法** `private static func testOrderOperationDurationFormatting()` — 验证订单、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1961 · 方法** `private static func testServerWriteMaterialPreviewOrdering()` — 验证Server 数据、材料、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`, `sortedServerWriteMaterialChanges`；是否真实写入仍取决于分支和参数。

- **L1978 · 方法** `private static func testServerWriteHardwareChangeLayout()` — 验证Server 数据、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1984 · 方法** `private static func testProductionOrderPaths()` — 验证生产、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L1995 · 方法** `private static func testStockFailureKeepsManualRetryEnabled()` — 验证与 `testStockFailureKeepsManualRetryEnabled` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L2010 · 方法** `private static func testExistingTravelerCanBeUpdatedAfterPreviewFailure()` — 验证Traveler、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderUpdateActionReady`；是否真实写入仍取决于分支和参数。

- **L2025 · 方法** `private static func testDashboardTravelerActionsUseDatabaseFacts()` — 验证看板、Traveler、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L2038 · 方法** `private static func testRelatedPreviewMissingMaterialIssue()` — 验证预览、材料、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L2054 · 方法** `private static func testPP0067MissingMaterialShowsPrompt()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2225` `MacOSUIRegressionTests.fail`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2217` `MacOSUIRegressionTests.pumpRunLoop`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`；是否真实写入仍取决于分支和参数。

- **L2075 · 方法** `private static func testFullPageHeaderBoundaryAlignment()` — 验证与 `testFullPageHeaderBoundaryAlignment` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2084` `MacOSUIRegressionTests.headerBoundaryY`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L2084 · 方法** `private static func headerBoundaryY(flexibleContent: Bool) -> CGFloat` — 封装 `headerBoundaryY` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`flexibleContent: Bool`
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:21` `HeaderBoundaryProbeBox`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:39` `PageLayoutHarness`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2217` `MacOSUIRegressionTests.pumpRunLoop`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2225` `MacOSUIRegressionTests.fail`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L2103 · 方法** `private static func testOperationLogScrollsAfterAppending()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2205` `MacOSUIRegressionTests.step`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:4` `OperationLogHarnessModel`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:12` `OperationLogHarnessView`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2217` `MacOSUIRegressionTests.pumpRunLoop`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2209` `MacOSUIRegressionTests.firstScrollView`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2225` `MacOSUIRegressionTests.fail`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L2154 · 方法** `private static func testOperationLogReader()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`

- **L2164 · 方法** `private static func testOperationLogMaintenance()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`；`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2221` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`；是否真实写入仍取决于分支和参数。

- **L2193 · 方法** `private static func traveler(_ name: String, folder: String, modifiedAt: String) -> InventoryTraveler` — 封装Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`folder: String`；`modifiedAt: String`
  - 返回：`InventoryTraveler`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2205 · 方法** `private static func step(_ index: Int) -> InventoryStep` — 封装 `step` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ index: Int`
  - 返回：`InventoryStep`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2209 · 方法** `private static func firstScrollView(in view: NSView) -> NSScrollView?` — 封装 `firstScrollView` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`in view: NSView`
  - 返回：`NSScrollView?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2217 · 方法** `private static func pumpRunLoop(for seconds: TimeInterval)` — 封装 `pumpRunLoop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`for seconds: TimeInterval`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run`；是否真实写入仍取决于分支和参数。

- **L2221 · 方法** `private static func require(_ condition: @autoclosure () -> Bool, _ message: String)` — 封装 `require` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ condition: @autoclosure () -> Bool`；`_ message: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift:2225` `MacOSUIRegressionTests.fail`

- **L2225 · 方法** `private static func fail(_ message: String) -> Never` — 封装 `fail` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Never`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `docs/learning/pending-center-preview/PendingCenterPreview.swift`

项目文档：PendingCenterPreview。

- **L3 · 枚举** `PendingKind` — 定义 `PendingKind` 枚举，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L9 · 计算属性** `var id: String` — 根据当前状态计算并返回`id` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L11 · 计算属性** `var color: Color` — 根据当前状态计算并返回颜色。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Color`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L20 · 计算属性** `var symbol: String` — 根据当前状态计算并返回`symbol` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`String`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L30 · 结构体** `PendingItem` — 定义与项目相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L47 · 枚举** `MappingStage` — 定义与映射相关的枚举，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L54 · 结构体** `PendingCenterPreviewApp` — 定义与预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L55 · 计算属性** `var body: some Scene` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some Scene`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:64` `PendingCenterPreview`

- **L64 · 结构体** `PendingCenterPreview` — 定义与预览相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L70 · 计算属性** `private var selectedItem: PendingItem` — 选择项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`PendingItem`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L74 · 计算属性** `private var filteredItems: [PendingItem]` — 根据当前状态计算并返回`filteredItems` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[PendingItem]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L83 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:264` `AppHeader`

- **L103 · 计算属性** `private var queue: some View` — 根据当前状态计算并返回`queue` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:293` `QueueRow`

- **L154 · 计算属性** `private var detail: some View` — 根据当前状态计算并返回`detail` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:325` `StatusPill`；`docs/learning/pending-center-preview/PendingCenterPreview.swift:214` `PendingCenterPreview.actionButtons`；`docs/learning/pending-center-preview/PendingCenterPreview.swift:362` `PendingDetail`；`docs/learning/pending-center-preview/PendingCenterPreview.swift:382` `FailureDetail`；`docs/learning/pending-center-preview/PendingCenterPreview.swift:402` `ConfirmationDetail`；`docs/learning/pending-center-preview/PendingCenterPreview.swift:425` `ManualDetail`

- **L214 · 方法** `private func actionButtons(for kind: PendingKind) -> some View` — 封装 `actionButtons` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`for kind: PendingKind`
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:251` `PendingCenterPreview.beginMappingResume`

- **L251 · 方法** `private func beginMappingResume()` — 封装映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L264 · 结构体** `AppHeader` — 定义 `AppHeader` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L267 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L293 · 结构体** `QueueRow` — 定义与行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L297 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L325 · 结构体** `StatusPill` — 定义与状态相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L328 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L338 · 结构体** `DetailSection<Content` — 定义 `DetailSection<Content` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L343 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L362 · 结构体** `PendingDetail` — 定义 `PendingDetail` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L365 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:464` `KeyValueRow`

- **L382 · 结构体** `FailureDetail` — 定义 `FailureDetail` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L385 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:464` `KeyValueRow`

- **L402 · 结构体** `ConfirmationDetail` — 定义 `ConfirmationDetail` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L405 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:477` `ComparisonRow`

- **L425 · 结构体** `ManualDetail` — 定义 `ManualDetail` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L429 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`docs/learning/pending-center-preview/PendingCenterPreview.swift:464` `KeyValueRow`

- **L464 · 结构体** `KeyValueRow` — 定义与行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L469 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L477 · 结构体** `ComparisonRow` — 定义与行数据相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L483 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `outputs/pp0018-material-cost/extract_pp0018.py`

历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。

- **L16 · 函数** `text(value) -> str` — 封装 `text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L20 · 函数** `parse_quantity(value) -> float` — 解析数量相关数据或步骤。
  - 输入：`value`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `text(value).replace`；是否真实写入仍取决于分支和参数。

- **L37 · 函数** `normalize_name(value: str) -> str` — 规范化名称相关数据或步骤。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `value.replace`；是否真实写入仍取决于分支和参数。

- **L43 · 函数** `material_rows(path: Path, sheet_name: str) -> list[dict]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`sheet_name: str`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`；`outputs/pp0018-material-cost/extract_pp0018.py:37` `normalize_name`；`outputs/pp0018-material-cost/extract_pp0018.py:20` `parse_quantity`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.close`；是否真实写入仍取决于分支和参数。

- **L85 · 函数** `room_name(path: Path) -> str` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.close`；是否真实写入仍取决于分支和参数。

- **L93 · 函数** `load_prices() -> dict[str, dict]` — 读取与 `load_prices` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`dict[str, dict]`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.close`；是否真实写入仍取决于分支和参数。

- **L115 · 函数** `mapped_price(material_name: str, raw_remark: str, prices: dict[str, dict]) -> dict` — 封装 `mapped_price` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`material_name: str`；`raw_remark: str`；`prices: dict[str, dict]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:37` `normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `normalize_name(material_name).replace`；是否真实写入仍取决于分支和参数。

- **L162 · 函数** `main() -> None` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:93` `load_prices`；`outputs/pp0018-material-cost/extract_pp0018.py:85` `room_name`；`outputs/pp0018-material-cost/extract_pp0018.py:43` `material_rows`；`outputs/pp0018-material-cost/extract_pp0018.py:37` `normalize_name`；`outputs/pp0018-material-cost/extract_pp0018.py:115` `mapped_price`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `normalize_name(row['name']).replace`, `set`, `normalize_name(item['name']).replace`, `entry.update`, `OUTPUT_JSON.parent.mkdir`, `OUTPUT_JSON.write_text`；是否真实写入仍取决于分支和参数。

## `scripts/build-app`

构建 PP FlowHub.app，组装 Swift、Python、资源和辅助工具。

- **L1 · 脚本过程** `scripts/build-app "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/install-app`

签名、校验并把构建产物安装到 /Applications。

- **L1 · 脚本过程** `scripts/install-app "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/pp-flowhub`

统一命令入口：选择 Python 运行时并分发 assistant/order/inventory 子命令。

- **L1 · 脚本过程** `scripts/pp-flowhub "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/test-aimes-table`

项目配置、资源或辅助文件。

- **L1 · 脚本过程** `scripts/test-aimes-table "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/test-macos-ui`

编译并运行 Swift/macOS 源码契约与 UI 回归测试。

- **L1 · 脚本过程** `scripts/test-macos-ui "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/test-release`

正式发布测试门禁：串联 Python、Swift UI 和工作簿测试。

- **L1 · 脚本过程** `scripts/test-release "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/test-workbook-e2e`

用固定样本执行 Traveler/材料工作簿端到端验证。

- **L1 · 脚本过程** `scripts/test-workbook-e2e "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · Shell 函数** `search_text(位置参数)` — 封装 `search_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$1…：位置参数`
  - 返回：`进程状态`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L17 · Shell 函数** `search_text(位置参数)` — 封装 `search_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$1…：位置参数`
  - 返回：`进程状态`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_aimes_table.mjs`

自动化测试：验证 `aimes_table` 模块或业务场景。

- **L8 · 函数** `tableMarkup(headers = HEADERS, rows = [])` — 封装 `tableMarkup` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`headers = HEADERS`；`rows = []`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 函数** `withPage(browser, body, test)` — 封装 `withPage` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`browser`；`body`；`test`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `setContent`, `close`；是否真实写入仍取决于分支和参数。

- **L32 · 函数** `main()` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tests/test_aimes_table.mjs:21` `withPage`；`tests/test_aimes_table.mjs:8` `tableMarkup`；`tools/aimes_table.mjs:77` `readAimesTable`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `launch`, `setTimeout`, `insertAdjacentHTML`, `close`；是否真实写入仍取决于分支和参数。

## `tests/test_command_router.py`

自动化测试：验证 `command_router` 模块或业务场景。

- **L14 · 类** `LocalCommandRouterTests` — 定义 `LocalCommandRouterTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 方法** `LocalCommandRouterTests.test_common_phrasings_are_zero_token_commands()` — 验证与 `test_common_phrasings_are_zero_token_commands` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L20 · 方法** `LocalCommandRouterTests.test_spoken_mixed_digits_are_normalized_before_routing()` — 验证与 `test_spoken_mixed_digits_are_normalized_before_routing` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L26 · 方法** `LocalCommandRouterTests.test_stock_comparison_has_priority_over_order_preview()` — 验证订单、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L32 · 方法** `LocalCommandRouterTests.test_write_commands_require_approval()` — 验证与 `test_write_commands_require_approval` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L56 · 方法** `LocalCommandRouterTests.test_manual_hardware_gateway_stops_at_preview_without_approval()` — 验证五金、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `execute_local_command`；是否真实写入仍取决于分支和参数。

- **L75 · 方法** `LocalCommandRouterTests.test_stock_comparison_uses_database_order_facts()` — 验证数据库、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `execute_local_command`；是否真实写入仍取决于分支和参数。

- **L88 · 方法** `LocalCommandRouterTests.test_cut_to_size_commands_use_the_cut_to_size_source()` — 验证来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pp_folder.mkdir`, `cs_folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L101 · 方法** `LocalCommandRouterTests.test_missing_order_reports_the_directory_actually_searched()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `root.mkdir`；是否真实写入仍取决于分支和参数。

- **L111 · 方法** `LocalCommandRouterTests.test_unrecognized_text_requests_agent()` — 验证与 `test_unrecognized_text_requests_agent` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L114 · 方法** `LocalCommandRouterTests.test_agent_factory_suffix_is_rebuilt_only_when_present_in_user_text()` — 验证工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L140 · 方法** `LocalCommandRouterTests.test_split_order_factory_name_is_not_mixed_into_base_order()` — 验证订单、工厂单、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L146 · 方法** `LocalCommandRouterTests.test_gateway_rejects_unknown_tools()` — 验证与 `test_gateway_rejects_unknown_tools` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `execute_local_command`；是否真实写入仍取决于分支和参数。

## `tests/test_core.py`

自动化测试：验证 `core` 模块或业务场景。

- **L23 · 类** `CoreTests` — 定义 `CoreTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L24 · 方法** `CoreTests.test_aimes_failure_parser_ignores_progress_and_prefers_final_error()` — 验证AIMES 数据、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L33 · 方法** `CoreTests.test_aimes_table_not_ready_has_distinct_classification()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L37 · 方法** `CoreTests.test_aimes_table_schema_still_has_schema_classification()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L41 · 方法** `CoreTests.test_aimes_failure_logs_final_error_with_credentials_and_url_redacted()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L55 · 方法** `CoreTests.test_aimes_failure_logs_final_error_with_credentials_and_url_redacted.fail_with_progress(command, input_text, env, timeout, on_stderr_line)` — 封装进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`command`；`input_text`；`env`；`timeout`；`on_stderr_line`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L92 · 方法** `CoreTests.test_aimes_real_credential_error_keeps_credential_classification()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L117 · 方法** `CoreTests.test_aimes_failure_log_respects_disabled_operation_logging()` — 验证AIMES 数据、日志、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L139 · 方法** `CoreTests.test_aimes_bulk_defaults_to_50_but_exact_lookup_has_no_bulk_limit()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L155 · 方法** `CoreTests.test_name_normalization()` — 验证名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L159 · 方法** `CoreTests.test_exact_aimes_verification_preserves_missing_rows_as_a_distinct_result()` — 验证AIMES 数据、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L178 · 方法** `CoreTests.test_recent_fetch_and_exact_verification_share_one_lookup_session()` — 验证与 `test_recent_fetch_and_exact_verification_share_one_lookup_session` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L217 · 方法** `CoreTests.test_settings_load_only_runtime_paths_and_cutoff()` — 验证设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L233 · 方法** `CoreTests.test_invalid_cutoff_date_is_rejected()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L241 · 方法** `CoreTests.test_server_profile_uses_production_paths_when_active_source_is_local()` — 验证Server 数据、生产、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L258 · 方法** `CoreTests.test_aimes_username_is_loaded_without_loading_a_password()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L267 · 方法** `CoreTests.test_local_profile_derives_all_isolated_paths()` — 验证与 `test_local_profile_derives_all_isolated_paths` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L278 · 方法** `CoreTests.test_operation_log_setting_is_loaded_and_defaults_to_enabled()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

## `tests/test_costing.py`

自动化测试：验证 `costing` 模块或业务场景。

- **L13 · 类** `CostingTests` — 定义 `CostingTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L14 · 方法** `CostingTests._config(root: Path) -> Config` — 封装 `_config` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`root: Path`
  - 返回：`Config`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_replace_product_database`；是否真实写入仍取决于分支和参数。

- **L29 · 方法** `CostingTests.test_order_total_uses_order_material_summary_and_raw_quantities()` — 验证订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_costing.py:14` `CostingTests._config`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`, `workbook.close`；是否真实写入仍取决于分支和参数。

- **L66 · 方法** `CostingTests.test_missing_cost_price_is_not_treated_as_zero()` — 验证成本相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_costing.py:14` `CostingTests._config`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L84 · 方法** `CostingTests.test_display_lines_use_material_business_order_and_aggregate_hardware()` — 验证材料、订单、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_costing.py:85` `CostingTests.test_display_lines_use_material_business_order_and_aggregate_hardware.line`

- **L85 · 方法** `CostingTests.test_display_lines_use_material_business_order_and_aggregate_hardware.line(category, code, name, quantity, factory = '材料汇总', unit = 'pcs', price = 1.0)` — 封装 `line` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`category`；`code`；`name`；`quantity`；`factory = '材料汇总'`；`unit = 'pcs'`；`price = 1.0`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_hardware_facts.py`

自动化测试：验证 `hardware_facts` 模块或业务场景。

- **L17 · 类** `HardwareFactsTests` — 定义与五金相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L18 · 方法** `HardwareFactsTests.setUp()` — 设置与 `setUp` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_replace_product_database`, `self.store.upsert_order`, `self.store.upsert_factory`, `self.store.commit`；是否真实写入仍取决于分支和参数。

- **L35 · 方法** `HardwareFactsTests.test_path_switch_repeat_and_restart_preserve_one_projection()` — 验证路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `replace_factory_hardware`, `self.c.commit`, `reopened.execute`, `self.c.execute`；是否真实写入仍取决于分支和参数。

- **L45 · 方法** `HardwareFactsTests.test_duplicate_legacy_paths_replaced_and_manual_preserved()` — 验证与 `test_duplicate_legacy_paths_replaced_and_manual_preserved` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.c.execute`, `replace_factory_hardware`；是否真实写入仍取决于分支和参数。

- **L54 · 方法** `HardwareFactsTests.test_failed_insert_rolls_back_deletion_even_when_caller_commits()` — 验证与 `test_failed_insert_rolls_back_deletion_even_when_caller_commits` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `replace_factory_hardware`, `self.c.commit`, `self.c.execute`；是否真实写入仍取决于分支和参数。

- **L63 · 方法** `HardwareFactsTests.test_material_only_preview_and_missing_factory_do_not_delete()` — 验证材料、预览、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `replace_factory_hardware`, `self.c.commit`, `self.c.execute`；是否真实写入仍取决于分支和参数。

- **L72 · 方法** `HardwareFactsTests.test_test_source_cannot_target_production_database()` — 验证来源、生产、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L82 · 方法** `HardwareFactsTests.test_confirmed_shipment_survives_changed_missing_data_and_rename()` — 验证与 `test_confirmed_shipment_survives_changed_missing_data_and_rename` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.c.execute`, `self.c.commit`, `replace_factory_hardware`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L102 · 方法** `HardwareFactsTests.test_complete_empty_and_missing_source_have_distinct_meanings()` — 验证来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `replace_factory_hardware`, `self.c.execute`；是否真实写入仍取决于分支和参数。

## `tests/test_inventory.py`

自动化测试：验证 `inventory` 模块或业务场景。

- **L68 · 类** `_FakeNodeInput` — 定义 `_FakeNodeInput` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L71 · 方法** `_FakeNodeInput.__init__()` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L75 · 方法** `_FakeNodeInput.write(value)` — 写入与 `write` 对应的数据或步骤。
  - 输入：`value`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L79 · 方法** `_FakeNodeInput.close()` — 关闭与 `close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L83 · 类** `_FakeNodeProcess` — 定义 `_FakeNodeProcess` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L86 · 方法** `_FakeNodeProcess.__init__(result = None, timeout = None)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`result = None`；`timeout = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:68` `_FakeNodeInput`

- **L96 · 方法** `_FakeNodeProcess.wait(timeout = None)` — 封装 `wait` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`timeout = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L102 · 方法** `_FakeNodeProcess.kill()` — 封装 `kill` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L116 · 函数** `make_traveler(path: Path, items)` — 创建Traveler相关数据或步骤。
  - 输入：`path: Path`；`items`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L173 · 函数** `make_catalog(path: Path)` — 创建商品目录相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L190 · 函数** `make_priced_catalog(path: Path)` — 创建商品目录相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L200 · 函数** `seed_sku_products(connection) -> None` — 封装 `seed_sku_products` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.executemany`；是否真实写入仍取决于分支和参数。

- **L230 · 类** `InventoryTests` — 定义与库存相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L231 · 方法** `InventoryTests.test_database_outbound_blocks_multiple_base_server_material_sources()` — 验证数据库、出库、Server 数据、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L255 · 方法** `InventoryTests.test_shipment_without_hardware_marks_status_without_inventory_document()` — 验证五金、状态、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(config.state_dir / 'inventory').mkdir`, `store.connection.execute`, `store.commit`, `store.close`, `mark_no_hardware_outbound`, `sqlite3.connect(config.workflow_database).execute`；是否真实写入仍取决于分支和参数。

- **L286 · 方法** `InventoryTests.test_customer_supplied_outbound_marks_database_only_and_reopens_on_fact_change()` — 验证出库、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`, `database_outbound_fingerprint`, `mark_customer_supplied_outbound`, `connection.execute`, `_refresh_outbound_status`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L351 · 方法** `InventoryTests.test_hardware_scope_requires_actual_positive_hardware_facts()` — 验证五金、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `outbound_scope_decisions`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L372 · 方法** `InventoryTests.test_outbound_scope_read_returns_latest_relevant_saved_decision()` — 验证出库、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`, `outbound_scope_decisions`；是否真实写入仍取决于分支和参数。

- **L408 · 方法** `InventoryTests.test_cut_to_size_customer_supplied_material_stays_fact_but_is_not_outbound()` — 验证材料、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`；`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(config.state_dir / 'inventory').mkdir`, `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`, `sqlite3.connect(config.workflow_database).execute`；是否真实写入仍取决于分支和参数。

- **L451 · 方法** `InventoryTests.test_database_outbound_blocks_mismatched_factory_name_order_prefix()` — 验证数据库、出库、工厂单、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L475 · 方法** `InventoryTests.test_customer_supplied_scope_is_rejected_for_owned_order()` — 验证范围、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L489 · 方法** `InventoryTests.test_owned_order_rejects_even_normalized_outbound_scope_decision()` — 验证订单、出库、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.commit`, `store.close`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L503 · 方法** `InventoryTests.test_remainder_decision_allows_empty_order_without_opening_browser()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L520 · 方法** `InventoryTests.test_database_order_outbound_preview_maps_without_traveler_file()` — 验证数据库、订单、出库、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`；`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'inventory').mkdir`, `(state / 'inventory' / 'mappings.json').write_text`, `store.connection.execute`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L570 · 方法** `InventoryTests.test_order_context_source_no_longer_requires_traveler_gate()` — 验证订单、来源、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L657 · 方法** `InventoryTests.test_database_outbound_status_changes_when_persisted_order_data_changes()` — 验证数据库、出库、状态、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`；`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'inventory').mkdir`, `(state / 'inventory' / 'mappings.json').write_text`, `store.connection.execute`, `store.commit`, `store.close`, `_refresh_outbound_status`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L721 · 方法** `InventoryTests.test_inventory_page_detection_accepts_tenant_workbench_subdomain()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L732 · 方法** `InventoryTests.test_inventory_service_workbench_is_an_entry_page()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L738 · 方法** `InventoryTests.test_inventory_page_detection_still_rejects_login_and_non_inventory_urls()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L743 · 方法** `InventoryTests.test_jdy_cdp_cleanup_uses_playwright_browser_close()` — 验证与 `test_jdy_cdp_cleanup_uses_playwright_browser_close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L753 · 方法** `InventoryTests.test_outbound_navigation_reuses_existing_list_and_opens_visible_menu_item()` — 验证出库、项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L798 · 方法** `InventoryTests.test_outbound_timeout_persists_completed_documents_before_retry()` — 验证出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L805 · 方法** `InventoryTests.test_jdy_outbound_uses_direct_edit_and_post_save_history_verification()` — 验证出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L817 · 方法** `InventoryTests.test_jdy_error_detail_explains_reused_page_menu_timeout()` — 验证与 `test_jdy_error_detail_explains_reused_page_menu_timeout` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L824 · 方法** `InventoryTests.test_outbound_preview_hides_bottom_write_note()` — 验证出库、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L828 · 方法** `InventoryTests.test_outbound_preview_rows_are_full_row_clickable_and_scroll_independently()` — 验证出库、预览、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L856 · 方法** `InventoryTests.test_order_dashboard_outbound_refresh_and_panel_color_layout_contract()` — 验证订单、看板、出库、颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L870 · 方法** `InventoryTests.test_server_hardware_choice_highlights_selected_action()` — 验证Server 数据、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L882 · 方法** `InventoryTests.test_inventory_chrome_success_result_has_no_hidden_login_prompt()` — 验证库存、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L888 · 方法** `InventoryTests.test_order_preview_materials_can_be_mapped_for_stock_check()` — 验证订单、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog.parent.mkdir`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L908 · 方法** `InventoryTests.test_jdy_runtime_uses_portable_overrides_and_rejects_missing_dependencies()` — 验证与 `test_jdy_runtime_uses_portable_overrides_and_rejects_missing_dependencies` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `node.parent.mkdir`, `(modules / 'playwright').mkdir`, `(modules / 'playwright-core').mkdir`；是否真实写入仍取决于分支和参数。

- **L935 · 方法** `InventoryTests.test_stock_requirements_default_to_materials_and_can_include_hardware()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L952 · 方法** `InventoryTests.test_stock_check_compares_required_and_available_quantities()` — 验证与 `test_stock_check_compares_required_and_available_quantities` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog.parent.mkdir`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L980 · 方法** `InventoryTests.test_cut_to_size_folder_status_can_be_reconciled()` — 验证文件夹、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L1000 · 方法** `InventoryTests.test_online_catalog_update_exports_validates_and_installs()` — 验证商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_catalog_online`, `loaded.close`；是否真实写入仍取决于分支和参数。

- **L1005 · 方法** `InventoryTests.test_online_catalog_update_exports_validates_and_installs.fake_export(_config, action, **kwargs)` — 封装 `fake_export` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_config`；`action`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`

- **L1023 · 方法** `InventoryTests.test_catalog_import_persists_cost_price_and_keeps_missing_price_null()` — 验证商品目录、成本相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:190` `make_priced_catalog`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`, `loaded.close`；是否真实写入仍取决于分支和参数。

- **L1046 · 方法** `InventoryTests.test_catalog_change_summary_reports_added_updated_and_removed_products()` — 验证商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1061 · 方法** `InventoryTests.test_catalog_change_summary_detects_cost_price_change()` — 验证商品目录、成本相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1070 · 方法** `InventoryTests.test_close_inventory_chrome_uses_dedicated_cdp_action()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close_inventory_chrome`；是否真实写入仍取决于分支和参数。

- **L1088 · 方法** `InventoryTests.test_lazy_traveler_listing_reports_existing_catalog_status()` — 验证Traveler、商品目录、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`

- **L1103 · 方法** `InventoryTests.test_catalog_refresh_keeps_only_latest_xlsx_backup()` — 验证商品目录、备份相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `inventory_dir.mkdir`, `old_backup.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1122 · 方法** `InventoryTests.test_runtime_product_search_uses_database_after_xlsx_is_removed()` — 验证数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog.parent.mkdir`, `catalog.unlink`, `loaded.close`；是否真实写入仍取决于分支和参数。

- **L1136 · 方法** `InventoryTests.test_browser_error_preserves_specific_reason()` — 验证与 `test_browser_error_preserves_specific_reason` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1143 · 方法** `InventoryTests.test_multiline_browser_error_keeps_first_specific_reason()` — 验证与 `test_multiline_browser_error_keeps_first_specific_reason` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1151 · 方法** `InventoryTests.test_login_failure_hides_full_page_dump_and_explains_retry()` — 验证与 `test_login_failure_hides_full_page_dump_and_explains_retry` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1162 · 方法** `InventoryTests.test_security_challenge_error_explains_visible_login_recovery()` — 验证与 `test_security_challenge_error_explains_visible_login_recovery` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1171 · 方法** `InventoryTests.test_profile_lock_failure_is_reported_as_retryable()` — 验证与 `test_profile_lock_failure_is_reported_as_retryable` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1181 · 方法** `InventoryTests.test_browser_runtime_noise_does_not_hide_specific_export_timeout()` — 验证与 `test_browser_runtime_noise_does_not_hide_specific_export_timeout` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1192 · 方法** `InventoryTests.test_run_jdy_passes_attachable_chrome_endpoint()` — 验证与 `test_run_jdy_passes_attachable_chrome_endpoint` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:83` `_FakeNodeProcess`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1217 · 方法** `InventoryTests.test_run_jdy_reuses_existing_inventory_page_without_reading_keychain()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:83` `_FakeNodeProcess`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1246 · 方法** `InventoryTests.test_inventory_operation_journal_reuses_confirmed_production_across_retry_batch_numbers()` — 验证库存、操作、生产相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `journal.update`；是否真实写入仍取决于分支和参数。

- **L1281 · 方法** `InventoryTests.test_inventory_operation_journal_resumes_after_partial_document_confirmation()` — 验证库存、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `journal.update`；是否真实写入仍取决于分支和参数。

- **L1310 · 方法** `InventoryTests.test_open_inventory_chrome_launches_dedicated_profile_and_debug_port()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open_inventory_chrome`；是否真实写入仍取决于分支和参数。

- **L1328 · 方法** `InventoryTests.test_open_inventory_chrome_does_not_launch_second_browser_on_login_page()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open_inventory_chrome`；是否真实写入仍取决于分支和参数。

- **L1341 · 方法** `InventoryTests.test_outbound_stops_before_browser_when_material_mapping_is_missing()` — 验证出库、材料、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `traveler.parent.mkdir`, `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1357 · 方法** `InventoryTests.test_database_shipped_factory_is_hard_blocked()` — 验证数据库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `assert_factory_orders_outbound_allowed`；是否真实写入仍取决于分支和参数。

- **L1381 · 方法** `InventoryTests.test_database_shipped_factory_with_changed_data_can_be_updated()` — 验证数据库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `assert_factory_orders_outbound_allowed`；是否真实写入仍取决于分支和参数。

- **L1409 · 方法** `InventoryTests.test_run_jdy_converts_browser_timeout_to_actionable_rule_error()` — 验证与 `test_run_jdy_converts_browser_timeout_to_actionable_rule_error` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:83` `_FakeNodeProcess`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1426 · 方法** `InventoryTests.test_keychain_timeout_is_reported_as_credentials_error()` — 验证与 `test_keychain_timeout_is_reported_as_credentials_error` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `helper.write_text`；是否真实写入仍取决于分支和参数。

- **L1441 · 方法** `InventoryTests.test_parse_dynamic_regions_and_zero()` — 验证与 `test_parse_dynamic_regions_and_zero` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`

- **L1450 · 方法** `InventoryTests.test_fixed_mapping_and_push_open_expansion()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1471 · 方法** `InventoryTests.test_factory_selection_keeps_order_materials_and_selected_hardware_only()` — 验证工厂单、订单、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`, `set`；是否真实写入仍取决于分支和参数。

- **L1498 · 方法** `InventoryTests.test_zero_quantity_items_are_not_outbound_rows()` — 验证数量、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1513 · 方法** `InventoryTests.test_unique_exact_inventory_name_maps_bls36()` — 验证库存、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1530 · 方法** `InventoryTests.test_ignored_material_requires_reason_and_is_visible()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1543 · 方法** `InventoryTests.test_edge_quantity_is_rounded_half_up_for_inventory()` — 验证数量、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1556 · 方法** `InventoryTests.test_manual_edge_mapping_also_rounds_quantity_for_inventory()` — 验证映射、数量、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1577 · 方法** `InventoryTests.test_edge_prefers_matching_color_abs_banding_with_24mm_suffix()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1598 · 方法** `InventoryTests.test_back_panel_8mm_and_9mm_are_bidirectional_aliases()` — 验证与 `test_back_panel_8mm_and_9mm_are_bidirectional_aliases` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`；`tests/test_inventory.py:116` `make_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1615 · 方法** `InventoryTests.test_ignored_mapping_can_be_saved_and_removed()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_ignored`；是否真实写入仍取决于分支和参数。

- **L1627 · 方法** `InventoryTests.test_source_codes_are_not_treated_as_inventory_skus()` — 验证来源、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set_ignored_mapping`；是否真实写入仍取决于分支和参数。

- **L1648 · 方法** `InventoryTests.test_lower_rail_names_resolve_to_l_rail_sku()` — 验证与 `test_lower_rail_names_resolve_to_l_rail_sku` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1667 · 方法** `InventoryTests.test_repair_hardware_collapses_lower_rail_pair_rows()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`；`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `connection.executemany`, `connection.commit`, `connection.close`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L1704 · 方法** `InventoryTests.test_ignoring_hardware_removes_existing_database_facts()` — 验证五金、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.executemany`, `connection.commit`, `connection.close`, `set_ignored_mapping`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L1749 · 方法** `InventoryTests.test_manual_mapping_can_be_saved_and_replaces_ignore()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_ignored`, `InventoryMappings(path).save_manual`；是否真实写入仍取决于分支和参数。

- **L1759 · 方法** `InventoryTests.test_manual_mapping_can_be_viewed_updated_and_removed()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save_manual_mapping`, `update_manual_mapping`；是否真实写入仍取决于分支和参数。

- **L1773 · 方法** `InventoryTests.test_hardware_display_name_is_shared_by_sku_aliases()` — 验证五金、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save_manual_mapping`；是否真实写入仍取决于分支和参数。

- **L1794 · 方法** `InventoryTests.test_sync_status_changes_with_traveler_fingerprint()` — 验证状态、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mapping_path.write_text`, `store.save_success`；是否真实写入仍取决于分支和参数。

- **L1815 · 方法** `InventoryTests.test_order_material_outbound_links_only_selected_split_factories()` — 验证订单、材料、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`；`tests/test_inventory.py:1856` `InventoryTests.test_order_material_outbound_links_only_selected_split_factories.preview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.connection.execute`, `store.commit`, `store.close`, `OutboundItem`, `sync.save_success`, `connection.execute`, `connection.close`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L1856 · 方法** `InventoryTests.test_order_material_outbound_links_only_selected_split_factories.preview(factory_order)` — 预览预览相关数据或步骤。
  - 输入：`factory_order`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1947 · 方法** `InventoryTests.test_production_material_outbound_does_not_mark_factory_orders_shipped()` — 验证生产、材料、出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `OutboundItem`, `_persist_single_outbound_result`, `connection.execute`, `sync.save_success`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2036 · 方法** `InventoryTests.test_production_browser_success_commits_materials_and_batch()` — 验证生产相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`；`tests/test_inventory.py:83` `_FakeNodeProcess`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `OutboundItem`, `run_jdy`, `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2124 · 方法** `InventoryTests.test_split_production_material_document_cleans_stale_factory_links()` — 验证生产、材料、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:200` `seed_sku_products`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `OutboundItem`, `sync.save_success`, `connection.execute`, `connection.commit`, `connection.close`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L2222 · 方法** `InventoryTests.test_previous_hardware_block_becoming_empty_requires_manual_void()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`；`tests/test_inventory.py:173` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mapping_path.write_text`, `store.save_success`；是否真实写入仍取决于分支和参数。

- **L2248 · 方法** `InventoryTests.test_hardware_shipment_ignores_previous_order_material_document()` — 验证五金、订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`, `OutboundItem`；是否真实写入仍取决于分支和参数。

- **L2298 · 方法** `InventoryTests.test_outbound_status_prefers_factory_hardware_over_order_material_record()` — 验证出库、状态、工厂单、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_refresh_outbound_status`, `_has_factory_hardware_outbound_record`；是否真实写入仍取决于分支和参数。

- **L2332 · 方法** `InventoryTests.test_sqlite_outbound_record_uses_sync_kind_for_hardware_reconciliation()` — 验证出库、记录、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `connection.execute`, `connection.commit`, `connection.close`, `_load_outbound_records`, `reconcile_outbound_statuses`, `reopened.execute`；是否真实写入仍取决于分支和参数。

- **L2395 · 方法** `InventoryTests.test_same_hardware_name_is_aggregated_within_factory()` — 验证五金、名称、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:116` `make_traveler`

## `tests/test_legacy_fittings.py`

自动化测试：验证 `legacy_fittings` 模块或业务场景。

- **L12 · 类** `LegacyFittingsTests` — 定义 `LegacyFittingsTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L13 · 方法** `LegacyFittingsTests.test_discovery_and_parsing_across_report_versions()` — 验证与 `test_discovery_and_parsing_across_report_versions` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

## `tests/test_macos_ui.swift`

自动化测试：验证 `macos_ui` 模块或业务场景。

- **L4 · 类** `OperationLogHarnessModel` — 定义与操作、日志相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7 · 初始化器** `init(steps: [InventoryStep])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L12 · 结构体** `OperationLogHarnessView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 类** `HeaderBoundaryProbeBox` — 定义 `HeaderBoundaryProbeBox` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L25 · 结构体** `HeaderBoundaryProbe` — 定义 `HeaderBoundaryProbe` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L28 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L34 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L39 · 结构体** `PageLayoutHarness` — 定义 `PageLayoutHarness` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L43 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:25` `HeaderBoundaryProbe`

- **L64 · 结构体** `MacOSUIRegressionTests` — 定义 `MacOSUIRegressionTests` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L65 · 方法** `static func main()` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2026` `MacOSUIRegressionTests.testInventoryTravelerNewestFirst`；`tests/test_macos_ui.swift:118` `MacOSUIRegressionTests.testPushToTalkShortcut`；`tests/test_macos_ui.swift:124` `MacOSUIRegressionTests.testSpeechCommandCanonicalization`；`tests/test_macos_ui.swift:130` `MacOSUIRegressionTests.testAssistantOrderResultParsing`；`tests/test_macos_ui.swift:151` `MacOSUIRegressionTests.testAssistantCompactHelpAndCancelRules`；`tests/test_macos_ui.swift:159` `MacOSUIRegressionTests.testMaterialDisplayNames`；`tests/test_macos_ui.swift:231` `MacOSUIRegressionTests.testOrderDetailMaterialRows`；`tests/test_macos_ui.swift:259` `MacOSUIRegressionTests.testOrderDashboardRules`；`tests/test_macos_ui.swift:1080` `MacOSUIRegressionTests.testDashboardActivityIsScopedToAppSession`；`tests/test_macos_ui.swift:1107` `MacOSUIRegressionTests.testDashboardSessionMessagesAndAimesProgress`；`tests/test_macos_ui.swift:1297` `MacOSUIRegressionTests.testDashboardStartupProgressAndHistory`；`tests/test_macos_ui.swift:1447` `MacOSUIRegressionTests.testDashboardAimesStatusResolution`；另有 37 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `testOrderOutboundFactorySelection`, `testServerWriteMaterialPreviewOrdering`, `testServerWriteHardwareChangeLayout`；是否真实写入仍取决于分支和参数。

- **L118 · 方法** `private static func testPushToTalkShortcut()` — 验证与 `testPushToTalkShortcut` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L124 · 方法** `private static func testSpeechCommandCanonicalization()` — 验证与 `testSpeechCommandCanonicalization` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L130 · 方法** `private static func testAssistantOrderResultParsing()` — 验证订单、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L151 · 方法** `private static func testAssistantCompactHelpAndCancelRules()` — 验证与 `testAssistantCompactHelpAndCancelRules` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L159 · 方法** `private static func testMaterialDisplayNames()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`；`tests/test_macos_ui.swift:196` `MacOSUIRegressionTests.material`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `inventoryCatalogUpdateSuccessStatus`, `inventoryCatalogUpdateFailureStatus`, `Set`；是否真实写入仍取决于分支和参数。

- **L196 · 方法** `func material(_ kind: String, _ thickness: Double, _ color: String = "") -> OrderMaterialPreview` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ kind: String`；`_ thickness: Double`；`_ color: String = ""`
  - 返回：`OrderMaterialPreview`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L231 · 方法** `private static func testOrderDetailMaterialRows()` — 验证订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L259 · 方法** `private static func testOrderDashboardRules()` — 验证订单、看板相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openRequestedOrderIfAvailable`, `openOrderDetail`, `Set`；是否真实写入仍取决于分支和参数。

- **L1080 · 方法** `private static func testDashboardActivityIsScopedToAppSession()` — 验证看板相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L1107 · 方法** `private static func testDashboardSessionMessagesAndAimesProgress()` — 验证看板、AIMES 数据、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`；`tests/test_macos_ui.swift:1128` `MacOSUIRegressionTests.aimesPayload`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `insert`, `refreshDashboardOrdersAfterOutbound`；是否真实写入仍取决于分支和参数。

- **L1128 · 方法** `func aimesPayload(changed: Bool, changes: [[String: Any]], duration: Double) -> [String: Any]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`changed: Bool`；`changes: [[String: Any]]`；`duration: Double`
  - 返回：`[String: Any]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1297 · 方法** `private static func testDashboardStartupProgressAndHistory()` — 验证看板、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1303` `MacOSUIRegressionTests.aimesResult`；`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`；`tests/test_macos_ui.swift:2827` `MacOSUIRegressionTests.fail`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`；是否真实写入仍取决于分支和参数。

- **L1303 · 方法** `func aimesResult() -> [String: Any]` — 封装AIMES 数据、结果相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`[String: Any]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1447 · 方法** `private static func testDashboardAimesStatusResolution()` — 验证看板、AIMES 数据、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `dashboardAimesStatusUpdate`；是否真实写入仍取决于分支和参数。

- **L1527 · 方法** `private static func testPendingServerSelectionAndRefreshContract()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardAfterServerWrite`, `closePendingCenterIfEmpty`；是否真实写入仍取决于分支和参数。

- **L1556 · 方法** `private static func testPendingInventorySourceFolderPath()` — 验证库存、来源、文件夹、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L1574 · 方法** `private static func testPendingMaterialMappingIssueRoute()` — 验证材料、映射、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L1606 · 方法** `private static func testPendingInventoryMappingResumeContract()` — 验证库存、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryMapping`, `presentServerWritePreview`；是否真实写入仍取决于分支和参数。

- **L1644 · 方法** `private static func testPendingCenterWorkflowUIContract()` — 验证与 `testPendingCenterWorkflowUIContract` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L1660 · 方法** `private static func testSelectedServerPreviewFailure()` — 验证Server 数据、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L1675 · 方法** `private static func testHardwareSourceSelectionFlow()` — 验证五金、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L1704 · 方法** `private static func testFolderPreviewMappingRecovery()` — 验证文件夹、预览、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryMapping`；是否真实写入仍取决于分支和参数。

- **L1723 · 方法** `private static func testPendingMappingCallbacks()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3132` `AppModel.retryPendingMappingPreview`；`.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift:3092` `AppModel.inventoryMappingWorkspaceDidDismiss`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryMapping`, `closeInventoryMappingWorkspace`, `saveInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L1838 · 方法** `private static func testPendingMappingMergesFolderIssues()` — 验证映射、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `saveInventoryMapping`, `closeInventoryMappingWorkspace`, `saveInventoryIgnoredMapping`；是否真实写入仍取决于分支和参数。

- **L1867 · 方法** `private static func testOrderOutboundFactorySelection()` — 验证订单、出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `orderDashboardOutboundDisplay`, `orderDashboardNeedsOutboundUpdateSelection`, `orderDashboardOutboundActionTitle`；是否真实写入仍取决于分支和参数。

- **L1927 · 方法** `private static func testProductionFeedbackAndDashboardProgress()` — 验证生产、看板、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L2026 · 方法** `private static func testInventoryTravelerNewestFirst()` — 验证库存、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2795` `MacOSUIRegressionTests.traveler`；`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2039 · 方法** `private static func testSharedPageHeaderHeight()` — 验证与 `testSharedPageHeaderHeight` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2063 · 方法** `private static func testAssistantOrderTimelineContract()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderCenter`；是否真实写入仍取决于分支和参数。

- **L2223 · 方法** `private static func testAssistantStageIconAssets()` — 验证与 `testAssistantStageIconAssets` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2238 · 方法** `private static func testGlassDatePickerContract()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2282 · 方法** `private static func testTodoTableHeaderRoundedCorners()` — 验证待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2305 · 方法** `private static func testSettingsDefaultWindowLayoutContract()` — 验证设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2395 · 方法** `private static func testFixedWindowSizeContract()` — 验证与 `testFixedWindowSizeContract` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2416 · 方法** `private static func testInventoryActionLayoutRules()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`；`tests/test_macos_ui.swift:2432` `MacOSUIRegressionTests.preview`

- **L2432 · 方法** `func preview(_ name: String, _ section: String) -> InventoryPreviewRow` — 预览预览相关数据或步骤。
  - 输入：`_ name: String`；`_ section: String`
  - 返回：`InventoryPreviewRow`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2461 · 方法** `private static func testRunningProgressReusesOperationRow()` — 验证进度、操作、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2827` `MacOSUIRegressionTests.fail`；`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2475 · 方法** `private static func testDashboardInventoryProgressText()` — 验证看板、库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2497 · 方法** `private static func testInventoryProgressKeepsStageHistory()` — 验证库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2508 · 方法** `private static func testDashboardSeparatesInventoryAndRefreshTiming()` — 验证看板、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2534 · 方法** `private static func testOrderOperationDurationFormatting()` — 验证订单、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2539 · 方法** `private static func testServerWriteMaterialPreviewOrdering()` — 验证Server 数据、材料、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`, `sortedServerWriteMaterialChanges`；是否真实写入仍取决于分支和参数。

- **L2556 · 方法** `private static func testServerWriteHardwareChangeLayout()` — 验证Server 数据、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteOrderPreview`；是否真实写入仍取决于分支和参数。

- **L2586 · 方法** `private static func testProductionOrderPaths()` — 验证生产、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2597 · 方法** `private static func testStockFailureKeepsManualRetryEnabled()` — 验证与 `testStockFailureKeepsManualRetryEnabled` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2612 · 方法** `private static func testExistingTravelerCanBeUpdatedAfterPreviewFailure()` — 验证Traveler、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderUpdateActionReady`；是否真实写入仍取决于分支和参数。

- **L2627 · 方法** `private static func testDashboardTravelerActionsUseDatabaseFacts()` — 验证看板、Traveler、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L2640 · 方法** `private static func testRelatedPreviewMissingMaterialIssue()` — 验证预览、材料、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2656 · 方法** `private static func testPP0067MissingMaterialShowsPrompt()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2827` `MacOSUIRegressionTests.fail`；`tests/test_macos_ui.swift:2819` `MacOSUIRegressionTests.pumpRunLoop`；`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`；是否真实写入仍取决于分支和参数。

- **L2677 · 方法** `private static func testFullPageHeaderBoundaryAlignment()` — 验证与 `testFullPageHeaderBoundaryAlignment` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2686` `MacOSUIRegressionTests.headerBoundaryY`；`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2686 · 方法** `private static func headerBoundaryY(flexibleContent: Bool) -> CGFloat` — 封装 `headerBoundaryY` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`flexibleContent: Bool`
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:21` `HeaderBoundaryProbeBox`；`tests/test_macos_ui.swift:39` `PageLayoutHarness`；`tests/test_macos_ui.swift:2819` `MacOSUIRegressionTests.pumpRunLoop`；`tests/test_macos_ui.swift:2827` `MacOSUIRegressionTests.fail`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L2705 · 方法** `private static func testOperationLogScrollsAfterAppending()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2807` `MacOSUIRegressionTests.step`；`tests/test_macos_ui.swift:4` `OperationLogHarnessModel`；`tests/test_macos_ui.swift:12` `OperationLogHarnessView`；`tests/test_macos_ui.swift:2819` `MacOSUIRegressionTests.pumpRunLoop`；`tests/test_macos_ui.swift:2811` `MacOSUIRegressionTests.firstScrollView`；`tests/test_macos_ui.swift:2827` `MacOSUIRegressionTests.fail`；`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`；`tests/test_inventory.py:79` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L2756 · 方法** `private static func testOperationLogReader()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`

- **L2766 · 方法** `private static func testOperationLogMaintenance()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:75` `_FakeNodeInput.write`；`tests/test_macos_ui.swift:2823` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`；是否真实写入仍取决于分支和参数。

- **L2795 · 方法** `private static func traveler(_ name: String, folder: String, modifiedAt: String) -> InventoryTraveler` — 封装Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`folder: String`；`modifiedAt: String`
  - 返回：`InventoryTraveler`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2807 · 方法** `private static func step(_ index: Int) -> InventoryStep` — 封装 `step` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ index: Int`
  - 返回：`InventoryStep`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2811 · 方法** `private static func firstScrollView(in view: NSView) -> NSScrollView?` — 封装 `firstScrollView` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`in view: NSView`
  - 返回：`NSScrollView?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2819 · 方法** `private static func pumpRunLoop(for seconds: TimeInterval)` — 封装 `pumpRunLoop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`for seconds: TimeInterval`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run`；是否真实写入仍取决于分支和参数。

- **L2823 · 方法** `private static func require(_ condition: @autoclosure () -> Bool, _ message: String)` — 封装 `require` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ condition: @autoclosure () -> Bool`；`_ message: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:2827` `MacOSUIRegressionTests.fail`

- **L2827 · 方法** `private static func fail(_ message: String) -> Never` — 封装 `fail` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Never`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_operation_log.py`

自动化测试：验证 `operation_log` 模块或业务场景。

- **L10 · 类** `OperationLogTests` — 定义与操作、日志相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L11 · 方法** `OperationLogTests.test_append_log_has_timestamp_and_never_stores_sensitive_values()` — 验证日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L26 · 方法** `OperationLogTests.test_disabled_logger_does_not_create_or_append_file()` — 验证文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_operation_log`；是否真实写入仍取决于分支和参数。

- **L32 · 方法** `OperationLogTests.test_database_trace_records_operation_shape_without_bound_values()` — 验证数据库、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_order_details.py`

自动化测试：验证 `order_details` 模块或业务场景。

- **L12 · 类** `OrderDetailsTests` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L13 · 方法** `OrderDetailsTests.test_hardware_detail_projects_display_name_without_changing_raw_fact()` — 验证五金、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `OrderIndexStore(config.workflow_database).close`, `_replace_product_database`, `connection.execute`, `connection.commit`, `connection.close`, `save_manual_mapping`；是否真实写入仍取决于分支和参数。

- **L52 · 方法** `OrderDetailsTests.test_panel_projection_uses_one_color_image_identity_across_thicknesses()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `OrderIndexStore(config.workflow_database).close`, `_replace_product_database`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

## `tests/test_order_index.py`

自动化测试：验证 `order_index` 模块或业务场景。

- **L80 · 类** `OrderIndexTests` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L82 · 方法** `OrderIndexTests._seed_sku_products(connection)` — 封装 `_seed_sku_products` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.executemany`；是否真实写入仍取决于分支和参数。

- **L123 · 方法** `OrderIndexTests._seed_config_products(config)` — 封装 `_seed_config_products` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`config`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L132 · 方法** `OrderIndexTests._resolved_hinge_inventory(_config, pairs)` — 解析并确定库存相关数据或步骤。
  - 输入：`_config`；`pairs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L144 · 方法** `OrderIndexTests._set_permanent_server_policy(store, order_id, folder)` — 设置Server 数据相关数据或步骤。
  - 输入：`store`；`order_id`；`folder`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.save_server_scan_policy`；是否真实写入仍取决于分支和参数。

- **L153 · 方法** `OrderIndexTests.test_desktop_cs004_and_pp0072_are_offline_memory_preview_fixtures()` — 验证预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L176 · 方法** `OrderIndexTests.test_server_preview_summarizes_changes_and_excludes_shipped_factory_orders()` — 验证Server 数据、预览、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `current.upsert_order`, `current.upsert_factory`, `current.connection.execute`, `current.commit`, `current.close`, `preview.upsert_order`, `preview.upsert_factory`, `preview.connection.executemany`, `preview.connection.execute`；是否真实写入仍取决于分支和参数。

- **L305 · 方法** `OrderIndexTests.test_invalid_preview_folder_reports_path_without_copying_database()` — 验证预览、文件夹、路径、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / 'nesting_result.xml').write_text`；是否真实写入仍取决于分支和参数。

- **L322 · 方法** `OrderIndexTests.test_server_preview_requires_factory_confirmation_before_production_write()` — 验证Server 数据、预览、工厂单、生产相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `stale.upsert_order`, `stale.upsert_factory`, `stale.connection.execute`, `stale.commit`, `stale.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L398 · 方法** `OrderIndexTests.test_selected_server_folder_validation_does_not_touch_other_aimes_orders()` — 验证Server 数据、文件夹、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `store.upsert_order`, `store.connection.execute`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L456 · 方法** `OrderIndexTests.test_server_preview_preserves_recut_material_and_requires_hardware_choice()` — 验证Server 数据、预览、材料、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `current.upsert_order`, `current.upsert_factory`, `current.connection.execute`, `current.commit`, `current.close`；是否真实写入仍取决于分支和参数。

- **L580 · 方法** `OrderIndexTests.test_server_confirmation_writes_materials_and_factory_hardware_after_mapping()` — 验证Server 数据、工厂单、五金、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `current.upsert_order`, `current.upsert_factory`, `current.commit`, `current.close`, `InventoryMappings(config.workflow_database).save_manual`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L619 · 方法** `OrderIndexTests.test_server_confirmation_writes_materials_and_factory_hardware_after_mapping.resolve_items(current_config, pairs)` — 解析并确定与 `resolve_items` 对应的数据或步骤。
  - 输入：`current_config`；`pairs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L753 · 方法** `OrderIndexTests.test_cut_to_size_server_confirmation_can_skip_hardware_for_entire_order()` — 验证Server 数据、五金、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `current.upsert_order`, `current.commit`, `current.close`, `report.mkdir`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L785 · 方法** `OrderIndexTests.test_cut_to_size_server_confirmation_can_skip_hardware_for_entire_order.unresolved(current_config, pairs)` — 封装 `unresolved` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`current_config`；`pairs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L848 · 方法** `OrderIndexTests.test_server_scan_blocks_material_preview_until_source_file_is_fixed()` — 验证Server 数据、材料、预览、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `material_path.write_bytes`；是否真实写入仍取决于分支和参数。

- **L911 · 方法** `OrderIndexTests.test_server_preview_validates_material_before_room_allocation()` — 验证Server 数据、预览、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L941 · 方法** `OrderIndexTests.test_server_material_allocation_splits_one_source_row_between_orders()` — 验证Server 数据、材料、来源、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.upsert_order`, `preview.upsert_factory`, `preview.connection.execute`, `preview.commit`, `preview.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1013 · 方法** `OrderIndexTests.test_server_material_allocation_ignores_stale_sqlite_row_ids()` — 验证Server 数据、材料、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.upsert_order`, `preview.connection.execute`, `preview.commit`, `preview.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1086 · 方法** `OrderIndexTests.test_resolved_mapping_clears_stale_order_validation_error()` — 验证映射、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.connection.execute`, `set`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1116 · 方法** `OrderIndexTests.test_unresolved_mapping_keeps_order_validation_error()` — 验证映射、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1146 · 方法** `OrderIndexTests.test_fully_shipped_temporary_order_is_excluded_from_unfinished_stage()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1180 · 方法** `OrderIndexTests.test_temporary_projection_is_removed_without_overwriting_formal_order()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `formal_folder.mkdir`, `store.upsert_order`, `store.upsert_factory`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1218 · 方法** `OrderIndexTests.test_aimes_stage_durations_exclude_aggregate_and_account_for_backend_overhead()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1234 · 方法** `OrderIndexTests.test_order_annotations_store_single_actual_installation_start_date()` — 验证订单、日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `save_order_annotations`, `reopened.upsert_order`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L1287 · 方法** `OrderIndexTests.test_order_annotations_reject_multiple_actual_installation_dates()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.commit`, `store.save_order_annotations`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1306 · 方法** `OrderIndexTests.test_order_index_collapses_historical_actual_installation_dates()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.connection.execute`, `store.connection.executemany`, `store.connection.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L1341 · 方法** `OrderIndexTests.test_order_annotations_allow_missing_installer_but_reject_duplicate_dates()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.commit`, `store.save_order_annotations`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1383 · 方法** `OrderIndexTests.test_server_folder_rename_requires_unique_identical_report_signature()` — 验证Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1397 · 方法** `OrderIndexTests.test_server_material_replacement_collapses_old_source_path_rows()` — 验证Server 数据、材料、来源、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.commit`, `current_path.parent.mkdir`, `current_path.write_bytes`, `store.connection.execute`, `_replace_server_material_facts`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1434 · 方法** `OrderIndexTests.test_server_material_scope_retires_rows_from_previous_server_root()` — 验证Server 数据、材料、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1476 · 方法** `OrderIndexTests.test_prepared_sync_can_resolve_material_mappings_before_fittings_import_path()` — 验证材料、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `material.parent.mkdir`, `material.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1505 · 方法** `OrderIndexTests.test_server_read_trace_is_grouped_by_folder_and_file_kind()` — 验证Server 数据、文件夹、文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1522 · 方法** `OrderIndexTests.test_server_read_trace_limits_folder_examples()` — 验证Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1534 · 方法** `OrderIndexTests.test_server_scan_covers_owned_and_cut_to_size_roots()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `owned.mkdir`, `cut_to_size.mkdir`, `(owned / 'PP9999 materials.xlsx').write_bytes`, `(cut_to_size / 'CS999 materials.xlsx').write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1570 · 方法** `OrderIndexTests.test_successful_cut_to_size_preview_does_not_claim_optimization_without_aicnc_evidence()` — 验证预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1594 · 方法** `OrderIndexTests.test_cut_to_size_xml_cannot_mark_optimized_when_material_is_absent()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `artifact.parent.mkdir`, `report.write_bytes`, `artifact.write_text`；是否真实写入仍取决于分支和参数。

- **L1624 · 方法** `OrderIndexTests.test_xml_only_sync_never_optimizes_even_with_all_active_factory_artifacts()` — 验证工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `first.parent.mkdir`, `first.write_text`, `second.parent.mkdir`, `second.write_text`, `evidence_connection.execute`, `evidence_connection.close`；是否真实写入仍取决于分支和参数。

- **L1681 · 方法** `OrderIndexTests.test_optimization_marker_scan_uses_known_paths_without_recursive_file_walk()` — 验证文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `kitchen_root.mkdir`, `(kitchen_root / 'Optimize file.xml').write_text`, `(kitchen_root / 'layout file').mkdir`, `nesting.write_text`, `unexpected.parent.mkdir`, `unexpected.write_text`；是否真实写入仍取决于分支和参数。

- **L1705 · 方法** `OrderIndexTests.test_folder_timing_total_equals_final_file_timing_sum()` — 验证文件夹、文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `optimize_root.mkdir`, `(optimize_root / 'Optimize file.xml').write_text`, `(optimize_root / 'layout file').mkdir`, `(optimize_root / 'layout file' / 'nesting_result.xml').write_text`；是否真实写入仍取决于分支和参数。

- **L1722 · 方法** `OrderIndexTests.test_visible_server_scan_keeps_optimization_state_unchanged()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `artifact.parent.mkdir`, `artifact.write_text`, `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1756 · 方法** `OrderIndexTests.test_exact_standard_order_folder_wins_over_mixed_factory_report_folder()` — 验证订单、文件夹、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(mixed_folder / 'Report').mkdir`, `(mixed_folder / 'Report' / '板材清单.xlsx').write_bytes`, `exact_folder.mkdir`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1796 · 方法** `OrderIndexTests.test_cut_to_size_fittings_are_not_persisted_as_hardware()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / 'CS999 materials.xlsx').write_bytes`, `(folder / 'Fittingslist.xlsx').write_bytes`, `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1826 · 方法** `OrderIndexTests.test_incremental_sync_reuses_unchanged_server_report_and_rechecks_changes()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1868 · 方法** `OrderIndexTests.test_server_sync_preserves_hardware_when_report_is_unchanged_or_mapping_fails()` — 验证Server 数据、五金、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `fittings.parent.mkdir`, `store.upsert_order`, `store.upsert_factory`, `store.upsert_source_file`, `store.connection.execute`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1968 · 方法** `OrderIndexTests.test_server_sync_replaces_hardware_by_factory_order_across_source_paths()` — 验证Server 数据、五金、工厂单、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `first.parent.mkdir`, `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `second.parent.mkdir`, `store.connection.execute`, `third.parent.mkdir`；是否真实写入仍取决于分支和参数。

- **L2064 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / f'{name} materials.xlsx').write_bytes`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2065 · 类** `TrackingExecutor` — 定义 `TrackingExecutor` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2066 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.__init__(max_workers)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`max_workers`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2069 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.__enter__()` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2072 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.__exit__(exc_type, exc_value, traceback)` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：`exc_type`；`exc_value`；`traceback`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2075 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.map(function, folders)` — 封装 `map` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`function`；`folders`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2088 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.make_executor(max_workers)` — 创建与 `make_executor` 对应的数据或步骤。
  - 输入：`max_workers`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:2065` `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor`

- **L2116 · 方法** `OrderIndexTests.test_sync_index_reuses_scan_snapshot_and_reports_phase_durations()` — 验证与 `test_sync_index_reuses_scan_snapshot_and_reports_phase_durations` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2153 · 方法** `OrderIndexTests.test_prebaseline_temporary_folder_is_excluded_and_stale_pending_cleared()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_source_file`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L2191 · 方法** `OrderIndexTests.test_named_mixed_folder_is_not_marked_as_temporary()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L2206 · 方法** `OrderIndexTests.test_fully_shipped_mixed_folder_is_watched_then_reopened_by_aimes()` — 验证文件夹、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `store.commit`, `store.close`, `reopened.upsert_aimes_factory`, `reopened.commit`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L2254 · 方法** `OrderIndexTests.test_shipped_server_order_becomes_permanent_after_seven_day_watch()` — 验证Server 数据、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / 'PP9999 materials.xlsx').write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2288 · 方法** `OrderIndexTests.test_initial_date_orders_are_marked_shipped_without_fabricating_documents()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `old_folder.mkdir`, `factory_folder.mkdir`, `store.upsert_aimes_factory`, `store.upsert_order`, `store.connection.execute`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2330 · 方法** `OrderIndexTests.test_mark_temporary_folder_manual_starts_three_day_xml_watch()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `xml_root.mkdir`, `(xml_root / 'Optimize file.xml').write_text`, `(xml_root / 'layout file').mkdir`, `(xml_root / 'layout file' / 'nesting_result.xml').write_text`, `(folder / 'manual materials.xlsx').write_bytes`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2362 · 方法** `OrderIndexTests.test_removed_server_folder_ignore_table_is_cleaned_on_open()` — 验证Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `config.state_dir.mkdir`, `connection.execute`, `connection.commit`, `connection.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2385 · 方法** `OrderIndexTests.test_reportless_mixed_folder_requires_review()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L2400 · 方法** `OrderIndexTests.test_processed_temporary_folder_uses_three_day_xml_watch_then_is_permanent()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `xml.parent.mkdir`, `xml.write_text`, `(folder / 'material.xlsx').write_bytes`, `store.upsert_temporary_order`, `store.save_server_scan_xml_baseline`, `store.commit`, `store.close`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2459 · 方法** `OrderIndexTests.test_failed_temporary_processing_remains_in_pending_server_changes()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / 'material.xlsx').write_bytes`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2492 · 方法** `OrderIndexTests.test_temporary_fittings_report_is_deferred_until_user_approves_processing()` — 验证与 `test_temporary_fittings_report_is_deferred_until_user_approves_processing` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `fittings.parent.mkdir`, `fittings.write_bytes`；是否真实写入仍取决于分支和参数。

- **L2508 · 方法** `OrderIndexTests.test_manual_temporary_outbound_records_server_baseline_case_insensitively()` — 验证出库、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `(folder / 'INSERTHOOD CABINET OLD CNC materials.xlsx').write_bytes`, `(report / 'Fittingslist.xlsx').write_bytes`, `(report / 'pp-板材清单-new.xlsx').write_bytes`, `record_temporary_outbound`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2545 · 方法** `OrderIndexTests.test_shipped_temporary_folder_is_skipped_without_report_rescan()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`, `xml.parent.mkdir`, `xml.write_text`, `record_temporary_outbound`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2582 · 方法** `OrderIndexTests.test_old_temporary_folder_is_filtered_before_report_rescan()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`；是否真实写入仍取决于分支和参数。

- **L2604 · 方法** `OrderIndexTests.test_temporary_processing_generates_material_traveler_and_outbounds()` — 验证材料、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`

- **L2632 · 方法** `OrderIndexTests.test_temporary_processing_can_skip_hardware_in_traveler_and_outbound()` — 验证五金、Traveler、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`

- **L2663 · 方法** `OrderIndexTests.test_temporary_folder_without_aimes_identity_uses_folder_name_everywhere()` — 验证文件夹、AIMES 数据、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`；是否真实写入仍取决于分支和参数。

- **L2705 · 方法** `OrderIndexTests.test_temporary_outbound_is_not_repeated_when_folder_content_is_unchanged()` — 验证出库、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`

- **L2730 · 方法** `OrderIndexTests.test_failed_outbound_reuses_unchanged_generated_traveler_on_retry()` — 验证出库、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`

- **L2764 · 方法** `OrderIndexTests.test_temporary_folder_uses_unique_aimes_review_match_when_available()` — 验证文件夹、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`；`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.replace_aimes_review_rows`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2806 · 方法** `OrderIndexTests.test_factory_order_initial_date_cutoff_uses_embedded_date()` — 验证工厂单、订单、日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2812 · 方法** `OrderIndexTests.test_initial_date_removes_stale_ownership_issue_and_does_not_recreate_it()` — 验证日期、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_factory`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L2853 · 方法** `OrderIndexTests.test_server_change_message_identifies_order_factory_and_data()` — 验证Server 数据、订单、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2859 · 方法** `OrderIndexTests.test_server_change_message_explains_action_and_path()` — 验证Server 数据、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2872 · 方法** `OrderIndexTests.test_invalid_and_test_aimes_rows_are_warnings_only()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2918 · 方法** `OrderIndexTests.test_aimes_factory_name_order_prefix_mismatch_is_a_warning()` — 验证AIMES 数据、工厂单、名称、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2939 · 方法** `OrderIndexTests.test_fittings_factory_order_uses_order_folder_hint()` — 验证工厂单、订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2954 · 方法** `OrderIndexTests.test_unowned_factory_uses_exact_aimes_name_to_derive_order()` — 验证工厂单、AIMES 数据、名称、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2975 · 方法** `OrderIndexTests.test_existing_database_factory_skips_exact_aimes_lookup()` — 验证数据库、工厂单、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3013 · 方法** `OrderIndexTests.test_active_issue_is_persisted_and_resolved()` — 验证待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_active_issue`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3031 · 方法** `OrderIndexTests.test_deleted_aimes_factory_is_audit_only_and_not_in_summaries()` — 验证AIMES 数据、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_aimes_factory`, `store.commit`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3056 · 方法** `OrderIndexTests.test_invalid_aimes_rows_persist_for_reopen_without_entering_business_tables()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3087 · 方法** `OrderIndexTests.test_skipped_aimes_refresh_keeps_persisted_warning_visible_after_reopen()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.replace_aimes_review_rows`, `store.record_run`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3119 · 方法** `OrderIndexTests.test_persisted_aimes_warning_can_be_assigned_when_valid_cache_excludes_it()` — 验证AIMES 数据、缓存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.replace_aimes_review_rows`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3172 · 方法** `OrderIndexTests.test_exactly_verified_aimes_factory_is_persisted_as_aimes_identity()` — 验证AIMES 数据、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L3221 · 方法** `OrderIndexTests.test_business_errors_are_actionable_and_hide_technical_details()` — 验证与 `test_business_errors_are_actionable_and_hide_technical_details` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3236 · 方法** `OrderIndexTests.test_business_aimes_message_uses_explicit_error_type_before_message_words()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3250 · 方法** `OrderIndexTests.test_old_status_is_migrated_and_validation_reason_is_persisted()` — 验证状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.connection.execute`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3284 · 方法** `OrderIndexTests.test_schema_migration_resolves_legacy_warning_from_unique_order_folder()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `source_folder.mkdir`, `store.upsert_factory`, `store.connection.execute`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3313 · 方法** `OrderIndexTests.test_aimes_owner_wins_over_stale_server_owner()` — 验证AIMES 数据、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3336 · 方法** `OrderIndexTests.test_aimes_order_validation_and_test_filter()` — 验证AIMES 数据、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3357 · 方法** `OrderIndexTests.test_historical_pp_server_paths_are_in_dashboard_scope()` — 验证Server 数据、看板、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3366 · 方法** `OrderIndexTests.test_summary_aggregates_factory_status()` — 验证工厂单、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3405 · 方法** `OrderIndexTests.test_standard_outbound_status_reconciles_and_survives_reopen()` — 验证出库、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `reconcile_outbound_statuses`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3446 · 方法** `OrderIndexTests.test_fully_shipped_order_is_completed_even_if_optimization_evidence_is_missing()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3471 · 方法** `OrderIndexTests.test_grouped_outbound_document_reconciles_all_factory_orders_after_reindex()` — 验证出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `connection.execute`, `connection.commit`, `connection.close`, `_load_outbound_records`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L3545 · 方法** `OrderIndexTests.test_order_level_outbound_record_is_not_broadcast_to_split_factories()` — 验证订单、出库、记录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `reconcile_outbound_statuses`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3578 · 方法** `OrderIndexTests.test_partial_factory_upsert_preserves_persisted_business_statuses()` — 验证工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_factory`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3610 · 方法** `OrderIndexTests.test_fully_shipped_aimes_order_is_not_a_server_scan_candidate()` — 验证AIMES 数据、订单、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_aimes_factory`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3636 · 方法** `OrderIndexTests.test_scan_does_not_parse_material_source_as_traveler_during_outbound_reconcile()` — 验证材料、来源、Traveler、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:144` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `workbook.save`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3686 · 方法** `OrderIndexTests.test_fully_shipped_folder_resolves_stale_material_validation_issue()` — 验证文件夹、材料、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:144` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `material_path.write_bytes`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3745 · 方法** `OrderIndexTests.test_completed_production_resolves_post_production_material_issue()` — 验证生产、材料、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `material_path.write_bytes`, `store.upsert_order`, `store.upsert_aimes_factory`, `store.connection.execute`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3834 · 方法** `OrderIndexTests.test_fully_shipped_folder_resolves_stale_hardware_selection_issue()` — 验证文件夹、五金、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:144` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3892 · 方法** `OrderIndexTests.test_fully_shipped_folder_resolves_stale_order_validation_issue()` — 验证文件夹、订单、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:144` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3950 · 方法** `OrderIndexTests.test_automatic_server_snapshot_skips_shipped_order_until_aimes_adds_factory()` — 验证Server 数据、订单、AIMES 数据、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `shipped_folder.mkdir`, `active_folder.mkdir`, `unindexed_folder.mkdir`, `(shipped_folder / 'PP9999 materials.xlsx').write_bytes`, `(active_folder / 'PP8888 materials.xlsx').write_bytes`, `(unindexed_folder / 'PP7777 materials.xlsx').write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4016 · 方法** `OrderIndexTests.test_new_current_aimes_factory_reopens_server_scan_candidate()` — 验证AIMES 数据、工厂单、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `config.source_root.mkdir`, `(config.source_root / 'PP9999').mkdir`；是否真实写入仍取决于分支和参数。

- **L4042 · 方法** `OrderIndexTests.test_skipped_standard_order_does_not_resolve_its_old_issue()` — 验证订单、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:144` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `config.source_root.mkdir`, `folder.mkdir`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4068 · 方法** `OrderIndexTests.test_orders_sort_by_latest_factory_split_time()` — 验证工厂单、时间相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4084 · 方法** `OrderIndexTests.test_summary_includes_confirmed_server_report_factory_assigned_to_normal_order()` — 验证Server 数据、工厂单、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4103 · 方法** `OrderIndexTests.test_aimes_if_needed_runs_once_per_day_after_success()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `config.source_root.mkdir`；是否真实写入仍取决于分支和参数。

- **L4136 · 方法** `OrderIndexTests.test_aimes_only_sync_reports_change_then_skips_after_daily_success()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4165 · 方法** `OrderIndexTests.test_server_scan_is_non_mutating_until_full_processing()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:190` `make_product_catalog`；`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `nesting.parent.mkdir`, `nesting.write_text`, `store.upsert_aimes_factory`, `store.commit`, `store.close`, `report_folder.mkdir`, `store.connection.execute`, `report.write_bytes`, `report.unlink`；是否真实写入仍取决于分支和参数。

- **L4284 · 方法** `OrderIndexTests.test_confirm_without_materials_does_not_establish_xml_scan_baseline()` — 验证与 `test_confirm_without_materials_does_not_establish_xml_scan_baseline` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `xml.parent.mkdir`, `xml.write_text`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4330 · 方法** `OrderIndexTests.test_preview_scopes_optimization_artifacts_to_selected_order()` — 验证预览、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `other_folder.mkdir`, `preview.upsert_order`, `preview.upsert_factory`, `preview.connection.execute`, `preview.commit`, `preview.close`；是否真实写入仍取决于分支和参数。

- **L4368 · 方法** `OrderIndexTests.test_business_confirmation_persists_optimization_evidence_for_list_index()` — 验证与 `test_business_confirmation_persists_optimization_evidence_for_list_index` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:123` `OrderIndexTests._seed_config_products`；`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `preview.upsert_order`, `preview.upsert_factory`, `preview.connection.execute`, `(folder / 'material.xlsx').write_bytes`, `preview.upsert_source_file`, `preview.commit`, `preview.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4424 · 方法** `OrderIndexTests.test_memory_confirmation_upserts_selected_optimization_evidence_idempotently()` — 验证与 `test_memory_confirmation_upserts_selected_optimization_evidence_idempotently` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:82` `OrderIndexTests._seed_sku_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `current.upsert_order`, `current.upsert_factory`, `current.connection.execute`, `current.commit`, `current.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4505 · 方法** `OrderIndexTests.test_memory_evidence_confirmation_rolls_back_on_baseline_failure()` — 验证与 `test_memory_evidence_confirmation_rolls_back_on_baseline_failure` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `shared.execute`, `bootstrap.close`, `shared.close`；是否真实写入仍取决于分支和参数。

- **L4536 · 方法** `OrderIndexTests.test_server_scan_baseline_covers_both_server_roots()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:190` `make_product_catalog`；`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `nesting.parent.mkdir`, `nesting.write_text`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4581 · 方法** `OrderIndexTests.test_report_edits_are_ignored_by_xml_only_server_scan()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `store.upsert_source_file`, `store.commit`, `store.close`, `materials.write_bytes`, `_record_generated_material_baseline`；是否真实写入仍取决于分支和参数。

- **L4626 · 方法** `OrderIndexTests.test_selected_server_folder_reuses_index_processing_for_one_folder()` — 验证Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_order`, `store.commit`, `store.close`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L4654 · 方法** `OrderIndexTests.test_selected_non_order_folder_is_rejected_without_processing_children()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `child_order.mkdir`, `(child_order / 'material.xlsx').write_bytes`；是否真实写入仍取决于分支和参数。

- **L4669 · 方法** `OrderIndexTests.test_selected_non_order_folder_with_recognized_report_is_temporary_order()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `selected.mkdir`, `(selected / 'material.xlsx').write_bytes`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4691 · 方法** `OrderIndexTests.test_scan_reports_unprocessed_non_order_folder_as_manual_only()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `selected.mkdir`, `(selected / 'material.xlsx').write_bytes`；是否真实写入仍取决于分支和参数。

## `tests/test_order_service.py`

自动化测试：验证 `order_service` 模块或业务场景。

- **L12 · 类** `OrderServiceTests` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L13 · 方法** `OrderServiceTests.test_confirmation_response_cannot_replace_list_index_cache()` — 验证缓存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_service.py:22` `OrderServiceTests.test_confirmation_response_cannot_replace_list_index_cache.Logger`

- **L22 · 类** `Logger` — 定义 `Logger` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L23 · 方法** `OrderServiceTests.test_confirmation_response_cannot_replace_list_index_cache.Logger.event(*args, **kwargs)` — 封装 `event` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`*args`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L26 · 方法** `OrderServiceTests.test_confirmation_response_cannot_replace_list_index_cache.fake_main(arguments, **kwargs)` — 封装 `fake_main` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`arguments`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_order_workflow.py`

自动化测试：验证 `order_workflow` 模块或业务场景。

- **L46 · 函数** `seed_products(connection, rows)` — 封装 `seed_products` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`；`rows`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.executemany`, `code.replace`；是否真实写入仍取决于分支和参数。

- **L80 · 函数** `make_materials(path: Path, order_id: str = 'PP9999', fractional: bool = False, edge: float = 12.5)` — 创建与 `make_materials` 对应的数据或步骤。
  - 输入：`path: Path`；`order_id: str = 'PP9999'`；`fractional: bool = False`；`edge: float = 12.5`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L104 · 函数** `make_board(path: Path, factory: str, name: str)` — 创建与 `make_board` 对应的数据或步骤。
  - 输入：`path: Path`；`factory: str`；`name: str`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L113 · 函数** `make_board_material_report(path: Path, factory: str = 'F100', name: str = 'PP9999-KITCHEN', plywood_qty: int = 2, panel_qty: int = 3, edge_qty: float = 12.5)` — 创建材料相关数据或步骤。
  - 输入：`path: Path`；`factory: str = 'F100'`；`name: str = 'PP9999-KITCHEN'`；`plywood_qty: int = 2`；`panel_qty: int = 3`；`edge_qty: float = 12.5`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `wb.save`；是否真实写入仍取决于分支和参数。

- **L138 · 函数** `make_fittings(path: Path, groups: list[tuple[str, float]])` — 创建与 `make_fittings` 对应的数据或步骤。
  - 输入：`path: Path`；`groups: list[tuple[str, float]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L159 · 函数** `make_rail_fittings(path: Path, left_quantity: float, right_quantity: float | None, left_name: str = 'Left Rail', right_name: str = 'Right Rail')` — 创建与 `make_rail_fittings` 对应的数据或步骤。
  - 输入：`path: Path`；`left_quantity: float`；`right_quantity: float | None`；`left_name: str = 'Left Rail'`；`right_name: str = 'Right Rail'`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L185 · 函数** `make_template(path: Path)` — 创建与 `make_template` 对应的数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L190 · 函数** `make_product_catalog(path: Path)` — 创建商品目录相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L210 · 函数** `picking_layout_snapshot(sheet)` — 封装 `picking_layout_snapshot` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`sheet`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L237 · 类** `OrderWorkflowTests` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L238 · 方法** `OrderWorkflowTests.test_memory_server_confirmation_command_reads_json_from_stdin()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L260 · 方法** `OrderWorkflowTests.test_database_order_traveler_uses_sqlite_facts_without_source_material()` — 验证数据库、订单、Traveler、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:185` `make_template`；`tests/test_order_workflow.py:46` `seed_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L334 · 方法** `OrderWorkflowTests.test_database_order_traveler_keeps_fifth_and_later_hardware_visible()` — 验证数据库、订单、Traveler、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:185` `make_template`；`tests/test_order_workflow.py:46` `seed_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.executemany`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L408 · 方法** `OrderWorkflowTests.test_database_order_traveler_writes_manual_hardware_to_accessory_section()` — 验证数据库、订单、Traveler、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:185` `make_template`；`tests/test_order_workflow.py:46` `seed_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.executemany`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L502 · 方法** `OrderWorkflowTests.test_legacy_traveler_gets_usage_list_and_material_from_picking_list()` — 验证Traveler、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:185` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `local_order.mkdir`, `workbook.save`, `target.mkdir`；是否真实写入仍取决于分支和参数。

- **L554 · 方法** `OrderWorkflowTests.test_missing_material_can_be_generated_from_report_summary()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`

- **L587 · 方法** `OrderWorkflowTests.test_generated_material_color_table_aggregates_repeated_report_colors()` — 验证材料、颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`

- **L621 · 方法** `OrderWorkflowTests.test_complex_report_generation_requests_manual_material()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:113` `make_board_material_report`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L635 · 方法** `OrderWorkflowTests.test_local_test_source_is_repeatable_and_matches_server_layout()` — 验证来源、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sentinel.write_text`；是否真实写入仍取决于分支和参数。

- **L663 · 方法** `OrderWorkflowTests.test_usage_list_expands_and_rewrites_summary_formulas()` — 验证与 `test_usage_list_expands_and_rewrites_summary_formulas` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:185` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L708 · 方法** `OrderWorkflowTests.test_usage_list_normalizes_alias_color_before_color_table_formulas()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:185` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L745 · 方法** `OrderWorkflowTests.test_order_folders_are_sorted_by_modified_time_descending()` — 验证订单、时间相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L766 · 方法** `OrderWorkflowTests.test_cut_to_size_requires_materials_workbook()` — 验证与 `test_cut_to_size_requires_materials_workbook` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `order.mkdir`；是否真实写入仍取决于分支和参数。

- **L777 · 方法** `OrderWorkflowTests.test_cut_to_size_generates_materials_only_traveler()` — 验证Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_workflow.py:185` `make_template`；`tests/test_order_workflow.py:210` `picking_layout_snapshot`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `order.mkdir`, `untouched.save`, `set`；是否真实写入仍取决于分支和参数。

- **L849 · 方法** `OrderWorkflowTests.test_source_component_code_is_not_written_as_sku()` — 验证来源、编码相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`；`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_workflow.py:185` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`；是否真实写入仍取决于分支和参数。

- **L877 · 方法** `OrderWorkflowTests.test_opt_out_hardware_omits_report_fittings_from_traveler()` — 验证五金、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`；`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_workflow.py:185` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`；是否真实写入仍取决于分支和参数。

- **L907 · 方法** `OrderWorkflowTests.test_invalid_empty_dimension_returns_one_business_error()` — 验证与 `test_invalid_empty_dimension_returns_one_business_error` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Workbook().save`, `payload.replace`；是否真实写入仍取决于分支和参数。

- **L923 · 方法** `OrderWorkflowTests.test_equal_rail_pair_is_collapsed_but_mismatch_stops_read()` — 验证与 `test_equal_rail_pair_is_collapsed_but_mismatch_stops_read` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:159` `make_rail_fittings`

- **L954 · 方法** `OrderWorkflowTests.test_equal_rail_pair_preview_consumes_canonical_quantity()` — 验证预览、数量相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`；`tests/test_order_workflow.py:159` `make_rail_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`；是否真实写入仍取决于分支和参数。

- **L975 · 方法** `OrderWorkflowTests.test_single_color_materials_and_integer_validation()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`

- **L988 · 方法** `OrderWorkflowTests.test_multicolor_materials_accepts_color_table_marker_in_total_row()` — 验证颜色、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1022 · 方法** `OrderWorkflowTests.test_single_color_materials_without_color_table_is_a_schema_error()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1041 · 方法** `OrderWorkflowTests.test_single_color_materials_keep_edge_when_panel_is_zero()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1059 · 方法** `OrderWorkflowTests.test_repairs_empty_single_color_table_from_detail_rows_without_changing_details()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1104 · 方法** `OrderWorkflowTests.test_repairs_missing_color_table_colors_and_rebuilds_all_summary_formulas()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1144 · 方法** `OrderWorkflowTests.test_preview_rejects_incomplete_color_table_without_rewriting_source()` — 验证预览、颜色、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `order.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1166 · 方法** `OrderWorkflowTests.test_repair_aggregates_repeated_detail_color_rows()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1193 · 方法** `OrderWorkflowTests.test_existing_complete_color_table_mismatch_requires_manual_handling()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1211 · 方法** `OrderWorkflowTests.test_eight_color_table_is_read_without_seven_color_limit_error()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `set`；是否真实写入仍取决于分支和参数。

- **L1244 · 方法** `OrderWorkflowTests.test_integer_display_format_uses_the_total_qty_values_excel_shows()` — 验证与 `test_integer_display_format_uses_the_total_qty_values_excel_shows` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L1273 · 方法** `OrderWorkflowTests.test_material_detail_quantity_requires_color()` — 验证材料、数量、颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1287 · 方法** `OrderWorkflowTests.test_total_qty_and_color_table_must_match_before_material_write()` — 验证颜色、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1311 · 方法** `OrderWorkflowTests.test_formula_without_cached_values_uses_display_values_for_totals_and_color_table()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L1339 · 方法** `OrderWorkflowTests.test_integer_display_format_is_also_used_for_room_rows()` — 验证与 `test_integer_display_format_is_also_used_for_room_rows` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L1355 · 方法** `OrderWorkflowTests.test_room_section_factory_name_extracts_exact_order_and_rejects_ambiguous_rows()` — 验证工厂单、名称、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1378 · 方法** `OrderWorkflowTests.test_related_update_reports_the_specific_order_error()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_related_orders`；是否真实写入仍取决于分支和参数。

- **L1394 · 方法** `OrderWorkflowTests.test_related_update_response_keeps_all_orders_and_factories()` — 验证与 `test_related_update_response_keeps_all_orders_and_factories` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_related_orders`；是否真实写入仍取决于分支和参数。

- **L1422 · 方法** `OrderWorkflowTests.test_duplicate_fittings_require_choice_regardless_of_time()` — 验证时间相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `older.parent.mkdir`, `newer.parent.mkdir`；是否真实写入仍取决于分支和参数。

- **L1448 · 方法** `OrderWorkflowTests.test_empty_malformed_fittings_is_skipped_and_traveler_can_generate()` — 验证Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`；`tests/test_order_workflow.py:185` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `workbook.save`, `empty.save`；是否真实写入仍取决于分支和参数。

- **L1504 · 方法** `OrderWorkflowTests.test_global_ignore_and_generate_one_order_workbook()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`；`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_workflow.py:185` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report_a.mkdir`, `report_b.mkdir`, `set_ignored`, `set_ignored_mapping`, `wb.save`, `materials_wb.save`, `update_order_traveler`；是否真实写入仍取决于分支和参数。

- **L1606 · 方法** `OrderWorkflowTests.test_ignored_hardware_is_not_persisted_when_order_is_rescanned()` — 验证五金、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`；`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_workflow.py:190` `make_product_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `connection.execute`, `connection.close`, `set_ignored`；是否真实写入仍取决于分支和参数。

- **L1641 · 方法** `OrderWorkflowTests.test_add_manual_hardware_writes_database_and_aggregates_same_sku()` — 验证五金、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`；`tests/test_order_workflow.py:138` `make_fittings`；`tests/test_order_workflow.py:190` `make_product_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `index.connection.execute`, `index.connection.commit`, `index.close`, `traveler.parent.mkdir`, `traveler.write_text`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1742 · 方法** `OrderWorkflowTests.test_manual_hardware_accepts_factory_number_without_traveler()` — 验证五金、工厂单、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:190` `make_product_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `index.close`, `connection.close`；是否真实写入仍取决于分支和参数。

## `tests/test_production.py`

自动化测试：验证 `production` 模块或业务场景。

- **L19 · 类** `ProductionTransactionTests` — 定义与生产相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 方法** `ProductionTransactionTests._seed_products(connection)` — 封装 `_seed_products` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.executemany`；是否真实写入仍取决于分支和参数。

- **L36 · 方法** `ProductionTransactionTests.test_production_preview_aggregates_duplicate_order_material_rows()` — 验证生产、预览、订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_production.py:21` `ProductionTransactionTests._seed_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.executemany`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L74 · 方法** `ProductionTransactionTests.test_production_preview_deducts_legacy_inventory_materials()` — 验证生产、预览、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_production.py:21` `ProductionTransactionTests._seed_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.executemany`, `store.commit`, `store.close`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L187 · 方法** `ProductionTransactionTests.test_prepare_production_is_read_only_until_inventory_succeeds()` — 验证生产、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_production.py:21` `ProductionTransactionTests._seed_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `store.commit`, `store.close`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L241 · 方法** `ProductionTransactionTests.test_completed_production_can_share_the_local_commit()` — 验证生产相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_production.py:21` `ProductionTransactionTests._seed_products`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record_completed_production`, `connection.commit`, `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

## `tests/test_report_selection.py`

自动化测试：验证 `report_selection` 模块或业务场景。

- **L19 · 类** `ReportSelectionTests` — 定义 `ReportSelectionTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L20 · 方法** `ReportSelectionTests.test_changed_choice_requires_reselection_and_identical_content_deduplicates()` — 验证与 `test_changed_choice_requires_reselection_and_identical_content_deduplicates` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`；是否真实写入仍取决于分支和参数。

- **L39 · 方法** `ReportSelectionTests.test_choices_apply_per_factory_in_multiblock_files()` — 验证工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`

- **L55 · 方法** `ReportSelectionTests.test_database_ownership_precedes_display_prefix_and_no_network()` — 验证数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L71 · 方法** `ReportSelectionTests.test_report_cache_is_request_local_copied_and_file_change_sensitive()` — 验证缓存、文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`

- **L86 · 方法** `ReportSelectionTests.test_process_progress_delivered_before_exit_and_timeout_kills_child()` — 验证进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_with_progress`, `os.environ.copy`；是否真实写入仍取决于分支和参数。

- **L102 · 方法** `ReportSelectionTests.test_aimes_adapter_forwards_live_events_to_app_stderr()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_run_aimes_lookup`；是否真实写入仍取决于分支和参数。

- **L107 · 方法** `ReportSelectionTests.test_aimes_adapter_forwards_live_events_to_app_stderr.process(*args, **kwargs)` — 处理与 `process` 对应的数据或步骤。
  - 输入：`*args`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L116 · 方法** `ReportSelectionTests.test_zero_quantity_report_is_not_silently_discarded()` — 验证数量相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`

- **L125 · 方法** `ReportSelectionTests.test_confirmed_source_is_fixed_until_content_changes_and_keep_survives_restart()` — 验证来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:190` `make_product_catalog`；`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

## `tests/test_runtime_store.py`

自动化测试：验证 `runtime_store` 模块或业务场景。

- **L13 · 类** `RuntimeStoreTests` — 定义 `RuntimeStoreTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L14 · 方法** `RuntimeStoreTests.test_runtime_database_uses_a_private_file()` — 验证数据库、文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L19 · 方法** `RuntimeStoreTests.test_unknown_database_version_is_not_deleted()` — 验证数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L30 · 方法** `RuntimeStoreTests.test_assistant_usage_does_not_touch_workflow_database()` — 验证数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L64 · 方法** `RuntimeStoreTests.test_agent_usage_has_week_month_and_total_summaries()` — 验证与 `test_agent_usage_has_week_month_and_total_summaries` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.record_agent_usage`；是否真实写入仍取决于分支和参数。

- **L73 · 方法** `RuntimeStoreTests.test_agent_route_is_learned_as_an_exact_normalized_phrase()` — 验证与 `test_agent_route_is_learned_as_an_exact_normalized_phrase` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L83 · 方法** `RuntimeStoreTests.test_learned_command_preserves_typed_arguments()` — 验证与 `test_learned_command_preserves_typed_arguments` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_security.py`

自动化测试：验证 `security` 模块或业务场景。

- **L14 · 类** `CredentialSafetyTests` — 定义 `CredentialSafetyTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 方法** `CredentialSafetyTests.test_repository_contains_no_likely_credentials()` — 验证与 `test_repository_contains_no_likely_credentials` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L45 · 方法** `CredentialSafetyTests.test_sensitive_local_files_are_gitignored()` — 验证与 `test_sensitive_local_files_are_gitignored` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_server_rail_units.py`

自动化测试：验证 `server_rail_units` 模块或业务场景。

- **L20 · 类** `ServerRailUnitsTests` — 定义与Server 数据相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 方法** `ServerRailUnitsTests.setUp()` — 设置与 `setUp` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:80` `make_materials`；`tests/test_order_workflow.py:104` `make_board`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `wb.save`, `mappings.save_manual`, `mappings.save_ignored`, `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L56 · 方法** `ServerRailUnitsTests.write_report(quantities)` — 写入与 `write_report` 对应的数据或步骤。
  - 输入：`quantities`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:138` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L67 · 方法** `ServerRailUnitsTests.rows()` — 封装 `rows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L71 · 方法** `ServerRailUnitsTests.test_preview_and_repeated_confirmation_convert_raw_counts_only_once()` — 验证预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_server_rail_units.py:56` `ServerRailUnitsTests.write_report`；`tests/test_server_rail_units.py:67` `ServerRailUnitsTests.rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.write_report`；是否真实写入仍取决于分支和参数。

- **L83 · 方法** `ServerRailUnitsTests.test_odd_report_blocks_preview_and_preserves_existing_facts()` — 验证预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_server_rail_units.py:56` `ServerRailUnitsTests.write_report`；`tests/test_server_rail_units.py:67` `ServerRailUnitsTests.rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.write_report`；是否真实写入仍取决于分支和参数。

- **L98 · 方法** `ServerRailUnitsTests.test_confirmation_revalidates_raw_counts_before_any_write()` — 验证与 `test_confirmation_revalidates_raw_counts_before_any_write` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_server_rail_units.py:56` `ServerRailUnitsTests.write_report`；`tests/test_server_rail_units.py:67` `ServerRailUnitsTests.rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.write_report`；是否真实写入仍取决于分支和参数。

- **L107 · 方法** `ServerRailUnitsTests.test_direct_sync_converts_and_reports_odd_quantity_without_replacing()` — 验证数量相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_server_rail_units.py:56` `ServerRailUnitsTests.write_report`；`tests/test_server_rail_units.py:67` `ServerRailUnitsTests.rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.write_report`, `store.close`；是否真实写入仍取决于分支和参数。

- **L120 · 方法** `ServerRailUnitsTests.test_h_and_l_rail_source_pairs_keep_canonical_quantity()` — 验证来源、数量相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_server_rail_units.py:56` `ServerRailUnitsTests.write_report`；`tests/test_server_rail_units.py:67` `ServerRailUnitsTests.rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.write_report`, `wb.save`；是否真实写入仍取决于分支和参数。

- **L136 · 方法** `ServerRailUnitsTests.test_legacy_order_preview_persistence_converts_once_and_rolls_back_on_odd()` — 验证订单、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_server_rail_units.py:56` `ServerRailUnitsTests.write_report`；`tests/test_server_rail_units.py:67` `ServerRailUnitsTests.rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.write_report`；是否真实写入仍取决于分支和参数。

- **L149 · 方法** `ServerRailUnitsTests.test_existing_pair_rules_and_other_skus_are_not_halved()` — 验证与 `test_existing_pair_rules_and_other_skus_are_not_halved` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_workflow_database.py`

自动化测试：验证 `workflow_database` 模块或业务场景。

- **L14 · 类** `WorkflowDatabaseTests` — 定义与数据库相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 方法** `WorkflowDatabaseTests.test_grouped_outbound_document_migrates_to_factory_links()` — 验证出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.commit`, `connection.close`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L68 · 方法** `WorkflowDatabaseTests.test_material_table_migrates_to_order_scope_and_removes_allocations()` — 验证材料、订单、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.commit`, `connection.close`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L128 · 方法** `WorkflowDatabaseTests.test_legacy_order_database_migrates_without_reading_inventory_database()` — 验证订单、数据库、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `state.mkdir`, `connection.execute`, `connection.commit`, `connection.close`, `legacy_inventory.parent.mkdir`；是否真实写入仍取决于分支和参数。

- **L159 · 方法** `WorkflowDatabaseTests.test_one_factory_order_gets_one_batch_and_conflict_raises_open_issue()` — 验证工厂单、订单、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_aimes_factory`, `store.update_source_file_identity`, `store.record_batch_evidence`, `store.commit`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L174 · 方法** `WorkflowDatabaseTests.test_backup_status_requires_user_action_without_successful_record()` — 验证备份、状态、记录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L181 · 方法** `WorkflowDatabaseTests.test_retention_keeps_recent_daily_and_sunday_weekly_backups()` — 验证与 `test_retention_keeps_recent_daily_and_sunday_weekly_backups` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L202 · 方法** `WorkflowDatabaseTests.test_perform_backup_uses_local_database_backup_directory()` — 验证备份、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sqlite3.connect(destination).execute`；是否真实写入仍取决于分支和参数。

## `tools/aimes_lookup.mjs`

通过浏览器自动化查询 AIMES 工厂单名称和近期订单。

- **L10 · 函数** `safePageURL()` — 封装 `safePageURL` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L19 · 函数** `log(message, details = {})` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`message`；`details = {}`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L25 · 函数** `recordStage(stage, label, startedAt)` — 记录记录相关数据或步骤。
  - 输入：`stage`；`label`；`startedAt`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/aimes_lookup.mjs:19` `log`

- **L33 · 函数** `retryPageStep(label, action)` — 封装 `retryPageStep` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`label`；`action`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/aimes_lookup.mjs:19` `log`

## `tools/aimes_table.mjs`

Node.js ES Module 辅助脚本。

- **L63 · 函数** `notReadyError(snapshot, timeoutMs)` — 封装 `notReadyError` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`snapshot`；`timeoutMs`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L69 · 函数** `schemaError(headers, missing)` — 封装 `schemaError` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`headers`；`missing`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L77 · 函数** `readAimesTable(page, { timeoutMs = 15000, requireMetadata = true } = {})` — 读取AIMES 数据相关数据或步骤。
  - 输入：`page`；`{ timeoutMs = 15000`；`requireMetadata = true } = {}`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tools/generate_code_reference.py`

静态扫描一方源码，生成中文文件地图和符号索引。

- **L269 · 类** `Symbol` — 定义 `Symbol` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L283 · 函数** `tracked_files() -> list[str]` — 封装 `tracked_files` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `subprocess.run`；是否真实写入仍取决于分支和参数。

- **L291 · 函数** `split_words(name: str) -> list[str]` — 封装 `split_words` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L298 · 函数** `translated_subject(name: str) -> str` — 封装 `translated_subject` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:291` `split_words`

- **L309 · 函数** `symbol_purpose(symbol: Symbol) -> str` — 封装 `symbol_purpose` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`symbol: Symbol`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:298` `translated_subject`

- **L336 · 函数** `file_purpose(path: str) -> str` — 封装文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L387 · 函数** `annotation_text(node: ast.expr | None) -> str` — 封装 `annotation_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.expr | None`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L397 · 函数** `python_parameter_text(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]` — 封装 `python_parameter_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.FunctionDef | ast.AsyncFunctionDef`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:387` `annotation_text`

- **L426 · 类** `DirectCallVisitor` — 定义 `DirectCallVisitor` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L429 · 方法** `DirectCallVisitor.__init__(root: ast.AST) -> None` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`root: ast.AST`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L433 · 方法** `DirectCallVisitor.visit_FunctionDef(node: ast.FunctionDef) -> None` — 封装 `visit_FunctionDef` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.FunctionDef`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L439 · 方法** `DirectCallVisitor.visit_Lambda(node: ast.Lambda) -> None` — 封装 `visit_Lambda` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.Lambda`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L442 · 方法** `DirectCallVisitor.visit_ClassDef(node: ast.ClassDef) -> None` — 封装 `visit_ClassDef` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.ClassDef`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L446 · 方法** `DirectCallVisitor.visit_Call(node: ast.Call) -> None` — 封装 `visit_Call` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.Call`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L456 · 函数** `python_symbols(path: Path) -> list[Symbol]` — 封装 `python_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:463` `python_symbols.walk`

- **L463 · 方法** `python_symbols.walk(body: Iterable[ast.stmt], parents: list[str]) -> None` — 封装 `walk` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`body: Iterable[ast.stmt]`；`parents: list[str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:463` `python_symbols.walk`；`tools/generate_code_reference.py:397` `python_parameter_text`；`tools/generate_code_reference.py:387` `annotation_text`；`tools/generate_code_reference.py:426` `DirectCallVisitor`

- **L523 · 函数** `line_number(source: str, offset: int) -> int` — 封装 `line_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source: str`；`offset: int`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L528 · 函数** `declaration_end(source: str, start: int) -> int` — 封装 `declaration_end` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source: str`；`start: int`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L564 · 函数** `matching_brace(source: str, opening: int) -> int` — 匹配与 `matching_brace` 对应的数据或步骤。
  - 输入：`source: str`；`opening: int`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L622 · 函数** `swift_parameter_list(signature: str) -> list[str]` — 封装 `swift_parameter_list` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`signature: str`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L646 · 函数** `swift_return_type(signature: str, raw_kind: str) -> str` — 封装 `swift_return_type` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`signature: str`；`raw_kind: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L671 · 函数** `swift_symbols(path: Path) -> list[Symbol]` — 封装 `swift_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:523` `line_number`；`tools/generate_code_reference.py:564` `matching_brace`；`tools/generate_code_reference.py:528` `declaration_end`；`tools/generate_code_reference.py:646` `swift_return_type`；`tools/generate_code_reference.py:693` `swift_symbols.container_name`；`tools/generate_code_reference.py:622` `swift_parameter_list`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L693 · 方法** `swift_symbols.container_name(offset: int) -> str | None` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`offset: int`
  - 返回：`str | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L750 · 函数** `js_symbols(path: Path) -> list[Symbol]` — 封装 `js_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:564` `matching_brace`；`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:523` `line_number`

- **L772 · 函数** `shell_symbols(path: Path) -> list[Symbol]` — 封装 `shell_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:564` `matching_brace`；`tools/generate_code_reference.py:523` `line_number`

- **L794 · 函数** `project_source_paths(files: list[str]) -> list[Path]` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`files: list[str]`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L805 · 函数** `collect_symbols(files: list[str]) -> list[Symbol]` — 封装 `collect_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`files: list[str]`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:794` `project_source_paths`；`tools/generate_code_reference.py:456` `python_symbols`；`tools/generate_code_reference.py:671` `swift_symbols`；`tools/generate_code_reference.py:750` `js_symbols`；`tools/generate_code_reference.py:772` `shell_symbols`；`tools/generate_code_reference.py:269` `Symbol`

- **L824 · 函数** `resolve_calls(symbols: list[Symbol]) -> None` — 解析并确定与 `resolve_calls` 对应的数据或步骤。
  - 输入：`symbols: list[Symbol]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:291` `split_words`

- **L870 · 函数** `markdown_escape(value: str) -> str` — 标记与 `markdown_escape` 对应的数据或步骤。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `value.replace('`', "'").replace`, `value.replace`；是否真实写入仍取决于分支和参数。

- **L875 · 函数** `render_symbol(symbol: Symbol) -> list[str]` — 封装 `render_symbol` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`symbol: Symbol`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:870` `markdown_escape`；`tools/generate_code_reference.py:309` `symbol_purpose`

- **L892 · 函数** `write_text(path: Path, lines: list[str]) -> None` — 写入与 `write_text` 对应的数据或步骤。
  - 输入：`path: Path`；`lines: list[str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:892` `write_text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `path.write_text`；是否真实写入仍取决于分支和参数。

- **L898 · 函数** `render_file_map(files: list[str], symbols: list[Symbol], git_tracked_count: int) -> None` — 封装文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`files: list[str]`；`symbols: list[Symbol]`；`git_tracked_count: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:336` `file_purpose`；`tools/generate_code_reference.py:892` `write_text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_text`；是否真实写入仍取决于分支和参数。

- **L951 · 函数** `reference_header(title: str, scope: str, count: int) -> list[str]` — 封装 `reference_header` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: str`；`scope: str`；`count: int`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L969 · 函数** `render_reference(path: Path, title: str, scope: str, symbols: list[Symbol]) -> None` — 封装 `render_reference` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`title: str`；`scope: str`；`symbols: list[Symbol]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:951` `reference_header`；`tools/generate_code_reference.py:336` `file_purpose`；`tools/generate_code_reference.py:875` `render_symbol`；`tools/generate_code_reference.py:892` `write_text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_text`；是否真实写入仍取决于分支和参数。

- **L983 · 函数** `main() -> int` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`int`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:283` `tracked_files`；`tools/generate_code_reference.py:805` `collect_symbols`；`tools/generate_code_reference.py:824` `resolve_calls`；`tools/generate_code_reference.py:898` `render_file_map`；`tools/generate_code_reference.py:969` `render_reference`

## `tools/jdy_inventory.mjs`

通过浏览器自动化读取库存、填单并执行金蝶云出库。

- **L13 · 函数** `safePageURL()` — 封装 `safePageURL` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L22 · 函数** `log(message, details = {})` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`message`；`details = {}`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L29 · 函数** `timed(label, operation)` — 封装 `timed` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`label`；`operation`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:22` `log`

- **L49 · 函数** `timedWait(page, milliseconds, label)` — 封装 `timedWait` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`milliseconds`；`label`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L52 · 函数** `exact(page, text)` — 封装 `exact` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L60 · 函数** `clickVisibleText(page, text)` — 封装 `clickVisibleText` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L71 · 函数** `clickVisibleTextAcrossFrames(page, text)` — 封装 `clickVisibleTextAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:60` `clickVisibleText`

- **L77 · 函数** `visibleTextLocatorsAcrossFrames(page, text)` — 封装 `visibleTextLocatorsAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L88 · 函数** `visibleLeftNavigationLocators(page, text)` — 封装 `visibleLeftNavigationLocators` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L97 · 函数** `waitForVisibleLeftNavigationItem(page, text, timeoutMs = UI_STEP_TIMEOUT)` — 封装项目相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`；`timeoutMs = UI_STEP_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:88` `visibleLeftNavigationLocators`

- **L112 · 函数** `waitForVisibleTextAcrossFrames(page, text, timeoutMs = UI_STEP_TIMEOUT)` — 封装 `waitForVisibleTextAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`；`timeoutMs = UI_STEP_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:77` `visibleTextLocatorsAcrossFrames`

- **L121 · 函数** `visiblePatternLocatorsAcrossFrames(page, pattern)` — 封装 `visiblePatternLocatorsAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`pattern`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L132 · 函数** `waitForVisiblePatternToDisappear(page, pattern, timeoutMs = UI_STEP_TIMEOUT)` — 封装 `waitForVisiblePatternToDisappear` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`pattern`；`timeoutMs = UI_STEP_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:121` `visiblePatternLocatorsAcrossFrames`

- **L140 · 函数** `moveAndClick(label, locator)` — 封装 `moveAndClick` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`label`；`locator`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:29` `timed`

- **L144 · 函数** `waitForVisibleFrame(page, predicate, timeoutMs = 15000)` — 封装 `waitForVisibleFrame` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`predicate`；`timeoutMs = 15000`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L156 · 函数** `hasVisibleLocator(frame, selector)` — 封装 `hasVisibleLocator` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`frame`；`selector`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L190 · 函数** `outboundSaveControlDiagnostics(currentPage, preferredFrame)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`currentPage`；`preferredFrame`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `visibleOutboundSaveControls`, `isOutboundSaveControlDisabled`；是否真实写入仍取决于分支和参数。

- **L214 · 函数** `waitForOutboundSaveControl(currentPage, preferredFrame, documentNumber)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`currentPage`；`preferredFrame`；`documentNumber`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:190` `outboundSaveControlDiagnostics`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `visibleOutboundSaveControls`, `isOutboundSaveControlDisabled`, `outboundSaveControlDiagnostics`；是否真实写入仍取决于分支和参数。

- **L308 · 函数** `assertOutboundFormMatchesRequest(frame, items, quantityColumnId)` — 强制校验出库相关数据或步骤。
  - 输入：`frame`；`items`；`quantityColumnId`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outboundMaterialRows`, `replace`；是否真实写入仍取决于分支和参数。

- **L345 · 函数** `waitForOtherOutboundListFrame(page, timeoutMs = PAGE_NAVIGATION_TIMEOUT)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`timeoutMs = PAGE_NAVIGATION_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `hasOtherOutboundListControls`；是否真实写入仍取决于分支和参数。

- **L355 · 函数** `waitForOtherOutboundFormFrame(page, timeoutMs = PAGE_NAVIGATION_TIMEOUT)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`timeoutMs = PAGE_NAVIGATION_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `isOtherOutboundFormFrame`；是否真实写入仍取决于分支和参数。

- **L392 · 函数** `openOtherOutboundMenuItem(page, label = "其他出库单")` — 打开出库、项目相关数据或步骤。
  - 输入：`page`；`label = "其他出库单"`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:97` `waitForVisibleLeftNavigationItem`；`tools/jdy_inventory.mjs:77` `visibleTextLocatorsAcrossFrames`

- **L473 · 函数** `applyOutboundDate(input, value)` — 应用出库、日期相关数据或步骤。
  - 输入：`input`；`value`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L482 · 函数** `findExactOutboundRows(listFrame, remark)` — 查找出库相关数据或步骤。
  - 输入：`listFrame`；`remark`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:473` `applyOutboundDate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `applyOutboundDate`, `replace`；是否真实写入仍取决于分支和参数。

## `tools/repair_hardware_history.py`

Python 源码或一次性辅助文件。

- **L21 · 函数** `records(connection, sql, parameters = ())` — 记录与 `records` 对应的数据或步骤。
  - 输入：`connection`；`sql`；`parameters = ()`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L27 · 函数** `quantities(rows)` — 封装 `quantities` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`rows`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L34 · 函数** `plan_repair(connection, reference)` — 封装 `plan_repair` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`；`reference`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tools/repair_hardware_history.py:21` `records`；`tools/repair_hardware_history.py:27` `quantities`

- **L72 · 函数** `digest_documents(connection)` — 封装 `digest_documents` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tools/repair_hardware_history.py:21` `records`

- **L77 · 函数** `main()` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tools/repair_hardware_history.py:34` `plan_repair`；`tools/repair_hardware_history.py:72` `digest_documents`；`tools/repair_hardware_history.py:21` `records`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `args.backup_dir.mkdir`, `backup.close`, `source.close`, `connection.execute`, `replace_factory_hardware`, `(args.backup_dir / 'repair-report.json').write_text`, `connection.commit`, `connection.close`, `reference.close`；是否真实写入仍取决于分支和参数。
