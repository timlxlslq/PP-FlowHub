# pp-flowhub 项目导航与协作规则

## 项目与当前阶段

pp-flowhub 是内部 Workflow Assistant。当前主产品是 SwiftUI 生产工作流 App，正在完善可测试、可复用的 Python 业务模块；已有有限的 Agent 结构化路由和 Skills 资料，但还不是完整的自动 Workflow Agent。

长期目标是：SwiftUI App → Workflow Agent → 单一职责 Skills → 确定性 Python Engine → Excel / SMB / Playwright / WeCom SmartSheet。SQLite 持久事实独立于这些投影和外部适配层。

当前运行入口分两条：订单中心主要由 App 直接调用 CLI / `order-service`；助手入口经过本地命令解析、有限 Agent 和 Typed Gateway。两条路径最终都应落到确定性的 Python 业务模块。

用户是 Python 初学者。新功能先把输入、输出和错误边界做清楚并能用 Python 测试；只有稳定、重复且输入输出明确的流程才抽成 Skill。Agent 负责理解目标和组织调用，Python 负责读取、解析、校验和处理；不要把确定性业务逻辑塞进提示词。避免无必要的依赖、设计模式、元编程、过度抽象和大重写。

## 代码与文档地图

| 范围 | 入口或权威内容 |
| --- | --- |
| 环境与快速运行 | [README.md](README.md) |
| macOS App | [macos/](macos/)、[scripts/build-app](scripts/build-app)、[scripts/install-app](scripts/install-app) |
| CLI 入口 | [scripts/pp-flowhub](scripts/pp-flowhub)、[traveler_assistant/assistant_cli.py](traveler_assistant/assistant_cli.py) |
| Python 业务 | [traveler_assistant/core.py](traveler_assistant/core.py)、`order_workflow.py`、`order_index.py`、`production.py`、`inventory.py` |
| 外部适配与配置 | [tools/](tools/)、[traveler_assistant/](traveler_assistant/)；配置集中管理地址和非敏感规则 |
| 模板与回归 | [resources/](resources/)、[tests/](tests/) |
| 架构与数据 | [docs/architecture/system-architecture.md](docs/architecture/system-architecture.md)、[docs/architecture/pp-flowhub-data-model.md](docs/architecture/pp-flowhub-data-model.md) |
| 业务规则 | [docs/business-rules.md](docs/business-rules.md)、[docs/inventory-outbound-rules.md](docs/inventory-outbound-rules.md) |
| 发布验证 | [docs/release-testing.md](docs/release-testing.md) |
| 学习索引与源码地图 | [docs/learning/04-handoff-guide.md](docs/learning/04-handoff-guide.md)、[docs/learning/05-file-map.md](docs/learning/05-file-map.md) |
| 当前上下文与历史 | [docs/project-static-context.md](docs/project-static-context.md)、[docs/project-handoff-log.md](docs/project-handoff-log.md) |

每份文档有自己的权威范围。静态上下文只保留经过当前源码或发布流程校正的事实；历史教程、原型、计划和迁移指南保留学习价值，并标明历史适用范围及现行入口，不覆盖现行规则。

## 判断、协作与教学

执行前先独立判断需求，检查错误前提、逻辑漏洞、遗漏、歧义、风险和更简单的长期方案，并说明取舍；同时评估维护成本、兼容性、回归风险、数据安全、用户工作流和发布影响。修改前阅读与任务相关的源码、文档、工作树状态和差异；按相关性渐进阅读，不把每次任务都变成全仓通读仪式。

按任务选择最小充分的阅读范围：UI 修改先读实际入口和调用链；业务修改先读对应 Python 模块、数据模型和回归；文档修改先读其权威来源和被引用段落；发布修改先读发布文档与脚本帮助。生成的 05–08、schema 等参考索引用于定位符号，具体行为仍以当前源码为准。每次修改前解释问题和改法；每个有教学价值的阶段补充现有 learning 文档。

汇报时分开写明：已由源码、文件、测试、日志、权威资料或实际运行确认的事实；有证据但尚未直接验证的推测；以及仍依赖验证的假设。涉及代码、数据、依赖、版本、接口、运行行为或外部状态时，先查可用证据，不凭空编造结果、接口、版本或行为。验证结论只能覆盖实际证据范围，单元测试通过不等于真实用户流程通过，构建成功不等于正式安装成功。

缺失信息只有在会改变目标、结果、安全性或实现路径时才请求确认；低风险细节采用明确标注的假设继续。初学 Python 时用小步骤和可运行例子教学，保持简单明确、少依赖，避免无收益的抽象和大重写；完成后解释语法、设计、架构位置和下一步学习点。

遵守“只诊断”“先讨论”“执行修改”等控制词。自动发布授权不等于任何真实业务写入授权；外部系统写入、库存确认和业务事实变更仍遵守用户明确的操作边界。

