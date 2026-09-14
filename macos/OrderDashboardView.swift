// Order-center views and layout helpers.  The dashboard renders persisted
// order facts and starts operations through AppModel; it should not infer
// production, shipment, or installation facts from display-only state.
import SwiftUI
import AppKit
import UniformTypeIdentifiers

let orderDashboardStatuses = [
    "已设计",
    "已拆单待优化",
    "部分优化",
    "已优化",
    "部分出货",
    "已出货",
    "待人工处理",
    "待确认",
    "数据异常",
]

let orderDashboardMetricColumnCount = 8
let orderDashboardMetricMinimumWidth: CGFloat = 110
let orderDashboardMetricSpacing: CGFloat = 10
// Give the factory identity/status columns practical minimum widths. The
// order-level Panel colors are shown above the table, so the table no longer
// needs a separate color column.
let orderDashboardFactoryColumnWidths: [CGFloat] = [150, 220, 110, 110, 120, 170]
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

    var dataWidth: CGFloat {
        totalWidth - orderDashboardOperationColumnWidth
    }

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

    var dataColumns: [GridItem] {
        Array(columns.dropLast())
    }
}

let dashboardMessageVisibleRowCount = 3
let dashboardMessageRowHeight: CGFloat = 74
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

    init(selection: Binding<Date>, compact: Bool = false) {
        _selection = selection
        _displayedMonth = State(initialValue: selection.wrappedValue)
        self.compact = compact
    }

    private var daySize: CGFloat { compact ? 30 : 34 }
    private var gridSpacing: CGFloat { compact ? 4 : 6 }
    private var columns: [GridItem] {
        Array(repeating: GridItem(.fixed(daySize), spacing: gridSpacing), count: 7)
    }

    private var calendar: Calendar {
        var value = Calendar(identifier: .gregorian)
        value.locale = Locale(identifier: "zh_CN")
        value.timeZone = .current
        value.firstWeekday = 1
        return value
    }

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

private func appGlassDatePickerDisplayDate(_ date: Date) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: "zh_CN")
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.dateFormat = "yyyy年M月d日"
    return formatter.string(from: date)
}

private func appGlassDatePickerMonthTitle(_ date: Date) -> String {
    let formatter = DateFormatter()
    formatter.locale = Locale(identifier: "zh_CN")
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.dateFormat = "yyyy年M月"
    return formatter.string(from: date)
}

extension View {
    func appGlassDatePickerPopoverSurface() -> some View {
        padding(10)
            .presentationBackground(.clear)
    }
}

func currentIssueRequiresInventoryMapping(_ issue: CurrentIssue) -> Bool {
    if issue.kind == "material_mapping" || issue.kind == "hardware_mapping" {
        return true
    }
    if issue.kind == "temporary_processing" && issue.message.contains("未映射材料") {
        return true
    }
    // Material SKU failures are currently persisted as material_validation
    // together with ordinary workbook/read failures. Only the explicit SKU
    // wording should open the mapping workspace; malformed files must keep
    // the normal "mark handled" action.
    return issue.kind == "material_validation"
        && issue.message.contains("未完成商品 SKU 处理")
}

private func serverWriteMaterialTypeRank(_ materialType: String) -> Int {
    switch materialType.trimmingCharacters(in: .whitespacesAndNewlines).lowercased() {
    case "plywood": return 0
    case "panel", "back": return 1
    case "edge": return 2
    default: return 3
    }
}

private func serverWritePlywoodThicknessRank(_ thickness: String) -> Int {
    let value = Double(thickness) ?? .greatestFiniteMagnitude
    if abs(value - 18) < 0.01 { return 0 }
    if abs(value - 14.5) < 0.01 { return 1 }
    if abs(value - 5.4) < 0.01 { return 2 }
    return 3
}

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

func dashboardMessageHoverCanPresent(appIsActive: Bool, mainWindowIsFrontmost: Bool) -> Bool {
    appIsActive && mainWindowIsFrontmost
}

let orderDashboardMetricColumns = Array(
    repeating: GridItem(.flexible(minimum: orderDashboardMetricMinimumWidth), spacing: orderDashboardMetricSpacing),
    count: orderDashboardMetricColumnCount
)

let orderDetailGridColumnCount = 4
let orderDetailCardMinHeight: CGFloat = 50

func orderDashboardMetricsFit(width: CGFloat, horizontalPadding: CGFloat) -> Bool {
    let cards = CGFloat(orderDashboardMetricColumnCount) * orderDashboardMetricMinimumWidth
    let gaps = CGFloat(orderDashboardMetricColumnCount - 1) * orderDashboardMetricSpacing
    return width - horizontalPadding * 2 >= cards + gaps
}

func orderDashboardPanelColors(_ materials: [OrderMaterialPreview]) -> [String] {
    var result: [String] = []
    for material in materials where material.kind == "panel" {
        let color = material.color.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !color.isEmpty, !result.contains(where: { $0.caseInsensitiveCompare(color) == .orderedSame }) else { continue }
        result.append(color)
    }
    return result
}

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

    override func mouseEntered(with event: NSEvent) {
        onMouseEntered?()
        super.mouseEntered(with: event)
    }

    override func mouseExited(with event: NSEvent) {
        onMouseExited?()
        super.mouseExited(with: event)
    }
}

private struct PanelMaterialHoverTracking: NSViewRepresentable {
    let onMouseEntered: () -> Void
    let onMouseExited: () -> Void

    func makeNSView(context: Context) -> PanelMaterialHoverTrackingView {
        let view = PanelMaterialHoverTrackingView(frame: .zero)
        view.onMouseEntered = onMouseEntered
        view.onMouseExited = onMouseExited
        return view
    }

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

    init(material: OrderMaterialPreview, @ViewBuilder content: () -> Content) {
        self.material = material
        self.content = content()
    }

    private var imageURL: URL? {
        panelMaterialImageURL(productCode: material.productCode)
    }

    private var previewImage: NSImage? {
        imageURL.flatMap { NSImage(contentsOf: $0) }
    }

    private var previewImageWidth: CGFloat {
        guard let image = previewImage, image.size.height > 0 else {
            return previewImageHeight
        }
        return previewImageHeight * image.size.width / image.size.height
    }

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

func orderDetailPlywoodRows(_ rows: [OrderMaterialPreview]) -> [OrderMaterialPreview] {
    orderedMaterialRows(rows.filter { $0.kind == "plywood" })
}

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

func orderDetailPanelThicknessRank(_ thickness: Double) -> Int {
    if abs(thickness - 19.1) < 0.01 { return 0 }
    if abs(thickness - 8) < 0.01 || abs(thickness - 9) < 0.01 { return 1 }
    return 2
}

func orderDetailEdgeColors(_ colors: [String]) -> [String] {
    colors.sorted {
        let left = $0.trimmingCharacters(in: .whitespacesAndNewlines)
        let right = $1.trimmingCharacters(in: .whitespacesAndNewlines)
        return left.localizedStandardCompare(right) == .orderedAscending
    }
}

func orderDashboardShortageCount(_ rows: [OrderStockPreview]) -> Int {
    rows.filter { !$0.sufficient }.count
}

func orderDashboardStatus(previewValidated: Bool, hasError: Bool, isExistingTraveler: Bool) -> String {
    if hasError { return "数据异常" }
    if previewValidated { return "已优化" }
    return "待校验"
}

func orderDashboardExpandedID(current: String?, tapped: String, forceOpen: Bool = false) -> String? {
    if !forceOpen, current == tapped { return nil }
    return tapped
}

struct OrderDashboardClickContainer<Content: View>: NSViewRepresentable {
    let content: Content
    let onSingleClick: () -> Void
    let onDoubleClick: () -> Void

