import SwiftUI

private enum PendingKind: String, CaseIterable, Identifiable {
    case pending = "待处理"
    case failed = "处理失败"
    case confirmation = "待人工确认"
    case manual = "需人工处理"

    var id: String { rawValue }

    var color: Color {
        switch self {
        case .pending: return .blue
        case .failed: return .red
        case .confirmation: return .orange
        case .manual: return .purple
        }
    }

    var symbol: String {
        switch self {
        case .pending: return "doc.text.magnifyingglass"
        case .failed: return "exclamationmark.triangle.fill"
        case .confirmation: return "person.fill"
        case .manual: return "arrow.triangle.2.circlepath"
        }
    }
}

private struct PendingItem: Identifiable {
    let id: String
    let order: String
    let title: String
    let detail: String
    let time: String
    let kind: PendingKind
}

private let pendingItems = [
    PendingItem(id: "PP0042", order: "PP0042", title: "发现 Server 文件变化", detail: "/Volumes/server/Optimized Orders/PP0042", time: "今天 22:52", kind: .pending),
    PendingItem(id: "PP0077", order: "PP0077", title: "服务器目录不可访问", detail: "/Volumes/server/Optimized Orders/mario extracabinets", time: "今天 22:40", kind: .failed),
    PendingItem(id: "PP0063-2", order: "PP0063-2", title: "材料映射待人工确认", detail: "存在 2 处材料映射不确定，需要人工确认", time: "今天 21:18", kind: .confirmation),
    PendingItem(id: "PP0058-1", order: "PP0058-1", title: "AIMES 读取异常", detail: "AIMES 接口超时（错误码：E_TIMEOUT）", time: "今天 20:32", kind: .failed),
    PendingItem(id: "PP0018", order: "PP0018", title: "材料 SKU 尚未映射", detail: "原始名称：White Oak；需要选择库存商品", time: "今天 19:46", kind: .manual)
]

private enum MappingStage {
    case idle
    case rereading
    case previewReady
}

@main
struct PendingCenterPreviewApp: App {
    var body: some Scene {
        WindowGroup("待处理中心预览") {
            PendingCenterPreview()
                .frame(minWidth: 920, idealWidth: 980, minHeight: 580, idealHeight: 620)
        }
        .windowStyle(.hiddenTitleBar)
    }
}

private struct PendingCenterPreview: View {
    @Environment(\.dismiss) private var dismiss
    @State private var selectedID = pendingItems[0].id
    @State private var searchText = ""
    @State private var mappingStage: MappingStage = .idle

    private var selectedItem: PendingItem {
        pendingItems.first(where: { $0.id == selectedID }) ?? pendingItems[0]
    }

    private var filteredItems: [PendingItem] {
        guard !searchText.isEmpty else { return pendingItems }
        return pendingItems.filter { item in
            item.order.localizedCaseInsensitiveContains(searchText)
                || item.title.localizedCaseInsensitiveContains(searchText)
                || item.detail.localizedCaseInsensitiveContains(searchText)
        }
    }

    var body: some View {
        VStack(spacing: 0) {
            AppHeader()

            HStack(spacing: 24) {
                queue
                    .frame(width: 310)
                detail
            }
            .padding(.horizontal, 20)
            .padding(.vertical, 18)
            .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
            .background(Color(nsColor: .windowBackgroundColor))
        }
        .preferredColorScheme(.light)
        .onChange(of: selectedID) { _, _ in
            mappingStage = .idle
        }
    }

    private var queue: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(spacing: 10) {
                Image(systemName: "magnifyingglass")
                    .foregroundStyle(.secondary)
                TextField("搜索订单号、问题或材料", text: $searchText)
                    .textFieldStyle(.plain)
                Image(systemName: "line.3.horizontal.decrease")
                    .foregroundStyle(.secondary)
            }
            .padding(.horizontal, 14)
            .frame(height: 42)
            .background(.white.opacity(0.72), in: RoundedRectangle(cornerRadius: 10))
            .overlay(RoundedRectangle(cornerRadius: 10).stroke(.black.opacity(0.08)))

