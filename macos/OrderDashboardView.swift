// 订单中心视图与布局辅助方法。看板显示已持久化订单事实，并通过 AppModel 发起操作；
// 不得从仅用于显示的状态推断生产、出货或安装事实。
import SwiftUI
import AppKit
import UniformTypeIdentifiers

let orderDashboardStatuses = [
    "已拆单待优化",
    "部分优化",
    "已优化",
    "部分出货",
    "已出货",
    "已中止",
]

let orderDashboardMetricColumnCount = 8
let orderDashboardMetricMinimumWidth: CGFloat = 110
let orderDashboardMetricSpacing: CGFloat = 10
// 为工厂单身份和状态列保留实用的最小宽度。订单级 Panel 颜色已在表格上方显示，
// 因此表格无需单独的颜色列。
let orderDashboardFactoryColumnWidths: [CGFloat] = [150, 220, 127.5, 127.5, 127.5, 127.5]
let orderDashboardFactorySelectionColumnWidth: CGFloat = 54
let orderDashboardOperationColumnWidth: CGFloat = 136
let orderDashboardFactoryCountColumnWidth: CGFloat = 90
let orderDashboardUpdatedAtColumnWidth: CGFloat = 176
private let orderDashboardLeadingColumnWidth: CGFloat = 40
private let orderDashboardFlexibleColumnCount = 6
private let orderDashboardScrollIndicatorReservation: CGFloat = 16
private let orderDashboardDataHeaderTitles: Set<String> = [
    "订单",
    "状态",
    "工厂单",
    "材料",
    "优化进度",
    "生产进度",
    "出货进度",
]
private let orderDashboardDataHeaderOffset: CGFloat = 2

private struct OrderDashboardTableLayout {
    let flexibleColumnWidth: CGFloat
    let totalWidth: CGFloat
    let containerWidth: CGFloat

    /// 根据容器宽度分配固定列和弹性列，并预留滚动条空间。
    /// - Parameters:
    ///   - totalWidth: 表格容器总宽度，单位为逻辑点。
    init(totalWidth: CGFloat) {
        self.containerWidth = totalWidth
        let fixedWidth = orderDashboardLeadingColumnWidth
            + orderDashboardFactoryCountColumnWidth
            + orderDashboardUpdatedAtColumnWidth
            + orderDashboardOperationColumnWidth
        let contentWidth = max(0, totalWidth - orderDashboardScrollIndicatorReservation)
        self.flexibleColumnWidth = max(
            100,
            (contentWidth - fixedWidth) / CGFloat(orderDashboardFlexibleColumnCount)
        )
        self.totalWidth = max(
            contentWidth,
            fixedWidth + flexibleColumnWidth * CGFloat(orderDashboardFlexibleColumnCount)
        )
    }

    /// 返回不包含操作按钮列的数据区域宽度。
    var dataWidth: CGFloat {
        totalWidth - orderDashboardOperationColumnWidth
    }

    /// 计算表格内容之后需要补齐的空白宽度。
    var trailingSpacerWidth: CGFloat {
        max(0, containerWidth - totalWidth)
    }

    var columns: [GridItem] {
        [
            orderDashboardLeadingColumnWidth,
            flexibleColumnWidth,
            flexibleColumnWidth,
            orderDashboardFactoryCountColumnWidth,
            flexibleColumnWidth,
            flexibleColumnWidth,
            flexibleColumnWidth,
            flexibleColumnWidth,
            orderDashboardUpdatedAtColumnWidth,
            orderDashboardOperationColumnWidth,
        ].map { GridItem(.fixed($0), spacing: 0) }
    }

    /// 取得不包含最后操作列的网格列配置。
    var dataColumns: [GridItem] {
        Array(columns.dropLast())
    }
}

let dashboardMessageVisibleRowCount = 3
let dashboardMessageRowHeight: CGFloat = 59
let dashboardMessageViewportHeight = CGFloat(dashboardMessageVisibleRowCount) * dashboardMessageRowHeight
let dashboardMessageHoverDelay: TimeInterval = 1.0
let dashboardMessageHoverCloseGrace: TimeInterval = 0.8
let panelMaterialHoverDelay: TimeInterval = 1.0
let orderInstallationDateButtonWidth: CGFloat = 184
let orderInstallationDisplayDateFormat = "yyyy年M月d日"

struct AppGlassDatePickerCalendar: View {
    @Binding var selection: Date
    @State private var displayedMonth: Date
    let compact: Bool

    private let weekdays = ["日", "一", "二", "三", "四", "五", "六"]

    /// 绑定日期选择，并用当前选择初始化显示月份。
    /// - Parameters:
    ///   - selection: 日历选中日期的双向绑定。
    ///   - compact: 是否使用紧凑日历尺寸。
    init(selection: Binding<Date>, compact: Bool = false) {
        _selection = selection
        _displayedMonth = State(initialValue: selection.wrappedValue)
        self.compact = compact
    }

    /// 根据紧凑模式选择日历日期单元格边长。
    private var daySize: CGFloat { compact ? 30 : 34 }
    /// 根据紧凑模式选择日历网格间距。
    private var gridSpacing: CGFloat { compact ? 4 : 6 }
    private var columns: [GridItem] {
        Array(repeating: GridItem(.fixed(daySize), spacing: gridSpacing), count: 7)
    }

    /// 创建周日开始的公历，用于日历网格和日期选择。
    private var calendar: Calendar {
        var value = Calendar(identifier: .gregorian)
        value.locale = Locale(identifier: "zh_CN")
        value.timeZone = .current
        value.firstWeekday = 1
        return value
    }

    /// 生成当前显示月份所需的完整周日期网格。
    private var gridDates: [Date] {
        guard let month = calendar.dateInterval(of: .month, for: displayedMonth) else { return [] }
        let firstDay = calendar.startOfDay(for: month.start)
        let leadingDays = (calendar.component(.weekday, from: firstDay) - calendar.firstWeekday + 7) % 7
        guard let gridStart = calendar.date(byAdding: .day, value: -leadingDays, to: firstDay) else { return [] }
        return (0..<42).compactMap { offset in
            calendar.date(byAdding: .day, value: offset, to: gridStart)
        }
    }

    var body: some View {
        VStack(spacing: compact ? 10 : 13) {
            HStack(spacing: 10) {
                Text(appGlassDatePickerMonthTitle(displayedMonth))
                    .font(.system(size: 20, weight: .semibold, design: .rounded))
                Spacer(minLength: 12)
                monthButton(symbol: "chevron.left", delta: -1, label: "上个月")
                Button {
                    displayedMonth = Date()
                } label: {
                    Circle()
                        .fill(AppPalette.accent.opacity(0.82))
                        .frame(width: 9, height: 9)
                        .frame(width: 28, height: 28)
                }
                .buttonStyle(.plain)
                .help("回到本月")
                .accessibilityLabel("回到本月")
                monthButton(symbol: "chevron.right", delta: 1, label: "下个月")
            }

            LazyVGrid(columns: columns, spacing: gridSpacing) {
                ForEach(weekdays, id: \.self) { weekday in
                    Text(weekday)
                        .font(.caption.weight(.semibold))
                        .foregroundStyle(.secondary)
                        .frame(width: daySize, height: compact ? 20 : 24)
                }

                ForEach(gridDates, id: \.self) { date in
                    dayButton(date)
                }
            }
        }
        .padding(compact ? 12 : 18)
        .frame(width: compact ? 278 : 316)
        .glassEffect(
            .regular.tint(Color.white.opacity(0.12)),
            in: RoundedRectangle(cornerRadius: 24, style: .continuous)
        )
        .overlay {
            RoundedRectangle(cornerRadius: 24, style: .continuous)
                .stroke(Color.white.opacity(0.38), lineWidth: 1)
        }
        .onAppear { displayedMonth = selection }
    }

    /// 构造日历切月按钮并按月份偏移更新显示。
    /// - Parameters:
    ///   - symbol: 系统图标名称。
    ///   - delta: 切换月份的偏移量，前月为负、后月为正。
    ///   - label: 按钮的辅助功能说明。
    private func monthButton(symbol: String, delta: Int, label: String) -> some View {
        Button {
            if let nextMonth = calendar.date(byAdding: .month, value: delta, to: displayedMonth) {
                displayedMonth = nextMonth
            }
        } label: {
            Image(systemName: symbol)
                .font(.caption.weight(.bold))
                .frame(width: 28, height: 28)
                .glassEffect(.clear, in: Circle())
        }
        .buttonStyle(.plain)
        .help(label)
        .accessibilityLabel(label)
    }

    /// 构造单个日历日期按钮并保持原选择的时间分量。
    /// - Parameters:
    ///   - date: 待显示、选择或计算的日期时间。
    private func dayButton(_ date: Date) -> some View {
        let isSelected = calendar.isDate(date, inSameDayAs: selection)
        let isToday = calendar.isDateInToday(date)
        let isDisplayedMonth = calendar.isDate(date, equalTo: displayedMonth, toGranularity: .month)

        return Button {
            selection = appGlassDatePickerDate(date, preservingTimeFrom: selection, calendar: calendar)
            if !isDisplayedMonth { displayedMonth = date }
        } label: {
            ZStack {
                if isSelected {
                    Circle()
                        .fill(AppPalette.accent.opacity(0.90))
                        .glassEffect(.regular.tint(AppPalette.accent.opacity(0.28)), in: Circle())
                } else if isToday {
                    Circle()
                        .stroke(AppPalette.accent.opacity(0.72), lineWidth: 1.5)
                }
                Text("\(calendar.component(.day, from: date))")
                    .font(.system(size: 14, weight: isSelected ? .semibold : .regular, design: .rounded))
                    .foregroundStyle(
                        isSelected
                            ? Color.white
                            : (isDisplayedMonth ? Color.primary : Color.secondary.opacity(0.48))
                    )
            }
            .frame(width: daySize, height: daySize)
            .contentShape(Circle())
        }
        .buttonStyle(.plain)
        .help(appGlassDatePickerDisplayDate(date))
        .accessibilityLabel(appGlassDatePickerDisplayDate(date))
        .accessibilityValue(isSelected ? "已选择" : "")
    }
}

/// 采用选中日期的年月日并保留原时间分量。
/// - Parameters:
///   - date: 待显示、选择或计算的日期时间。
///   - original: 需要保留时分秒的原日期时间。
///   - calendar: 用于日期计算的日历。
func appGlassDatePickerDate(_ date: Date, preservingTimeFrom original: Date, calendar: Calendar) -> Date {
    let dateParts = calendar.dateComponents([.year, .month, .day], from: date)
    let timeParts = calendar.dateComponents([.hour, .minute, .second, .nanosecond], from: original)
    var combined = DateComponents()
    combined.timeZone = calendar.timeZone
    combined.year = dateParts.year
    combined.month = dateParts.month
    combined.day = dateParts.day
    combined.hour = timeParts.hour
    combined.minute = timeParts.minute
    combined.second = timeParts.second
    combined.nanosecond = timeParts.nanosecond
    return calendar.date(from: combined) ?? date
}

/// 生成日期选择器的中文日期文字。
/// - Parameters:
///   - date: 待显示、选择或计算的日期时间。
private func appGlassDatePickerDisplayDate(_ date: Date) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: "zh_CN")
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.dateFormat = "yyyy年M月d日"
    return formatter.string(from: date)
}

/// 格式化日历顶部显示的年月标题。
/// - Parameters:
///   - date: 待显示、选择或计算的日期时间。
private func appGlassDatePickerMonthTitle(_ date: Date) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: "zh_CN")
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.dateFormat = "yyyy年M月"
    return formatter.string(from: date)
}

extension View {
    /// 为日历弹出层应用统一玻璃背景和圆角。
    /// 无参数。
    func appGlassDatePickerPopoverSurface() -> some View {
        padding(10)
            .presentationBackground(.clear)
    }
}

/// 识别明确的 SKU 映射问题，避免把普通报表错误送入映射工作区。
/// - Parameters:
///   - issue: 待判断或处理的当前业务问题。
func currentIssueRequiresInventoryMapping(_ issue: CurrentIssue) -> Bool {
    if issue.kind == "material_mapping" || issue.kind == "hardware_mapping" {
        return true
    }
    if issue.kind == "temporary_processing" && issue.message.contains("未映射材料") {
        return true
    }
    // 材料 SKU 失败目前与普通工作簿或读取失败一起保存为 material_validation。
    // 只有明确的 SKU 提示才应打开映射工作区；文件格式错误仍使用普通的“标记已处理”操作。
    return issue.kind == "material_validation"
        && issue.message.contains("未完成商品 SKU 处理")
}

/// 为 Server 材料变化列表中的类别分配排序权重。
/// - Parameters:
///   - materialType: 材料类别代码。
private func serverWriteMaterialTypeRank(_ materialType: String) -> Int {
    switch materialType.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() {
    case "plywood": return 0
    case "panel", "back": return 1
    case "edge": return 2
    default: return 3
    }
}

/// 按常用 Plywood 厚度设置变化列表显示优先级。
/// - Parameters:
///   - thickness: 材料厚度，按毫米表示。
private func serverWritePlywoodThicknessRank(_ thickness: String) -> Int {
    let value = Double(thickness) ?? .greatestFiniteMagnitude
    if abs(value - 18) < 0.01 { return 0 }
    if abs(value - 14.5) < 0.01 { return 1 }
    if abs(value - 5.4) < 0.01 { return 2 }
    return 3
}

/// 按类别、颜色、厚度等规格排列 Server 材料变化。
/// - Parameters:
///   - changes: Server 材料数量变化列表。
func sortedServerWriteMaterialChanges(_ changes: [ServerWriteMaterialChange]) -> [ServerWriteMaterialChange] {
    changes.sorted { left, right in
        let leftType = serverWriteMaterialTypeRank(left.materialType)
        let rightType = serverWriteMaterialTypeRank(right.materialType)
        if leftType != rightType { return leftType < rightType }

        if leftType == 0 {
            let leftThicknessRank = serverWritePlywoodThicknessRank(left.thickness)
            let rightThicknessRank = serverWritePlywoodThicknessRank(right.thickness)
            if leftThicknessRank != rightThicknessRank { return leftThicknessRank < rightThicknessRank }
        }

        let leftThickness = Double(left.thickness) ?? .greatestFiniteMagnitude
        let rightThickness = Double(right.thickness) ?? .greatestFiniteMagnitude
        if abs(leftThickness - rightThickness) > 0.01 { return leftThickness < rightThickness }

        let leftLabel = [left.color, left.thickness, left.edge]
            .joined(separator: "|")
            .folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current)
        let rightLabel = [right.color, right.thickness, right.edge]
            .joined(separator: "|")
            .folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current)
        return leftLabel.localizedStandardCompare(rightLabel) == .orderedAscending
    }
}

/// 仅在 App 活动且主窗口位于前方时允许悬停详情。
/// - Parameters:
///   - appIsActive: App 当前是否处于活动状态。
///   - mainWindowIsFrontmost: 主窗口是否位于最前方。
func dashboardMessageHoverCanPresent(appIsActive: Bool, mainWindowIsFrontmost: Bool) -> Bool {
    appIsActive && mainWindowIsFrontmost
}

let orderDashboardMetricColumns = Array(
    repeating: GridItem(.flexible(minimum: orderDashboardMetricMinimumWidth), spacing: orderDashboardMetricSpacing),
    count: orderDashboardMetricColumnCount
)

let orderDetailGridColumnCount = 4
let orderDetailCardMinHeight: CGFloat = 50

/// 判断可用宽度是否足够容纳整行订单统计卡片。
/// - Parameters:
///   - width: 单元格或容器宽度，单位为逻辑点。
///   - horizontalPadding: 统计区域左右留白，单位为逻辑点。
func orderDashboardMetricsFit(width: CGFloat, horizontalPadding: CGFloat) -> Bool {
    let cards = CGFloat(orderDashboardMetricColumnCount) * orderDashboardMetricMinimumWidth
    let gaps = CGFloat(orderDashboardMetricColumnCount - 1) * orderDashboardMetricSpacing
    return width - horizontalPadding * 2 >= cards + gaps
}

/// 从订单材料中提取去重的 Panel 颜色。
/// - Parameters:
///   - materials: 订单材料预览列表。
func orderDashboardPanelColors(_ materials: [OrderMaterialPreview]) -> [String] {
    var result: [String] = []
    for material in materials where material.kind == "panel" {
        let color = material.color.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !color.isEmpty, !result.contains(where: { $0.caseInsensitiveCompare(color) == .orderedSame }) else { continue }
        result.append(color)
    }
    return result
}

/// 提取用于订单行显示的 Panel 材料并整理顺序。
/// - Parameters:
///   - materials: 订单材料预览列表。
func orderDashboardPanelMaterials(_ materials: [OrderMaterialPreview]) -> [OrderMaterialPreview] {
    var result: [OrderMaterialPreview] = []
    for material in materials where material.kind == "panel" {
        let color = material.color.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !color.isEmpty, !result.contains(where: {
            $0.color.trimmingCharacters(in: .whitespacesAndNewlines)
                .caseInsensitiveCompare(color) == .orderedSame
        }) else { continue }
        result.append(material)
    }
    return result
}

/// 根据材料 SKU 构造图片路径，缺少有效代码时返回空值。
/// - Parameters:
///   - productCode: 库存商品的规范 SKU 代码。
func panelMaterialImageURL(productCode: String) -> URL? {
    let code = productCode.trimmingCharacters(in: .whitespacesAndNewlines)
    guard !code.isEmpty,
          let resourceRoot = Bundle.main.resourceURL?.appendingPathComponent("project/resources/panel-images")
    else { return nil }
    let files = (try? FileManager.default.contentsOfDirectory(
        at: resourceRoot,
        includingPropertiesForKeys: [.isRegularFileKey],
        options: [.skipsHiddenFiles]
    )) ?? []
    return files.first {
        let name = $0.deletingPathExtension().lastPathComponent
        return name == code || name.hasPrefix("\(code)_")
    }
}

private final class PanelMaterialHoverTrackingView: NSView {
    var onMouseEntered: (() -> Void)?
    var onMouseExited: (() -> Void)?

    /// 按当前视图边界重新注册鼠标进入和离开跟踪区域。
    /// 无参数。
    override func updateTrackingAreas() {
        trackingAreas.forEach(removeTrackingArea)
        addTrackingArea(
            NSTrackingArea(
                rect: bounds,
                options: [.mouseEnteredAndExited, .activeAlways, .inVisibleRect],
                owner: self,
                userInfo: nil
            )
        )
        super.updateTrackingAreas()
    }

    /// 将鼠标进入跟踪区域的事件转发给悬停回调。
    /// - Parameters:
    ///   - event: 系统派发的鼠标进入或离开事件。
    override func mouseEntered(with event: NSEvent) {
        onMouseEntered?()
        super.mouseEntered(with: event)
    }

    /// 将鼠标离开跟踪区域的事件转发给悬停回调。
    /// - Parameters:
    ///   - event: 系统派发的鼠标进入或离开事件。
    override func mouseExited(with event: NSEvent) {
        onMouseExited?()
        super.mouseExited(with: event)
    }
}

private struct PanelMaterialHoverTracking: NSViewRepresentable {
    let onMouseEntered: () -> Void
    let onMouseExited: () -> Void

    /// 创建材料悬停跟踪视图并连接进入、离开回调。
    /// - Parameters:
    ///   - context: SwiftUI 提供的桥接上下文与协调器。
    func makeNSView(context: Context) -> PanelMaterialHoverTrackingView {
        let view = PanelMaterialHoverTrackingView(frame: .zero)
        view.onMouseEntered = onMouseEntered
        view.onMouseExited = onMouseExited
        return view
    }

    /// 将最新材料悬停回调更新到已有跟踪视图。
    /// - Parameters:
    ///   - nsView: 已创建并需要更新或卸载的 AppKit 视图。
    ///   - context: SwiftUI 提供的桥接上下文与协调器。
    func updateNSView(_ nsView: PanelMaterialHoverTrackingView, context: Context) {
        nsView.onMouseEntered = onMouseEntered
        nsView.onMouseExited = onMouseExited
    }
}

struct PanelMaterialHoverPreview<Content: View>: View {
    private let previewImageHeight: CGFloat = 360
    let material: OrderMaterialPreview
    let content: Content
    @State private var isPresented = false
    @State private var hoverGeneration = 0

    /// 保存材料与内容，供悬停时展示对应 Panel 图片。
    /// - Parameters:
    ///   - material: 订单材料预览。
    ///   - content: 生成卡片或容器内部视图的闭包。
    init(material: OrderMaterialPreview, @ViewBuilder content: () -> Content) {
        self.material = material
        self.content = content()
    }

    /// 取得当前 Panel 材料对应的预览图片位置。
    private var imageURL: URL? {
        panelMaterialImageURL(productCode: material.productCode)
    }

    /// 读取当前材料的本地预览图片。
    private var previewImage: NSImage? {
        imageURL.flatMap { NSImage(contentsOf: $0) }
    }

    /// 按图片比例计算预览宽度，避免变形或超出限制。
    private var previewImageWidth: CGFloat {
        guard let image = previewImage, image.size.height > 0 else {
            return previewImageHeight
        }
        return previewImageHeight * image.size.width / image.size.height
    }

    /// 组合当前 Panel 材料的可读名称。
    private var panelDisplayName: String {
        let brand = material.brand.trimmingCharacters(in: .whitespacesAndNewlines)
        let color = material.color.trimmingCharacters(in: .whitespacesAndNewlines)
        return brand.isEmpty ? color : "\(brand) · \(color)"
    }

    var body: some View {
        content
            .background(
                PanelMaterialHoverTracking(
                    onMouseEntered: {
                        hoverGeneration += 1
                        let generation = hoverGeneration
                        DispatchQueue.main.asyncAfter(deadline: .now() + panelMaterialHoverDelay) {
                            guard generation == hoverGeneration else { return }
                            isPresented = previewImage != nil
                        }
                    },
                    onMouseExited: {
                        hoverGeneration += 1
                        isPresented = false
                    }
                )
            )
        .disabled(false)
            .popover(
                isPresented: $isPresented,
                attachmentAnchor: .rect(.bounds),
                arrowEdge: .bottom
            ) {
                VStack(spacing: 10) {
                    if let image = previewImage {
                        Image(nsImage: image)
                            .resizable()
                            .scaledToFit()
                            .frame(width: previewImageWidth, height: previewImageHeight)
                            .clipShape(RoundedRectangle(cornerRadius: 6, style: .continuous))
                    }
                    Text(panelDisplayName)
                        .font(.headline)
                        .lineLimit(1)
                        .minimumScaleFactor(0.7)
                        .truncationMode(.tail)
                        .frame(width: previewImageWidth)
                        .padding(.bottom, 2)
                }
                .frame(width: previewImageWidth, alignment: .center)
                .padding(.top, 10)
            }
    }
}

/// 筛选订单 Plywood 材料并按业务厚度顺序排序。
/// - Parameters:
///   - rows: 订单材料预览列表。
func orderDetailPlywoodRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview] {
    orderedMaterialRows(rows.filter { $0.kind == "plywood" })
}

/// 筛选 Panel 并按颜色、厚度优先级和数量排序。
/// - Parameters:
///   - rows: 订单材料预览列表。
func orderDetailPanelRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview] {
    rows
        .filter { $0.kind == "panel" }
        .sorted {
            let leftColor = $0.color.trimmingCharacters(in: .whitespacesAndNewlines)
            let rightColor = $1.color.trimmingCharacters(in: .whitespacesAndNewlines)
            let leftColorKey = leftColor.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current)
            let rightColorKey = rightColor.folding(options: [.caseInsensitive, .diacriticInsensitive], locale: .current)
            let colorOrder = leftColorKey.localizedStandardCompare(rightColorKey)
            if colorOrder != .orderedSame { return colorOrder == .orderedAscending }
            let leftThicknessRank = orderDetailPanelThicknessRank($0.thickness)
            let rightThicknessRank = orderDetailPanelThicknessRank($1.thickness)
            if leftThicknessRank != rightThicknessRank { return leftThicknessRank < rightThicknessRank }
            if abs($0.thickness - $1.thickness) > 0.01 { return $0.thickness < $1.thickness }
            return $0.quantity < $1.quantity
        }
}

/// 优先显示 19.1 毫米门板，其次为 8 或 9 毫米背板。
/// - Parameters:
///   - thickness: 材料厚度，按毫米表示。
func orderDetailPanelThicknessRank(_ thickness: Double) -> Int {
    if abs(thickness - 19.1) < 0.01 { return 0 }
    if abs(thickness - 8) < 0.01 || abs(thickness - 9) < 0.01 { return 1 }
    return 2
}

/// 按自然名称顺序排列订单详情中的封边颜色。
/// - Parameters:
///   - colors: 待排列的颜色名称列表。
func orderDetailEdgeColors(_ colors: [String]) -> [String] {
    colors.sorted {
        let left = $0.trimmingCharacters(in: .whitespacesAndNewlines)
        let right = $1.trimmingCharacters(in: .whitespacesAndNewlines)
        return left.localizedStandardCompare(right) == .orderedAscending
    }
}

/// 统计库存预览中数量不足的商品行数。
/// - Parameters:
///   - rows: 实时库存预览列表。
func orderDashboardShortageCount(_ rows: [OrderStockPreview]) -> Int {
    rows.filter { !$0.sufficient }.count
}

/// 按错误和预览校验状态生成订单行状态文字。
/// - Parameters:
///   - previewValidated: 订单预览是否通过校验。
///   - hasError: 预览或校验是否存在错误。
///   - isExistingTraveler: 是否已有 Traveler；当前状态推导不使用此值。
func orderDashboardStatus(previewValidated: Bool, hasError: Bool, isExistingTraveler: Bool) -> String {
    if hasError { return "数据异常" }
    if previewValidated { return "已优化" }
    return "待校验"
}

/// 根据点击和强制展开标志决定展开的订单身份。
/// - Parameters:
///   - current: 当前展开的订单身份；为空表示全部折叠。
///   - tapped: 本次点击的订单身份。
///   - forceOpen: 是否强制展开，禁止再次点击时折叠。
func orderDashboardExpandedID(current: String?, tapped: String, forceOpen: Bool = false) -> String? {
    if !forceOpen, current == tapped { return nil }
    return tapped
}

struct OrderDashboardClickContainer<Content: View>: View {
    let content: Content
    let onSingleClick: () -> Void
    let onDoubleClick: () -> Void

    /// 保存行内容及单击、双击回调，供透明手势层接收事件。
    /// - Parameters:
    ///   - onSingleClick: 单击订单行时执行的回调。
    ///   - onDoubleClick: 双击订单行时执行的回调。
    ///   - content: 生成卡片或容器内部视图的闭包。
    init(
        onSingleClick: @escaping () -> Void,
        onDoubleClick: @escaping () -> Void,
        @ViewBuilder content: () -> Content
    ) {
        self.content = content()
        self.onSingleClick = onSingleClick
        self.onDoubleClick = onDoubleClick
    }

    var body: some View {
        content.overlay {
            OrderDashboardClickReceiver(onSingleClick: onSingleClick, onDoubleClick: onDoubleClick)
        }
    }
}

// 此视图没有固有内容尺寸，也不承载 SwiftUI 内容。父视图提供点击区域，
// 手势不能反向影响尺寸约束。
struct OrderDashboardClickReceiver: NSViewRepresentable {
    let onSingleClick: () -> Void
    let onDoubleClick: () -> Void

    /// 创建负责 AppKit 事件与 SwiftUI 状态衔接的协调器。
    /// 无参数。
    func makeCoordinator() -> Coordinator {
        Coordinator(onSingleClick: onSingleClick, onDoubleClick: onDoubleClick)
    }

    /// 创建透明点击视图，注册单击和双击手势并设置依赖关系。
    /// - Parameters:
    ///   - context: SwiftUI 提供的桥接上下文与协调器。
    func makeNSView(context: Context) -> NSView {
        let container = NSView(frame: .zero)
        let doubleClick = NSClickGestureRecognizer(
            target: context.coordinator,
            action: #selector(Coordinator.doubleClick)
        )
        doubleClick.numberOfClicksRequired = 2
        let singleClick = NSClickGestureRecognizer(
            target: context.coordinator,
            action: #selector(Coordinator.singleClick)
        )
        singleClick.numberOfClicksRequired = 1
        singleClick.delegate = context.coordinator
        doubleClick.delegate = context.coordinator
        container.addGestureRecognizer(doubleClick)
        container.addGestureRecognizer(singleClick)
        return container
    }

    /// 将最新订单行单击和双击回调同步到协调器。
    /// - Parameters:
    ///   - nsView: 已创建并需要更新或卸载的 AppKit 视图。
    ///   - context: SwiftUI 提供的桥接上下文与协调器。
    func updateNSView(_ nsView: NSView, context: Context) {
        context.coordinator.onSingleClick = onSingleClick
        context.coordinator.onDoubleClick = onDoubleClick
    }

    final class Coordinator: NSObject, NSGestureRecognizerDelegate {
        var onSingleClick: () -> Void
        var onDoubleClick: () -> Void

        /// 保存订单行的单击与双击事件回调。
        /// - Parameters:
        ///   - onSingleClick: 单击订单行时执行的回调。
        ///   - onDoubleClick: 双击订单行时执行的回调。
        init(onSingleClick: @escaping () -> Void, onDoubleClick: @escaping () -> Void) {
            self.onSingleClick = onSingleClick
            self.onDoubleClick = onDoubleClick
        }

        /// 让单击识别等待双击失败，避免双击同时触发单击。
        /// - Parameters:
        ///   - gestureRecognizer: 正在询问依赖关系的手势识别器。
        ///   - otherGestureRecognizer: 可能优先处理双击的另一手势识别器。
        func gestureRecognizer(_ gestureRecognizer: NSGestureRecognizer, shouldRequireFailureOf otherGestureRecognizer: NSGestureRecognizer) -> Bool {
            gestureRecognizer is NSClickGestureRecognizer
                && (gestureRecognizer as? NSClickGestureRecognizer)?.numberOfClicksRequired == 1
                && otherGestureRecognizer is NSClickGestureRecognizer
                && (otherGestureRecognizer as? NSClickGestureRecognizer)?.numberOfClicksRequired == 2
        }

        /// 执行订单行单击回调。
        /// 无参数。
        @objc func singleClick() { onSingleClick() }
        /// 执行订单行双击回调。
        /// 无参数。
        @objc func doubleClick() { onDoubleClick() }
    }
}

/// 返回切换指定工厂单选择后的新集合。
/// - Parameters:
///   - selected: 当前选中的工厂单号集合。
///   - factoryOrder: 目标工厂单号。
func toggledOrderFactorySelection(_ selected: Set<String>, factoryOrder: String) -> Set<String> {
    var next = selected
    if next.contains(factoryOrder) {
        next.remove(factoryOrder)
    } else {
        next.insert(factoryOrder)
    }
    return next
}

/// 按所选工厂单身份取得非空订单名称。
/// - Parameters:
///   - factories: 工厂单预览列表。
///   - selected: 当前选中的工厂单号集合。
func selectedOrderFactoryNames(_ factories: [OrderFactoryPreview], selected: Set<String>) -> [String] {
    factories
        .filter { selected.contains($0.factoryOrder) }
        .map(\.orderName)
        .filter { !$0.isEmpty }
}

/// 检查所选工厂单是否包含已出库记录。
/// - Parameters:
///   - selected: 当前选中的工厂单号集合。
///   - statuses: 以工厂单号为键的出库状态。
func orderDashboardHasShippedSelection(
    _ selected: Set<String>,
    statuses: [String: String]
) -> Bool {
    selected.contains { statuses[$0] == "已出库" }
}

/// 检查所选工厂单是否包含需要更新出库的记录。
/// - Parameters:
///   - selected: 当前选中的工厂单号集合。
///   - statuses: 以工厂单号为键的出库状态。
func orderDashboardNeedsOutboundUpdateSelection(
    _ selected: Set<String>,
    statuses: [String: String]
) -> Bool {
    selected.contains { statuses[$0] == "需要更新" }
}

