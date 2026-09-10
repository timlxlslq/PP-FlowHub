import AppKit
import SwiftUI

private final class OperationLogHarnessModel: ObservableObject {
    @Published var steps: [InventoryStep]

    init(steps: [InventoryStep]) {
        self.steps = steps
    }
}

private struct OperationLogHarnessView: View {
    @ObservedObject var model: OperationLogHarnessModel

    var body: some View {
        SelectableOperationLogView(steps: model.steps, emptyText: "empty")
            .frame(width: 720, height: AppLayout.operationLogHeight)
    }
}

private final class HeaderBoundaryProbeBox {
    weak var view: NSView?
}

private struct HeaderBoundaryProbe: NSViewRepresentable {
    let box: HeaderBoundaryProbeBox

    func makeNSView(context: Context) -> NSView {
        let view = NSView(frame: .zero)
        box.view = view
        return view
    }

    func updateNSView(_ nsView: NSView, context: Context) {
        box.view = nsView
    }
}

private struct PageLayoutHarness: View {
    let box: HeaderBoundaryProbeBox
    let flexibleContent: Bool

    var body: some View {
        TabView {
            VStack(spacing: 0) {
                AppPageHeader(systemImage: "square", title: "页面", subtitle: "完整页面布局测试") {
                    Button("操作") {}
                }
                HeaderBoundaryProbe(box: box).frame(height: 1)
                if flexibleContent {
                    Color.clear.frame(maxWidth: .infinity, maxHeight: .infinity)
                } else {
                    Color.clear.frame(height: 420)
                }
            }
            .appPageFrame()
            .tabItem { Text("页面") }
        }
        .frame(width: AppLayout.windowMinWidth, height: 900)
    }
}

@main
private struct MacOSUIRegressionTests {
    static func main() {
        testInventoryTravelerNewestFirst()
        testPushToTalkShortcut()
        testSpeechCommandCanonicalization()
        testAssistantOrderResultParsing()
        testAssistantCompactHelpAndCancelRules()
        testMaterialDisplayNames()
        testOrderDetailMaterialRows()
        testOrderDashboardRules()
        testDashboardActivityIsScopedToAppSession()
        testPendingServerSelectionAndRefreshContract()
        testPendingInventorySourceFolderPath()
        testPendingMaterialMappingIssueRoute()
        testPendingInventoryMappingResumeContract()
        testSelectedServerPreviewFailure()
        testHardwareSourceSelectionFlow()
        testFolderPreviewMappingRecovery()
        testPendingMappingCallbacks()
        testPendingMappingMergesFolderIssues()
        testPendingCenterWorkflowUIContract()
        testOrderOutboundFactorySelection()
        testProductionFeedbackAndDashboardProgress()
        testServerWriteMaterialPreviewOrdering()
        testServerWriteHardwareChangeLayout()
        testAssistantOrderTimelineContract()
        testAssistantStageIconAssets()
        testGlassDatePickerContract()
        testTodoTableHeaderRoundedCorners()
        testSettingsDefaultWindowLayoutContract()
        testFixedWindowSizeContract()
        testSharedPageHeaderHeight()
        testInventoryActionLayoutRules()
        testProductionOrderPaths()
        testRelatedPreviewMissingMaterialIssue()
        testPP0067MissingMaterialShowsPrompt()
        testStockFailureKeepsManualRetryEnabled()
        testExistingTravelerCanBeUpdatedAfterPreviewFailure()
        testDashboardTravelerActionsUseDatabaseFacts()
        testFullPageHeaderBoundaryAlignment()
        testOperationLogScrollsAfterAppending()
        testOperationLogReader()
        testOperationLogMaintenance()
        testRunningProgressReusesOperationRow()
        testDashboardInventoryProgressText()
        testDashboardSeparatesInventoryAndRefreshTiming()
        testInventoryProgressKeepsStageHistory()
        testOrderOperationDurationFormatting()
        print("macOS UI regression tests passed")
    }

    private static func testPushToTalkShortcut() {
        require(isPushToTalkShortcut(keyCode: 49, modifiers: .option), "⌥Space 应触发按住说话")
        require(!isPushToTalkShortcut(keyCode: 49, modifiers: .command), "⌘Space 不应被语音输入占用")
        require(!isPushToTalkShortcut(keyCode: 36, modifiers: .option), "⌥Return 不应触发语音输入")
    }

    private static func testSpeechCommandCanonicalization() {
        require(canonicalSpeechCommand("查找 PP 0零6八") == "查找PP0068", "语音订单号未规范化为 PP0068")
        require(canonicalSpeechCommand("查找 P P 零 零 六 八") == "查找PP0068", "分开识别的 PP 未规范化")
        require(canonicalSpeechCommand("查找 PP 0零35杠二") == "查找PP0035-2", "语音分单号未规范化")
    }

    private static func testAssistantOrderResultParsing() {
        let object: [String: Any] = [
            "order_id": "PP0068",
            "materials_file": "/orders/PP0068 materials.xlsx",
            "materials": [["kind": "panel", "thickness": 19.1, "color": "Basalto", "quantity": 6]],
            "edge_banding": ["Basalto": 22.5],
            "factories": [[
                "factory_order": "F100",
                "order_name": "PP0068-Kitchen",
                "fittings": [["key": "hinge", "name": "Hinge", "code": "71T950A", "quantity": 4]],
            ]],
            "warnings": [],
        ]
        guard let result = AssistantOrderResult(object: object) else {
            fatalError("助手订单预览数据解析失败")
        }
        require(result.orderId == "PP0068", "助手预览订单号错误")
        require(result.materials.count == 1, "助手预览板材数据缺失")
        require(result.factories.count == 1 && result.fittings.count == 1, "助手预览工厂单或五金数据缺失")
    }

    private static func testAssistantCompactHelpAndCancelRules() {
        require(assistantCommandHints.count >= 5, "悬停命令示例内容不完整")
        require(assistantCommandHints.contains(where: { $0.contains("Find order") }), "命令示例缺少英文命令")
        require(assistantTaskShowsHeaderCancel("排队中"), "排队任务应允许在顶部取消")
        require(assistantTaskShowsHeaderCancel("执行中"), "可中断执行任务应显示顶部取消")
        require(!assistantTaskShowsHeaderCancel("等待确认"), "等待确认时不应同时显示两个取消按钮")
    }

    private static func testMaterialDisplayNames() {
        require(AppLayout.headerHeight == 64, "顶部导航与页面标题栏应采用 64pt 紧凑高度")
        require(AppLayout.topNavHeight == AppLayout.headerHeight, "顶部导航与页面页头应合并为单层")
        require(AppLayout.topPageTitleFontSize >= 19, "顶部页面标题字号仍然过小")
        require(AppLayout.headerActionSize == 44, "顶部图标操作按钮应保持统一的 44pt 尺寸")
        require(AppLayout.controlHeight == 44, "关键按钮与输入框应保持 44pt 操作目标")
        require(AppPalette.interfaceColorScheme == .light, "固定白色表面必须配套浅色文字环境")
        require(AppLayout.inventoryPreviewMinHeight >= 320, "库存预览区最小高度不足")
        require(AppLayout.windowMinWidth >= 1120, "窗口最小宽度不足以容纳导航和操作控件")
        require(AppLayout.windowIdealWidth == 1120, "默认窗口宽度应与当前助手看板截图一致")
        require(AppLayout.windowIdealHeight == 768, "默认窗口高度应与当前助手看板截图一致")
        require(AppLayout.todoDeadlineColumnWidth >= 270, "截止时间列不足以同时显示时间和过期提醒")
        require(AppLayout.todoListMaxHeight == 340, "待办列表高度未按要求压缩")
        require(AppLayout.todoInputMinHeight >= 92, "新增待办输入框高度不足三行")
        require(
            inventoryCatalogUpdateSuccessStatus(5) == "✅ 商品资料更新成功，共 5 个商品",
            "商品资料成功提示未包含明确结果和数量"
        )
        require(
            inventoryCatalogUpdateSuccessStatus(5, added: 2, updated: 1, removed: 3)
                == "✅ 商品资料更新成功，共 5 个商品（新增 2，更新 1，删除 3）",
            "商品资料成功提示未包含新增、更新和删除摘要"
        )
        require(
            inventoryCatalogUpdateFailureStatus("连接失败") == "❌ 商品资料更新失败：连接失败",
            "商品资料失败提示未包含明确错误"
        )
        require(settingsStatusKind("✅ 设置已保存") == .success, "成功状态未统一识别")
        require(settingsStatusKind("❌ 保存失败") == .danger, "错误状态未统一识别")
        require(settingsStatusKind("正在更新商品资料…") == .info, "进行中状态未统一识别")
        require(
            settingsStatusDisplayText("❌ 商品资料更新失败：连接失败") == "商品资料更新失败：连接失败",
            "统一状态提示没有移除重复状态图标"
        )
        require(AppLayout.todoTableHeaderFontSize >= 17, "待办表格标题字体仍然过小")
        require(AppLayout.todoTableBodyFontSize >= 16, "待办表格内容字体仍然过小")
        require(AppLayout.materialNameFontSize >= 18, "板材与封边名称字体仍然过小")
        func material(_ kind: String, _ thickness: Double, _ color: String = "") -> OrderMaterialPreview {
            OrderMaterialPreview(kind: kind, thickness: thickness, color: color, quantity: 1)
        }
        require(orderMaterialDisplayName(material("plywood", 18)) == "柜体板", "18mm Plywood 名称错误")
        require(orderMaterialDisplayName(material("plywood", 14.5)) == "抽屉板", "14.5mm Plywood 名称错误")
        require(orderMaterialDisplayName(material("plywood", 5.4)) == "背板", "5.4mm Plywood 名称错误")
        require(orderMaterialDisplayName(material("panel", 19.1, "Woodline 4")) == "Woodline 4", "19.1mm Panel 应只显示颜色")
        require(orderMaterialDisplayName(material("panel", 8, "Ivory Oak")) == "Ivory Oak", "8mm Panel 应只显示颜色")
        require(orderMaterialDisplayName(material("panel", 9, "Basalto")) == "Basalto", "9mm Panel 应只显示颜色")

        let productionPanel = ProductionMaterialDraft(
            id: "panel|Woodline 4|19.1|pcs",
            key: "panel|Woodline 4|19.1||pcs",
            label: "panel · Woodline 4 · 19.1 · pcs",
            materialType: "panel",
            color: "Woodline 4",
            thickness: "19.1",
            edge: "",
            unit: "pcs",
            remainingQuantity: 1,
            quantity: "1"
        )
        require(
            productionMaterialName(productionPanel) == "Woodline 4 · 19.1mm",
            "生产弹窗 Panel 应显示真实厚度，而不是厚度占位文本"
        )

        let mixed = [
            material("panel", 19.1, "Woodline 4"),
            material("panel", 9, " woodline 4 "),
            material("panel", 19.1, "Basalto"),
        ]
        require(panelColorsNeedingThicknessWarning(mixed) == Set(["woodline 4"]), "同色门板与背板未触发规格警示")
    }

    private static func testOrderDetailMaterialRows() {
        let rows = [
            OrderMaterialPreview(kind: "panel", thickness: 8, color: " woodline 4 ", quantity: 1),
            OrderMaterialPreview(kind: "plywood", thickness: 5.4, color: "", quantity: 3),
            OrderMaterialPreview(kind: "panel", thickness: 19.1, color: "Basalto", quantity: 1),
            OrderMaterialPreview(kind: "plywood", thickness: 18, color: "", quantity: 4),
            OrderMaterialPreview(kind: "panel", thickness: 9, color: "Woodline 4", quantity: 1),
            OrderMaterialPreview(kind: "panel", thickness: 19.1, color: "Woodline 4", quantity: 2),
        ]
        require(
            orderDetailPlywoodRows(rows).map { orderMaterialDisplayName($0) } == ["柜体板", "背板"],
            "订单详情 Plywood 未保持厚度顺序"
        )
        let panelRows = orderDetailPanelRows(rows)
        let expectedPanelRows = [("Basalto", 19.1), ("Woodline 4", 19.1), (" woodline 4 ", 8), ("Woodline 4", 9)]
        require(
            panelRows.count == expectedPanelRows.count
                && zip(panelRows, expectedPanelRows).allSatisfy { row, expected in
                    row.color == expected.0 && row.thickness == expected.1
                },
            "订单详情 Panel 未按颜色分组，或同色未按 19.1mm、8/9mm 顺序显示"
        )
        require(
            orderDetailEdgeColors(["Woodline 4", "Basalto", "Ivory Oak"]) == ["Basalto", "Ivory Oak", "Woodline 4"],
            "订单详情封边条未按颜色排序"
        )
    }