    init(
        onSingleClick: @escaping () -> Void,
        onDoubleClick: @escaping () -> Void,
        @ViewBuilder content: () -> Content
    ) {
        self.content = content()
        self.onSingleClick = onSingleClick
        self.onDoubleClick = onDoubleClick
    }

    func makeCoordinator() -> Coordinator {
        Coordinator(onSingleClick: onSingleClick, onDoubleClick: onDoubleClick)
    }

    func makeNSView(context: Context) -> NSView {
        let container = NSView()
        let hosting = NSHostingView(rootView: content)
        hosting.translatesAutoresizingMaskIntoConstraints = false
        container.addSubview(hosting)
        NSLayoutConstraint.activate([
            hosting.leadingAnchor.constraint(equalTo: container.leadingAnchor),
            hosting.trailingAnchor.constraint(equalTo: container.trailingAnchor),
            hosting.topAnchor.constraint(equalTo: container.topAnchor),
            hosting.bottomAnchor.constraint(equalTo: container.bottomAnchor),
        ])

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

    func updateNSView(_ nsView: NSView, context: Context) {
        context.coordinator.onSingleClick = onSingleClick
        context.coordinator.onDoubleClick = onDoubleClick
        if let hosting = nsView.subviews.compactMap({ $0 as? NSHostingView<Content> }).first {
            hosting.rootView = content
        }
    }

    final class Coordinator: NSObject, NSGestureRecognizerDelegate {
        var onSingleClick: () -> Void
        var onDoubleClick: () -> Void

        init(onSingleClick: @escaping () -> Void, onDoubleClick: @escaping () -> Void) {
            self.onSingleClick = onSingleClick
            self.onDoubleClick = onDoubleClick
        }

        func gestureRecognizer(_ gestureRecognizer: NSGestureRecognizer, shouldRequireFailureOf otherGestureRecognizer: NSGestureRecognizer) -> Bool {
            gestureRecognizer is NSClickGestureRecognizer
                && (gestureRecognizer as? NSClickGestureRecognizer)?.numberOfClicksRequired == 1
                && otherGestureRecognizer is NSClickGestureRecognizer
                && (otherGestureRecognizer as? NSClickGestureRecognizer)?.numberOfClicksRequired == 2
        }

        @objc func singleClick() { onSingleClick() }
        @objc func doubleClick() { onDoubleClick() }
    }
}

func toggledOrderFactorySelection(_ selected: Set<String>, factoryOrder: String) -> Set<String> {
    var next = selected
    if next.contains(factoryOrder) {
        next.remove(factoryOrder)
    } else {
        next.insert(factoryOrder)
    }
    return next
}

func selectedOrderFactoryNames(_ factories: [OrderFactoryPreview], selected: Set<String>) -> [String] {
    factories
        .filter { selected.contains($0.factoryOrder) }
        .map(\.orderName)
        .filter { !$0.isEmpty }
}

func orderDashboardHasShippedSelection(
    _ selected: Set<String>,
    statuses: [String: String]
) -> Bool {
    selected.contains { statuses[$0] == "已出库" }
}

func orderDashboardNeedsOutboundUpdateSelection(
    _ selected: Set<String>,
    statuses: [String: String]
) -> Bool {
    selected.contains { statuses[$0] == "需要更新" }
}

func orderDashboardHasProducedSelection(
    _ selected: Set<String>,
    produced: [String: Bool]
) -> Bool {
    selected.contains { produced[$0] == true }
}

func orderDashboardOutboundActionTitle(
    _ selected: Set<String>,
    statuses: [String: String]
) -> String {
    "出货"
}

func orderDashboardOutboundDisplay(status: String, documentNumber: String) -> String {
    let trimmedStatus = status.trimmingCharacters(in: .whitespacesAndNewlines)
    let trimmedDocument = documentNumber.trimmingCharacters(in: .whitespacesAndNewlines)
    guard trimmedStatus == "已出库", !trimmedDocument.isEmpty else { return trimmedStatus }
    return "\(trimmedStatus) · \(trimmedDocument)"
}

func orderDashboardStageMatchesFilter(_ stage: String, statusFilter: String) -> Bool {
    if statusFilter == "全部订单" {
        return true
    }
    if statusFilter == "未完成订单" || statusFilter == "全部状态" {
        return !orderDashboardIsCompleted(stage)
    }
    return stage == statusFilter
}

func orderDashboardIsCompleted(_ stage: String) -> Bool {
    stage == "已出货"
}

func orderDashboardStatusHelp(status: String, validationMessage: String) -> String {
    guard status == "数据异常" else { return "" }
    let message = validationMessage.trimmingCharacters(in: .whitespacesAndNewlines)
    return message.isEmpty
        ? "订单数据未能通过校验。请检查订单报表后重新扫描 Server。"
        : message
}

func orderDashboardProgressFraction(completed: Int, total: Int) -> Double {
    guard total > 0 else { return 0 }
    return min(max(Double(completed) / Double(total), 0), 1)
}

func orderInstallationDisplayDate(_ value: String) -> String {
    let parts = value.split(separator: "-")
    guard parts.count == 3,
          let month = Int(parts[1]),
          let day = Int(parts[2]) else {
        return value
    }
    return "\(parts[0])年\(month)月\(day)日"
}

func orderInstallationDateSummary(_ days: [OrderInstallationDay]) -> String {
    guard let date = days.map(\.date).sorted().first else { return "" }
    return orderInstallationDisplayDate(date)
}

func orderInstallationPlannedDateSummary(_ days: [OrderInstallationDay]) -> String {
    guard let date = days.map(\.date).sorted().first else { return "" }
    return orderInstallationDisplayDate(date)
}

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

    init(completed: Int, total: Int, accessibilityTitle: String = "优化进度") {
        self.completed = completed
        self.total = total
        self.accessibilityTitle = accessibilityTitle
    }