/// 检查所选工厂单是否已有生产完成事实。
/// - Parameters:
///   - selected: 当前选中的工厂单号集合。
///   - produced: 以工厂单号为键的生产完成状态。
func orderDashboardHasProducedSelection(
    _ selected: Set<String>,
    produced: [String: Bool]
) -> Bool {
    selected.contains { produced[$0] == true }
}

/// 返回当前统一使用的出货按钮标题。
/// - Parameters:
///   - selected: 当前选中的工厂单号集合。
///   - statuses: 以工厂单号为键的出库状态。
func orderDashboardOutboundActionTitle(
    _ selected: Set<String>,
    statuses: [String: String]
) -> String {
    "出货"
}

/// 显示出库状态；已出库且有单号时附加单据号。
/// - Parameters:
///   - status: 业务状态文字或状态代码。
///   - documentNumber: 外部系统返回的出库单据号。
func orderDashboardOutboundDisplay(status: String, documentNumber: String) -> String {
    let trimmedStatus = status.trimmingCharacters(in: .whitespacesAndNewlines)
    let trimmedDocument = documentNumber.trimmingCharacters(in: .whitespacesAndNewlines)
    guard trimmedStatus == "已出库", !trimmedDocument.isEmpty else { return trimmedStatus }
    return "\(trimmedStatus) · \(trimmedDocument)"
}

/// 判断订单阶段是否符合全部、未完成或指定状态筛选。
/// - Parameters:
///   - stage: 订单或操作的当前阶段标识。
///   - statusFilter: 当前订单阶段筛选选项。
func orderDashboardStageMatchesFilter(_ stage: String, statusFilter: String) -> Bool {
    if statusFilter == "全部订单" {
        return true
    }
    if statusFilter == "未完成订单" || statusFilter == "全部状态" {
        return !orderDashboardIsCompleted(stage)
    }
    return stage == statusFilter
}

/// 将已出货和已中止视为列表筛选中的已完成阶段。
/// - Parameters:
///   - stage: 订单或操作的当前阶段标识。
func orderDashboardIsCompleted(_ stage: String) -> Bool {
    stage == "已出货" || stage == "已中止"
}

/// 为数据异常状态提供校验详情或默认处理建议。
/// - Parameters:
///   - status: 业务状态文字或状态代码。
///   - validationMessage: 订单校验的详细提示。
func orderDashboardStatusHelp(status: String, validationMessage: String) -> String {
    guard status == "数据异常" else { return "" }
    let message = validationMessage.trimmingCharacters(in: .whitespacesAndNewlines)
    return message.isEmpty
        ? "订单数据未能通过校验。请检查订单报表后重新扫描 Server。"
        : message
}

/// 将完成数转换为限制在零到一之间的进度比例。
/// - Parameters:
///   - completed: 该阶段已完成的工厂单数量。
///   - total: 该阶段工厂单总数。
func orderDashboardProgressFraction(completed: Int, total: Int) -> Double {
    guard total > 0 else { return 0 }
    return min(max(Double(completed) / Double(total), 0), 1)
}

/// 将年月日字符串转为中文日期；无法拆分时保留原值。
/// - Parameters:
///   - value: 待解析或显示的业务日期时间字符串。
func orderInstallationDisplayDate(_ value: String) -> String {
    let parts = value.split(separator: "-")
    guard parts.count == 3,
          let month = Int(parts[1]),
          let day = Int(parts[2]) else {
        return value
    }
    return "\(parts[0])年\(month)月\(day)日"
}

/// 提取最早实际安装日期并格式化为摘要。
/// - Parameters:
///   - days: 用于摘要的安装日期与人员记录。
func orderInstallationDateSummary(_ days: [OrderInstallationDay]) -> String {
    guard let date = days.map(\.date).sorted().first else { return "" }
    return orderInstallationDisplayDate(date)
}

/// 提取最早计划安装日期并格式化为摘要。
/// - Parameters:
///   - days: 用于摘要的安装日期与人员记录。
func orderInstallationPlannedDateSummary(_ days: [OrderInstallationDay]) -> String {
    guard let date = days.map(\.date).sorted().first else { return "" }
    return orderInstallationDisplayDate(date)
}

/// 组合非空的计划安装和实际安装日期提示。
/// - Parameters:
///   - planned: 计划安装记录列表。
///   - actual: 实际安装记录列表。
func orderInstallationQuickSummaries(
    planned: [OrderInstallationDay],
    actual: [OrderInstallationDay]
) -> [String] {
    var summaries: [String] = []
    let plannedSummary = orderInstallationPlannedDateSummary(planned)
    if !plannedSummary.isEmpty {
        summaries.append("计划安装 \(plannedSummary)")
    }
    let actualSummary = orderInstallationDateSummary(actual)
    if !actualSummary.isEmpty {
        summaries.append("实际安装 \(actualSummary)")
    }
    return summaries
}

private struct OrderDashboardProgressBar: View {
    let completed: Int
    let total: Int
    let accessibilityTitle: String

    /// 保存阶段完成数、总数和辅助功能名称。
    /// - Parameters:
    ///   - completed: 该阶段已完成的工厂单数量。
    ///   - total: 该阶段工厂单总数。
    ///   - accessibilityTitle: 辅助功能朗读的进度名称。
    init(completed: Int, total: Int, accessibilityTitle: String = "优化进度") {
        self.completed = completed
        self.total = total
        self.accessibilityTitle = accessibilityTitle
    }

    /// 将阶段完成数转换为进度条填充比例。
    private var fraction: Double {
        orderDashboardProgressFraction(completed: completed, total: total)
    }

    /// 按阶段是否全部完成选择进度条颜色。
    private var progressColor: Color {
        completed >= total ? AppPalette.success : AppPalette.warning
    }

    var body: some View {
        GeometryReader { geometry in
            ZStack(alignment: .leading) {
                Capsule()
                    .fill(AppPalette.separator)
                Capsule()
                    .fill(progressColor)
                    .frame(width: geometry.size.width * fraction)
            }
        }
        .frame(width: 76, height: 7)
        .accessibilityElement(children: .ignore)
        .accessibilityLabel(accessibilityTitle)
        .accessibilityValue("\(completed) / \(total)")
    }
}

/// 根据显示选项和 AIMES 待确认、格式警告决定是否打开待处理中心。
/// - Parameters:
///   - presentIfNeeded: 有待处理问题时是否主动打开面板。
///   - pendingAimesReviews: 尚未人工确认的 AIMES 工厂单记录。
///   - aimesFormatWarnings: AIMES 销售单格式异常记录。
func shouldPresentPendingCenterAfterAimes(
    presentIfNeeded: Bool,
    pendingAimesReviews: [AimesReviewItem],
    aimesFormatWarnings: [AimesReviewItem] = []
) -> Bool {
    presentIfNeeded && (!pendingAimesReviews.isEmpty || !aimesFormatWarnings.isEmpty)
}

struct DashboardMessage: Identifiable, Equatable {
    let id: String
    let source: String
    let time: String
    let title: String
    let detail: String
    let state: String
    let manualPaths: [String]
    let operationDetails: [String]
    let contextDetails: [String]
    let duration: TimeInterval?
    let operationDurations: [DashboardOperationDuration]

    /// 建立看板消息并规范化、去重关联的人工处理路径。
    /// - Parameters:
    ///   - id: 记录或请求的唯一标识。
    ///   - source: 看板操作来源键，如 aimes、server、inventory 或 sync。
    ///   - time: 消息或步骤的显示时间。
    ///   - title: 界面或操作记录的标题。
    ///   - detail: 操作或消息的详细说明。
    ///   - state: 运行、成功、警告或失败等展示状态。
    ///   - manualPaths: 消息关联的人工处理路径。
    ///   - operationDetails: 操作执行过程的说明列表。
    ///   - contextDetails: 消息关联的业务上下文说明。
    ///   - duration: 操作耗时，单位为秒。
    ///   - operationDurations: 互不重叠的操作阶段及耗时。
    init(
        id: String,
        source: String,
        time: String,
        title: String,
        detail: String,
        state: String,
        manualPaths: [String] = [],
        operationDetails: [String] = [],
        contextDetails: [String] = [],
        duration: TimeInterval? = nil,
        operationDurations: [DashboardOperationDuration] = []
    ) {
        self.id = id
        self.source = source
        self.time = time
        self.title = title
        self.detail = detail
        self.state = state
        self.manualPaths = Array(Set(manualPaths.filter { !$0.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty })).sorted()
        self.operationDetails = operationDetails
        self.contextDetails = contextDetails
        self.duration = duration
        self.operationDurations = operationDurations
    }
}

struct DashboardOperationDisplay {
    let message: DashboardMessage
    let isRunning: Bool
}

/// 通过状态前缀识别消息的失败、警告、成功或普通状态。
/// - Parameters:
///   - text: 待解析或显示的文本。
func dashboardMessageState(_ text: String) -> String {
    if text.hasPrefix("❌") { return "failure" }
    if text.hasPrefix("⚠️") { return "warning" }
    if text.hasPrefix("✅") { return "success" }
    return "info"
}

/// 去除消息开头的状态图标并清理空白。
/// - Parameters:
///   - text: 待解析或显示的文本。
func dashboardMessageDetail(_ text: String) -> String {
    for marker in ["✅", "⚠️", "❌"] where text.hasPrefix(marker) {
        return String(text.dropFirst(marker.count)).trimmingCharacters(in: .whitespacesAndNewlines)
    }
    return text
}

/// 识别实际运行中的状态文字，排除终态和待处理中心名称。
/// - Parameters:
///   - text: 待解析或显示的文本。
func dashboardStatusIsInProgress(_ text: String) -> Bool {
    if ["✅", "⚠️", "❌"].contains(where: { text.hasPrefix($0) }) { return false }
    // 页面名称包含“处理中”，但不代表正在执行操作。仅去掉该名词，
    // 确保“正在读取待处理中心…”仍被识别为运行中。
    let detail = dashboardMessageDetail(text).replacingOccurrences(of: "待处理中心", with: "")
    return detail.contains("正在") || detail.contains("处理中")
}

/// 优先使用显式消息状态，必要时兼容旧运行文字。
/// - Parameters:
///   - message: 需要解析、记录或显示的业务消息。
func dashboardMessageIsRunning(_ message: DashboardMessage) -> Bool {
    if message.state == "running" { return true }
    // 兼容未显式设置运行状态的旧调用方；终态标记始终优先于文字匹配。
    guard message.state == "info" else { return false }
    return dashboardStatusIsInProgress(message.detail)
}

private let dashboardStatusPlaceholders: Set<String> = [
    "订单数据尚未同步",
    "库存操作尚未执行",
    "AIMES 尚未检查",
    "Server 尚未扫描",
]

/// 合并会话历史和各来源当前状态，去重并保留耗时与上下文详情。
/// - Parameters:
///   - syncStatus: 订单同步当前状态。
///   - syncTime: 订单同步状态发生时间。
///   - inventoryStatus: 库存操作当前状态提示。
///   - inventoryTime: 库存操作状态发生时间。
///   - aimesStatus: AIMES 当前状态提示。
///   - aimesTime: AIMES 状态发生时间。
///   - serverStatus: Server 当前扫描或处理状态。
///   - serverTime: Server 状态发生时间。
///   - activity: 当前订单活动步骤列表。
///   - operationDetailsBySource: 按操作来源归组的执行过程说明。
///   - manualPathsBySource: 按来源归组的人工处理路径。
///   - contextDetailsBySource: 按操作来源归组的业务上下文说明。
///   - durationsBySource: 按操作来源保存的总耗时（秒）。
///   - operationDurationsBySource: 按来源归组的独立阶段耗时。
///   - sessionMessages: 本次会话已记录的消息；为空时从活动列表生成历史。
func dashboardMessages(
    syncStatus: String,
    syncTime: String,
    inventoryStatus: String = "库存操作尚未执行",
    inventoryTime: String = "",
    aimesStatus: String,
    aimesTime: String,
    serverStatus: String,
    serverTime: String,
    activity: [InventoryStep],
    operationDetailsBySource: [String: [String]] = [:],
    manualPathsBySource: [String: [String]] = [:],
    contextDetailsBySource: [String: [String]] = [:],
    durationsBySource: [String: TimeInterval] = [:],
    operationDurationsBySource: [String: [DashboardOperationDuration]] = [:],
    sessionMessages: [DashboardMessage]? = nil
) -> [DashboardMessage] {
    // AIMES 状态也被复制到 syncStatus 时，优先保留 AIMES 消息，
    // 避免后续详情去重丢失其权威耗时、阶段和警告信息。
    let statuses = [
        ("inventory", "库存操作", inventoryStatus, inventoryTime),
        ("aimes", "AIMES", aimesStatus, aimesTime),
        ("server", "Server", serverStatus, serverTime),
        ("sync", "订单数据", syncStatus, syncTime),
    ]
    var seenDetails: Set<String> = []
    var currentStatuses: [DashboardMessage] = []
    for (source, title, rawDetail, time) in statuses {
        let detail = dashboardMessageDetail(rawDetail).trimmingCharacters(in: .whitespacesAndNewlines)
        let state = dashboardStatusIsInProgress(rawDetail) ? "running" : dashboardMessageState(rawDetail)
        guard !detail.isEmpty,
              !dashboardStatusPlaceholders.contains(detail),
              sessionMessages == nil || state == "running",
              seenDetails.insert(detail).inserted else { continue }
        currentStatuses.append(DashboardMessage(
            id: "status:\(source)",
            source: source,
            time: time,
            title: title,
            detail: detail,
            state: state,
            manualPaths: manualPathsBySource[source] ?? [],
            operationDetails: operationDetailsBySource[source] ?? [],
            contextDetails: contextDetailsBySource[source] ?? [],
            duration: durationsBySource[source],
            operationDurations: operationDurationsBySource[source] ?? []
        ))
    }
    currentStatuses.sort { ($0.time, $0.id) < ($1.time, $1.id) }
    let history = sessionMessages ?? activity.reversed().map { step in
        DashboardMessage(
            id: "activity:\(step.id.uuidString)",
            source: "activity",
            time: step.time,
            title: step.title,
            detail: step.detail,
            state: step.state,
            manualPaths: step.paths,
            operationDetails: step.operationDetails,
            contextDetails: step.contextDetails,
            duration: step.duration,
            operationDurations: []
        )
    }
    let combined = history + currentStatuses
    if sessionMessages != nil {
        return combined
    }
    return combined.enumerated()
        .sorted { left, right in
            if left.element.time != right.element.time {
                return left.element.time < right.element.time
            }
            return left.offset < right.offset
        }
        .map(\.element)
}

/// 任务运行时从历史区移除运行中消息，避免与顶部当前操作重复。
/// - Parameters:
///   - messages: 待展示或筛选的看板消息列表。
///   - isRunning: 是否存在正在执行的操作。
func dashboardVisibleMessages(_ messages: [DashboardMessage], isRunning: Bool) -> [DashboardMessage] {
    guard isRunning else { return messages }
    return messages.filter { !dashboardMessageIsRunning($0) }
}

/// 从消息集合中选择顶部当前操作显示内容。
/// - Parameters:
///   - messages: 待展示或筛选的看板消息列表。
///   - isRunning: 是否存在正在执行的操作。
func dashboardCurrentOperation(
    messages: [DashboardMessage],
    isRunning: Bool
) -> DashboardOperationDisplay? {
    if isRunning,
       let running = messages.last(where: dashboardMessageIsRunning) {
        return DashboardOperationDisplay(message: running, isRunning: true)
    }
    if let completed = messages.last(where: { ["success", "warning", "failure"].contains($0.state) }) {
        return DashboardOperationDisplay(message: completed, isRunning: false)
    }
    return messages.last.map { DashboardOperationDisplay(message: $0, isRunning: false) }
}

/// 生成随消息内容变化的滚动定位键。
/// - Parameters:
///   - messages: 待展示或筛选的看板消息列表。
func dashboardMessageScrollKey(_ messages: [DashboardMessage]) -> String {
    messages.map {
        let stageKey = $0.operationDurations
            .map { "\($0.label):\($0.duration)" }
            .joined(separator: ";")
        return "\($0.id)|\($0.time)|\($0.detail)|\($0.operationDetails.joined(separator: "|"))|\($0.contextDetails.joined(separator: "|"))|\($0.duration ?? -1)|\(stageKey)"
    }.joined(separator: "\n")
}

/// 判断消息是否具备可供悬停展示的扩展详情。
/// - Parameters:
///   - message: 需要解析、记录或显示的业务消息。
func dashboardMessageSupportsHoverDetail(_ message: DashboardMessage) -> Bool {
    !dashboardMessageIsRunning(message)
        && (message.state == "warning" || message.state == "failure"
            || !message.manualPaths.isEmpty
            || !message.operationDetails.isEmpty
            || !message.contextDetails.isEmpty
            || !message.operationDurations.isEmpty)
}

/// 在消息正文后附加总耗时和独立阶段耗时。
/// - Parameters:
///   - message: 需要解析、记录或显示的业务消息。
func dashboardMessageDetailText(_ message: DashboardMessage) -> String {
    var detail = message.detail
    if let duration = message.duration {
        detail += "（总用时 \(operationDurationText(duration))）"
    }
    if !message.operationDurations.isEmpty {
        let stages = message.operationDurations.map {
            "\($0.label)：\(operationDurationText($0.duration))"
        }.joined(separator: "；")
        detail += "；阶段：\(stages)"
    }
    return detail
}

/// 生成一行消息摘要，并按选项附加耗时。
/// - Parameters:
///   - message: 需要解析、记录或显示的业务消息。
///   - showsDuration: 是否在步骤或消息中显示耗时。
func dashboardMessageSummaryText(_ message: DashboardMessage, showsDuration: Bool = true) -> String {
    var summary = message.detail
    if showsDuration, let duration = message.duration {
        summary += "（总计用时 \(operationDurationText(duration))）"
    }
    return summary
}

/// 组合工厂单、销售单和原因形成 AIMES 处理说明。
/// - Parameters:
///   - item: AIMES 人工确认记录。
///   - status: 业务状态文字或状态代码。
func dashboardAimesReviewDetail(_ item: AimesReviewItem, status: String) -> String {
    let factoryOrder = item.factoryOrder.isEmpty ? "工厂单号为空" : item.factoryOrder
    let factoryName = item.factoryName.isEmpty ? "名称为空" : item.factoryName
    let salesOrder = item.salesOrderName.isEmpty ? "销售单名称为空" : item.salesOrderName
    var detail = "\(status)：工厂单 \(factoryOrder)，工厂单名称“\(factoryName)”；销售单名称“\(salesOrder)”"
    if !item.reason.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
        detail += "；原因：\(item.reason)"
    }
    return detail
}

/// 分别汇总待确认、已忽略和已指定归属的 AIMES 工厂单。
/// - Parameters:
///   - pending: 尚待人工确认的 AIMES 工厂单。
///   - ignored: 已被人工忽略的 AIMES 工厂单记录。
///   - assigned: 已人工指定订单归属的 AIMES 记录。
func dashboardAimesActionDetails(
    pending: [AimesReviewItem],
    ignored: [AimesReviewItem],
    assigned: [AimesReviewItem]
) -> [String] {
    var details: [String] = []
    if !pending.isEmpty {
        details.append("待人工确认 \(pending.count) 条：")
        details += pending.map { dashboardAimesReviewDetail($0, status: "待确认") }
    }
    if !ignored.isEmpty {
        details.append("已忽略 \(ignored.count) 条：")
        details += ignored.map { dashboardAimesReviewDetail($0, status: "已忽略") }
    }
    if !assigned.isEmpty {
        details.append("已确认 \(assigned.count) 条：")
        details += assigned.map { dashboardAimesReviewDetail($0, status: "已确认归属") }
    }
    return details
}

/// 将 AIMES 警告转换为可展示的逐条详情。
/// - Parameters:
///   - warnings: 后端返回的 AIMES 警告记录。
func dashboardAimesWarningDetails(_ warnings: [[String: Any]]) -> [String] {
    guard !warnings.isEmpty else { return [] }
    var details = ["销售单格式异常 " + String(warnings.count) + " 条，均未写入数据库："]
    details += warnings.map { warning in
        let factoryOrder = warning["factory_order"] as? String ?? "工厂单号为空"
        let factoryName = warning["factory_name"] as? String ?? "名称为空"
        let salesOrder = warning["sales_order_name"] as? String ?? "销售单名称为空"
        let reason = warning["reason"] as? String ?? "销售单名称格式不符合规则"
        let displayedFactoryOrder = factoryOrder.isEmpty ? "工厂单号为空" : factoryOrder
        let displayedFactoryName = factoryName.isEmpty ? "名称为空" : factoryName
        let displayedSalesOrder = salesOrder.isEmpty ? "销售单名称为空" : salesOrder
        return "工厂单 " + displayedFactoryOrder + "，工厂单名称“" + displayedFactoryName + "”；销售单名称“" + displayedSalesOrder + "”；原因：" + reason
    }
    return details
}

private struct DashboardMessageTracePopover: View {
    let message: DashboardMessage