遇到 UI 文案、日志、缓存、SQLite、Excel 或外部系统结果不一致时，沿调用链核对来源、持久事实、时间和状态转换；明确区分扫描、预览、确认、回滚、刷新、操作记录以及代码派生状态。用户说“只诊断”时保持只读。

## 工程与业务边界

- CLI、外部读取解析、业务处理和 UI 各负其责。外部命令非零退出、空输出、无效 JSON 或业务错误码必须形成可诊断结果，并先校验输入；外部适配层返回干净、可验证的数据。
- 不写入凭据，不在示例、日志或汇报中暴露凭据。地址、表格 ID 等配置集中管理，示例放在专门文档。
- 保留工作树中与本任务无关的修改；不删除、重置或覆盖用户已有工作。真实数据库不因重构重建，迁移和 fixture 必须隔离。
- SQLite 持久化订单、材料、硬件、扫描和操作事实；Traveler 按需生成或读取。生产完成不等于工厂单出货；外部出库成功而本地失败时先对账，禁止重复扣减。详见 [业务规则](docs/business-rules.md) 和 [数据模型](docs/architecture/pp-flowhub-data-model.md)。
- 库存检查默认只包含板材和封边，五金按明确选项处理，不比较跨系统单位字符串；库存实时结果不缓存，新功能不新增缓存，保留现有缓存机制。详见 [库存出库规则](docs/inventory-outbound-rules.md)。
- AIMES、Server 扫描、预览、确认、待处理和外部写入的事实边界以 [业务规则](docs/business-rules.md)、[系统架构](docs/architecture/system-architecture.md) 为准，不把警告、扫描结果或投影误报为业务事实。

库存来源、订单材料、硬件身份、生产消耗、外部出库单据和 UI 投影属于不同事实层。修改其中一层前先确认它的来源和写入责任，保留可追溯的原始名称、代码、数量和业务时间；显示别名只在读取层处理，详细约束见 [业务规则](docs/business-rules.md)。

外部系统成功后要核对返回单据和本地事实再决定下一步；刷新或重试不能隐式重复写入。同步镜像、实时来源和历史操作记录也要分别处理，不能用镜像行覆盖真实来源的状态或时长。

## 运行验证与发布

命令帮助可用 `./scripts/pp-flowhub order --help` 和 `./scripts/pp-flowhub inventory --help` 查询；它们是入口参考，不是每次任务都必须执行的仪式。正式门禁使用 `./scripts/test-release`，环境、入口和详细流程以 [README.md](README.md) 与 [docs/release-testing.md](docs/release-testing.md) 为准。

完成代码或 App 修改后，Codex 按发布门禁执行完整测试、一次串行 `./scripts/build-app`，再通过可用的普通 macOS Terminal/Aqua 会话运行绝对路径 `/Users/lantian/Documents/pp-flowhub/scripts/install-app`，完成 Apple Development 签名、正式安装，并验证安装包和实际改动。已有长期授权，无需重复确认安装。

后台会话没有签名 identity 只说明该会话不可用，应优先使用可用普通 Terminal/Aqua；工具明确拒绝或签名安装失败时保留产物并准确报告失败位置，尊重工具限制，不使用降级签名，也不声称已经交付。必要时由 Codex 退出旧 App、重开验证，再退出验证 App 以及本次启动的安装 Terminal，不关闭用户其他终端窗口。

如果自动测试不便执行或代价明显过高，应说明测试目的、人工步骤和预期结果；未执行的验证不能写成通过。纯 Markdown 修改只做差异、链接、命令和一致性检查，不构建、不安装；其他修改执行与其影响相称的回归，并简要报告成功结果，失败时保留定位所需证据。

纯文档修改不改变业务事实，也不应借机修复未授权的代码问题。文档中发现的源码冲突应标出权威来源并单独提出；生成的符号参考由生成器更新，不手工改生成文件。

## 计划与维护

复杂功能、跨模块修改、重大重构或明显架构取舍任一成立时才新建计划；简单修改直接实施。沿用现有 [superpowers/plans](docs/superpowers/plans/) 中的目标、约束、步骤、验证、完成项和剩余决策，并随任务更新；计划文首记录目标、状态、约束、步骤、验证和剩余决策，不为形式新建空目录。

ADR001 的现行原则是不增加无价值的兼容分支，同时保留真实数据与现有迁移；详细历史和数据变更依据见 [ADR-001](docs/architecture/decisions/001-simple-single-path.md) 与 [数据模型](docs/architecture/pp-flowhub-data-model.md)。

项目 Skill 的描述应明确适用任务，支持资料按需读取，避免仅凭宽泛关键词触发；不要因为出现数据库或 Excel 关键词就强制套用 Skill。完成标准是：用户要求已实际实现，必要的错误路径和回归范围已验证，文档与代码入口一致，没有意外的无关文件更改，变更证据、设计原因、下一步学习点、未验证事项和环境阻碍均已准确说明。
