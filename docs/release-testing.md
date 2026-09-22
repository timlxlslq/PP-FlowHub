# 发布测试与安装验收

## 验收目标

发布验收要回答两个问题：中央 SQLite 中的订单、工厂单、材料、五金、生产和出货事实，是否与界面显示一致；AIMES、Server、库存系统之间的边界，是否能从日志、单据号和数据库记录追溯。

Traveler 是按需导出能力，不是查询订单、登记生产或确认出货的前置条件。材料需求优先读取 SQLite；若缺少材料事实，或读取 SQLite 时出现受支持的读取异常，则回退到订单材料预览，且仍需材料校验。material 工作簿也参与材料事实的生成与解析。

自动测试是回归入口和业务不变量检查，不代表所有分支、外部服务或真实用户流程都已验收。正式结论必须分别报告源码/离线测试、构建、签名安装和安装版业务验证。

## Codex 发布测试门禁

纯 Markdown 修改只做差异、链接/命令和一致性检查，不触发 `test-release`、`build-app` 或 `install-app`；代码或 App 修改仍按下述完整门禁执行。

代码或 App 改动后，先定位受影响的业务链，确认测试覆盖真实 payload、重复操作、失败恢复和状态边界，再使用唯一门禁入口：

```bash
./scripts/test-release
```

该入口的实际执行顺序如下：

| 顺序 | 命令 | 实际覆盖 | 明确未覆盖 |
| --- | --- | --- | --- |
| 1 | [Python 回归](../scripts/test-release) | 运行 `tests/test_*.py`，覆盖隔离夹具、SQLite 事实、订单索引、AIMES 适配、Server 预览/扫描、库存状态、生产与出货边界、工作簿解析和源数据保护。关键入口见 [test_order_index.py](../tests/test_order_index.py)、[test_inventory.py](../tests/test_inventory.py)、[test_order_workflow.py](../tests/test_order_workflow.py)。 | 以隔离夹具和 mock 验证，不构成现场 Server/SMB、AIMES 或金蝶服务、数据库验收。 |
| 2 | [macOS UI 回归](../scripts/test-macos-ui) | 编译 `OperationLog.swift`、`TravelerAssistant.swift`、`AssistantView.swift`、`OrderDashboardView.swift` 与 [test_macos_ui.swift](../tests/test_macos_ui.swift)，执行订单中心、助手、待处理、消息、进度、生产/出货显示和源码约束断言。 | 这是测试二进制直接调用的 Swift/model 回归，不是已安装 App 的真实窗口点击、键盘操作、外部服务或现场数据库验收。 |
| 3 | [AIMES 表格离线回归](../scripts/test-aimes-table) | [test_aimes_table.mjs](../tests/test_aimes_table.mjs) 用 Playwright 本地页面 markup 验证延迟表头/行、加载遮罩、空表、缺列和未就绪错误；`page.route("**/*", route => route.abort())` 禁止网络。 | 不验证 AIMES 登录、真实工厂单、真实页面结构、真实返回数据或完整 `aimes_lookup.mjs` 查询链。 |
| 4 | [PP0067 workbook 专项](../scripts/test-workbook-e2e) | 将 [data/local-source/Optimized Orders/PP0067](<../data/local-source/Optimized Orders/PP0067>) 复制到临时目录，执行 `generate-material` → `update-related`；检查 ZIP/OOXML、禁止 `UNIQUE`/`FILTER`、要求 `SUMIF` 和 Color Table 数值；用 [verify_workbook.mjs](../tools/verify_workbook.mjs) 的 artifact-tool 导入、检查和渲染 material/Traveler。 | 不是现场 Server 文件、不是用户当前 workbook、不是打开 Microsoft Excel；渲染成功不等于 Excel 实际打开或人工视觉验收。 |
| 5 | `git diff --check` | 检查提交差异中的空白错误。 | 不检查业务逻辑、数据一致性或运行结果。 |

`test-release` 不包含 `build-app` 或 `install-app`。通过 wrapper 后不要重复运行其中已经完成的子门禁；只有新增修改、修复失败或需要定位回归时，才运行相应的必要完整门禁。

## 开发阶段如何安排测试

本节优化测试顺序和停止条件；代码或 App 修改仍须完成上面的完整发布门禁及后续签名安装。纯 Markdown 任务按本次差异判断，不因工作树已有其他任务的代码修改而触发发布，也不替那些修改宣布测试通过。