    var body: some View {
        ScrollView {
            VStack(alignment: .leading, spacing: 10) {
                if message.state == "warning" || message.state == "failure" {
                    Text("需要人工处理")
                        .font(.headline)
                        .foregroundColor(AppPalette.warning)
                }
                Text(dashboardMessageDetailText(message))
                    .fixedSize(horizontal: false, vertical: true)
                if !message.operationDurations.isEmpty {
                    Text("后台操作耗时")
                        .font(.headline)
                    ForEach(message.operationDurations) { operation in
                        dashboardTraceBullet("\(operation.label)：\(operationDurationText(operation.duration))")
                    }
                }
                if message.manualPaths.isEmpty {
                    Text("当前消息没有可打开的本地文件路径；请按上面的说明处理。")
                        .font(.caption)
                        .foregroundColor(.secondary)
                } else {
                    Text("相关文件或文件夹")
                        .font(.subheadline.weight(.semibold))
                    ForEach(message.manualPaths, id: \.self) { path in
                        Text(path)
                            .font(.caption.monospaced())
                            .textSelection(.enabled)
                            .lineLimit(3)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
                if !message.operationDetails.isEmpty {
                    Text("自动处理详情")
                        .font(.headline)
                    ForEach(message.operationDetails, id: \.self) { detail in
                        dashboardTraceBullet(detail)
                    }
                }
                if !message.contextDetails.isEmpty {
                    Text("相关处理记录")
                        .font(.headline)
                    ForEach(message.contextDetails, id: \.self) { detail in
                        dashboardTraceBullet(detail)
                    }
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
        .padding(14)
        .frame(width: 520, alignment: .leading)
        .frame(maxHeight: 560, alignment: .leading)
        .background(AppPalette.surface)
    }

    /// 构造消息详情中的项目符号文本行。
    /// - Parameters:
    ///   - text: 待解析或显示的文本。
    private func dashboardTraceBullet(_ text: String) -> some View {
        HStack(alignment: .top, spacing: 7) {
            Text("•")
                .foregroundColor(.secondary)
            Text(text)
                .font(.caption)
                .fixedSize(horizontal: false, vertical: true)
        }
    }
}

private final class DashboardMessageTraceTrackingView: NSView {
    var onMouseEntered: (() -> Void)?
    var onMouseExited: (() -> Void)?

    /// 按当前视图边界重新注册鼠标进入和离开跟踪区域。
    /// 无参数。
    override func updateTrackingAreas() {
        trackingAreas.forEach(removeTrackingArea)
        addTrackingArea(
            NSTrackingArea(
                rect: bounds,
                options: [.mouseEnteredAndExited, .activeAlways, .inVisibleRect],
                owner: self,
                userInfo: nil
            )
        )
        super.updateTrackingAreas()
    }

    /// 将鼠标进入跟踪区域的事件转发给悬停回调。
    /// - Parameters:
    ///   - event: 系统派发的鼠标进入或离开事件。
    override func mouseEntered(with event: NSEvent) {
        onMouseEntered?()
        super.mouseEntered(with: event)
    }

    /// 将鼠标离开跟踪区域的事件转发给悬停回调。
    /// - Parameters:
    ///   - event: 系统派发的鼠标进入或离开事件。
    override func mouseExited(with event: NSEvent) {
        onMouseExited?()
        super.mouseExited(with: event)
    }
}

private struct DashboardMessageTracePanelPresenter: NSViewRepresentable {
    let message: DashboardMessage
    @Binding var isPresented: Bool
    let onPanelEntered: () -> Void
    let onPanelExited: () -> Void

    /// 创建负责 AppKit 事件与 SwiftUI 状态衔接的协调器。
    /// 无参数。
    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    /// 创建用于定位消息悬停详情面板的透明锚点视图。
    /// - Parameters:
    ///   - context: SwiftUI 提供的桥接上下文与协调器。
    func makeNSView(context: Context) -> NSView {
        let view = NSView(frame: .zero)
        view.wantsLayer = true
        return view
    }

    /// 把消息、显示状态和鼠标回调传给详情面板协调器。
    /// - Parameters:
    ///   - nsView: 已创建并需要更新或卸载的 AppKit 视图。
    ///   - context: SwiftUI 提供的桥接上下文与协调器。
    func updateNSView(_ nsView: NSView, context: Context) {
        context.coordinator.update(
            anchorView: nsView,
            message: message,
            isPresented: isPresented,
            onPanelEntered: onPanelEntered,
            onPanelExited: onPanelExited
        )
    }

    /// 在桥接视图卸载时关闭悬停详情面板。
    /// - Parameters:
    ///   - nsView: 已创建并需要更新或卸载的 AppKit 视图。
    ///   - coordinator: 持有事件监听和面板状态的桥接协调器。
    static func dismantleNSView(_ nsView: NSView, coordinator: Coordinator) {
        coordinator.close()
    }

    final class Coordinator: NSObject {
        private var panel: NSPanel?
        private var hostingController: NSHostingController<AnyView>?
        private weak var anchorView: NSView?
        private var message: DashboardMessage?
        private var isPresented = false
        private var onPanelEntered: (() -> Void)?
        private var onPanelExited: (() -> Void)?

        /// 同步悬停锚点、消息和面板回调，按显示状态打开或关闭面板。
        /// - Parameters:
        ///   - anchorView: 决定悬停生命周期的 AppKit 锚点视图。
        ///   - message: 需要解析、记录或显示的业务消息。
        ///   - isPresented: 面板当前的显示状态或其双向绑定。
        ///   - onPanelEntered: 鼠标进入详情面板的回调。
        ///   - onPanelExited: 鼠标离开详情面板的回调。
        func update(
            anchorView: NSView,
            message: DashboardMessage,
            isPresented: Bool,
            onPanelEntered: @escaping () -> Void,
            onPanelExited: @escaping () -> Void
        ) {
            self.anchorView = anchorView
            self.message = message
            self.isPresented = isPresented
            self.onPanelEntered = onPanelEntered
            self.onPanelExited = onPanelExited

            guard isPresented else {
                close()
                return
            }
            presentIfNeeded()
            if panel != nil {
                updatePosition()
            }
        }

        /// 创建或刷新悬停详情面板，并注册位置跟踪。
        /// 无参数。
        private func presentIfNeeded() {
            guard panel == nil,
                  let message,
                  let anchorView,
                  let anchorWindow = anchorView.window,
                  dashboardMessageHoverCanPresent(
                      appIsActive: NSApp.isActive,
                      mainWindowIsFrontmost: anchorWindow.isKeyWindow
                          && (anchorWindow.isMainWindow || NSApp.mainWindow === anchorWindow)
                  ) else { return }
            let hostingController = NSHostingController(
                rootView: AnyView(
                    DashboardMessageTracePopover(
                        message: message
                    )
                )
            )
            let panel = NSPanel(
                contentRect: NSRect(x: 0, y: 0, width: 520, height: 200),
                styleMask: [.borderless, .nonactivatingPanel],
                backing: .buffered,
                defer: true
            )
            panel.isOpaque = false
            panel.backgroundColor = .clear
            panel.hasShadow = true
            panel.isFloatingPanel = true
            panel.level = .floating
            panel.hidesOnDeactivate = false
            panel.becomesKeyOnlyIfNeeded = true
            panel.ignoresMouseEvents = false
            panel.acceptsMouseMovedEvents = true
            hostingController.view.layoutSubtreeIfNeeded()
            let fittingSize = hostingController.view.fittingSize
            let panelSize = NSSize(
                width: 520,
                height: max(120, min(560, fittingSize.height))
            )
            panel.setContentSize(panelSize)

            let trackingView = DashboardMessageTraceTrackingView(
                frame: NSRect(origin: .zero, size: panelSize)
            )
            trackingView.autoresizingMask = [.width, .height]
            trackingView.onMouseEntered = { [weak self] in self?.onPanelEntered?() }
            trackingView.onMouseExited = { [weak self] in self?.onPanelExited?() }
            hostingController.view.translatesAutoresizingMaskIntoConstraints = false
            trackingView.addSubview(hostingController.view)
            NSLayoutConstraint.activate([
                hostingController.view.leadingAnchor.constraint(equalTo: trackingView.leadingAnchor),
                hostingController.view.trailingAnchor.constraint(equalTo: trackingView.trailingAnchor),
                hostingController.view.topAnchor.constraint(equalTo: trackingView.topAnchor),
                hostingController.view.bottomAnchor.constraint(equalTo: trackingView.bottomAnchor),
            ])
            panel.contentView = trackingView

            self.hostingController = hostingController
            self.panel = panel
            updatePosition()
            panel.orderFront(nil)
        }

        /// 依据鼠标与屏幕可用范围放置详情面板，保持行作为悬停生命周期锚点。
        /// 无参数。
        private func updatePosition() {
            guard let panel, let anchorView, anchorView.window != nil else { return }
            // 保持消息行作为悬停生命周期的锚点。下面有意沿用基于鼠标位置的布局；
            // 关闭宽限期和面板跟踪可避免鼠标小幅移动就立即关闭详情。
            let screenPoint = NSEvent.mouseLocation
            let visibleFrame = NSScreen.screens.first(where: { $0.frame.contains(screenPoint) })?.visibleFrame
                ?? NSScreen.main?.visibleFrame
                ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
            let gap: CGFloat = 14
            // 沿用原有定位行为：相对当前鼠标放置面板，在屏幕边缘空间不足时左右翻转；
            // 消息行仍作为悬停生命周期锚点。
            var originX = screenPoint.x + gap
            var originY = screenPoint.y - panel.frame.height - gap
            if originX + panel.frame.width > visibleFrame.maxX {
                originX = screenPoint.x - panel.frame.width - gap
            }
            if originY < visibleFrame.minY {
                originY = screenPoint.y + gap
            }
            originX = min(max(originX, visibleFrame.minX + 8), visibleFrame.maxX - panel.frame.width - 8)
            originY = min(max(originY, visibleFrame.minY + 8), visibleFrame.maxY - panel.frame.height - 8)
            panel.setFrameOrigin(NSPoint(x: originX, y: originY))
        }

        /// 关闭悬停详情面板并释放窗口引用。
        /// 无参数。
        func close() {
            panel?.orderOut(nil)
            panel = nil
            hostingController = nil
        }

        /// 释放协调器时移除事件监听并关闭详情面板。
        /// 无参数。
        deinit {
            close()
        }
    }
}

private struct DashboardMessageTraceHost<Content: View>: View {
    let message: DashboardMessage
    @Binding var activeMessageID: String?
    @ViewBuilder let content: () -> Content
    @State private var anchorHovering = false
    @State private var panelHovering = false
    @State private var showPopover = false
    @State private var hoverGeneration = 0

    var body: some View {
        content()
            // 悬停跟踪区域覆盖整行宽度，不局限于内容的固有宽度。
            .frame(maxWidth: .infinity, alignment: .leading)
            .contentShape(Rectangle())
            .onHover { hovering in
                if hovering {
                    beginHover()
                } else {
                    endHover()
                }
            }
            .onChange(of: activeMessageID) { _, activeID in
                guard activeID != message.id else { return }
                anchorHovering = false
                panelHovering = false
                hoverGeneration += 1
                showPopover = false
            }
            .background(
                DashboardMessageTracePanelPresenter(
                    message: message,
                    isPresented: $showPopover,
                    onPanelEntered: panelEntered,
                    onPanelExited: panelExited
                )
            )
    }

    /// 进入消息行后安排延迟显示，并复用宽限期内的已有面板。
    /// 无参数。
    private func beginHover() {
        guard !anchorHovering else { return }
        let wasPopoverVisible = showPopover
        activeMessageID = message.id
        anchorHovering = true
        hoverGeneration += 1
        if wasPopoverVisible {
            // 关闭宽限期内重新进入消息行时，保留已显示的面板，避免先隐藏再弹出。
            return
        }
        showPopover = false
        let generation = hoverGeneration
        DispatchQueue.main.asyncAfter(deadline: .now() + dashboardMessageHoverDelay) {
            guard generation == hoverGeneration, anchorHovering else { return }
            showPopover = true
        }
    }

    /// 标记已离开消息行并安排延迟关闭详情。
    /// 无参数。
    private func endHover() {
        guard activeMessageID == message.id else { return }
        anchorHovering = false
        hoverGeneration += 1
        schedulePopoverClose()
    }

    /// 当行和面板均未悬停时，在宽限期后关闭详情。
    /// 无参数。
    private func schedulePopoverClose() {
        let generation = hoverGeneration
        DispatchQueue.main.asyncAfter(deadline: .now() + dashboardMessageHoverCloseGrace) {
            guard generation == hoverGeneration, !panelHovering else { return }
            showPopover = false
            if activeMessageID == message.id {
                activeMessageID = nil
            }
        }
    }

    /// 进入详情面板时取消延迟关闭。
    /// 无参数。
    private func panelEntered() {
        guard activeMessageID == nil || activeMessageID == message.id else { return }
        activeMessageID = message.id
        panelHovering = true
        hoverGeneration += 1
    }

    /// 离开详情面板后安排延迟关闭。
    /// 无参数。
    private func panelExited() {
        guard activeMessageID == message.id else { return }
        panelHovering = false
        hoverGeneration += 1
        schedulePopoverClose()
    }
}

// 这是短暂的值快照，不是数据缓存。相等性排除订单选择、材料、五金和详情加载；
// 真正的消息或进度变化仍会触发渲染。
struct OrderDashboardActivityInput: Equatable {
    let pendingServerChanges: [ServerChangePreview]
    let pendingAimesReviews: [AimesReviewItem]
    let ignoredAimesFactories: [AimesReviewItem]
    let assignedAimesFactories: [AimesReviewItem]
    let dashboardActivity: [InventoryStep]
    let dashboardSyncStatus: String
    let dashboardSyncStatusTime: String
    let dashboardInventoryOperationStatus: String
    let dashboardInventoryOperationStatusTime: String
    let dashboardAimesStatus: String
    let dashboardAimesStatusTime: String
    let dashboardServerStatus: String
    let dashboardServerStatusTime: String
    let dashboardOperationDetails: [String: [String]]
    let dashboardOperationProgress: [String: [String]]
    let dashboardOperationDurations: [String: TimeInterval]
    let dashboardOperationStageDurations: [String: [DashboardOperationDuration]]
    let dashboardSessionMessages: [DashboardMessage]
    let inventoryRunning: Bool
    let dashboardOperationStartUptimes: [String: TimeInterval]
    let aimesWarningDetails: [String]

    /// 从 AppModel 提取仅影响消息区域的短暂值快照。
    /// - Parameters:
    ///   - model: 共享的 App 状态及业务命令入口。
    init(model: AppModel) {
        pendingServerChanges = model.pendingServerChanges
        pendingAimesReviews = model.pendingAimesReviews
        ignoredAimesFactories = model.ignoredAimesFactories
        assignedAimesFactories = model.assignedAimesFactories
        dashboardActivity = model.dashboardActivity
        dashboardSyncStatus = model.dashboardSyncStatus
        dashboardSyncStatusTime = model.dashboardSyncStatusTime
        dashboardInventoryOperationStatus = model.dashboardInventoryOperationStatus
        dashboardInventoryOperationStatusTime = model.dashboardInventoryOperationStatusTime
        dashboardAimesStatus = model.dashboardAimesStatus
        dashboardAimesStatusTime = model.dashboardAimesStatusTime
        dashboardServerStatus = model.dashboardServerStatus
        dashboardServerStatusTime = model.dashboardServerStatusTime
        dashboardOperationDetails = model.dashboardOperationDetails
        dashboardOperationProgress = model.dashboardOperationProgress
        dashboardOperationDurations = model.dashboardOperationDurations
        dashboardOperationStageDurations = model.dashboardOperationStageDurations
        dashboardSessionMessages = model.dashboardSessionMessages
        inventoryRunning = model.inventoryRunning
        dashboardOperationStartUptimes = model.dashboardOperationStartUptimes
        aimesWarningDetails = dashboardAimesWarningDetails(model.aimesWarnings)
    }

    /// 合并库存运行标志和各来源状态，判断是否显示当前操作。
    var operationRunning: Bool {
        inventoryRunning || [dashboardSyncStatus, dashboardInventoryOperationStatus,
                             dashboardAimesStatus, dashboardServerStatus]
            .contains(where: dashboardStatusIsInProgress)
    }

    /// 合并各来源操作详情和去重后的实时进度文字。
    var dashboardMessageOperationDetails: [String: [String]] {
        var merged = dashboardOperationDetails
        for (source, progress) in dashboardOperationProgress {
            var details = merged[source] ?? []
            for message in progress where !details.contains(message) { details.append(message) }
            merged[source] = details
        }
        return merged
    }

    /// 按单调时钟计算指定来源操作的已运行秒数。
    /// - Parameters:
    ///   - source: 看板操作来源键，如 aimes、server、inventory 或 sync。
    func dashboardElapsedTime(_ source: String) -> TimeInterval? {
        guard let start = dashboardOperationStartUptimes[source] else { return nil }
        return max(0, ProcessInfo.processInfo.systemUptime - start)
    }
}

#if TESTING
enum OrderDashboardRenderProbe {
    static var messageBodyCount = 0
    /// 记录消息视图正文的求值次数，供渲染隔离测试使用。
    /// 无参数。
    static func recordMessageBody() { messageBodyCount += 1 }
}
#endif

struct OrderDashboardView: View {
    @ObservedObject var model: AppModel
    @State private var searchText = ""
    @State private var statusFilter = "未完成订单"
    @State private var showServerFolderImporter = false

    var body: some View {
        VStack(alignment: .leading, spacing: AppLayout.sectionSpacing) {
            toolbar
            OrderDashboardActivityView(input: OrderDashboardActivityInput(model: model))
                .equatable()
            OrderDashboardListView(
                model: model,
                searchText: $searchText,
                statusFilter: $statusFilter,
                showServerFolderImporter: $showServerFolderImporter
            )
        }
        .frame(maxHeight: .infinity, alignment: .top)
        .padding(AppLayout.contentPadding)
        .appPageFrame()
    }

    private var toolbar: some View {
        HStack(spacing: 10) {
            HStack(spacing: 7) {
                Image(systemName: "magnifyingglass").foregroundColor(.secondary)
                TextField("搜索订单号、工厂单号或工厂单名称", text: $searchText)
                    .textFieldStyle(.plain)
            }
            .padding(.horizontal, 10)
            .frame(width: 360, height: AppLayout.controlHeight)
            .glassEffect(.clear, in: RoundedRectangle(cornerRadius: 14, style: .continuous))

            Menu {
                Button("未完成订单") { statusFilter = "未完成订单" }
                Button("全部订单") { statusFilter = "全部订单" }
                ForEach(orderDashboardStatuses, id: \.self) { status in
                    Button(status) { statusFilter = status }
                }
            } label: {
                HStack(spacing: 7) {
                    Text(statusFilter)
                        .lineLimit(1)
                    Spacer(minLength: 0)
                    Image(systemName: "chevron.up.chevron.down")
                        .font(.caption2.weight(.semibold))
                        .foregroundColor(.secondary)
                }
                .font(.callout.weight(.medium))
                .padding(.horizontal, 11)
                .frame(width: 130, height: AppLayout.controlHeight, alignment: .leading)
                .background(AppPalette.subtleSurface)
                .clipShape(RoundedRectangle(cornerRadius: 14, style: .continuous))
            }
            .menuStyle(.borderlessButton)
            .accessibilityLabel("状态")
            .help("按订单状态筛选")

            Spacer(minLength: 0)
            Button {
                model.syncDashboardAimes(force: true)
            } label: {
                Label("获取 AIMES", systemImage: "arrow.triangle.2.circlepath")
            }
            .appActionButton(minWidth: 126)
            .disabled(model.orderRunning)
            Button {
                model.scanDashboardServer()
            } label: {
                Label("扫描 Server", systemImage: "externaldrive")
            }
            .appActionButton(minWidth: 132)
            .disabled(model.orderRunning)
            Button {
                showServerFolderImporter = true
            } label: {
                Label("处理文件夹", systemImage: "folder.badge.gearshape")
            }
            .appActionButton(minWidth: 132)
            .disabled(model.orderRunning)
        }
    }

}

struct OrderDashboardActivityView: View, Equatable {
    let input: OrderDashboardActivityInput
    @State private var activeMessageID: String?
    @State private var dashboardMessageContentWidth: CGFloat?

    /// 仅比较消息输入快照，判断是否需要重新计算消息视图。
    /// - Parameters:
    ///   - lhs: 等值比较左侧的视图。
    ///   - rhs: 等值比较右侧的视图。
    static func == (lhs: Self, rhs: Self) -> Bool { lhs.input == rhs.input }

    /// 为具备详情的消息包裹悬停面板宿主。
    /// - Parameters:
    ///   - message: 需要解析、记录或显示的业务消息。
    ///   - content: 生成卡片或容器内部视图的闭包。
    @ViewBuilder
    private func traceHost<Content: View>(
        for message: DashboardMessage,
        @ViewBuilder content: @escaping () -> Content
    ) -> some View {
        if dashboardMessageSupportsHoverDetail(message) {
            DashboardMessageTraceHost(
                message: message,
                activeMessageID: $activeMessageID,
                content: content
            )
        } else {
            content()
        }
    }

    var body: some View {
#if TESTING
        let _ = OrderDashboardRenderProbe.recordMessageBody()
#endif
        let serverGroups = serverFolderChangeGroups(input.pendingServerChanges)
        let aimesManualPaths = (
            input.pendingAimesReviews + input.ignoredAimesFactories + input.assignedAimesFactories
        ).map(\.sourcePath)
        let serverManualPaths = input.pendingServerChanges.map(\.path)
        // 同步状态行代表最新警告或错误。仅附上该活动的文件路径，
        // 不要把无关 Server/AIMES 操作的路径汇入悬停消息。
        let latestActivityPaths = input.dashboardActivity.first {
            $0.state == "failure" || $0.state == "warning"
        }?.paths ?? []
        let aimesActionDetails: [String] = dashboardStatusIsInProgress(input.dashboardAimesStatus)
            ? []
            : dashboardAimesActionDetails(
                pending: input.pendingAimesReviews,
                ignored: input.ignoredAimesFactories,
                assigned: input.assignedAimesFactories
            ) + input.aimesWarningDetails
        let serverActionDetails: [String] = {
            if dashboardStatusIsInProgress(input.dashboardServerStatus) {
                return []
            }
            if input.pendingServerChanges.isEmpty {
                return ["Server 已完成扫描，当前没有新增、修改或删除的订单文件。"]
            }
            return ["待处理 Server 变化 \(serverGroups.count) 个文件夹："] + serverGroups.map {
                let handling = $0.manualOnly ? "（临时文件夹）" : ""
                let names = $0.changes.map { displayPathName($0.path) }.joined(separator: "、")
                return "\($0.folderName)\(handling)：\(names)"
            }
        }()
        let messages = dashboardMessages(
            syncStatus: input.dashboardSyncStatus,
            syncTime: input.dashboardSyncStatusTime,
            inventoryStatus: input.dashboardInventoryOperationStatus,
            inventoryTime: input.dashboardInventoryOperationStatusTime,
            aimesStatus: input.dashboardAimesStatus,
            aimesTime: input.dashboardAimesStatusTime,
            serverStatus: input.dashboardServerStatus,
            serverTime: input.dashboardServerStatusTime,
            activity: input.dashboardActivity,
            operationDetailsBySource: input.dashboardMessageOperationDetails,
            manualPathsBySource: [
                "sync": latestActivityPaths,
                "aimes": aimesManualPaths,
                "server": serverManualPaths,
            ],
            contextDetailsBySource: [
                "sync": [],
                "aimes": aimesActionDetails,
                "server": serverActionDetails,
            ],
            durationsBySource: input.dashboardOperationDurations,
            operationDurationsBySource: input.dashboardOperationStageDurations,
            sessionMessages: input.dashboardSessionMessages
        )
        let operationRunning = input.operationRunning
        let visibleMessages = dashboardVisibleMessages(messages, isRunning: operationRunning)
        let currentOperation = dashboardCurrentOperation(messages: messages, isRunning: operationRunning)
        let scrollKey = dashboardMessageScrollKey(visibleMessages)
        return AppSurfaceCard(padding: 0) {
            VStack(spacing: 0) {
                currentOperationRow(currentOperation)
                Divider()
                ScrollViewReader { proxy in
                    ScrollView {
                        LazyVStack(spacing: 0) {
                            if visibleMessages.isEmpty {
                                Text("暂无订单消息")
                                    .font(.body)
                                    .foregroundColor(.secondary)
                                    .frame(maxWidth: .infinity, minHeight: dashboardMessageViewportHeight, alignment: .topLeading)
                                    .padding(12)
                            } else {
                                ForEach(visibleMessages) { message in
                                    traceHost(for: message) {
                                        HStack(alignment: .center, spacing: 10) {
                                        Image(systemName: activityIcon(message.state))
                                            .foregroundColor(activityColor(message.state))
                                            .frame(width: 20, height: 22)
                                        VStack(alignment: .leading, spacing: 1) {
                                            HStack(spacing: 10) {
                                                Text(message.title)
                                                    .font(.callout.weight(.semibold))
                                                Spacer(minLength: 0)
                                                Text(message.time)
                                                    .font(.caption.monospacedDigit())
                                                    .foregroundColor(.secondary)
                                            }
                                            Text(dashboardMessageDetailText(message))
                                                .font(.callout)
                                                .foregroundColor(message.state == "failure" ? AppPalette.danger : .primary)
                                                .lineLimit(message.operationDurations.isEmpty ? 1 : nil)
                                        }
                                        }
                                        .padding(.horizontal, 12)
                                        .frame(minHeight: dashboardMessageRowHeight)
                                    }
                                    .id(message.id)
                                    if message.id != visibleMessages.last?.id { Divider() }
                                }
                            }
                        }
                        .onGeometryChange(for: CGFloat.self) { geometry in
                            geometry.size.width
                        } action: { width in
                            dashboardMessageContentWidth = width
                        }
                    }
                    .frame(height: dashboardMessageViewportHeight)
                    .onAppear { scrollMessagesToBottom(proxy, messages: messages) }
                    .onChange(of: scrollKey) { _, _ in
                        scrollMessagesToBottom(proxy, messages: messages)
                    }
                }
            }
        }
        // 标题和历史共用同一玻璃背景及外轮廓。
        .clipShape(RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius, style: .continuous))
    }

    /// 构造顶部当前操作行，显示状态和运行耗时。
    /// - Parameters:
    ///   - display: 当前操作消息及运行状态。
    @ViewBuilder
    private func currentOperationRow(_ display: DashboardOperationDisplay?) -> some View {
        if let display {
            HStack(spacing: 10) {
                currentOperationIcon(display)
                Text(display.isRunning ? "当前操作" : "最近结果")
                    .font(.callout.weight(.semibold))
                Text(dashboardMessageSummaryText(display.message, showsDuration: !display.isRunning))
                    .font(.callout)
                    .lineLimit(1)
                Spacer(minLength: 0)
                if display.isRunning {
                    TimelineView(.periodic(from: .now, by: 1)) { _ in
                        if let elapsed = input.dashboardElapsedTime(display.message.source) {
                            Text("已用 \(operationDurationText(elapsed))")
                                .font(.caption.monospacedDigit()).foregroundColor(.secondary)
                        }
                    }
                } else {
                    Text(display.message.time)
                        .font(.caption.monospacedDigit()).foregroundColor(.secondary)
                }
            }
            .padding(.horizontal, 12)
            .frame(width: dashboardMessageContentWidth, height: 44)
            .frame(maxWidth: .infinity, alignment: .leading)
        } else {
            HStack(spacing: 10) {
                Image(systemName: "pause.circle.fill").foregroundColor(.secondary)
                Text("当前无正在进行的操作").font(.callout).foregroundColor(.secondary)
                Spacer()
            }
            .padding(.horizontal, 12)
            .frame(height: 44)
        }
    }

    /// 按当前操作的运行或结束状态选择图标。
    /// - Parameters:
    ///   - display: 当前操作消息及运行状态。
    @ViewBuilder
    private func currentOperationIcon(_ display: DashboardOperationDisplay) -> some View {
        if display.isRunning {
            TimelineView(.animation) { context in
                let degrees = context.date.timeIntervalSinceReferenceDate
                    .truncatingRemainder(dividingBy: 1) * 360
                Image(systemName: "arrow.triangle.2.circlepath.circle.fill")
                    .foregroundColor(AppPalette.accent)
                    .rotationEffect(.degrees(degrees))
                    .frame(width: 20)
                    .accessibilityLabel("操作进行中")
            }
        } else {
            Image(systemName: activityIcon(display.message.state))
                .foregroundColor(activityColor(display.message.state))
                .frame(width: 20)
        }
    }

    /// 在消息变化后滚动到最新一条消息。
    /// - Parameters:
    ///   - proxy: 控制消息滚动位置的代理。
    ///   - messages: 待展示或筛选的看板消息列表。
    private func scrollMessagesToBottom(_ proxy: ScrollViewProxy, messages: [DashboardMessage]) {
        guard let lastID = messages.last?.id else { return }
        DispatchQueue.main.async {
            proxy.scrollTo(lastID, anchor: .bottom)
        }
    }

    /// 将活动状态映射到系统图标名称。
    /// - Parameters:
    ///   - state: 运行、成功、警告或失败等展示状态。
    private func activityIcon(_ state: String) -> String {
        switch state {
        case "failure": return "xmark.circle.fill"
        case "warning": return "exclamationmark.triangle.fill"
        case "success": return "checkmark.circle.fill"
        default: return "info.circle.fill"
        }
    }

    /// 将活动状态映射到对应的强调颜色。
    /// - Parameters:
    ///   - state: 运行、成功、警告或失败等展示状态。
    private func activityColor(_ state: String) -> Color {
        switch state {
        case "failure": return AppPalette.danger
        case "warning": return AppPalette.warning
        case "success": return AppPalette.success
        default: return AppPalette.accent
        }
    }

}

struct OrderDashboardListView: View {
    @ObservedObject var model: AppModel
    @State private var expandedOrderID: String?
    @State private var detailOrder: OrderDashboardItem?
    @State private var orderArrangementOrder: OrderDashboardItem?
    @State private var selectedFactoryID: String?
    @State private var selectedFactoryIDs: Set<String> = []
    @Binding var searchText: String
    @Binding var statusFilter: String
    @State private var showFactoryStock = false
    @State private var showManualHardware = false
    @State private var showProductionSheet = false
    @State private var pendingShipment: OrderShipmentRequest?
    @State private var showOutboundScope = false
    @Binding var showServerFolderImporter: Bool

    /// 按搜索词与阶段筛选当前订单列表。
    private var filteredOrders: [OrderDashboardItem] {
        let query = searchText.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        return model.dashboardOrders.filter { item in
            let factoryText = item.factories.map { "\($0.factoryOrder) \($0.orderName)" }.joined(separator: " ")
            let matchesQuery = query.isEmpty || item.orderId.lowercased().contains(query) || item.sourceFolder.lowercased().contains(query) || factoryText.lowercased().contains(query)
            let matchesStatus = orderDashboardStageMatchesFilter(item.stage, statusFilter: statusFilter)
            return matchesQuery && matchesStatus
        }
    }

    /// 取得当前选择的工厂单预览。
    private var selectedFactory: OrderFactoryPreview? {
        model.orderFactories.first { $0.factoryOrder == selectedFactoryID }
    }

    /// 取得当前订单中有可用五金的工厂单集合。
    private var availableHardwareFactoryOrders: Set<String> {
        Set(
            model.orderFittings
                .filter { $0.quantity > 0 }
                .map { $0.factoryOrder }
        )
    }

    var body: some View {
        orderTable
        .onAppear {
            model.startOrderDashboard()
            openRequestedOrderIfAvailable()
        }
        .onChange(of: model.dashboardOrders.map(\.id)) { _, _ in
            openRequestedOrderIfAvailable()
        }
        .sheet(item: $detailOrder) { item in
            OrderDashboardDetailPage(
                model: model,
                order: item
            )
            .frame(minWidth: 960, minHeight: 680)
        }
        .sheet(item: $orderArrangementOrder) { item in
            OrderAnnotationsSheet(model: model, order: item)
        }
        .sheet(isPresented: $model.showCostSheet) {
            OrderCostSheet(model: model)
                .frame(minWidth: 780, idealWidth: 980, minHeight: 560, idealHeight: 720)
        }
        .sheet(isPresented: $showFactoryStock) {
            FactoryStockComparisonSheet(
                model: model,
                orderID: model.selectedOrderId
            )
            .frame(minWidth: 760, idealWidth: 900, minHeight: 520, idealHeight: 640)
        }
        .sheet(isPresented: $showManualHardware) {
            ManualHardwareSheet(model: model, orderID: model.selectedOrderId)
        }
        .sheet(isPresented: $showProductionSheet) {
            ProductionSheet(
                model: model,
                orderID: model.selectedOrderId,
                factoryOrders: selectedFactoryIDs.sorted(),
                onClose: { showProductionSheet = false }
            )
            .frame(width: 620, height: 560)
        }
        .sheet(item: $pendingShipment) { request in
            OrderShipmentConfirmationSheet(
                model: model,
                orderID: request.orderID,
                factoryOrders: request.factoryOrders,
                onCancel: { pendingShipment = nil },
                onConfirm: {
                    pendingShipment = nil
                    model.startDirectOrderShipment(
                        orderID: request.orderID,
                        factoryOrders: request.factoryOrders
                    )
                }
            )
            .frame(width: 620, height: 560)
        }
        .sheet(isPresented: $showOutboundScope) {
            OutboundScopeSheet(
                model: model,
                orderID: model.selectedOrderId,
                orderType: model.dashboardOrders.first(where: { $0.orderId == model.selectedOrderId })?.orderType ?? "owned",
                factoryOrders: selectedFactoryIDs.sorted().filter { availableHardwareFactoryOrders.contains($0) },
                hardwareFactoryOrders: availableHardwareFactoryOrders
            )
            .frame(width: 520, height: 430)
        }
        .alert(
            "AIMES 获取失败",
            isPresented: Binding(
                get: { !model.aimesFailureAlert.isEmpty },
                set: { if !$0 { model.aimesFailureAlert = "" } }
            )
        ) {
            Button("知道了") { model.aimesFailureAlert = "" }
        } message: {
            Text("本次未能获取最新 AIMES 数据，Server 扫描将继续使用最近一次成功缓存。\n\n\(model.aimesFailureAlert)")
        }
        .fileImporter(
            isPresented: $showServerFolderImporter,
            allowedContentTypes: [.folder],
            allowsMultipleSelection: false
        ) { result in
            guard case .success(let urls) = result, let folder = urls.first else { return }
            model.prepareSelectedServerFolder(folder)
        }
        .sheet(isPresented: $model.showServerProcessingOptions) {
            ServerProcessingOptionsSheet(model: model)
                .frame(width: 520, height: 300)
        }
    }

    private var orderTable: some View {
        GeometryReader { geometry in
            let layout = OrderDashboardTableLayout(totalWidth: geometry.size.width)
            AppSurfaceCard(padding: 0) {
                VStack(spacing: 0) {
                    orderTableHeader(layout: layout)
                    Divider()
                    ScrollView {
                        LazyVStack(spacing: 0) {
                            if filteredOrders.isEmpty {
                                VStack(spacing: 8) {
                                    Image(systemName: "magnifyingglass")
                                        .font(.title2)
                                        .foregroundColor(.secondary)
                                    Text("没有符合条件的订单").fontWeight(.semibold)
                                    Text("请调整搜索或状态筛选条件").font(.caption).foregroundColor(.secondary)
                                }
                                .frame(maxWidth: .infinity, minHeight: 220)
                            } else {
                                ForEach(Array(filteredOrders.enumerated()), id: \.element.id) { index, item in
                                    let isLastRow = index == filteredOrders.count - 1
                                    orderRow(item, isLastRow: isLastRow, layout: layout)
                                    if !isLastRow { Divider() }
                                }
                            }
                        }
                        .frame(width: layout.containerWidth, alignment: .leading)
                    }
                    .frame(maxHeight: .infinity)
                }
                .clipShape(RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius, style: .continuous))
            }
            .frame(width: layout.containerWidth, alignment: .leading)
            .frame(maxHeight: .infinity, alignment: .topLeading)
            .clipShape(RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius, style: .continuous))
            .mask(RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius, style: .continuous))
        }
        .frame(maxHeight: .infinity)
    }

    /// 按统一列布局构造订单表格表头。
    /// - Parameters:
    ///   - layout: 订单表格各列的计算宽度。
    private func orderTableHeader(layout: OrderDashboardTableLayout) -> some View {
        HStack(spacing: 0) {
            LazyVGrid(columns: layout.columns, spacing: 0) {
                Color.clear
                tableHeader("订单", width: layout.flexibleColumnWidth)
                tableHeader("状态", width: layout.flexibleColumnWidth)
                tableHeader("工厂单", width: orderDashboardFactoryCountColumnWidth)
                tableHeader("材料", width: layout.flexibleColumnWidth)
                tableHeader("优化进度", width: layout.flexibleColumnWidth)
                tableHeader("生产进度", width: layout.flexibleColumnWidth)
                tableHeader("出货进度", width: layout.flexibleColumnWidth)
                tableHeader("更新时间", width: orderDashboardUpdatedAtColumnWidth)
                tableHeader("操作", width: orderDashboardOperationColumnWidth)
            }
            .frame(width: layout.totalWidth)
            Color.clear.frame(width: layout.trailingSpacerWidth)
        }
        .frame(width: layout.containerWidth, alignment: .leading)
        .font(.caption.weight(.semibold))
        .foregroundColor(.secondary)
        .padding(.vertical, 11)
        .background(AppPalette.subtleSurface)
        .clipShape(
            UnevenRoundedRectangle(
                cornerRadii: .init(
                    topLeading: AppLayout.cardCornerRadius,
                    bottomLeading: 0,
                    bottomTrailing: 0,
                    topTrailing: AppLayout.cardCornerRadius
                ),
                style: .continuous
            )
        )
        // 不要让表格的弹性高度建议值拉伸表头。
        .fixedSize(horizontal: true, vertical: true)
    }

    /// 显示订单数据、进度及操作，并绑定行选择与详情入口。
    /// - Parameters:
    ///   - item: 订单看板记录。
    ///   - isLastRow: 是否为最后一行，用于控制分隔样式。
    ///   - layout: 订单表格各列的计算宽度。
    private func orderRow(
        _ item: OrderDashboardItem,
        isLastRow: Bool = false,
        layout: OrderDashboardTableLayout
    ) -> some View {
        let isExpanded = expandedOrderID == item.orderId
        let isSelected = model.selectedOrderId.caseInsensitiveCompare(item.orderId) == .orderedSame
            && model.selectedOrderPath == item.sourceFolder
        let status = item.stage
        let rowShape = UnevenRoundedRectangle(
            cornerRadii: .init(
                topLeading: 0,
                bottomLeading: isLastRow && !isExpanded ? AppLayout.cardCornerRadius : 0,
                bottomTrailing: isLastRow && !isExpanded ? AppLayout.cardCornerRadius : 0,
                topTrailing: 0
            ),
            style: .continuous
        )
        return VStack(spacing: 0) {
            HStack(spacing: 0) {
                ZStack(alignment: .leading) {
                    LazyVGrid(columns: layout.dataColumns, spacing: 0) {
                    Image(systemName: isExpanded ? "chevron.down" : "chevron.right")
                        .frame(width: 28, height: 28)
                        .frame(width: orderDashboardLeadingColumnWidth)

                    tableCell(width: layout.flexibleColumnWidth) {
                        VStack(spacing: 3) {
                            Text(item.orderId).font(.headline).foregroundColor(AppPalette.accent)
                            Text(item.orderType == "cutToSize" ? "来料加工" : (item.orderType == "temporary" ? "临时任务" : "自有订单"))
                                .font(.caption2).foregroundColor(.secondary)
                            if !item.userNote.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty {
                                Label(item.userNote.trimmingCharacters(in: .whitespacesAndNewlines), systemImage: "note.text")
                                    .font(.caption2)
                                    .foregroundColor(AppPalette.accent)
                                    .lineLimit(1)
                                    .help(item.userNote)
                            }
                            ForEach(
                                orderInstallationQuickSummaries(
                                    planned: item.plannedInstallationDays,
                                    actual: item.actualInstallationDays
                                ),
                                id: \.self
                            ) { installation in
                                Label(installation, systemImage: "calendar")
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                                    .lineLimit(1)
                            }
                        }
                    }
                    tableCell(width: layout.flexibleColumnWidth) {
                        AppStatusBadge(text: status, kind: statusKind(status))
                            .help(orderDashboardStatusHelp(
                                status: status,
                                validationMessage: item.validationMessage
                            ))
                    }
                    tableCell(width: orderDashboardFactoryCountColumnWidth) {
                        Text(item.factoryCount > 0 ? "\(item.factoryCount)" : "—")
                            .fontWeight(.semibold)
                    }
                    tableCell(width: layout.flexibleColumnWidth) {
                        VStack(spacing: 4) {
                            Text(item.materialStatus)
                        }
                    }
                    tableCell(width: layout.flexibleColumnWidth) {
                        VStack(spacing: 4) {
                            Text(item.optimizationProgress)
                                .fontWeight(.semibold)
                            if item.factoryCount > 0 {
                                OrderDashboardProgressBar(
                                    completed: item.optimizedCount,
                                    total: item.factoryCount
                                )
                            }
                        }
                    }
                    tableCell(width: layout.flexibleColumnWidth) {
                        VStack(spacing: 4) {
                            Text(item.productionProgress)
                                .fontWeight(.semibold)
                            if item.factoryCount > 0 {
                                OrderDashboardProgressBar(
                                    completed: item.producedCount,
                                    total: item.factoryCount,
                                    accessibilityTitle: "生产进度"
                                )
                            }
                        }
                    }
                    tableCell(width: layout.flexibleColumnWidth) {
                        VStack(spacing: 3) {
                            Text(item.outboundProgress)
                            if item.factoryCount > 0 {
                                OrderDashboardProgressBar(
                                    completed: item.shippedCount,
                                    total: item.factoryCount,
                                    accessibilityTitle: "出货进度"
                                )
                            }
                        }
                    }
                    tableCell(width: orderDashboardUpdatedAtColumnWidth) {
                        Text(item.modifiedAt.isEmpty ? "—" : appDisplayTimestamp(item.modifiedAt)).lineLimit(1)
                    }
                    }
                    .frame(width: layout.dataWidth, alignment: .leading)
                    OrderDashboardClickContainer(
                        onSingleClick: { toggleExpanded(item) },
                        onDoubleClick: { openOrderDetail(item) }
                    ) {
                        Color.clear
                    }
                    .frame(width: layout.dataWidth, alignment: .leading)
                    .frame(maxHeight: .infinity)
                }
                .frame(width: layout.dataWidth, alignment: .leading)
                .padding(.vertical, 11)

                // 将操作按钮放在行级手势识别区域之外。
                tableCell(width: orderDashboardOperationColumnWidth) {
                    HStack(spacing: 8) {
                        Button("详情") {
                            openOrderDetail(item)
                        }
                        .buttonStyle(.borderless)
                        .foregroundColor(AppPalette.accent)

                        Button("订单安排") {
                            orderArrangementOrder = item
                        }
                        .buttonStyle(.borderless)
                        .foregroundColor(AppPalette.accent)
                        .help("打开订单说明和安装日期")
                    }
                }
                .frame(width: orderDashboardOperationColumnWidth)
                .padding(.vertical, 11)
                Color.clear.frame(width: layout.trailingSpacerWidth)
            }
            .frame(width: layout.containerWidth, alignment: .leading)
            .background(isSelected ? AppPalette.accent.opacity(0.045) : AppPalette.surface)
            .clipShape(rowShape)
            .contentShape(rowShape)

            if isExpanded {
                OrderDashboardDetailCard(
                    model: model,
                    dashboardFactories: item.factories,
                    selectedFactoryID: $selectedFactoryID,
                    selectedFactoryIDs: $selectedFactoryIDs,
                    onQueryStock: { showFactoryStock = true; model.checkSelectedOrderStock() },
                    onOpenProduction: {
                        showProductionSheet = true
                    },
                    onOpenOutbound: {
                        pendingShipment = OrderShipmentRequest(
                            orderID: item.orderId,
                            factoryOrders: selectedFactoryIDs.sorted()
                        )
                    },
                    onOpenScope: { showOutboundScope = true },
                    onOpenManualHardware: { showManualHardware = true },
                    orderType: item.orderType,
                    isCompletedOrder: orderDashboardIsCompleted(item.stage),
                    orderID: item.orderId,
                    isAborted: item.stage == "已中止"
                )
                .padding(.horizontal, 12)
                .padding(.bottom, 12)
            }
        }
    }

    /// 同步所选订单身份并请求数据库详情。
    /// - Parameters:
    ///   - item: 订单看板记录。
    private func prepareSelectedOrder(_ item: OrderDashboardItem) {
        selectedFactoryID = nil
        selectedFactoryIDs = []
        model.selectedOrderIsOptimized = item.stage == "已优化"
        model.selectedOrderIsCompleted = orderDashboardIsCompleted(item.stage)
        model.loadOrderDetailFromDatabase(item)
    }

    /// 切换订单展开状态并准备对应详情。
    /// - Parameters:
    ///   - item: 订单看板记录。
    private func toggleExpanded(_ item: OrderDashboardItem) {
        let next = orderDashboardExpandedID(current: expandedOrderID, tapped: item.orderId)
        expandedOrderID = next
        guard next != nil else { return }
        prepareSelectedOrder(item)
    }

    /// 选择订单并打开订单详情面板。
    /// - Parameters:
    ///   - item: 订单看板记录。
    private func openOrderDetail(_ item: OrderDashboardItem) {
        prepareSelectedOrder(item)
        detailOrder = item
    }

    /// 响应跨页面定位请求，在当前列表找到订单后打开详情。
    /// 无参数。
    private func openRequestedOrderIfAvailable() {
        let orderID = model.requestedOrderCenterOrderID.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !orderID.isEmpty,
              let item = model.dashboardOrders.first(where: {
                  $0.orderId.caseInsensitiveCompare(orderID) == .orderedSame
              }) else { return }
        model.requestedOrderCenterOrderID = ""
        searchText = item.orderId
        statusFilter = orderDashboardIsCompleted(item.stage) ? item.stage : "未完成订单"
        expandedOrderID = nil
    }

    /// 构造指定宽度的订单表格标题单元格。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - width: 单元格或容器宽度，单位为逻辑点。
    private func tableHeader(_ title: String, width: CGFloat) -> some View {
        Text(title)
            .frame(minWidth: width, idealWidth: width, maxWidth: width, alignment: .center)
            .offset(x: (orderDashboardDataHeaderTitles.contains(title) ? orderDashboardDataHeaderOffset : 0) - 5)
    }

    /// 为订单表格内容应用统一宽度和对齐方式。
    /// - Parameters:
    ///   - width: 单元格或容器宽度，单位为逻辑点。
    ///   - content: 生成卡片或容器内部视图的闭包。
    private func tableCell<Content: View>(width: CGFloat, @ViewBuilder content: () -> Content) -> some View {
        content()
            .frame(minWidth: width, idealWidth: width, maxWidth: width, alignment: .center)
            .multilineTextAlignment(.center)
    }

    /// 将订单状态映射为状态徽章类型。
    /// - Parameters:
    ///   - status: 业务状态文字或状态代码。
    private func statusKind(_ status: String) -> AppStatusBadge.Kind {
        switch status {
        case "已优化", "已生产", "部分生产", "部分出货", "部分生产，部分出货", "已出货": return .info
        case "数据异常": return .danger
        case "部分优化", "待确认": return .warning
        default: return .neutral
        }
    }
}

private struct OrderShipmentRequest: Identifiable {
    let id = UUID()
    let orderID: String
    let factoryOrders: [String]
}

struct OrderDashboardMetricsView: View {
    @ObservedObject var model: AppModel

