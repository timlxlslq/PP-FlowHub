# 材料确认写入后才完成优化

- 目标：扫描/取消预览不保存优化文件事实或基线、不推进优化状态；材料确认成功后原子保存材料、工厂单优化状态和文件基线。
- 状态：实现、完整发布门禁、构建、Apple Development 正式签名安装及安装版扫描/材料验收全部完成。
- 约束：保留现有工作树改动、已确认材料和生产/出货事实；独立人工文件夹登记规则不变；不操作真实库存。
- 步骤：核对扫描与确认调用链；调整持久化责任；覆盖重复扫描、预览取消、失败回滚、材料确认和新增工厂单；更新权威及学习文档；完整发布门禁、串行构建、正式签名安装、安装版验证。
- 验证：隔离数据库/文件夹回归，完整 `scripts/test-release`；安装包与当前源码一致；实际 App 只读检查及扫描边界检查。
- 剩余决策：无。已确认文件与确认版本比较；未确认文件每次作为待处理发现。历史扫描日志保留为审计记录，不作为优化或扫描基线依据。

## 已完成

- 扫描移除优化证据写入及 XML 基线自动补齐，磁盘快照排除 XML。
- 材料确认事务保存所选工厂单状态和预览版本基线，汇总真实已确认状态；逐单确认未结束时保留待处理提醒。
- 新增 7 项隔离回归，覆盖重复扫描、取消预览、失败回滚、无 XML 材料确认、新增工厂单、逐单确认和预览后 XML 变化；权威与学习文档同步更新。
- Xcode 初始化完成后完整重跑发布门禁：Python 回归 338 项通过（1 项缺少本地桌面夹具而跳过）、macOS UI、AIMES 离线表格和 PP0067 工作簿专项全部通过；差异空白检查通过。日志：`/tmp/pp-flowhub-optimization-release-xcode.log`。
- 构建运行时检查通过（Node v24.19.0）；正式安装脚本完成 App/helper 签名、验证、同 Team 检查、安装文件哈希和 keychain probe。安装位置 `/Applications/PP FlowHub.app`，版本 0.4.1 (5)，Bundle ID `com.pacificpride.ppflowhub`；可执行文件 SHA-256 `6813ede05e7886e4a01fabfbcf18483adb5c02872a79eb524637cd47e0617cda`。打包的 order_index/database/order_workflow 与当前源码一致。日志：`/tmp/pp-flowhub-optimization-build-normal.log`、`/tmp/pp-flowhub-optimization-install.log`；元数据：`/tmp/pp-flowhub-optimization-installed.json`。
- 重开安装版后，启动扫描与手动第二次扫描都发现相同 12 项变化、3 个待处理文件夹；未确认文件再次提示。启动扫描仅新增 PP0087 文件夹对应的“已设计”订单，已有订单状态不变；工厂单优化字段、优化文件记录、XML 比较基线和材料逐行不变。第二次扫描上述全部记录及所有订单状态不变，磁盘扫描快照不含 XML 路径。证据：`/tmp/pp-flowhub-optimization-startup-check.json`（订单集合差异仅为新增 PP0087）、`/tmp/pp-flowhub-optimization-repeat-check.json`。
- 安装版 PP0086 详情显示 5 条板材/封边材料（板材 27 张、封边 263.95 m）及两个工厂单的五金明细，保持已优化；验收后退出 App。现场只验证扫描与已有材料读取，未对其他真实订单确认材料或操作库存；确认成功、取消预览与失败回滚由隔离回归验证。

## 发布环境记录

- 初次门禁的 UI 回归通过，AIMES Chrome 在沙箱内以 EPERM/SIGABRT 退出；该离线专项在普通权限环境重跑通过。
- 最终扫描提示修改后曾遇到 Xcode 许可未接受、独立 Command Line Tools 缺少 `SwiftUIMacros.StateMacro`。用户完成 Xcode 初始化后，使用 Xcode 27.0 正常通过最终完整门禁，未为环境错误修改业务代码。
- 首次构建受沙箱限制，Xcode 的 swift-plugin-server 无法启动；该次没有生成新产物。之后在普通权限环境串行重试，构建成功，未并行构建或修改签名标准。
- 电脑控制明确禁止操作 Terminal；遵守工具限制，直接在获准的普通权限会话运行正式安装脚本，成功取得 Apple Development identity 并完成安装。没有启动安装 Terminal，也没有降级签名。