    private static func testOrderDashboardRules() {
        require(
            dashboardOrderRows(from: ["order": ["order_id": "PP0072"]]) == nil,
            "部分订单响应不应被当作完整订单列表"
        )
        require(
            dashboardOrderRows(from: ["orders": [["order_id": "PP0072"]]])?.count == 1,
            "完整订单列表响应没有被识别"
        )
        let dashboardSource = try! String(
            contentsOfFile: "macos/OrderDashboardView.swift",
            encoding: .utf8
        )
        let assistantSource = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        require(
            dashboardSource.contains("Button(\"详情\")")
                && dashboardSource.contains("Button(\"订单安排\")")
                && dashboardSource.contains(".sheet(item: $orderArrangementOrder)")
                && dashboardSource.contains("OrderDashboardTableLayout")
                && dashboardSource.contains("tableHeader(\"订单\", width: layout.flexibleColumnWidth)")
                && dashboardSource.contains("tableCell(width: layout.flexibleColumnWidth)")
                && dashboardSource.contains("LazyVGrid(columns: layout.columns, spacing: 0)")
                && dashboardSource.contains("LazyVGrid(columns: layout.dataColumns, spacing: 0)")
                && dashboardSource.contains(".frame(width: layout.dataWidth, alignment: .leading)")
                && dashboardSource.contains(".frame(width: layout.containerWidth, alignment: .leading)")
                && dashboardSource.contains("orderDashboardScrollIndicatorReservation")
                && dashboardSource.contains("trailingSpacerWidth")
                && dashboardSource.contains(".fixedSize(horizontal: true, vertical: true)")
                && dashboardSource.contains("minWidth: width, idealWidth: width, maxWidth: width"),
            "订单行没有同时提供材料详情和独立订单安排入口"
        )
        if let requestedStart = dashboardSource.range(of: "private func openRequestedOrderIfAvailable()"),
           let requestedEnd = dashboardSource.range(of: "private func tableHeader", range: requestedStart.upperBound..<dashboardSource.endIndex) {
            let requestedSource = String(dashboardSource[requestedStart.lowerBound..<requestedEnd.lowerBound])
            require(
                requestedSource.contains("searchText = item.orderId")
                    && requestedSource.contains("expandedOrderID = nil")
                    && !requestedSource.contains("openOrderDetail(item)"),
                "看板双击订单后只能定位到订单中心，不应自动打开订单详情"
            )
        } else {
            require(false, "无法定位看板双击订单的跳转逻辑")
        }
        require(
            dashboardSource.contains("count: 3")
                && dashboardSource.contains("LazyVGrid(columns: orderCostSourceColumns, spacing: 0)"),
            "成本来源没有使用三个等宽列"
        )
        require(
            dashboardSource.contains("Text(\"SKU\").frame(width: 68, alignment: .center)")
                && dashboardSource.contains("Text(row.productCode.isEmpty ? \"—\" : row.productCode)"),
            "成本明细没有将 SKU 从商品列拆分为独立列"
        )
        if let rowStart = dashboardSource.range(of: "private func orderRow"),
           let rowEnd = dashboardSource.range(of: "private func prepareSelectedOrder", range: rowStart.upperBound..<dashboardSource.endIndex) {
            let rowSource = String(dashboardSource[rowStart.lowerBound..<rowEnd.lowerBound])
            if let gestureStart = rowSource.range(of: "OrderDashboardClickContainer("),
               let gestureEnd = rowSource.range(of: "// Keep action buttons outside the row-level gesture recognizers.", range: gestureStart.upperBound..<rowSource.endIndex) {
                let gestureSource = String(rowSource[gestureStart.lowerBound..<gestureEnd.lowerBound])
                require(
                    !gestureSource.contains("Button(\"详情\")")
                        && !gestureSource.contains("Button(\"订单安排\")"),
                    "订单操作按钮仍位于订单行单/双击手势区域内"
                )
            } else {
                require(false, "无法定位订单行手势区域与操作列的边界")
            }
        } else {
            require(false, "无法定位订单行源码范围")
        }
        if let detailStart = dashboardSource.range(of: "struct OrderDashboardDetailPage: View"),
           let detailEnd = dashboardSource.range(of: "private var orderIdentityCard", range: detailStart.upperBound..<dashboardSource.endIndex) {
            let detailHeader = String(dashboardSource[detailStart.lowerBound..<detailEnd.lowerBound])
            require(
                !detailHeader.contains("OrderAnnotationsEditor("),
                "材料详情页不应继续嵌入订单备注与安装安排编辑器"
            )
        }
        require(dashboardStatusIsInProgress("正在后台扫描 Server 变化…"), "进行中的 Server 状态未被识别")
        require(!dashboardStatusIsInProgress("✅ Server 扫描完成"), "已完成的 Server 状态被误判为进行中")
        require(orderDashboardIsCompleted("已出货"), "已出货订单没有被识别为已完成")
        require(!orderDashboardIsCompleted("部分出货"), "部分出货订单被错误识别为已完成")
        require(dashboardMessageHoverDelay == 1.0, "消息悬停详情必须停留超过一秒后才显示")
        require(dashboardMessageHoverCloseGrace == 0.8, "消息悬停离开后应保持 0.8 秒")
        require(
            dashboardMessageHoverCanPresent(appIsActive: true, mainWindowIsFrontmost: true),
            "前台主窗口不允许显示消息悬停详情"
        )
        require(
            !dashboardMessageHoverCanPresent(appIsActive: false, mainWindowIsFrontmost: true),
            "App 不在前台时不应显示消息悬停详情"
        )
        require(
            !dashboardMessageHoverCanPresent(appIsActive: true, mainWindowIsFrontmost: false),
            "主窗口不在最前面时不应显示消息悬停详情"
        )
        let successfulAimesTrace = DashboardMessage(
            id: "aimes-success",
            source: "aimes",
            time: "12:00:00",
            title: "AIMES",
            detail: "获取 AIMES 数据成功",
            state: "success",
            operationDurations: [
                DashboardOperationDuration(label: "登录 AIMES", duration: 9.29),
            ]
        )
        require(
            dashboardMessageSupportsHoverDetail(successfulAimesTrace),
            "成功 AIMES 消息有阶段耗时时必须支持悬停详情"
        )
        require(
            !dashboardMessageSupportsHoverDetail(DashboardMessage(
                id: "aimes-running",
                source: "aimes",
                time: "12:00:01",
                title: "AIMES",
                detail: "正在获取 AIMES 数据…",
                state: "info",
                operationDurations: [
                    DashboardOperationDuration(label: "登录 AIMES", duration: 9.29),
                ]
            )),
            "进行中的 AIMES 消息不应提前显示悬停详情"
        )
        let materials = [
            OrderMaterialPreview(kind: "panel", thickness: 19.1, color: "Basalto SM", quantity: 7),
            OrderMaterialPreview(kind: "panel", thickness: 19.1, color: " basalto sm ", quantity: 1),
            OrderMaterialPreview(kind: "panel", thickness: 19.1, color: "Woodline 4", quantity: 2),
        ]
        require(orderDashboardPanelColors(materials) == ["Basalto SM", "Woodline 4"], "订单中心 Panel 颜色未按颜色去重")
        let sameColorDifferentThickness = [
            OrderMaterialPreview(kind: "panel", thickness: 19.1, color: "Woodline 4", quantity: 2, productCode: "M0019", brand: "LIOHER"),
            OrderMaterialPreview(kind: "panel", thickness: 8, color: "Woodline 4", quantity: 1, productCode: "M0019", brand: "LIOHER"),
        ]
        let panelMaterials = orderDashboardPanelMaterials(sameColorDifferentThickness)
        require(panelMaterials.count == 1 && panelMaterials[0].productCode == "M0019", "同一颜色不同厚度未共用同一个Panel图片身份")

        let stockRows = [
            OrderStockPreview(id: "A", productCode: "A", productName: "Basalto SM", unit: "张", travelerNames: [], required: 7, available: 6, shortage: 1, sufficient: false),
            OrderStockPreview(id: "B", productCode: "B", productName: "封边条", unit: "m", travelerNames: [], required: 222, available: 640, shortage: 0, sufficient: true),
        ]
        require(orderDashboardShortageCount(stockRows) == 1, "库存比对弹窗未正确统计不足项目")
        require(orderDashboardStatus(previewValidated: true, hasError: false, isExistingTraveler: true) == "已优化", "订单中心已校验状态错误")
        require(orderDashboardStatus(previewValidated: false, hasError: true, isExistingTraveler: false) == "数据异常", "订单中心异常状态错误")
        require(orderDashboardStatuses.count == 9, "订单状态列表数量发生意外变化")
        require(orderDashboardStatuses.first == "已设计" && orderDashboardStatuses.last == "数据异常", "订单状态列表顺序错误")
        require(orderDashboardMetricColumnCount == 8, "订单指标卡必须固定为一行 8 列")
        require(orderDashboardMetricColumns.count == orderDashboardMetricColumnCount, "订单指标卡列配置数量错误")
        require(
            orderDashboardFactoryCountColumnWidth == 90
                && orderDashboardUpdatedAtColumnWidth == 176
                && orderDashboardFactoryCountColumnWidth < orderDashboardUpdatedAtColumnWidth,
            "订单主表必须缩窄工厂单列，并为更新时间保留完整显示空间"
        )
        require(
            orderDashboardProgressFraction(completed: 1, total: 1) == 1,
            "订单中心已完成优化的进度条比例错误"
        )
        require(
            orderDashboardProgressFraction(completed: 1, total: 2) == 0.5,
            "订单中心部分优化的进度条比例错误"
        )
        require(
            orderDashboardProgressFraction(completed: 3, total: 2) == 1
                && orderDashboardProgressFraction(completed: -1, total: 2) == 0,
            "订单中心进度条比例未限制在有效范围"
        )
        let installationDays = [
            OrderInstallationDay(date: "2026-07-08", installer: "安装组 A"),
            OrderInstallationDay(date: "2026-07-11", installer: "安装组 B"),
        ]
        require(
            orderInstallationDateSummary(installationDays) == "2026年7月8日",
            "实际安装日期摘要必须只显示最早的安装开始日期"
        )
        require(
            orderInstallationQuickSummaries(
                planned: [OrderInstallationDay(date: "2026-07-08", installer: "安装组 A")],
                actual: [OrderInstallationDay(date: "2026-07-09", installer: "安装组 B")]
            ) == ["计划安装 2026年7月8日", "实际安装 2026年7月9日"],
            "订单行必须同时保留计划安装和实际安装摘要，不能用实际日期覆盖计划日期"
        )
        require(
            orderInstallationPlannedDateSummary([
                OrderInstallationDay(date: "2026-07-08", installer: "安装组 A"),
                OrderInstallationDay(date: "2026-07-11", installer: "安装组 B"),
            ]) == "2026年7月8日",
            "计划安装摘要必须只显示开始日期"
        )
        require(orderInstallationDisplayDate("2026-07-08") == "2026年7月8日", "安装日期显示格式错误")
        require(
            dashboardSource.contains("orderInstallationDateButtonWidth: CGFloat = 184")
                && dashboardSource.contains("struct AppGlassDatePickerCalendar: View")
                && dashboardSource.contains("LazyVGrid(columns: columns")
                && dashboardSource.contains("appGlassDatePickerDate(date, preservingTimeFrom: selection")
                && dashboardSource.contains(".presentationBackground(.clear)")
                && dashboardSource.contains("orderInstallationPickerDisplayDate")
                && dashboardSource.contains("datePickerRowID")
                && dashboardSource.contains("installationRows(title: \"实际安装开始日期\", rows: $actualDays)")
                && !dashboardSource.contains("allowsMultiple:")
                && dashboardSource.contains("AppGlassDatePickerCalendar(selection: $day.date, compact: true)")
                && dashboardSource.contains("arrowEdge: .trailing")
                && !dashboardSource.contains(".datePickerStyle(.graphical)")
                && !dashboardSource.contains("struct AppGraphicalDatePicker")
                && dashboardSource.contains("yyyy年M月d日"),
            "安装日期必须完整显示，并统一使用自定义玻璃月历"
        )

        var glassCalendar = Calendar(identifier: .gregorian)
        glassCalendar.timeZone = TimeZone(secondsFromGMT: 0)!
        let originalDateTime = glassCalendar.date(
            from: DateComponents(year: 2026, month: 8, day: 22, hour: 14, minute: 35, second: 41)
        )!
        let replacementDate = glassCalendar.date(
            from: DateComponents(year: 2026, month: 9, day: 15)
        )!
        let combinedDateTime = appGlassDatePickerDate(
            replacementDate,
            preservingTimeFrom: originalDateTime,
            calendar: glassCalendar
        )
        require(
            glassCalendar.dateComponents(
                [.year, .month, .day, .hour, .minute, .second],
                from: combinedDateTime
            ) == DateComponents(year: 2026, month: 9, day: 15, hour: 14, minute: 35, second: 41),
            "玻璃月历切换日期时必须保留待办原有的时分秒"
        )
        require(
            dashboardSource.contains("orderInstallationInstallerSuggestions")
                && dashboardSource.contains("Menu {")
                && dashboardSource.contains("TextField(\"安装人/安装小组\"")
                && !dashboardSource.contains("Image(systemName: \"chevron.down\")"),
            "安装人输入框必须支持历史下拉选择和直接输入新名称"
        )
        require(
            dashboardSource.contains(".frame(minWidth: 640, idealWidth: 700)")
                && dashboardSource.contains(".fixedSize(horizontal: false, vertical: true)")
                && dashboardSource.contains(".frame(maxHeight: 420)"),
            "订单安排窗口尺寸没有按紧凑布局调整"
        )
        require(
            dashboardSource.contains(".background(LiquidGlassPreviewBackdrop())")
                && !dashboardSource.contains(".frame(minWidth: 640, idealWidth: 700)\n        .appPageFrame()"),
            "订单安排弹窗不应继续继承主窗口的最小高度"
        )
        require(
            orderDashboardMetricsFit(width: AppLayout.windowMinWidth, horizontalPadding: AppLayout.contentPadding),
            "订单指标卡在最小窗口宽度下无法保持一行显示"
        )
        let reviewObject: [String: Any] = [
            "aimes_issues": [[
                "ignore_key": "factory:F200",
                "factory_order": "F200",
                "factory_name": "TEST ROOM",
                "sales_order_name": "BAD-ORDER",
                "reason": "销售单名称不符合规则",
                "suggested_order_id": "CS001",
            ]],
            "ignored_aimes": [[
                "ignore_key": "factory:F201",
                "factory_order": "F201",
                "factory_name": "OFFICE TEST",
                "sales_order_name": "PP0035",
                "reason": "名称包含 test",
                "ignored_at": "2026-08-10T12:00:00",
            ]],
            "assigned_aimes": [[
                "ignore_key": "factory:F202",
                "factory_order": "F202",
                "factory_name": "CS001-Unnamed",
                "sales_order_name": "SHERRY 001",
                "reason": "已按工厂单名称确认归入 CS001",
                "suggested_order_id": "CS001",
                "ignored_at": "2026-08-10T13:00:00",
            ]],
        ]
        let pendingReviews = aimesReviewItems(reviewObject, key: "aimes_issues")
        let ignoredReviews = aimesReviewItems(reviewObject, key: "ignored_aimes")
        let assignedReviews = aimesReviewItems(reviewObject, key: "assigned_aimes")
        require(pendingReviews.count == 1 && pendingReviews[0].factoryOrder == "F200", "AIMES 待确认清单解析错误")
        require(
            !shouldPresentPendingCenterAfterAimes(
                presentIfNeeded: true,
                pendingAimesReviews: [],
                aimesFormatWarnings: []
            ),
            "仅有 Server 待处理项目时，获取 AIMES 不应弹出待处理中心"
        )
        require(
            shouldPresentPendingCenterAfterAimes(
                presentIfNeeded: true,
                pendingAimesReviews: pendingReviews,
                aimesFormatWarnings: []
            ),
            "存在 AIMES 待确认记录时，应允许获取 AIMES 后打开待处理中心"
        )
        require(pendingReviews[0].suggestedOrderID == "CS001", "AIMES 工厂单名称建议订单号解析错误")
        require(ignoredReviews.count == 1 && !ignoredReviews[0].ignoredAt.isEmpty, "AIMES 已忽略记录解析错误")
        require(assignedReviews.count == 1 && assignedReviews[0].suggestedOrderID == "CS001", "AIMES 已确认建议归属解析错误")
        let warningReviews = aimesReviewItemsFromWarnings([[
            "ignore_key": "factory:F203",
            "factory_order": "F203",
            "factory_name": "CS001-Unnamed",
            "sales_order_name": "SHERRY 001",
            "reason": "销售单名称不是标准订单号",
            "suggested_order_id": "CS001",
        ]])
        require(
            warningReviews.count == 1
                && warningReviews[0].salesOrderName == "SHERRY 001"
                && warningReviews[0].suggestedOrderID == "CS001",
            "销售单格式异常没有转换为可人工处理记录"
        )
        require(
            shouldPresentPendingCenterAfterAimes(
                presentIfNeeded: true,
                pendingAimesReviews: [],
                aimesFormatWarnings: warningReviews
            ),
            "存在 AIMES 销售单格式异常时，应进入统一待处理中心"
        )
        let aimesActionDetails = dashboardAimesActionDetails(
            pending: pendingReviews,
            ignored: ignoredReviews,
            assigned: assignedReviews
        )
        require(aimesActionDetails.contains("已忽略 1 条："), "AIMES 已忽略数量详情缺失")
        require(aimesActionDetails.contains(where: { $0.contains("F201") && $0.contains("OFFICE TEST") }), "AIMES 已忽略具体工厂单详情缺失")
        let normalizedAimesStages = dashboardFlatOperationDurations([
            ["stage": "browser_launch", "label": "启动 AIMES 浏览器", "duration_seconds": 0.37],
            ["stage": "attempt", "label": "获取 AIMES 数据成功，总计用时", "duration_seconds": 44.11],
            ["stage": "factory_order_verify", "label": "精确核验工厂单存在性", "duration_seconds": 28.83],
        ])
        require(
            normalizedAimesStages.map(\.label) == ["启动 AIMES 浏览器", "精确核验工厂单存在性"],
            "AIMES 总耗时不应作为阶段重复显示"
        )
        let warningDetails = dashboardAimesWarningDetails([[
            "factory_order": "F2606150155",
            "factory_name": "PP0018 DRAWER",
            "sales_order_name": "PP0018 DRAWER",
            "reason": "销售单名称不是标准订单号",
        ]])
        require(warningDetails.contains(where: { $0.contains("PP0018 DRAWER") && $0.contains("销售单名称") }), "销售单格式异常详情没有显示销售单名称")
        let aimesPerformanceMessages = dashboardMessages(
            syncStatus: "订单数据同步完成",
            syncTime: "12:02:00",
            aimesStatus: "⚠️ AIMES 发现 1 条销售单格式异常",
            aimesTime: "12:02:01",
            serverStatus: "Server 尚未扫描",
            serverTime: "12:02:02",
            activity: [],
            contextDetailsBySource: ["aimes": warningDetails],
            durationsBySource: ["aimes": 61.95],
            operationDurationsBySource: ["aimes": [
                DashboardOperationDuration(label: "启动 AIMES 浏览器", duration: 0.74),
                DashboardOperationDuration(label: "登录 AIMES", duration: 35.10),
                DashboardOperationDuration(label: "读取 AIMES 工厂订单表格", duration: 1.20),
            ]]
        )
        let aimesPerformance = aimesPerformanceMessages.first(where: { $0.source == "aimes" })
        require(dashboardMessageDetailText(aimesPerformance!).contains("启动 AIMES 浏览器：0.74 秒"), "AIMES 阶段耗时没有进入消息列表")
        let aimesSummary = dashboardMessageSummaryText(aimesPerformance!)
        require(aimesSummary.contains("总计用时 61.95 秒"), "消息标题没有显示 AIMES 总计用时")
        require(!aimesSummary.contains("启动 AIMES 浏览器"), "消息标题不应显示阶段明细")
        let runningSummary = dashboardMessageSummaryText(
            DashboardMessage(
                id: "running",
                source: "sync",
                time: "12:04:00",
                title: "订单数据",
                detail: "正在读取本地订单缓存…",
                state: "info",
                duration: 0
            ),
            showsDuration: false
        )
        require(!runningSummary.contains("总计用时"), "当前操作不应显示尚未完成的总计用时")
        require(aimesPerformance?.contextDetails.contains(where: { $0.contains("PP0018 DRAWER") }) == true, "销售单异常明细没有进入消息上下文")
        let duplicateStatusMessages = dashboardMessages(
            syncStatus: "⚠️ AIMES 发现 1 条销售单格式异常",
            syncTime: "12:03:00",
            aimesStatus: "⚠️ AIMES 发现 1 条销售单格式异常",
            aimesTime: "12:03:01",
            serverStatus: "Server 尚未扫描",
            serverTime: "12:03:02",
            activity: [],
            durationsBySource: ["sync": 0.66, "aimes": 17.36],
            operationDurationsBySource: ["aimes": [
                DashboardOperationDuration(label: "登录 AIMES", duration: 9.99),
            ]]
        )
        let duplicateAimes = duplicateStatusMessages.first(where: { $0.source == "aimes" })
        require(duplicateStatusMessages.filter { $0.detail.contains("销售单格式异常") }.count == 1, "相同状态消息没有正确去重")
        require(duplicateAimes?.duration == 17.36, "相同状态去重时错误保留了订单数据耗时")
        require(duplicateAimes?.operationDurations.first?.label == "登录 AIMES", "相同状态去重时 AIMES 阶段明细丢失")

        let serverFolder = "/Volumes/server/Optimized Orders/pp0035-2"
        let serverChanges = [
            ServerChangePreview(
                id: "added:\(serverFolder)",
                changeType: "added",
                kind: "folder",
                orderId: "PP0035-2",
                sourceFolder: serverFolder,
                path: serverFolder,
                message: "新增订单文件夹",
                manualOnly: false,
                eventTime: "2026-08-12T10:00:00"
            ),
            ServerChangePreview(
                id: "modified:\(serverFolder)/material.xlsx",
                changeType: "modified",
                kind: "material",
                orderId: "PP0035-2",
                sourceFolder: serverFolder,
                path: "\(serverFolder)/material.xlsx",
                message: "材料发生变化",
                manualOnly: false,
                eventTime: "2026-08-12T10:01:00"
            ),
        ]
        let folderIssue = CurrentIssue(
            id: "order_validation:\(serverFolder)",
            kind: "order_validation",
            orderId: "PP0035-2",
            factoryOrder: "",
            path: "\(serverFolder)/material.xlsx",
            message: "材料映射失败，请检查 material。",
            firstSeen: "2026-08-12T10:00:00",
            lastSeen: "2026-08-12T10:00:00"
        )
        let unifiedItems = buildPendingCenterItems(
            serverChanges: serverChanges,
            currentIssues: [folderIssue],
            aimesReviews: []
        )
        require(unifiedItems.count == 1, "同一 Server 文件夹不应同时显示为多个待处理项目")
        require(unifiedItems[0].serverGroup?.changes.count == 2, "待处理中心没有保留文件变化明细")
        require(unifiedItems[0].issues.count == 1 && unifiedItems[0].status == "处理失败", "文件夹失败原因没有合并到主记录")
        let readyItems = buildPendingCenterItems(
            serverChanges: [serverChanges[0]],
            currentIssues: [],
            aimesReviews: []
        )
        require(readyItems.count == 1 && readyItems[0].status == "待处理", "扫描完成但未发现问题的项目应显示为待处理")
        let manualItems = buildPendingCenterItems(
            serverChanges: [serverChanges[0]],
            currentIssues: [CurrentIssue(
                id: "temporary_mapping",
                kind: "temporary_processing",
                orderId: "PP0035-2",
                factoryOrder: "",
                path: serverFolder,
                message: "未映射材料",
                firstSeen: "2026-08-12T10:00:00",
                lastSeen: "2026-08-12T10:00:00"
            )],
            aimesReviews: []
        )
        require(manualItems.count == 1 && manualItems[0].status == "需人工处理", "材料映射问题应显示为需人工处理")
        let withSeparateAimes = buildPendingCenterItems(
            serverChanges: serverChanges,
            currentIssues: [folderIssue],
            aimesReviews: pendingReviews
        )
        require(withSeparateAimes.count == 2, "AIMES 独立待确认记录没有进入统一待处理中心")
        require(withSeparateAimes.contains(where: { $0.aimesReviews.count == 1 }), "AIMES 待确认记录类型丢失")
        let withFormatWarning = buildPendingCenterItems(
            serverChanges: [],
            currentIssues: [],
            aimesReviews: [],
            aimesFormatWarnings: warningReviews
        )
        require(withFormatWarning.count == 1 && withFormatWarning[0].aimesFormatWarnings.count == 1, "AIMES 格式异常没有进入统一待处理中心")
        require(withFormatWarning[0].status == "待人工确认", "AIMES 格式异常必须显示待人工确认")
        require(withSeparateAimes.last?.status == "待人工确认", "AIMES review 必须显示待人工确认")
        for kind in ["factory_ownership", "server_missing_report", "material_mapping", "hardware_mapping", "material_validation"] {
            let issue = CurrentIssue(id: kind, kind: kind, orderId: "PP0035-2", factoryOrder: "F1", path: serverFolder + "/Report/material.xlsx", message: "未完成商品 SKU 处理：A", firstSeen: "", lastSeen: "")
            for changes in [serverChanges, []] {
                let items = buildPendingCenterItems(serverChanges: changes, currentIssues: [issue], aimesReviews: [])
                let expected = ["factory_ownership", "server_missing_report"].contains(kind) ? "待人工确认" : "需人工处理"
                require(items.first?.status == expected, "独立和合并问题必须保持相同分类：\(kind)")
                require(!items.contains { $0.status == "稍后处理" }, "稍后处理不能成为状态")
            }
        }
        let dashboardLog = dashboardActivitySteps([
            "changes": [[
                "observed_at": "2026-08-10T12:34:56",
                "severity": "warning",
                "kind": "order_validation",
                "order_id": "PP0063-2",
                "factory_order": "F2607270215",
                "path": "/Volumes/server/Optimized Orders/pp0063-2/materials.xlsx",
                "message": "订单报表需要检查，请补充 material 后重新处理。",
            ]],
        ])
        require(dashboardLog.count == 1, "看板操作记录没有解析数据变化")
        require(dashboardLog[0].time == "12:34:56" && dashboardLog[0].state == "warning", "看板操作记录时间或状态错误")
        require(
            dashboardLog[0].operationDetails.contains(where: { $0.contains("PP0063-2") && $0.contains("F2607270215") }),
            "订单更新悬停详情没有显示订单号和工厂单号"
        )
        require(
            dashboardLog[0].operationDetails.contains(where: { $0.contains("materials.xlsx") }),
            "订单更新悬停详情没有显示来源文件"
        )
        require(
            dashboardActivitySteps(["changes": [["message": "历史消息"]]], includeChanges: false).isEmpty,
            "读取本地缓存时不应把历史消息放进本次消息记录"
        )
        let combinedDashboardMessages = dashboardMessages(
            syncStatus: "✅ 已显示本地缓存；后台检查完成",
            syncTime: "12:00:01",
            aimesStatus: "✅ 今天已成功获取过 AIMES，本次略过",
            aimesTime: "12:00:02",
            serverStatus: "⚠️ 服务器目录不可访问",
            serverTime: "12:00:03",
            activity: dashboardLog
        )
        require(combinedDashboardMessages.count == 4, "当前状态和历史记录没有合并到同一个消息框")
        require(combinedDashboardMessages.map(\.source) == ["sync", "aimes", "server", "activity"], "消息没有按统一时间顺序排列")
        require(!combinedDashboardMessages[0].detail.hasPrefix("✅"), "消息记录正文不应重复显示状态图标")
        require(combinedDashboardMessages.dropFirst().allSatisfy { !$0.time.isEmpty }, "消息记录没有显示时间")
        let tracedDashboardMessages = dashboardMessages(
            syncStatus: "✅ 订单数据同步完成",
            syncTime: "12:01:00",
            aimesStatus: "AIMES 尚未检查",
            aimesTime: "12:01:01",
            serverStatus: "✅ Server 变化已处理（2 项）",
            serverTime: "12:01:02",
            activity: [],
            operationDetailsBySource: ["server": ["从 Server 目录读取订单号 1 个、工厂单号 2 个的报表。", "写入到了 order-index.sqlite3。"]],
            manualPathsBySource: ["server": ["/Volumes/server/PP0035-2/material.xlsx", ""]],
            contextDetailsBySource: ["server": ["Server 已完成扫描，当前没有新增、修改或删除的订单文件。"]]
        )
        let tracedServer = tracedDashboardMessages.first(where: { $0.source == "server" })
        require(tracedServer?.operationDetails.count == 2, "自动处理详情没有附加到看板消息")
        require(tracedServer?.manualPaths == ["/Volumes/server/PP0035-2/material.xlsx"], "人工处理文件路径没有附加到看板消息")
        require(tracedServer?.contextDetails.count == 1, "看板处理结果摘要没有附加到消息")
        let performanceTrace = dashboardMessages(
            syncStatus: "订单数据同步完成",
            syncTime: "12:01:00",
            aimesStatus: "AIMES 尚未检查",
            aimesTime: "12:01:01",
            serverStatus: "Server 扫描完成",
            serverTime: "12:01:02",
            activity: [],
            operationDetailsBySource: ["server": [
                "快速检查 8 个相关 XML 文件，复用 2 个订单文件夹，深度扫描 1 个订单文件夹，总用时 0.12 秒。",
                "扫描范围：订单文件夹 3 个，相关 XML 文件 8 个（目录：/Volumes/server/Optimized Orders）。",
                "变化统计：新增 1 个，修改 2 个，删除 0 个。",
            ]],
            durationsBySource: ["server": 20.205],
            operationDurationsBySource: ["server": [
                DashboardOperationDuration(label: "扫描 Server", duration: 18.485),
                DashboardOperationDuration(label: "更新 Server 订单索引", duration: 1.720),
            ]]
        )
        let performanceServer = performanceTrace.first(where: { $0.source == "server" })
        require(performanceServer?.operationDetails.contains("快速检查 8 个相关 XML 文件，复用 2 个订单文件夹，深度扫描 1 个订单文件夹，总用时 0.12 秒。") == true, "Server 扫描方式统计没有进入悬停详情")
        require(performanceServer?.operationDetails.contains("扫描范围：订单文件夹 3 个，相关 XML 文件 8 个（目录：/Volumes/server/Optimized Orders）。") == true, "Server 扫描范围统计没有进入悬停详情")
        require(performanceServer?.operationDetails.contains("变化统计：新增 1 个，修改 2 个，删除 0 个。") == true, "Server 变化数量统计没有进入悬停详情")
        require(dashboardMessageDetailText(performanceServer!).contains("用时 20.20 秒"), "订单消息没有显示总操作用时")
        require(dashboardMessageDetailText(performanceServer!).contains("扫描 Server："), "Server 阶段耗时没有进入消息列表")
        require(dashboardMessageDetailText(performanceServer!).contains("更新 Server 订单索引："), "Server 每个阶段耗时没有进入消息列表")
        require(performanceServer?.operationDurations.map(\.label) == ["扫描 Server", "更新 Server 订单索引"], "Server 后台阶段没有完整保留")
        require(performanceServer?.operationDurations.map(\.duration) == [18.485, 1.720], "Server 后台阶段耗时没有完整保留")
        require(dashboardMessageVisibleRowCount == 3, "消息记录框必须一次显示 3 条记录")
        require(dashboardMessageViewportHeight == dashboardMessageRowHeight * 3, "消息记录框高度与三条记录不匹配")
        let deduplicatedMessages = dashboardMessages(
            syncStatus: "⚠️ 服务器目录不可访问",
            syncTime: "12:00:01",
            aimesStatus: "✅ AIMES 获取成功",
            aimesTime: "12:00:02",
            serverStatus: "⚠️ 服务器目录不可访问",
            serverTime: "12:00:03",
            activity: []
        )
        require(deduplicatedMessages.count == 2, "相同状态消息没有自动去重")
        let runningDisplay = dashboardCurrentOperation(messages: [
            DashboardMessage(id: "1", source: "aimes", time: "12:00:00", title: "AIMES", detail: "正在获取数据…", state: "info"),
            DashboardMessage(id: "2", source: "server", time: "12:00:01", title: "Server", detail: "扫描完成", state: "success"),
        ], isRunning: true)
        require(runningDisplay?.isRunning == true && runningDisplay?.message.id == "1", "进行中操作没有优先显示")
        let runningMessages = dashboardMessages(
            syncStatus: "订单数据同步完成",
            syncTime: "12:01:00",
            aimesStatus: "AIMES 尚未检查",
            aimesTime: "12:01:01",
            serverStatus: "正在自动处理 Server 变化并解析相关报表…",
            serverTime: "12:01:02",
            activity: []
        )
        let visibleWhileRunning = dashboardVisibleMessages(runningMessages, isRunning: true)
        require(!visibleWhileRunning.contains(where: { dashboardStatusIsInProgress($0.detail) }), "进行中的操作不应显示在消息列表")
        require(dashboardVisibleMessages(runningMessages, isRunning: false).count == runningMessages.count, "操作完成后不应隐藏消息记录")
        let orderedMessages = dashboardMessages(
            syncStatus: "✅ 订单列表刷新完成",
            syncTime: "12:00:03",
            aimesStatus: "✅ AIMES 完成",
            aimesTime: "12:00:01",
            serverStatus: "✅ Server 完成",
            serverTime: "12:00:02",
            activity: [InventoryStep(time: "12:00:00", title: "生产", detail: "生产完成", state: "success")]
        )
        require(
            orderedMessages.map(\.time) == ["12:00:00", "12:00:01", "12:00:02", "12:00:03"],
            "消息列表没有按统一时间队列排列"
        )
        let serverRows = serverChangePreviews([
            [
                "id": "added:/Volumes/server/CS003 PP0047",
                "change_type": "added",
                "kind": "folder",
                "order_id": "CS003、PP0047",
                "source_folder": "/Volumes/server/CS003 PP0047",
                "path": "/Volumes/server/CS003 PP0047",
                "message": "Server 混单文件夹新增：CS003 PP0047",
                "manual_only": false,
                "event_time": "2026-08-12T10:00:00",
                "mixed_order": true,
            ],
            [
                "id": "added:/Volumes/server/b12",
                "change_type": "added",
                "kind": "folder",
                "order_id": "",
                "source_folder": "/Volumes/server/b12",
                "path": "/Volumes/server/b12",
                "message": "Server 临时订单文件夹新增：b12",
                "manual_only": true,
                "event_time": "2026-08-12T10:02:00",
            ],
            [
                "id": "missing_report:/Volumes/server/CS003 PP0047",
                "change_type": "missing_report",
                "kind": "folder",
                "order_id": "CS003、PP0047",
                "source_folder": "/Volumes/server/CS003 PP0047",
                "path": "/Volumes/server/CS003 PP0047",
                "message": "Server 混单文件夹缺少可识别的报表",
                "manual_only": false,
                "event_time": "2026-08-12T10:00:00",
                "mixed_order": true,
            ],
        ])
        require(serverRows.count == 3 && !serverRows[0].manualOnly && serverRows[1].manualOnly, "Server 混单与临时目录状态解析错误")
        require(serverRows[0].orderId == "CS003、PP0047", "Server 混单订单号没有保留完整订单集合")
        require(serverRows[0].eventTime == "2026-08-12T10:00:00", "Server 文件变化时间没有保留")
        let groupedServerRows = serverFolderChangeGroups(serverRows)
        require(groupedServerRows.count == 2, "Server 待处理变化没有按文件夹分组")
        require(groupedServerRows.allSatisfy { $0.changes.count == 2 || $0.changes.count == 1 }, "Server 文件夹分组没有保留文件变化明细")
        require(groupedServerRows.contains { $0.requiresManualReview }, "缺少报表的混单文件夹没有标记为人工检查")
        require(
            dashboardSource.contains("已人工处理") &&
                dashboardSource.contains("model.markTemporaryFolderManual(group.folderPath)"),
            "普通临时 Server 文件夹没有已人工处理入口"
        )
        require(
            assistantSource.contains("serverChangesExcludingFolder") &&
                !dashboardSource.contains("忽略此文件夹") &&
                !assistantSource.contains("ignoreServerFolder"),
            "已人工处理动作不应保留旧的 Server 文件夹忽略入口"
        )
        let handledFolder = "/Volumes/server/Optimized Orders/temporary"
        let retainedServerChanges = serverChangesExcludingFolder(
            [
                ServerChangePreview(
                    id: "temporary",
                    changeType: "added",
                    kind: "folder",
                    orderId: "",
                    sourceFolder: handledFolder,
                    path: handledFolder,
                    message: "临时文件夹",
                    manualOnly: true,
                    eventTime: ""
                ),
                ServerChangePreview(
                    id: "other",
                    changeType: "added",
                    kind: "folder",
                    orderId: "",
                    sourceFolder: "/Volumes/server/Optimized Orders/other",
                    path: "/Volumes/server/Optimized Orders/other",
                    message: "其他文件夹",
                    manualOnly: true,
                    eventTime: ""
                ),
            ],
            folderPath: handledFolder
        )
        require(
            retainedServerChanges.map(\.id) == ["other"],
            "处理一个 Server 文件夹时不应丢失其他待处理文件夹"
        )
        let completedDisplay = dashboardCurrentOperation(messages: combinedDashboardMessages, isRunning: false)
        require(completedDisplay?.isRunning == false && completedDisplay?.message.state == "warning", "空闲时没有显示最近成功或失败结果")
        require(!dashboardMessageScrollKey(combinedDashboardMessages).isEmpty, "消息变化无法触发自动滚动")
        let reviewModel = AppModel()
        reviewModel.toggleAimesReviewSelection(pendingReviews[0])
        require(reviewModel.selectedAimesReviewIDs == Set(["factory:F200"]), "AIMES 待确认记录无法选中")
        reviewModel.toggleAimesReviewSelection(pendingReviews[0])
        require(reviewModel.selectedAimesReviewIDs.isEmpty, "AIMES 待确认记录无法取消选择")
        require(
            orderDashboardStatusHelp(status: "数据异常", validationMessage: "缺少 material，请补充后重新扫描 Server。")
                == "缺少 material，请补充后重新扫描 Server。",
            "数据异常悬停提示没有使用数据库中的业务原因"
        )
        require(orderDashboardStatusHelp(status: "已优化", validationMessage: "不应显示").isEmpty, "正常状态不应显示异常提示")
        let technical = businessFriendlyMessage(
            "Traceback: Error Domain=NSPOSIXErrorDomain Code=2, status code 500",
            operation: "订单操作"
        )
        require(technical.contains("订单操作未完成"), "底层错误没有转换为业务提示")
        require(!technical.lowercased().contains("traceback") && !technical.contains("500"), "业务提示仍泄露底层错误代码")
        require(
            businessFriendlyMessage("未找到 material 文件，请补充后重试。", operation: "订单操作").contains("material"),
            "可执行的中文业务提示不应被覆盖"
        )
        require(
            dashboardFailureMessage(
                "更新 Server 订单索引失败",
                rawError: "订单操作未完成。请重试；如果仍然失败，请检查相关文件、网络和登录状态后再操作。",
                operation: "更新 Server 订单索引"
            ) == "更新 Server 订单索引失败",
            "Server 订单索引失败没有显示当前阶段的失败文案"
        )
        require(
            businessFriendlyMessage(
                "locator.waitFor: Timeout 10000ms exceeded #storage/otherOutbound_menu",
                operation: "库存操作"
            ).contains("库存操作未完成") &&
                businessFriendlyMessage(
                    "locator.waitFor: Timeout 10000ms exceeded #storage/otherOutbound_menu",
                    operation: "库存操作"
                ).contains("左侧“仓库”菜单"),
            "出库菜单超时没有转换为可执行的阶段提示"
        )
        let leakedPythonDetail = businessFriendlyMessage(
            "Excel 文件无法读取，请检查文件是否损坏或仍在编辑：cannot access local variable 'order_hint' where it is not associated with a value",
            operation: "订单数据"
        )
        require(
            leakedPythonDetail.contains("订单数据未完成") && !leakedPythonDetail.contains("order_hint"),
            "中文错误消息仍泄露 Python 局部变量名"
        )
        require(
            appDisplayTimestamp("2026-07-31T14:57:15") == "2026-07-31 14:57:15",
            "时间显示没有将 ISO 的 T 替换为空格"
        )
        let fileSpecificActivity = dashboardActivitySteps([
            "changes": [[
                "observed_at": "2026-08-12T11:11:40",
                "severity": "warning",
                "kind": "report_error",
                "path": "/Volumes/server/Optimized Orders/Report/Fittingslist.xlsx",
                "message": "Fittingslist Fittingslist.xlsx 无法读取，请检查文件格式。",
            ]],
        ])
        require(
            fileSpecificActivity.first?.detail.contains("Fittingslist.xlsx") == true,
            "Excel 读取失败详情没有显示具体文件名"
        )
        require(orderDashboardExpandedID(current: nil, tapped: "PP0035-2") == "PP0035-2", "点击折叠订单行应展开")
        require(orderDashboardExpandedID(current: "PP0035-2", tapped: "PP0035-2") == nil, "再次点击同一订单行应折叠")
        require(orderDashboardExpandedID(current: "PP0035", tapped: "PP0035-2") == "PP0035-2", "点击其他订单行应切换展开项")
        require(orderDashboardExpandedID(current: "PP0035-2", tapped: "PP0035-2", forceOpen: true) == "PP0035-2", "强制打开不应意外折叠")
        require(appDefaultSectionRawValue == "orders", "App 默认页面必须继续是订单中心")
        let augustReference = dashboardBusinessDate("2026-08-29T12:00:00")!
        require(
            dashboardTimestamp("2026-08-01T08:30:00", isInSameMonthAs: augustReference),
            "助手看板没有按订单完成时间统计本月已完成"
        )
        require(
            !dashboardTimestamp("2026-07-31T23:59:59", isInSameMonthAs: augustReference),
            "助手看板把上月完成订单计入本月"
        )
        require(
            !dashboardTimestamp("", isInSameMonthAs: augustReference),
            "缺少完成时间的订单不应计入本月已完成"
        )
        _ = OrderDashboardMetricsView(model: AppModel())
        _ = OrderDashboardView(model: AppModel())
    }

