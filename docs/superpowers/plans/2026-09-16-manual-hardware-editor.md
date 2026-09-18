# 订单人工五金编辑

- 目标：在计算成本右侧增加人工五金入口，按用户确认草图提供按工厂单分组的列表、SKU/名称搜索、新增和删除，无备注 UI。
- 状态：已实现；完整门禁及构建通过，用户完成正式签名安装；安装版入口、检索、暂存取消及只读保护已验证。
- 约束：保留现有工作树修改；只编辑 manual 来源；不写真实业务测试数据；新增和删除暂存后统一保存；不修改 Traveler 或外部库存。
- 步骤：Python 列表/事务保存及 CLI → SwiftUI 弹窗及刷新 → 隔离回归 → 完整门禁 → 串行构建 → Aqua 签名安装 → 安装版只读验收。
- 验证：归属校验、启用商品、正整数、删除范围、重复提交、并发变化、失败回滚、自动五金保留；UI 空态、检索、暂存、取消和保存。
- 决策：已出库或失效工厂单显示已有记录但禁止修改；保存校验基线版本，冲突时要求重新载入。2026-09-17 用户明确要求人工五金直接删除，并移除 hardware_items.active；其他来源字段暂保留。
- 本轮状态：代码、文档、迁移及完整门禁已完成；串行构建完成；用户在普通 Terminal 完成正式安装，Codex 已验证签名及安装版界面。界面缩至 820×620、输入对齐、回车搜索、异常恢复入口均已实现。
- 本轮剩余决策：无。正式库检查仅两条 inactive 人工五金，其余 116 条有效记录必须保持原值。
- 验收边界：未对真实订单执行保存或删除写库；原子保存、删除、撤销范围和并发失败由隔离回归覆盖。真实记录只读查看，测试草稿已放弃。
- 视觉目标：用户确认 exec-3d2be2c8-489c-4c6e-ad52-9c3412e1f4c7.png（按工厂单分组，无备注）。

- 2026-09-17 迁移证据：正式库 118→116 行，仅删除 PP0064 / F2609150254 / M1068、M1069 两条旧人工记录；有效行逐字段、其他业务表、外键和完整性均通过。备份：`/Users/lantian/Documents/pp-flowhub/data/database-backups/hardware-direct-delete-20260917-090524/workflow-before.sqlite3`。PP0064、PP0077 的详情（去除废弃 active 字段后）、成本、库存需求在旧/新源码隔离副本中完全一致。
- 本轮门禁：378 项 Python 测试、1 项跳过；macOS UI、AIMES 离线表格、PP0067 workbook、diff check 通过。沙盒 Swift 宏插件启动失败后在正常 macOS 环境重跑通过。

- 构建：0.4.1 (5)，Bundle `com.pacificpride.ppflowhub`；`/tmp/pp-flowhub-build/PP FlowHub.app`，可执行文件 SHA-256 `57634b4d83defb8c79d20984c9a254ca6effe68c97a7bd1fac89e4b9aa7ae52d`；8 个相关 Python 资源与源码逐字节一致，打包 Node 验证通过。
- 安装阻碍：Computer Use 禁止操作 com.apple.Terminal；后台提权安装又被自动审批拒绝（替换 /Applications App，且项目规定普通 Terminal/Aqua）。未绕过、未降级签名，未启动旧版 App。等待用户手工运行绝对路径 install-app；本轮缩窄、对齐与回车搜索的安装版验收尚未完成。

- 安装闭环：用户回复已安装；正常 macOS 环境 codesign --verify --deep --strict 通过，Apple Development 证书链与 TeamIdentifier ZF64PZKWMD 确认。安装版 SHA-256 `f094bfc1e4cea62593da0ea1ac1dd2206f88429d79593b05e4b7ef4093b7614d`，8 个 Python 资源与源码一致。后台沙盒曾报 CSSMERR_TP_NOT_TRUSTED，正常环境只读复核通过。
- 安装版验收：实际截图 820×620，工厂单与 SKU 输入框左边缘对齐，常驻重新载入已移除；M1068 + Return 返回一个正确商品；删除草稿→撤销，保存重新禁用，取消退出。全部 116 条 hardware_items 与迁移演练逐字段一致，完整性/外键通过。没有用真实订单执行新增或删除保存。异常恢复入口已实现，未在真实安装版人为制造后台故障。App 已退出，用户安装 Terminal 未操作。