            HStack(spacing: 12) {
                Text("全部 5").foregroundStyle(.blue)
                Text("待处理 5")
                Text("处理失败 2")
                Text("待人工确认 1")
                Text("需人工处理 1")
            }
            .font(.system(size: 11, weight: .semibold))
            .padding(.horizontal, 6)

            VStack(spacing: 0) {
                ForEach(filteredItems) { item in
                    Button {
                        selectedID = item.id
                    } label: {
                        QueueRow(item: item, selected: selectedID == item.id)
                    }
                    .buttonStyle(.plain)
                }
            }
            .background(.white.opacity(0.70), in: RoundedRectangle(cornerRadius: 14))
            .overlay(RoundedRectangle(cornerRadius: 14).stroke(.black.opacity(0.08)))

            Spacer()
            HStack {
                Image(systemName: "arrow.clockwise")
                Text("刚刚刷新")
                Spacer()
                Text("共 \(pendingItems.count) 项")
            }
            .font(.system(size: 13))
            .foregroundStyle(.secondary)
            .padding(.horizontal, 8)
        }
    }

    private var detail: some View {
        VStack(alignment: .leading, spacing: 0) {
            HStack(alignment: .top) {
                HStack(spacing: 12) {
                    Image(systemName: selectedItem.kind.symbol)
                        .foregroundStyle(selectedItem.kind.color)
                    Text(selectedItem.order)
                        .font(.system(size: 22, weight: .bold))
                    StatusPill(kind: selectedItem.kind)
                }
                Spacer()
                actionButtons(for: selectedItem.kind)
            }

            Text(selectedItem.title)
                .font(.system(size: 16))
                .foregroundStyle(.secondary)
                .padding(.top, 8)

            HStack {
                Text("发现时间：2026-08-31 22:40")
                Spacer()
                Text("问题路径：\(selectedItem.detail)")
            }
            .font(.system(size: 12))
            .foregroundStyle(.secondary)
            .padding(.top, 18)

            Divider().padding(.vertical, 18)

            ScrollView {
                switch selectedItem.kind {
                case .pending:
                    PendingDetail(item: selectedItem)
                case .failed:
                    FailureDetail(item: selectedItem)
                case .confirmation:
                    ConfirmationDetail(item: selectedItem)
                case .manual:
                    ManualDetail(item: selectedItem, stage: mappingStage)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)

            Spacer(minLength: 18)
            HStack {
                Image(systemName: "person.crop.circle")
                Text("发现人：PP FlowHub 系统")
                Spacer()
                Text("最后更新：2026-08-31 22:40")
            }
            .font(.system(size: 12))
            .foregroundStyle(.secondary)
        }
        .padding(24)
        .background(.white.opacity(0.78), in: RoundedRectangle(cornerRadius: 18))
        .overlay(RoundedRectangle(cornerRadius: 18).stroke(.black.opacity(0.08)))
    }

    @ViewBuilder
    private func actionButtons(for kind: PendingKind) -> some View {
        switch kind {
        case .pending:
            HStack {
                Button("稍后处理") {}
                    .buttonStyle(.bordered)
                Button("选择并预览") {}
                    .buttonStyle(.borderedProminent)
            }
        case .failed:
            HStack {
                Button("稍后处理") {}
                    .buttonStyle(.bordered)
                Button("检查并确认重试") {}
                    .buttonStyle(.borderedProminent)
            }
        case .confirmation:
            HStack {
                Button("稍后处理") {}
                    .buttonStyle(.bordered)
                Button("打开只读预览") {}
                    .buttonStyle(.bordered)
                Button("确认后写入") {}
                    .buttonStyle(.borderedProminent)
            }
        case .manual:
            HStack {
                Button("稍后处理") {}
                    .buttonStyle(.bordered)
                Button(mappingStage == .previewReady ? "打开只读预览" : "处理映射") {
                    beginMappingResume()
                }
                .buttonStyle(.borderedProminent)
            }
        }
    }

    private func beginMappingResume() {
        guard mappingStage != .rereading else { return }
        if mappingStage == .previewReady { return }
        mappingStage = .rereading
        Task {
            try? await Task.sleep(nanoseconds: 800_000_000)
            await MainActor.run {
                mappingStage = .previewReady
            }
        }
    }
}