    private static func testDashboardActivityIsScopedToAppSession() {
        let sessionStartedAt = dashboardBusinessDate("2026-09-04T08:45:00")!
        let activity = dashboardActivitySteps(
            [
                "changes": [
                    [
                        "observed_at": "2026-09-03T12:00:00",
                        "message": "昨天的历史消息",
                    ],
                    [
                        "observed_at": "2026-09-04T08:44:59",
                        "message": "本次启动前的历史消息",
                    ],
                    [
                        "observed_at": "2026-09-04T08:45:01",
                        "message": "本次启动后的消息",
                    ],
                ],
            ],
            sessionStartedAt: sessionStartedAt
        )
        require(
            activity.map(\.detail) == ["本次启动后的消息"],
            "订单中心操作记录应只显示本次 App 打开后发生的记录"
        )
    }

    private static func testPendingServerSelectionAndRefreshContract() {
        let dashboardSource = try! String(
            contentsOfFile: "macos/OrderDashboardView.swift",
            encoding: .utf8
        )
        let assistantSource = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        require(
            assistantSource.contains("selectedServerFolderPaths = [folderPath]")
                && !dashboardSource.contains("Button(\"全选\") { model.selectAllServerFolders() }")
                && !dashboardSource.contains("Button(\"取消全选\") { model.clearServerFolderSelection() }")
                && assistantSource.contains("serverChangesExcludingFolders")
                && assistantSource.contains("refreshDashboardAfterServerWrite(processedFolders: preview.sourceFolders)")
                && assistantSource.contains("pendingServerChanges = serverChangesExcludingFolders")
                && assistantSource.contains("closePendingCenterIfEmpty()"),
            "待处理中心必须单选，并在 Server 写入成功后同步订单、助手和待处理列表"
        )
        require(
            assistantSource.contains("aimesFormatWarnings: aimesFormatWarnings")
                && assistantSource.contains("hasAimesHistory")
                && !assistantSource.contains("AimesReviewSheet(model: model)")
                && !dashboardSource.contains("处理 AIMES 异常")
                && dashboardSource.contains("历史 AIMES 记录"),
            "AIMES 异常必须统一进入待处理中心，并保留默认收起的历史记录"
        )
    }