    var body: some View {
        let shortageCount = orderDashboardShortageCount(model.orderStockRows)
        LazyVGrid(columns: orderDashboardMetricColumns, spacing: orderDashboardMetricSpacing) {
            metric("全部订单", "\(model.dashboardOrders.count)", .primary)
            metric("已设计", "\(model.dashboardOrders.filter { $0.stage == "已设计" }.count)", .secondary)
            metric("待优化", "\(model.dashboardOrders.filter { $0.stage == "已拆单待优化" || $0.stage == "部分优化" }.count)", .secondary)
            metric("已优化", "\(model.dashboardOrders.filter { $0.stage == "已优化" || $0.stage == "部分出货" || $0.stage == "已出货" }.count)", AppPalette.accent)
            metric("库存不足", "\(shortageCount)", shortageCount > 0 ? AppPalette.danger : AppPalette.success)
            metric("部分出货", "\(model.dashboardOrders.filter { $0.stage == "部分出货" }.count)", AppPalette.warning)
            metric("已出货", "\(model.dashboardOrders.filter { $0.stage == "已出货" }.count)", AppPalette.success)
            metric("数据异常", "\(model.dashboardOrders.filter { $0.stage == "数据异常" || $0.stage == "待确认" }.count)", model.dashboardOrders.contains { $0.stage == "数据异常" || $0.stage == "待确认" } ? AppPalette.danger : .primary)
        }
        .onAppear { model.startOrderDashboard() }
    }

    /// 构造订单摘要的标题、数值和颜色组合。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - value: 需要显示的数值或状态文字。
    ///   - color: 界面使用的强调颜色。
    private func metric(_ title: String, _ value: String, _ color: Color) -> some View {
        AppSurfaceCard(padding: 12) {
            VStack(alignment: .leading, spacing: 5) {
                Text(title).font(.caption).foregroundColor(.secondary)
                Text(value).font(.title2.weight(.semibold)).foregroundColor(color)
            }
            .frame(maxWidth: .infinity, minHeight: 62, alignment: .leading)
        }
    }
}

struct OrderDashboardDetailPage: View {
    @ObservedObject var model: AppModel
    let order: OrderDashboardItem
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        GeometryReader { geometry in
            VStack(alignment: .leading, spacing: 14) {
                orderIdentityCard
                ScrollView(.vertical) {
                    VStack(alignment: .leading, spacing: 14) {
                        if model.orderDetailWaiting,
                           model.selectedOrderId.caseInsensitiveCompare(order.orderId) == .orderedSame {
                            AppSurfaceCard(padding: 12) {
                                HStack(spacing: 10) {
                                    ProgressView().controlSize(.small)
                                    Text("正在扫描，扫描完成后自动读取详情")
                                        .foregroundColor(.secondary)
                                    Spacer(minLength: 0)
                                }
                            }
                        }
                        boardAndEdgeSection
                        hardwareSection
                    }
                    .frame(maxWidth: .infinity, alignment: .topLeading)
                }
                .scrollIndicators(.automatic)
                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
            }
            .frame(
                width: min(max(0, geometry.size.width - AppLayout.contentPadding * 2), 1120),
                height: max(0, geometry.size.height - AppLayout.contentPadding * 2),
                alignment: .top
            )
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
            .padding(.vertical, AppLayout.contentPadding)
        }
        .appPageFrame()
    }

    private var orderIdentityCard: some View {
        return HStack(alignment: .center, spacing: 12) {
            HStack(spacing: 10) {
                Text("订单 (\(order.orderId))")
                    .font(.title2.weight(.semibold))
                AppStatusBadge(text: order.stage, kind: order.stage == "数据异常" ? .danger : .info)
            }
            Spacer(minLength: 0)
            HStack(spacing: 8) {
                Button("生成 Traveler") { model.generateSelectedOrder() }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 112)
                    .disabled(!model.orderCanGenerateTraveler)
                Button("关闭") { dismiss() }
                    .appActionButton(minWidth: 80)
            }
        }
        .frame(maxWidth: .infinity, minHeight: 42, alignment: .leading)
        .padding(.horizontal, 10)
    }

    private var boardAndEdgeSection: some View {
        AppSurfaceCard(padding: 14) {
            VStack(alignment: .leading, spacing: 12) {
                Text("板材与封边")
                    .font(.headline)
                    .foregroundColor(AppPalette.accent)
                if model.orderMaterials.isEmpty && model.orderEdgeBanding.isEmpty {
                    Text("数据库中暂无材料明细")
                        .foregroundColor(.secondary)
                } else {
                    materialRow(title: "Plywood", rows: orderDetailPlywoodRows(model.orderMaterials))
                    materialRow(title: "Panel", rows: orderDetailPanelRows(model.orderMaterials))
                    edgeBandingRow
                }
            }
        }
    }

    /// 按材料类别绘制详情行及适用的厚度提示。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - rows: 订单材料预览列表。
    @ViewBuilder
    private func materialRow(title: String, rows: [OrderMaterialPreview]) -> some View {
        if !rows.isEmpty {
            VStack(alignment: .leading, spacing: 6) {
                Text(title)
                    .font(.subheadline.weight(.semibold))
                    .foregroundColor(.secondary)
                LazyVGrid(
                    columns: Array(repeating: GridItem(.flexible(), spacing: 10), count: orderDetailGridColumnCount),
                    alignment: .leading,
                    spacing: 10
                ) {
                    ForEach(rows) { row in
                        orderDetailCard(
                            name: orderMaterialDisplayName(row),
                            subtitle: "\(row.thickness.formatted())mm",
                            value: row.quantity.formatted(),
                            panelMaterial: row.kind == "panel" ? row : nil
                        )
                    }
                }
            }
        }
    }

    @ViewBuilder
    private var edgeBandingRow: some View {
        let colors = orderDetailEdgeColors(Array(model.orderEdgeBanding.keys))
        if !colors.isEmpty {
            VStack(alignment: .leading, spacing: 6) {
                Text("封边条")
                    .font(.subheadline.weight(.semibold))
                    .foregroundColor(.secondary)
                LazyVGrid(
                    columns: Array(repeating: GridItem(.flexible(), spacing: 10), count: orderDetailGridColumnCount),
                    alignment: .leading,
                    spacing: 10
                ) {
                    ForEach(colors, id: \.self) { color in
                        orderDetailCard(
                            name: color.isEmpty ? "封边" : color,
                            subtitle: "Edge Banding",
                            value: "\((model.orderEdgeBanding[color] ?? 0).formatted()) m"
                        )
                    }
                }
            }
        }
    }

    private var hardwareSection: some View {
        AppSurfaceCard(padding: 14) {
            VStack(alignment: .leading, spacing: 12) {
                Text("五金")
                    .font(.headline)
                    .foregroundColor(AppPalette.accent)
                VStack(alignment: .leading, spacing: 12) {
                    if model.orderFactories.isEmpty {
                        hardwareFactorySection(title: "暂无工厂单", rows: [])
                    } else {
                        ForEach(model.orderFactories) { factory in
                            hardwareFactorySection(
                                title: "\(factory.factoryOrder) · \(factory.orderName)",
                                rows: model.orderFittings.filter { $0.factoryOrder == factory.factoryOrder }
                            )
                        }
                    }
                }
            }
        }
    }

    /// 按工厂单显示五金明细分组。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - rows: 工厂单五金预览列表。
    private func hardwareFactorySection(title: String, rows: [OrderFittingPreview]) -> some View {
        VStack(alignment: .leading, spacing: 6) {
            Text(title)
                .font(.subheadline.weight(.semibold))
                .foregroundColor(.secondary)
            LazyVGrid(
                columns: Array(repeating: GridItem(.flexible(), spacing: 10), count: orderDetailGridColumnCount),
                alignment: .leading,
                spacing: 10
            ) {
                if rows.isEmpty {
                    orderDetailCard(name: "暂无五金", subtitle: "", value: "—")
                } else {
                    ForEach(rows) { row in
                        orderDetailCard(
                            name: row.displayName.isEmpty
                                ? (row.name.isEmpty ? row.code : row.name)
                                : row.displayName,
                            subtitle: "",
                            value: row.quantity.formatted()
                        )
                    }
                }
            }
        }
    }

    /// 构造材料详情卡片，可附带 Panel 图片悬停入口。
    /// - Parameters:
    ///   - name: 来源材料或五金的名称。
    ///   - subtitle: 卡片副标题或规格说明。
    ///   - value: 需要显示的数值或状态文字。
    ///   - panelMaterial: 可选的 Panel 材料，用于图片悬停预览。
    private func orderDetailCard(
        name: String,
        subtitle: String,
        value: String,
        panelMaterial: OrderMaterialPreview? = nil
    ) -> some View {
        HStack(spacing: 8) {
            VStack(alignment: .leading, spacing: 3) {
                if let panelMaterial {
                    PanelMaterialHoverPreview(material: panelMaterial) {
                        Text(name)
                            .fontWeight(.semibold)
                            .lineLimit(2)
                    }
                } else {
                    Text(name)
                        .fontWeight(.semibold)
                        .lineLimit(2)
                }
                if !subtitle.isEmpty {
                    Text(subtitle)
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
            Spacer(minLength: 4)
            Text(value)
                .font(.title3.weight(.semibold))
                .foregroundColor(AppPalette.accent)
                .lineLimit(1)
        }
        .padding(10)
        .frame(maxWidth: .infinity, minHeight: orderDetailCardMinHeight, alignment: .leading)
        .background(AppPalette.accent.opacity(0.07))
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }
}

private struct OrderInstallationDraft: Identifiable {
    let id = UUID()
    var date: Date
    var installer: String
}

/// 创建安装安排存储日期使用的固定格式转换器。
/// 无参数。
private func orderInstallationDateFormatter() -> DateFormatter {
    let formatter = DateFormatter()
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.locale = Locale(identifier: "en_US_POSIX")
    formatter.timeZone = .current
    formatter.dateFormat = "yyyy-MM-dd"
    return formatter
}

/// 把已保存的安装日期转换为草稿日期，解析失败时使用当前日期。
/// - Parameters:
///   - value: 待解析或显示的业务日期时间字符串。
private func orderInstallationDraftDate(_ value: String) -> Date {
    orderInstallationDateFormatter().date(from: value) ?? Date()
}

/// 将安装草稿日期转换为存储用年月日字符串。
/// - Parameters:
///   - value: 待格式化的日期时间。
private func orderInstallationDraftValue(_ value: Date) -> String {
    orderInstallationDateFormatter().string(from: value)
}

/// 格式化安装日期按钮的中文显示文本。
/// - Parameters:
///   - value: 待格式化的日期时间。
private func orderInstallationPickerDisplayDate(_ value: Date) -> String {
    let formatter = DateFormatter()
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.locale = Locale(identifier: "en_US_POSIX")
    formatter.timeZone = .current
    formatter.dateFormat = orderInstallationDisplayDateFormat
    return formatter.string(from: value)
}

/// 从已有订单安装记录提取去重的安装人员建议。
/// - Parameters:
///   - orders: 订单看板记录列表。
private func orderInstallationInstallerSuggestions(from orders: [OrderDashboardItem]) -> [String] {
    let installers = orders.flatMap { item in
        item.plannedInstallationDays + item.actualInstallationDays
    }
    return Set(
        installers
            .map { $0.installer.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }
    ).sorted {
        $0.localizedStandardCompare($1) == .orderedAscending
    }
}

private struct OrderAnnotationsSheet: View {
    @ObservedObject var model: AppModel
    let order: OrderDashboardItem

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(spacing: 14) {
                Text("订单安排").font(.title.weight(.semibold))
                Rectangle().fill(.secondary.opacity(0.35)).frame(width: 1, height: 22)
                Text(order.orderId).font(.title2.weight(.medium)).foregroundStyle(.secondary)
            }
            .padding(.bottom, 14)
            OrderAnnotationsEditor(model: model, order: order)
        }
        .padding(AppLayout.contentPadding)
        .frame(minWidth: 640, idealWidth: 700)
        .fixedSize(horizontal: false, vertical: true)
        .background(LiquidGlassPreviewBackdrop())
    }
}

private struct OrderAnnotationsEditor: View {
    @ObservedObject var model: AppModel
    let order: OrderDashboardItem
    @State private var note: String
    @State private var plannedDays: [OrderInstallationDraft]
    @State private var actualDays: [OrderInstallationDraft]
    @State private var datePickerRowID: UUID?
    @State private var status = ""
    @State private var saveSucceeded = false
    @Environment(\.dismiss) private var dismiss

    /// 以当前订单备注及安装记录初始化独立编辑草稿。
    /// - Parameters:
    ///   - model: 共享的 App 状态及业务命令入口。
    ///   - order: 订单看板记录。
    init(model: AppModel, order: OrderDashboardItem) {
        self.model = model
        self.order = order
        _note = State(initialValue: order.userNote)
        _plannedDays = State(initialValue: order.plannedInstallationDays.map {
            OrderInstallationDraft(date: orderInstallationDraftDate($0.date), installer: $0.installer)
        })
        _actualDays = State(initialValue: order.actualInstallationDays.sorted { $0.date < $1.date }.prefix(1).map {
            OrderInstallationDraft(date: orderInstallationDraftDate($0.date), installer: $0.installer)
        })
        _datePickerRowID = State(initialValue: nil)
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            ScrollView(.vertical) {
                VStack(alignment: .leading, spacing: 16) {
                    Text("订单说明").font(.headline)
                    TextEditor(text: $note)
                        .font(.body)
                        .scrollContentBackground(.hidden)
                        .frame(height: 80)
                        .padding(10)
                        .background(.white.opacity(0.72), in: RoundedRectangle(cornerRadius: 8))
                        .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
                        .overlay(alignment: .topLeading) {
                            if note.isEmpty {
                                Text("填写客户要求、待确认事项或特殊交付说明")
                                    .foregroundColor(.secondary)
                                    .padding(.horizontal, 15)
                                    .padding(.vertical, 18)
                                    .allowsHitTesting(false)
                            }
                        }
                        .accessibilityLabel("订单说明")
                    Divider().padding(.top, 8)
                    HStack(spacing: 14) {
                        Text("安排类型").frame(width: 140, alignment: .leading)
                        Text("开始日期").frame(width: orderInstallationDateButtonWidth, alignment: .leading)
                        Text("安装人/安装小组").frame(maxWidth: .infinity, alignment: .leading)
                        Color.clear.frame(width: 24, height: 1)
                    }
                    .font(.subheadline.weight(.medium))
                    .foregroundStyle(.secondary)
                    Divider()
                    installationRows(title: "计划安装日期", rows: $plannedDays)
                    Divider()
                    installationRows(title: "实际安装开始日期", rows: $actualDays)
                    Divider()
                }
                .padding(.vertical, 2)
            }
            .scrollIndicators(.automatic)
            .frame(maxHeight: 420)
            .disabled(model.orderRunning || saveSucceeded)

            HStack(spacing: 8) {
                if !status.isEmpty {
                    Text(status)
                        .font(.caption)
                        .foregroundColor(status.contains("失败") ? AppPalette.danger : .secondary)
                        .accessibilityAddTraits(.updatesFrequently)
                }
                Spacer(minLength: 0)
                Button("关闭") { dismiss() }
                    .appActionButton(minWidth: 80)
                    .disabled(model.orderRunning)
                Button("保存") { save() }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 80)
                    .disabled(model.orderRunning || saveSucceeded)
            }
        }
        .task(id: saveSucceeded) {
            guard saveSucceeded else { return }
            // 返回订单中心前短暂保留成功提示。
            do { try await Task.sleep(for: .seconds(0.9)) } catch { return }
            dismiss()
        }
    }

    /// 显示可增删的安装日期与人员草稿列表。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - rows: 可编辑安装日期和人员草稿列表的双向绑定。
    @ViewBuilder
    private func installationRows(
        title: String,
        rows: Binding<[OrderInstallationDraft]>
    ) -> some View {
        HStack(alignment: .center, spacing: 14) {
            Text(title)
                .font(.subheadline.weight(.semibold))
                .frame(width: 140, alignment: .leading)
            if rows.wrappedValue.isEmpty {
                Button {
                    let day = OrderInstallationDraft(date: Date(), installer: "")
                    rows.wrappedValue.append(day)
                    datePickerRowID = day.id
                } label: {
                    Label("选择日期", systemImage: "calendar")
                        .padding(.horizontal, 9)
                        .frame(width: orderInstallationDateButtonWidth, height: 36, alignment: .leading)
                        .contentShape(Rectangle())
                }
                .buttonStyle(.plain)
                .background(.white.opacity(0.65), in: RoundedRectangle(cornerRadius: 8))
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
                .foregroundStyle(.secondary)
                .accessibilityLabel("\(title)：选择日期")
                Text("选择日期后填写安装人")
                    .font(.callout).foregroundStyle(.secondary)
                    .frame(maxWidth: .infinity, alignment: .leading)
                Color.clear.frame(width: 24, height: 1)
            } else {
                VStack(spacing: 10) {
                    ForEach(rows) { $day in
                        HStack(spacing: 14) {
                            Button {
                                datePickerRowID = datePickerRowID == day.id ? nil : day.id
                            } label: {
                                HStack(spacing: 6) {
                                    Image(systemName: "calendar")
                                        .foregroundColor(.secondary)
                                    Text(orderInstallationPickerDisplayDate(day.date))
                                        .frame(maxWidth: .infinity, alignment: .leading)
                                }
                                .padding(.horizontal, 9)
                                .frame(width: orderInstallationDateButtonWidth, height: 36, alignment: .leading)
                            }
                            .buttonStyle(.plain)
                            .background(.white.opacity(0.65), in: RoundedRectangle(cornerRadius: 8))
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
                            .accessibilityLabel("\(title)：\(orderInstallationPickerDisplayDate(day.date))")
                            .popover(
                                isPresented: Binding(
                                    get: { datePickerRowID == day.id },
                                    set: { isPresented in
                                        if !isPresented && datePickerRowID == day.id {
                                            datePickerRowID = nil
                                        }
                                    }
                                ),
                                // 在日期按钮旁显示日历；较高的订单面板容纳完整日历，避免日历在表单下方被裁切。
                                arrowEdge: .trailing
                            ) {
                                AppGlassDatePickerCalendar(selection: $day.date, compact: true)
                                    .appGlassDatePickerPopoverSurface()
                            }

                            HStack(spacing: 0) {
                                TextField("安装人/安装小组", text: $day.installer)
                                    .textFieldStyle(.plain)
                                    .padding(.leading, 8)
                                    .frame(minHeight: 36)
                                Menu {
                                    let suggestions = orderInstallationInstallerSuggestions(from: model.dashboardOrders)
                                    if suggestions.isEmpty {
                                        Text("暂无历史安装人")
                                    } else {
                                        ForEach(suggestions, id: \.self) { installer in
                                            Button(installer) {
                                                day.installer = installer
                                            }
                                        }
                                    }
                                } label: {
                                    Text("")
                                        .frame(width: 28, height: 30)
                                }
                                .menuStyle(.borderlessButton)
                                .accessibilityLabel("选择以前使用过的安装人或安装小组")
                                .help("选择以前使用过的安装人或安装小组")
                            }
                            .background(.white.opacity(0.55), in: RoundedRectangle(cornerRadius: 8))
                            .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
                            .frame(maxWidth: .infinity)
                            Button {
                                // 修改前先取得身份：$day 的索引仍指向原数组。
                                let removedID = day.id
                                if datePickerRowID == removedID {
                                    datePickerRowID = nil
                                }
                                rows.wrappedValue.removeAll { $0.id == removedID }
                            } label: {
                                Image(systemName: "trash")
                            }
                            .buttonStyle(.borderless)
                            .foregroundColor(AppPalette.danger)
                            .frame(width: 24)
                            .accessibilityLabel("清除\(title)")
                        }
                    }
                }
            }
        }
        .padding(.vertical, 4)
    }

    /// 提交备注和安装草稿，仅保留最早一条实际安装记录，并显示保存结果。
    /// 无参数。
    private func save() {
        let planned = plannedDays.map {
            OrderInstallationDay(
                date: orderInstallationDraftValue($0.date),
                installer: $0.installer.trimmingCharacters(in: .whitespacesAndNewlines)
            )
        }
        let actual = actualDays.sorted { $0.date < $1.date }.prefix(1).map {
            OrderInstallationDay(
                date: orderInstallationDraftValue($0.date),
                installer: $0.installer.trimmingCharacters(in: .whitespacesAndNewlines)
            )
        }
        status = "正在保存…"
        model.saveOrderAnnotations(
            orderID: order.orderId,
            userNote: note,
            plannedDays: planned,
            actualDays: actual,
            onStatusChange: { message in
                status = message
            },
            onSuccess: {
                status = "订单安排已保存"
                saveSucceeded = true
            }
        )
    }
}

struct OrderDashboardDetailCard: View {
    @ObservedObject var model: AppModel
    let dashboardFactories: [OrderDashboardFactory]
    @Binding var selectedFactoryID: String?
    @Binding var selectedFactoryIDs: Set<String>
    let onQueryStock: () -> Void
    let onOpenProduction: () -> Void
    let onOpenOutbound: () -> Void
    let onOpenScope: () -> Void
    let onOpenManualHardware: () -> Void
    let orderType: String
    let isCompletedOrder: Bool
    let orderID: String
    let isAborted: Bool
    @State private var showAbortConfirmation = false

    var body: some View {
        AppSurfaceCard(padding: 14) {
            VStack(alignment: .leading, spacing: 7) {
                detailActions
                factoriesPanel
            }
        }
        .alert("是否中止订单 \(orderID)？", isPresented: $showAbortConfirmation) {
            Button("取消", role: .cancel) {}
            Button("确认中止", role: .destructive) { model.abortOrder(orderID: orderID) }
        } message: {
            Text("中止后订单将标记为“已中止”，不再继续生产或出库。已有材料、生产和出库记录会保留，不会退回库存。")
        }
    }

    private var detailActions: some View {
        let outboundStatuses = Dictionary(uniqueKeysWithValues: dashboardFactories.map {
            ($0.factoryOrder, $0.outboundStatus)
        })
        let produced = Dictionary(uniqueKeysWithValues: dashboardFactories.map { ($0.factoryOrder, $0.produced) })
        let outboundActionTitle = orderDashboardOutboundActionTitle(selectedFactoryIDs, statuses: outboundStatuses)
        return HStack(alignment: .center, spacing: 12) {
            HStack(spacing: 8) {
                Button { onQueryStock() } label: {
                    Text("查询库存").frame(minWidth: 72)
                }
                    .appActionButton(minWidth: 0)
                    .disabled(isCompletedOrder || model.selectedOrderId.isEmpty || model.orderRunning || !model.orderPreviewReady)
                    .help(isCompletedOrder ? "订单已结束，不能再查询库存" : "查询当前订单库存")
                Button {
                    model.calculateSelectedOrderCost()
                } label: {
                    Text("计算成本").frame(minWidth: 72)
                }
                .appActionButton(minWidth: 0)
                .disabled(model.selectedOrderId != orderID || !model.canCalculateOrderCost)
                .help(model.canCalculateOrderCost ? "按已保存材料和五金计算成本" : "订单暂无可用材料数据，材料保存后可计算成本")
                Button { onOpenManualHardware() } label: {
                    Text("人工五金").frame(minWidth: 72)
                }
                    .appActionButton(minWidth: 0)
                    .disabled(model.selectedOrderId.isEmpty || model.orderRunning || model.inventoryRunning)
                    .help("查看、新增或删除本订单的人工五金")
                if orderType != "owned" {
                    Button { onOpenScope() } label: {
                        Text("设置出库范围").frame(minWidth: 88)
                    }
                        .appActionButton(minWidth: 0)
                        .disabled(isCompletedOrder || model.selectedOrderId.isEmpty || model.orderRunning)
                        .help(isCompletedOrder ? "订单已结束，不能再设置出库范围" : "设置当前订单出库范围")
                }
                Button { onOpenProduction() } label: {
                    Text("生产").frame(width: 37)
                }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 0)
                    .disabled(
                        isCompletedOrder || model.orderRunning || model.inventoryRunning || selectedFactoryIDs.isEmpty ||
                        orderDashboardHasProducedSelection(selectedFactoryIDs, produced: produced) ||
                        selectedFactoryIDs.contains { factoryID in
                            dashboardFactories.first(where: { $0.factoryOrder == factoryID })?.optimized != true
                        }
                    )
                    .help("选择一个或多个已优化且未生产的工厂单，登记本次实际消耗的订单材料")
                Button { onOpenOutbound() } label: {
                    Text(outboundActionTitle).frame(width: 37)
                }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 0)
                    .disabled(
                        isCompletedOrder
                        || model.orderRunning
                        || model.inventoryRunning
                        || selectedFactoryIDs.isEmpty
                        || selectedFactoryIDs.contains { factoryID in
                            dashboardFactories.first(where: { $0.factoryOrder == factoryID })?.produced != true
                        }
                        || orderDashboardHasShippedSelection(
                            selectedFactoryIDs,
                            statuses: Dictionary(uniqueKeysWithValues: dashboardFactories.map {
                                ($0.factoryOrder, $0.outboundStatus)
                            })
                        )
                    )
                    .help(
                        isCompletedOrder
                            ? "订单已结束，不能再处理出库"
                            : "只有已生产且未出库的工厂单可以出货；有五金则出库五金，没有五金则只更新出货状态"
                    )
                Button(role: .destructive) { showAbortConfirmation = true } label: {
                    Text("中止").frame(width: 37)
                }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 0)
                    .disabled(isAborted || model.orderRunning || model.inventoryRunning || orderID.isEmpty)
                    .help("中止整个订单，保留已有业务记录")
            }
            .fixedSize(horizontal: true, vertical: false)
            Spacer(minLength: 12)
            panelColorsSummary
        }
    }

    private var panelColorsSummary: some View {
        let materials = orderDashboardPanelMaterials(model.orderMaterials)
        return HStack(alignment: .center, spacing: 10) {
            Text("Panel颜色")
                .font(.subheadline.weight(.semibold))
                .foregroundColor(.secondary)
                .fixedSize(horizontal: true, vertical: false)
            if materials.isEmpty {
                Text("—")
                    .font(.title3.weight(.medium))
            } else {
                HStack(alignment: .center, spacing: 12) {
                    ForEach(materials) { material in
                        PanelMaterialHoverPreview(material: material) {
                            Text(material.color)
                                .font(.title3.weight(.medium))
                                .lineLimit(1)
                                .fixedSize(horizontal: true, vertical: false)
                        }
                    }
                }
            }
        }
        .frame(minHeight: AppLayout.controlHeight, alignment: .center)
        .fixedSize(horizontal: true, vertical: false)
        .padding(.trailing, 64)
    }

    private var factoriesPanel: some View {
        VStack(alignment: .leading, spacing: 8) {
            factoryTable
        }
    }

    private var factoryTable: some View {
        VStack(spacing: 0) {
            factoryTableRow(isHeader: true, factory: nil)
            Divider()
            ForEach(dashboardFactories) { factory in
                Button {
                    selectedFactoryIDs = toggledOrderFactorySelection(
                        selectedFactoryIDs,
                        factoryOrder: factory.factoryOrder
                    )
                    selectedFactoryID = selectedFactoryIDs.sorted().first
                } label: {
                    factoryTableRow(
                        isHeader: false,
                        dashboardFactory: factory,
                        selected: selectedFactoryIDs.contains(factory.factoryOrder)
                    )
                }
                .buttonStyle(.plain)
                .disabled(factory.outboundStatus == "已出库")
                .help(factory.outboundStatus == "已出库" ? "该工厂单已出库，不能重复出库" : "选择该工厂单")
                .background(selectedFactoryIDs.contains(factory.factoryOrder) ? AppPalette.accent.opacity(0.10) : Color.clear)
                Divider()
            }
        }
        .background(AppPalette.subtleSurface)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
        .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
        .frame(maxWidth: .infinity, alignment: .leading)
    }

    /// 使用统一列宽绘制工厂单表头或数据行。
    /// - Parameters:
    ///   - isHeader: 是否绘制表头行。
    ///   - factory: 工厂单预览。
    ///   - dashboardFactory: 看板中的工厂单状态；表头时可为空。
    ///   - selected: 当前行是否选中。
    @ViewBuilder
    private func factoryTableRow(
        isHeader: Bool,
        factory: OrderFactoryPreview? = nil,
        dashboardFactory: OrderDashboardFactory? = nil,
        selected: Bool = false
    ) -> some View {
        let factoryOrder = dashboardFactory?.factoryOrder ?? factory?.factoryOrder ?? ""
        let factoryName = dashboardFactory?.orderName ?? factory?.orderName ?? ""
        let optimization = dashboardFactory == nil
            ? (model.orderPreviewValidated ? "已优化" : "待校验")
            : (dashboardFactory?.optimized == true ? "已优化" : "待优化")
        let outbound = dashboardFactory?.outboundStatus ?? "未查询"
        let outboundDocument = dashboardFactory?.outboundDocument ?? ""
        HStack(spacing: 0) {
            Image(systemName: isHeader ? "square" : (selected ? "checkmark.square.fill" : "square"))
                .font(.system(size: isHeader ? 1 : 20, weight: .medium))
                .foregroundColor(selected ? AppPalette.accent : .secondary)
                .opacity(isHeader ? 0 : 1)
                .frame(width: orderDashboardFactorySelectionColumnWidth, alignment: .center)
            factoryCell(isHeader ? "工厂单" : factoryOrder, width: orderDashboardFactoryColumnWidths[0])
            factoryCell(isHeader ? "名称" : factoryName, width: orderDashboardFactoryColumnWidths[1])
            factoryCell(isHeader ? "拆单" : "已拆单", width: orderDashboardFactoryColumnWidths[2], status: isHeader ? nil : true)
            factoryCell(isHeader ? "优化" : optimization, width: orderDashboardFactoryColumnWidths[3], status: isHeader ? nil : optimization == "已优化")
            factoryCell(
                isHeader ? "生产" : (dashboardFactory?.produced == true ? "已生产" : "未生产"),
                width: orderDashboardFactoryColumnWidths[4],
                status: isHeader ? nil : dashboardFactory?.produced == true
            )
            factoryCell(
                isHeader ? "出库" : orderDashboardOutboundDisplay(status: outbound, documentNumber: outboundDocument),
                width: orderDashboardFactoryColumnWidths[5],
                status: isHeader ? nil : outbound == "已出库"
            )
        }
        .font(isHeader ? .caption.weight(.semibold) : .caption)
        .foregroundColor(isHeader ? .secondary : .primary)
        .padding(.vertical, isHeader ? 9 : 10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .contentShape(Rectangle())
    }

    /// 显示工厂单文本或居中的状态徽章。
    /// - Parameters:
    ///   - text: 待解析或显示的文本。
    ///   - width: 单元格或容器宽度，单位为逻辑点。
    ///   - status: 业务状态文字或状态代码。
    private func factoryCell(_ text: String, width: CGFloat, status: Bool? = nil) -> some View {
        Group {
            if let completed = status {
                HStack(spacing: 6) {
                    Image(systemName: completed ? "checkmark.circle.fill" : "circle")
                        .font(.system(size: 13, weight: .medium))
                        .foregroundColor(completed ? AppPalette.success : Color(red: 0.48, green: 0.52, blue: 0.58))
                        .accessibilityHidden(true)
                    Text(text)
                        .font(.caption)
                        .foregroundColor(completed
                            ? Color(red: 0.13, green: 0.43, blue: 0.28)
                            : Color(red: 0.57, green: 0.60, blue: 0.65))
                        .lineLimit(1)
                        .truncationMode(.tail)
                }
                .padding(.horizontal, 8)
                .frame(height: 24)
                .background(completed ? AppPalette.success.opacity(0.10) : Color.clear)
                .clipShape(RoundedRectangle(cornerRadius: 6, style: .continuous))
                .padding(.horizontal, 4)
                .help(text)
            } else {
                Text(text).lineLimit(1).truncationMode(.tail)
            }
        }
        // 将整个徽章居中对齐到与表头一致的固定列轴线上。
        .frame(width: width, alignment: .center)
        .multilineTextAlignment(.center)
    }

}