private struct AppHeader: View {
    @Environment(\.dismiss) private var dismiss

    var body: some View {
        HStack(spacing: 14) {
            Image(systemName: "square.grid.2x2")
                .font(.system(size: 22, weight: .medium))
                .foregroundStyle(.blue)
            VStack(alignment: .leading, spacing: 2) {
                Text("待处理中心")
                    .font(.system(size: 18, weight: .bold))
                Text("Server 文件夹、订单问题和 AIMES 待确认统一展示；需人工确认和处理失败分别保留状态。")
                    .font(.system(size: 11))
                    .foregroundStyle(.secondary)
            }
            Spacer()
            Button("关闭") { dismiss() }
                .buttonStyle(.bordered)
            Image(systemName: "exclamationmark.triangle")
                .foregroundStyle(.orange)
            Image(systemName: "info.circle")
        }
        .padding(.horizontal, 20)
        .frame(height: 64)
        .background(Color(nsColor: .windowBackgroundColor).opacity(0.96))
        .overlay(alignment: .bottom) { Divider() }
    }
}

private struct QueueRow: View {
    let item: PendingItem
    let selected: Bool

    var body: some View {
        HStack(alignment: .top, spacing: 12) {
            Image(systemName: item.kind.symbol)
                .foregroundStyle(item.kind.color)
                .padding(.top, 3)
            VStack(alignment: .leading, spacing: 7) {
                HStack {
                    Text(item.order).font(.system(size: 16, weight: .semibold))
                    Text(item.kind.rawValue).foregroundStyle(item.kind.color)
                    Spacer()
                    Text(item.time)
                }
                Text(item.title).font(.system(size: 14, weight: .semibold))
                Text(item.detail)
                    .font(.system(size: 12))
                    .foregroundStyle(.secondary)
                    .lineLimit(2)
            }
        }
        .padding(14)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(selected ? Color.blue.opacity(0.08) : .clear)
        .overlay(alignment: .leading) {
            if selected { Rectangle().fill(.blue).frame(width: 3) }
        }
    }
}

private struct StatusPill: View {
    let kind: PendingKind

    var body: some View {
        Text(kind.rawValue)
            .font(.system(size: 12, weight: .semibold))
            .foregroundStyle(kind.color)
            .padding(.horizontal, 9)
            .padding(.vertical, 5)
            .background(kind.color.opacity(0.12), in: Capsule())
    }
}

private struct DetailSection<Content: View>: View {
    let number: String
    let title: String
    @ViewBuilder let content: Content

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(spacing: 10) {
                Text(number)
                    .font(.system(size: 13, weight: .bold))
                    .foregroundStyle(.white)
                    .frame(width: 24, height: 24)
                    .background(.green, in: Circle())
                Text(title).font(.system(size: 16, weight: .semibold))
            }
            Divider()
            content
        }
        .padding(16)
        .background(.white.opacity(0.55), in: RoundedRectangle(cornerRadius: 14))
        .overlay(RoundedRectangle(cornerRadius: 14).stroke(.black.opacity(0.07)))
    }
}

private struct PendingDetail: View {
    let item: PendingItem

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            DetailSection(number: "1", title: "发现的变化") {
                KeyValueRow(label: "来源", value: "Server 扫描")
                KeyValueRow(label: "文件夹", value: item.detail)
                KeyValueRow(label: "变化", value: "发现 3 个文件变化，尚未读取订单内容")
                KeyValueRow(label: "当前阶段", value: "等待选择并进入预览", valueColor: .blue)
            }
            DetailSection(number: "2", title: "安全边界") {
                Text("“选择并预览”只会读取和生成预览数据，不会写入订单、工厂单或材料事实。预览完成后仍需单独确认写入。")
                    .font(.system(size: 14))
                    .foregroundStyle(.secondary)
            }
        }
    }
}