    private static func testPendingInventorySourceFolderPath() {
        let reportFile = "/Volumes/server/Optimized Orders/pp0072/PP0072-MasterBed_Landing_Bed1_Bed2_Office/Report/FittingslistPC124429962608190002.xlsx"
        require(
            inventoryMappingSourceFolderPath(reportFile) == "/Volumes/server/Optimized Orders/pp0072/PP0072-MasterBed_Landing_Bed1_Bed2_Office",
            "订单文件映射重读没有回到标准订单根目录"
        )
        let reportFolder = "/Volumes/server/Optimized Orders/pp0072/PP0072-MasterBed_Landing_Bed1_Bed2_Office/Report"
        require(
            inventoryMappingSourceFolderPath(reportFolder) == "/Volumes/server/Optimized Orders/pp0072/PP0072-MasterBed_Landing_Bed1_Bed2_Office",
            "Report 文件夹路径没有回到标准订单根目录"
        )
        let temporaryReport = "/Volumes/server/temporary-order/Fittingslist.xlsx"
        require(
            inventoryMappingSourceFolderPath(temporaryReport) == "/Volumes/server/temporary-order",
            "临时订单报表路径没有保留临时订单文件夹"
        )
    }

    private static func testPendingMaterialMappingIssueRoute() {
        let materialMappingIssue = CurrentIssue(
            id: "material_validation:PP0057:/server/PP0057 materials.xlsx",
            kind: "material_validation",
            orderId: "PP0057",
            factoryOrder: "",
            path: "/Volumes/server/Optimized Orders/pp0057/pp0057 materials.xlsx",
            message: "material 文件 pp0057 materials.xlsx 校验未通过：订单 PP0057 存在未完成商品 SKU 处理：19.1mm--Muratti 4、Edge banding--Muratti 4；请先设置映射或加入全局忽略清单。",
            firstSeen: "2026-08-25T08:32:35",
            lastSeen: "2026-08-25T08:32:35"
        )
        require(
            currentIssueRequiresInventoryMapping(materialMappingIssue),
            "材料 SKU 校验失败应进入订单文件映射工作台"
        )

        let malformedWorkbookIssue = CurrentIssue(
            id: "material_validation:PP0057:/server/PP0057 materials.xlsx",
            kind: "material_validation",
            orderId: "PP0057",
            factoryOrder: "",
            path: "/Volumes/server/Optimized Orders/pp0057/pp0057 materials.xlsx",
            message: "material 文件无法读取：工作簿格式不正确。",
            firstSeen: "2026-08-25T08:32:35",
            lastSeen: "2026-08-25T08:32:35"
        )
        require(
            !currentIssueRequiresInventoryMapping(malformedWorkbookIssue),
            "普通 material 文件读取失败不应误显示 SKU 映射入口"
        )
    }

    private static func testPendingInventoryMappingResumeContract() {
        let source = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        require(
            source.contains("private struct PendingResumeContext")
                && source.contains("case rereadSourceThenPresentReadOnlyPreview")
                && source.contains("let originalItem: PendingCenterItem?"),
            "材料映射续接必须保存明确的来源文件重读与只读预览上下文"
        )
        guard let saveStart = source.range(of: "func saveInventoryMapping(travelerName: String, productCode: String)"),
              let saveEnd = source.range(of: "\n    func saveServerHardwareMapping", range: saveStart.upperBound..<source.endIndex) else {
            require(false, "无法找到材料映射保存方法"
            )
            return
        }
        let saveSource = String(source[saveStart.lowerBound..<saveEnd.lowerBound])
        require(
            saveSource.contains("resumePendingMappingOperationAfterMapping()")
                && !saveSource.contains("previewSelectedInventory()")
                && !saveSource.contains("rereadPendingSourceFolder()"),
            "映射保存完成后必须进入单一续接协调器，不能同时启动预览和来源文件重读"
        )
        require(
            source.contains("onDismiss: model.inventoryMappingWorkspaceDidDismiss")
                && source.contains("presentServerWritePreview(preview)")
                && source.contains("pendingResumeContext = nil"),
            "来源文件重读成功后才可设置只读预览提示，并清理一次性续接上下文"
        )
        require(
            !saveSource.contains("confirmServerWrite")
                && !saveSource.contains("writeInventory")
                && !saveSource.contains("--confirm-save"),
            "材料映射续接不得自动确认或触发真实写入"
        )
    }

