# 订单展开性能与布局稳定性

目标：消除 PP0064 展开时 UI 主线程的路径属性查询，隔离消息区和订单列表更新，移除点击层的嵌套 Hosting 尺寸反馈。

状态：完成。代码、完整发布门禁、一次串行构建、用户正式安装及安装版验收均完成。

约束：保留现有工作树修改、单击展开/双击详情、独立操作按钮和消息进度；不新增缓存、不改业务事实、不通过库存/生产写入验收。

## 步骤

- [x] 路径展示使用纯字符串处理，不触发 Server 文件系统访问。
- [x] 独立列表拥有展开与选择状态；消息区只接收可比较的相关输入。
- [x] 透明 AppKit 点击层不包含 NSHostingView；保留助手卡片交互。
- [x] 回归覆盖输入隔离、消息更新、路径边界和点击层结构。
- [x] 完整 test-release、一次串行 build-app。
- [x] 用户完成 Terminal/Aqua Apple Development 安装，Codex 核验正式签名。
- [x] 安装版 PP0064 展开/收起/滚动、详情和小订单回归；核对日志与性能采样。

## 证据与验证

诊断中两次 PP0064 后台 detail 耗时约 3–4 ms，App 主线程完成记录延迟 4.35 s / 11.74 s（第二次有采样开销）。采样主线程 550/1179 样本停在 lstat，入口是消息区及待处理分组的 URL(fileURLWithPath:)。历史崩溃报告显示 NSGenericException / 布局约束更新次数超限；点击层是待验证的优先修复点，不能只凭源码称唯一根因已证实。

剩余决策：工厂单懒布局先不改变；若基础修复后实测仍有明显瓶颈，再依据采样处理。

## 本次验证记录

- `test-release` 通过：401 项 Python（跳过 1 项）、macOS UI、AIMES 离线、PP0067 workbook、diff 空白检查。
- 首次 Swift 编译被沙箱宏插件限制阻断；普通执行环境中定位并修正一个遗漏的无障碍报表名称引用后，完整门禁通过。
- `testDashboardExpansionIsolation` 实际挂载消息视图：材料、选中订单与 detail running 改变后消息 body 计数不增加；真实 Server 进度和失败后计数增加。点击接收视图没有子视图、内容约束或固有尺寸；单击仍等待双击失败。
- 电脑工具对 `com.apple.Terminal` 返回 `Computer Use is not allowed to use the app 'com.apple.Terminal' for safety reasons.`，未执行安装，不使用其他方式绕过工具限制，也不使用降级签名。
- 此时不能声称安装版 PP0064 的延迟已经降到某个数值，或历史崩溃唯一根因已证实；待签名安装后实测。
- 一次串行构建成功，未签名产物 `/tmp/pp-flowhub-build/PP FlowHub.app`；版本 `0.4.1 (5)`，Bundle Identifier `com.pacificpride.ppflowhub`；可执行文件 SHA-256 `6d4614d03b4ba1898d60848e5216bece93252d6f3e60730bb5c441e509733a64`。打包 Node v24.19.0 验证通过，`codesign -dv` 确認产物未签名。
- 本轮前后只读逐行摘要核对 `material_items`、`hardware_items`、`production_materials`、`outbound_documents`、`outbound_document_factories` 均未变化。未操作生产、库存或订单中止。

## 用户安装后的验收（2026-09-18 15:23–15:27）

- 已核对安装归档的未签名可执行文件 SHA-256 与本次构建一致；安装文件与归档 Mach-O UUID 同为 `1AA9956B-E90D-3FC1-BA39-5D7F8FB4478E`。普通只读环境 `codesign --verify --deep --strict` 通过，Apple Development 证书链有效，TeamIdentifier 为 `ZF64PZKWMD`。沙箱内曾返回证书信任错误，不能将其误报为正式签名失败。
- 退出安装前旧进程后重新启动安装版，验收 PID `12341`、session `1591D002-2579-4C33-8463-65E892D552BB`。启动自动扫描后仅关闭待处理提示，未确认业务写入。
- PP0064 四次单击展开的 App operation.completed 耗时分别为 0.005677、0.002429、0.005015、0.099987 秒；Python detail 仍为毫秒级。旧版同计时点为 4.35 / 11.74 秒，后者有采样开销。这是请求开始到主线程记录完成的时间，不是鼠标点击到完整绘制的精确时长。双击详情另测约 0.305 秒。
- 完成三次收起及第四次筛选后展开、长列表上下滚动、工厂单勾选/取消、双击详情/关闭、订单安排打开/关闭未保存，以及 PP0089 单工厂单回归。消息内容及顶部位置保持稳定。助手卡片双击仍定位订单中心并筛选 PP0064，不误开详情。
- 20 秒采样覆盖滚动/收起及再次展开，`/tmp/pp0064-after-sample.txt` 中未采到 `lstat`；本次进程的最终布局异常筛选 `/tmp/pp0064-after-layout-log.txt` 无匹配记录；最新 PPFlowHub 崩溃报告仍为验收前 14:56。结论限于本次操作范围，不能保证所有条件下永不崩溃。
- 五张被核对业务表的行数与逐行摘要均未变化（材料、五金、生产材料、出库单、出库单工厂关联）。验收 App 已退出；用户自行打开的安装 Terminal 未操作。
