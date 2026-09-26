import Foundation
import Darwin

struct OperationLogEntry: Identifiable, Equatable {
    let id: UUID
    let timestamp: Date
    let operation: String
    let event: String
    let component: String
    let operationID: String
    let sessionID: String
    let safeDetails: [String: String]
    let durationSeconds: Double?

    var isFailure: Bool { event.hasSuffix(".failed") || event == "operation.failed" }

    /// 建立具有身份、发生时间和操作说明的日志条目。
    /// - Parameters:
    ///   - id: 记录或请求的唯一标识。
    ///   - timestamp: 操作日志发生时间。
    ///   - operation: 用于错误提示或日志显示的业务操作名称。
    init(
        id: UUID = UUID(), timestamp: Date, operation: String,
        event: String = "", component: String = "", operationID: String = "", sessionID: String = "",
        safeDetails: [String: String] = [:], durationSeconds: Double? = nil
    ) {
        self.id = id
        self.timestamp = timestamp
        self.operation = operation
        self.event = event
        self.component = component
        self.operationID = operationID
        self.sessionID = sessionID
        self.safeDetails = safeDetails
        self.durationSeconds = durationSeconds
    }

    /// 将日志发生时间格式化为中文界面使用的完整日期时间。
    var displayTime: String {
        OperationLogEntry.displayFormatter.string(from: timestamp)
    }

    private static let displayFormatter: DateFormatter = {
        let formatter = DateFormatter()
        formatter.locale = Locale(identifier: "zh_CN")
        formatter.calendar = Calendar(identifier: .gregorian)
        formatter.dateFormat = "yyyy-MM-dd HH:mm:ss"
        return formatter
    }()
}

struct OperationLogReadResult {
    let entries: [OperationLogEntry]
    let invalidLineCount: Int
    let error: String?
}

struct OperationLogTrimResult: Equatable {
    let removedEntries: Int
    let retainedEntries: Int
    let byteCount: Int64
}

enum OperationLogMaintenanceError: LocalizedError {
    case invalidLine(Int)
    case logChangedDuringCleanup

    /// 提供日志损坏或清理期间文件变化的中文错误说明。
    var errorDescription: String? {
        switch self {
        case .invalidLine(let line):
            return "第 \(line) 行不是有效的操作日志，已停止清理。"
        case .logChangedDuringCleanup:
            return "日志在清理期间发生变化，请停止正在运行的任务后重试。"
        }
    }
}

enum OperationLogReader {
    /// 读取逐行 JSON 操作日志，忽略无法解析的记录。
    /// - Parameters:
    ///   - url: 待读取或清理的日志文件地址。
    static func entries(from url: URL) -> [OperationLogEntry] {
        read(from: url).entries
    }

    /// 读取日志文件并统计无效行；url 为日志文件地址，返回有效记录、错误数和文件错误。
    static func read(from url: URL) -> OperationLogReadResult {
        guard FileManager.default.fileExists(atPath: url.path) else {
            return OperationLogReadResult(entries: [], invalidLineCount: 0, error: nil)
        }
        let data: Data
        do {
            data = try Data(contentsOf: url)
        } catch {
            return OperationLogReadResult(entries: [], invalidLineCount: 0, error: "操作日志读取失败，请检查文件权限后重试。")
        }
        guard let text = String(data: data, encoding: .utf8) else {
            return OperationLogReadResult(entries: [], invalidLineCount: 0, error: "操作日志编码无效，无法按 UTF-8 读取。")
        }
        var entries: [OperationLogEntry] = []
        var invalidLineCount = 0
        for line in text.split(whereSeparator: \.isNewline) {
            if let entry = parse(line: String(line)) {
                entries.append(entry)
            } else {
                invalidLineCount += 1
            }
        }
        return OperationLogReadResult(entries: entries, invalidLineCount: invalidLineCount, error: nil)
    }