    private var fraction: Double {
        orderDashboardProgressFraction(completed: completed, total: total)
    }

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

func shouldPresentPendingCenterAfterAimes(
    presentIfNeeded: Bool,
    pendingAimesReviews: [AimesReviewItem],
    aimesFormatWarnings: [AimesReviewItem] = []
) -> Bool {
    presentIfNeeded && (!pendingAimesReviews.isEmpty || !aimesFormatWarnings.isEmpty)
}

struct DashboardMessage: Identifiable {
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

func dashboardMessageState(_ text: String) -> String {
    if text.hasPrefix("❌") { return "failure" }
    if text.hasPrefix("⚠️") { return "warning" }
    if text.hasPrefix("✅") { return "success" }
    return "info"
}

func dashboardMessageDetail(_ text: String) -> String {
    for marker in ["✅", "⚠️", "❌"] where text.hasPrefix(marker) {
        return String(text.dropFirst(marker.count)).trimmingCharacters(in: .whitespacesAndNewlines)
    }
    return text
}

func dashboardStatusIsInProgress(_ text: String) -> Bool {
    if ["✅", "⚠️", "❌"].contains(where: { text.hasPrefix($0) }) { return false }
    let detail = dashboardMessageDetail(text)
    return detail.contains("正在") || detail.contains("处理中")
}

func dashboardMessageIsRunning(_ message: DashboardMessage) -> Bool {
    if message.state == "running" { return true }
    // Keep compatibility with older callers that did not set the explicit
    // running state. Terminal markers always win over text matching.
    guard message.state == "info" else { return false }
    return dashboardStatusIsInProgress(message.detail)
}

private let dashboardStatusPlaceholders: Set<String> = [
    "订单数据尚未同步",
    "库存操作尚未执行",
    "AIMES 尚未检查",
    "Server 尚未扫描",
]

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
    // When the AIMES status is also copied into syncStatus, prefer the AIMES
    // message so its authoritative duration, stages, and warning details are
    // not discarded by the duplicate-detail filter below.
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

func dashboardVisibleMessages(_ messages: [DashboardMessage], isRunning: Bool) -> [DashboardMessage] {
    guard isRunning else { return messages }
    return messages.filter { !dashboardMessageIsRunning($0) }
}

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

func dashboardMessageScrollKey(_ messages: [DashboardMessage]) -> String {
    messages.map {
        let stageKey = $0.operationDurations
            .map { "\($0.label):\($0.duration)" }
            .joined(separator: ";")
        return "\($0.id)|\($0.time)|\($0.detail)|\($0.operationDetails.joined(separator: "|"))|\($0.contextDetails.joined(separator: "|"))|\($0.duration ?? -1)|\(stageKey)"
    }.joined(separator: "\n")
}

func dashboardMessageSupportsHoverDetail(_ message: DashboardMessage) -> Bool {
    !dashboardMessageIsRunning(message)
        && (message.state == "warning" || message.state == "failure"
            || !message.manualPaths.isEmpty
            || !message.operationDetails.isEmpty
            || !message.contextDetails.isEmpty
            || !message.operationDurations.isEmpty)
}

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

func dashboardMessageSummaryText(_ message: DashboardMessage, showsDuration: Bool = true) -> String {
    var summary = message.detail
    if showsDuration, let duration = message.duration {
        summary += "（总计用时 \(operationDurationText(duration))）"
    }
    return summary
}

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

    override func mouseEntered(with event: NSEvent) {
        onMouseEntered?()
        super.mouseEntered(with: event)
    }

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

    func makeCoordinator() -> Coordinator {
        Coordinator()
    }

    func makeNSView(context: Context) -> NSView {
        let view = NSView(frame: .zero)
        view.wantsLayer = true
        return view
    }

    func updateNSView(_ nsView: NSView, context: Context) {
        context.coordinator.update(
            anchorView: nsView,
            message: message,
            isPresented: isPresented,
            onPanelEntered: onPanelEntered,
            onPanelExited: onPanelExited
        )
    }

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

        private func updatePosition() {
            guard let panel, let anchorView, anchorView.window != nil else { return }
            // Keep the message row as the hover lifetime anchor. Placement is
            // intentionally pointer-based below for the established UI
            // behavior; the close grace and panel tracking prevent small
            // pointer movements from closing the detail immediately.
            let screenPoint = NSEvent.mouseLocation
            let visibleFrame = NSScreen.screens.first(where: { $0.frame.contains(screenPoint) })?.visibleFrame
                ?? NSScreen.main?.visibleFrame
                ?? NSRect(x: 0, y: 0, width: 1440, height: 900)
            let gap: CGFloat = 14
            // Keep the previous placement behavior: position relative to the
            // current pointer and flip left/right when the screen edge clips
            // the panel. The row remains the hover lifetime anchor.
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

        func close() {
            panel?.orderOut(nil)
            panel = nil
            hostingController = nil
        }

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
            // Keep the hover tracking area at the full row width instead of
            // the content's intrinsic width.
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

    private func beginHover() {
        guard !anchorHovering else { return }
        let wasPopoverVisible = showPopover
        activeMessageID = message.id
        anchorHovering = true
        hoverGeneration += 1
        if wasPopoverVisible {
            // Re-entering the row during the close grace period keeps the
            // already-visible panel instead of hiding and re-presenting it.
            return
        }
        showPopover = false
        let generation = hoverGeneration
        DispatchQueue.main.asyncAfter(deadline: .now() + dashboardMessageHoverDelay) {
            guard generation == hoverGeneration, anchorHovering else { return }
            showPopover = true
        }
    }

    private func endHover() {
        guard activeMessageID == message.id else { return }
        anchorHovering = false
        hoverGeneration += 1
        schedulePopoverClose()
    }

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

    private func panelEntered() {
        guard activeMessageID == nil || activeMessageID == message.id else { return }
        activeMessageID = message.id
        panelHovering = true
        hoverGeneration += 1
    }

    private func panelExited() {
        guard activeMessageID == message.id else { return }
        panelHovering = false
        hoverGeneration += 1
        schedulePopoverClose()
    }
}

struct OrderDashboardView: View {
    @ObservedObject var model: AppModel
    @State private var expandedOrderID: String?
    @State private var detailOrder: OrderDashboardItem?
    @State private var orderArrangementOrder: OrderDashboardItem?
    @State private var selectedFactoryID: String?
    @State private var selectedFactoryIDs: Set<String> = []
    @State private var searchText = ""
    @State private var statusFilter = "未完成订单"
    @State private var showFactoryStock = false
    @State private var showProductionSheet = false
    @State private var pendingShipment: OrderShipmentRequest?
    @State private var showOutboundScope = false
    @State private var showServerFolderImporter = false
    @State private var activeMessageID: String?

    private var filteredOrders: [OrderDashboardItem] {
        let query = searchText.trimmingCharacters(in: .whitespacesAndNewlines).lowercased()
        return model.dashboardOrders.filter { item in
            let factoryText = item.factories.map { "\($0.factoryOrder) \($0.orderName)" }.joined(separator: " ")
            let matchesQuery = query.isEmpty || item.orderId.lowercased().contains(query) || item.sourceFolder.lowercased().contains(query) || factoryText.lowercased().contains(query)
            let matchesStatus = orderDashboardStageMatchesFilter(item.stage, statusFilter: statusFilter)
            return matchesQuery && matchesStatus
        }
    }