    private static func testPendingCenterWorkflowUIContract() {
        let source = try! String(contentsOfFile: "macos/OrderDashboardView.swift", encoding: .utf8)
        let app = try! String(contentsOfFile: "macos/TravelerAssistant.swift", encoding: .utf8)
        let start = source.range(of: "struct PendingCenterSheet: View")!.lowerBound
        let end = source.range(of: "struct ServerWriteConfirmationSheet: View")!.lowerBound
        let sheet = String(source[start..<end])
        require(sheet.contains(".frame(width: 980, height: 620)") && app.contains(".frame(minWidth: 980, minHeight: 620)"), "待处理中心根容器与详情必须采用紧凑尺寸")
        require(sheet.contains("[\"全部\", \"待处理\", \"处理失败\", \"待人工确认\", \"需人工处理\"]"), "筛选必须使用四种业务分类")
        require(sheet.contains("visibleItems.first { $0.id == selectedID }") && sheet.contains("selectedID = item.id"), "详情必须跟随可见队列选择")
        require(sheet.contains("model.selectedServerFolderPaths.removeAll()") && sheet.contains("model.selectedAimesReviewIDs.removeAll()"), "切换项目必须清除旧操作选择")
        require(sheet.contains("Button(\"稍后处理\") { model.showPendingCenterPrompt = false }") && sheet.contains("选择并预览"), "稍后处理只关闭，预览必须有明确入口")
        require(sheet.contains(".alert(confirmationTitle, isPresented: $showActionConfirmation)") && sheet.contains("pendingAction?()"), "待处理业务动作必须经过二次确认")
        let preview = String(source[end...])
        require(preview.contains(".alert(\"确认后写入\", isPresented: $showWriteConfirmation)") && preview.contains("guard canConfirmWrite else { return }"), "写入预览必须保留显式二次确认和校验门禁")
    }

    private static func testSelectedServerPreviewFailure() {
        let model = AppModel()
        let folder = URL(fileURLWithPath: "/tmp/PP0062-KITCHEN_20260908145832")
        var fail: (() -> Void)?
        model.pendingOrderRunner = { _, failure, _ in fail = failure }
        model.processSelectedServerFolder(folder, includeHardware: true)
        require(model.orderRunning && dashboardStatusIsInProgress(model.dashboardServerStatus), "预览开始应显示运行中")
        model.orderError = "无法识别所选文件夹：" + folder.path
        fail?()
        require(!model.orderRunning && !dashboardStatusIsInProgress(model.dashboardServerStatus), "预览失败后不得继续显示运行中")
        require(model.dashboardServerStatus.contains(folder.path) && model.dashboardSyncStatus == model.dashboardServerStatus, "失败状态应保留真实错误及路径")
        require(model.dashboardActivity.first?.state == "failure" && model.dashboardActivity.first?.detail == model.dashboardServerStatus, "活动记录应显示实际失败原因")
        require(!dashboardStatusIsInProgress("⚠️ 正在读取的文件已被移除"), "错误描述含正在也不能判为运行中")
    }

    private static func testHardwareSourceSelectionFlow() {
        let model = AppModel()
        let folder = "/tmp/PP9999"
        let request: [String: Any] = ["source_folders": [folder], "include_hardware": true, "conflicts": [
            ["factory_order": "F100", "candidates": [
                ["id": "old-content", "path": folder + "/main/Fittingslist.xlsx", "items": [["name": "Hinge", "quantity": 2]]],
                ["id": "new-content", "path": folder + "/leftovers/Fittingslist.xlsx", "items": [["name": "Hinge", "quantity": 5]]]
            ]]
        ]]
        var commands: [[String]] = []
        var complete: (([String: Any]) -> Void)?
        model.pendingOrderRunner = { args, _, success in commands.append(args); complete = success }
        model.processSelectedServerFolder(URL(fileURLWithPath: folder), includeHardware: true)
        complete?(["hardware_source_selection": request])
        require(model.showHardwareSourceSelection && !model.showServerWriteConfirmation, "报表冲突必须先选择，不能进入写入确认")
        require(model.hardwareSourceChoices.isEmpty && !model.canResumeHardwareSourcePreview, "不得按名称或时间默认选择")
        model.hardwareSourceChoices["F100"] = "old-content"
        model.confirmHardwareSourceSelection()
        require(commands.count == 1, "等来源选择 Sheet 关闭后才能重试")
        model.hardwareSourceSelectionDidDismiss()
        require(commands.count == 2 && commands.last?.first == "preview-server-changes", "选择只能重新预览，不能写入")
        require(commands.last?.contains("--hardware-source-choices") == true && commands.last?.last?.contains("old-content") == true, "必须传递用户选择及内容标识")
        let payload: [String: Any] = ["write_records": [:], "source_folders": [folder], "orders": [["order_id": "PP9999"]], "hardware_source_selection": request]
        complete?(["server_write_preview": payload])
        require(model.showServerWriteConfirmation, "完成来源预览后应保留独立的写入确认")
        require(model.hardwareSourceChoices["F100"] == "old-content", "选定来源应保持到写入确认，不提供更换入口")

    }

    private static func testFolderPreviewMappingRecovery() {
        let model = AppModel()
        let folder = URL(fileURLWithPath: "/Volumes/server/Optimized Orders/PP0008")
        var fail: (() -> Void)?
        var commands: [[String]] = []
        model.pendingOrderRunner = { args, failure, _ in commands.append(args); fail = failure }
        model.processSelectedServerFolder(folder, includeHardware: false)
        model.orderError = "材料文件尚未通过校验：订单 PP0008 存在未完成商品 SKU 处理：8mm--Walnut；请先设置映射"
        fail?()
        require(model.currentIssues.isEmpty && model.showInventoryMappingWorkspace, "内存预览发现映射问题应直接打开入口，无需已保存的待处理问题")
        require(model.inventoryMappingTargetNames == ["8mm--Walnut"], "入口应列出实际缺失材料")
        model.pendingInventoryRunner = { _, _, success in success([:]) }
        model.saveInventoryMapping(travelerName: "8mm--Walnut", productCode: "TEST")
        require(commands.count == 2 && commands.last == ["preview-server-changes", "--server-folder", folder.path, "--include-hardware", "false"], "映射后只重试原文件夹预览，并保留五金选项")
        model.orderError = "未完成商品 SKU 处理：另一材料；请先设置映射"
        fail?()
        require(model.inventoryMappingTargetNames == ["另一材料"], "重试发现的新映射问题应提供处理入口")
    }

    private static func testPendingMappingCallbacks() {
        let folder = "/Volumes/server/Optimized Orders/PP0099"
        let path = folder + "/Report/material.xlsx"
        let issue = CurrentIssue(id: "mapping-99", kind: "material_validation", orderId: "PP0099", factoryOrder: "F99", path: path, message: "未完成商品 SKU 处理：A、B", firstSeen: "", lastSeen: "")
        let preview: [String: Any] = ["server_write_preview": ["write_records": [:], "source_folders": [folder], "orders": [["order_id": "PP0099"]]]]
        let model = AppModel()
        model.currentIssues = [issue]
        var commands: [[String]] = []
        var inventorySuccess: (([String: Any]) -> Void)?
        var inventoryFailure: ((String) -> Void)?
        var orderSuccess: (([String: Any]) -> Void)?
        var orderFailure: (() -> Void)?
        model.pendingInventoryRunner = { args, failure, success in
            commands.append(args); inventoryFailure = failure; inventorySuccess = success
        }
        model.pendingOrderRunner = { args, failure, success in
            commands.append(args); orderFailure = failure; orderSuccess = success
        }
        model.requestInventoryMapping(folderPath: path, message: issue.message)
        let originalID = model.pendingCenterItems[0].id
        model.saveInventoryMapping(travelerName: "A", productCode: "M1")
        inventoryFailure?("save failed")
        require(model.pendingCenterItems[0].id == originalID && model.inventoryMappingTargetNames == ["A", "B"], "保存失败不能清除原项目或剩余映射")
        let saveFailure = model.pendingMappingResumeMessage(for: model.pendingCenterItems[0])
        model.closeInventoryMappingWorkspace()
        require(!saveFailure.isEmpty && model.pendingMappingResumeStates[originalID]?.failureMessage == saveFailure, "关闭必须保留项目级保存失败")
        model.requestInventoryMapping(folderPath: path, message: issue.message)
        require(model.activePendingMappingResumeState?.failureMessage == saveFailure && model.inventoryMappingTargetNames == ["A", "B"], "重开必须恢复失败和剩余项目")
        model.saveInventoryMapping(travelerName: "A", productCode: "M1")
        inventorySuccess?([:])
        require(model.inventoryMappingTargetNames == ["B"] && commands.count == 2, "多个映射未完成前不得续跑")
        model.closeInventoryMappingWorkspace()
        model.requestInventoryMapping(folderPath: path, message: issue.message)
        require(model.inventoryMappingTargetNames == ["B"], "重开不能从旧错误消息重新引入已保存的 A")
        model.saveInventoryMapping(travelerName: "B", productCode: "M2")
        inventorySuccess?([:])
        require(commands.last == ["preview-server-changes", "--server-folder", folder, "--include-hardware", "true"], "续跑必须使用规范化原目录的内存预览")
        let count = commands.count
        model.retryPendingMappingPreview()
        require(commands.count == count, "预览进行中不得并行启动续跑")
        orderFailure?()
        require(model.pendingCenterItems[0].id == originalID && model.showInventoryMappingWorkspace, "预览失败必须保留原项目和重试入口")
        let previewFailure = model.pendingMappingResumeMessage(for: model.pendingCenterItems[0])
        model.closeInventoryMappingWorkspace()
        model.requestInventoryMapping(folderPath: path, message: issue.message)
        require(!previewFailure.isEmpty && model.inventoryMappingTargetNames.isEmpty && model.activePendingMappingResumeState?.failureMessage == previewFailure, "预览失败后重开不能重新引入已保存映射")
        model.retryPendingMappingPreview()
        orderSuccess?([:])
        require(!model.showServerWriteConfirmation, "无效预览不能呈现确认界面")
        model.retryPendingMappingPreview()
        let beforePreviewResult = commands.count
        orderSuccess?(preview)
        require(commands.count == beforePreviewResult, "预览成功后不得启动 list-index 或任何替代查询")
        require(!model.showInventoryMappingWorkspace && !model.showServerWriteConfirmation, "必须等待映射 Sheet 完成关闭")
        model.inventoryMappingWorkspaceDidDismiss()
        require(model.showServerWriteConfirmation && model.serverWritePreview?.sourceFolders == [folder], "成功后必须真正呈现原文件夹 Server 预览")
        require(model.pendingCenterItems[0].id == originalID, "预览成功不代表原问题已写入或已解决")
        require(!commands.contains { $0[0].hasPrefix("confirm-") || $0[0] == "process-server-folder" || $0[0] == "list-index" }, "自动续跑不能调用业务写入或列表协调命令")

        model.showServerWriteConfirmation = false
        model.requestInventoryMapping(folderPath: path, message: "处理：A")
        require(model.inventoryMappingTargetNames.isEmpty && model.activePendingMappingResumeState?.failureMessage == "", "成功后重开应保持已完成映射并清除旧失败")
        model.saveInventoryMapping(travelerName: "A", productCode: "M1")
        let staleSave = inventorySuccess
        model.closeInventoryMappingWorkspace()
        let beforeCancel = commands.count
        staleSave?([:])
        require(commands.count == beforeCancel && !model.showServerWriteConfirmation, "取消后的保存回调不能启动预览")
        model.requestInventoryMapping(folderPath: path, message: "处理：A")
        model.saveInventoryMapping(travelerName: "A", productCode: "M1")
        inventorySuccess?([:])
        let stalePreview = orderSuccess
        model.requestInventoryMapping(folderPath: "/Volumes/server/Other/Report/file.xlsx", message: "处理：C")
        let beforeSwitch = commands.count
        stalePreview?(preview)
        require(commands.count == beforeSwitch && model.inventoryMappingTargetNames == ["C"], "旧预览回调不得覆盖新项目")
        model.inventoryMappingWorkspaceDidDismiss()
        require(model.showInventoryMappingWorkspace && model.inventoryMappingTargetNames == ["C"], "旧 Sheet 关闭通知不得取消新请求")
        model.closeInventoryMappingWorkspace()

        // Ignoring one mapping uses the same serial continuation and preserves unsaved items.
        let ignorePath = "/Volumes/server/Ignore/Report/material.xlsx"
        model.requestInventoryMapping(folderPath: ignorePath, message: "未映射材料：A、B。请处理")
        model.saveInventoryIgnoredMapping(name: "A", reason: "test")
        inventoryFailure?("ignore failed")
        require(model.inventoryMappingTargetNames == ["A", "B"], "忽略保存失败必须保留全部映射")
        model.saveInventoryIgnoredMapping(name: "A", reason: "test")
        inventorySuccess?([:])
        require(model.inventoryMappingTargetNames == ["B"] && commands.last?.first == "ignore-item", "忽略首项后不得提前预览")
        model.closeInventoryMappingWorkspace()
        model.requestInventoryMapping(folderPath: ignorePath, message: "未映射材料：A、B。请处理")
        require(model.inventoryMappingTargetNames == ["B"], "关闭重开不能重新引入已忽略的 A")
        model.orderRunning = true
        model.saveInventoryMapping(travelerName: "B", productCode: "M2")
        inventorySuccess?([:])
        require(model.inventoryStatus.contains("订单操作进行中"), "忙碌的订单通道必须提供可恢复提示，不能静默丢弃续跑")
        model.orderRunning = false
        model.retryPendingMappingPreview()
        let staleResult = orderSuccess
        model.closeInventoryMappingWorkspace()
        staleResult?(preview)
        model.inventoryMappingWorkspaceDidDismiss()
        require(!model.showServerWriteConfirmation && model.pendingCenterItems[0].id == originalID, "预览期间取消不能呈现预览或移除待处理项目")

        let latePath = "/Volumes/server/Late/Report/material.xlsx"
        model.requestInventoryMapping(folderPath: latePath, message: "处理：Late")
        model.saveInventoryMapping(travelerName: "Late", productCode: "M3")
        model.closeInventoryMappingWorkspace()
        let beforeLateSave = commands.count
        inventorySuccess?([:])
        model.requestInventoryMapping(folderPath: latePath, message: "处理：Late")
        require(model.inventoryMappingTargetNames.isEmpty && commands.count == beforeLateSave, "关闭后完成的保存必须记住，不能自动续跑或重新引入材料")
        model.closeInventoryMappingWorkspace()
    }

    private static func testPendingMappingMergesFolderIssues() {
        let folder = "/Volumes/server/Optimized Orders/PP0100"
        let pathA = folder + "/Report/a.xlsx"
        let pathB = folder + "/Report/b.xlsx"
        let model = AppModel()
        model.pendingServerChanges = [ServerChangePreview(id: "folder-100", changeType: "modified", kind: "folder", orderId: "PP0100", sourceFolder: folder, path: folder, message: "changed", manualOnly: false, eventTime: "")]
        model.currentIssues = [pathA, pathB].enumerated().map { index, path in
            CurrentIssue(id: "issue-\(index)", kind: "material_mapping", orderId: "PP0100", factoryOrder: "", path: path, message: "处理：\(index == 0 ? "A" : "B")", firstSeen: "", lastSeen: "")
        }
        model.pendingInventoryRunner = { _, _, success in success([:]) }
        model.pendingOrderRunner = { _, failure, _ in failure() }
        let item = model.pendingCenterItems[0]
        require(model.pendingCenterItems.count == 1, "测试必须为同一文件夹合并的两个问题")
        model.requestInventoryMapping(folderPath: pathA, message: "处理：A")
        model.saveInventoryMapping(travelerName: "A", productCode: "M1")
        model.closeInventoryMappingWorkspace()
        model.requestInventoryMapping(folderPath: pathB, message: "处理：B")
        require(model.inventoryMappingTargetNames == ["B"], "同文件夹第二问题的 B 不能被首个问题缓存隐藏")
        model.closeInventoryMappingWorkspace()
        model.requestInventoryMapping(folderPath: pathA, message: "处理：a、B、C")
        require(model.inventoryMappingTargetNames == ["B", "C"], "重开必须合并新 C，去重 B，并排除已保存 A 的大小写变体")
        require(model.pendingMappingResumeState(for: item)?.completedNames == ["A"], "已完成集合必须独立于剩余列表保存")
        model.saveInventoryIgnoredMapping(name: "B", reason: "test")
        model.closeInventoryMappingWorkspace()
        model.requestInventoryMapping(folderPath: pathB, message: "处理：A、B、C、D")
        require(model.inventoryMappingTargetNames == ["C", "D"], "已忽略 B 不能复活；尚未见过的 D 必须出现")
        model.closeInventoryMappingWorkspace()
    }

