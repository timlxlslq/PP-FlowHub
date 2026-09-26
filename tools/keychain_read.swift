// 从 macOS 钥匙串读取库存系统账号密码，并写入标准输出供调用方使用。
// 参数：命令行第一个参数为账号名称；必须且只能提供一个账号。
// 参数缺失以状态 2 退出；读取失败、非 UTF-8 或空密码以状态 3 退出。
import Foundation
import Security

guard CommandLine.arguments.count == 2 else {
    fputs("missing account\n", stderr)
    exit(2)
}

let query: [String: Any] = [
    kSecClass as String: kSecClassGenericPassword,
    kSecAttrService as String: "com.pacificpride.workflow-assistant.jdy",
    kSecAttrAccount as String: CommandLine.arguments[1],
    kSecReturnData as String: true,
    kSecMatchLimit as String: kSecMatchLimitOne,
]
var result: CFTypeRef?
let status = SecItemCopyMatching(query as CFDictionary, &result)
guard status == errSecSuccess,
      let data = result as? Data,
      let password = String(data: data, encoding: .utf8),
      !password.isEmpty else {
    fputs("keychain read failed: \(status)\n", stderr)
    exit(3)
}
FileHandle.standardOutput.write(Data(password.utf8))