1. **先确定验收行为。** 开始修改时简述“改了什么行为、用哪个回归验证、何时算完成”。缺陷修复优先在隔离夹具重现失败；新增功能从用户要求和业务规则确定预期值，不从新实现反推断言。已有测试充分时直接复用。
2. **开发中快速反馈。** 按下表选择最小相关入口。测试能揭示真实风险才新增；重复提交、事务回滚、非法输入等按实际影响选择，不要求每个小改动机械覆盖所有类别。
3. **代码稳定后收口。** 运行一次 `./scripts/test-release`，不把所有子门禁再预跑一遍。成功后进入一次串行构建、正式安装和相关入口验收。门禁后若改了代码、测试、依赖或运行配置，先验证受影响部分，再对最终版本完成完整门禁；仅补充 Markdown 记录不使已有运行证据失效。
4. **失败有依据地处理。** 记录失败命令、退出码和关键错误，判断是产品缺陷、测试预期错误还是环境阻碍；修复或环境变化后先重跑失败入口。相同输入、相同环境的失败不要盲目循环，不能删断言或增加 skip 换取通过。确需修改旧预期时说明对应业务规则变化，保留仍有效的保护。

| 本次差异 | 开发中优先验证 | 收口要求 |
| --- | --- | --- |
| 纯 Markdown | 差异、相对链接/锚点、命令与脚本一致性 | 到此结束，不构建安装 |
| 局部 Python 业务 | 对应 unittest 方法或模块；必要时补错误路径 | 完整门禁、构建安装、相关入口验收 |
| SwiftUI/model | `./scripts/test-macos-ui`；布局和交互另在安装版检查 | 完整门禁、构建安装；源码断言不能替代真实交互 |
| AIMES 页面解析 | `./scripts/test-aimes-table` 及相关 Python 适配测试 | 完整门禁；真实登录/页面验证单列 |
| Excel 解析、公式、模板 | 对应 Python 测试；需要时执行 `./scripts/test-workbook-e2e` | 完整门禁；Excel 打开和视觉检查按改动单列 |
| 数据迁移、出库、跨模块事实 | 隔离库中的身份、幂等、失败回滚与前后事实比较 | 完整门禁及专项验收；真实库结构变更仍须明确确认 |

使用项目已有 `unittest`，不为定向测试添加框架。例如从仓库根目录选择一个已存在的测试：

```bash
.venv/bin/python -m unittest tests.test_aimes_production_verification.AimesProductionVerificationTests.test_all_produced_still_reads_recent_page_without_exact_queries
```

执行前确认该测试的临时目录和外部 mock；定向测试通过仅说明该行为通过，不代表完整门禁。

**串行与等待：** `test-release` 已顺序调用子门禁。`test-macos-ui` 使用固定 `/tmp/pp-flowhub-ui-tests` 与 module cache，不并发启动多个实例，也不同时另开包含它的完整门禁。构建、签名安装保持串行。长测试运行时可以阅读相关差异或准备验收说明，不修改正在受测的源码、夹具或依赖；等待进程退出后再作结论。

**轻量证据：** 在当前任务或已有交接记录中保留命令、受测版本/未提交差异范围、结果与跳过项、必要日志路径。研究效率时再记录耗时、重跑次数及原因；不另建台账系统。完成条件是必要检查通过且对应风险已验证，不以测试数量、回复长度或运行时长判断质量。没有本项目的前后测量，不宣称提速百分比。

### GPT-6 Astra 调研依据（2026-09-21）

以下来源已阅读；官方建议、作者实测和待执行方法分开看待。本节安排是结合本仓库脚本作出的工程选择，不是第三方对 PP FlowHub 的验证。