private struct FailureDetail: View {
    let item: PendingItem

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            DetailSection(number: "1", title: "失败原因与影响") {
                KeyValueRow(label: "问题", value: item.title)
                KeyValueRow(label: "路径", value: item.detail)
                KeyValueRow(label: "影响", value: "本次优化未生成结果，相关材料仍待处理")
                KeyValueRow(label: "可信度", value: "低（无法访问 Server，可能存在数据不一致）", valueColor: .red)
            }
            DetailSection(number: "2", title: "建议处理") {
                Text("确认 Server 路径与权限后重试。此次操作只会重新读取和预览，不会直接写入业务数据。")
                    .font(.system(size: 14))
                    .foregroundStyle(.secondary)
            }
        }
    }
}

private struct ConfirmationDetail: View {
    let item: PendingItem

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            DetailSection(number: "1", title: "将发生的变化（待确认）") {
                ComparisonRow(category: "板材", item: "柜体板", current: "—（无法读取）", suggested: "16mm 实木颗粒板-白色")
                ComparisonRow(category: "封边", item: "柜体封边", current: "—（无法读取）", suggested: "PVC 1mm 白色")
                ComparisonRow(category: "五金", item: "铰链", current: "—（无法读取）", suggested: "阻尼铰链（全盖）")
            }
            DetailSection(number: "2", title: "操作边界") {
                Label("只读预览", systemImage: "eye")
                Text("预览不会修改任何数据，用于人工核对变更内容。")
                    .foregroundStyle(.secondary)
                Label("写入触发条件", systemImage: "square.and.pencil")
                Text("仅在点击“确认后写入”并通过二次确认时，系统才会执行真实写入。")
                    .foregroundStyle(.secondary)
            }
        }
        .font(.system(size: 14))
    }
}

private struct ManualDetail: View {
    let item: PendingItem
    let stage: MappingStage

    var body: some View {
        VStack(alignment: .leading, spacing: 18) {
            DetailSection(number: "1", title: "需要补充的映射") {
                KeyValueRow(label: "原始名称", value: "White Oak")
                KeyValueRow(label: "来源", value: item.detail)
                KeyValueRow(label: "阻塞原因", value: "找不到可靠的库存商品 SKU")
                KeyValueRow(label: "影响", value: "映射完成后才能继续材料校验和订单预览")
            }
            if stage == .rereading {
                DetailSection(number: "2", title: "正在继续处理") {
                    Label("映射已保存", systemImage: "checkmark.circle.fill")
                        .foregroundStyle(.green)
                    Text("正在重新读取订单文件并继续未完成的扫描、解析和校验；完成后会自动呈现只读预览。")
                        .foregroundStyle(.secondary)
                }
            } else if stage == .previewReady {
                DetailSection(number: "2", title: "只读预览已准备好") {
                    Label("重新读取完成", systemImage: "checkmark.circle.fill")
                        .foregroundStyle(.green)
                    Text("映射已经应用到本次预览。请核对材料变化，确认无误后再执行写入。")
                        .foregroundStyle(.secondary)
                    Button("打开只读预览") {}
                        .buttonStyle(.borderedProminent)
                }
            } else {
                DetailSection(number: "2", title: "处理边界") {
                    Text("先完成映射，系统会自动继续读取和校验，随后把结果带回只读预览。映射保存不等于业务事实写入。")
                        .foregroundStyle(.secondary)
                }
            }
        }
        .font(.system(size: 14))
    }
}

private struct KeyValueRow: View {
    let label: String
    let value: String
    var valueColor: Color = .primary

    var body: some View {
        HStack(alignment: .top) {
            Text(label).frame(width: 72, alignment: .leading).foregroundStyle(.secondary)
            Text(value).foregroundStyle(valueColor)
        }
    }
}

private struct ComparisonRow: View {
    let category: String
    let item: String
    let current: String
    let suggested: String

    var body: some View {
        Grid(alignment: .leading, horizontalSpacing: 22, verticalSpacing: 9) {
            GridRow {
                Text(category).foregroundStyle(.secondary)
                Text(item)
                Text(current).foregroundStyle(.secondary)
                Text(suggested)
                Text("待确认").foregroundStyle(.orange)
            }
        }
    }
}