    /// 按失败状态和关键词筛选日志；entries 为候选记录，failuresOnly 控制是否仅保留失败，search 为搜索词。
    static func filtered(_ entries: [OperationLogEntry], failuresOnly: Bool, search: String) -> [OperationLogEntry] {
        let term = search.trimmingCharacters(in: .whitespacesAndNewlines)
        return entries.filter { entry in
            (!failuresOnly || entry.isFailure) &&
            (term.isEmpty || entry.operation.localizedCaseInsensitiveContains(term) ||
             (entry.safeDetails["order_id"] ?? "").localizedCaseInsensitiveContains(term) ||
             (entry.safeDetails["factory_order"] ?? "").localizedCaseInsensitiveContains(term))
        }
    }

    /// 汇总同一操作的脱敏诊断文本；entry 为选中记录，entries 为当前日志集合。
    static func diagnosticText(for entry: OperationLogEntry, in entries: [OperationLogEntry]) -> String {
        let related = entry.operationID.isEmpty ? [entry] : entries.filter {
            $0.operationID == entry.operationID && $0.sessionID == entry.sessionID
        }
        return related.map { item in
            var lines = ["\(item.displayTime)  \(OperationLogWriter.redactText(item.operation))"]
            lines.append("  事件: \(OperationLogWriter.redactText(item.event))")
            lines.append("  来源: \(OperationLogWriter.redactText(item.component))")
            if !item.operationID.isEmpty { lines.append("  操作标识: \(OperationLogWriter.redactText(item.operationID))") }
            if !item.sessionID.isEmpty { lines.append("  会话标识: \(OperationLogWriter.redactText(item.sessionID))") }
            for key in item.safeDetails.keys.sorted() {
                lines.append("  \(key): \(OperationLogWriter.redactText(item.safeDetails[key] ?? ""))")
            }
            return lines.joined(separator: "\n")
        }.joined(separator: "\n\n")
    }

    /// 解析一条日志的时间和业务说明；内容无效时返回空值。
    /// - Parameters:
    ///   - line: 一行原始 JSON 日志文本。
    static func parse(line: String) -> OperationLogEntry? {
        guard let data = line.data(using: .utf8),
              let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
              let timestampText = payload["timestamp"] as? String,
              let timestamp = timestamp(from: timestampText) else {
            return nil
        }
        // 旧 AIMES 日志保留动作说明，显示时去掉历史的省略占位提示，不恢复被隐藏的内容。
        let message = (payload["message"] as? String)?
            .replacingOccurrences(of: #"[（(](?:内容|网址(?:参数)?)已省略[）)]"#, with: "", options: .regularExpression)
            .trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
        let event = (payload["event"] as? String)?.trimmingCharacters(in: .whitespacesAndNewlines) ?? ""
        let operation = message.isEmpty ? friendlyEvent(event) : message
        guard !operation.isEmpty else { return nil }
        let details = payload["details"] as? [String: Any] ?? [:]
        let allowedKeys: Set<String> = [
            "action", "order_id", "factory_order", "code", "exception_type", "stack",
            "duration_seconds", "exit_status", "app_version", "app_build", "stage", "error",
            "operation_log_enabled", "enabled_after_change", "retained_entries", "removed_entries",
        ]
        var safeDetails: [String: String] = [:]
        for (key, value) in details where allowedKeys.contains(key) {
            if key == "stack", let frames = value as? [[String: Any]] {
                let locations = frames.prefix(8).compactMap { frame -> String? in
                    guard let module = frame["module"] as? String,
                          let function = frame["function"] as? String,
                          let line = frame["line"] as? Int else { return nil }
                    return "\(module).\(function):\(line)"
                }
                safeDetails[key] = OperationLogWriter.redactText(locations.joined(separator: " → "))
            } else if let scalar = value as? String {
                safeDetails[key] = OperationLogWriter.redactText(String(scalar.prefix(500)))
            } else if let number = value as? NSNumber {
                safeDetails[key] = number.stringValue
            }
        }
        return OperationLogEntry(
            timestamp: timestamp, operation: OperationLogWriter.redactText(operation), event: event,
            component: payload["component"] as? String ?? "",
            operationID: payload["operation_id"] as? String ?? "",
            sessionID: payload["session_id"] as? String ?? "",
            safeDetails: safeDetails,
            durationSeconds: (details["duration_seconds"] as? NSNumber)?.doubleValue
        )
    }

    /// 解析带有或不带小数秒的 ISO 日志时间。
    /// - Parameters:
    ///   - text: 待解析或显示的文本。
    static func timestamp(from text: String) -> Date? {
        if let date = ISO8601DateFormatter.operationLog.date(from: text) { return date }
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime]
        return formatter.date(from: text)
    }