    private var selectedFactory: OrderFactoryPreview? {
        model.orderFactories.first { $0.factoryOrder == selectedFactoryID }
    }

    private var availableHardwareFactoryOrders: Set<String> {
        Set(
            model.orderFittings
                .filter { $0.quantity > 0 }
                .map { $0.factoryOrder }
        )
    }

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
        dashboardSections
            .padding(AppLayout.contentPadding)
        .appPageFrame()
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

    private var dashboardSections: some View {
        VStack(alignment: .leading, spacing: AppLayout.sectionSpacing) {
            toolbar
            dashboardActivityLog
            orderTable
        }
        .frame(maxHeight: .infinity, alignment: .top)
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

    private var dashboardActivityLog: some View {
        let serverGroups = serverFolderChangeGroups(model.pendingServerChanges)
        let aimesManualPaths = (
            model.pendingAimesReviews + model.ignoredAimesFactories + model.assignedAimesFactories
        ).map(\.sourcePath)
        let serverManualPaths = model.pendingServerChanges.map(\.path)
        // The sync status row represents the latest warning/error. Attach only
        // that activity's file path; do not aggregate paths from unrelated
        // Server/AIMES operations into the hovered message.
        let latestActivityPaths = model.dashboardActivity.first {
            $0.state == "failure" || $0.state == "warning"
        }?.paths ?? []
        let aimesActionDetails: [String] = dashboardStatusIsInProgress(model.dashboardAimesStatus)
            ? []
            : dashboardAimesActionDetails(
                pending: model.pendingAimesReviews,
                ignored: model.ignoredAimesFactories,
                assigned: model.assignedAimesFactories
            ) + dashboardAimesWarningDetails(model.aimesWarnings)
        let serverActionDetails: [String] = {
            if dashboardStatusIsInProgress(model.dashboardServerStatus) {
                return []
            }
            if model.pendingServerChanges.isEmpty {
                return ["Server 已完成扫描，当前没有新增、修改或删除的订单文件。"]
            }
            return ["待处理 Server 变化 \(serverGroups.count) 个文件夹："] + serverGroups.map {
                let handling = $0.manualOnly ? "（临时文件夹）" : ""
                let names = $0.changes.map { URL(fileURLWithPath: $0.path).lastPathComponent }.joined(separator: "、")
                return "\($0.folderName)\(handling)：\(names)"
            }
        }()
        let messages = dashboardMessages(
            syncStatus: model.dashboardSyncStatus,
            syncTime: model.dashboardSyncStatusTime,
            inventoryStatus: model.dashboardInventoryOperationStatus,
            inventoryTime: model.dashboardInventoryOperationStatusTime,
            aimesStatus: model.dashboardAimesStatus,
            aimesTime: model.dashboardAimesStatusTime,
            serverStatus: model.dashboardServerStatus,
            serverTime: model.dashboardServerStatusTime,
            activity: model.dashboardActivity,
            operationDetailsBySource: model.dashboardMessageOperationDetails,
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
            durationsBySource: model.dashboardOperationDurations,
            operationDurationsBySource: model.dashboardOperationStageDurations,
            sessionMessages: model.dashboardSessionMessages
        )
        let operationRunning = model.orderRunning
            || model.inventoryRunning
            || dashboardStatusIsInProgress(model.dashboardSyncStatus)
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
                    }
                    .frame(height: dashboardMessageViewportHeight)
                    .onAppear { scrollMessagesToBottom(proxy, messages: messages) }
                    .onChange(of: scrollKey) { _, _ in
                        scrollMessagesToBottom(proxy, messages: messages)
                    }
                }
            }
        }
    }

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
                        if let elapsed = model.dashboardElapsedTime(display.message.source) {
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
            .frame(height: 44)
            .glassEffect(.clear, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        } else {
            HStack(spacing: 10) {
                Image(systemName: "pause.circle.fill").foregroundColor(.secondary)
                Text("当前无正在进行的操作").font(.callout).foregroundColor(.secondary)
                Spacer()
            }
            .padding(.horizontal, 12)
            .frame(height: 44)
            .glassEffect(.clear, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
        }
    }

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

    private func scrollMessagesToBottom(_ proxy: ScrollViewProxy, messages: [DashboardMessage]) {
        guard let lastID = messages.last?.id else { return }
        DispatchQueue.main.async {
            proxy.scrollTo(lastID, anchor: .bottom)
        }
    }

    private func activityIcon(_ state: String) -> String {
        switch state {
        case "failure": return "xmark.circle.fill"
        case "warning": return "exclamationmark.triangle.fill"
        case "success": return "checkmark.circle.fill"
        default: return "info.circle.fill"
        }
    }

    private func activityColor(_ state: String) -> Color {
        switch state {
        case "failure": return AppPalette.danger
        case "warning": return AppPalette.warning
        case "success": return AppPalette.success
        default: return AppPalette.accent
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
        // Do not let the table's flexible height proposal stretch the header.
        .fixedSize(horizontal: true, vertical: true)
    }

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
                            if !item.validationStatus.isEmpty { Text(item.validationStatus).font(.caption2).foregroundColor(.secondary) }
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

                // Keep action buttons outside the row-level gesture recognizers.
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
                        model.loadProductionPreview(orderID: item.orderId, factoryOrders: selectedFactoryIDs.sorted())
                        showProductionSheet = true
                    },
                    onOpenOutbound: {
                        pendingShipment = OrderShipmentRequest(
                            orderID: item.orderId,
                            factoryOrders: selectedFactoryIDs.sorted()
                        )
                    },
                    onOpenScope: { showOutboundScope = true },
                    orderType: item.orderType,
                    isCompletedOrder: orderDashboardIsCompleted(item.stage)
                )
                .padding(.horizontal, 12)
                .padding(.bottom, 12)
            }
        }
    }

    private func prepareSelectedOrder(_ item: OrderDashboardItem) {
        selectedFactoryID = nil
        selectedFactoryIDs = []
        model.selectedOrderIsOptimized = item.stage == "已优化"
        model.selectedOrderIsCompleted = orderDashboardIsCompleted(item.stage)
        model.loadOrderDetailFromDatabase(item)
    }

    private func toggleExpanded(_ item: OrderDashboardItem) {
        let next = orderDashboardExpandedID(current: expandedOrderID, tapped: item.orderId)
        expandedOrderID = next
        guard next != nil else { return }
        prepareSelectedOrder(item)
    }

    private func openOrderDetail(_ item: OrderDashboardItem) {
        prepareSelectedOrder(item)
        detailOrder = item
    }

    private func openRequestedOrderIfAvailable() {
        let orderID = model.requestedOrderCenterOrderID.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !orderID.isEmpty,
              let item = model.dashboardOrders.first(where: {
                  $0.orderId.caseInsensitiveCompare(orderID) == .orderedSame
              }) else { return }
        model.requestedOrderCenterOrderID = ""
        searchText = item.orderId
        statusFilter = item.stage == "已出货" ? "已出货" : "未完成订单"
        expandedOrderID = nil
    }

    private func tableHeader(_ title: String, width: CGFloat) -> some View {
        Text(title)
            .frame(minWidth: width, idealWidth: width, maxWidth: width, alignment: .center)
            .offset(x: orderDashboardDataHeaderTitles.contains(title) ? orderDashboardDataHeaderOffset : 0)
    }

    private func tableCell<Content: View>(width: CGFloat, @ViewBuilder content: () -> Content) -> some View {
        content()
            .frame(minWidth: width, idealWidth: width, maxWidth: width, alignment: .center)
            .multilineTextAlignment(.center)
    }

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