struct ProductionSheet: View {
    @ObservedObject var model: AppModel
    let orderID: String
    let factoryOrders: [String]
    let onClose: () -> Void
    @State private var didLoad = false
    @State private var operationState: SheetOperationState = .idle
    @State private var operationMessage = ""
    @State private var retryAllowed = false
    @State private var previewReady = false
    @State private var previewLoading = false
    @State private var previewFailed = false

    private enum SheetOperationState {
        case idle
        case preparing
        case running
        case success
        case failure
        case uncertain
    }

    /// 判断生产面板是否正在准备或执行库存操作。
    private var isProcessing: Bool {
        operationState == .preparing || operationState == .running
    }

    /// 统计本次生产消耗数量大于零的材料项目。
    private var selectedQuantityCount: Int {
        model.productionMaterials.filter { (Double($0.quantity) ?? 0) > 0 }.count
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("生产").font(.title2.weight(.semibold))
                    Text("订单 \(orderID) · 已选择 \(factoryOrders.count) 个工厂单；相同颜色材料可合并一次扣减")
                        .font(.caption).foregroundColor(.secondary)
                }
                Spacer()
                if isProcessing { ProgressView().controlSize(.small) }
            }
            Divider()
            if !model.productionPreviewStatus.isEmpty {
                Text(model.productionPreviewStatus).font(.caption).foregroundColor(.secondary)
            }
            if !operationMessage.isEmpty {
                productionOperationBanner
            }
            if model.productionMaterials.isEmpty {
                ContentUnavailableView("没有订单材料", systemImage: "shippingbox", description: Text("无需新增领料时，可仅确认所选工厂单生产完成。"))
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            } else {
                Text("填写本次实际消耗数量（不是每个工厂单分别填写；同色板材一次合并扣减）")
                    .font(.subheadline.weight(.semibold))
                ScrollView {
                    VStack(spacing: 0) {
                        HStack(spacing: 10) {
                            Text("类型")
                                .frame(width: 76, alignment: .leading)
                            Text("材料名")
                                .frame(maxWidth: .infinity, alignment: .leading)
                            Text("单位")
                                .frame(width: 52, alignment: .center)
                            Text("剩余")
                                .frame(width: 76, alignment: .trailing)
                            Text("数量")
                                .frame(width: 88, alignment: .center)
                        }
                        .font(.caption.weight(.semibold))
                        .foregroundColor(.secondary)
                        .padding(.vertical, 7)
                        Divider()
                        ForEach(sortedProductionMaterialDrafts(model.productionMaterials)) { material in
                            if let index = model.productionMaterials.firstIndex(where: { $0.id == material.id }) {
                            HStack(spacing: 10) {
                                Text(productionMaterialTypeDisplayName(material))
                                    .frame(width: 76, alignment: .leading)
                                Text(productionMaterialName(material))
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                    .lineLimit(2)
                                Text(material.unit.isEmpty ? "—" : material.unit)
                                    .frame(width: 52, alignment: .center)
                                Text("\(material.remainingQuantity, specifier: "%g")")
                                    .font(.caption).foregroundColor(.secondary)
                                    .frame(width: 76, alignment: .trailing)
                                TextField("数量", text: Binding(
                                    get: { model.productionMaterials[index].quantity },
                                    set: { model.productionMaterials[index].quantity = $0 }
                                ))
                                .textFieldStyle(.roundedBorder)
                                .frame(width: 88)
                                .disabled(
                                    material.remainingQuantity <= 0
                                    || isProcessing || operationState == .success
                                )
                            }
                            .opacity(material.remainingQuantity <= 0 ? 0.55 : 1)
                            .padding(.vertical, 8)
                            Divider()
                            }
                        }
                    }
                }
                .frame(maxHeight: .infinity)
            }
            if previewReady && selectedQuantityCount == 0 && operationState == .idle {
                Text("本次数量为 0：仅记录所选工厂单生产完成，不扣减板材和封边。")
                    .font(.caption).foregroundColor(.secondary)
            }
            HStack {
                Spacer()
                Button(operationState == .success ? "完成" : "关闭") { onClose() }
                    .buttonStyle(.glass)
                    .disabled(isProcessing)
                if previewFailed && operationState == .idle {
                    Button("重新读取材料") { loadPreview() }
                        .disabled(previewLoading || model.orderRunning)
                        .accessibilityIdentifier("production.reloadPreview")
                }
                if operationState == .failure && retryAllowed {
                    Button("重试") { submitProduction() }
                        .buttonStyle(.glassProminent)
                        .disabled(!canSubmit)
                } else if operationState == .idle {
                    if selectedQuantityCount == 0 {
                        Button("仅确认生产，不扣减材料") { submitProduction() }
                            .buttonStyle(.glassProminent)
                            .disabled(!canSubmit)
                            .accessibilityIdentifier("production.confirmWithoutMaterials")
                    } else {
                        Button("确认生产并扣减材料") { submitProduction() }
                            .buttonStyle(.glassProminent)
                            .disabled(!canSubmit)
                    }
                }
            }
        }
        .padding(22)
        .onAppear {
            guard !didLoad else { return }
            didLoad = true
            loadPreview()
        }
    }

    /// 弹窗统一读取预览，失败或忙碌后允许用户重试；成功回调才启用确认。
    private func loadPreview() {
        guard !previewLoading else { return }
        previewReady = false
        previewFailed = false
        previewLoading = true
        model.loadProductionPreview(orderID: orderID, factoryOrders: factoryOrders) { ready in
            previewLoading = false
            previewReady = ready
            previewFailed = !ready
        }
    }

    /// 预览成功且输入合法后允许提交，包括明确的全零消耗。
    private var canSubmit: Bool {
        previewReady && !previewLoading && !isProcessing && !model.orderRunning
            && productionDraftHasValidQuantities(model.productionMaterials)
    }

    private var productionOperationBanner: some View {
        let color: Color
        let icon: String
        let title: String
        switch operationState {
        case .preparing:
            color = AppPalette.accent
            icon = "clock.arrow.circlepath"
            title = "正在准备生产"
        case .running:
            color = AppPalette.accent
            icon = "shippingbox"
            title = selectedQuantityCount == 0 ? "正在保存生产记录" : "正在执行生产出库"
        case .success:
            color = AppPalette.success
            icon = "checkmark.circle.fill"
            title = selectedQuantityCount == 0 ? "生产已完成" : "生产出库成功"
        case .failure:
            color = AppPalette.danger
            icon = "xmark.octagon.fill"
            title = selectedQuantityCount == 0 ? "生产未完成" : "生产出库失败"
        case .uncertain:
            color = AppPalette.warning
            icon = "questionmark.circle.fill"
            title = "库存结果待核对"
        case .idle:
            color = .secondary
            icon = "info.circle"
            title = ""
        }
        return HStack(alignment: .top, spacing: 10) {
            Image(systemName: icon)
                .foregroundColor(color)
            VStack(alignment: .leading, spacing: 3) {
                if !title.isEmpty {
                    Text(title).font(.subheadline.weight(.semibold)).foregroundColor(color)
                }
                Text(operationMessage)
                    .font(.caption)
                    .foregroundColor(.primary)
                    .fixedSize(horizontal: false, vertical: true)
            }
            Spacer(minLength: 0)
        }
        .padding(10)
        .background(color.opacity(0.10))
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }

    /// 先准备生产请求，再提交实际消耗并根据结果更新面板。
    /// 无参数。
    private func submitProduction() {
        guard canSubmit else { return }
        if selectedQuantityCount == 0 {
            operationState = .running
            operationMessage = "正在保存生产记录……"
            retryAllowed = false
            model.confirmProductionWithoutMaterials(orderID: orderID, factoryOrders: factoryOrders, materials: model.productionMaterials) { result in
                operationState = result.state == .success ? .success : .failure
                operationMessage = result.message
                retryAllowed = result.retryAllowed
            }
            return
        }
        operationState = .preparing
        operationMessage = "正在校验本次材料数量，尚未操作库存系统……"
        retryAllowed = false
        model.prepareProduction(
            orderID: orderID,
            factoryOrders: factoryOrders,
            materials: model.productionMaterials,
            onResult: { requestID, preparationError in
                guard let requestID, !requestID.isEmpty else {
                    operationState = .failure
                    operationMessage = preparationError ?? "生产准备失败；本次未操作库存系统，也未写入本地生产完成记录"
                    return
                }
                operationState = .running
                operationMessage = "材料数量校验通过，正在连接库存系统执行出库……"
                model.startDirectProduction(
                    orderID: orderID,
                    factoryOrders: factoryOrders,
                    materials: model.productionMaterials,
                    requestID: requestID
                ) { result in
                    switch result.state {
                    case .success:
                        operationState = .success
                    case .failure:
                        operationState = .failure
                    case .uncertain:
                        operationState = .uncertain
                    }
                    operationMessage = result.message
                    retryAllowed = result.retryAllowed
                }
            }
        )
    }
}

struct OrderShipmentConfirmationSheet: View {
    @ObservedObject var model: AppModel
    let orderID: String
    let factoryOrders: [String]
    let onCancel: () -> Void
    let onConfirm: () -> Void

    /// 筛选所选工厂单中未忽略且数量为正的五金。
    private var fittings: [OrderFittingPreview] {
        model.orderFittings.filter { factoryOrders.contains($0.factoryOrder) && !$0.ignored && $0.quantity > 0 }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("确认出货").font(.title2.weight(.semibold))
                    Text("订单 \(orderID) · 已选择 \(factoryOrders.count) 个已生产工厂单")
                        .font(.caption).foregroundColor(.secondary)
                }
                Spacer()
                AppStatusBadge(text: "库存余额不作门禁", kind: .warning)
            }
            Divider()
            Text("本次只把数据库中已确认的五金内容直接提交库存系统；不重复做 SKU 映射，也不查询库存余额。")
                .font(.subheadline)
                .foregroundColor(.secondary)
                .fixedSize(horizontal: false, vertical: true)
            AppSurfaceCard {
                VStack(alignment: .leading, spacing: 8) {
                    Text("本次操作内容").font(.headline)
                    Text("工厂单：\(factoryOrders.sorted().joined(separator: "、"))")
                        .font(.subheadline)
                    Divider()
                    if fittings.isEmpty {
                        Text("没有可出库五金；确认后只更新所选工厂单的出货状态，不创建库存出库单")
                            .foregroundColor(AppPalette.warning)
                    } else {
                        ScrollView {
                            LazyVStack(alignment: .leading, spacing: 6) {
                                ForEach(fittings) { fitting in
                                    HStack(spacing: 8) {
                                        Text(fitting.orderName.isEmpty ? fitting.factoryOrder : fitting.orderName)
                                            .frame(width: 150, alignment: .leading)
                                        Text(fitting.displayName.isEmpty
                                            ? (fitting.name.isEmpty ? fitting.code : fitting.name)
                                            : fitting.displayName)
                                            .frame(maxWidth: .infinity, alignment: .leading)
                                        Text(fitting.quantity.formatted())
                                            .frame(width: 70, alignment: .trailing)
                                    }
                                    .font(.subheadline)
                                }
                            }
                        }
                        .frame(maxHeight: 260)
                    }
                }
            }
            Spacer(minLength: 0)
            HStack {
                Spacer()
                Button("取消") { onCancel() }
                    .buttonStyle(.glass)
                    .appActionButton(minWidth: 90)
                Button("确认并直接出货") { onConfirm() }
                    .buttonStyle(.glassProminent)
                    .tint(AppPalette.danger)
                    .appActionButton(minWidth: 150)
                    .disabled(model.inventoryRunning)
            }
        }
        .padding(22)
    }
}

struct OutboundScopeSheet: View {
    @ObservedObject var model: AppModel
    let orderID: String
    let orderType: String
    let factoryOrders: [String]
    let hardwareFactoryOrders: Set<String>
    @Environment(\.dismiss) private var dismiss
    @State private var scopeType = "material"
    @State private var requirement = "required"
    @State private var factoryOrder = ""
    @State private var reason = ""
    @State private var isLoadingSavedScope = false
    @State private var didLoadSavedScope = false

    /// 判断当前订单是否属于 CUT TO SIZE 来料加工。
    private var incomingProcessing: Bool { orderType == "cutToSize" }
    /// 判断当前出库范围选择是否表示无需出库。
    private var noOutboundDecision: Bool {
        requirement == "customer_supplied" || requirement == "remainder" || requirement == "not_required"
    }
    /// 判断当前范围是否有工厂单五金可供选择。
    private var hardwareAvailable: Bool { !hardwareFactoryOrders.isEmpty }

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("设置出库范围").font(.title2.weight(.semibold))
            Text("先保留订单文件读取的材料事实，再单独决定哪些项目进入出库单。数据库没有材料时不会自动判定为余料生产。")
                .font(.caption).foregroundColor(.secondary)
            HStack(spacing: 2) {
                scopeSegment("板材与封边", value: "material")
                scopeSegment("五金", value: "hardware", disabled: !hardwareAvailable)
            }
            .padding(2)
            .background(Color.secondary.opacity(0.10))
            .clipShape(RoundedRectangle(cornerRadius: 6, style: .continuous))
            .disabled(isLoadingSavedScope)
            if !hardwareAvailable {
                Text("当前订单没有可用五金数据，不能设置五金出库范围。")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            if scopeType == "hardware" {
                Picker("工厂单", selection: $factoryOrder) {
                    Text("请选择工厂单").tag("")
                    ForEach(factoryOrders, id: \.self) { Text($0).tag($0) }
                }
                .disabled(isLoadingSavedScope)
            }
            Picker("出库决定", selection: $requirement) {
                Text("需要出库").tag("required")
                if scopeType == "material" && incomingProcessing {
                    Text("客户提供材料（不入库存）").tag("customer_supplied")
                }
                Text("余料生产，不出库").tag("remainder")
                Text("其他原因，不出库").tag("not_required")
            }
            .pickerStyle(.radioGroup)
            .disabled(isLoadingSavedScope)
            if noOutboundDecision {
                TextField("必须填写原因，例如：客户提供板材和封边", text: $reason)
                    .textFieldStyle(.roundedBorder)
                    .disabled(isLoadingSavedScope)
            }
            if isLoadingSavedScope {
                Label("正在读取上次保存的出库范围…", systemImage: "arrow.triangle.2.circlepath")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
            Spacer()
            HStack {
                Spacer()
                Button("取消") { dismiss() }
                Button("保存") {
                    model.saveOutboundScope(
                        orderID: orderID,
                        scopeType: scopeType,
                        requirement: requirement,
                        factoryOrder: factoryOrder,
                        reason: reason
                    ) { success in
                        if success { dismiss() }
                    }
                }
                .buttonStyle(.glassProminent)
                .disabled(isLoadingSavedScope || model.inventoryRunning || orderID.isEmpty || (scopeType == "hardware" && factoryOrder.isEmpty) || (noOutboundDecision && reason.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty))
            }
        }
        .padding(22)
        .onAppear { loadSavedScopeIfNeeded() }
        .onChange(of: scopeType) { _, value in
            if value == "hardware" && (!hardwareAvailable || requirement == "customer_supplied") {
                scopeType = "material"
                factoryOrder = ""
            }
            if value == "material" { factoryOrder = "" }
        }
    }

    /// 为当前订单和工厂单载入已保存的出库范围草稿。
    /// 无参数。
    private func loadSavedScopeIfNeeded() {
        guard !didLoadSavedScope else { return }
        didLoadSavedScope = true
        isLoadingSavedScope = true
        model.loadOutboundScope(orderID: orderID, factoryOrders: factoryOrders) { object in
            defer { isLoadingSavedScope = false }
            guard let object,
                  let decision = object["last_decision"] as? [String: Any],
                  let savedScopeType = decision["scope_type"] as? String,
                  let savedRequirement = decision["requirement"] as? String else {
                return
            }
            if savedScopeType == "hardware" {
                let savedFactoryOrder = decision["factory_order"] as? String ?? ""
                guard hardwareAvailable, factoryOrders.contains(savedFactoryOrder) else { return }
                scopeType = "hardware"
                factoryOrder = savedFactoryOrder
            } else {
                scopeType = "material"
                factoryOrder = ""
            }
            requirement = savedRequirement
            reason = decision["reason"] as? String ?? ""
        }
    }

    /// 构造出库范围选项按钮并显示选择和禁用状态。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - value: 此出库范围选项对应的保存值。
    ///   - disabled: 是否禁用此选项。
    private func scopeSegment(_ title: String, value: String, disabled: Bool = false) -> some View {
        Button {
            if !disabled { scopeType = value }
        } label: {
            Text(title)
                .frame(maxWidth: .infinity)
                .padding(.vertical, 5)
        }
        .buttonStyle(.plain)
        .foregroundColor(disabled ? .secondary.opacity(0.45) : (scopeType == value ? AppPalette.accent : .secondary))
        .background(scopeType == value ? AppPalette.surface : Color.clear)
        .clipShape(RoundedRectangle(cornerRadius: 5, style: .continuous))
        .disabled(disabled)
    }
}

struct FolderManualHandlingSheet: View {
    @ObservedObject var model: AppModel
    let group: ServerFolderChangeGroup
    @Environment(\.dismiss) private var dismiss
    @State private var referenceText = ""
    @State private var outboundDocument = ""

    /// 把用户填写的参考订单拆分为有效订单号列表。
    private var references: [String] {
        referenceText.components(separatedBy: CharacterSet(charactersIn: "、,，;； \n"))
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines).uppercased() }
            .filter { !$0.isEmpty }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("登记已人工处理").font(.title2.weight(.semibold))
            Text(group.folderName).font(.headline).textSelection(.enabled)
            Text(group.folderPath).font(.caption).foregroundColor(.secondary).textSelection(.enabled)
            Text("确认这个文件夹对应的本次补单或临时任务已在库存系统完成出库。App 只保存登记结果，不会再次扣减库存，也不会修改原订单。")
                .font(.callout)
            TextField("参考订单（可留空；多个用逗号分隔）", text: $referenceText)
                .textFieldStyle(.roundedBorder)
            Text("参考订单仅用于追溯，不参与材料、生产或出货汇总。")
                .font(.caption).foregroundColor(.secondary)
            TextField("外部出库单号（可留空）", text: $outboundDocument)
                .textFieldStyle(.roundedBorder)
            Text("登记后移出待处理；三天内 XML 变化会重新提醒。")
                .font(.caption).foregroundColor(.secondary)
            HStack {
                Spacer()
                Button("取消") { dismiss() }.keyboardShortcut(.cancelAction)
                Button("确认已在外部出库") {
                    model.markTemporaryFolderManual(
                        group.folderPath, referenceOrderIDs: references,
                        outboundDocument: outboundDocument.trimmingCharacters(in: .whitespacesAndNewlines)
                    )
                    dismiss()
                }
                .buttonStyle(.glassProminent)
                .disabled(model.orderRunning || model.inventoryRunning)
            }
        }
        .padding(24)
        .frame(width: 560)
        .background(LiquidGlassPreviewBackdrop())
        .onAppear { referenceText = group.referenceOrderIDs.joined(separator: "、") }
    }
}

struct PendingCenterSheet: View {
    @ObservedObject var model: AppModel
    @State private var selectedID: String?
    @State private var searchText = ""
    @State private var category = "全部"
    @State private var orderIDs: [String: String] = [:]
    @State private var confirmationTitle = ""
    @State private var pendingAction: (() -> Void)?
    @State private var showActionConfirmation = false
    @State private var manualHandlingGroup: ServerFolderChangeGroup?

    /// 弹出确认对话框，仅在用户确认后执行动作。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - action: 用户确认或点击按钮后执行的动作。
    private func confirm(_ title: String, action: @escaping () -> Void) {
        confirmationTitle = title
        pendingAction = action
        showActionConfirmation = true
    }

    /// 读取模型当前生成的待处理队列。
    private var items: [PendingCenterItem] { model.pendingCenterItems }
    /// 按当前筛选条件取得待处理队列的可见项目。
    private var visibleItems: [PendingCenterItem] {
        items.filter {
            (category == "全部" || $0.status == category) &&
            (searchText.isEmpty || "\($0.title) \($0.subtitle) \($0.folderPath) \($0.issues.map(\.message).joined(separator: " "))".localizedCaseInsensitiveContains(searchText))
        }
    }

    /// 从当前记录中取得所选身份对应的项目。
    private var selectedItem: PendingCenterItem? {
        visibleItems.first { $0.id == selectedID } ?? visibleItems.first
    }

    /// 使待处理项选择与当前可见队列保持一致。
    /// 无参数。
    private func reconcileSelection() {
        guard !visibleItems.contains(where: { $0.id == selectedID }) else { return }
        selectedID = visibleItems.first?.id
        model.selectedAimesReviewIDs.removeAll()
        model.selectedServerFolderPaths.removeAll()
    }