    /// 将日志文件大小转换为适合显示的容量文字。
    /// - Parameters:
    ///   - url: 待读取或清理的日志文件地址。
    static func fileSizeText(from url: URL) -> String {
        let attributes = try? FileManager.default.attributesOfItem(atPath: url.path)
        let bytes = (attributes?[.size] as? NSNumber)?.int64Value ?? 0
        let formatter = ByteCountFormatter()
        formatter.allowedUnits = [.useKB, .useMB, .useGB]
        formatter.countStyle = .file
        return formatter.string(fromByteCount: bytes)
    }

    /// 按自然日保留近期日志；校验所有行及文件并发变化后原子替换文件。
    /// - Parameters:
    ///   - days: 需要保留的自然日天数（包含今天）。
    ///   - url: 待读取或清理的日志文件地址。
    ///   - now: 清理日志使用的参考当前时间。
    ///   - calendar: 用于日期计算的日历。
    static func trim(
        toRecentDays days: Int,
        at url: URL,
        now: Date = Date(),
        calendar: Calendar = .current
    ) throws -> OperationLogTrimResult {
        guard days > 0 else { return OperationLogTrimResult(removedEntries: 0, retainedEntries: 0, byteCount: 0) }
        guard FileManager.default.fileExists(atPath: url.path) else {
            return OperationLogTrimResult(removedEntries: 0, retainedEntries: 0, byteCount: 0)
        }

        let originalAttributes = try FileManager.default.attributesOfItem(atPath: url.path)
        let originalData = try Data(contentsOf: url)
        guard let text = String(data: originalData, encoding: .utf8) else {
            throw OperationLogMaintenanceError.invalidLine(1)
        }

        let localCalendar = calendar
        let todayStart = localCalendar.startOfDay(for: now)
        guard let cutoff = localCalendar.date(byAdding: .day, value: -(days - 1), to: todayStart),
              let tomorrowStart = localCalendar.date(byAdding: .day, value: 1, to: todayStart) else {
            return OperationLogTrimResult(removedEntries: 0, retainedEntries: 0, byteCount: Int64(originalData.count))
        }

        let lines = text.split(whereSeparator: \.isNewline).map(String.init)
        var retainedLines: [String] = []
        retainedLines.reserveCapacity(lines.count)
        for (index, line) in lines.enumerated() {
            guard let data = line.data(using: .utf8),
                  let payload = try? JSONSerialization.jsonObject(with: data) as? [String: Any],
                  let timestampText = payload["timestamp"] as? String,
                  let timestamp = timestamp(from: timestampText) else {
                throw OperationLogMaintenanceError.invalidLine(index + 1)
            }
            if timestamp >= cutoff && timestamp < tomorrowStart {
                retainedLines.append(line)
            }
        }

        let hadTrailingNewline = text.last?.isNewline == true
        var output = retainedLines.joined(separator: "\n")
        if hadTrailingNewline && !retainedLines.isEmpty { output.append("\n") }
        let outputData = Data(output.utf8)

        let latestAttributes = try FileManager.default.attributesOfItem(atPath: url.path)
        let originalSize = (originalAttributes[.size] as? NSNumber)?.int64Value ?? Int64(originalData.count)
        let latestSize = (latestAttributes[.size] as? NSNumber)?.int64Value ?? -1
        let originalModified = originalAttributes[.modificationDate] as? Date
        let latestModified = latestAttributes[.modificationDate] as? Date
        guard originalSize == latestSize && originalModified == latestModified else {
            throw OperationLogMaintenanceError.logChangedDuringCleanup
        }

        let temporaryURL = url
            .deletingLastPathComponent()
            .appendingPathComponent(".operation-log-cleanup-\(UUID().uuidString).tmp")
        var replaced = false
        defer {
            if !replaced { try? FileManager.default.removeItem(at: temporaryURL) }
        }
        try outputData.write(to: temporaryURL, options: .atomic)
        if let permissions = originalAttributes[.posixPermissions] {
            try? FileManager.default.setAttributes([.posixPermissions: permissions], ofItemAtPath: temporaryURL.path)
        }
        _ = try FileManager.default.replaceItemAt(url, withItemAt: temporaryURL, backupItemName: nil, options: [])
        replaced = true

        return OperationLogTrimResult(
            removedEntries: lines.count - retainedLines.count,
            retainedEntries: retainedLines.count,
            byteCount: Int64(outputData.count)
        )
    }

