# 临时文件夹永久忽略

目标：恢复独立忽略按钮；按用户最新要求，忽略后不再观察。
状态：实现、完整门禁和构建完成；自动安装因电脑操作工具禁止访问 Terminal 而受阻。
约束：保留原工作树改动；不替真实目录执行忽略，不登记真实出库；已人工处理仍观察三天。

- [x] 核对当前扫描、人工登记、界面和历史移除原因。
- [x] 新增永久忽略决定，接入自动扫描/同步/快照复用及两个界面。
- [x] 补充隔离回归、业务规则、数据模型和学习文档。
- [x] 完整发布门禁、一次串行构建。
- [ ] 普通 Terminal/Aqua 签名安装与安装版确认框取消验收。

验证：隔离数据库测试状态边界、幂等、失败回滚、扫描排除、其他待处理保留及业务事实不变；UI model 测试成功/失败/重复点击。
剩余决策：无。恢复忽略的管理入口不在本次范围；按路径跳过，改名视为新目录。

## 发布证据

- 定向 10 项测试通过。完整门禁：413 项 Python 测试（1 项原有跳过）、Swift UI、AIMES 离线、PP0067 workbook、diff 检查均通过。首次沙箱运行被 SwiftUI macro 的 sandbox_apply 阻断；允许的普通编译环境重跑通过。
- 一次串行构建通过：`/tmp/pp-flowhub-build/PP FlowHub.app`，0.4.1 (5)，Bundle ID `com.pacificpride.ppflowhub`；打包 Node v24.19.0 验证通过，两个改动 Python 模块与源码逐字节一致。
- 未签名可执行文件 SHA-256：`446062b2a258bec97deb60865873cccfcaef24ff03f05f4b444da4ecfe749d76`。
- `cua.getApp("com.apple.Terminal")` 明确返回 `Computer Use is not allowed to use the app 'com.apple.Terminal' for safety reasons.`；没有执行安装、降级签名或安装版验收，没有关闭现有 App 或用户终端。
- 产物保留待普通 Terminal 执行 `/Users/lantian/Documents/pp-flowhub/scripts/install-app`。未对截图目录或其他真实目录执行忽略，测试使用隔离数据库。

## 操作区排版调整

按用户截图调整：说明独立在上，忽略和已人工处理下方同排靠右，8 点间距，两个标签均为 112 点宽、regular 控件尺寸。待处理中心和 Server 变化窗口同步。沿用当前原生玻璃样式，无业务规则变更。

完整门禁再次通过：413 项 Python（1 项原有跳过）、Swift UI、AIMES 离线、工作簿专项。一次串行构建成功，替换为最新待安装产物；未签名可执行文件 SHA-256 为 `7a7ba6b0fbb185720614268185abf37788e256bfe770820124a2a3bc51be9635`。Terminal 的电脑操作限制仍阻止自动安装，尚未完成本次布局的安装版视觉验收；未操作真实忽略或登记。