    private static func testOrderOutboundFactorySelection() {
        require(orderDashboardFactorySelectionColumnWidth >= 48, "工厂单选择框列宽过窄")
        let first = toggledOrderFactorySelection([], factoryOrder: "F100")
        let both = toggledOrderFactorySelection(first, factoryOrder: "F200")
        let removed = toggledOrderFactorySelection(both, factoryOrder: "F100")
        require(first == Set(["F100"]), "首次点击工厂单应建立选择")
        require(both == Set(["F100", "F200"]), "工厂单应支持多选")
        require(removed == Set(["F200"]), "再次点击已选工厂单应取消选择")
        let factories = [
            OrderFactoryPreview(id: "F100", factoryOrder: "F100", orderName: "PP0099-KITCHEN"),
            OrderFactoryPreview(id: "F200", factoryOrder: "F200", orderName: "PP0099-OFFICE"),
        ]
        require(
            selectedOrderFactoryNames(factories, selected: both) == ["PP0099-KITCHEN", "PP0099-OFFICE"],
            "出库上下文应传入所选工厂单名称"
        )
        require(
            orderDashboardHasShippedSelection(["F100"], statuses: ["F100": "已出库", "F200": "需要更新"]),
            "已出库工厂单必须阻止再次出库"
        )
        require(
            orderDashboardOutboundDisplay(status: "已出库", documentNumber: "QTCK20260729007") == "已出库 · QTCK20260729007",
            "已出库工厂单没有显示出库单据编号"
        )
        require(
            orderDashboardOutboundDisplay(status: "需要更新", documentNumber: "QTCK-OLD") == "需要更新",
            "未出库状态不应错误显示历史出库单据编号"
        )
        require(
            !orderDashboardHasShippedSelection(["F200"], statuses: ["F100": "已出库", "F200": "需要更新"]),
            "历史状态工厂单应允许进入出货"
        )
        require(
            orderDashboardNeedsOutboundUpdateSelection(["F200"], statuses: ["F100": "已出库", "F200": "需要更新"]),
            "历史状态工厂单应保留状态识别"
        )
        require(
            orderDashboardOutboundActionTitle(["F200"], statuses: ["F100": "已出库", "F200": "需要更新"]) == "出货",
            "出货按钮应统一显示出货"
        )
        require(
            orderDashboardOutboundActionTitle(["F100"], statuses: ["F100": "已出库", "F200": "需要更新"]) == "出货",
            "出货按钮应统一显示出货"
        )
        require(
            !orderDashboardStageMatchesFilter("已出货", statusFilter: "未完成订单")
                && orderDashboardStageMatchesFilter("已出货", statusFilter: "已出货")
                && orderDashboardStageMatchesFilter("已优化", statusFilter: "未完成订单"),
            "订单中心默认列表没有隐藏已完成订单，或状态筛选无法查看已出货订单"
        )
    }

    private static func testProductionFeedbackAndDashboardProgress() {
        let root = URL(fileURLWithPath: FileManager.default.currentDirectoryPath)
        let dashboard = try! String(
            contentsOf: root.appendingPathComponent("macos/OrderDashboardView.swift"),
            encoding: .utf8
        )
        let assistant = try! String(
            contentsOf: root.appendingPathComponent("macos/TravelerAssistant.swift"),
            encoding: .utf8
        )
        require(
            dashboard.contains("let panelMaterialHoverDelay: TimeInterval = 1.0"),
            "Panel 图片悬停延迟没有固定为 1 秒"
        )
        require(
            dashboard.contains("DispatchQueue.main.asyncAfter(deadline: .now() + panelMaterialHoverDelay)"),
            "Panel 图片没有使用延迟悬停触发"
        )
        require(
            dashboard.contains("operationState == .success ? \"完成\" : \"关闭\"") &&
                dashboard.contains("Button(\"重试\")") &&
                dashboard.contains("productionOperationBanner"),
            "生产弹窗没有保留成功/失败/重试结果提示"
        )
        require(
            assistant.contains("struct ProductionOperationResult") &&
                assistant.contains("本地生产记录已保存") &&
                assistant.contains("state: uncertain ? .uncertain : .failure"),
            "生产操作没有向弹窗返回完整结果状态"
        )
        require(
            dashboard.contains("accessibilityTitle: \"出货进度\"") &&
                dashboard.contains("completed: item.shippedCount"),
            "订单行出货进度没有使用与优化进度相同的进度条格式"
        )
        require(
            dashboard.contains("tableHeader(\"生产进度\", width: layout.flexibleColumnWidth)") &&
                dashboard.contains("accessibilityTitle: \"生产进度\"") &&
                dashboard.contains("completed: item.producedCount") &&
                dashboard.contains("Text(item.productionProgress)"),
            "订单行没有使用生产完成数显示生产进度列"
        )
        let materialHeader = dashboard.range(of: "tableHeader(\"材料\", width: layout.flexibleColumnWidth)")
        let optimizationHeader = dashboard.range(of: "tableHeader(\"优化进度\", width: layout.flexibleColumnWidth)")
        require(
            materialHeader != nil && optimizationHeader != nil && materialHeader!.lowerBound < optimizationHeader!.lowerBound,
            "材料列应显示在优化进度列前面"
        )
        require(
            dashboard.contains("remainingQuantity <= 0"),
            "生产弹窗没有禁用零剩余材料输入框"
        )
        require(
            dashboard.contains("HStack(alignment: .center, spacing: 10)") &&
                dashboard.contains("HStack(alignment: .center, spacing: 12)") &&
                dashboard.contains(".lineLimit(1)") &&
                dashboard.contains(".fixedSize(horizontal: true, vertical: false)") &&
                dashboard.contains(".padding(.trailing, 64)"),
            "Panel颜色标题和颜色值没有使用紧凑的右侧安全布局"
        )
        require(
            dashboard.contains("Button(\"确认生产并扣减材料\")") &&
                !dashboard.contains("Button(\"确认生产并出库\")"),
            "生产按钮没有明确区分材料扣减与工厂单出货"
        )
        require(
            assistant.contains("已读取 \\(materials.count) 项订单材料") &&
                assistant.contains("其中 \\(availableCount) 项有待分配数量") &&
                !assistant.contains("已读取 (materials.count) 项订单材料"),
            "生产弹窗材料数量没有显示真实总项数和可分配项数"
        )
        require(
            dashboard.contains(".frame(width: 620, height: 560)") &&
                dashboard.contains("Text(\"类型\")") &&
                dashboard.contains("Text(\"材料名\")") &&
                dashboard.contains("Text(\"单位\")") &&
                dashboard.contains("Text(\"剩余\")") &&
                dashboard.contains("Text(\"数量\")") &&
                assistant.contains("sortedProductionMaterialDrafts"),
            "生产弹窗没有显示材料表头或按业务顺序排序"
        )
        require(
            assistant.contains("static func aggregated(_ changes: [ServerWriteMaterialChange])") &&
                assistant.contains("Server 材料写入完成") &&
                assistant.contains("duration: duration") &&
                !assistant.contains("self.showServerWriteConfirmation = false\n            self.refreshDashboardAfterServerWrite()") &&
                assistant.contains("订单中心、助手和待处理中心已刷新") &&
                !assistant.contains("订单列表已刷新；正在刷新待处理中心…\"\n            self.scanDashboardServer(background: true, presentIfNeeded: false)"),
            "Server 确认写入没有汇总材料、保留成功提示、记录耗时或取消写入后的自动扫描"
        )
        require(
            dashboard.contains("invalidOrderValidations") &&
                dashboard.contains("订单校验未通过") &&
                dashboard.contains("禁止确认写入") &&
                dashboard.contains("!invalidOrderValidations.isEmpty"),
            "Server 预览没有显示订单校验结果或阻止异常订单确认写入"
        )
    }

    private static func testInventoryTravelerNewestFirst() {
        let rows = [
            traveler("old-a", folder: "PP0001", modifiedAt: "2026-07-01T10:00:00"),
            traveler("new-a", folder: "PP0001", modifiedAt: "2026-07-03T10:00:00"),
            traveler("newest", folder: "PP0002", modifiedAt: "2026-07-04T10:00:00"),
            traveler("old-b", folder: "PP0002", modifiedAt: "2026-07-02T10:00:00"),
        ]
        let grouped = groupInventoryTravelersByNewest(rows)
        require(grouped.map(\.0) == ["PP0002", "PP0001"], "Traveler 文件夹未按最新文件时间降序")
        require(grouped[0].1.map(\.fileName) == ["newest", "old-b"], "PP0002 内文件未按时间降序")
        require(grouped[1].1.map(\.fileName) == ["new-a", "old-a"], "PP0001 内文件未按时间降序")
    }

    private static func testSharedPageHeaderHeight() {
        let headers = [
            AnyView(AppPageHeader(systemImage: "folder", title: "生产文件", subtitle: "测试") {
                Button("刷新") {}
            }),
            AnyView(AppPageHeader(systemImage: "shippingbox", title: "出库", subtitle: "测试") {
                Text("商品资料")
                Button("更新") {}
                Button("刷新") {}
            }),
            AnyView(AppPageHeader(systemImage: "checkmark.square", title: "待办事项", subtitle: "测试") {
                Label("1 项未完成", systemImage: "circle.dashed")
            }),
            AnyView(AppPageHeader(systemImage: "gearshape", title: "设置", subtitle: "测试") {
                EmptyView()
            }),
        ]
        for header in headers {
            let hosting = NSHostingView(rootView: header.frame(width: AppLayout.windowMinWidth))
            hosting.layoutSubtreeIfNeeded()
            require(hosting.fittingSize.height <= 0.5, "底部重复页头未移除：\(hosting.fittingSize.height)")
        }
    }

    private static func testAssistantOrderTimelineContract() {
        let assistantSource = try! String(
            contentsOfFile: "macos/AssistantView.swift",
            encoding: .utf8
        )
        require(
            assistantSource.contains("assistantProgressRail")
                && assistantSource.contains("assistantStageIcon")
                && assistantSource.contains("OrderDashboardClickContainer(")
                && assistantSource.contains("onDoubleClick: { openOrderCenter(item.orderId) }")
                && assistantSource.contains(".symbolEffect(.rotate")
                && assistantSource.contains("ProgressView()")
                && assistantSource.contains("static let metricValue: CGFloat = 40")
                && assistantSource.contains("static let orderID: CGFloat = 20")
                && assistantSource.contains("static let stageValue: CGFloat = 13")
                && assistantSource.contains("GeometryReader")
                && assistantSource.contains("completedCount: Int")
                && assistantSource.contains("totalCount: Int")
                && assistantSource.contains("let allStagesComplete = stages.allSatisfy")
                && assistantSource.contains("let firstIncompleteIndex = stages.firstIndex")
                && assistantSource.contains("let segmentState")
                && assistantSource.contains("leadingStubLength")
                && assistantSource.contains("segmentMidpoint")
                && assistantSource.contains("index < firstIncompleteIndex")
                && assistantSource.contains("let iconColor = completed ? AssistantDashboardTypography.stageEmerald : Color.secondary.opacity(0.62)")
                && assistantSource.contains("GlassEffectContainer(spacing: 20)")
                && assistantSource.contains(".regular.tint(AssistantDashboardTypography.stageEmerald.opacity(0.28))")
                && assistantSource.contains(".regular.tint(AppPalette.separator.opacity(0.18))")
                && assistantSource.contains("assistantProgressValue(item.outboundProgress), \"truck.box.fill\"")
                && assistantSource.contains("item.factoryCount > 0 ? \"\\(item.factoryCount)/\\(item.factoryCount)\" : \"—\", \"arrow.triangle.branch\"")
                && assistantSource.contains("assistantProgressValue(item.optimizationProgress), \"square.stack\"")
                && assistantSource.contains("assistantProgressValue(item.productionProgress), \"scissors\"")
                && assistantSource.contains("Image(systemName: fallbackSymbol)")
                && assistantSource.contains("AssistantDashboardTypography.stageEmerald.opacity(0.92)")
                && assistantSource.contains(".contentTransition(.symbolEffect(.replace))")
                && assistantSource.contains("assistantProgressValue")
                && assistantSource.contains("Text(stage.title)")
                && assistantSource.contains("Text(stage.value)")
                && assistantSource.contains("centerY - 20")
                && assistantSource.contains("centerY + 20")
                && assistantSource.contains(".font(.system(size: 34, weight: .semibold))")
                && assistantSource.contains(".frame(width: 64, height: 64)")
                && assistantSource.contains("let centerY: CGFloat = 50")
                && assistantSource.contains(".frame(width: columnWidth, height: 100, alignment: .center)")
                && assistantSource.contains("assistantProgressRail(item)\n                    .padding(.leading, 80)")
                && assistantSource.contains(".frame(height: 100)")
                && assistantSource.contains("let leadingStubLength: CGFloat = 64")
                && assistantSource.contains("let stageStep: CGFloat = 10")
                && assistantSource.contains("let baseCenterX =")
                && assistantSource.contains("let stageShift = CGFloat(index + 1) * stageStep")
                && assistantSource.contains("let centerX = baseCenterX + stageShift")
                && assistantSource.contains(".offset(x: stageShift)")
                && assistantSource.contains("AppPalette.separator.opacity(0.82)")
                && assistantSource.contains("AppPalette.separator.opacity(0.90)")
                && assistantSource.contains("TimelineView(.animation(minimumInterval: 1.0 / 20.0")
                && assistantSource.contains("dashPhase: dashPhase")
                && assistantSource.contains("accessibilityReduceMotion")
                && assistantSource.contains("lineWidth: 9")
                && assistantSource.contains("assistantStageIcon")
                && assistantSource.contains("stageEmerald")
                && assistantSource.contains("LinearGradient(")
                && assistantSource.contains("RadialGradient(")
                && assistantSource.contains("Color.white.opacity(0.55)")
                && !assistantSource.contains(".offset(x: 22, y: 22)")
                && !assistantSource.contains("阻塞")
                && !assistantSource.contains("blocked")
                && assistantSource.contains("ScrollView(.vertical)")
                && !assistantSource.contains("assistantOrderStatusBadge")
                && !assistantSource.contains("双击订单行进入订单中心")
                && !assistantSource.contains("订单中心查看"),
            "助手看板必须使用图标和连接线显示状态，并保持统一的完成色、数字列与局部滚动"
        )
        require(
            assistantSource.contains("beginCommandHintsAnchorHover")
                && assistantSource.contains("beginCommandHintsPanelHover")
                && assistantSource.contains("dashboardMessageHoverDelay")
                && assistantSource.contains("dashboardMessageHoverCloseGrace")
                && !assistantSource.contains("Task.sleep(for: .milliseconds(220))"),
            "助手命令提示框必须与订单中心统一悬停显示和关闭保留时序"
        )
        if let railStart = assistantSource.range(of: "private func assistantProgressRail"),
           let railEnd = assistantSource.range(of: "private func assistantStageIcon", range: railStart.upperBound..<assistantSource.endIndex) {
            let railSource = String(assistantSource[railStart.lowerBound..<railEnd.lowerBound])
            let titlePosition = railSource.range(of: "Text(stage.title)")?.lowerBound
            let valuePosition = railSource.range(of: "Text(stage.value)")?.lowerBound
            require(
                titlePosition != nil && valuePosition != nil && titlePosition! < valuePosition!,
                "助手看板阶段名称和数值必须绑定在线段上下"
            )
            require(
                !railSource.contains("completedSegment")
                    && !railSource.contains("stages[index].1 && stages[index + 1].1"),
                "助手看板连接线不能再按相邻图标共同完成决定颜色"
            )
        } else {
            require(false, "未找到助手看板进度轨道源码")
        }
        guard
            let commandStart = assistantSource.range(of: "private var commandStrip: some View"),
            let boardStart = assistantSource.range(of: "private var orderStatusBoard: some View"),
            let metricStart = assistantSource.range(of: "private func assistantMetric", range: boardStart.upperBound..<assistantSource.endIndex)
        else {
            require(false, "未找到助手输入、当前操作或订单总览卡片")
            return
        }
        let commandCardSource = String(assistantSource[commandStart.lowerBound..<boardStart.lowerBound])
        let orderBoardSource = String(assistantSource[boardStart.lowerBound..<metricStart.lowerBound])
        require(
            commandCardSource.contains("AppSurfaceCard(padding: 0)")
                && commandCardSource.contains("currentOperationSummary")
                && orderBoardSource.contains("assistantMetric(\"总订单数\"")
                && orderBoardSource.contains("ForEach(ongoingOrders)")
                && assistantSource.contains("orderStatusBoard\n                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)")
                && assistantSource.contains(".frame(maxHeight: .infinity)")
                && !orderBoardSource.contains("currentOperationSummary"),
            "助手输入与当前操作应共用一张卡片，订单总览与订单行应共用另一张卡片"
        )
        require(
            assistantSource.contains("assistantMetric(\"总订单数\", value: effectiveOrders.count, symbol:")
                && !assistantSource.contains("Text(\"当前订单\")")
                && !assistantSource.contains("未完成订单 · 以图标和颜色显示各状态数据")
                && assistantSource.contains("Image(systemName: \"doc.text\")")
                && assistantSource.contains(".frame(width: 172, height: 42, alignment: .center)")
                && assistantSource.contains(".padding(.leading, 10)")
                && assistantSource.contains(".padding(.horizontal, 34)")
                && assistantSource.contains("orderIdentityText = Color(red: 0.08, green: 0.36, blue: 0.20)")
                && assistantSource.contains(".background(AppPalette.success.opacity(0.10), in: Capsule())")
                && assistantSource.contains(".glassEffect(.regular.tint(AppPalette.success.opacity(0.12)), in: Capsule())"),
            "助手看板未按要求居中并右移淡绿色订单身份牌"
        )
        let dashboardSource = try! String(
            contentsOfFile: "macos/OrderDashboardView.swift",
            encoding: .utf8
        )
        require(
            dashboardSource.contains("private let orderDashboardDataHeaderOffset: CGFloat = 2"),
            "订单中心从订单到出货进度的标题行必须向左微调"
        )
        require(
            dashboardSource.contains("orderInstallationDateButtonWidth")
                && dashboardSource.contains("UnevenRoundedRectangle")
                && dashboardSource.contains(".clipShape(RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius")
                && dashboardSource.contains(".mask(RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius")
                && dashboardSource.contains("Array(filteredOrders.enumerated())")
                && dashboardSource.contains("isLastRow && !isExpanded ? AppLayout.cardCornerRadius : 0")
                && dashboardSource.contains("Menu {"),
            "订单中心的日期、表格圆角和状态菜单布局没有统一"
        )

        let appSource = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        require(
            !appSource.contains("liquidGlassPreview")
                && !appSource.contains("LiquidGlassPreviewView"),
            "玻璃预览入口或路由仍残留在正式 App"
        )
    }