    /// 始终从当前可见选择推导操作目标。
    /// 按当前可见选择定位待处理项并打开对应预览或处理入口。
    /// - Parameters:
    ///   - item: 待处理队列项。
    private func preview(_ item: PendingCenterItem) {
        guard !model.orderRunning, !item.folderPath.isEmpty else { return }
        model.selectedAimesReviewIDs.removeAll()
        model.processSelectedServerFolder(
            URL(fileURLWithPath: inventoryMappingSourceFolderPath(item.folderPath)),
            includeHardware: true
        )
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 5) {
                    Text("待处理中心")
                        .font(.title2.weight(.semibold))
                    Text("外部修复后重新检查；核对通过后自动移除提示。")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                Spacer()
                AppStatusBadge(text: "\(items.count) 项", kind: .warning)
            }
            HStack(spacing: 10) {
                Button("重新扫描 Server") { model.scanDashboardServer(presentIfNeeded: false) }
                Button("同步 AIMES 并检查") { model.syncDashboardAimes(force: true) }
                Spacer()
            }
            .disabled(model.orderRunning || model.inventoryRunning)
            ForEach(model.pendingSourceFailures.keys.sorted(), id: \.self) { source in
                Text("\(source) 状态尚未确认：\(model.pendingSourceFailures[source] ?? "")")
                    .font(.caption).foregroundColor(AppPalette.warning).fixedSize(horizontal: false, vertical: true)
            }
            if !model.pendingCheckStatus.isEmpty {
                Text(model.pendingCheckStatus).font(.caption).foregroundColor(.secondary)
                    .textSelection(.enabled).fixedSize(horizontal: false, vertical: true)
            }
            HStack(alignment: .top, spacing: 14) {
                VStack(alignment: .leading, spacing: 10) {
                    HStack(spacing: 8) {
                        TextField("搜索订单、问题或路径", text: $searchText)
                            .textFieldStyle(.roundedBorder)
                        Picker("类型", selection: $category) {
                            ForEach(["全部", "待处理", "待核对", "处理失败", "待人工确认", "需人工处理"], id: \.self) { type in
                                Text("\(type) · \(type == "全部" ? items.count : items.filter { $0.status == type }.count)").tag(type)
                            }
                        }
                        .labelsHidden()
                        .frame(width: 112)
                    }
                    ScrollView {
                        LazyVStack(spacing: 6) {
                            ForEach(visibleItems) { item in queueRow(item) }
                        }
                    }
                    if visibleItems.isEmpty {
                        Text(items.isEmpty ? "当前没有待处理项目" : "没有符合筛选的项目")
                            .font(.caption).foregroundColor(.secondary)
                    }
                }
                .frame(width: 280)
                AppSurfaceCard(padding: 0) {
                    if let item = selectedItem {
                        VStack(alignment: .leading, spacing: 12) {
                            HStack {
                                Text(item.title).font(.title3.weight(.semibold))
                                Spacer()
                                Text(item.status).font(.caption.weight(.semibold))
                                    .foregroundColor(item.status == "处理失败" ? AppPalette.danger : AppPalette.accent)
                            }
                            ScrollView {
                                VStack(alignment: .leading, spacing: 12) {
                                    Text(item.subtitle).font(.caption).foregroundColor(.secondary)
                                    Text(detailTitle(item)).font(.headline)
                                    Text(detailExplanation(item)).font(.callout).foregroundColor(.secondary)
                                    if !model.pendingMappingResumeMessage(for: item).isEmpty {
                                        Text(model.pendingMappingResumeMessage(for: item))
                                            .font(.callout).foregroundColor(AppPalette.warning)
                                            .textSelection(.enabled)
                                    }
                                    pendingItemDetails(item)
                                }.frame(maxWidth: .infinity, alignment: .leading)
                            }
                            Divider()
                            HStack(spacing: 8) {
                                Spacer()
                                postponeButton
                                if !(item.aimesReviews + item.aimesFormatWarnings).isEmpty {
                                    let reviews = (item.aimesReviews + item.aimesFormatWarnings).filter { model.selectedAimesReviewIDs.contains($0.id) }
                                    Button("忽略选中项") {
                                        let ids = Set(reviews.map(\.id))
                                        let names = reviews.map { $0.factoryOrder.isEmpty ? $0.factoryName : $0.factoryOrder }.joined(separator: "、")
                                        confirm("确认忽略 \(names)？") {
                                            model.selectedAimesReviewIDs = ids
                                            model.ignoreSelectedAimesFactories()
                                        }
                                    }
                                    .buttonStyle(.glass)
                                    .disabled(model.orderRunning || reviews.isEmpty)
                                }
                                if item.status == "待处理" || item.status == "处理失败" {
                                    if !item.folderPath.isEmpty && item.serverGroup?.independentManual != true {
                                        Button(item.status == "处理失败" ? "重新读取并预览" : "选择并预览") { preview(item) }
                                            .buttonStyle(.glassProminent)
                                            .disabled(model.orderRunning || model.inventoryRunning)
                                    }
                                }
                            }
                        }
                        .padding(14)
                    } else {
                        VStack(spacing: 12) {
                            ContentUnavailableView("请选择待处理项目", systemImage: "tray")
                                .frame(maxWidth: .infinity, maxHeight: .infinity)
                            Divider()
                            HStack {
                                Spacer()
                                postponeButton
                            }
                        }
                        .padding(14)
                    }
                }
            }
            .frame(maxHeight: .infinity)

        }
        .padding(20)
        .background(LiquidGlassPreviewBackdrop())
        .frame(width: 980, height: 620)
        .sheet(item: $manualHandlingGroup) { group in
            FolderManualHandlingSheet(model: model, group: group)
        }
        .onAppear { reconcileSelection() }
        .onChange(of: visibleItems.map(\.id)) { _, _ in reconcileSelection() }
        .alert(confirmationTitle, isPresented: $showActionConfirmation) {
            Button("取消", role: .cancel) { pendingAction = nil }
            Button("确认") {
                guard !model.orderRunning, !model.inventoryRunning else { return }
                pendingAction?()
                pendingAction = nil
            }
        } message: {
            Text("此操作会保存你的处理结果。请确认当前订单和处理范围无误。")
        }
    }

    // 即使队列或筛选结果为空，也保留关闭入口。
    private var postponeButton: some View {
        Button("稍后处理") { model.showPendingCenterPrompt = false }
            .buttonStyle(.glass)
            .keyboardShortcut(.cancelAction)
    }

    /// 根据待处理项类型生成详情标题。
    /// - Parameters:
    ///   - item: 待处理队列项。
    private func detailTitle(_ item: PendingCenterItem) -> String {
        switch item.status {
        case "待核对": return "历史出库记录还需要核对"
        case "处理失败": return "本次处理未完成"
        case "待人工确认": return "核对来源并确认归属"
        case "需人工处理": return "补充材料与商品映射"
        default: return "本次来源变化"
        }
    }

    /// 根据待处理项来源和问题类型生成处理说明。
    /// - Parameters:
    ///   - item: 待处理队列项。
    private func detailExplanation(_ item: PendingCenterItem) -> String {
        if item.serverGroup?.independentManual == true {
            return "这是独立人工处理文件夹。补单依据最近同步的 AIMES 工厂单和已出库事实识别；请在外部完成出库后登记。"
        }
        switch item.status {
        case "待核对": return "先点击“核对并恢复本地记录”。若仍无法核对，可打开库存系统检查对应单据；在外部修复后再次点击核对，全部一致后提示会自动移除。此操作不会再次扣库存。"
        case "处理失败": return "请根据下方原因检查文件或连接，再重新读取。预览准备好后才能确认写入。"
        case "待人工确认": return "请核对原始信息和建议值，再确认具体操作；缺少的资料需要先补齐。"
        case "需人工处理": return "完成映射后会自动继续读取原订单并准备只读预览。"
        default: return "扫描已完成。预览将读取下列文件，供你核对板材、封边和五金。"
        }
    }

    /// 构造待处理中心队列行及其状态标识。
    /// - Parameters:
    ///   - item: 待处理队列项。
    private func queueRow(_ item: PendingCenterItem) -> some View {
        Button {
            selectedID = item.id
            model.selectedAimesReviewIDs.removeAll()
            model.selectedServerFolderPaths.removeAll()
        } label: {
            VStack(alignment: .leading, spacing: 6) {
                HStack {
                    Text(item.title).font(.headline).lineLimit(1)
                    Spacer()
                    Text(item.status).font(.caption)
                }
                Text(item.issues.first?.message ?? item.subtitle)
                    .font(.caption).foregroundColor(.secondary).lineLimit(2)
                if let time = item.issues.map(\.lastSeen).filter({ !$0.isEmpty }).max() ?? item.serverGroup?.changes.map(\.eventTime).filter({ !$0.isEmpty }).max() {
                    Text(appDisplayTimestamp(time)).font(.caption2).foregroundColor(.secondary)
                }
            }
            .padding(10).frame(maxWidth: .infinity, alignment: .leading)
            .background(selectedItem?.id == item.id ? AppPalette.accent.opacity(0.10) : AppPalette.subtleSurface)
            .clipShape(RoundedRectangle(cornerRadius: 10))
            .overlay(RoundedRectangle(cornerRadius: 10).stroke(selectedItem?.id == item.id ? AppPalette.accent : .clear))
        }.buttonStyle(.plain)
    }

    /// 按 Server、问题和 AIMES 类型显示所选待处理项详情。
    /// - Parameters:
    ///   - item: 待处理队列项。
    @ViewBuilder
    private func pendingItemDetails(_ item: PendingCenterItem) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            if let group = item.serverGroup {
                VStack(alignment: .leading, spacing: 6) {
                    Text("Server 文件变化（\(group.changes.count) 项）")
                        .font(.subheadline.weight(.semibold))
                    ForEach(group.changes) { change in
                        HStack(alignment: .top, spacing: 6) {
                            Image(systemName: changeIcon(change.changeType))
                                .foregroundColor(changeColor(change.changeType))
                                .frame(width: 16)
                            VStack(alignment: .leading, spacing: 2) {
                                                    let timeSuffix = change.eventTime.isEmpty ? "" : " · \(changeTimeLabel(change))"
                                                    Text("\(changeTypeName(change.changeType))：\(displayPathName(change.path))\(timeSuffix)")
                                                        .font(.caption)
                                                    if change.handlingMode == "layout_review" { Text(change.message).font(.caption).foregroundColor(.orange) }
                                                    Text(change.path)
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                                    .lineLimit(1)
                            }
                        }
                    }
                    if !group.changes.contains(where: { $0.handlingMode == "layout_review" }) && (group.manualOnly || group.requiresManualReview || group.changes.contains(where: { $0.handlingMode == "aicnc" })) {
                        VStack(alignment: .leading, spacing: 10) {
                            if group.manualOnly {
                                Text("按此文件夹独立登记。请先在库存系统完成出库；参考订单可留空，登记不会改变原订单。完成后三天独立观察 XML。")
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                                    .fixedSize(horizontal: false, vertical: true)
                            }
                            HStack(spacing: 8) {
                                Spacer(minLength: 0)
                                ServerFolderIgnoreButton(model: model, group: group)
                                if group.manualOnly {
                                    Button {
                                        manualHandlingGroup = group
                                    } label: {
                                        Text("已人工处理").frame(width: 112)
                                    }
                                    .buttonStyle(.glassProminent)
                                    .controlSize(.regular)
                                    .disabled(model.orderRunning || model.inventoryRunning)
                                }
                            }
                        }
                        .padding(.top, 6)
                    }
                }
            }

            ForEach(item.issues) { issue in
                issueDetails(issue)
            }

            ForEach(item.aimesReviews) { review in
                aimesDetails(review)
            }

            ForEach(item.aimesFormatWarnings) { warning in
                aimesFormatWarningDetails(warning)
            }
        }
    }

    /// 显示当前问题来源、原因及对应处理入口。
    /// - Parameters:
    ///   - issue: 待判断或处理的当前业务问题。
    @ViewBuilder
    private func issueDetails(_ issue: CurrentIssue) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top, spacing: 8) {
                Image(systemName: issue.kind == "factory_ownership" ? "person.crop.circle.badge.questionmark" : "exclamationmark.triangle.fill")
                    .foregroundColor(issue.kind == "factory_ownership" ? AppPalette.warning : AppPalette.danger)
                VStack(alignment: .leading, spacing: 3) {
                    Text(issue.kind == "aicnc_legacy_retired" ? "旧版监控已结束" : issue.kind == "inventory_recovery" ? "库存操作待核对" : issue.kind == "factory_ownership" ? "订单归属问题" : (issue.kind == "server_missing_report" ? "报表检查" : (currentIssueRequiresInventoryMapping(issue) ? "出库前需要材料映射" : (issue.kind == "hardware_integrity" ? "本地五金记录待核对" : "资料待核对"))))
                        .font(.subheadline.weight(.semibold))
                    Text([issue.orderId.isEmpty ? "" : "订单：\(issue.orderId)",
                          issue.factoryOrder.isEmpty ? "" : "工厂单：\(issue.factoryOrder)"].filter { !$0.isEmpty }.joined(separator: "；"))
                        .font(.caption)
                    Text(issue.message).fixedSize(horizontal: false, vertical: true)
                    if !issue.path.isEmpty {
                        Text(issue.path)
                            .font(.caption.monospaced())
                            .foregroundColor(.secondary)
                            .lineLimit(2)
                    }
                }
            }
            HStack(spacing: 8) {
                if !issue.path.isEmpty {
                    Button("打开所在文件夹") { model.openDashboardLocation(issue.path) }
                        .buttonStyle(.link)
                }
                if issue.kind == "aicnc_legacy_retired" {
                    Button("知道了") { model.dismissLegacyMonitorReminder() }
                        .disabled(model.orderRunning)
                } else if issue.kind == "inventory_recovery" {
                    Button("核对并恢复本地记录") {
                        confirm("核对外部单据并补齐本地记录？不会再次扣库存。") {
                            model.recoverPendingInventory(issue)
                        }
                    }
                    .buttonStyle(.glassProminent)
                    .disabled(model.orderRunning || model.inventoryRunning)
                    Button("打开库存系统") { model.openInventoryChrome() }
                        .buttonStyle(.glass)
                        .disabled(model.orderRunning || model.inventoryRunning)
                } else if issue.kind == "factory_ownership" {
                    TextField("确认订单号，如 PP0037", text: Binding(
                        get: { orderIDs[issue.id] ?? "" },
                        set: { orderIDs[issue.id] = $0 }
                    ))
                    .textFieldStyle(.roundedBorder)
                    .frame(width: 180)
                    Button("自动处理") { confirm("确认处理 \(issue.factoryOrder) 的归属？") { model.autoResolveCurrentIssue(issue) } }
                        .buttonStyle(.glass)
                        .disabled(model.orderRunning)
                    Button("确认归属") {
                        let orderID = orderIDs[issue.id] ?? ""
                        confirm("确认归属到 \(orderID)？") { model.resolveCurrentIssue(issue, orderID: orderID) }
                    }
                        .buttonStyle(.glassProminent)
                        .disabled(model.orderRunning || (orderIDs[issue.id] ?? "").trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                } else if currentIssueRequiresInventoryMapping(issue) {
                    Button("处理订单文件映射") { model.requestInventoryMapping(folderPath: issue.path, message: issue.message) }
                        .buttonStyle(.glassProminent)
                        .disabled(model.orderRunning)
                } else if issue.kind == "server_missing_report" {
                    Button("重新检查报表") { model.recheckPendingIssue(issue) }
                        .buttonStyle(.glass)
                        .disabled(model.orderRunning)
                }
                if issue.kind != "aicnc_legacy_retired" && issue.kind != "inventory_recovery" && issue.kind != "factory_ownership" && issue.kind != "server_missing_report" {
                    Button("重新检查") { model.recheckPendingIssue(issue) }
                        .buttonStyle(.glass)
                        .disabled(model.orderRunning || model.inventoryRunning)
                }
            }
        }
        .padding(10)
        .background(AppPalette.subtleSurface)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }

    /// 显示 AIMES 工厂单归属问题及人工确认操作。
    /// - Parameters:
    ///   - item: AIMES 人工确认记录。
    @ViewBuilder
    private func aimesDetails(_ item: AimesReviewItem) -> some View {
        HStack(alignment: .top, spacing: 8) {
            Button { model.toggleAimesReviewSelection(item) } label: {
                Image(systemName: model.selectedAimesReviewIDs.contains(item.id) ? "checkmark.square.fill" : "square")
                    .foregroundColor(model.selectedAimesReviewIDs.contains(item.id) ? AppPalette.accent : .secondary)
                    .frame(width: 20, height: 20)
            }
            .buttonStyle(.plain)
            VStack(alignment: .leading, spacing: 4) {
                Text("AIMES 待确认 · \(item.factoryOrder.isEmpty ? "工厂单号为空" : item.factoryOrder)")
                    .font(.subheadline.weight(.semibold))
                Text("工厂单名称：\(item.factoryName.isEmpty ? "名称为空" : item.factoryName)")
                    .font(.caption)
                Text("销售单名称：\(item.salesOrderName.isEmpty ? "空" : item.salesOrderName)")
                    .font(.caption)
                Text(item.reason).font(.caption).foregroundColor(AppPalette.warning)
            }
            Spacer(minLength: 8)
            if !item.suggestedOrderID.isEmpty {
                Button("按 \(item.suggestedOrderID) 处理") { confirm("确认归属到 \(item.suggestedOrderID)？") { model.assignAimesFactoryToSuggestedOrder(item) } }
                    .buttonStyle(.glassProminent)
                    .disabled(model.orderRunning)
            }
        }
        .padding(10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(AppPalette.subtleSurface)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }

    /// 显示 AIMES 销售单格式异常与处理说明。
    /// - Parameters:
    ///   - item: AIMES 人工确认记录。
    @ViewBuilder
    private func aimesFormatWarningDetails(_ item: AimesReviewItem) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top, spacing: 8) {
                Button { model.toggleAimesReviewSelection(item) } label: {
                    Image(systemName: model.selectedAimesReviewIDs.contains(item.id) ? "checkmark.square.fill" : "square")
                        .foregroundColor(model.selectedAimesReviewIDs.contains(item.id) ? AppPalette.accent : .secondary)
                        .frame(width: 20, height: 20)
                }
                .buttonStyle(.plain)
                VStack(alignment: .leading, spacing: 4) {
                    Text("AIMES 销售单格式异常 · \(item.factoryOrder)")
                        .font(.subheadline.weight(.semibold))
                    Text("工厂单名称：\(item.factoryName.isEmpty ? "名称为空" : item.factoryName)")
                        .font(.caption)
                    Text("原始销售单名称：\(item.salesOrderName.isEmpty ? "空" : item.salesOrderName)")
                        .font(.caption)
                    Text(item.reason).font(.caption).foregroundColor(AppPalette.warning)
                }
            }
            HStack(spacing: 8) {
                TextField(
                    "订单号，如 PP0037 或 CS001",
                    text: Binding(
                        get: { orderIDs[item.id] ?? item.suggestedOrderID },
                        set: { orderIDs[item.id] = $0 }
                    )
                )
                .textFieldStyle(.roundedBorder)
                .frame(width: 220)
                if !item.suggestedOrderID.isEmpty {
                    Text("建议：\(item.suggestedOrderID)")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                Button("确认归属") {
                    let orderID = orderIDs[item.id] ?? item.suggestedOrderID
                    confirm("确认归属到 \(orderID)？") {
                        model.assignAimesFactoryToOrder(item, orderID: orderID)
                    }
                }
                .buttonStyle(.glassProminent)
                .disabled(
                    model.orderRunning
                        || (orderIDs[item.id] ?? item.suggestedOrderID)
                            .trimmingCharacters(in: .whitespacesAndNewlines).isEmpty
                )
            }
        }
        .padding(10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(AppPalette.subtleSurface)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }

    /// 将文件变化类型转换为中文标签。
    /// - Parameters:
    ///   - type: 文件或业务变化的类型代码。
    private func changeTypeName(_ type: String) -> String {
        switch type {
        case "added": return "新增"
        case "removed": return "删除"
        case "renamed": return "改名"
        case "missing_report": return "缺少报表"
        default: return "修改"
        }
    }

    /// 为新增、修改、删除等变化选择图标。
    /// - Parameters:
    ///   - type: 文件或业务变化的类型代码。
    private func changeIcon(_ type: String) -> String {
        switch type {
        case "added": return "plus.circle.fill"
        case "removed": return "minus.circle.fill"
        case "renamed": return "arrow.right.circle.fill"
        case "missing_report": return "doc.questionmark.fill"
        default: return "pencil.circle.fill"
        }
    }

    /// 为文件或材料变化类型选择强调色。
    /// - Parameters:
    ///   - type: 文件或业务变化的类型代码。
    private func changeColor(_ type: String) -> Color {
        switch type {
        case "added": return AppPalette.success
        case "removed": return AppPalette.danger
        case "renamed": return AppPalette.accent
        case "missing_report": return AppPalette.warning
        default: return AppPalette.warning
        }
    }

    /// 将变化时间转换为详情中的可读标签。
    /// - Parameters:
    ///   - change: 待显示的 Server 文件变化。
    private func changeTimeLabel(_ change: ServerChangePreview) -> String {
        switch change.changeType {
        case "added": return "创建时间：\(appDisplayTimestamp(change.eventTime))"
        case "modified": return "修改时间：\(appDisplayTimestamp(change.eventTime))"
        case "renamed": return "改名时间：\(appDisplayTimestamp(change.eventTime))"
        default: return "记录时间：\(appDisplayTimestamp(change.eventTime))"
        }
    }
}

struct OrderCostSheet: View {
    @ObservedObject var model: AppModel
    private let orderCostSourceColumns = Array(
        repeating: GridItem(.flexible(), spacing: 8, alignment: .center),
        count: 3
    )

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack(alignment: .center, spacing: 12) {
                VStack(alignment: .leading, spacing: 4) {
                    Text("订单成本 (\(model.selectedOrderId))")
                        .font(.title2.weight(.semibold))
                }
                Spacer(minLength: 12)
                HStack(spacing: 8) {
                    Button("导出 Excel") {
                        model.calculateSelectedOrderCost(export: true)
                    }
                    .buttonStyle(.glassProminent)
                    .disabled(model.orderRunning)
                    Button("关闭") { model.showCostSheet = false }
                        .appActionButton(minWidth: 72)
                }
            }
            .padding(.top, 8)
            .padding(.bottom, 6)
            Divider()
            VStack(alignment: .leading, spacing: 14) {
                LazyVGrid(
                    columns: Array(repeating: GridItem(.flexible(), spacing: 12), count: 4),
                    spacing: 12
                ) {
                    costCard("总成本", value: model.orderCostTotal.map { $0.formatted(.number.precision(.fractionLength(2))) } ?? "待补充", warning: model.orderCostTotal == nil)
                    costCard("已确认成本", value: model.orderCostKnown.formatted(.number.precision(.fractionLength(2))), warning: false)
                    costCard("成本行数", value: model.orderCostLines.count.formatted(), warning: false)
                    costCard("状态", value: model.orderCostMissingItems.isEmpty ? "已完成" : "待补充", warning: !model.orderCostMissingItems.isEmpty)
                }
                .padding(.trailing, 12)

                if !model.orderCostMissingItems.isEmpty {
                    GroupBox {
                        VStack(alignment: .leading, spacing: 6) {
                            ForEach(model.orderCostMissingItems, id: \.self) { item in
                                Label(item, systemImage: "exclamationmark.triangle.fill")
                                    .font(.caption)
                                    .foregroundColor(AppPalette.warning)
                                    .fixedSize(horizontal: false, vertical: true)
                            }
                        }
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .padding(.vertical, 4)
                    }
                }

                GroupBox("成本来源") {
                    VStack(spacing: 0) {
                        LazyVGrid(columns: orderCostSourceColumns, spacing: 0) {
                            Text("材料类型")
                            Text("成本")
                            Text("状态")
                        }
                        .font(.caption.weight(.semibold)).foregroundColor(.secondary)
                        .padding(.vertical, 7)
                        Divider()
                        ForEach(orderCostSourceTotals) { row in
                            LazyVGrid(columns: orderCostSourceColumns, spacing: 0) {
                                Text(row.factoryOrder).lineLimit(1)
                                Text(row.hasMissing ? "待补充" : row.total.formatted(.number.precision(.fractionLength(2))))
                                Text(row.hasMissing ? "待补充" : "已完成")
                                    .foregroundColor(row.hasMissing ? AppPalette.warning : AppPalette.success)
                            }
                            .padding(.vertical, 7)
                            Divider()
                        }
                    }
                }

                GroupBox("成本明细") {
                    ScrollView(.vertical) {
                        VStack(spacing: 0) {
                            costLineHeader
                            ForEach(model.orderCostLines) { row in
                                costLine(row)
                                Divider()
                            }
                        }
                    }
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
            .padding(.vertical, 14)
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
        }
        .padding(20)
        .frame(minWidth: 700, idealWidth: 900, minHeight: 560, idealHeight: 720)
        .background(LiquidGlassPreviewBackdrop())
    }

    /// 构造订单成本汇总卡片并标识缺失信息。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - value: 需要显示的数值或状态文字。
    ///   - warning: 是否显示警告样式。
    private func costCard(_ title: String, value: String, warning: Bool) -> some View {
        VStack(alignment: .leading, spacing: 5) {
            Text(title).font(.caption).foregroundColor(.secondary)
            Text(value).font(.title3.weight(.semibold)).foregroundColor(warning ? AppPalette.warning : AppPalette.accent)
        }
        .frame(maxWidth: .infinity, alignment: .leading)
        .padding(10)
        .background(AppPalette.surface)
        .clipShape(RoundedRectangle(cornerRadius: 8))
        .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
    }

    private var costLineHeader: some View {
        HStack(spacing: 8) {
            Text("类别").frame(width: 70, alignment: .center)
            Text("SKU").frame(width: 68, alignment: .center)
            Text("商品").frame(maxWidth: .infinity, alignment: .center)
            Text("数量").frame(width: 68, alignment: .center)
            Text("单位").frame(width: 50, alignment: .center)
            Text("单价").frame(width: 72, alignment: .center)
            Text("金额").frame(width: 92, alignment: .center)
        }
        .font(.caption.weight(.semibold)).foregroundColor(.secondary)
        .multilineTextAlignment(.center)
        .padding(.vertical, 7)
    }

    /// 显示成本项目的数量、单价、金额和缺失提示。
    /// - Parameters:
    ///   - row: 成本项目。
    private func costLine(_ row: OrderCostLine) -> some View {
        HStack(spacing: 8) {
            Text(row.category)
                .frame(width: 70, alignment: .center)
            Text(row.productCode.isEmpty ? "—" : row.productCode)
                .foregroundColor(row.productCode.isEmpty ? .secondary : .primary)
                .lineLimit(1)
                .frame(width: 68, alignment: .center)
            Text(row.name).lineLimit(1)
            .frame(maxWidth: .infinity, alignment: .leading)
            Text(row.quantity.formatted())
                .frame(width: 68, alignment: .center)
            Text(row.unit)
                .frame(width: 50, alignment: .center)
            Text(row.costPrice?.formatted(.number.precision(.fractionLength(2))) ?? "—")
                .frame(width: 72, alignment: .center)
            VStack(alignment: .center, spacing: 2) {
                Text(row.amount?.formatted(.number.precision(.fractionLength(2))) ?? "待补充")
                    .foregroundColor(row.amount == nil ? AppPalette.warning : .primary)
                if !row.missing.isEmpty {
                    Text(row.missing)
                        .font(.caption2)
                        .foregroundColor(AppPalette.warning)
                        .lineLimit(1)
                }
            }
                .frame(width: 92, alignment: .center)
        }
        .font(.caption)
        .padding(.vertical, 7)
    }

    /// 按成本来源类别构造汇总金额与缺失状态。
    private var orderCostSourceTotals: [OrderCostFactoryTotal] {
        [
            sourceTotal(
                id: "materials",
                title: "板材及封边条",
                categories: ["板材", "封边条"]
            ),
            sourceTotal(
                id: "hardware",
                title: "五金",
                categories: ["五金"]
            ),
        ]
    }

    /// 按来源类别汇总成本金额并判断是否有缺失单价。
    /// - Parameters:
    ///   - id: 记录或请求的唯一标识。
    ///   - title: 界面或操作记录的标题。
    ///   - categories: 计入此成本汇总的来源类别。
    private func sourceTotal(
        id: String,
        title: String,
        categories: [String]
    ) -> OrderCostFactoryTotal {
        let lines = model.orderCostLines.filter { categories.contains($0.category) }
        return OrderCostFactoryTotal(
            id: id,
            factoryOrder: title,
            total: lines.reduce(0) { $0 + ($1.amount ?? 0) },
            hasMissing: lines.contains { !$0.missing.isEmpty }
        )
    }
}

struct ServerProcessingOptionsSheet: View {
    @ObservedObject var model: AppModel

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            Text("处理 Server 文件夹")
                .font(.title2.weight(.semibold))
            Text("系统将重新读取报表并写入中央数据库；Traveler 仅在需要打印或导出时按需生成。")
                .font(.callout)
                .foregroundColor(.secondary)
            Toggle("出库包含五金件", isOn: $model.includeHardwareForServerProcessing)
                .toggleStyle(.checkbox)
            Text("关闭后，即使文件夹中有 Fittingslist，本次也不会写入五金事实，库存出库不会包含五金。")
                .font(.caption)
                .foregroundColor(.secondary)
            Spacer()
            HStack {
                Spacer()
                Button("取消") {
                    model.showServerProcessingOptions = false
                    model.pendingServerFolderURL = nil
                }
                .appActionButton(minWidth: 88)
                Button("开始处理") {
                    guard let folder = model.pendingServerFolderURL else { return }
                    model.showServerProcessingOptions = false
                    model.pendingServerFolderURL = nil
                    model.processSelectedServerFolder(
                        folder,
                        includeHardware: model.includeHardwareForServerProcessing
                    )
                }
                .buttonStyle(.glassProminent)
                .appActionButton(minWidth: 100)
                .disabled(model.orderRunning)
            }
        }
        .padding(24)
        .background(LiquidGlassPreviewBackdrop())
    }
}

struct CurrentIssuesSheet: View {
    @ObservedObject var model: AppModel
    @State private var orderIDs: [String: String] = [:]

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    Text("当前未解决问题")
                        .font(.title2.weight(.semibold))
                    Text("这里只显示当前仍存在的问题；历史操作记录保留在数据库中，但不会在新打开 App 时重复显示。")
                        .font(.callout)
                        .foregroundColor(.secondary)
                }
                Spacer()
                AppStatusBadge(text: "\(model.currentIssues.count) 项", kind: .warning)
            }

            if model.currentIssues.isEmpty {
                ContentUnavailableView("当前没有未解决问题", systemImage: "checkmark.circle", description: Text("系统会在扫描和处理 Server 时自动更新此列表。"))
            } else {
                AppSurfaceCard(padding: 0) {
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 0) {
                            ForEach(model.currentIssues) { issue in
                                VStack(alignment: .leading, spacing: 8) {
                                    HStack(alignment: .top, spacing: 10) {
                                        Image(systemName: issue.kind == "factory_ownership" ? "person.crop.circle.badge.questionmark" : "exclamationmark.triangle.fill")
                                            .foregroundColor(AppPalette.warning)
                                            .frame(width: 22, height: 22)
                                        VStack(alignment: .leading, spacing: 4) {
                                            Text(issue.factoryOrder.isEmpty ? (issue.orderId.isEmpty ? "当前问题" : issue.orderId) : issue.factoryOrder)
                                                .font(.headline)
                                            Text(issue.message)
                                                .fixedSize(horizontal: false, vertical: true)
                                            if !issue.path.isEmpty {
                                                Text(issue.path)
                                                    .font(.caption.monospaced())
                                                    .foregroundColor(.secondary)
                                                    .textSelection(.enabled)
                                                    .lineLimit(2)
                                            }
                                        }
                                    }
                                    HStack(spacing: 10) {
                                        if !issue.path.isEmpty {
                                            Button("打开所在文件夹") { model.openDashboardLocation(issue.path) }
                                                .buttonStyle(.link)
                                        }
                                        if issue.kind == "factory_ownership" {
                                            TextField(
                                                "确认订单号，如 PP0037",
                                                text: Binding(
                                                    get: { orderIDs[issue.id] ?? "" },
                                                    set: { orderIDs[issue.id] = $0 }
                                                )
                                            )
                                            .textFieldStyle(.roundedBorder)
                                            .frame(width: 180)
                                            Button("自动处理") { model.autoResolveCurrentIssue(issue) }
                                                .buttonStyle(.glass)
                                                .disabled(model.orderRunning)
                                            Button("确认归属") { model.resolveCurrentIssue(issue, orderID: orderIDs[issue.id] ?? "") }
                                                .buttonStyle(.glassProminent)
                                                .disabled(model.orderRunning || (orderIDs[issue.id] ?? "").trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                                        } else if currentIssueRequiresInventoryMapping(issue) {
                                            Button("处理订单文件映射") { model.requestInventoryMapping(folderPath: issue.path, message: issue.message) }
                                                .buttonStyle(.glassProminent)
                                                .disabled(model.orderRunning)
                                        } else {
                                            Button("标记已处理") { model.resolveCurrentIssue(issue, orderID: "") }
                                                .buttonStyle(.glass)
                                                .disabled(model.orderRunning)
                                        }
                                        Spacer()
                                    }
                                }
                                .padding(14)
                                if issue.id != model.currentIssues.last?.id { Divider() }
                            }
                        }
                    }
                }
            }

            HStack {
                Spacer()
                Button("关闭") { model.showCurrentIssuesPrompt = false }
                    .appActionButton(minWidth: 80)
            }
        }
        .padding(20)
        .background(LiquidGlassPreviewBackdrop())
    }
}

struct ServerChangesSheet: View {
    @ObservedObject var model: AppModel
    @State private var manualHandlingGroup: ServerFolderChangeGroup?

    var body: some View {
        let groups = serverFolderChangeGroups(model.pendingServerChanges)
        let selectedCount = groups.filter { model.selectedServerFolderPaths.contains($0.folderPath) }.count
        VStack(alignment: .leading, spacing: 16) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 5) {
                    Text("发现 Server 数据变化")
                        .font(.title2.weight(.semibold))
                    Text("以下变化尚未解析，也没有修改订单数据库。点击“自动处理”后，系统才会读取相关报表并更新看板。")
                        .font(.callout)
                        .foregroundColor(.secondary)
                }
                Spacer()
                AppStatusBadge(text: "\(groups.count) 个文件夹待处理", kind: .warning)
            }

            HStack(spacing: 10) {
                Text("请选择一个要自动处理的文件夹（已选 \(selectedCount) 个）")
                    .font(.callout.weight(.semibold))
                Spacer()
                Button("取消选择") { model.clearServerFolderSelection() }
                    .buttonStyle(.link)
                    .disabled(selectedCount == 0)
            }

            AppSurfaceCard(padding: 0) {
                ScrollView {
                    LazyVStack(spacing: 0) {
                        ForEach(groups) { group in
                            let selected = model.selectedServerFolderPaths.contains(group.folderPath)
                            HStack(alignment: .top, spacing: 12) {
                                Button {
                                    model.toggleServerFolderSelection(group.folderPath)
                                } label: {
                                    HStack(alignment: .top, spacing: 12) {
                                        Image(systemName: selected ? "checkmark.square.fill" : "square")
                                            .foregroundColor(selected ? AppPalette.accent : .secondary)
                                            .font(.system(size: 20, weight: .semibold))
                                            .frame(width: 22, height: 22)
                                        VStack(alignment: .leading, spacing: 5) {
                                            HStack(spacing: 8) {
                                                Text(group.manualOnly ? "临时订单文件夹" : (group.orderId.isEmpty ? "混单文件夹" : group.orderId))
                                                    .fontWeight(.semibold)
                                                Text(group.folderName)
                                                    .font(.caption)
                                                    .foregroundColor(.secondary)
                                            }
                                            Text("包含 \(group.changes.count) 项变化：")
                                                .font(.caption)
                                                .foregroundColor(.secondary)
                                            ForEach(group.changes) { change in
                                                HStack(alignment: .top, spacing: 6) {
                                                    Image(systemName: changeIcon(change.changeType))
                                                        .foregroundColor(changeColor(change.changeType))
                                                        .frame(width: 16)
                                                    VStack(alignment: .leading, spacing: 2) {
                                                        Text("\(serverChangeTypeName(change.changeType))：\(displayPathName(change.path))")
                                                            .font(.caption)
                                                        Text(change.path)
                                                            .font(.caption2)
                                                            .foregroundColor(.secondary)
                                                            .lineLimit(1)
                                                    }
                                                }
                                            }
                                            if group.manualOnly && !group.independentManual {
                                                Text("自动处理时将校验文件格式，优先读取 material；缺少时从 Report 生成材料并尝试出库，失败会保留在待处理清单。")
                                                    .font(.caption)
                                                    .foregroundColor(.orange)
                                            }
                                        }
                                        Spacer(minLength: 0)
                                    }
                                    .contentShape(Rectangle())
                                }
                                .buttonStyle(.plain)
                                .frame(maxWidth: .infinity, alignment: .leading)
                                if !group.changes.contains(where: { $0.handlingMode == "layout_review" }) && (group.manualOnly || group.requiresManualReview || group.changes.contains(where: { $0.handlingMode == "aicnc" })) {
                                    HStack(spacing: 8) {
                                        Spacer(minLength: 0)
                                        ServerFolderIgnoreButton(model: model, group: group)
                                        if group.manualOnly {
                                            Button {
                                                manualHandlingGroup = group
                                            } label: {
                                                Text("已人工处理").frame(width: 112)
                                            }
                                            .buttonStyle(.glassProminent)
                                            .controlSize(.regular)
                                            .disabled(model.orderRunning || model.inventoryRunning)
                                        }
                                    }
                                }
                            }
                            .padding(12)
                            if group.id != groups.last?.id { Divider() }
                        }
                    }
                }
            }

            HStack {
                Text("选择“稍后处理”后，下次扫描仍会再次提醒；只有勾选的文件夹会进入自动处理，失败的文件夹会继续保留。")
                    .font(.caption)
                    .foregroundColor(.secondary)
                Spacer()
                Button("稍后处理") { model.showServerChangesPrompt = false }
                    .appActionButton(minWidth: 108)
                    .disabled(model.orderRunning)
                Button("预览并逐单确认") { model.processPendingServerChanges() }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 118)
                    .disabled(model.orderRunning || selectedCount == 0)
            }
        }
        .padding(20)
        .background(LiquidGlassPreviewBackdrop())
        .sheet(item: $manualHandlingGroup) { group in
            FolderManualHandlingSheet(model: model, group: group)
        }
    }

    /// 为新增、修改、删除等变化选择图标。
    /// - Parameters:
    ///   - type: 文件或业务变化的类型代码。
    private func changeIcon(_ type: String) -> String {
        switch type {
        case "added": return "plus.circle.fill"
        case "removed": return "minus.circle.fill"
        default: return "pencil.circle.fill"
        }
    }

    /// 为文件或材料变化类型选择强调色。
    /// - Parameters:
    ///   - type: 文件或业务变化的类型代码。
    private func changeColor(_ type: String) -> Color {
        switch type {
        case "added": return AppPalette.success
        case "removed": return AppPalette.danger
        default: return AppPalette.warning
        }
    }
}