- [OpenAI：GPT-6 Astra 的测试与验证建议](https://developers.openai.com/api/docs/guides/latest-model#testing-and-verification)：小任务可能测试过宽；按影响验证，通过后仅在变化、失败或未解决疑点出现时追加检查。其指令遵循章节还建议检查 AGENTS/Skills 的冲突，因此将规则集中在现有入口，不叠加新插件。
- [GitHub：Frontier-simplify](https://github.com/MongLong0214/frontier-simplify)：作者强调减少自创流程和重复评审，同时保留真实正确性要求。Astra 数据仅为一个场景、每组一次的观察；输出缩短不代表质量或测试速度提高。
- [GitHub：Lattice 的 Astra 配对记录](https://github.com/moulwyse/lattice/blob/main/docs/evidence/owner-run-gpt-6-astra.md)：作者使用独立目录、原始验收测试和明确版本；仅一个固定夹具的一次配对，不能外推其节省比例。这里采用独立验收的原则，不安装其工具。
- [AstraCode：编码评测方法](https://astracode.io/blog/benchmarking-gpt-6-astra/)：保护验收文件、隔离夹具并检查坏输入是否被拒绝。文章明确尚未公布 Astra 付费评测结果；借鉴方法，不引用为模型效果实证，也不把模型评测的多次尝试要求套到每次开发测试。
- [Matt Shumer：Astra 使用体验](https://somethingbig.ai/astra-review)：长任务可能陷入局部细节，阶段目标有助于推进；复杂多会话组织来自个人大型实验。这里采用明确完成条件，普通修改不照搬其多 Agent 规模或无限评审循环。

## 业务规则验收清单

下表是发布后选择实际入口的依据。每行描述必须保持的业务边界和现有回归入口；它不是“所有代码分支已覆盖”的声明。

| 业务链 | 必须验证的行为 | 现有自动测试入口 |
| --- | --- | --- |
| 启动与同步 | 启动按本地缓存 → 当日 AIMES 检查 → Server 扫描；手动获取 AIMES 与手动扫描 Server 相互独立，手动 `force` 不会隐式重扫 Server；重复运行不能把成功事实误报成新的外部操作。 | [test_order_index.py](../tests/test_order_index.py) 的 AIMES daily/force 测试；[test_macos_ui.swift](../tests/test_macos_ui.swift) 的启动进度与历史测试。 |
| AIMES 事实与进度 | 成功标志、缓存、警告和持久事实一致；失败保留可用缓存；后台 progress、阶段耗时和完成消息按同一次运行保存。非法销售单名称不进入有效映射缓存，而进入持久 `aimes_review_rows`；Swift 将 `aimesFormatWarnings` 投影为待人工确认，并支持确认归属或忽略。 | [test_core.py](../tests/test_core.py) 的错误分类/脱敏/exact verify；[test_order_index.py](../tests/test_order_index.py) 的 warning、review、重开、确认/忽略和按日跳过；[test_report_selection.py](../tests/test_report_selection.py) 的流式进度；[test_macos_ui.swift](../tests/test_macos_ui.swift) 的 AIMES 会话消息。 |
| Server 发现到确认 | `scan-server` 只返回本次优化文件发现，不保存优化证据、优化时间或 XML baseline；磁盘快照排除 XML。材料确认后才推进工厂单及订单优化状态，并保存预览版本的文件基线。重复扫描、取消预览、写入失败均不得推进状态或基线。“确认无变化”仅更新已有材料确认文件夹的预览 XML 基线，不修改业务事实；拒绝未校验、有差异或本地事实已变化的预览。 | [test_order_index.py](../tests/test_order_index.py) 的 preview/confirm/scan 测试，以及 [test_confirmed_material_optimization.py](../tests/test_confirmed_material_optimization.py) 的重复扫描、取消预览、事务回滚、无 XML 材料确认、新增工厂单、逐单确认和预览后 XML 变化回归。 |
| 报表变更与五金来源 | 报表内容变化要重新进入预览；已确认五金来源按工厂单保护，内容未变化时重复预览不能切换或重复替换；失败写入必须回滚。 | [test_report_selection.py](../tests/test_report_selection.py) 的 source choice/restart 测试；[test_hardware_facts.py](../tests/test_hardware_facts.py) 的 projection、rollback 和 confirmed shipment 测试。 |
| SKU 映射与待处理 | 未完成映射且未按规则有效忽略的项目，阻止需要映射的写入；有效忽略按规则排除，不能绕过其他校验；“稍后处理”只是动作，不解决问题；映射保存成功后回读并继续原文件夹预览；不得重复提交业务写入或丢失已确认映射。 | [test_inventory.py](../tests/test_inventory.py) 的 mapping/block 测试；[test_macos_ui.swift](../tests/test_macos_ui.swift) 的 pending mapping callback/resume 测试；[test_order_index.py](../tests/test_order_index.py) 的 pending/review 持久化测试。 |
| 材料 SKU schema 与迁移 | 五张 SKU 引用表有 `products(code)` 外键，相关连接在事务前启用约束；旧材料、生产消耗和 Server 分配唯一迁移到 SKU，无法匹配时整体回滚；商品目录缺失的历史 SKU 保留且阻断新写入；映射或忽略规则改变不重绑或移除已确认 SKU，订单材料行删除后生产消耗/Server 分配仍保护商品业务属性；历史 raw fingerprint/journal 保持五字段来源快照，SKU 或数量真实变化仍触发更新；名义厚度/规范颜色、生产累计、详情、成本、库存和 Traveler 在迁移前后保持业务等价。 | [test_material_sku_contract.py](../tests/test_material_sku_contract.py) 的旧库迁移、失败回滚、外键、目录保留、属性锁定、映射不重绑、库存需求和读写链回归；[test_material_sku_outbound_history.py](../tests/test_material_sku_outbound_history.py) 的旧指纹兼容、SKU/数量变化、后改 mapping/ignore 不重绑回归；相关 [test_production.py](../tests/test_production.py)、[test_inventory.py](../tests/test_inventory.py)、[test_order_index.py](../tests/test_order_index.py)。 |
| 生产与出货 | 订单级板材/封边生产消耗写入生产事实；工厂单五金出货写入出货事实。已确认无可出库五金时仅按规则更新出货状态，不创建虚假库存单据；生产不等于工厂单出货。 | [test_production.py](../tests/test_production.py)；[test_inventory.py](../tests/test_inventory.py) 的 production/outbound separation、factory selection 和 shipped-block 测试；[test_macos_ui.swift](../tests/test_macos_ui.swift) 的生产/出货显示测试。 |
| 外部单据与本地同步 | 外部库存单据成功而本地同步失败时，先按单据号和本地事实对账；没有确认前不能盲目重试扣减或删除已成功的外部单据。 | [test_inventory.py](../tests/test_inventory.py) 的 outbound timeout、operation journal、document reconciliation 测试；[test_workflow_database.py](../tests/test_workflow_database.py) 的出货关系迁移测试。 |
| 订单中心与助手读层 | 订单中心、助手、成本和阶段进度来自持久事实的读层聚合；业务事件时间（优化、生产、出库）与操作耗时分开显示。 | [test_order_index.py](../tests/test_order_index.py) 的 summary/status/timing 测试；[test_macos_ui.swift](../tests/test_macos_ui.swift) 的 dashboard、cost、production/outbound 和 duration 测试。 |
| 会话消息 | 每次 App 会话从空集合起步；当前操作随 progress 更新，完成记录追加步骤和耗时；同一变化重复回读不增加历史消息，两次独立操作即使结果相同也各自保留。progress 更新不要求每一步都单独成为历史消息行。 | [test_macos_ui.swift](../tests/test_macos_ui.swift) 的 `testDashboardActivityIsScopedToAppSession`、`testDashboardSessionMessagesAndAimesProgress`、`testDashboardStartupProgressAndHistory`。 |
| Traveler/material 文件专项 | 只验证文件生成、解析与导出专项：material 生成、Traveler 更新、OOXML 公式安全、Color Table 数值和 artifact-tool 渲染。 | [test-workbook-e2e](../scripts/test-workbook-e2e)、[test_order_workflow.py](../tests/test_order_workflow.py)。 |

## 人工五金直接删除与 schema 迁移

`tests/test_manual_hardware.py` 覆盖人工五金物理删除、重复行合并、批量新增失败回滚、并发/重复提交、工厂单权限、旧失效行清理、字段移除、迁移失败完整回滚与幂等；`test_hardware_facts.py` 验证移除字段不会改变既有来源指纹。正式升级前执行 SQLite Online Backup，并在副本核对所有有效五金逐字段一致、其他业务表不变、完整性及外键通过；元数据迁移执行时间允许不同。关键订单详情、成本和库存需求在旧/新源码的隔离副本对比，不能只比较总行数。

安装版检查人工五金 820×620 弹窗、工厂单与 SKU 输入左对齐、回车搜索、正常状态不显示重新载入，以及暂存删除可撤销。读取失败显示重试，保存失败可重新载入；有草稿时先提示放弃。未经额外授权，不在真实订单保存验收草稿。

## Traveler 与 material 的专项边界

PP0067 测试使用 `data/local-source/Optimized Orders/PP0067` 的本地复制品，并在临时目录执行：

```text
generate-material → update-related
```

专项检查包括：

- ZIP/OOXML 可以读取，Usage List 和 material 不含 `UNIQUE`/`FILTER`；
- 公式使用兼容的 `SUM`/`SUMIF`；
- Color Table、Panel/edge 汇总和 PP0067 样本数值正确；
- artifact-tool 能导入、检查并输出各工作表渲染图。

这条脚本没有打开 Microsoft Excel，也没有完成现场 Server 或人工视觉验收。涉及模板、合并单元格、列宽、打印区域或页面布局时，保持至少两个独立读取器校验，并补充人工/视觉检查，不能把当前脚本描述成完成了全部模板比对。

### 独立文件夹人工登记回归

`tests/test_folder_manual_handling.py` 覆盖普通无订单任务、单订单/混单补单识别、新 AIMES 工厂单使待处理补单恢复正常规则、未知订单、可空参考和单号、相同内容重复登记、XML 删除/修改、变化待处理跨观察期限、到期跳过、旧台账增量迁移，以及事务失败回滚。通过有材料/五金/生产事实的隔离数据库快照比较，检查登记与同步没有修改正式订单；库存入口被 mock 禁止调用。

安装版检查待处理中心是否按文件夹显示补单、提供“已人工处理”和可留空的参考输入。可以打开并取消登记表单；未经真实出库事实确认，不点击最终登记按钮。自动测试不代表已替真实文件夹补登记。

## 构建与正式安装

材料 SKU 迁移在正式发布前还要做数据库级验收，不能只看单元测试：先用 SQLite Online Backup 创建可恢复备份并在副本完整演练；记录迁移前后五张表行数、按订单/SKU/来源汇总数量、关键订单详情/成本/库存需求结果，以及 `integrity_check` 和 `foreign_key_check`。正式库只在副本无未解决项后迁移；迁移成功、完整门禁通过、正式签名安装和安装版回读必须分别报告，不能把其中任何一层替代另一层。

门禁通过后只进行一次串行构建：

```bash
./scripts/build-app
```

[build-app](../scripts/build-app) 实际检查固定 Bundle Identifier、Python 依赖、Node 架构和动态库，编译 Swift 与钥匙串 helper，复制 Python/Node/Playwright/项目资源，先执行打包 Node 的 `--version` 验证能启动，再验证绝对路径能 import Playwright 且 `chromium.launch` 接口存在；Playwright 只做 import 与接口检查，不启动浏览器，最后生成 `/tmp/pp-flowhub-build/PP FlowHub.app`。应记录 `CFBundleName`、`CFBundleExecutable`、`CFBundleIdentifier`、版本、可执行文件 mtime/SHA-256 和关键资源是否与当前源一致。

构建成功不等于正式安装成功。构建成功后，由 Codex 主动自动通过可用的普通 macOS Terminal/Aqua 会话签名安装，无需重复确认。运行绝对路径：

```bash
/Users/lantian/Documents/pp-flowhub/scripts/install-app
```

[install-app](../scripts/install-app) 不运行测试或重新编译。它检查 Apple Development identity、临时 App、Bundle Identifier 和可执行文件；分别签名/验证钥匙串 helper 和 App，检查 Authority、TeamIdentifier、Designated Requirement；随后原子替换 `/Applications/PP FlowHub.app`，校验安装后的可执行文件 SHA-256、Bundle 和 keychain helper probe，最后归档已消费的构建副本。

后台会话看不到签名 identity 时，应优先使用可用的普通 Terminal/Aqua。若工具明确拒绝或签名安装失败，保留构建产物并报告失败位置；不能降低签名标准、使用 ad-hoc 签名或为了签名失败重复构建。安装过程本身不证明业务流程通过。

### AIMES 未生产工厂单核验（2026-09-17）

`tests/test_aimes_production_verification.py` 使用临时数据库和 mock AIMES，验证完成生产批次（包括共享批次）排除、未完成批次继续核验、订单与工厂单双键匹配、最近页面排除、已生产事实不被删除结果停用，以及全部已生产时仍读取最近 50 条。测试不调用真实 AIMES，也不证明现场耗时。

## 安装版实际入口验收

安装后按改动影响选择真实入口：

1. 先确认 `/Applications/PP FlowHub.app` 的 Bundle Identifier 和可执行文件 SHA-256，退出旧进程，再重新打开安装版 App。
2. 至少验证本次改动对应的订单中心、助手、AIMES、Server、待处理或生产/出货入口；后端启动、状态文本、事实回读和失败恢复要分别记录。
3. 真实库存扣减、业务事实确认和 Server 写入只在本次任务明确授权的业务操作范围内执行；发布授权不等于任意真实出库授权。默认优先使用隔离夹具或测试环境。
4. 如果外部服务不可用或测试不便由 Codex 完成，说明未验证项，给出用户可执行的操作步骤和预期结果；不能把离线测试、源码约束或渲染图写成现场验收。
5. 验证完成后退出本次启动的 PP FlowHub 和安装 Terminal，不关闭用户的其他 Terminal 窗口。

## 结果记录

每次发布记录以下五层证据：

- 改动影响的业务链和对应回归入口；
- 自动门禁结果（通过数量、跳过项、失败位置）；
- build 产物路径、Bundle metadata、Node/Playwright 和关键 SHA-256；
- Aqua Terminal 签名安装结果、安装包 SHA-256 和 `/Applications` 路径；
- 安装版实际入口结果、未覆盖项和失败原因。

“存在测试文件”不等于覆盖全部业务；“构建成功”不等于签名安装成功；“安装成功”不等于真实 Server、AIMES、库存或 Excel 用户流程验收。

### 五金 SKU 归一化验证（2026-09-17）

`test_hardware_sku_contract.py` 覆盖字段移除与事务失败回滚、商品名称/规格实时读取、缺失或禁用 SKU 阻断、映射与忽略不改变已有事实、引用单位保护以及人工数量不折半。`test_server_rail_units.py` 继续覆盖左右轨单边数量和 M1094–M1097 偶数除二；迁移不得再次换算已有数量。正式库须先备份和副本演练，逐行核对所有保留字段与其他业务表，来源版本仅重算 SKU/数量指纹；回读成本、库存需求和出库状态，再分别记录完整门禁、构建、正式安装和安装版验证。

## 生产结构精简门禁

`test_production_schema.py` 检查旧记录 ID/历史时间保留、重复工厂单迁移失败完整回滚、删除表/字段不会重建、跨订单同 SKU 消耗、一次生产约束、写入失败回滚和临时校验结果不持久化。生产数量、出库单据、五金、材料分配及所有未改业务表在副本按行比较；无 Server/AIMES/库存外部写入。正式发布记录副本与正式备份路径、schema 差异、门禁、构建、签名安装及安装版只读回读。

## 订单中止（2026-09-18）

`tests/test_order_abort.py` 在隔离数据库验证显式确认、未知订单拒绝、重复请求幂等、工厂单事实保留、重启与同步 upsert 后仍中止、新增/失效工厂单、临时投影清理，以及生产/出库在访问外部系统前阻断。Swift 回归验证中止订单的默认排除与指定筛选。安装版检查生产、出库右侧的中止按钮，打开确认框并取消；不对真实订单执行最终中止。

## 计算成本材料门槛（2026-09-18）

`testOrderCostMaterialAvailability` 验证无材料拒绝发起请求、零数量禁用、板材及仅封边可用、读取中/排队禁用和材料清空后重新禁用。安装版应分别打开无材料的已拆单待优化订单和已有材料订单，观察成本按钮灰色/可点击状态，并检查三个动作按钮等宽、间距保持 8；该检查不涉及真实中止或库存写入。

## 临时文件夹永久忽略（2026-09-18）

`test_server_folder_ignore.py` 覆盖永久跳过、内容变化不重新提醒、不读取忽略目录内文件、重启/重复请求、路径范围、符号链接、事务回滚、其他文件夹保留，以及业务事实/基线不变。Swift model 回归覆盖失败保留队列、成功只移除目标及重复点击阻断。安装版打开“忽略此文件夹”确认框后取消，不替真实目录执行忽略；同时确认“已人工处理”仍可用。


## 五金一致性边界（2026-09-21）

`test_hardware_integrity_boundaries.py` 覆盖 PP0064 范围核对不生成 PP0008 问题、空范围、显式维护审计只读且保留路径、人工同版重启、变版重新选择、保留手工五金和出货事实、旧 token 拒绝、人工确认末步失败回滚、多工厂单报表末步失败回滚，以及数据库/未知异常分类。新增故障注入使用 mock，不新增测试触发器。Swift 回归验证来源、订单、工厂单和路径经过错误呈现后仍保留；旧轨道数量回归先选择变版来源，再验证奇数阻断。

真实 PP0008 不作为写入验收夹具，不执行补登记或删问题；其历史人工处理意图需独立确认。安装版业务入口验证优先隔离 state-dir；无法安全隔离启动时只验证签名、包内资源及隔离后端，不将其称为真实订单窗口验收。