    private static func testAssistantStageIconAssets() {
        let assistantSource = try! String(
            contentsOfFile: "macos/AssistantView.swift",
            encoding: .utf8
        )
        require(
            assistantSource.contains("fallbackSymbol: String")
                && assistantSource.contains("Image(systemName: fallbackSymbol)")
                && !assistantSource.contains("status-icon-split.png")
                && !assistantSource.contains("status-icon-optimization.png")
                && !assistantSource.contains("status-icon-production.png"),
            "助手状态图标必须使用已选方案的原生线性符号，并清理旧的附件图标映射"
        )
    }

    private static func testGlassDatePickerContract() {
        let appSource = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        let dashboardSource = try! String(
            contentsOfFile: "macos/OrderDashboardView.swift",
            encoding: .utf8
        )
        let buildSource = try! String(
            contentsOfFile: "scripts/build-app",
            encoding: .utf8
        )
        let uiTestSource = try! String(
            contentsOfFile: "scripts/test-macos-ui",
            encoding: .utf8
        )

        require(
            dashboardSource.contains("struct AppGlassDatePickerCalendar: View")
                && dashboardSource.contains("private let weekdays = [\"日\", \"一\", \"二\", \"三\", \"四\", \"五\", \"六\"]")
                && dashboardSource.contains("ForEach(gridDates, id: \\.self)")
                && dashboardSource.contains("isDateInToday")
                && dashboardSource.contains("appGlassDatePickerPopoverSurface")
                && dashboardSource.contains(".presentationBackground(.clear)")
                && dashboardSource.contains("AppGlassDatePickerCalendar(selection: $day.date, compact: true)")
                && appSource.contains("AppGlassDatePickerCalendar(selection: $model.initialDate)")
                && appSource.contains("AppGlassDatePickerCalendar(selection: $selection)")
                && appSource.contains("displayedComponents: [.hourAndMinute]")
                && !dashboardSource.contains("AppGraphicalDatePicker")
                && !appSource.contains("AppGraphicalDatePicker"),
            "设置、订单安排和待办日期必须统一使用自定义玻璃月历，时间输入仍单独保留"
        )
        require(
            !appSource.contains("case datePreview")
                && !appSource.contains("DatePickerStylePreviewView")
                && !buildSource.contains("DatePickerStylePreviewView.swift")
                && !uiTestSource.contains("DatePickerStylePreviewView.swift"),
            "正式采用玻璃月历后必须移除临时日期预览入口和构建目标"
        )

        _ = AppGlassDatePickerCalendar(selection: .constant(Date()))
    }

    private static func testTodoTableHeaderRoundedCorners() {
        let source = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        guard
            let headerStart = source.range(of: "Text(\"截止时间\")"),
            let rowsStart = source.range(of: "if sortedItems.isEmpty", range: headerStart.upperBound..<source.endIndex)
        else {
            require(false, "未找到待办列表表头源码")
            return
        }
        let headerSource = String(source[headerStart.lowerBound..<rowsStart.lowerBound])
        require(
            headerSource.contains("UnevenRoundedRectangle(")
                && headerSource.contains("topLeading: AppLayout.cardCornerRadius")
                && headerSource.contains("bottomLeading: 0")
                && headerSource.contains("bottomTrailing: 0")
                && headerSource.contains("topTrailing: AppLayout.cardCornerRadius"),
            "待办列表表头必须显示顶部圆角，并保持与列表连接处为直角"
        )
    }

    private static func testSettingsDefaultWindowLayoutContract() {
        let source = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        guard
            let settingsStart = source.range(of: "struct SettingsView: View"),
            let settingsEnd = source.range(
                of: "struct InventoryIgnoredMappingsSheet: View",
                range: settingsStart.upperBound..<source.endIndex
            )
        else {
            require(false, "未找到设置页面源码")
            return
        }
        let settingsSource = String(source[settingsStart.lowerBound..<settingsEnd.lowerBound])
        require(
            !settingsSource.contains("ScrollView {")
                && !settingsSource.contains("GeometryReader { geometry in")
                && settingsSource.contains("SettingsCard(title: \"运行与文件\"")
                && settingsSource.contains("SettingsCard(title: \"系统账户\"")
                && settingsSource.contains("SettingsCard(title: \"库存资料与规则\"")
                && settingsSource.contains("SettingsCard(title: \"备份与日志\"")
                && settingsSource.contains(".frame(minHeight: AppLayout.settingsTopRowMinHeight)")
                && settingsSource.contains(".frame(minHeight: AppLayout.settingsBottomRowMinHeight)")
                && settingsSource.contains("showInitialDatePicker")
                && settingsSource.contains("settingsDateDisplay(model.initialDate)")
                && settingsSource.contains(".frame(width: 168, height: 30, alignment: .leading)")
                && settingsSource.contains("AppGlassDatePickerCalendar(selection: $model.initialDate)")
                && settingsSource.contains(".frame(height: 56)"),
            "设置页面必须使用紧凑布局，并通过宽日期按钮和玻璃月历完整显示初始扫描日期"
        )
        require(
            !settingsSource.contains("Button(\"待确认记录\")")
                && settingsSource.contains("showManualMappingList = true"),
            "设置页面不应显示待确认记录按钮，但应保留其他查看入口"
        )
        require(
            settingsSource.contains("initialDate")
                && settingsSource.contains("sourceRoot")
                && settingsSource.contains("orderRoot")
                && settingsSource.contains("backupRoot")
                && settingsSource.contains("jdyUsername")
                && settingsSource.contains("aimesUsername")
                && settingsSource.contains("updateInventoryCatalog")
                && settingsSource.contains("showManualMappingList = true")
                && settingsSource.contains("showIgnoredHardwareList = true")
                && settingsSource.contains("performBackup")
                && settingsSource.contains("operationLogEnabled")
                && settingsSource.contains("saveAllSettings"),
            "设置页面重新分组后遗漏了原有配置或维护入口"
        )
        require(
            !settingsSource.contains("程序只在你手工点击运行后执行。")
                && !settingsSource.contains("从库存系统更新商品名称、SKU、规格、类别和单位等资料。")
                && !settingsSource.contains("App 每天首次启动时，在本地订单缓存读取完成后自动备份")
                && !settingsSource.contains("用于发生错误时按时间顺序回溯。"),
            "设置页面仍保留会挤占默认窗口空间的长说明文字"
        )
        require(
            source.contains("static let todoDeadlineDatePickerWidth: CGFloat = 226")
                && source.contains("static let todoDeadlineDatePickerHeight: CGFloat = 30")
                && source.contains("static let todoDeadlineTimeCardWidth: CGFloat = 300")
                && source.contains("static let todoDeadlineTimePickerWidth: CGFloat = 224")
                && source.contains("static let todoDeadlineTimePickerTrailingInset: CGFloat = 10")
                && source.contains("width: AppLayout.todoDeadlineTimePickerWidth,")
                && source.contains("height: AppLayout.todoDeadlineTimePickerHeight,")
                && source.contains("alignment: .trailing")
                && source.contains(".fixedSize(horizontal: true, vertical: false)")
                && source.contains(".padding(.trailing, AppLayout.todoDeadlineTimePickerTrailingInset)")
                && source.contains(".frame(width: AppLayout.todoDeadlineTimeCardWidth, height: 44)")
                && source.components(separatedBy: "TodoDeadlinePickerControl(selection:").count == 3
                && source.contains("dateFormat = \"yyyy年M月d日 HH:mm\"")
                && source.contains("AppGlassDatePickerCalendar(selection: $selection)")
                && source.contains("displayedComponents: [.hourAndMinute]"),
            "待办新增和编辑界面没有统一使用中文玻璃日期时间控件"
        )
        require(
            source.contains("func loadSettings() -> Bool")
                && source.contains("var passwordResults: [String] = []")
                && source.contains("常规设置和已填写的钥匙串密码均已保存。")
                && settingsSource.contains("库存规则由各自按钮单独保存。")
                && settingsSource.components(separatedBy: "SecureField(\"用户名\"").count == 3
                && !settingsSource.contains("TextField(\"用户名\"")
                && !source.contains("Label(\"重新载入\"")
                && !source.contains("放弃页面中尚未保存的常规设置"),
            "设置页没有移除重新载入按钮、掩码账号字段或保留准确的保存范围"
        )
    }

    private static func testFixedWindowSizeContract() {
        let source = try! String(
            contentsOfFile: "macos/TravelerAssistant.swift",
            encoding: .utf8
        )
        require(
            AppLayout.windowMinWidth == 1120
                && AppLayout.windowIdealWidth == 1120
                && AppLayout.windowMinHeight == 768
                && AppLayout.windowIdealHeight == 768,
            "PP FlowHub 默认窗口必须固定为 1120×768"
        )
        require(
            source.contains(".windowResizability(.contentSize)")
                && source.contains("window.styleMask.remove([.resizable, .fullScreen])")
                && source.contains("window.minSize = fixedFrame.size")
                && source.contains("window.maxSize = fixedFrame.size"),
            "PP FlowHub 窗口必须禁止用户调整大小"
        )
    }

    private static func testInventoryActionLayoutRules() {
        require(AppLayout.inventoryActionMinWidth >= 128, "库存按钮最小宽度过窄")
        require(AppLayout.actionSpacing == 10, "库存按钮间距未统一")
        require(AppLayout.inventoryOrderContextWidth == 735, "上下文出库窗口宽度未缩小到 735pt")
        require(
            AppLayout.inventoryOrderContextWidth - AppLayout.contentPadding * 2 >= 4 * 156 + 3 * AppLayout.actionSpacing,
            "735pt 出库窗口不足以让四个操作按钮保持一排"
        )
        require(
            inventoryActionColumnCount(availableWidth: 420) >= 2,
            "库存操作区在常规宽度下未能并排按钮"
        )
        require(
            inventoryActionColumnCount(availableWidth: AppLayout.inventoryActionMinWidth) == 1,
            "库存操作区在窄窗口下未换行为单列"
        )
        func preview(_ name: String, _ section: String) -> InventoryPreviewRow {
            InventoryPreviewRow(
                travelerName: name,
                productCode: "M0001",
                productName: name,
                quantity: 1,
                source: "测试",
                status: "已映射",
                section: section
            )
        }
        let sorted = sortedInventoryPreviewRows([
            preview("Hinge", "五金"),
            preview("Edge banding--Basalto SM", "板材与封边"),
            preview("14.5mm--Plywood", "板材与封边"),
            preview("19.1mm--Basalto SM", "板材与封边"),
            preview("5.4mm--Plywood", "板材与封边"),
            preview("18mm--Plywood", "板材与封边")
        ])
        require(
            sorted.map(\.travelerName) == [
                "18mm--Plywood", "14.5mm--Plywood", "5.4mm--Plywood",
                "19.1mm--Basalto SM", "Edge banding--Basalto SM", "Hinge"
            ],
            "出库预览没有按 Plywood、Panel、封边条、五金及 Plywood 子分类排序"
        )
        _ = InventoryView(model: AppModel(), onClose: {}, orderContextID: "PP0001")
    }

    private static func testRunningProgressReusesOperationRow() {
        let id = UUID()
        let steps = [
            InventoryStep(id: id, time: "12:00:00", title: "查询实时库存", detail: "任务已开始", state: "running")
        ]
        guard let updated = updatingLatestRunningStep(steps, detail: "正在后台连接库存系统") else {
            fail("后台进度没有找到正在执行的操作行")
        }
        require(updated.count == 1, "后台进度不应新增重复操作行")
        require(updated[0].id == id, "后台进度更新不应更换操作行标识")
        require(updated[0].state == "running", "后台进度不应被标记为成功")
        require(updated[0].detail == "正在后台连接库存系统", "后台进度文案未更新")
    }