    /// 将已知日志事件代码转换为中文操作名称。
    /// - Parameters:
    ///   - event: 操作日志的事件代码。
    private static func friendlyEvent(_ event: String) -> String {
        switch event {
        case "app.started": return "应用启动"
        case "operation.started": return "开始执行操作"
        case "backend.command.started": return "开始执行后台操作"
        case "backend.command.completed": return "后台操作完成"
        case "backend.command.failed": return "后台操作失败"
        case "file.write": return "保存文件"
        default: return event.replacingOccurrences(of: ".", with: " ")
        }
    }
}

final class OperationLogWriter {
    static let shared = OperationLogWriter()

    private let lock = NSLock()
    private let sessionID = UUID().uuidString
    private var enabled = true

    /// 取得本机操作日志文件的位置。
    private var logURL: URL {
        URL(fileURLWithPath: NSHomeDirectory())
            .appendingPathComponent("Documents/pp-flowhub/data/operation-log.jsonl")
    }

    /// 在锁保护下更新操作日志开关。
    /// - Parameters:
    ///   - value: 是否启用操作日志。
    func setEnabled(_ value: Bool) {
        lock.lock()
        enabled = value
        lock.unlock()
    }

    /// 在锁保护下读取操作日志开关。
    /// 无参数。
    func isEnabled() -> Bool {
        lock.lock()
        defer { lock.unlock() }
        return enabled
    }

    /// 脱敏后追加并落盘一条操作日志；日志失败不影响业务操作。
    /// - Parameters:
    ///   - event: 操作日志的事件代码。
    ///   - message: 需要解析、记录或显示的业务消息。
    ///   - actor: 发起日志事件的角色名称。
    ///   - component: 产生日志的组件名称。
    ///   - details: 写入日志的附加结构化信息。
    ///   - operationID: 关联 App 与后端日志的操作标识。
    ///   - force: 日志关闭时是否仍强制写入本条事件。
    func record(
        _ event: String,
        message: String,
        actor: String = "app",
        component: String = "swiftui",
        details: [String: Any] = [:],
        operationID: String? = nil,
        force: Bool = false
    ) {
        lock.lock()
        defer { lock.unlock() }
        guard enabled || force else { return }

        var payload: [String: Any] = [
            "timestamp": ISO8601DateFormatter.operationLog.string(from: Date()),
            "event": event,
            "actor": actor,
            "component": component,
            "message": Self.redact(message),
            "session_id": sessionID,
            "operation_id": operationID ?? "",
            "details": Self.redact(details),
        ]
        do {
            let data = try JSONSerialization.data(withJSONObject: payload, options: [.sortedKeys])
            try FileManager.default.createDirectory(
                at: logURL.deletingLastPathComponent(),
                withIntermediateDirectories: true
            )
            if !FileManager.default.fileExists(atPath: logURL.path) {
                FileManager.default.createFile(atPath: logURL.path, contents: nil)
                try? FileManager.default.setAttributes([.posixPermissions: 0o600], ofItemAtPath: logURL.path)
            }
            var line = data
            line.append(0x0A)
            let descriptor = Darwin.open(logURL.path, O_WRONLY | O_CREAT | O_APPEND, S_IRUSR | S_IWUSR)
            guard descriptor >= 0 else { return }
            defer { Darwin.close(descriptor) }
            line.withUnsafeBytes { bytes in
                guard let baseAddress = bytes.baseAddress else { return }
                _ = Darwin.write(descriptor, baseAddress, bytes.count)
            }
            _ = Darwin.fsync(descriptor)
        } catch {
            // 审计日志失败不得中断用户的业务操作。
        }
        payload.removeAll()
    }

