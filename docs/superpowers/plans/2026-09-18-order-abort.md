# 订单中止

目标：新增已中止状态与生产、出库右侧的二次确认中止按钮。
状态：完成。用户已安装；已核对 Apple Development 签名，并完成安装版按钮、确认框取消及筛选验收。
约束：保留现有工作树；不修改真实订单事实，不自动退库存；沿用 orders.stage，无 schema 迁移。

- [x] 追踪状态聚合、CLI/service、生产和出库入口。
- [x] 实现确认后持久化、刷新保护、默认筛选与后台操作阻断。
- [x] 增加隔离回归及业务/学习说明。
- [x] 完整 test-release 门禁、一次串行构建。
- [x] 用户完成普通 Terminal 安装；Codex 核对 Apple Development 签名及安装版只读验收。

验证：未确认、未知订单、幂等、重启/同步/新增工厂单、旧预览阻断、历史事实保留、筛选。真实验收只打开并取消确认框，不中止真实订单。
剩余决策：无；恢复与填写中止原因不在本次需求范围。

## 发布证据

- 完整门禁通过：401 项 Python 测试（1 项原有跳过），Swift UI、AIMES 离线、PP0067 workbook 专项通过。
- 初次沙箱执行受 SwiftUI macro 的 sandbox_apply 限制；允许编译环境重跑后成功。新增状态使旧数量断言失败，已更新为 10 种并重跑完整门禁通过。
- 一次构建成功：`/tmp/pp-flowhub-build/PP FlowHub.app`，版本 0.4.1 (5)，标识 `com.pacificpride.ppflowhub`；打包 Node v24.19.0 验证通过，四个改动 Python 模块与源码逐字节一致。
- 可执行文件 SHA-256：`5189b0a4df36a3093135cd0c948fb6f0eea887237ea424ef62944c0b2992406b`。
- 电脑操作工具对 `com.apple.Terminal` 明确返回禁止访问；未运行安装脚本，未使用降级签名。保留未签名产物，当前安装版未替换。原先运行的 App 保持原状，没有启动安装 Terminal。
- 未执行安装版按钮/确认框视觉验收；真实数据库只读核对，中止订单数前后均为 0。

## 用户安装后的验收

用户报告已安装后，核对 `/Applications/PP FlowHub.app` 四个改动 Python 模块与源码一致；安装脚本归档的构建可执行文件哈希与本次构建一致。签名后的可执行文件 SHA-256 为 `e9b7cded47a1abbd0c3b517e7788fbd3c456ee4ab5cf46b0a2e723ff08e7d683`。沙箱内证书链不可用；提升只读验证权限后 `codesign --verify --deep --strict` 通过，Authority 为 Apple Development，TeamIdentifier 为 ZF64PZKWMD。

安装版实际展开 PP0089：按钮位于生产、出货右侧，无遮挡；点击中止出现含订单号和影响说明的确认框，提供取消与确认中止。已点击取消；SQLite 中 PP0089 仍为已拆单待优化，中止订单数仍为 0。筛选菜单含已中止。未执行真实中止，最终写入逻辑由隔离回归覆盖。启动时 App 自动扫描 Server 并显示待处理提醒，仅关闭提醒，未确认任何业务写入。