    private static func testDashboardInventoryProgressText() {
        require(
            dashboardInventoryProgressText("[+47.75s] 库存系统：正在填写 1/2：M1001") == "正在填写 1/2：M1001",
            "库存进度标题没有去掉耗时和库存系统前缀"
        )
        require(
            dashboardInventoryProgressText("[+49.48s] 库存系统：已填写商品 M1001，数量 16") == "正在处理：已填写商品 M1001，数量 16",
            "已完成的库存阶段没有转成当前处理中提示"
        )
        let messages = dashboardMessages(
            syncStatus: "正在填写 1/2：M1001",
            syncTime: "12:00:01",
            aimesStatus: "AIMES 尚未检查",
            aimesTime: "12:00:02",
            serverStatus: "Server 尚未扫描",
            serverTime: "12:00:03",
            activity: []
        )
        let current = dashboardCurrentOperation(messages: messages, isRunning: true)
        require(current?.isRunning == true && current?.message.detail == "正在填写 1/2：M1001", "库存当前步骤没有进入订单中心标题行")
    }

    private static func testInventoryProgressKeepsStageHistory() {
        let steps = [
            InventoryStep(time: "12:00:00", title: "库存操作", detail: "任务已开始", state: "running")
        ]
        let updated = appendingInventoryProgressStep(steps, message: "登录页面：实际耗时 2.00 秒")
        require(updated.count == 2, "库存分阶段进度不应覆盖上一条记录")
        require(updated[0].state == "success", "上一阶段完成后应保留为已完成")
        require(updated[1].state == "running", "最新库存阶段应保持执行中")
        require(updated[1].detail.contains("实际耗时"), "库存阶段应显示实际耗时")
    }

    private static func testDashboardSeparatesInventoryAndRefreshTiming() {
        let messages = dashboardMessages(
            syncStatus: "✅ 订单列表已刷新",
            syncTime: "12:00:02",
            inventoryStatus: "✅ PP0070 出货已完成",
            inventoryTime: "12:00:01",
            aimesStatus: "AIMES 尚未检查",
            aimesTime: "12:00:00",
            serverStatus: "Server 尚未扫描",
            serverTime: "12:00:00",
            activity: [],
            durationsBySource: ["inventory": 69.23, "sync": 0.61]
        )
        let shipment = messages.first(where: { $0.source == "inventory" })
        let refresh = messages.first(where: { $0.source == "sync" })
        require(shipment?.duration == 69.23, "出货耗时被列表刷新覆盖")
        require(refresh?.duration == 0.61, "订单列表刷新耗时错误")
        let latest = dashboardCurrentOperation(messages: messages, isRunning: false)
        require(latest?.message.source == "sync", "最近结果应显示最后完成的列表刷新")
        require(
            dashboardMessageSummaryText(latest!.message).contains("订单列表已刷新")
                && dashboardMessageSummaryText(latest!.message).contains("0.61 秒"),
            "列表刷新结果不应再冒充出货总耗时"
        )
    }

    private static func testOrderOperationDurationFormatting() {
        require(operationDurationText(1.236) == "1.24 秒", "操作用时没有按最多两位小数显示")
        require(operationDurationText(2) == "2.00 秒", "整秒操作用时格式错误")
    }

    private static func testServerWriteMaterialPreviewOrdering() {
        let changes = [
            ServerWriteMaterialChange(id: "edge", changeType: "新增", materialType: "edge", color: "Rosales 3", thickness: "", edge: "", unit: "m", oldQuantity: 0, newQuantity: 185, delta: 185),
            ServerWriteMaterialChange(id: "panel", changeType: "新增", materialType: "panel", color: "Rosales 3", thickness: "19.1", edge: "", unit: "pcs", oldQuantity: 0, newQuantity: 5, delta: 5),
            ServerWriteMaterialChange(id: "plywood-5.4", changeType: "新增", materialType: "plywood", color: "", thickness: "5.4", edge: "", unit: "pcs", oldQuantity: 0, newQuantity: 3, delta: 3),
            ServerWriteMaterialChange(id: "plywood-14.5", changeType: "新增", materialType: "plywood", color: "", thickness: "14.5", edge: "", unit: "pcs", oldQuantity: 0, newQuantity: 1, delta: 1),
            ServerWriteMaterialChange(id: "plywood-18", changeType: "新增", materialType: "plywood", color: "", thickness: "18", edge: "", unit: "pcs", oldQuantity: 0, newQuantity: 9, delta: 9),
        ]
        let ordered = sortedServerWriteMaterialChanges(changes)
        require(
            ordered.map { "\($0.materialType)-\($0.thickness)" } == [
                "plywood-18", "plywood-14.5", "plywood-5.4", "panel-19.1", "edge-"
            ],
            "Server 材料预览没有按 18mm、14.5mm、5.4mm、Panel、封边顺序显示"
        )
    }

    private static func testServerWriteHardwareChangeLayout() {
        require(serverHardwareUnitText("Piece") == "Piece", "五金单位已有值时不应被替换")
        require(serverHardwareUnitText("  ") == "—", "五金单位缺失时应显示占位符")
        require(serverHardwareUnitText("") == "—", "五金单位为空时应显示占位符")
    }

    private static func testProductionOrderPaths() {
        let model = AppModel()
        model.sourceRoot = "/Volumes/server/Optimized Orders"
        model.orderRoot = "/production/Order"
        model.backupRoot = "/production/Backups"
        require(model.activeOwnedSourceRoot == "/Volumes/server/Optimized Orders", "服务器目录错误")
        require(model.activeCutToSizeRoot == "/Volumes/server/CUT TO SIZE", "来料加工目录错误")
        require(model.activeOrderRoot == "/production/Order", "Traveler 目录错误")
        require(model.activeBackupRoot == "/production/Backups", "备份目录错误")
    }

    private static func testStockFailureKeepsManualRetryEnabled() {
        let model = AppModel()
        model.selectedOrderPath = "/orders/PP0067"
        model.selectedOrderId = "PP0067"
        model.orderMaterials = [
            OrderMaterialPreview(kind: "plywood", thickness: 18, color: "", quantity: 2)
        ]
        model.orderFactories = [OrderFactoryPreview(id: "F0067", factoryOrder: "F0067", orderName: "PP0067")]
        model.orderPreviewValidated = true
        model.orderError = "库存系统登录未成功"
        model.orderRunning = false
        require(model.orderPreviewReady, "库存查询失败不应清除已通过的订单预检状态")
        require(!model.orderRunning && model.orderPreviewReady, "库存查询失败后应允许再次手工点击查询")
    }

    private static func testExistingTravelerCanBeUpdatedAfterPreviewFailure() {
        require(
            orderUpdateActionReady(
                existingTravelerPath: "/orders/PP0067/Work Order Traveler(PP0067).xlsx",
                selectedOrderPath: "/orders/PP0067",
                selectedOrderId: "PP0067"
            ),
            "已有 Traveler 时，即使预览校验失败也应允许执行更新"
        )
        require(
            !orderUpdateActionReady(existingTravelerPath: "", selectedOrderPath: "/orders/PP0067", selectedOrderId: "PP0067"),
            "没有现有 Traveler 时不应绕过生成前校验"
        )
    }

    private static func testDashboardTravelerActionsUseDatabaseFacts() {
        let model = AppModel()
        model.selectedOrderId = "CS005"
        model.orderExistingTravelerPath = ""
        require(model.orderCanGenerateTraveler, "选中订单后应允许从数据库生成 Traveler")

        let temporary = FileManager.default.temporaryDirectory
            .appendingPathComponent("traveler-action-\(UUID().uuidString).xlsx")
        FileManager.default.createFile(atPath: temporary.path, contents: Data())
        defer { try? FileManager.default.removeItem(at: temporary) }
        require(orderTravelerOpenActionReady(existingTravelerPath: temporary.path), "存在 Traveler 文件时打开按钮应启用")
    }

    private static func testRelatedPreviewMissingMaterialIssue() {
        let response: [String: Any] = [
            "order_id": "PP0067",
            "orders": [],
            "errors": [[
                "order_id": "PP0067",
                "code": "missing_materials",
                "message": "PP0067 根目录找不到文件名包含 material 的 Excel",
            ]],
        ]
        let issues = orderPreviewIssues(response)
        require(issues.count == 1, "preview-related 的 errors 没有被界面识别")
        require(issues[0].orderId == "PP0067", "缺少 material 的订单号解析错误")
        require(issues[0].code == "missing_materials", "缺少 material 的错误码解析错误")
    }

    private static func testPP0067MissingMaterialShowsPrompt() {
        let root = FileManager.default.temporaryDirectory
            .appendingPathComponent("workflow-ui-missing-material-\(UUID().uuidString)", isDirectory: true)
        let folder = root.appendingPathComponent("PP0067", isDirectory: true)
        do {
            try FileManager.default.createDirectory(at: folder, withIntermediateDirectories: true)
        } catch {
            fail("无法创建缺少 material 的隔离测试目录：\(error)")
        }
        defer { try? FileManager.default.removeItem(at: root) }
        let model = AppModel()
        model.previewOrderFolder(OrderFolderItem(id: folder.path, orderId: "PP0067", modifiedAt: ""))
        let deadline = Date().addingTimeInterval(8)
        while model.orderRunning && Date() < deadline {
            pumpRunLoop(for: 0.05)
        }
        require(!model.orderRunning, "PP0067 后台预览超时")
        require(model.orderError.contains("material"), "PP0067 缺少 material 没有进入错误状态")
        require(model.showMaterialGenerationPrompt, "PP0067 缺少 material 没有显示自动生成提示")
    }

    private static func testFullPageHeaderBoundaryAlignment() {
        let fixedBoundary = headerBoundaryY(flexibleContent: false)
        let flexibleBoundary = headerBoundaryY(flexibleContent: true)
        require(
            abs(fixedBoundary - flexibleBoundary) <= 0.5,
            "完整页面内容高度改变了页头分隔线位置：fixed=\(fixedBoundary), flexible=\(flexibleBoundary)"
        )
    }

    private static func headerBoundaryY(flexibleContent: Bool) -> CGFloat {
        let box = HeaderBoundaryProbeBox()
        let hosting = NSHostingView(rootView: PageLayoutHarness(box: box, flexibleContent: flexibleContent))
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: AppLayout.windowMinWidth, height: 900),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        window.contentView = hosting
        window.orderFrontRegardless()
        hosting.layoutSubtreeIfNeeded()
        pumpRunLoop(for: 0.15)
        guard let probe = box.view else { fail("未找到完整页面页头边界探针") }
        let boundary = probe.convert(probe.bounds, to: hosting).maxY
        window.close()
        return boundary
    }

    private static func testOperationLogScrollsAfterAppending() {
        let initial = (0..<8).map { step($0) }
        let model = OperationLogHarnessModel(steps: initial)
        let hosting = NSHostingView(rootView: OperationLogHarnessView(model: model))
        let window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 720, height: AppLayout.operationLogHeight),
            styleMask: [.borderless],
            backing: .buffered,
            defer: false
        )
        window.contentView = hosting
        window.orderFrontRegardless()
        hosting.layoutSubtreeIfNeeded()
        pumpRunLoop(for: 0.2)

        guard let scrollView = firstScrollView(in: hosting),
              let documentView = scrollView.documentView else {
            fail("未找到操作记录的 NSScrollView")
        }
        scrollView.contentView.scroll(to: .zero)
        scrollView.reflectScrolledClipView(scrollView.contentView)

        model.steps.append(step(8))
        pumpRunLoop(for: 0.3)
        documentView.layoutSubtreeIfNeeded()

        let visibleBottom = scrollView.contentView.bounds.maxY
        let documentBottom = documentView.bounds.maxY
        require(
            abs(visibleBottom - documentBottom) <= 2,
            "追加记录后未滚动到底部：visible=\(visibleBottom), document=\(documentBottom)"
        )

        scrollView.contentView.scroll(to: .zero)
        scrollView.reflectScrolledClipView(scrollView.contentView)
        let last = model.steps.count - 1
        model.steps[last] = InventoryStep(
            time: model.steps[last].time,
            title: model.steps[last].title,
            detail: "updated detail",
            state: "success"
        )
        pumpRunLoop(for: 0.3)
        documentView.layoutSubtreeIfNeeded()
        require(
            abs(scrollView.contentView.bounds.maxY - documentView.bounds.maxY) <= 2,
            "更新运行中记录后未滚动到底部"
        )
        window.close()
    }

    private static func testOperationLogReader() {
        let line = "{\"event\":\"user.action\",\"message\":\"点击保存设置\",\"timestamp\":\"2026-08-13T15:30:45.123-07:00\"}"
        guard let entry = OperationLogReader.parse(line: line) else {
            fatalError("操作日志 JSONL 读取失败")
        }
        require(entry.operation == "点击保存设置", "操作日志查看页未显示用户可理解的操作内容")
        require(entry.displayTime == "2026-08-13 15:30:45", "操作日志时间未格式化为本地可读格式")
        require(OperationLogReader.parse(line: "不是 JSON") == nil, "无效操作日志行不应导致读取失败")
    }

    private static func testOperationLogMaintenance() {
        let fileManager = FileManager.default
        let url = fileManager.temporaryDirectory
            .appendingPathComponent("operation-log-test-\(UUID().uuidString).jsonl")
        defer { try? fileManager.removeItem(at: url) }

        let lines = [
            "{\"event\":\"user.action\",\"message\":\"旧记录\",\"timestamp\":\"2026-01-07T23:59:59-08:00\"}",
            "{\"event\":\"user.action\",\"message\":\"三天边界\",\"timestamp\":\"2026-01-08T00:00:00-08:00\"}",
            "{\"event\":\"user.action\",\"message\":\"今天记录\",\"timestamp\":\"2026-01-10T12:00:00-08:00\"}",
            "{\"event\":\"user.action\",\"message\":\"UTC 今天记录\",\"timestamp\":\"2026-01-11T07:30:00Z\"}",
        ]
        try! lines.joined(separator: "\n").appending("\n").data(using: .utf8)!.write(to: url)

        var calendar = Calendar(identifier: .gregorian)
        calendar.timeZone = TimeZone(identifier: "America/Los_Angeles")!
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime]
        let now = formatter.date(from: "2026-01-10T12:00:00-08:00")!
        let result = try! OperationLogReader.trim(toRecentDays: 3, at: url, now: now, calendar: calendar)
        let remaining = try! String(contentsOf: url, encoding: .utf8)

        require(result.removedEntries == 1, "日志清理未删除三天前的记录")
        require(result.retainedEntries == 3, "日志清理未保留近三天的记录")
        require(!remaining.contains("旧记录"), "日志清理仍保留三天前的记录")
        require(remaining.contains("三天边界") && remaining.contains("UTC 今天记录"), "日志清理错误处理日期边界或 UTC 时间")
        require(OperationLogReader.fileSizeText(from: url) != "0 bytes", "日志文件大小显示未读取文件")
    }

    private static func traveler(_ name: String, folder: String, modifiedAt: String) -> InventoryTraveler {
        InventoryTraveler(
            id: folder + name,
            ppFolder: folder,
            fileName: name,
            orderName: "",
            modifiedAt: modifiedAt,
            status: "未出库",
            documentNumber: ""
        )
    }

    private static func step(_ index: Int) -> InventoryStep {
        InventoryStep(time: "08:00:\(index)", title: "step \(index)", detail: "detail \(index)", state: "success")
    }

    private static func firstScrollView(in view: NSView) -> NSScrollView? {
        if let scrollView = view as? NSScrollView { return scrollView }
        for child in view.subviews {
            if let found = firstScrollView(in: child) { return found }
        }
        return nil
    }

    private static func pumpRunLoop(for seconds: TimeInterval) {
        RunLoop.current.run(until: Date().addingTimeInterval(seconds))
    }

    private static func require(_ condition: @autoclosure () -> Bool, _ message: String) {
        if !condition() { fail(message) }
    }

    private static func fail(_ message: String) -> Never {
        fputs("FAIL: \(message)\n", stderr)
        exit(1)
    }
}
