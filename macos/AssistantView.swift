// 助手页面负责语音与文字输入、命令预览、审批和结果展示。
// 命令解释和业务校验由 Python CLI/Gateway 负责，确保 App 与 CLI 使用同一契约。
import AVFoundation
import AppKit
import Speech
import SwiftUI

/// 将语音中的订单前缀、中文数字和连接符规范化为订单命令。
/// - Parameters:
///   - text: 原始语音转写文字。
func canonicalSpeechCommand(_ text: String) -> String {
    let pattern = #"(?i)(p\s*p|c\s*s)\s*([0-9零〇○一二两三四五六七八九幺\s]+)(?:(?:-|\s*[杠横]\s*)([0-9零〇○一二两三四五六七八九幺\s]+))?"#
    guard let expression = try? NSRegularExpression(pattern: pattern) else { return text }
    let source = text as NSString
    let matches = expression.matches(in: text, range: NSRange(location: 0, length: source.length))
    let digitMap: [Character: Character] = [
        "零": "0", "〇": "0", "○": "0", "一": "1", "幺": "1", "二": "2", "两": "2",
        "三": "3", "四": "4", "五": "5", "六": "6", "七": "7", "八": "8", "九": "9",
    ]
    let result = NSMutableString(string: text)
    for match in matches.reversed() {
        let prefix = source.substring(with: match.range(at: 1))
            .replacingOccurrences(of: " ", with: "").uppercased()
        /// 提取当前正则匹配的数字分组，去空白并转换中文数字。
        /// - Parameters:
        ///   - index: 正则捕获组序号。
        func digits(at index: Int) -> String {
            guard match.range(at: index).location != NSNotFound else { return "" }
            return source.substring(with: match.range(at: index)).compactMap { character in
                if character.isWhitespace { return nil }
                return digitMap[character] ?? character
            }.map(String.init).joined()
        }
        let suffix = digits(at: 3)
        let replacement = prefix + digits(at: 2) + (suffix.isEmpty ? "" : "-\(suffix)")
        result.replaceCharacters(in: match.range, with: replacement)
    }
    return (result as String).replacingOccurrences(of: #"\s+"#, with: "", options: .regularExpression)
}

struct AssistantOrderResult {
    let orderId: String
    let materialsFile: String
    let existingTraveler: String
    let materials: [OrderMaterialPreview]
    let edgeBanding: [String: Double]
    let factories: [OrderFactoryPreview]
    let fittings: [OrderFittingPreview]
    let warnings: [String]

    /// 解析助手返回的订单材料、工厂单和五金；订单身份不完整时失败。
    /// - Parameters:
    ///   - object: 后端返回的 JSON 结果对象。
    init?(object: [String: Any]) {
        guard object["materials"] != nil,
              let orderId = object["order_id"] as? String, !orderId.isEmpty else { return nil }
        self.orderId = orderId
        materialsFile = object["materials_file"] as? String ?? ""
        existingTraveler = object["existing_traveler"] as? String ?? ""
        warnings = object["warnings"] as? [String] ?? []
        materials = (object["materials"] as? [[String: Any]] ?? []).map {
            OrderMaterialPreview(
                kind: $0["kind"] as? String ?? "",
                thickness: ($0["thickness"] as? NSNumber)?.doubleValue ?? 0,
                color: $0["color"] as? String ?? "",
                quantity: ($0["quantity"] as? NSNumber)?.doubleValue ?? 0
            )
        }
        edgeBanding = (object["edge_banding"] as? [String: NSNumber] ?? [:]).mapValues(\.doubleValue)
        var parsedFactories: [OrderFactoryPreview] = []
        var parsedFittings: [OrderFittingPreview] = []
        for factory in object["factories"] as? [[String: Any]] ?? [] {
            let number = factory["factory_order"] as? String ?? ""
            let name = factory["order_name"] as? String ?? ""
            parsedFactories.append(OrderFactoryPreview(id: number, factoryOrder: number, orderName: name))
            for fitting in factory["fittings"] as? [[String: Any]] ?? [] {
                let key = fitting["key"] as? String ?? UUID().uuidString
                parsedFittings.append(OrderFittingPreview(
                    id: number + ":" + key,
                    key: key,
                    factoryOrder: number,
                    orderName: name,
                    name: fitting["name"] as? String ?? "",
                    displayName: fitting["display_name"] as? String ?? fitting["name"] as? String ?? "",
                    code: fitting["code"] as? String ?? "",
                    size: fitting["size"] as? String ?? "",
                    unit: fitting["unit"] as? String ?? "",
                    quantity: (fitting["quantity"] as? NSNumber)?.doubleValue ?? 0,
                    ignored: fitting["ignored"] as? Bool ?? false
                ))
            }
        }
        factories = parsedFactories
        fittings = parsedFittings
    }
}

@MainActor
final class SpeechInputController: ObservableObject {
    @Published var transcript = ""
    @Published var isRecording = false
    @Published var isHolding = false
    @Published var errorMessage = ""

    private let recognizer = SFSpeechRecognizer(locale: Locale(identifier: "zh_CN"))
    private let audioEngine = AVAudioEngine()
    private var request: SFSpeechAudioBufferRecognitionRequest?
    private var task: SFSpeechRecognitionTask?
    private var pendingCompletion: ((String) -> Void)?
    private var finalResultAvailable = false

    /// 重置语音草稿并申请权限，开始按住说话流程。
    /// 无参数。
    func beginPushToTalk() {
        guard !isHolding else { return }
        isHolding = true
        transcript = ""
        errorMessage = ""
        finalResultAvailable = false
        requestAccessAndStart()
    }

    /// 结束录音并等待最终识别结果，超时后使用已有转写。
    /// - Parameters:
    ///   - onComplete: 结束识别后接收非空转写文字的回调。
    func endPushToTalk(onComplete: @escaping (String) -> Void) {
        guard isHolding else { return }
        isHolding = false
        guard isRecording else { return }
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        request?.endAudio()
        isRecording = false
        pendingCompletion = onComplete
        if finalResultAvailable {
            completeRecognition()
            return
        }
        DispatchQueue.main.asyncAfter(deadline: .now() + 1.5) { [weak self] in
            self?.completeRecognition()
        }
    }

    /// 停止录音和识别任务，清除待完成回调及按住状态。
    /// 无参数。
    func stop() {
        audioEngine.stop()
        audioEngine.inputNode.removeTap(onBus: 0)
        request?.endAudio()
        task?.cancel()
        request = nil
        task = nil
        pendingCompletion = nil
        finalResultAvailable = false
        isRecording = false
        isHolding = false
    }

    /// 释放识别任务，将非空转写交给待执行回调。
    /// 无参数。
    private func completeRecognition() {
        guard let completion = pendingCompletion else { return }
        pendingCompletion = nil
        let finalText = transcript.trimmingCharacters(in: .whitespacesAndNewlines)
        task?.cancel()
        task = nil
        request = nil
        if finalText.isEmpty {
            errorMessage = "没有识别到语音，请重试。"
        } else {
            completion(finalText)
        }
    }

    /// 依次申请语音识别和麦克风权限，在仍按住时启动录音。
    /// 无参数。
    private func requestAccessAndStart() {
        SFSpeechRecognizer.requestAuthorization { status in
            guard status == .authorized else {
                Task { @MainActor in self.errorMessage = "请在系统设置中允许语音识别。" }
                return
            }
            AVCaptureDevice.requestAccess(for: .audio) { allowed in
                Task { @MainActor in
                    if !allowed {
                        self.isHolding = false
                        self.errorMessage = "请在系统设置中允许麦克风。"
                    } else if self.isHolding {
                        self.start()
                    }
                }
            }
        }
    }

    /// 配置音频采样和中文语音识别，持续更新转写及异常状态。
    /// 无参数。
    private func start() {
        guard !isRecording, let recognizer, recognizer.isAvailable else {
            errorMessage = "语音识别暂不可用。"
            return
        }
        transcript = ""
        errorMessage = ""
        let recognitionRequest = SFSpeechAudioBufferRecognitionRequest()
        recognitionRequest.shouldReportPartialResults = true
        request = recognitionRequest
        let input = audioEngine.inputNode
        let format = input.outputFormat(forBus: 0)
        input.installTap(onBus: 0, bufferSize: 1024, format: format) { buffer, _ in
            recognitionRequest.append(buffer)
        }
        task = recognizer.recognitionTask(with: recognitionRequest) { result, error in
            Task { @MainActor in
                if let result {
                    self.transcript = result.bestTranscription.formattedString
                    if result.isFinal {
                        self.finalResultAvailable = true
                        if self.pendingCompletion != nil { self.completeRecognition() }
                        else if !self.isHolding { self.stop() }
                    }
                } else if error != nil {
                    if self.pendingCompletion != nil {
                        self.completeRecognition()
                    } else if self.isRecording {
                        self.stop()
                        self.errorMessage = "语音识别中断，请重试。"
                    }
                }
            }
        }
        do {
            audioEngine.prepare()
            try audioEngine.start()
            isRecording = true
        } catch {
            stop()
            errorMessage = businessFriendlyMessage(error.localizedDescription, operation: "启动麦克风")
        }
    }
}

/// 判断按键是否为仅按住 Option 的空格键快捷键。
/// - Parameters:
///   - keyCode: 系统按键代码。
///   - modifiers: 按键事件的修饰键集合。
func isPushToTalkShortcut(keyCode: UInt16, modifiers: NSEvent.ModifierFlags) -> Bool {
    keyCode == 49 && modifiers.intersection(.deviceIndependentFlagsMask) == .option
}

@MainActor
final class PushToTalkShortcutMonitor: ObservableObject {
    private var keyDownMonitor: Any?
    private var keyUpMonitor: Any?
    private var held = false

    /// 注册本地按下和松开事件，避免长按时重复触发录音。
    /// - Parameters:
    ///   - onPress: 首次按下语音快捷键时执行的回调。
    ///   - onRelease: 松开语音快捷键时执行的回调。
    func install(onPress: @escaping () -> Void, onRelease: @escaping () -> Void) {
        guard keyDownMonitor == nil else { return }
        keyDownMonitor = NSEvent.addLocalMonitorForEvents(matching: .keyDown) { [weak self] event in
            guard isPushToTalkShortcut(keyCode: event.keyCode, modifiers: event.modifierFlags) else { return event }
            if self?.held == false {
                self?.held = true
                onPress()
            }
            return nil
        }
        keyUpMonitor = NSEvent.addLocalMonitorForEvents(matching: .keyUp) { [weak self] event in
            guard event.keyCode == 49, self?.held == true else { return event }
            self?.held = false
            onRelease()
            return nil
        }
    }

    /// 移除键盘事件监听并清除长按状态。
    /// 无参数。
    func uninstall() {
        if let keyDownMonitor { NSEvent.removeMonitor(keyDownMonitor) }
        if let keyUpMonitor { NSEvent.removeMonitor(keyUpMonitor) }
        keyDownMonitor = nil
        keyUpMonitor = nil
        held = false
    }
}

struct AssistantOrderPreviewView: View {
    let result: AssistantOrderResult

    var body: some View {
        VStack(alignment: .leading, spacing: 14) {
            HStack(spacing: 10) {
                metricCard("订单号", result.orderId, "checkmark.seal.fill")
                metricCard("工厂单", "\(result.factories.count) 份", "building.2.fill")
                metricCard("材料项目", "\(result.materials.count + result.edgeBanding.count) 项", "square.stack.3d.up.fill")
                metricCard("本机 Traveler", result.existingTraveler.isEmpty ? "未生成" : "已存在", "doc.badge.checkmark")
            }

            if !result.materials.isEmpty {
                sectionTitle("板材用量", "rectangle.stack.fill")
                LazyVGrid(
                    columns: [GridItem(.adaptive(minimum: 170, maximum: 230), spacing: 9)],
                    alignment: .leading,
                    spacing: 9
                ) {
                    ForEach(result.materials) { row in
                        VStack(alignment: .leading, spacing: 5) {
                            Text(orderMaterialDisplayName(row))
                                .font(.system(size: AppLayout.materialNameFontSize, weight: .semibold))
                                .lineLimit(2)
                            HStack {
                                Text("规格 \(row.thickness.formatted())mm")
                                    .font(.caption).foregroundColor(.secondary)
                                Spacer()
                                Text("\(row.quantity.formatted()) 张")
                                    .font(.title3).fontWeight(.bold).foregroundColor(AppPalette.accent)
                            }
                        }
                        .padding(10)
                        .background(AppPalette.accent.opacity(row.kind == "panel" ? 0.12 : 0.06))
                        .clipShape(RoundedRectangle(cornerRadius: 9))
                    }
                }
            }

            if !result.edgeBanding.isEmpty {
                sectionTitle("封边用量", "lines.measurement.horizontal")
                LazyVGrid(
                    columns: [GridItem(.adaptive(minimum: 180, maximum: 230), spacing: 9)],
                    alignment: .leading,
                    spacing: 9
                ) {
                    ForEach(result.edgeBanding.keys.sorted(), id: \.self) { color in
                        HStack {
                            Text(color).fontWeight(.semibold).lineLimit(1)
                            Spacer()
                            Text("\((result.edgeBanding[color] ?? 0).formatted())m")
                                .font(.title3).fontWeight(.bold).foregroundColor(AppPalette.accent)
                        }
                        .padding(10)
                        .background(AppPalette.accent.opacity(0.06))
                        .clipShape(RoundedRectangle(cornerRadius: 9))
                    }
                }
            }

            if !result.factories.isEmpty {
                sectionTitle("工厂单与五金", "wrench.and.screwdriver.fill")
                ForEach(result.factories) { factory in
                    let rows = result.fittings.filter { $0.factoryOrder == factory.factoryOrder }
                    VStack(spacing: 0) {
                        HStack {
                            Text("\(factory.factoryOrder) · \(factory.orderName)").fontWeight(.semibold)
                            Spacer()
                            Text("\(rows.count) 项五金").font(.caption).foregroundColor(.secondary)
                        }
                        .padding(9)
                        .background(AppPalette.accent.opacity(0.09))
                        ForEach(rows) { row in
                            HStack {
                                Text(row.displayName.isEmpty ? row.name : row.displayName)
                                    .frame(maxWidth: .infinity, alignment: .leading)
                                Text(row.code).foregroundColor(.secondary).frame(width: 100, alignment: .leading)
                                Text(row.size.isEmpty ? "—" : row.size).foregroundColor(.secondary).frame(width: 110, alignment: .leading)
                                Text("\(row.quantity.formatted()) \(row.unit)")
                                    .fontWeight(.semibold).frame(width: 100, alignment: .trailing)
                            }
                            .padding(.horizontal, 9).padding(.vertical, 6)
                            Divider()
                        }
                    }
                    .background(AppPalette.surface)
                    .clipShape(RoundedRectangle(cornerRadius: 9))
                    .overlay(RoundedRectangle(cornerRadius: 9).stroke(AppPalette.accent.opacity(0.14)))
                }
            }

            ForEach(result.warnings, id: \.self) { warning in
                Label(warning, systemImage: "exclamationmark.triangle.fill")
                    .foregroundColor(AppPalette.warning)
            }
        }
        .padding(12)
    }

    /// 构造订单预览中带图标的统计卡片。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - value: 需要显示的数值或状态文字。
    ///   - icon: 系统图标名称。
    private func metricCard(_ title: String, _ value: String, _ icon: String) -> some View {
        VStack(alignment: .leading, spacing: 5) {
            Label(title, systemImage: icon).font(.caption).foregroundColor(.secondary)
            Text(value).font(.headline).lineLimit(1)
        }
        .padding(10)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(AppPalette.accent.opacity(0.07))
        .clipShape(RoundedRectangle(cornerRadius: 9))
    }

    /// 构造订单预览中的图标分区标题。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - icon: 系统图标名称。
    private func sectionTitle(_ title: String, _ icon: String) -> some View {
        Label(title, systemImage: icon).font(.headline).foregroundColor(AppPalette.accent)
    }
}

struct AssistantOrderListView: View {
    let orders: [OrderFolderItem]

    var body: some View {
        LazyVGrid(columns: [GridItem(.adaptive(minimum: 190), spacing: 9)], spacing: 9) {
            ForEach(orders) { order in
                HStack {
                    Image(systemName: "folder.fill").foregroundColor(AppPalette.accent)
                    VStack(alignment: .leading, spacing: 3) {
                        Text(order.orderId).fontWeight(.semibold)
                        Text(appDisplayTimestamp(order.modifiedAt)).font(.caption).foregroundColor(.secondary)
                    }
                    Spacer()
                }
                .padding(10)
                .background(AppPalette.accent.opacity(0.06))
                .clipShape(RoundedRectangle(cornerRadius: 9))
            }
        }
        .padding(12)
    }
}

struct AssistantStockComparisonView: View {
    let orderId: String
    let traveler: String
    let rows: [OrderStockPreview]

    var body: some View {
        VStack(alignment: .leading, spacing: 12) {
            HStack {
                Label(orderId, systemImage: "shippingbox.and.arrow.backward")
                    .font(.title3).fontWeight(.semibold).foregroundColor(AppPalette.accent)
                Spacer()
                let shortages = rows.filter { !$0.sufficient }.count
                Text(shortages == 0 ? "库存全部充足" : "\(shortages) 项库存不足")
                    .fontWeight(.semibold)
                    .foregroundColor(shortages == 0 ? AppPalette.success : AppPalette.warning)
            }
            Text(displayPathName(traveler))
                .font(.caption).foregroundColor(.secondary).lineLimit(1)

            HStack(spacing: 10) {
                Text("商品").frame(maxWidth: .infinity, alignment: .leading)
                Text("编号").frame(width: 86, alignment: .leading)
                Text("单位").frame(width: 50, alignment: .center)
                Text("所需").frame(width: 72, alignment: .trailing)
                Text("库存").frame(width: 72, alignment: .trailing)
                Text("结果").frame(width: 90, alignment: .trailing)
            }
            .font(.caption).foregroundColor(.secondary)
            Divider()
            ForEach(rows) { row in
                HStack(spacing: 10) {
                    VStack(alignment: .leading, spacing: 2) {
                        Text(row.productName).fontWeight(.medium).lineLimit(1)
                        Text(row.travelerNames.joined(separator: "、"))
                            .font(.caption2).foregroundColor(.secondary).lineLimit(1)
                    }
                    .frame(maxWidth: .infinity, alignment: .leading)
                    Text(row.productCode).frame(width: 86, alignment: .leading)
                    Text(row.unit.isEmpty ? "—" : row.unit).frame(width: 50, alignment: .center)
                    Text(row.required.formatted()).frame(width: 72, alignment: .trailing)
                    Text(row.available.formatted()).frame(width: 72, alignment: .trailing)
                    Text(row.sufficient ? "充足" : "缺 \(row.shortage.formatted())")
                        .fontWeight(.semibold)
                        .foregroundColor(row.sufficient ? AppPalette.success : AppPalette.warning)
                        .frame(width: 90, alignment: .trailing)
                }
                .padding(.vertical, 7)
                Divider()
            }
        }
        .padding(12)
    }
}

let assistantCommandHints = [
    "查找 PP0063  ·  Find order PP0063",
    "查找 CS004  ·  Find cut-to-size order CS004",
    "生成 PP0063 的 Traveler  ·  Generate Traveler for PP0063",
    "更新 Traveler PP0063  ·  Update Traveler PP0063",
    "刷新订单  ·  Refresh order list",
    "检查 PP0063  ·  Check order PP0063",
    "给 PP1234-2-LAUNDRY 添加人工五金 M0144 数量 2",
    "Add 2 pieces of M0144 to PP1234-2-LAUNDRY",
]

/// 判断任务状态是否允许在顶部显示取消入口。
/// - Parameters:
///   - status: 业务状态文字或状态代码。
func assistantTaskShowsHeaderCancel(_ status: String) -> Bool {
    status == "排队中" || status == "执行中"
}

struct AssistantCommandHintsContent: View {
    var body: some View {
        VStack(alignment: .leading, spacing: 9) {
            Label("常用命令", systemImage: "lightbulb.fill")
                .font(.headline).foregroundColor(AppPalette.accent)
            ForEach(assistantCommandHints, id: \.self) { command in
                Text(command).font(.callout).textSelection(.enabled)
            }
        }
        .padding(14)
        .frame(width: 520, alignment: .leading)
    }
}

extension AppModel {
    /// 异步读取助手 Token 使用统计并更新用量摘要。
    /// 无参数。
    func loadAssistantUsage() {
        let root = projectRoot
        let executable = root.appendingPathComponent("scripts/pp-flowhub")
        DispatchQueue.global(qos: .utility).async {
            let process = Process()
            let output = Pipe()
            process.executableURL = executable
            process.currentDirectoryURL = root
            process.arguments = ["assistant", "--usage"]
            process.standardOutput = output
            do {
                try process.run()
                let data = output.fileHandleForReading.readDataToEndOfFile()
                process.waitUntilExit()
                guard let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                      let usage = object["usage"] as? [String: Any] else { return }
                let week = usage["week"] as? Int ?? 0
                let month = usage["month"] as? Int ?? 0
                let total = usage["total"] as? Int ?? 0
                DispatchQueue.main.async {
                    self.assistantUsageSummary = "本周 \(week) · 本月 \(month) · 累计 \(total) Token"
                }
            } catch {}
        }
    }

    /// 将输入指令加入助手队列，或继续执行已获批准的指令。
    /// - Parameters:
    ///   - approved: 当前指令是否已获用户批准。
    func runAssistantCommand(approved: Bool = false) {
        if approved {
            guard let id = assistantActiveTaskID,
                  let task = assistantTasks.first(where: { $0.id == id }) else { return }
            assistantPendingApproval = false
            assistantWriteInProgress = true
            logUserAction("点击确认执行助手命令", details: ["approved": true])
            executeAssistantTask(task, approved: true)
            return
        }
        let text = assistantInput.trimmingCharacters(in: .whitespacesAndNewlines)
        guard !text.isEmpty else { return }
        logUserAction("点击执行助手命令", details: ["input_present": true])
        assistantTasks.append(AssistantTaskItem(text: text))
        assistantInput = ""
        processNextAssistantTask()
    }

    /// 取消排队或正在执行的助手任务，并保护进行中的写入。
    /// - Parameters:
    ///   - id: 助手任务的唯一标识。
    func cancelAssistantTask(_ id: UUID) {
        guard let index = assistantTasks.firstIndex(where: { $0.id == id }) else { return }
        logUserAction("点击取消助手任务", details: ["task_active": id == assistantActiveTaskID])
        if id == assistantActiveTaskID {
            guard !assistantWriteInProgress else { return }
            assistantProcess?.terminate()
            assistantProcess = nil
            assistantRunning = false
            assistantPendingApproval = false
            assistantTasks[index].status = "已取消"
            assistantActiveTaskID = nil
            processNextAssistantTask()
        } else if assistantTasks[index].status == "排队中" {
            assistantTasks[index].status = "已取消"
        }
    }

    /// 在助手空闲且无需审批时启动下一个排队任务。
    /// 无参数。
    func processNextAssistantTask() {
        guard assistantActiveTaskID == nil,
              let index = assistantTasks.firstIndex(where: { $0.status == "排队中" }) else { return }
        assistantActiveTaskID = assistantTasks[index].id
        executeAssistantTask(assistantTasks[index], approved: false)
    }

    /// 调用助手 CLI，解析审批、预览和结果并更新任务界面。
    /// - Parameters:
    ///   - task: 正在执行的助手队列任务。
    ///   - approved: 当前指令是否已获用户批准。
    private func executeAssistantTask(_ task: AssistantTaskItem, approved: Bool) {
        guard !assistantRunning else { return }
        assistantRunning = true
        if let index = assistantTasks.firstIndex(where: { $0.id == task.id }) {
            assistantTasks[index].status = approved ? "正在写入" : "执行中"
        }
        assistantTokenSummary = "本次 0 Token（本地解析）"
        assistantOrderPreview = nil
        assistantOrderList = []
        assistantStockRows = []
        assistantStockOrderId = ""
        assistantStockTraveler = ""
        assistantOutput = "正在执行指令…"
        let root = projectRoot
        let executable = root.appendingPathComponent("scripts/pp-flowhub")
        let operationID = newOperationID(
            "助手后台操作",
            details: ["command": "assistant", "approved": approved]
        )
        DispatchQueue.global(qos: .userInitiated).async {
            let process = Process()
            let output = Pipe()
            process.executableURL = executable
            process.currentDirectoryURL = root
            process.arguments = ["assistant", task.text] + (approved ? ["--approve"] : [])
            process.environment = self.environmentForOperation(operationID)
            process.standardOutput = output
            do {
                DispatchQueue.main.async { self.assistantProcess = process }
                try process.run()
                let data = output.fileHandleForReading.readDataToEndOfFile()
                process.waitUntilExit()
                DispatchQueue.main.async {
                    self.assistantProcess = nil
                    self.assistantRunning = false
                    self.assistantWriteInProgress = false
                    if self.assistantTasks.first(where: { $0.id == task.id })?.status == "已取消" {
                        return
                    }
                    guard let object = try? JSONSerialization.jsonObject(with: data) as? [String: Any] else {
                        self.assistantOutput = "本地助手没有返回有效结果。"
                        self.finishAssistantTask(task.id, status: "失败")
                        return
                    }
                    let status = object["status"] as? String ?? "failed"
                    self.assistantPendingApproval = status == "approval_required"
                    let previewObject = object["preview"] as? [String: Any] ?? object
                    self.assistantOrderPreview = AssistantOrderResult(object: previewObject)
                    if object["result_type"] as? String == "stock_comparison" {
                        self.assistantStockOrderId = object["order_id"] as? String ?? ""
                        self.assistantStockTraveler = object["traveler"] as? String ?? ""
                        self.assistantStockRows = (object["rows"] as? [[String: Any]] ?? []).map { row in
                            let code = row["productCode"] as? String ?? UUID().uuidString
                            return OrderStockPreview(
                                id: code,
                                productCode: code,
                                productName: row["productName"] as? String ?? "",
                                unit: row["unit"] as? String ?? "",
                                travelerNames: row["travelerNames"] as? [String] ?? [],
                                required: (row["requiredQuantity"] as? NSNumber)?.doubleValue ?? 0,
                                available: (row["availableQuantity"] as? NSNumber)?.doubleValue ?? 0,
                                shortage: (row["shortageQuantity"] as? NSNumber)?.doubleValue ?? 0,
                                sufficient: row["sufficient"] as? Bool ?? false
                            )
                        }
                    }
                    self.assistantOrderList = (object["orders"] as? [[String: Any]] ?? []).map {
                        OrderFolderItem(
                            id: $0["path"] as? String ?? UUID().uuidString,
                            orderId: $0["order_id"] as? String ?? "",
                            modifiedAt: $0["modified_at"] as? String ?? ""
                        )
                    }
                    if let usage = object["token_usage"] as? [String: Any] {
                        let input = usage["input"] as? Int ?? 0
                        let output = usage["output"] as? Int ?? 0
                        let total = usage["total"] as? Int ?? input + output
                        let source = object["source"] as? String ?? "local"
                        let label = source == "agent" ? "Agent" : (source == "learned_local" ? "本地学习" : "本地解析")
                        self.assistantTokenSummary = "本次 \(total) Token（\(label)：输入 \(input) / 输出 \(output)）"
                    }
                    if status == "agent_failed" {
                        let error = object["error"] as? [String: Any]
                        self.assistantOutput = businessFriendlyMessage(
                            error?["message"] as? String ?? "本地助手暂不可用，请稍后重试。",
                            operation: "运行本地助手"
                        )
                    } else if status == "unsupported" {
                        self.assistantOutput = object["explanation"] as? String ?? "暂不支持这项操作。"
                    } else if status == "approval_required" {
                        self.assistantOutput = self.assistantOrderPreview == nil
                            ? "预览已完成。这是真实写入操作，请确认后执行。" : ""
                    } else if let error = object["error"] as? [String: Any] {
                        self.assistantOutput = businessFriendlyMessage(
                            error["message"] as? String ?? "本地助手没有完成操作，请重试。",
                            operation: "运行本地助手"
                        )
                    } else {
                        self.assistantOutput = (self.assistantOrderPreview != nil || !self.assistantOrderList.isEmpty || !self.assistantStockRows.isEmpty)
                            ? "" : "操作已完成。"
                    }
                    if status == "approval_required" {
                        if let index = self.assistantTasks.firstIndex(where: { $0.id == task.id }) {
                            self.assistantTasks[index].status = "等待确认"
                        }
                    } else {
                        self.finishAssistantTask(task.id, status: status == "completed" ? "已完成" : "失败")
                    }
                    self.loadAssistantUsage()
                }
            } catch {
                DispatchQueue.main.async {
                    self.assistantProcess = nil
                    self.assistantRunning = false
                    self.assistantWriteInProgress = false
                    if self.assistantTasks.first(where: { $0.id == task.id })?.status == "已取消" {
                        return
                    }
                    self.assistantOutput = businessFriendlyMessage(error.localizedDescription, operation: "启动本地助手")
                    self.finishAssistantTask(task.id, status: "失败")
                }
            }
        }
    }

    /// 更新任务最终状态并清理活动任务，继续处理队列。
    /// - Parameters:
    ///   - id: 助手任务的唯一标识。
    ///   - status: 业务状态文字或状态代码。
    private func finishAssistantTask(_ id: UUID, status: String) {
        if let index = assistantTasks.firstIndex(where: { $0.id == id }) {
            assistantTasks[index].status = status
        }
        if assistantActiveTaskID == id { assistantActiveTaskID = nil }
        processNextAssistantTask()
    }

}

private enum AssistantDashboardTypography {
    static let metricLabel: CGFloat = 15
    static let metricValue: CGFloat = 40
    static let operationLabel: CGFloat = 15
    static let operationTitle: CGFloat = 20
    static let operationDetail: CGFloat = 14
    static let boardTitle: CGFloat = 28
    static let boardSubtitle: CGFloat = 15
    static let orderID: CGFloat = 26
    static let stageTitle: CGFloat = 15
    static let orderIdentityText = Color(red: 0.08, green: 0.28, blue: 0.22)
    static let stageEmerald = Color(red: 0.16, green: 0.58, blue: 0.39)
}

enum AssistantProgressSegmentState: Equatable {
    case completed
    case active
    case pending
}

// 每个阶段反映自身事实：不同工厂单可分批推进。
/// 根据阶段自身的完成数返回未开始、部分完成或完成状态。
/// - Parameters:
///   - completedCount: 该阶段已完成的工厂单数量。
///   - totalCount: 该阶段工厂单总数。
func assistantProgressSegmentState(completedCount: Int, totalCount: Int) -> AssistantProgressSegmentState {
    guard totalCount > 0, completedCount > 0 else { return .pending }
    return completedCount >= totalCount ? .completed : .active
}

struct AssistantView: View {
    @ObservedObject var model: AppModel
    @Environment(\.accessibilityReduceMotion) private var accessibilityReduceMotion
    @StateObject private var speech = SpeechInputController()
    @StateObject private var pushToTalkShortcut = PushToTalkShortcutMonitor()
    @State private var showCommandHints = false
    @State private var commandHintsTransitionTask: Task<Void, Never>?
    @State private var commandHintsAnchorHovering = false
    @State private var commandHintsPanelHovering = false
    @State private var commandHintsHoverGeneration = 0

    var body: some View {
        VStack(spacing: 18) {
            commandStrip
            orderStatusBoard
                .frame(maxWidth: .infinity, maxHeight: .infinity, alignment: .top)
            if showsAssistantWorkspace {
                HStack(alignment: .top, spacing: 16) {
                    workspaceCard.frame(maxWidth: .infinity)
                    if model.assistantPendingApproval {
                        approvalCard.frame(width: 320)
                    }
                }
            }
        }
        .padding(.horizontal, AppLayout.pageHorizontalPadding)
        .padding(.vertical, AppLayout.pageVerticalPadding)
        .frame(maxWidth: AppLayout.pageContentMaxWidth)
        .frame(maxWidth: .infinity, alignment: .top)
        .appPageFrame()
        .onChange(of: speech.transcript) { _, value in
            if !value.isEmpty { model.assistantInput = canonicalSpeechCommand(value) }
        }
        .onAppear {
            model.startOrderDashboard()
            pushToTalkShortcut.install(
                onPress: { speech.beginPushToTalk() },
                onRelease: { finishPushToTalk() }
            )
        }
        .onDisappear {
            commandHintsTransitionTask?.cancel()
            commandHintsAnchorHovering = false
            commandHintsPanelHovering = false
            showCommandHints = false
            pushToTalkShortcut.uninstall()
            speech.stop()
        }
    }

    private var commandStrip: some View {
        AppSurfaceCard(padding: 0) {
            VStack(spacing: 0) {
                HStack(spacing: 12) {
                    Image(systemName: "sparkles")
                        .font(.system(size: 18, weight: .semibold))
                        .foregroundColor(AppPalette.accent)
                        .frame(width: 38, height: 38)
                        .background(AppPalette.accent.opacity(0.10))
                        .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                    TextField("说或输入：查找订单、查询库存、生成 Traveler…", text: $model.assistantInput)
                        .textFieldStyle(.plain)
                        .font(.system(size: 16))
                        .padding(.horizontal, 14)
                        .frame(height: 46)
                        .glassEffect(.clear, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .onSubmit { model.runAssistantCommand() }
                        .onHover { hovering in
                            if hovering { beginCommandHintsAnchorHover() }
                            else { endCommandHintsAnchorHover() }
                        }
                        .popover(isPresented: $showCommandHints, arrowEdge: .bottom) {
                            AssistantCommandHintsContent()
                                .onHover { hovering in
                                    if hovering { beginCommandHintsPanelHover() }
                                    else { endCommandHintsPanelHover() }
                                }
                        }
                    Image(systemName: speech.isHolding ? "waveform.circle.fill" : "mic.fill")
                        .font(.system(size: 17, weight: .semibold))
                        .foregroundColor(speech.isHolding ? AppPalette.danger : AppPalette.accent)
                        .frame(width: 46, height: 46)
                        .background(AppPalette.accent.opacity(0.10))
                        .clipShape(RoundedRectangle(cornerRadius: 10, style: .continuous))
                        .contentShape(Rectangle())
                        .gesture(
                            DragGesture(minimumDistance: 0)
                                .onChanged { _ in speech.beginPushToTalk() }
                                .onEnded { _ in finishPushToTalk() }
                        )
                        .help("按住说话，松开执行（⌥Space）")
                    Button("执行") { model.runAssistantCommand() }
                        .buttonStyle(.glassProminent)
                        .appActionButton(minWidth: 88)
                        .disabled(model.assistantInput.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                    AppStatusBadge(
                        text: model.assistantRunning ? "执行中" : "本地优先",
                        kind: model.assistantRunning ? .info : .success
                    )
                }
                .padding(16)

                Divider()

                currentOperationSummary
            }
        }
    }

    private var orderStatusBoard: some View {
        AppSurfaceCard(padding: 0) {
            VStack(spacing: 0) {
                HStack(spacing: 0) {
                    assistantMetric("总订单数", value: effectiveOrders.count, symbol: "square.stack.3d.up", color: .primary)
                    Divider().frame(height: 54)
                    assistantMetric("本月已完成", value: monthlyCompletedCount, symbol: "checkmark.circle", color: AppPalette.success)
                    Divider().frame(height: 54)
                    assistantMetric("正在进行", value: ongoingOrders.count, symbol: "waveform.path.ecg", color: AppPalette.accent)
                }
                .frame(maxWidth: .infinity, alignment: .center)
                .padding(.vertical, 6)

                Divider()

                Group {
                    if ongoingOrders.isEmpty {
                        VStack(spacing: 8) {
                            Image(systemName: "checkmark.circle.fill")
                                .font(.system(size: 30))
                                .foregroundColor(AppPalette.success)
                            Text("当前没有进行中的订单")
                                .font(.system(size: 18, weight: .semibold))
                        }
                        .frame(maxWidth: .infinity, minHeight: 170)
                    } else {
                        ScrollView(.vertical) {
                            LazyVStack(spacing: 12) {
                                ForEach(ongoingOrders) { item in
                                    assistantOrderCard(item)
                                }
                            }
                            .padding(.horizontal, 20)
                            .padding(.vertical, 16)
                        }
                        .frame(maxHeight: .infinity)
                        .scrollIndicators(.automatic)
                    }
                }
            }
        }
    }

    /// 构造助手看板的彩色统计指标。
    /// - Parameters:
    ///   - title: 界面或操作记录的标题。
    ///   - value: 统计指标的数量。
    ///   - symbol: 系统图标名称。
    ///   - color: 界面使用的强调颜色。
    private func assistantMetric(_ title: String, value: Int, symbol: String, color: Color) -> some View {
        HStack(alignment: .top, spacing: 8) {
            Image(systemName: symbol)
                .font(.system(size: 17, weight: .semibold))
                .foregroundColor(color)
                .frame(width: 17, height: 18)
                .padding(.top, 1)
            VStack(alignment: .center, spacing: 5) {
                Text(title)
                    .font(.system(size: AssistantDashboardTypography.metricLabel, weight: .medium))
                    .foregroundColor(.secondary)
                    .lineLimit(1)
                Text("\(value)")
                    .font(.system(size: AssistantDashboardTypography.metricValue, weight: .semibold, design: .rounded).monospacedDigit())
                    .foregroundColor(color)
            }
        }
        .frame(width: 140, height: 78, alignment: .center)
        .padding(.horizontal, 16)
    }

    private var currentOperationSummary: some View {
        let operation = currentAssistantOperation
        return HStack(spacing: 10) {
                Image(systemName: operation.running ? "arrow.triangle.2.circlepath.circle.fill" : "checkmark.circle.fill")
                    .font(.system(size: 19))
                    .foregroundColor(operation.running ? AppPalette.accent : AppPalette.success)
                    .symbolEffect(.rotate, options: .repeating, isActive: operation.running)
                Text(operation.title)
                    .font(.system(size: 17, weight: .medium))
                    .lineLimit(1)
                    .help(operation.title)
                Spacer(minLength: 0)
        }
        .padding(.horizontal, 22)
        .frame(maxWidth: .infinity, minHeight: 48, maxHeight: 48, alignment: .leading)
        .overlay(alignment: .bottom) {
                if operation.running {
                    ProgressView()
                        .progressViewStyle(.linear)
                        .tint(AppPalette.accent)
                        .frame(maxWidth: .infinity)
                }
        }
    }

    /// 显示订单阶段、日期、材料和进入订单中心的入口。
    /// - Parameters:
    ///   - item: 订单看板记录。
    private func assistantOrderCard(_ item: OrderDashboardItem) -> some View {
        OrderDashboardClickContainer(
            onSingleClick: {},
            onDoubleClick: { openOrderCenter(item.orderId) }
        ) {
            HStack(alignment: .center, spacing: 24) {
                Text(item.orderId)
                    .font(.system(size: AssistantDashboardTypography.orderID, weight: .semibold).monospacedDigit())
                    .foregroundColor(AssistantDashboardTypography.orderIdentityText)
                    .lineLimit(1)
                    .minimumScaleFactor(0.65)
                    .help(item.orderId)
                    .frame(width: 176, alignment: .center)
                Divider()
                    .frame(height: 62)
                    .opacity(0.55)
                assistantProgressRail(item)
            }
            .padding(.horizontal, 24)
            .padding(.vertical, 16)
            .frame(maxWidth: .infinity, alignment: .leading)
            .background {
                RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius, style: .continuous)
                    .fill(.regularMaterial)
                    .overlay {
                        RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius, style: .continuous)
                            .fill(LinearGradient(
                                colors: [Color.white.opacity(0.72), Color(red: 0.90, green: 0.97, blue: 0.94).opacity(0.56)],
                                startPoint: .topLeading,
                                endPoint: .bottomTrailing
                            ))
                    }
                    .overlay {
                        RoundedRectangle(cornerRadius: AppLayout.cardCornerRadius, style: .continuous)
                            .strokeBorder(Color.white.opacity(0.72), lineWidth: 1)
                    }
                    .shadow(color: AssistantDashboardTypography.orderIdentityText.opacity(0.07), radius: 8, y: 4)
            }
            .contentShape(Rectangle())
        }
        .frame(maxWidth: .infinity)
    }

    /// 按各阶段独立事实显示订单进度连接线及节点。
    /// - Parameters:
    ///   - item: 订单看板记录。
    private func assistantProgressRail(_ item: OrderDashboardItem) -> some View {
        let stages: [(title: String, completedCount: Int, totalCount: Int, value: String, fallbackSymbol: String)] = [
            ("拆单", item.factoryCount, item.factoryCount, item.factoryCount > 0 ? "\(item.factoryCount)/\(item.factoryCount)" : "—", "arrow.triangle.branch"),
            ("优化", item.optimizedCount, item.factoryCount, assistantProgressValue(item.optimizationProgress), "square.3.layers.3d"),
            ("生产", item.producedCount, item.factoryCount, assistantProgressValue(item.productionProgress), "scissors"),
            ("出货", item.shippedCount, item.factoryCount, assistantProgressValue(item.outboundProgress), "truck.box"),
        ]
        return GeometryReader { geometry in
            let columnWidth = geometry.size.width / CGFloat(stages.count)
            let iconDiameter: CGFloat = 56
            let centerY: CGFloat = 52
            let iconRadius = iconDiameter / 2
            let connectorGap: CGFloat = 10
            ZStack(alignment: .topLeading) {
                ForEach(Array(stages.enumerated()), id: \.offset) { index, stage in
                    let centerX = columnWidth * (CGFloat(index) + 0.5)
                    let startX: CGFloat = index == 0
                        ? 0
                        : centerX - columnWidth + iconRadius + connectorGap
                    let endX = max(startX, centerX - iconRadius - connectorGap)
                    let segmentState = assistantProgressSegmentState(
                        completedCount: stage.completedCount, totalCount: stage.totalCount
                    )
                    let connector = Path { path in
                        path.move(to: CGPoint(x: startX, y: centerY))
                        path.addLine(to: CGPoint(x: endX, y: centerY))
                    }

                    Group {
                        switch segmentState {
                        case .completed:
                            connector.stroke(
                                AssistantDashboardTypography.stageEmerald.opacity(0.92),
                                style: StrokeStyle(lineWidth: 2.5, lineCap: .round)
                            )
                        case .active:
                            TimelineView(.animation(minimumInterval: 1.0 / 20.0, paused: accessibilityReduceMotion)) { context in
                                let elapsed = context.date.timeIntervalSinceReferenceDate
                                let dashPhase = accessibilityReduceMotion
                                    ? CGFloat.zero
                                    : -CGFloat(elapsed.truncatingRemainder(dividingBy: 1.2) / 1.2) * 16
                                connector.stroke(
                                    AssistantDashboardTypography.stageEmerald.opacity(0.92),
                                    style: StrokeStyle(
                                        lineWidth: 2.5,
                                        lineCap: .round,
                                        dash: [7, 9],
                                        dashPhase: dashPhase
                                    )
                                )
                            }
                        case .pending:
                            connector.stroke(
                                AppPalette.separator.opacity(0.90),
                                style: StrokeStyle(lineWidth: 2.5, lineCap: .round)
                            )
                        }
                    }
                    .allowsHitTesting(false)
                }

                HStack(spacing: 0) {
                    ForEach(Array(stages.enumerated()), id: \.offset) { _, stage in
                        let state = assistantProgressSegmentState(
                            completedCount: stage.completedCount, totalCount: stage.totalCount
                        )
                        VStack(spacing: 8) {
                            Text(stage.title)
                                .font(.system(size: AssistantDashboardTypography.stageTitle, weight: .semibold))
                                .frame(height: 16)
                            assistantStageIcon(
                                completed: state == .completed,
                                current: state == .active,
                                fallbackSymbol: stage.fallbackSymbol
                            )
                        }
                        .frame(width: columnWidth, height: 80, alignment: .top)
                        .accessibilityElement(children: .ignore)
                        .accessibilityLabel("\(stage.title) \(stage.value)")
                    }
                }
            }
        }
        .frame(height: 80)
    }

    /// 根据完成和当前状态绘制阶段节点图标。
    /// - Parameters:
    ///   - completed: 该节点是否已经完成。
    ///   - current: 该节点是否为当前阶段。
    ///   - fallbackSymbol: 未完成节点使用的系统图标名称。
    private func assistantStageIcon(
        completed: Bool,
        current: Bool,
        fallbackSymbol: String
    ) -> some View {
        let iconColor = completed || current ? AssistantDashboardTypography.stageEmerald : Color.secondary.opacity(0.62)
        let shape = RoundedRectangle(cornerRadius: 16, style: .continuous)
        return Image(systemName: fallbackSymbol)
            .font(.system(size: 28, weight: .medium))
            .symbolRenderingMode(.monochrome)
            .foregroundStyle(iconColor)
            .contentTransition(.symbolEffect(.replace))
            .frame(width: 56, height: 56)
            .background {
                shape.fill(LinearGradient(
                    colors: [
                        Color.white.opacity(0.88),
                        completed ? iconColor.opacity(0.18) : Color.white.opacity(0.38),
                    ],
                    startPoint: .topLeading,
                    endPoint: .bottomTrailing
                ))
            }
            .overlay {
                shape.strokeBorder(
                    completed || current ? iconColor.opacity(0.28) : AppPalette.separator,
                    lineWidth: 1
                )
                shape.inset(by: 1).strokeBorder(Color.white.opacity(0.72), lineWidth: 1)
            }
            .shadow(color: iconColor.opacity(completed || current ? 0.10 : 0.04), radius: 4, y: 2)
    }

    /// 将缺失或占位进度文本转换为统一的简洁显示。
    /// - Parameters:
    ///   - value: 后端返回的阶段进度文字。
    private func assistantProgressValue(_ value: String) -> String {
        value.replacingOccurrences(of: " ", with: "")
    }

    /// 筛选未完成订单，并按最近拆单时间和订单号倒序显示。
    private var ongoingOrders: [OrderDashboardItem] {
        effectiveOrders
            .filter { !orderDashboardIsCompleted($0.stage) }
            .sorted { ($0.latestSplitTime, $0.orderId) > ($1.latestSplitTime, $1.orderId) }
    }

    /// 统计本月完成出货的有效订单数量。
    private var monthlyCompletedCount: Int {
        effectiveOrders.filter {
            $0.stage == "已出货" && dashboardTimestamp($0.completedAt, isInSameMonthAs: Date.now)
        }.count
    }

    /// 排除临时订单及数据异常项，取得助手看板使用的订单。
    private var effectiveOrders: [OrderDashboardItem] {
        model.dashboardOrders.filter { $0.orderType != "temporary" && $0.stage != "数据异常" }
    }

    /// 判断是否有运行任务、审批或结果需要显示助手工作区。
    private var showsAssistantWorkspace: Bool {
        model.assistantRunning || model.assistantPendingApproval ||
            model.assistantOutput != "输入或说出一条指令。" ||
            !model.assistantStockRows.isEmpty || model.assistantOrderPreview != nil ||
            !model.assistantOrderList.isEmpty
    }

    /// 在紧凑的单行状态栏中显示当前后端步骤。
    private var currentAssistantOperation: (title: String, running: Bool) {
        if model.assistantRunning {
            let status = displayedTask?.status.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
            return (status.isEmpty ? (displayedTask?.text ?? "正在执行助手命令") : status, true)
        }
        if model.inventoryRunning {
            return (dashboardMessageDetail(model.dashboardInventoryOperationStatus), true)
        }
        if model.orderRunning || dashboardStatusIsInProgress(model.dashboardSyncStatus) {
            let status = [model.dashboardServerStatus, model.dashboardAimesStatus, model.dashboardSyncStatus]
                .first(where: dashboardStatusIsInProgress)
            return (status.map(dashboardMessageDetail) ?? "正在处理订单数据", true)
        }
        return ("操作完毕", false)
    }

    /// 根据订单阶段和待优化数量生成当前业务进度说明。
    /// - Parameters:
    ///   - item: 订单看板记录。
    private func assistantStageSummary(_ item: OrderDashboardItem) -> String {
        switch item.stage {
        case "已拆单待优化": return "拆单完成，等待 AICNC 优化"
        case "部分优化": return "仍有 \(max(0, item.factoryCount - item.optimizedCount)) 个工厂单待优化"
        case "已优化": return "全部工厂单优化完成，等待生产"
        case "部分生产": return "正在生产"
        case "已生产": return "生产完成，等待安排出货"
        case "部分出货", "部分生产，部分出货": return "正在分批出货"
        case "待确认": return "工厂单归属等待确认"
        case "数据异常": return item.validationMessage.isEmpty ? "订单数据需要检查" : item.validationMessage
        default: return item.stage
        }
    }

    /// 组合最近拆单和优化完成时间的摘要。
    /// - Parameters:
    ///   - item: 订单看板记录。
    private func assistantOrderDates(_ item: OrderDashboardItem) -> String {
        var values: [String] = []
        if !item.latestSplitTime.isEmpty {
            values.append("最近拆单 \(assistantDate(item.latestSplitTime))")
        }
        if !item.optimizationCompletedAt.isEmpty {
            values.append("完成优化 \(assistantDate(item.optimizationCompletedAt))")
        }
        return values.isEmpty ? "业务时间待同步" : values.joined(separator: "  ·  ")
    }

    /// 将业务时间显示为月日时分，解析失败时保留可读原文。
    /// - Parameters:
    ///   - value: 待解析或显示的业务日期时间字符串。
    private func assistantDate(_ value: String) -> String {
        guard let date = dashboardBusinessDate(value) else { return appDisplayTimestamp(value) }
        return date.formatted(.dateTime.month().day().hour().minute())
    }

    /// 将订单阶段转换为状态徽章的颜色类型。
    /// - Parameters:
    ///   - stage: 订单或操作的当前阶段标识。
    private func assistantStageKind(_ stage: String) -> AppStatusBadge.Kind {
        switch stage {
        case "数据异常": return .danger
        case "待确认", "部分优化": return .warning
        case "已生产", "已优化": return .success
        default: return .info
        }
    }

    /// 切换到订单中心，并可定位指定订单。
    /// - Parameters:
    ///   - orderID: 目标业务订单号。
    private func openOrderCenter(_ orderID: String?) {
        model.requestedOrderCenterOrderID = orderID ?? ""
        NotificationCenter.default.post(name: .ppOpenOrderCenter, object: nil)
    }

    private var commandCard: some View {
        AppSurfaceCard(padding: 24) {
            VStack(alignment: .leading, spacing: 14) {
                Text("工作流入口")
                    .font(.caption.weight(.bold))
                    .foregroundColor(.secondary)
                    .textCase(.uppercase)
                Text("把下一步工作交给助手")
                    .font(.system(size: 30, weight: .semibold))
                Text("常用命令在本机直接执行；只有模糊表达才会交给 Agent 解析。")
                    .foregroundColor(.secondary)

                HStack(spacing: 8) {
                    TextField("例如：查找 PP0063，或查询材料库存", text: $model.assistantInput)
                        .textFieldStyle(.plain)
                        .padding(.horizontal, 12)
                        .frame(height: AppLayout.controlHeight)
                        .background(AppPalette.surface)
                        .clipShape(RoundedRectangle(cornerRadius: 8))
                        .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))
                        .onSubmit { model.runAssistantCommand() }
                        .onHover { hovering in
                            if hovering { beginCommandHintsAnchorHover() }
                            else { endCommandHintsAnchorHover() }
                        }
                        .popover(isPresented: $showCommandHints, arrowEdge: .bottom) {
                            AssistantCommandHintsContent()
                                .onHover { hovering in
                                    if hovering { beginCommandHintsPanelHover() }
                                    else { endCommandHintsPanelHover() }
                                }
                        }
                    Image(systemName: speech.isHolding ? "waveform.circle.fill" : "mic.fill")
                        .foregroundColor(speech.isHolding ? AppPalette.danger : AppPalette.accent)
                        .frame(width: 44, height: 44)
                        .glassEffect(.clear, in: RoundedRectangle(cornerRadius: 14, style: .continuous))
                        .contentShape(Rectangle())
                        .gesture(
                            DragGesture(minimumDistance: 0)
                                .onChanged { _ in speech.beginPushToTalk() }
                                .onEnded { _ in finishPushToTalk() }
                        )
                        .help("按住说话，松开执行（⌥Space）")
                    Button("执行") { model.runAssistantCommand() }
                        .buttonStyle(.glassProminent)
                        .appActionButton(minWidth: 88)
                        .disabled(model.assistantInput.trimmingCharacters(in: .whitespacesAndNewlines).isEmpty)
                }

                HStack(spacing: 8) {
                    ForEach(Array(assistantCommandHints.prefix(3)), id: \.self) { hint in
                        Button(hint.components(separatedBy: "  ·  ").first ?? hint) {
                            model.assistantInput = hint.components(separatedBy: "  ·  ").first ?? hint
                        }
                        .buttonStyle(.plain)
                        .font(.caption)
                        .foregroundColor(.secondary)
                        .padding(.horizontal, 10)
                        .frame(minHeight: 30)
                        .background(AppPalette.subtleSurface)
                        .clipShape(Capsule())
                    }
                    Spacer()
                }

                HStack(spacing: 0) {
                    flowStep("01", "理解指令", active: model.assistantRunning)
                    flowStep("02", "读取与校验", active: displayedTask?.status == "执行中")
                    flowStep("03", "等待确认", active: model.assistantPendingApproval)
                    flowStep("04", "安全写入", active: model.assistantWriteInProgress)
                }
                .overlay(RoundedRectangle(cornerRadius: 8).stroke(AppPalette.separator))

                if !speech.errorMessage.isEmpty {
                    Label(speech.errorMessage, systemImage: "exclamationmark.triangle.fill")
                        .font(.caption).foregroundColor(AppPalette.danger)
                }
            }
        }
    }

    private var workspaceCard: some View {
        AppSurfaceCard(padding: 0) {
            VStack(spacing: 0) {
                HStack(spacing: 10) {
                    Image(systemName: workspaceIcon).foregroundColor(AppPalette.accent)
                    Text(workspaceTitle).fontWeight(.semibold)
                    Spacer()
                    if let task = displayedTask {
                        AppStatusBadge(text: task.status, kind: badgeKind(task.status))
                        if assistantTaskShowsHeaderCancel(task.status) {
                            Button("取消") { model.cancelAssistantTask(task.id) }
                                .appActionButton(minWidth: 64)
                                .disabled(task.status == "正在写入")
                        }
                    }
                }
                .padding(.horizontal, 16)
                .frame(height: 54)
                .overlay(Divider(), alignment: .bottom)

                Group {
                    if !model.assistantStockRows.isEmpty {
                        AssistantStockComparisonView(
                            orderId: model.assistantStockOrderId,
                            traveler: model.assistantStockTraveler,
                            rows: model.assistantStockRows
                        )
                    } else if let result = model.assistantOrderPreview {
                        AssistantOrderPreviewView(result: result)
                    } else if !model.assistantOrderList.isEmpty {
                        AssistantOrderListView(orders: model.assistantOrderList)
                    } else {
                        Text(model.assistantOutput)
                            .frame(maxWidth: .infinity, alignment: .leading)
                            .textSelection(.enabled)
                            .padding(16)
                    }
                }
                .frame(minHeight: 260, maxHeight: 460, alignment: .top)
            }
        }
    }

    private var approvalCard: some View {
        AppSurfaceCard {
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Text("等待确认").font(.headline)
                    Spacer()
                    AppStatusBadge(
                        text: model.assistantPendingApproval ? "需要处理" : "当前无项目",
                        kind: model.assistantPendingApproval ? .warning : .neutral
                    )
                }
                if model.assistantPendingApproval {
                    Text(displayedTask?.text ?? "写入操作")
                        .font(.title3.monospaced()).fontWeight(.semibold).lineLimit(2)
                    Text("确认后将写入真实文件；真实写入开始后不可取消。")
                        .font(.caption).foregroundColor(.secondary)
                    HStack {
                        Button("取消") {
                            if let id = model.assistantActiveTaskID { model.cancelAssistantTask(id) }
                        }
                        .appActionButton(minWidth: 72)
                        Button("确认执行") { model.runAssistantCommand(approved: true) }
                            .buttonStyle(.glassProminent)
                            .appActionButton()
                    }
                } else {
                    Text("需要写文件或库存时，确认卡会固定出现在这里。")
                        .font(.caption).foregroundColor(.secondary)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    private var queueCard: some View {
        AppSurfaceCard {
            VStack(alignment: .leading, spacing: 12) {
                HStack {
                    Text("任务队列").font(.headline)
                    Spacer()
                    Text("\(model.assistantTasks.count)").font(.headline.monospacedDigit())
                }
                if model.assistantTasks.isEmpty {
                    Text("暂无任务").font(.caption).foregroundColor(.secondary)
                } else {
                    ForEach(model.assistantTasks.suffix(3)) { task in
                        HStack(spacing: 9) {
                            Circle().fill(taskStatusColor(task.status)).frame(width: 7, height: 7)
                            Text(task.text).lineLimit(1)
                            Spacer()
                            Text(task.status).font(.caption).foregroundColor(.secondary)
                        }
                        .font(.caption)
                    }
                }
                if queuedTaskCount > 0 {
                    Text("另有 \(queuedTaskCount) 项排队")
                        .font(.caption).foregroundColor(AppPalette.accent)
                }
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    private var usageCard: some View {
        AppSurfaceCard {
            VStack(alignment: .leading, spacing: 8) {
                Text("运行状态").font(.headline)
                statusLine("本地命令", "优先")
                statusLine("任务模式", "串行")
                statusLine("Agent 用量", model.assistantUsageSummary)
                Text(model.assistantTokenSummary)
                    .font(.caption2).foregroundColor(.secondary).lineLimit(2)
            }
            .frame(maxWidth: .infinity, alignment: .leading)
        }
    }

    /// 构造助手指令流程中带序号和活动状态的步骤。
    /// - Parameters:
    ///   - number: 流程步骤的显示序号。
    ///   - title: 界面或操作记录的标题。
    ///   - active: 该流程步骤是否处于活动状态。
    private func flowStep(_ number: String, _ title: String, active: Bool) -> some View {
        VStack(alignment: .leading, spacing: 5) {
            Text(number).font(.caption2.monospacedDigit().weight(.bold))
            Text(title).font(.caption.weight(.semibold)).lineLimit(1)
        }
        .foregroundColor(active ? AppPalette.accent : .secondary)
        .padding(12)
        .frame(maxWidth: .infinity, alignment: .leading)
        .background(active ? AppPalette.accent.opacity(0.09) : Color.clear)
    }

    /// 构造助手状态区的标签和值。
    /// - Parameters:
    ///   - label: 阶段、项目或信息行的显示名称。
    ///   - value: 需要显示的数值或状态文字。
    private func statusLine(_ label: String, _ value: String) -> some View {
        HStack {
            Text(label).foregroundColor(.secondary)
            Spacer()
            Text(value).fontWeight(.semibold).lineLimit(1)
        }
        .font(.caption)
    }

    /// 将助手任务状态转换为徽章类型。
    /// - Parameters:
    ///   - status: 业务状态文字或状态代码。
    private func badgeKind(_ status: String) -> AppStatusBadge.Kind {
        switch status {
        case "已完成": return .success
        case "失败": return .danger
        case "等待确认", "正在写入": return .warning
        default: return .info
        }
    }

    /// 结束语音输入，将规范化转写填入并提交助手命令。
    /// 无参数。
    private func finishPushToTalk() {
        speech.endPushToTalk { text in
            model.assistantInput = canonicalSpeechCommand(text)
            model.runAssistantCommand()
        }
    }

    /// 进入命令提示入口时取消关闭任务并延迟显示提示面板。
    /// 无参数。
    private func beginCommandHintsAnchorHover() {
        commandHintsAnchorHovering = true
        commandHintsHoverGeneration += 1
        commandHintsTransitionTask?.cancel()
        guard !showCommandHints else { return }
        let generation = commandHintsHoverGeneration
        commandHintsTransitionTask = Task { @MainActor in
            try? await Task.sleep(for: .seconds(dashboardMessageHoverDelay))
            guard !Task.isCancelled,
                  generation == commandHintsHoverGeneration,
                  commandHintsAnchorHovering || commandHintsPanelHovering else { return }
            showCommandHints = true
        }
    }

    /// 离开命令提示入口并安排延迟关闭。
    /// 无参数。
    private func endCommandHintsAnchorHover() {
        commandHintsAnchorHovering = false
        commandHintsHoverGeneration += 1
        scheduleCommandHintsClose()
    }

    /// 进入提示面板时取消关闭任务，维持面板显示。
    /// 无参数。
    private func beginCommandHintsPanelHover() {
        commandHintsPanelHovering = true
        commandHintsHoverGeneration += 1
        commandHintsTransitionTask?.cancel()
    }

    /// 离开提示面板后安排延迟关闭。
    /// 无参数。
    private func endCommandHintsPanelHover() {
        commandHintsPanelHovering = false
        commandHintsHoverGeneration += 1
        scheduleCommandHintsClose()
    }

    /// 在入口和面板均未悬停时延迟关闭命令提示。
    /// 无参数。
    private func scheduleCommandHintsClose() {
        commandHintsTransitionTask?.cancel()
        let generation = commandHintsHoverGeneration
        commandHintsTransitionTask = Task { @MainActor in
            try? await Task.sleep(for: .seconds(dashboardMessageHoverCloseGrace))
            guard !Task.isCancelled,
                  generation == commandHintsHoverGeneration,
                  !commandHintsAnchorHovering,
                  !commandHintsPanelHovering else { return }
            showCommandHints = false
        }
    }

    /// 选择当前活动或适合展示的最近助手任务。
    private var displayedTask: AssistantTaskItem? {
        if let id = model.assistantActiveTaskID,
           let active = model.assistantTasks.first(where: { $0.id == id }) {
            return active
        }
        return model.assistantTasks.last
    }

    /// 统计仍在排队的助手任务数量。
    private var queuedTaskCount: Int {
        model.assistantTasks.filter { $0.status == "排队中" && $0.id != displayedTask?.id }.count
    }

    /// 根据助手运行、审批和结果状态生成工作区标题。
    private var workspaceTitle: String {
        if !model.assistantStockRows.isEmpty { return "库存比对" }
        if model.assistantOrderPreview != nil { return "订单预览" }
        if !model.assistantOrderList.isEmpty { return "订单列表" }
        if model.assistantRunning { return "正在执行" }
        return "执行结果"
    }

    /// 根据助手工作区状态选择标题图标。
    private var workspaceIcon: String {
        if !model.assistantStockRows.isEmpty { return "shippingbox.and.arrow.backward" }
        if model.assistantOrderPreview != nil { return "doc.text.magnifyingglass" }
        if !model.assistantOrderList.isEmpty { return "folder" }
        if model.assistantRunning { return "progress.indicator" }
        return "text.bubble"
    }

    /// 按助手任务状态返回列表标识颜色。
    /// - Parameters:
    ///   - status: 业务状态文字或状态代码。
    private func taskStatusColor(_ status: String) -> Color {
        switch status {
        case "已完成": return AppPalette.success
        case "失败": return AppPalette.danger
        case "等待确认", "正在写入": return AppPalette.warning
        default: return AppPalette.accent
        }
    }
}