private func orderInstallationDateFormatter() -> DateFormatter {
    let formatter = DateFormatter()
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.locale = Locale(identifier: "en_US_POSIX")
    formatter.timeZone = .current
    formatter.dateFormat = "yyyy-MM-dd"
    return formatter
}

private func orderInstallationDraftDate(_ value: String) -> Date {
    orderInstallationDateFormatter().date(from: value) ?? Date()
}

private func orderInstallationDraftValue(_ value: Date) -> String {
    orderInstallationDateFormatter().string(from: value)
}

private func orderInstallationPickerDisplayDate(_ value: Date) -> String {
    let formatter = DateFormatter()
    formatter.calendar = Calendar(identifier: .gregorian)
    formatter.locale = Locale(identifier: "en_US_POSIX")
    formatter.timeZone = .current
    formatter.dateFormat = orderInstallationDisplayDateFormat
    return formatter.string(from: value)
}

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
            Text(order.orderId)
                .font(.title2.weight(.semibold))
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
                AppSurfaceCard(padding: 14) {
                    VStack(alignment: .leading, spacing: 12) {
                        Text("订单说明")
                            .font(.headline)
                        TextEditor(text: $note)
                            .font(.body)
                            .frame(minHeight: 54, maxHeight: 72)
                            .padding(5)
                            .overlay(
                                RoundedRectangle(cornerRadius: 6)
                                    .stroke(AppPalette.separator)
                            )
                            .overlay(alignment: .topLeading) {
                                if note.isEmpty {
                                    Text("填写客户要求、待确认事项或特殊交付说明")
                                        .foregroundColor(.secondary)
                                        .padding(.horizontal, 10)
                                        .padding(.vertical, 12)
                                        .allowsHitTesting(false)
                                }
                            }

                        installationRows(title: "计划安装日期", rows: $plannedDays)
                        installationRows(title: "实际安装开始日期", rows: $actualDays)

                    }
                }
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
            // Keep success visible briefly before returning to the order center.
            do { try await Task.sleep(for: .seconds(0.9)) } catch { return }
            dismiss()
        }
    }

    @ViewBuilder
    private func installationRows(
        title: String,
        rows: Binding<[OrderInstallationDraft]>
    ) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack {
                Text(title).font(.subheadline.weight(.semibold))
                Spacer(minLength: 0)
                if rows.wrappedValue.isEmpty {
                    Button {
                        rows.wrappedValue.append(OrderInstallationDraft(date: Date(), installer: ""))
                    } label: {
                        Label("选择开始日期", systemImage: "plus")
                    }
                    .buttonStyle(.borderless)
                }
            }
            if rows.wrappedValue.isEmpty {
                Text("未填写")
                    .font(.caption)
                    .foregroundColor(.secondary)
            } else {
                ForEach(rows) { $day in
                    HStack(spacing: 8) {
                        Button {
                            datePickerRowID = datePickerRowID == day.id ? nil : day.id
                        } label: {
                            HStack(spacing: 6) {
                                Image(systemName: "calendar")
                                    .foregroundColor(AppPalette.accent)
                                Text(orderInstallationPickerDisplayDate(day.date))
                                    .frame(maxWidth: .infinity, alignment: .leading)
                            }
                            .padding(.horizontal, 9)
                            .frame(width: orderInstallationDateButtonWidth, height: 30, alignment: .leading)
                        }
                        .buttonStyle(.glass)
                        .popover(
                            isPresented: Binding(
                                get: { datePickerRowID == day.id },
                                set: { isPresented in
                                    if !isPresented && datePickerRowID == day.id {
                                        datePickerRowID = nil
                                    }
                                }
                            ),
                            // Present beside the date button; the taller order sheet keeps the
                            // complete calendar visible instead of clipping it below the form.
                            arrowEdge: .trailing
                        ) {
                            AppGlassDatePickerCalendar(selection: $day.date, compact: true)
                                .appGlassDatePickerPopoverSurface()
                        }

                        HStack(spacing: 0) {
                            TextField("安装人/安装小组", text: $day.installer)
                                .textFieldStyle(.plain)
                                .padding(.leading, 8)
                                .frame(minHeight: 30)
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
                        .background(
                            RoundedRectangle(cornerRadius: 6)
                                .stroke(AppPalette.separator)
                        )
                        .frame(maxWidth: .infinity)
                        Button {
                            rows.wrappedValue.removeAll { $0.id == day.id }
                            if datePickerRowID == day.id {
                                datePickerRowID = nil
                            }
                        } label: {
                            Image(systemName: "trash")
                        }
                        .buttonStyle(.borderless)
                        .foregroundColor(AppPalette.danger)
                    }
                }
                let summaries = rows.wrappedValue.prefix(1).map {
                    OrderInstallationDay(
                        date: orderInstallationDraftValue($0.date),
                        installer: $0.installer
                    )
                }
                Text("开始：\(orderInstallationDisplayDate(summaries.map(\.date).sorted().first ?? "—"))")
                    .font(.caption)
                    .foregroundColor(.secondary)
            }
        }
    }

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
    let orderType: String
    let isCompletedOrder: Bool

    var body: some View {
        AppSurfaceCard(padding: 14) {
            VStack(alignment: .leading, spacing: 12) {
                detailActions
                factoriesPanel
            }
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
                Button("查询库存") { onQueryStock() }
                    .appActionButton(minWidth: 96)
                    .disabled(isCompletedOrder || model.selectedOrderId.isEmpty || model.orderRunning || !model.orderPreviewReady)
                    .help(isCompletedOrder ? "订单已出货，不能再查询库存" : "查询当前订单库存")
                Button("计算成本") {
                    model.calculateSelectedOrderCost()
                }
                .appActionButton(minWidth: 96)
                .disabled(model.selectedOrderId.isEmpty || model.orderRunning)
                if orderType != "owned" {
                    Button("设置出库范围") { onOpenScope() }
                        .appActionButton(minWidth: 112)
                        .disabled(isCompletedOrder || model.selectedOrderId.isEmpty || model.orderRunning)
                        .help(isCompletedOrder ? "订单已出货，不能再设置出库范围" : "设置当前订单出库范围")
                }
                Button("生产") { onOpenProduction() }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 96)
                    .disabled(
                        isCompletedOrder || model.orderRunning || model.inventoryRunning || selectedFactoryIDs.isEmpty ||
                        orderDashboardHasProducedSelection(selectedFactoryIDs, produced: produced) ||
                        selectedFactoryIDs.contains { factoryID in
                            dashboardFactories.first(where: { $0.factoryOrder == factoryID })?.optimized != true
                        }
                    )
                    .help("选择一个或多个已优化且未生产的工厂单，登记本次实际消耗的订单材料")
                Button(outboundActionTitle) { onOpenOutbound() }
                    .buttonStyle(.glassProminent)
                    .appActionButton(minWidth: 96)
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
                            ? "订单已出货，不能再处理出库"
                            : "只有已生产且未出库的工厂单可以出货；有五金则出库五金，没有五金则只更新出货状态"
                    )
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
            factoryCell(isHeader ? "拆单" : "已拆单", width: orderDashboardFactoryColumnWidths[2], status: !isHeader)
            factoryCell(isHeader ? "优化" : optimization, width: orderDashboardFactoryColumnWidths[3], status: !isHeader && optimization == "已优化")
            factoryCell(
                isHeader ? "生产" : (dashboardFactory?.produced == true ? "已生产" : "未生产"),
                width: orderDashboardFactoryColumnWidths[4],
                status: !isHeader && dashboardFactory?.produced == true
            )
            factoryCell(
                isHeader ? "出库" : orderDashboardOutboundDisplay(status: outbound, documentNumber: outboundDocument),
                width: orderDashboardFactoryColumnWidths[5],
                status: !isHeader && outbound == "已出库"
            )
        }
        .font(isHeader ? .caption.weight(.semibold) : .caption)
        .foregroundColor(isHeader ? .secondary : .primary)
        .padding(.vertical, isHeader ? 9 : 10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .contentShape(Rectangle())
    }

    private func factoryCell(_ text: String, width: CGFloat? = nil, status: Bool = false) -> some View {
        HStack(spacing: 5) {
            if status { Circle().fill(AppPalette.success).frame(width: 7, height: 7) }
            Text(text).lineLimit(1).truncationMode(.tail)
        }
        .frame(minWidth: width ?? 0, maxWidth: width ?? .infinity, alignment: .center)
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

    private enum SheetOperationState {
        case idle
        case preparing
        case running
        case success
        case failure
        case uncertain
    }

    private var isProcessing: Bool {
        operationState == .preparing || operationState == .running
    }

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
                ContentUnavailableView("没有可生产的订单材料", systemImage: "shippingbox", description: Text("请确认工厂单已优化，且订单材料已经写入数据库。"))
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
                                    || isProcessing
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
            HStack {
                Spacer()
                Button(operationState == .success ? "完成" : "关闭") { onClose() }
                    .buttonStyle(.glass)
                    .disabled(isProcessing)
                if operationState == .failure && retryAllowed {
                    Button("重试") { submitProduction() }
                        .buttonStyle(.glassProminent)
                        .disabled(isProcessing)
                } else if operationState == .idle {
                    Button("确认生产并扣减材料") { submitProduction() }
                        .buttonStyle(.glassProminent)
                        .disabled(selectedQuantityCount == 0 || model.productionMaterials.isEmpty)
                }
            }
        }
        .padding(22)
        .onAppear {
            guard !didLoad else { return }
            didLoad = true
            model.loadProductionPreview(orderID: orderID, factoryOrders: factoryOrders)
        }
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
            title = "正在执行生产出库"
        case .success:
            color = AppPalette.success
            icon = "checkmark.circle.fill"
            title = "生产出库成功"
        case .failure:
            color = AppPalette.danger
            icon = "xmark.octagon.fill"
            title = "生产出库失败"
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

    private func submitProduction() {
        guard !isProcessing else { return }
        operationState = .preparing
        operationMessage = "正在校验本次材料数量，尚未操作库存系统……"
        retryAllowed = false
        model.prepareProduction(
            orderID: orderID,
            factoryOrders: factoryOrders,
            materials: model.productionMaterials,
            onResult: { batchNumber, preparationError in
                guard let batchNumber, !batchNumber.isEmpty else {
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
                    batchNumber: batchNumber
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

    private var incomingProcessing: Bool { orderType == "cutToSize" }
    private var noOutboundDecision: Bool {
        requirement == "customer_supplied" || requirement == "remainder" || requirement == "not_required"
    }
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

struct PendingCenterSheet: View {
    @ObservedObject var model: AppModel
    @State private var selectedID: String?
    @State private var searchText = ""
    @State private var category = "全部"
    @State private var orderIDs: [String: String] = [:]
    @State private var confirmationTitle = ""
    @State private var pendingAction: (() -> Void)?
    @State private var showActionConfirmation = false

    private func confirm(_ title: String, action: @escaping () -> Void) {
        confirmationTitle = title
        pendingAction = action
        showActionConfirmation = true
    }

    private var items: [PendingCenterItem] { model.pendingCenterItems }
    private var visibleItems: [PendingCenterItem] {
        items.filter {
            (category == "全部" || $0.status == category) &&
            (searchText.isEmpty || "\($0.title) \($0.subtitle) \($0.folderPath) \($0.issues.map(\.message).joined(separator: " "))".localizedCaseInsensitiveContains(searchText))
        }
    }

    private var selectedItem: PendingCenterItem? {
        visibleItems.first { $0.id == selectedID } ?? visibleItems.first
    }

    private func reconcileSelection() {
        guard !visibleItems.contains(where: { $0.id == selectedID }) else { return }
        selectedID = visibleItems.first?.id
        model.selectedAimesReviewIDs.removeAll()
        model.selectedServerFolderPaths.removeAll()
    }

    /// Always derive the action target from the visible selection.
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
                    Text("查看问题、补充资料并核对预览；确认后才写入订单。")
                        .font(.caption)
                        .foregroundColor(.secondary)
                }
                Spacer()
                AppStatusBadge(text: "\(items.count) 项", kind: .warning)
            }
            HStack(alignment: .top, spacing: 14) {
                VStack(alignment: .leading, spacing: 10) {
                    HStack(spacing: 8) {
                        TextField("搜索订单、问题或路径", text: $searchText)
                            .textFieldStyle(.roundedBorder)
                        Picker("类型", selection: $category) {
                            ForEach(["全部", "待处理", "处理失败", "待人工确认", "需人工处理"], id: \.self) { type in
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
                                    if !item.folderPath.isEmpty {
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

    // Keep a dismissal action available even when the queue or filter is empty.
    private var postponeButton: some View {
        Button("稍后处理") { model.showPendingCenterPrompt = false }
            .buttonStyle(.glass)
            .keyboardShortcut(.cancelAction)
    }

    private func detailTitle(_ item: PendingCenterItem) -> String {
        switch item.status {
        case "处理失败": return "本次处理未完成"
        case "待人工确认": return "核对来源并确认归属"
        case "需人工处理": return "补充材料与商品映射"
        default: return "本次来源变化"
        }
    }

    private func detailExplanation(_ item: PendingCenterItem) -> String {
        switch item.status {
        case "处理失败": return "请根据下方原因检查文件或连接，再重新读取。预览准备好后才能确认写入。"
        case "待人工确认": return "请核对原始信息和建议值，再确认具体操作；缺少的资料需要先补齐。"
        case "需人工处理": return "完成映射后会自动继续读取原订单并准备只读预览。"
        default: return "扫描已完成。预览将读取下列文件，供你核对板材、封边和五金。"
        }
    }

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
                                                    Text("\(changeTypeName(change.changeType))：\(URL(fileURLWithPath: change.path).lastPathComponent)\(timeSuffix)")
                                                        .font(.caption)
                                                    Text(change.path)
                                    .font(.caption2)
                                    .foregroundColor(.secondary)
                                    .lineLimit(1)
                            }
                        }
                    }
                    if group.manualOnly {
                        HStack(spacing: 8) {
                            Text("这是临时文件夹；确认已在外部手工完成出库后，系统会记录当前基线，未来三天只观察两个 XML 文件。")
                                .font(.caption)
                                .foregroundColor(.secondary)
                            Spacer()
                            Button("已人工处理") {
                                confirm("确认已在外部完成人工处理？") { model.markTemporaryFolderManual(group.folderPath) }
                            }
                            .buttonStyle(.glassProminent)
                            .disabled(model.orderRunning)
                        }
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

    @ViewBuilder
    private func issueDetails(_ issue: CurrentIssue) -> some View {
        VStack(alignment: .leading, spacing: 8) {
            HStack(alignment: .top, spacing: 8) {
                Image(systemName: issue.kind == "factory_ownership" ? "person.crop.circle.badge.questionmark" : "exclamationmark.triangle.fill")
                    .foregroundColor(issue.kind == "factory_ownership" ? AppPalette.warning : AppPalette.danger)
                VStack(alignment: .leading, spacing: 3) {
                    Text(issue.kind == "factory_ownership" ? "订单归属问题" : (issue.kind == "server_missing_report" ? "报表检查" : (currentIssueRequiresInventoryMapping(issue) ? "出库前需要材料映射" : "处理失败")))
                        .font(.subheadline.weight(.semibold))
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
                if issue.kind == "factory_ownership" {
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
                    Button("确认已补齐报表") { confirm("确认报表问题已处理？") { model.resolveCurrentIssue(issue, orderID: "") } }
                        .buttonStyle(.glass)
                        .disabled(model.orderRunning)
                }
            }
        }
        .padding(10)
        .background(AppPalette.subtleSurface)
        .clipShape(RoundedRectangle(cornerRadius: 8, style: .continuous))
    }

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

    private func changeTypeName(_ type: String) -> String {
        switch type {
        case "added": return "新增"
        case "removed": return "删除"
        case "renamed": return "改名"
        case "missing_report": return "缺少报表"
        default: return "修改"
        }
    }

    private func changeIcon(_ type: String) -> String {
        switch type {
        case "added": return "plus.circle.fill"
        case "removed": return "minus.circle.fill"
        case "renamed": return "arrow.right.circle.fill"
        case "missing_report": return "doc.questionmark.fill"
        default: return "pencil.circle.fill"
        }
    }

    private func changeColor(_ type: String) -> Color {
        switch type {
        case "added": return AppPalette.success
        case "removed": return AppPalette.danger
        case "renamed": return AppPalette.accent
        case "missing_report": return AppPalette.warning
        default: return AppPalette.warning
        }
    }

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
                                                        Text("\(serverChangeTypeName(change.changeType))：\(URL(fileURLWithPath: change.path).lastPathComponent)")
                                                            .font(.caption)
                                                        Text(change.path)
                                                            .font(.caption2)
                                                            .foregroundColor(.secondary)
                                                            .lineLimit(1)
                                                    }
                                                }
                                            }
                                            if group.manualOnly {
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
                                if group.manualOnly {
                                    Button("已人工处理") {
                                        model.markTemporaryFolderManual(group.folderPath)
                                    }
                                    .buttonStyle(.glassProminent)
                                    .disabled(model.orderRunning)
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
    }

    private func changeIcon(_ type: String) -> String {
        switch type {
        case "added": return "plus.circle.fill"
        case "removed": return "minus.circle.fill"
        default: return "pencil.circle.fill"
        }
    }

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

    private func formatQuantity(_ value: Double) -> String {
        value.rounded() == value ? String(format: "%.0f", value) : String(format: "%.2f", value)
    }

    // The full card is one button, including its rows and padded empty space.
    private func sourceCard(_ candidate: HardwareSourceCandidate, factoryOrder: String) -> some View {
        let selected = model.hardwareSourceChoices[factoryOrder] == candidate.id
        let reportURL = URL(fileURLWithPath: candidate.path)
        let folder = reportURL.deletingLastPathComponent().deletingLastPathComponent().lastPathComponent
        return Button {
            model.hardwareSourceChoices[factoryOrder] = candidate.id
        } label: {
            VStack(alignment: .leading, spacing: 10) {
                HStack(alignment: .top, spacing: 10) {
                    Image(systemName: selected ? "largecircle.fill.circle" : "circle")
                        .foregroundStyle(selected ? Color.accentColor : .secondary)
                    VStack(alignment: .leading, spacing: 4) {
                        Text(folder).font(.headline)
                        Text(reportURL.lastPathComponent).font(.subheadline)
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
        .accessibilityLabel("选择此报表，\(folder)，\(reportURL.lastPathComponent)")
        .accessibilityValue(selected ? "已选中" : "未选中")
    }

}

struct ServerWriteConfirmationSheet: View {
    @ObservedObject var model: AppModel
    @State private var mappingTarget: PendingInventoryMappingTarget?
    @State private var ignoreTarget: PendingInventoryMappingTarget?
    @State private var skippedHardwareOrderIDs: Set<String> = []
    @State private var showWriteConfirmation = false
    private var canConfirmWrite: Bool {
        !model.orderRunning && !model.inventoryRunning && !orders.isEmpty &&
        !model.serverWriteConfirmationFinished && activeHardwareRequirements.isEmpty && invalidOrderValidations.isEmpty
    }
    private var orders: [ServerWriteOrderPreview] { model.serverWritePreview?.orders ?? [] }
    private var activeHardwareRequirements: [ServerHardwareMappingRequirement] {
        model.serverHardwareMappingRequirements.filter { requirement in
            requirement.orderIDs.isEmpty || requirement.orderIDs.contains {
                !skippedHardwareOrderIDs.contains($0.uppercased())
            }
        }
    }
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
                    Text("Server 材料已经按房间归属解析到订单；正式数据库尚未写入。板材、封边和已明确归属的工厂单五金在本界面一次确认。")
                        .font(.callout)
                        .foregroundColor(.secondary)
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
                VStack(alignment: .leading, spacing: 0) {
                    HStack(alignment: .firstTextBaseline, spacing: 12) {
                        VStack(alignment: .leading, spacing: 3) {
                            Text("本次扫描发现的变化")
                                .font(.title3.weight(.semibold))
                            Text("订单材料和工厂单五金写入范围；已出货工厂单自动排除")
                                .font(.subheadline)
                                .foregroundColor(.secondary)
                        }
                        Spacer()
                        Text("\(orders.count) 个订单")
                            .font(.subheadline.weight(.medium))
                            .foregroundColor(AppPalette.accent)
                    }
                    Divider().padding(.top, 10)
                    ScrollView {
                        LazyVStack(alignment: .leading, spacing: 0) {
                            ForEach(orders) { order in
                                orderPreviewCard(order)
                            }
                        }
                    }
                    .frame(minHeight: 260, maxHeight: 440)
                }
            }

            HStack {
                Text(!invalidOrderValidations.isEmpty
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
                Button(model.serverWriteConfirmationFinished ? "已完成写入" : "确认写入订单材料和五金") {
                    showWriteConfirmation = true
                }
                .buttonStyle(.glassProminent)
                .disabled(!canConfirmWrite)
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
        let hasHardware = orders.contains { order in
            !order.hardwareChanges.isEmpty || order.factories.contains { !$0.hardware.isEmpty }
        }
        if hasHardware || !requirements.isEmpty {
            VStack(alignment: .leading, spacing: 8) {
                HStack(alignment: .firstTextBaseline) {
                    Text("工厂单五金 SKU 校验")
                        .font(.subheadline.weight(.semibold))
                    Spacer()
                    Text(requirements.isEmpty ? "已通过" : "待处理 \(requirements.count) 项")
                        .font(.caption.weight(.semibold))
                        .foregroundColor(requirements.isEmpty ? AppPalette.success : AppPalette.warning)
                }
                if requirements.isEmpty {
                    Text("本次五金均已匹配有效 SKU；确认时会按工厂单分别写入，不会进入订单级材料。")
                        .font(.caption)
                        .foregroundColor(.secondary)
                } else {
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
                            .disabled(model.inventoryRunning)
                            Button("忽略") {
                                ignoreTarget = PendingInventoryMappingTarget(name: item.name)
                            }
                            .buttonStyle(.glass)
                            .disabled(model.inventoryRunning)
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

    private func formatQuantity(_ value: Double) -> String {
        value.rounded() == value ? String(Int(value)) : String(format: "%.2f", value)
    }

    @ViewBuilder
    private func orderPreviewCard(_ order: ServerWriteOrderPreview) -> some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack(alignment: .firstTextBaseline, spacing: 10) {
                Text("订单 \(order.orderID)")
                    .font(.title3.weight(.semibold))
                Spacer()
                Text("\(order.materialChanges.count) 项材料变化")
                    .font(.subheadline.weight(.medium))
                    .foregroundColor(.secondary)
            }

            HStack(alignment: .firstTextBaseline, spacing: 8) {
                Text("订单校验")
                    .font(.subheadline.weight(.semibold))
                AppStatusBadge(
                    text: order.validationStatus.isEmpty ? "待校验" : order.validationStatus,
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
                VStack(alignment: .leading, spacing: 7) {
                    Text("订单材料变化")
                        .font(.subheadline.weight(.semibold))
                        .foregroundColor(.secondary)
                    ForEach(sortedServerWriteMaterialChanges(order.materialChanges)) { material in
                        materialChangeRow(material)
                    }
                }
            } else {
                Text("订单材料数量没有变化")
                    .font(.body)
                    .foregroundColor(.secondary)
            }

            if !order.factories.isEmpty {
                VStack(alignment: .leading, spacing: 7) {
                    Text("新增/变更工厂单")
                        .font(.subheadline.weight(.semibold))
                        .foregroundColor(.secondary)
                    ForEach(order.factories) { factory in
                        VStack(alignment: .leading, spacing: 6) {
                            HStack(spacing: 10) {
                                Text(factory.factoryOrder).font(.body.weight(.semibold))
                                    .frame(minWidth: 118, alignment: .leading)
                                Text(factory.factoryName.isEmpty ? "—" : factory.factoryName)
                                    .lineLimit(1)
                                Spacer()
                                Text(factory.changeType.isEmpty ? "发生变化" : factory.changeType)
                                    .foregroundColor(AppPalette.warning)
                            }
                            if !factory.hardware.isEmpty {
                                VStack(alignment: .leading, spacing: 1) {
                                    Text("五金（按 \(factory.factoryOrder) 写入）")
                                        .font(.caption.weight(.semibold))
                                        .foregroundColor(.secondary)
                                    ForEach(factory.hardware) { hardware in
                                        HStack(spacing: 8) {
                                            Text(hardware.displayName.isEmpty ? hardware.name : hardware.displayName)
                                                .frame(maxWidth: .infinity, alignment: .leading)
                                                .lineLimit(1)
                                            Text(hardware.productCode.isEmpty ? "SKU 已通过名称匹配" : "来源编码 \(hardware.productCode) · SKU 已校验")
                                                .font(.caption.monospaced())
                                                .foregroundColor(AppPalette.success)
                                            Text("× \(formatQuantity(hardware.quantity)) \(hardware.unit)")
                                                .font(.caption.monospacedDigit())
                                        }
                                        .padding(.vertical, 1)
                                    }
                                }
                                .padding(.leading, 10)
                            }
                        }
                        .padding(.vertical, 7)
                        Divider()
                    }
                }
            }

            if !order.hardwareChanges.isEmpty {
                VStack(alignment: .leading, spacing: 7) {
                    Text("五金变化（本次不写入）")
                        .font(.subheadline.weight(.semibold))
                        .foregroundColor(AppPalette.warning)
                    hardwareChangeHeaderRow()
                    ForEach(order.hardwareChanges) { hardware in
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
        .padding(.vertical, 14)
        .overlay(Divider(), alignment: .bottom)
    }

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

    private func materialChangeRow(_ material: ServerWriteMaterialChange) -> some View {
        let label = [material.materialType, material.color, material.thickness, material.edge]
            .filter { !$0.isEmpty }.joined(separator: " · ")
        return HStack(spacing: 10) {
            Image(systemName: material.materialType.caseInsensitiveCompare("edge") == .orderedSame ? "line.3.horizontal" : "square.3.layers.3d")
                .foregroundColor(AppPalette.accent)
                .frame(width: 24)
            Text(label)
                .font(.body.weight(.medium))
                .frame(width: 260, alignment: .leading)
                .lineLimit(2)
            Text(material.changeType).font(.caption).foregroundColor(material.changeType == "删除" ? AppPalette.danger : AppPalette.warning)
            Text("\(formatQuantity(material.oldQuantity)) → \(formatQuantity(material.newQuantity)) \(material.unit)")
                .font(.body.monospacedDigit())
        }
        .padding(.vertical, 7)
    }

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


/// Settings entry for reviewing and restoring historical AIMES decisions.
struct AimesHistorySheet: View {
    @ObservedObject var model: AppModel
    @Environment(\.dismiss) private var dismiss
    @State private var showAimesHistory = true
    @State private var confirmationTitle = ""
    @State private var pendingAction: (() -> Void)?
    @State private var showActionConfirmation = false

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