struct HardwareSourceSelectionSheet: View {
    @ObservedObject var model: AppModel
    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            Text("确认工厂单五金来源").font(.title2.bold())
            Text("首次选择确认写入后，来源固定。以后只有报表内容变化时，才可选择保留已确认五金或更新；当前仍是预览。")
                .foregroundStyle(.secondary)
            ScrollView {
                VStack(alignment: .leading, spacing: 18) {
                    ForEach(model.hardwareSourceConflicts) { conflict in
                        Text(conflict.id).font(.headline)
                        ForEach(conflict.candidates) { candidate in
                            sourceCard(candidate, factoryOrder: conflict.id)
                        }
                    }
                }
            }
            Divider()
            HStack {
                Button("稍后处理") { model.showHardwareSourceSelection = false }
                Spacer()
                Button("按所选来源重新预览") { model.confirmHardwareSourceSelection() }
                    .buttonStyle(.glassProminent).disabled(!model.canResumeHardwareSourcePreview)
            }
        }.padding(22).frame(width: 820, height: 620)
    }

    /// 用精简数字格式显示材料或五金数量。
    /// - Parameters:
    ///   - value: 待格式化的材料或五金数量。
    private func formatQuantity(_ value: Double) -> String {
        value.rounded() == value ? String(format: "%.0f", value) : String(format: "%.2f", value)
    }

    // 整张卡片都是按钮，包括内容行和留白区域。
    /// 把五金来源报表及其项目绘制为整张可点击的选择卡片。
    /// - Parameters:
    ///   - candidate: 待选择的五金来源报表及项目。
    ///   - factoryOrder: 目标工厂单号。
    private func sourceCard(_ candidate: HardwareSourceCandidate, factoryOrder: String) -> some View {
        let selected = model.hardwareSourceChoices[factoryOrder] == candidate.id
        let folder = displayPathName(displayParentPath(displayParentPath(candidate.path)))
        return Button {
            model.hardwareSourceChoices[factoryOrder] = candidate.id
        } label: {
            VStack(alignment: .leading, spacing: 10) {
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: selected ? "largecircle.fill.circle" : "circle")
                        .foregroundStyle(selected ? Color.accentColor : .secondary)
                    VStack(alignment: .leading, spacing: 4) {
                        Text(folder).font(.headline)
                        Text(displayPathName(candidate.path)).font(.subheadline)
                        Text(candidate.path)
                            .font(.caption).foregroundStyle(.secondary)
                            .fixedSize(horizontal: false, vertical: true)
                    }
                }
                Divider()
                VStack(alignment: .leading, spacing: 8) {
                    ForEach(Array(candidate.items.enumerated()), id: \.offset) { _, item in
                        HStack(alignment: .top, spacing: 12) {
                            VStack(alignment: .leading, spacing: 2) {
                                Text(item.name).font(.callout)
                                if !item.spec.isEmpty {
                                    Text(item.spec).font(.caption).foregroundStyle(.secondary)
                                }
                            }
                            .frame(maxWidth: .infinity, alignment: .leading)
                            Text(item.code.isEmpty ? "—" : item.code)
                                .font(.caption.monospaced()).foregroundStyle(.secondary)
                                .frame(width: 110, alignment: .leading)
                            Text("× \(formatQuantity(item.quantity)) \(item.unit)")
                                .font(.caption.monospacedDigit())
                                .frame(width: 100, alignment: .trailing)
                        }
                    }
                }
                .padding(.leading, 24)
            }
            .multilineTextAlignment(.leading)
            .padding(12)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background(selected ? Color.accentColor.opacity(0.08) : AppPalette.subtleSurface)
            .clipShape(RoundedRectangle(cornerRadius: 10))
            .overlay {
                RoundedRectangle(cornerRadius: 10)
                    .strokeBorder(selected ? Color.accentColor : .clear, lineWidth: 1.5)
            }
            .contentShape(Rectangle())
        }
        .buttonStyle(.plain)
        .accessibilityLabel("选择此报表，\(folder)，\(displayPathName(candidate.path))")
        .accessibilityValue(selected ? "已选中" : "未选中")
    }

}

struct ServerWriteConfirmationSheet: View {
    @ObservedObject var model: AppModel
    @State private var mappingTarget: PendingInventoryMappingTarget?
    @State private var ignoreTarget: PendingInventoryMappingTarget?
    @State private var skippedHardwareOrderIDs: Set<String> = []
    @State private var showWriteConfirmation = false
    @State private var collapsedFactoryIDs: Set<String> = []
    /// 在任务空闲、预览有效且所有校验通过时允许确认 Server 写入。
    private var canConfirmWrite: Bool {
        !model.orderRunning && !model.inventoryRunning && !orders.isEmpty &&
        !model.serverWriteConfirmationFinished && !model.serverWritePreviewNeedsRefresh && activeHardwareRequirements.isEmpty && invalidOrderValidations.isEmpty
    }
    /// 读取当前 Server 确认预览中的订单列表。
    private var orders: [ServerWriteOrderPreview] { model.serverWritePreview?.orders ?? [] }
    /// 排除已选择跳过五金的订单，得到仍需处理的 SKU 映射要求。
    private var activeHardwareRequirements: [ServerHardwareMappingRequirement] {
        model.serverHardwareMappingRequirements.filter { requirement in
            requirement.orderIDs.isEmpty || requirement.orderIDs.contains {
                !skippedHardwareOrderIDs.contains($0.uppercased())
            }
        }
    }
    /// 取得尚未通过正常校验的 Server 订单预览。
    private var invalidOrderValidations: [ServerWriteOrderPreview] {
        orders.filter { $0.validationStatus != "正常" }
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(alignment: .top) {
                VStack(alignment: .leading, spacing: 5) {
                    AppStatusBadge(text: "写入前确认", kind: .warning)
                    Text("确认 Server 订单材料")
                        .font(.title2.weight(.semibold))
                }
                Spacer()
                if activeHardwareRequirements.isEmpty && orders.contains(where: { !$0.hardwareChanges.isEmpty || $0.factories.contains(where: { !$0.hardware.isEmpty }) }) {
                    Label("SKU 校验已通过", systemImage: "checkmark.circle.fill")
                        .font(.callout.weight(.medium))
                        .foregroundStyle(AppPalette.success)
                        .padding(.horizontal, 12).padding(.vertical, 8)
                        .background(AppPalette.success.opacity(0.08), in: Capsule())
                }
            }

            if let sources = model.serverWritePreview?.payload["hardware_selected_sources"] as? [[String: Any]], !sources.isEmpty {
                DisclosureGroup("五金来源（\(sources.count) 张工厂单）") {
                    ForEach(Array(sources.enumerated()), id: \.offset) { _, source in
                        Text("\(source["factory_order"] as? String ?? "")：\(source["path"] as? String ?? "")")
                            .font(.caption).textSelection(.enabled)
                    }

                }
            }

            if !model.serverWriteConfirmationNotice.isEmpty {
                let noticeColor = model.serverWriteConfirmationNoticeIsError
                    ? AppPalette.danger
                    : AppPalette.success
                HStack(alignment: .top, spacing: 8) {
                    Image(systemName: model.serverWriteConfirmationNoticeIsError
                        ? "exclamationmark.triangle.fill"
                        : "checkmark.circle.fill")
                    Text(model.serverWriteConfirmationNotice)
                        .multilineTextAlignment(.leading)
                }
                .font(.callout.weight(.medium))
                .foregroundColor(noticeColor)
                .padding(12)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(noticeColor.opacity(0.10))
                .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
            }

            if model.serverWritePreviewNeedsRefresh && !model.orderRunning {
                Button("重试刷新五金预览") { model.refreshServerHardwarePreview() }
                    .disabled(model.inventoryRunning)
            }
            hardwareMappingSection

            if !invalidOrderValidations.isEmpty {
                VStack(alignment: .leading, spacing: 7) {
                    HStack(alignment: .firstTextBaseline) {
                        Text("订单校验未通过")
                            .font(.subheadline.weight(.semibold))
                        Spacer()
                        AppStatusBadge(text: "禁止确认写入", kind: .danger)
                    }
                    Text("请修正 Server 报表后重新读取；本次预览不会把未通过校验的订单写入正式数据库。")
                        .font(.caption)
                        .foregroundColor(.secondary)
                    ForEach(invalidOrderValidations) { order in
                        VStack(alignment: .leading, spacing: 3) {
                            Text("订单 \(order.orderID)：\(order.validationStatus.isEmpty ? "待校验" : order.validationStatus)")
                                .font(.caption.weight(.semibold))
                            if !order.validationMessage.isEmpty {
                                Text(order.validationMessage)
                                    .font(.caption)
                                    .foregroundColor(AppPalette.danger)
                            }
                        }
                    }
                }
                .padding(12)
                .frame(maxWidth: .infinity, alignment: .leading)
                .background(AppPalette.danger.opacity(0.08))
                .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
            }

            if orders.isEmpty {
                ContentUnavailableView("没有可确认的订单材料", systemImage: "exclamationmark.triangle", description: Text("请稍后重新扫描，或检查 Server 材料文件。"))
            } else {
                ScrollView {
                    LazyVStack(alignment: .leading, spacing: 14) {
                        ForEach(orders) { order in
                            orderPreviewCard(order)
                        }
                    }
                    .padding(.trailing, 6)
                }
                .frame(maxHeight: .infinity)
            }

            HStack {
                Text(model.serverWritePreview?.canAcknowledgeNoChanges == true
                    ? "材料和五金没有待写入变化；确认后更新文件夹监控状态并关闭，以后文件变化仍会提醒。"
                    : !invalidOrderValidations.isEmpty
                    ? "存在未通过订单校验的预览，修正报表并重新读取后才能确认写入。"
                    : activeHardwareRequirements.isEmpty
                        ? "确认后写入订单级板材/封边；五金按每个来料加工订单的选择写入或跳过，已出货工厂单不再处理。"
                        : "请先完成全部五金 SKU 映射或忽略，再确认写入。")
                    .font(.caption)
                    .foregroundColor(.secondary)
                Spacer()
                Button(model.serverWriteConfirmationFinished ? "关闭" : "稍后处理") {
                    model.showServerWriteConfirmation = false
                }
                .appActionButton(minWidth: 92)
                .disabled(model.orderRunning)
                if model.serverWritePreview?.canAcknowledgeNoChanges == true && !model.serverWriteConfirmationFinished {
                    Button("确认无变化") {
                        model.acknowledgeServerPreview()
                    }
                    .buttonStyle(.glassProminent)
                    .disabled(!canConfirmWrite)
                    .help("更新本次预览的文件夹监控基线并关闭；以后文件变化仍会提醒")
                } else {
                    Button(model.serverWriteConfirmationFinished ? "已完成写入" : "确认写入订单材料和五金") {
                        showWriteConfirmation = true
                    }
                    .buttonStyle(.glassProminent)
                    .disabled(!canConfirmWrite)
                }
            }
        }
        .padding(20)
        .background(LiquidGlassPreviewBackdrop())
        .alert("确认后写入", isPresented: $showWriteConfirmation) {
            Button("取消", role: .cancel) { }
            Button("确认写入") {
                guard canConfirmWrite else { return }
                model.confirmServerMaterialPreview(skipHardwareOrderIDs: skippedHardwareOrderIDs)
            }
        } message: {
            Text("将写入 \(orders.map(\.orderID).joined(separator: "、")) 的订单材料及本次选定五金。已出货工厂单自动排除。")
        }
        .sheet(item: $mappingTarget) { target in
            InventoryMappingSheet(
                model: model,
                travelerName: target.name,
                isPresented: Binding(
                    get: { mappingTarget != nil },
                    set: { if !$0 { mappingTarget = nil } }
                ),
                saveAction: { name, code in
                    model.saveServerHardwareMapping(name: name, productCode: code)
                }
            )
        }
        .sheet(item: $ignoreTarget) { target in
            PendingInventoryIgnoreSheet(
                model: model,
                travelerName: target.name,
                saveAction: { name, reason in
                    model.saveServerHardwareIgnoredMapping(name: name, reason: reason)
                }
            )
        }
    }

    @ViewBuilder
    private var hardwareMappingSection: some View {
        let requirements = activeHardwareRequirements
        if !requirements.isEmpty {
            VStack(alignment: .leading, spacing: 8) {
                HStack(alignment: .firstTextBaseline) {
                    Text("工厂单五金 SKU 校验")
                        .font(.subheadline.weight(.semibold))
                    Spacer()
                    Text(requirements.isEmpty ? "已通过" : "待处理 \(requirements.count) 项")
                        .font(.caption.weight(.semibold))
                        .foregroundColor(requirements.isEmpty ? AppPalette.success : AppPalette.warning)
                }
                if !requirements.isEmpty {
                    Text("以下五金没有有效 SKU。请选择映射或忽略；完成后仍在本界面继续确认写入。")
                        .font(.caption)
                        .foregroundColor(AppPalette.warning)
                    ForEach(requirements) { item in
                        HStack(alignment: .top, spacing: 10) {
                            VStack(alignment: .leading, spacing: 3) {
                                Text(item.name).font(.body.weight(.semibold))
                                let source = item.sourceCode.isEmpty ? "" : "来源编码：\(item.sourceCode)"
                                let factories = item.factoryOrders.isEmpty ? "" : "工厂单：\(item.factoryOrders.joined(separator: "、"))"
                                Text([source, factories].filter { !$0.isEmpty }.joined(separator: " · "))
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                            Spacer()
                            Button("映射 SKU") {
                                mappingTarget = PendingInventoryMappingTarget(name: item.name)
                            }
                            .buttonStyle(.glassProminent)
                            .disabled(model.inventoryRunning || model.orderRunning)
                            Button("忽略") {
                                ignoreTarget = PendingInventoryMappingTarget(name: item.name)
                            }
                            .buttonStyle(.glass)
                            .disabled(model.inventoryRunning || model.orderRunning)
                        }
                        .padding(.vertical, 6)
                        Divider()
                    }
                }
            }
            .padding(12)
            .background(AppPalette.surface)
            .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
        }
    }

    /// 用精简数字格式显示材料或五金数量。
    /// - Parameters:
    ///   - value: 待格式化的材料或五金数量。
    private func formatQuantity(_ value: Double) -> String {
        value.rounded() == value ? String(Int(value)) : String(format: "%.2f", value)
    }

    /// 显示 Server 订单材料和工厂单变化的确认卡片。
    /// - Parameters:
    ///   - order: Server 订单写入预览。
    @ViewBuilder
    private func orderPreviewCard(_ order: ServerWriteOrderPreview) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .firstTextBaseline, spacing: 10) {
                Text(order.orderID).font(.title3.weight(.semibold))
                Divider().frame(height: 16)
                AppStatusBadge(
                    text: order.validationStatus == "正常" ? "订单校验正常" : (order.validationStatus.isEmpty ? "待校验" : order.validationStatus),
                    kind: order.validationStatus == "正常" ? .success : .danger
                )
                Spacer()
            }
            if !order.validationMessage.isEmpty {
                Text(order.validationMessage)
                    .font(.caption)
                    .foregroundColor(order.validationStatus == "正常" ? .secondary : AppPalette.danger)
            }

            if order.orderType == "cutToSize" && !order.factories.isEmpty {
                cutToSizeHardwareChoice(for: order)
            }

            if !order.materialChanges.isEmpty {
                VStack(alignment: .leading, spacing: 0) {
                    Text("订单材料 · \(order.materialChanges.count) 项")
                        .font(.headline)
                        .padding(12)
                        .frame(maxWidth: .infinity, alignment: .leading)
                        .background(AppPalette.accent.opacity(0.05))
                    materialHeaderRow
                    ForEach(sortedServerWriteMaterialChanges(order.materialChanges)) { material in
                        Divider()
                        materialChangeRow(material)
                    }
                }
            } else {
                Text("订单材料数量没有变化")
                    .font(.body).foregroundColor(.secondary)
            }

            if !order.factories.isEmpty {
                Text("工厂单五金").font(.headline).padding(.top, 4)
                ForEach(order.factories) { factory in
                    let key = order.orderID + "|" + factory.factoryOrder
                    DisclosureGroup(isExpanded: Binding(
                        get: { !collapsedFactoryIDs.contains(key) },
                        set: { expanded in
                            if expanded { collapsedFactoryIDs.remove(key) }
                            else { collapsedFactoryIDs.insert(key) }
                        }
                    )) {
                        VStack(spacing: 0) {
                            HStack(spacing: 10) {
                                Text("五金名称").frame(maxWidth: .infinity, alignment: .leading)
                                Text("来源编码").frame(width: 100, alignment: .leading)
                                Text("数量").frame(width: 56, alignment: .trailing)
                                Text("单位").frame(width: 40, alignment: .trailing)
                            }
                            .font(.caption.weight(.semibold)).foregroundStyle(.secondary)
                            .padding(.vertical, 10)
                            ForEach(factory.hardware) { hardware in
                                Divider()
                                HStack(alignment: .firstTextBaseline, spacing: 10) {
                                    Text(hardware.displayName.isEmpty ? hardware.name : hardware.displayName)
                                        .frame(maxWidth: .infinity, alignment: .leading)
                                        .fixedSize(horizontal: false, vertical: true)
                                    Text(hardware.productCode.isEmpty ? "—" : hardware.productCode)
                                        .font(.callout.monospaced())
                                        .frame(width: 100, alignment: .leading)
                                    Text(formatQuantity(hardware.quantity))
                                        .monospacedDigit().frame(width: 56, alignment: .trailing)
                                    Text(hardware.unit.isEmpty ? "—" : hardware.unit)
                                        .frame(width: 40, alignment: .trailing)
                                }
                                .font(.callout).padding(.vertical, 10)
                            }
                            if factory.hardware.isEmpty {
                                Text("本工厂单无待写入五金")
                                    .font(.callout).foregroundStyle(.secondary).padding(.vertical, 10)
                            }
                        }
                        .padding(.horizontal, 12)
                    } label: {
                        HStack(alignment: .firstTextBaseline, spacing: 10) {
                            Text(factory.factoryOrder).fontWeight(.semibold)
                            Text(factory.factoryName.isEmpty ? "—" : factory.factoryName)
                                .fixedSize(horizontal: false, vertical: true)
                            Spacer(minLength: 8)
                            Text("\(factory.hardware.count) 项").foregroundStyle(.secondary)
                        }
                        .font(.callout)
                        .padding(.vertical, 10)
                    }
                    .padding(.horizontal, 12)
                    .background(AppPalette.accent.opacity(0.045))
                    .clipShape(RoundedRectangle(cornerRadius: 10))
                }
            }

            if !order.existingHardwareChanges.isEmpty {
                VStack(alignment: .leading, spacing: 7) {
                    Text("五金种类和数量变化")
                        .font(.subheadline.weight(.semibold))
                        .foregroundColor(AppPalette.warning)
                    hardwareChangeHeaderRow()
                    ForEach(order.existingHardwareChanges) { hardware in
                        hardwareChangeRow(hardware)
                    }
                }
            }

            if !order.excludedFactories.isEmpty {
                DisclosureGroup {
                    VStack(alignment: .leading, spacing: 7) {
                        ForEach(order.excludedFactories) { factory in
                            let outboundText = factory.outboundDocument.isEmpty
                                ? "已出货"
                                : "已出货 · " + factory.outboundDocument
                            HStack(spacing: 10) {
                                Text(factory.factoryOrder).font(.body.weight(.semibold))
                                Text(factory.factoryName).lineLimit(1)
                                Spacer()
                                Text(outboundText)
                                    .font(.caption)
                                    .foregroundColor(.secondary)
                            }
                        }
                    }
                    .padding(.top, 6)
                } label: {
                    Text("已排除 \(order.excludedFactories.count) 个已出货工厂单")
                }
                .font(.subheadline)
                .foregroundColor(.secondary)
            }

            if !order.sourceFolder.isEmpty {
                Label(order.sourceFolder, systemImage: "folder")
                    .font(.caption)
                    .foregroundColor(.secondary)
                    .lineLimit(1)
            }
        }
        .padding(12)
        .background(AppPalette.surface.opacity(0.92))
        .clipShape(RoundedRectangle(cornerRadius: 12))
    }

    /// 显示 CUT TO SIZE 订单是否纳入五金写入的选项。
    /// - Parameters:
    ///   - order: Server 订单写入预览。
    @ViewBuilder
    private func cutToSizeHardwareChoice(for order: ServerWriteOrderPreview) -> some View {
        let orderID = order.orderID.uppercased()
        let skipped = skippedHardwareOrderIDs.contains(orderID)
        VStack(alignment: .leading, spacing: 7) {
            HStack(alignment: .firstTextBaseline) {
                Text("来料加工订单五金")
                    .font(.subheadline.weight(.semibold))
                Spacer()
                Text(skipped ? "本次不写入" : "本次写入")
                    .font(.caption.weight(.semibold))
                    .foregroundColor(skipped ? AppPalette.warning : AppPalette.success)
            }
            Text("该选择适用于订单 (order.orderID) 下全部未出货工厂单，不能按工厂单拆分。")
                .font(.caption)
                .foregroundColor(.secondary)
            HStack(spacing: 8) {
                if skipped {
                    Button("本次写入五金") {
                        skippedHardwareOrderIDs.remove(orderID)
                    }
                    .buttonStyle(.glass)
                    .tint(.secondary)
                    Button("本次不写入五金") {
                        skippedHardwareOrderIDs.insert(orderID)
                    }
                    .buttonStyle(.glassProminent)
                    .tint(AppPalette.warning)
                } else {
                    Button("本次写入五金") {
                        skippedHardwareOrderIDs.remove(orderID)
                    }
                    .buttonStyle(.glassProminent)
                    .tint(AppPalette.success)
                    Button("本次不写入五金") {
                        skippedHardwareOrderIDs.insert(orderID)
                    }
                    .buttonStyle(.glass)
                    .tint(.secondary)
                }
            }
            if skipped {
                let requirements = model.serverHardwareMappingRequirements.filter {
                    $0.orderIDs.contains(orderID)
                }
                if !requirements.isEmpty {
                    Text("本订单五金仍显示为来源事实，但本次不写入，也不要求 SKU 映射：\(requirements.map(\.name).joined(separator: "、"))")
                        .font(.caption)
                        .foregroundColor(AppPalette.warning)
                } else {
                    Text("本订单五金只保留在本次预览中，不写入工厂单五金事实。")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
            }
        }
        .padding(10)
        .background(AppPalette.surface.opacity(0.75))
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }

    private var materialHeaderRow: some View {
        HStack(spacing: 10) {
            Text("材料类型")
                .frame(width: 110, alignment: .leading).offset(x: 10)
            Text("颜色 / 规格").frame(maxWidth: .infinity, alignment: .leading)
            Text("变化").frame(width: 60, alignment: .center)
            Text("数量变化")
                .frame(width: 125, alignment: .trailing).offset(x: -5)
        }
        .font(.caption.weight(.semibold)).foregroundStyle(.secondary)
        .padding(.horizontal, 12).padding(.vertical, 9)
    }

    /// 显示材料规格、旧数量、新数量和变化差额。
    /// - Parameters:
    ///   - material: Server 材料数量变化。
    private func materialChangeRow(_ material: ServerWriteMaterialChange) -> some View {
        let specification = [material.color, material.thickness, material.edge]
            .filter { !$0.isEmpty }
            .reduce(into: [String]()) { values, value in
                if !values.contains(value) { values.append(value) }
            }.joined(separator: " · ")
        return HStack(alignment: .firstTextBaseline, spacing: 10) {
            Label(material.materialType, systemImage: material.materialType.caseInsensitiveCompare("edge") == .orderedSame ? "line.3.horizontal" : "square.3.layers.3d")
                .labelStyle(.titleAndIcon)
                .font(.body.weight(.medium))
                .frame(width: 110, alignment: .leading)
            Text(specification.isEmpty ? "—" : specification)
                .frame(maxWidth: .infinity, alignment: .leading)
                .fixedSize(horizontal: false, vertical: true)
            Text(material.changeType)
                .font(.caption)
                .foregroundColor(material.changeType == "删除" ? AppPalette.danger : AppPalette.warning)
                .frame(width: 60, alignment: .center)
            Text("\(formatQuantity(material.oldQuantity)) → \(formatQuantity(material.newQuantity)) \(material.unit)")
                .font(.body.monospacedDigit())
                .frame(width: 125, alignment: .trailing)
        }
        .padding(.horizontal, 12).padding(.vertical, 11)
    }

    /// 显示工厂单五金的身份及数量变化。
    /// - Parameters:
    ///   - hardware: 待显示的五金数量变化。
    private func hardwareChangeRow(_ hardware: ServerWriteHardwareChange) -> some View {
        HStack(spacing: 10) {
            Text(hardware.factoryOrder).font(.caption.weight(.semibold)).frame(width: 110, alignment: .leading)
            Text(hardware.productCode.isEmpty ? "—" : hardware.productCode)
                .font(.caption.monospaced())
                .frame(width: 90, alignment: .leading)
                .lineLimit(1)
            Text(hardware.displayName.isEmpty ? hardware.name : hardware.displayName)
                .frame(maxWidth: .infinity, alignment: .leading)
                .lineLimit(1)
            Text(serverHardwareUnitText(hardware.unit))
                .font(.caption)
                .foregroundColor(hardware.unit.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty ? .secondary : .primary)
                .frame(width: 55, alignment: .leading)
                .lineLimit(1)
            Text(hardware.changeType)
                .font(.caption)
                .foregroundColor(AppPalette.warning)
                .frame(width: 55, alignment: .leading)
            Text("\(formatQuantity(hardware.oldQuantity)) → \(formatQuantity(hardware.newQuantity))")
                .font(.caption.monospacedDigit())
                .frame(width: 100, alignment: .trailing)
        }
        .padding(.vertical, 5)
    }

    /// 构造五金变化明细的统一表头。
    /// 无参数。
    private func hardwareChangeHeaderRow() -> some View {
        HStack(spacing: 10) {
            Text("工厂单号").frame(width: 110, alignment: .leading)
            Text("SKU").frame(width: 90, alignment: .leading)
            Text("五金名称").frame(maxWidth: .infinity, alignment: .leading)
            Text("单位").frame(width: 55, alignment: .leading)
            Text("变化").frame(width: 55, alignment: .leading)
            Text("数量").frame(width: 100, alignment: .trailing)
        }
        .font(.caption.weight(.semibold))
        .foregroundColor(.secondary)
    }

    /// 显示待写入材料的规格、数量、单位及来源。
    /// - Parameters:
    ///   - material: Server 待写入材料。
    private func materialPreviewRow(_ material: ServerWriteMaterialPreview) -> some View {
        let isEdge = material.materialType.caseInsensitiveCompare("edge") == .orderedSame
        let descriptors = [material.color, material.thickness]
            .map { $0.trimmingCharacters(in: .whitespacesAndNewlines) }
            .filter { !$0.isEmpty }
        return HStack(spacing: 12) {
            Image(systemName: isEdge ? "line.3.horizontal" : "square.3.layers.3d")
                .font(.title3)
                .foregroundColor(AppPalette.accent)
                .frame(width: 28)
            VStack(alignment: .leading, spacing: 3) {
                Text(isEdge ? "封边" : "板材")
                    .font(.caption.weight(.semibold))
                    .foregroundColor(.secondary)
                Text(([material.materialType] + descriptors).joined(separator: " · "))
                    .font(.body.weight(.medium))
                    .lineLimit(2)
            }
            Spacer(minLength: 12)
            VStack(alignment: .trailing, spacing: 2) {
                Text(formatQuantity(material.quantity))
                    .font(.title3.weight(.semibold))
                Text(material.unit.isEmpty ? "—" : material.unit)
                    .font(.subheadline)
                    .foregroundColor(.secondary)
            }
        }
        .padding(.horizontal, 12)
        .padding(.vertical, 10)
        .background(AppPalette.surface)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }
}

/// 将五金单位转换为适合界面显示的文字。
/// - Parameters:
///   - unit: 材料或五金计量单位。
func serverHardwareUnitText(_ unit: String) -> String {
    let value = unit.trimmingCharacters(in: .whitespacesAndNewlines)
    return value.isEmpty ? "—" : value
}

private struct ServerWriteSelectionRow: Identifiable {
    let id: String
    let title: String
    let subtitle: String
}

struct FactoryStockComparisonSheet: View {
    @ObservedObject var model: AppModel
    let orderID: String

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack {
                VStack(alignment: .leading, spacing: 4) {
                    AppStatusBadge(text: "库存比对", kind: .info)
                    Text("订单 \(orderID) 库存汇总").font(.title2.weight(.semibold))
                    Text("板材、封边和五金均按订单汇总，不按工厂单拆分")
                        .font(.caption).foregroundColor(.secondary)
                }
                Spacer()
                if model.orderRunning { ProgressView().controlSize(.small) }
            }

            if model.orderStockRows.isEmpty {
                VStack(spacing: 8) {
                    ProgressView()
                    Text(model.orderStatus.isEmpty ? "正在查询订单材料和五金库存…" : model.orderStatus)
                        .font(.caption).foregroundColor(.secondary)
                }
                .frame(maxWidth: .infinity, minHeight: 240)
            } else {
                AppSurfaceCard(padding: 0) {
                    VStack(spacing: 0) {
                        stockHeader
                        Divider()
                        ForEach(model.orderStockRows) { row in
                            stockRow(row)
                            Divider()
                        }
                    }
                }
            }

            HStack {
                Text("库存查询失败时，按钮保持可用，允许手工再次查询。")
                    .font(.caption).foregroundColor(.secondary)
                Spacer()
                Button("再次查询") { model.checkSelectedOrderStock() }
                    .appActionButton(minWidth: 112)
                    .disabled(model.orderRunning || !model.orderPreviewReady)
            }
        }
        .padding(20)
        .background(LiquidGlassPreviewBackdrop())
    }

    private var stockHeader: some View {
        HStack(spacing: 0) {
            Text("商品").frame(maxWidth: .infinity, alignment: .center)
            Text("单位").frame(width: 60, alignment: .center)
            Text("需求").frame(width: 80, alignment: .center)
            Text("库存").frame(width: 80, alignment: .center)
            Text("结果").frame(width: 100, alignment: .center)
        }
        .font(.caption.weight(.semibold))
        .foregroundColor(.secondary)
        .padding(.vertical, 10)
        .background(AppPalette.subtleSurface)
    }

    /// 显示库存商品的需求、可用量和缺料状态。
    /// - Parameters:
    ///   - row: 实时库存预览。
    private func stockRow(_ row: OrderStockPreview) -> some View {
        HStack(spacing: 0) {
            VStack(alignment: .leading, spacing: 2) {
                Text(row.productName).fontWeight(.medium)
                Text(row.productCode).font(.caption2).foregroundColor(.secondary)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
            Text(row.unit.isEmpty ? "—" : row.unit).frame(width: 60, alignment: .center)
            Text(row.required.formatted()).frame(width: 80, alignment: .center)
            Text(row.available.formatted()).frame(width: 80, alignment: .center)
            Text(row.sufficient ? "充足" : "缺 \(row.shortage.formatted())")
                .fontWeight(.semibold)
                .foregroundColor(row.sufficient ? AppPalette.success : AppPalette.warning)
                .frame(width: 100, alignment: .center)
        }
        .padding(.vertical, 10)
        .padding(.horizontal, 10)
        .background(row.sufficient ? Color.clear : AppPalette.danger.opacity(0.06))
    }
}