    /// 在写入锁保护下清理指定保留天数之外的日志。
    /// - Parameters:
    ///   - days: 需要保留的自然日天数（包含今天）。
    ///   - now: 清理日志使用的参考当前时间。
    ///   - calendar: 用于日期计算的日历。
    func trimLogToRecentDays(
        _ days: Int = 3,
        now: Date = Date(),
        calendar: Calendar = .current
    ) throws -> OperationLogTrimResult {
        lock.lock()
        defer { lock.unlock() }
        return try OperationLogReader.trim(toRecentDays: days, at: logURL, now: now, calendar: calendar)
    }

    /// 生成供子进程关联会话、操作和日志开关的环境变量。
    /// - Parameters:
    ///   - operationID: 关联 App 与后端日志的操作标识。
    func environment(operationID: String? = nil) -> [String: String] {
        [
            "WORKFLOW_OPERATION_LOG": logURL.path,
            "WORKFLOW_OPERATION_LOG_ENABLED": isEnabled() ? "1" : "0",
            "WORKFLOW_OPERATION_SESSION_ID": sessionID,
            "WORKFLOW_OPERATION_ID": operationID ?? "",
        ]
    }

    /// 判断字段名是否包含凭据或其他需要隐藏的敏感信息。
    /// - Parameters:
    ///   - key: 用于判断是否敏感的字段名。
    private static func sensitiveKey(_ key: String) -> Bool {
        let normalized = key.replacingOccurrences(of: "-", with: "_").lowercased()
        return ["password", "passwd", "secret", "token", "api_key", "apikey", "authorization", "cookie", "keychain", "credential", "username", "user_name", "remarks", "query", "input_value", "access_key", "private_key", "refresh_key"]
            .contains { normalized.contains($0) }
    }

    /// 隐藏文本中的凭据、网址和本机主目录；text 为待脱敏内容。
    static func redactText(_ text: String) -> String {
        var result = text
        let patterns: [(String, String)] = [
            (#"(?i)https?://[^\s\"'<>]+"#, "[网址已隐藏]"),
            (#"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9._~+/-]+"#, "[凭据已隐藏]"),
            (#"(?i)(?:password|passwd|secret|token|api[_-]?key|authorization|cookie|credential|username|user_name)\s*[:=]\s*[^\s,;]+"#, "[凭据已隐藏]"),
            (#"(?i)\"(?:password|passwd|secret|token|api[_-]?key|authorization|cookie|credential|username|user_name)\"\s*:\s*\"[^\"]*\""#, "[凭据已隐藏]"),
        ]
        for (pattern, replacement) in patterns {
            guard let expression = try? NSRegularExpression(pattern: pattern) else { continue }
            result = expression.stringByReplacingMatches(
                in: result, range: NSRange(result.startIndex..., in: result),
                withTemplate: replacement
            )
        }
        let home = NSHomeDirectory()
        if !home.isEmpty { result = result.replacingOccurrences(of: home, with: "~") }
        return result
    }

    /// 递归隐藏敏感字段，并将用户主目录替换为简写。
    /// - Parameters:
    ///   - value: 需要递归脱敏并序列化的值。
    ///   - key: 用于判断是否敏感的字段名。
    private static func redact(_ value: Any, key: String? = nil) -> Any {
        if let key, sensitiveKey(key) { return "[REDACTED]" }
        if let dictionary = value as? [String: Any] {
            return dictionary.reduce(into: [String: Any]()) { result, item in
                result[item.key] = redact(item.value, key: item.key)
            }
        }
        if let array = value as? [Any] { return array.map { redact($0) } }
        if let string = value as? String {
            return redactText(string)
        }
        if value is NSNull || value is String || value is NSNumber { return value }
        return redactText(String(describing: value))
    }
}

private extension ISO8601DateFormatter {
    static let operationLog: ISO8601DateFormatter = {
        let formatter = ISO8601DateFormatter()
        formatter.formatOptions = [.withInternetDateTime, .withFractionalSeconds]
        return formatter
    }()
}
