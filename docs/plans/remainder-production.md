# 零材料消耗的工厂单生产确认

状态：V0.5.5 已由用户安装，现场反馈按钮仍禁用；重复预览时序已修复，实际挂载弹窗回归与完整门禁通过，V0.5.6 已构建，签名安装受工具限制阻挡。

目标：本次数量全零时允许仅记录所选工厂单生产完成和时间；订单材料属于订单，选择工厂单不改变材料事实。有正数量时仍按实际数量走库存扣减。

约束：不增加生产方式或原因，不变更数据库结构。保留订单材料、历史生产消耗、五金、库存单和订单级出库范围。保留其他任务工作树修改，真实 PP0008 只打开面板并取消。

实现：
1. 撤去未安装 V0.5.4 方案的新增字段、迁移、余料选项和原因输入（已完成，正式库从未迁移）。
2. `confirm-production-without-materials` 校验显式确认、有限全零数量、工厂单归属/有效/已优化/未生产/未中止和库存待恢复；事务保存生产事实（已完成）。
3. 成功预览及合法草稿才可提交。全零按钮显示“仅确认生产，不扣减材料”，正量保留原流程，错误输入不默认为零（已完成）。
4. 隔离回归、真实库副本 schema/事实不变检查、完整门禁、一次串行构建、普通 Terminal/Aqua 签名安装、安装版只读验收（进行中）。

数据保护：在真实库只读快照的隔离副本执行初始化，逐表比较 schema 和旧数据，确保没有隐式迁移。真实生产确认不在本次授权范围内。

待完成：V0.5.6 签名安装及安装版只读入口验收。此前电脑操作工具拒绝访问 `com.apple.Terminal`（安全限制），后台没有有效签名身份，限制未获解除，不绕过或降级签名。构建后再次核对当前安装版仍为 V0.5.5；普通 Terminal 可执行 `/Users/lantian/Documents/pp-flowhub/scripts/install-app` 安装已构建产物。

验证结果：
- `test_zero_material_production`、`test_production`、`test_production_schema` 共 18 项通过。
- 完整 `scripts/test-release` 通过：454 项 Python（1 个原有缺失桌面夹具跳过）、Swift UI、AIMES 离线、PP0067 workbook E2E 与差异检查。日志 `/tmp/pp-flowhub-zero-production-release.log`。
- 真实库只读备份副本检查：31 表、2,929 行和全部 schema 不变，完整性/外键通过；报告 `/var/folders/80/v0wn4lyn4075k3fv5v2chmdw0000gn/T/pp-flowhub-zero-schema-7rnrb9k7/report.json`。
- 一次串行构建 V0.5.5：`/tmp/pp-flowhub-build/PP FlowHub.app`；打包 Node/Playwright 验证通过，后端四个改动文件与源码一致。可执行 SHA-256：`e125ff1e8d2d9a93d66c2e1aec1313e0027077d405012ec0bdc61cb3eb3127d6`。日志 `/tmp/pp-flowhub-zero-production-build.log`。
- 包内 CLI 在隔离真实库副本确认 PP0008 两工厂单，全零完成、重复拒绝，材料/历史消耗/五金/库存单/出库范围及 schema 保持不变。报告 `/var/folders/80/v0wn4lyn4075k3fv5v2chmdw0000gn/T/pp-flowhub-zero-bundle-d2ofa5o9/report.json`；不等于安装版 UI 验收。
- 真实 PP0008 两工厂单仍为已优化、生产关联为空；真实生产表仍为原六字段，未执行任何生产或库存确认。

V0.5.6 按钮时序修复验证：
- 移除订单中心预读，材料读取统一由弹窗发起；忙碌返回失败回调，失败后可重新读取。
- 实际 `NSHostingView` 挂载弹窗，模拟延迟和失败响应，验证读取中禁用、失败后可重读、全零成功后确认按钮启用、仅发出预期次数的请求以及忙碌回调。只点击模拟环境的重读按钮，不点击生产确认。独立回归日志 `/tmp/pp-flowhub-preview-lifecycle-ui.log`。
- 完整 `scripts/test-release` 通过：454 项 Python（1 项原有跳过）、SwiftUI、AIMES 离线、PP0067 workbook E2E 与差异检查；日志 `/tmp/pp-flowhub-preview-ready-release.log`。
- 一次串行构建 V0.5.6 成功，打包 Node 校验通过；日志 `/tmp/pp-flowhub-preview-ready-build.log`。产物 `/tmp/pp-flowhub-build/PP FlowHub.app`，可执行 SHA-256 `e22b8a6255b10ac929f1fb51a03f42cca1eb5d98eb8ce6ccb457371916f5e0c2`。
- 尚未签名安装，实际挂载测试不等于安装版验收。本轮不修改数据库结构，不提交真实生产或库存操作。