/// 设置中用于查看和恢复 AIMES 历史人工决定的入口。
struct AimesHistorySheet: View {
    @ObservedObject var model: AppModel
    @Environment(\.dismiss) private var dismiss
    @State private var showAimesHistory = true
    @State private var confirmationTitle = ""
    @State private var pendingAction: (() -> Void)?
    @State private var showActionConfirmation = false

    /// 弹出确认对话框，仅在用户确认后执行动作。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - action: 用户确认或点击按钮后执行的动作。
    private func confirm(_ title: String, action: @escaping () -> Void) {
        confirmationTitle = title
        pendingAction = action
        showActionConfirmation = true
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            HStack {
                Text("历史 AIMES 记录").font(.title2.weight(.semibold))
                Spacer()
                Button("关闭", systemImage: "xmark") { dismiss() }
                    .buttonStyle(.glass)
                    .keyboardShortcut(.cancelAction)
            }
            if model.hasAimesHistory {
                ScrollView { aimesHistorySection }
            } else {
                ContentUnavailableView("暂无历史 AIMES 记录", systemImage: "clock")
                    .frame(maxWidth: .infinity, maxHeight: .infinity)
            }
        }
        .padding(20)
        .frame(width: 760, height: 520)
        .background(LiquidGlassPreviewBackdrop())
        .alert(confirmationTitle, isPresented: $showActionConfirmation) {
            Button("取消", role: .cancel) { pendingAction = nil }
            Button("确认") {
                guard !model.orderRunning, !model.inventoryRunning else { return }
                pendingAction?()
                pendingAction = nil
            }
        } message: {
            Text("此操作会保存你的处理结果。请确认当前订单和处理范围无误。")
        }
    }

    @ViewBuilder
    private var aimesHistorySection: some View {
        if model.hasAimesHistory {
            VStack(alignment: .leading, spacing: 10) {
                Button {
                    showAimesHistory.toggle()
                } label: {
                    HStack(spacing: 8) {
                        Image(systemName: showAimesHistory ? "chevron.down" : "chevron.right")
                            .font(.caption.weight(.semibold))
                        Text("历史 AIMES 记录")
                            .font(.headline)
                        Text("已确认 \(model.assignedAimesFactories.count) · 已忽略 \(model.ignoredAimesFactories.count)")
                            .font(.caption)
                            .foregroundColor(.secondary)
                    }
                }
                .buttonStyle(.plain)

                if showAimesHistory {
                    AppSurfaceCard(padding: 0) {
                        VStack(spacing: 0) {
                            ForEach(model.assignedAimesFactories) { item in
                                aimesHistoryRow(item, title: "已确认归属") {
                                    model.restoreAimesFactoryAssignment(item)
                                } actionTitle: {
                                    "撤销归属"
                                }
                                if item.id != model.assignedAimesFactories.last?.id { Divider() }
                            }
                            if !model.assignedAimesFactories.isEmpty && !model.ignoredAimesFactories.isEmpty {
                                Divider()
                            }
                            ForEach(model.ignoredAimesFactories) { item in
                                aimesHistoryRow(item, title: "已忽略") {
                                    model.restoreAimesFactory(item)
                                } actionTitle: {
                                    "恢复"
                                }
                                if item.id != model.ignoredAimesFactories.last?.id { Divider() }
                            }
                        }
                    }
                }
            }
        }
    }

    /// 显示历史人工决定，并提供恢复操作按钮。
    /// - Parameters:
    ///   - item: AIMES 人工确认记录。
    ///   - title: 界面或操作记录的标题。
    ///   - action: 用户确认或点击按钮后执行的动作。
    ///   - actionTitle: 生成操作按钮标题的闭包。
    private func aimesHistoryRow(
        _ item: AimesReviewItem,
        title: String,
        action: @escaping () -> Void,
        actionTitle: @escaping () -> String
    ) -> some View {
        HStack(alignment: .top, spacing: 12) {
            VStack(alignment: .leading, spacing: 4) {
                Text("\(title) · \(item.factoryOrder.isEmpty ? "工厂单号为空" : item.factoryOrder)")
                    .font(.subheadline.weight(.semibold))
                Text("工厂单名称：\(item.factoryName.isEmpty ? "名称为空" : item.factoryName)")
                    .font(.caption)
                Text("销售单名称：\(item.salesOrderName.isEmpty ? "空" : item.salesOrderName)")
                    .font(.caption)
            }
            Spacer(minLength: 12)
            Button(actionTitle()) {
                confirm("确认\(actionTitle())：\(item.factoryOrder)？", action: action)
            }
                .appActionButton(minWidth: title == "已忽略" ? 72 : 92)
                .disabled(model.orderRunning)
        }
        .padding(12)
    }

}

// 在用户整体保存之前，草稿仅存在于此面板。
struct ManualHardwareFactory: Decodable, Identifiable {
    var id: String { factoryOrder }
    let factoryOrder: String
    let factoryName: String
    let editable: Bool
}

struct ManualHardwareRecord: Decodable, Identifiable {
    let id: Int
    let factoryOrder: String
    let productCode: String
    let name: String
    let spec: String
    let quantity: Double
    let unit: String
}

struct ManualHardwareSnapshot: Decodable {
    let factories: [ManualHardwareFactory]
    let items: [ManualHardwareRecord]
    let version: String

    /// 将 JSON 对象按蛇形字段名规则解码为人工五金快照。
    /// - Parameters:
    ///   - object: 后端返回的 JSON 结果对象。
    static func decode(_ object: [String: Any]) -> Self? {
        guard let data = try? JSONSerialization.data(withJSONObject: object) else { return nil }
        let decoder = JSONDecoder()
        decoder.keyDecodingStrategy = .convertFromSnakeCase
        return try? decoder.decode(Self.self, from: data)
    }
}

struct ManualHardwareProduct: Decodable, Identifiable {
    var id: String { code }
    let code: String
    let name: String
    let spec: String
    let unit: String
}

struct ManualHardwareDraft: Identifiable {
    let id = UUID()
    let factoryOrder: String
    let product: ManualHardwareProduct
    let quantity: Int
}

struct ManualHardwareSheet: View {
    @ObservedObject var model: AppModel
    let orderID: String
    private let barHeight: CGFloat = 50
    @Environment(\.dismiss) private var dismiss
    @State private var snapshot: ManualHardwareSnapshot?
    @State private var additions: [ManualHardwareDraft] = []
    @State private var deletions: Set<Int> = []
    @State private var factoryOrder = ""
    @State private var query = ""
    @State private var products: [ManualHardwareProduct] = []
    @State private var productCode = ""
    @State private var productPage = 0
    @State private var quantity = 1
    @State private var notice = ""
    @State private var searchNotice = ""
    @State private var showDiscard = false
    @State private var showReload = false
    @State private var needsReload = false
    /// 判断人工五金是否还有未保存的新增或删除草稿。
    private var dirty: Bool { !additions.isEmpty || !deletions.isEmpty }
    /// 判断订单或库存后台是否正在执行操作。
    private var busy: Bool { model.orderRunning || model.inventoryRunning }
    /// 从快照筛选仍允许编辑人工五金的工厂单。
    private var editableFactories: [ManualHardwareFactory] { snapshot?.factories.filter(\.editable) ?? [] }
    /// 按当前 SKU 取得商品搜索结果中的选中项。
    private var selectedProduct: ManualHardwareProduct? { products.first { $0.code == productCode } }

    var body: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                HStack(alignment: .firstTextBaseline, spacing: 12) {
                    Text("人工五金").font(.title2).fontWeight(.semibold)
                    Text("订单 \(orderID)").foregroundStyle(.secondary)
                }
                Spacer()
                if busy { ProgressView().controlSize(.small) }
                Button { close() } label: { Image(systemName: "xmark") }
                    .buttonStyle(.borderless).help("关闭").disabled(busy)
            }
            .padding(.horizontal, 20)
            .frame(height: barHeight)
            Divider()
            if let snapshot {
                if !editableFactories.isEmpty {
                    addForm
                        .fixedSize(horizontal: false, vertical: true)
                        .padding(.horizontal, 20)
                        .padding(.top, 14)
                }
                ScrollView {
                    VStack(alignment: .leading, spacing: 14) {
                        if snapshot.items.isEmpty && additions.isEmpty {
                            Text("本订单尚未添加人工五金").foregroundStyle(.secondary).padding(.vertical, 12)
                        }
                        ForEach(snapshot.factories.filter { factory in
                            snapshot.items.contains { $0.factoryOrder == factory.id } || additions.contains { $0.factoryOrder == factory.id }
                        }) { factory in
                            factoryGroup(factory, snapshot: snapshot)
                        }
                        // 即使工厂单已不存在，也保留历史事实的可见性。
                        let orphaned = snapshot.items.filter { item in !snapshot.factories.contains { $0.id == item.factoryOrder } }
                        if !orphaned.isEmpty {
                            Text("以下记录的工厂单已不存在，暂不能修改").foregroundStyle(.orange)
                            ForEach(orphaned) { item in
                                Text("\(item.factoryOrder) · \(item.productCode) · \(item.name) · \(item.quantity.formatted()) \(item.unit)")
                            }
                        }
                        if editableFactories.isEmpty {
                            Text("本订单没有可编辑的工厂单；已出库或失效工厂单的人工五金仅供查看。")
                                .foregroundStyle(.secondary)
                        }
                    }.padding(.horizontal, 20)
                }
                .frame(maxWidth: .infinity, maxHeight: .infinity)
                // 间距位于滚动区之外，让滚动条与列表可视区域等高。
                .padding(.top, 14)
                .padding(.bottom, 8)
            } else {
                if !busy {
                    HStack {
                        Text("未能载入人工五金。").foregroundStyle(.secondary)
                        Button("重试") { load() }.disabled(busy)
                    }.padding(20)
                }
                Spacer()
            }
            if !notice.isEmpty {
                HStack(alignment: .top) {
                    Text(notice).foregroundStyle(.red).textSelection(.enabled)
                    if needsReload && snapshot != nil {
                        Button("重新载入") {
                            if dirty { showReload = true } else { load() }
                        }.disabled(busy)
                    }
                }.padding(.horizontal, 20).padding(.bottom, 10)
            }
            Divider()
            HStack {
                Image(systemName: "info.circle").foregroundStyle(.secondary)
                Text(dirty ? "待保存：新增 \(additions.count) 条，删除 \(deletions.count) 条" : "新增和删除将在保存后生效。")
                    .font(.callout).foregroundStyle(.secondary)
                Spacer()
                Button("取消") { close() }.appActionButton(minWidth: 80).disabled(busy)
                Button("保存更改") { save() }
                    .buttonStyle(.glassProminent).appActionButton(minWidth: 112)
                    .disabled(!dirty || busy || snapshot == nil)
            }
            .padding(.horizontal, 20)
            .frame(height: barHeight)
        }
        .frame(width: 820, height: 620)
        .background(AppPalette.background)
        .interactiveDismissDisabled(dirty || busy)
        .onAppear { load() }
        .alert("放弃未保存的更改？", isPresented: $showDiscard) {
            Button("继续编辑", role: .cancel) {}
            Button("放弃更改", role: .destructive) { dismiss() }
        }
        .alert("重新载入会清除未保存的更改", isPresented: $showReload) {
            Button("继续编辑", role: .cancel) {}
            Button("重新载入", role: .destructive) { load() }
        }
    }

    /// 显示工厂单已有人工五金及本次新增、删除草稿。
    /// - Parameters:
    ///   - factory: 人工五金工厂单。
    ///   - snapshot: 包含版本与已有人工五金事实的快照。
    private func factoryGroup(_ factory: ManualHardwareFactory, snapshot: ManualHardwareSnapshot) -> some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack {
                Image(systemName: "chevron.down")
                Text(factory.factoryName.isEmpty ? factory.id : factory.factoryName).fontWeight(.semibold)
                Text("工厂单号：\(factory.id)").foregroundStyle(.secondary)
                Spacer()
                if !factory.editable { Text("仅查看").foregroundStyle(.secondary) }
            }.padding(14)
            Divider()
            HStack {
                Text("SKU").frame(width: 70, alignment: .leading)
                Text("五金名称").frame(maxWidth: .infinity, alignment: .leading)
                Text("规格").frame(width: 125, alignment: .leading)
                Text("数量 / 单位").frame(width: 90, alignment: .leading)
                Text(factory.editable ? "操作" : "").frame(width: 44, alignment: .trailing)
            }.font(.callout).foregroundStyle(.secondary).padding(.horizontal, 14).padding(.vertical, 10)
            ForEach(snapshot.items.filter { $0.factoryOrder == factory.id }) { item in
                Divider()
                hardwareRow(code: item.productCode, name: item.name, spec: item.spec,
                            amount: "\(item.quantity.formatted()) \(item.unit)",
                            pending: deletions.contains(item.id),
                            action: factory.editable ? (deletions.contains(item.id) ? "撤销" : "删除") : nil) {
                    if deletions.contains(item.id) { deletions.remove(item.id) } else { deletions.insert(item.id) }
                }.disabled(busy || !factory.editable)
            }
            ForEach(additions.filter { $0.factoryOrder == factory.id }) { item in
                Divider()
                hardwareRow(code: item.product.code, name: item.product.name + " · 待新增", spec: item.product.spec,
                            amount: "\(item.quantity) \(item.product.unit)", pending: false, action: "移除") {
                    additions.removeAll { $0.id == item.id }
                }.disabled(busy)
            }
        }
        .background(AppPalette.surface)
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .overlay(RoundedRectangle(cornerRadius: 12).stroke(AppPalette.separator))
    }

    /// 绘制人工五金规格、数量及删除或撤销入口。
    /// - Parameters:
    ///   - code: 商品或五金代码。
    ///   - name: 来源材料或五金的名称。
    ///   - spec: 五金商品规格文字。
    ///   - amount: 已格式化的数量与单位文字。
    ///   - pending: 此五金行是否待删除。
    ///   - action: 操作按钮文案；nil 时仅显示信息并保留列宽对齐。
    ///   - perform: 点击五金操作按钮时执行的动作。
    private func hardwareRow(code: String, name: String, spec: String, amount: String,
                             pending: Bool, action: String?, perform: @escaping () -> Void) -> some View {
        HStack {
            Text(code).frame(width: 70, alignment: .leading)
            Text(name).frame(maxWidth: .infinity, alignment: .leading)
            Text(spec).frame(width: 125, alignment: .leading)
            Text(amount).frame(width: 90, alignment: .leading)
            if let action {
                Button(action, action: perform).foregroundStyle(pending ? Color.accentColor : Color.red)
                    .buttonStyle(.borderless).frame(width: 44, alignment: .trailing)
            } else {
                Color.clear.frame(width: 44, height: 1).accessibilityHidden(true)
            }
        }
        .strikethrough(pending).opacity(pending ? 0.55 : 1).padding(14)
    }

    private var addForm: some View {
        VStack(alignment: .leading, spacing: 10) {
            Label("新增人工五金", systemImage: "plus").font(.headline)
            HStack {
                Text("工厂单 *").frame(width: 90, alignment: .leading)
                Picker("工厂单", selection: $factoryOrder) {
                    Text("请选择本订单的工厂单").tag("")
                    ForEach(editableFactories) { factory in
                        Text("\(factory.factoryName) / \(factory.id)").tag(factory.id)
                    }
                }.labelsHidden().pickerStyle(.menu)
                    .fixedSize(horizontal: true, vertical: false)
                    .frame(maxWidth: .infinity, alignment: .leading)
            }
            HStack {
                Text("搜索五金 *").frame(width: 90, alignment: .leading)
                TextField("输入 SKU 或五金名称", text: $query).textFieldStyle(.roundedBorder)
                    .onSubmit { search() }
                    .onKeyPress(.return) { search(); return .handled }
                    .onChange(of: query) { _, _ in products = []; productCode = ""; productPage = 0; searchNotice = "" }
                Button("搜索") { search() }.disabled(busy || query.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
            }
            if !searchNotice.isEmpty { Text(searchNotice).font(.caption).foregroundStyle(.secondary).padding(.leading, 98) }
            if !products.isEmpty {
                VStack(spacing: 0) {
                    HStack(spacing: 8) {
                        Color.clear.frame(width: 24, height: 1)
                        Text("SKU").frame(width: 70)
                        Text("五金名称").frame(maxWidth: .infinity)
                        Text("规格").frame(width: 188)
                        Text("单位").frame(width: 60)
                    }.font(.callout).foregroundStyle(.secondary).padding(10)
                    // 每页完整展示一项，长规格自然换行，上方表单不引入滚动区。
                    ForEach(Array(products.dropFirst(productPage).prefix(1))) { product in
                        Divider()
                        Button { productCode = product.code } label: {
                            HStack(spacing: 8) {
                                Image(systemName: productCode == product.code ? "largecircle.fill.circle" : "circle")
                                    .foregroundStyle(productCode == product.code ? Color.accentColor : Color.secondary)
                                    .frame(width: 24)
                                Text(product.code).frame(width: 70)
                                Text(product.name).frame(maxWidth: .infinity)
                                Text(product.spec).frame(width: 188)
                                Text(product.unit).frame(width: 60)
                            }
                            .multilineTextAlignment(.center)
                            .fixedSize(horizontal: false, vertical: true)
                            .padding(10).contentShape(Rectangle())
                        }.buttonStyle(.plain)
                    }
                    if products.count > 1 {
                        Divider()
                        HStack {
                            Button("上一项") { productPage -= 1 }.disabled(productPage == 0)
                            Text("\(productPage + 1) / \(products.count)").monospacedDigit().foregroundStyle(.secondary)
                            Button("下一项") { productPage += 1 }.disabled(productPage + 1 >= products.count)
                            Spacer()
                            if let selectedProduct {
                                Text("已选：\(selectedProduct.code)").foregroundStyle(.secondary)
                            }
                        }.font(.callout).padding(8)
                    }
                }
                .background(AppPalette.surface).clipShape(RoundedRectangle(cornerRadius: 8))
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
            }
            HStack {
                Text("数量 *").frame(width: 90, alignment: .leading)
                TextField("数量", value: $quantity, format: .number).textFieldStyle(.roundedBorder).frame(width: 80)
                Stepper("数量", value: $quantity, in: 1...Int.max).labelsHidden()
                Text(selectedProduct?.unit ?? "").foregroundStyle(.secondary)
                Spacer()
                Button("添加到列表") {
                    guard let product = selectedProduct, quantity > 0 else { return }
                    additions.append(ManualHardwareDraft(factoryOrder: factoryOrder, product: product, quantity: quantity))
                    productCode = ""; quantity = 1; notice = ""
                }.buttonStyle(.glassProminent).appActionButton(minWidth: 120)
                    .disabled(busy || selectedProduct == nil || quantity <= 0 || !editableFactories.contains { $0.id == factoryOrder })
            }
        }
        // 数量行包含 44 点按钮布局框，减小底部边距以平衡上下视觉留白。
        .padding(EdgeInsets(top: 16, leading: 16, bottom: 8, trailing: 16))
        .background(AppPalette.surface)
        .clipShape(RoundedRectangle(cornerRadius: 12))
        .overlay(RoundedRectangle(cornerRadius: 12).stroke(AppPalette.separator))
        .disabled(busy)
    }

    /// 读取人工五金快照，成功后清空草稿并选择唯一可编辑工厂单。
    /// 无参数。
    private func load() {
        guard !busy else { return }
        notice = ""
        model.loadManualHardware(orderID: orderID) { object in
            guard let object, let loaded = ManualHardwareSnapshot.decode(object) else {
                notice = model.orderError.isEmpty ? "人工五金返回内容无效" : model.orderError
                return
            }
            snapshot = loaded; additions = []; deletions = []; needsReload = false
            products = []; productCode = ""; productPage = 0; searchNotice = ""
            factoryOrder = loaded.factories.filter(\.editable).count == 1 ? (loaded.factories.first(where: \.editable)?.id ?? "") : ""
        }
    }

    /// 按当前 SKU 或名称搜索人工五金，丢弃过时查询的返回结果。
    /// 无参数。
    private func search() {
        guard !busy else { return }
        let requested = query.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !requested.isEmpty else { return }
        notice = ""; products = []; productCode = ""; productPage = 0
        model.searchManualHardware(requested) { object in
            guard requested == query.trimmingCharacters(in: .whitespacesAndNewlines) else { return }
            guard let object, let rows = object["products"],
                  let data = try? JSONSerialization.data(withJSONObject: rows),
                  let found = try? JSONDecoder().decode([ManualHardwareProduct].self, from: data) else {
                notice = model.orderError.isEmpty ? "商品搜索结果无效" : model.orderError
                return
            }
            products = found
            searchNotice = found.isEmpty ? "没有找到启用商品，请尝试其他 SKU 或名称" : "找到 \(found.count) 个商品，请选择规格和单位匹配的五金"
        }
    }

    /// 提交带版本号的人工五金增删草稿，成功后关闭，冲突时提示重新载入。
    /// 无参数。
    private func save() {
        guard let snapshot, dirty, !busy else { return }
        let payload: [String: Any] = [
            "version": snapshot.version,
            "deletions": deletions.sorted(),
            "additions": additions.map { ["factory_order": $0.factoryOrder, "product_code": $0.product.code, "quantity": $0.quantity] as [String: Any] }
        ]
        model.saveManualHardware(orderID: orderID, payload: payload) { success in
            if success { dismiss() } else {
                notice = model.orderError
                needsReload = true
            }
        }
    }

    /// 存在未保存五金草稿时请求放弃确认，否则直接关闭面板。
    /// 无参数。
    private func close() {
        if dirty { showDiscard = true } else { dismiss() }
    }
}

private struct ServerFolderIgnoreButton: View {
    @ObservedObject var model: AppModel
    let group: ServerFolderChangeGroup
    @State private var confirming = false

    var body: some View {
        Button { confirming = true } label: {
            Text("忽略此文件夹").frame(width: 112)
        }
            .buttonStyle(.glass)
            .controlSize(.regular)
            .disabled(model.orderRunning || model.inventoryRunning)
            .alert("忽略文件夹“\(group.folderName)”？", isPresented: $confirming) {
                Button("取消", role: .cancel) {}
                Button("确认忽略") { model.ignoreServerFolder(group.folderPath) }
            } message: {
                Text("忽略后不再扫描此文件夹，也不因报表或 XML 变化重新提醒。此操作不登记出库，也不表示已人工处理。")
            }
    }
}

/// 新版优化一次确认：工厂单用途、跨订单材料分配和五金版本在同一份预览中核对。
struct AicncConfirmationSheet: View {
    @ObservedObject var model: AppModel
    @Environment(\.dismiss) private var dismiss
    @State private var factories: [[String: Any]] = []
    @State private var amounts: [String: String] = [:]
    @State private var confirmWrite = false
    @State private var confirmIgnore = false

    private var materials: [[String: Any]] { model.aicncPreview["materials"] as? [[String: Any]] ?? [] }
    private var busy: Bool { model.orderRunning || model.inventoryRunning }
    private var resuming: Bool { model.aicncPreview["resuming"] as? Bool ?? false }
    private var groups: [String] {
        Array(Set(factories.compactMap { factory -> String? in
            let order = factory["order_id"] as? String ?? ""
            let purpose = factory["purpose"] as? String ?? ""
            return order.isEmpty || purpose.isEmpty ? nil : order + "|" + purpose
        })).sorted()
    }
    private func number(_ value: Any?) -> Double { (value as? NSNumber)?.doubleValue ?? 0 }
    private func format(_ value: Double) -> String { String(format: "%g", value) }
    private func key(_ group: String, _ code: String) -> String { group + "|" + code }
    private func label(_ group: String) -> String {
        let parts = group.components(separatedBy: "|")
        return parts[0] + (parts.last == "rework" ? " · 返工追加" : " · 正常优化")
    }
    private func field(_ index: Int, _ name: String) -> Binding<String> {
        Binding(get: { factories[index][name] as? String ?? "" }, set: { value in
            factories[index][name] = name == "order_id" ? value.uppercased().trimmingCharacters(in: .whitespaces) : value
            if name == "purpose" || name == "order_id" { amounts = [:]; fillSingleGroup() }
        })
    }
    private func fillSingleGroup() {
        if groups.count == 1, let group = groups.first {
            for material in materials {
                amounts[key(group, material["product_code"] as? String ?? "")] = format(number(material["quantity"]))
            }
        }
    }
    private var valid: Bool {
        guard !factories.isEmpty, factories.allSatisfy({
            !(($0["order_id"] as? String ?? "").isEmpty) && ["normal", "rework"].contains($0["purpose"] as? String ?? "") &&
            ["same", "absent", "shipped", "keep", "replace"].contains($0["hardware_choice"] as? String ?? "")
        }) else { return false }
        return materials.allSatisfy { material in
            let code = material["product_code"] as? String ?? ""
            var sum = 0.0
            for group in groups {
                guard let value = Double(amounts[key(group, code)] ?? "0"), value.isFinite, value >= 0, value.rounded() == value else { return false }
                sum += value
            }
            return abs(sum - number(material["quantity"])) < 0.000001
        }
    }
    private var payload: [String: Any] {
        var data = model.aicncPreview
        data["factories"] = factories
        data["allocations"] = groups.flatMap { group -> [[String: Any]] in
            let parts = group.components(separatedBy: "|")
            return materials.map { material in
                let code = material["product_code"] as? String ?? ""
                return ["order_id": parts[0], "purpose": parts[1], "product_code": code,
                        "quantity": Double(amounts[key(group, code)] ?? "0") ?? 0]
            }
        }
        return data
    }

    var body: some View {
        VStack(alignment: .leading, spacing: 16) {
            Text("确认本次优化").font(.title2.bold())
            Text(model.aicncPreview["optimization_id"] as? String ?? "").font(.headline)
            Text(resuming ? "此优化已有确认记录。继续处理将先核对已提交的出库单，使用原确认方案。" : "请确认每个工厂单的用途。混单或同时包含正常生产与返工时，分别分配板材和封边。")
                .foregroundColor(.secondary).fixedSize(horizontal: false, vertical: true)
            ScrollView {
                VStack(alignment: .leading, spacing: 20) {
                    ForEach(factories.indices, id: \.self) { index in factoryRow(index) }
                    Divider()
                    Text("板材与封边分配").font(.headline)
                    Text("正常优化：追加订单材料。返工追加：补开出库单，并同步增加材料总量与已消耗量，保留原订单和工厂单状态。")
                        .font(.callout).foregroundColor(.secondary)
                    ForEach(materials.indices, id: \.self) { index in materialRow(materials[index]) }
                }.padding(.trailing, 8)
            }
            if !model.aicncNotice.isEmpty { Text(model.aicncNotice).font(.callout).textSelection(.enabled) }
            HStack {
                Button("忽略此优化") { confirmIgnore = true }.disabled(busy || resuming)
                Spacer()
                if busy { ProgressView().controlSize(.small) }
                Button("稍后处理") { dismiss() }.disabled(busy)
                Button(resuming ? "继续核对并处理" : "确认并处理") { confirmWrite = true }
                    .buttonStyle(.borderedProminent).disabled(busy || !valid)
            }
        }
        .padding(24)
        .onAppear {
            factories = model.aicncPreview["factories"] as? [[String: Any]] ?? []
            for row in model.aicncPreview["allocations"] as? [[String: Any]] ?? [] {
                let group = (row["order_id"] as? String ?? "") + "|" + (row["purpose"] as? String ?? "")
                amounts[key(group, row["product_code"] as? String ?? "")] = format(number(row["quantity"]))
            }
            if amounts.isEmpty { fillSingleGroup() }
        }
        .alert("确认处理本次优化？", isPresented: $confirmWrite) {
            Button("取消", role: .cancel) {}
            Button("确认处理") { model.confirmAicnc(payload) }
        } message: {
            Text(groups.contains(where: { $0.hasSuffix("|rework") }) ? "将按上方分配追加材料，并为返工部分在库存系统补开出库单、登记等量消耗。处理后不再读取此优化文件夹的变化。" : "将追加本次分配的材料，按选择保留或替换五金，并同步正常优化工厂单的状态。处理后不再读取此优化文件夹的变化。")
        }
        .alert("忽略本次优化？", isPresented: $confirmIgnore) {
            Button("取消", role: .cancel) {}
            Button("确认忽略") { model.ignoreAicnc() }
        } message: { Text("不追加任何材料，也不再检查此优化文件夹。该订单下的其他优化仍会正常发现。") }
    }

    private func factoryRow(_ index: Int) -> some View {
        let factory = factories[index]
        let choice = factory["hardware_choice"] as? String ?? ""
        return VStack(alignment: .leading, spacing: 8) {
            Text("\(factory["factory_order"] as? String ?? "")  ·  \(factory["factory_name"] as? String ?? "")").font(.headline)
            HStack {
                TextField("订单号", text: field(index, "order_id")).frame(width: 140)
                    .disabled(resuming || !(factory["known_order_id"] as? String ?? "").isEmpty)
                Text("当前：\(factory["stage"] as? String ?? "待确认")").foregroundColor(.secondary)
                Spacer()
                Picker("本次用途", selection: field(index, "purpose")) {
                    Text("请选择").tag("")
                    Text("正常优化").tag("normal")
                    Text("返工追加（已生产）").tag("rework")
                }.frame(width: 290).disabled(busy || resuming)
            }
            if ["same", "absent", "shipped"].contains(choice) {
                Text(choice == "shipped" ? "工厂单已出货，不读取五金。" : choice == "same" ? "五金与已有内容一致。" : "此次无该工厂单五金，沿用已有记录。")
                    .font(.caption).foregroundColor(.secondary)
            } else {
                Picker("五金处理", selection: field(index, "hardware_choice")) {
                    Text("请选择").tag("")
                    Text("保留原五金").tag("keep")
                    if factory["hardware_error"] == nil { Text("使用新五金替换").tag("replace") }
                }.disabled(busy || resuming)
                if let error = factory["hardware_error"] as? String {
                    Text(error).font(.caption).foregroundColor(.orange)
                    Button("处理五金商品映射") {
                        model.showAicncConfirmation = false
                        model.requestInventoryMapping(folderPath: model.aicncPreview["source_folder"] as? String ?? "", message: error)
                    }.disabled(busy || resuming)
                }
                DisclosureGroup("查看已有与本次五金") {
                    hardwareRows("已有", factory["existing_hardware"] as? [[String: Any]] ?? [])
                    hardwareRows("本次", factory["hardware"] as? [[String: Any]] ?? [])
                }.font(.caption)
            }
        }.padding(12).background(AppPalette.subtleSurface).cornerRadius(8)
    }

    private func hardwareRows(_ title: String, _ rows: [[String: Any]]) -> some View {
        VStack(alignment: .leading, spacing: 4) {
            Text(title).bold()
            if rows.isEmpty { Text("无") }
            ForEach(rows.indices, id: \.self) { index in
                Text("\(rows[index]["product_code"] as? String ?? "")  \(rows[index]["name"] as? String ?? "") × \(format(number(rows[index]["quantity"])))")
            }
        }.frame(maxWidth: .infinity, alignment: .leading)
    }

    private func materialRow(_ material: [String: Any]) -> some View {
        let code = material["product_code"] as? String ?? ""
        let total = number(material["quantity"])
        let assigned = groups.reduce(0.0) { $0 + (Double(amounts[key($1, code)] ?? "0") ?? 0) }
        return VStack(alignment: .leading, spacing: 8) {
            Text("\(material["raw_name"] as? String ?? code) · \(code) · \(format(total)) \(material["unit"] as? String ?? "")").font(.headline)
            if material["material_type"] as? String == "edge" {
                Text("报表合计 \(format(number(material["raw_quantity"]))) 米；沿用整米登记规则。").font(.caption).foregroundColor(.secondary)
            }
            ForEach(groups, id: \.self) { group in
                HStack {
                    Text(label(group)).frame(width: 260, alignment: .leading)
                    TextField("0", text: Binding(get: { amounts[key(group, code)] ?? "" }, set: { amounts[key(group, code)] = $0 }))
                        .textFieldStyle(.roundedBorder).frame(width: 100).disabled(busy || resuming)
                }
            }
            Text("已分配 \(format(assigned)) / \(format(total))")
                .font(.caption).foregroundColor(abs(assigned - total) < 0.000001 ? .secondary : .orange)
        }.padding(.vertical, 6)
    }
}
