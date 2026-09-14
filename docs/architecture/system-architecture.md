# 系统架构

## 当前运行链路

```text
订单中心：SwiftUI App → `scripts/pp-flowhub order/order-service` → Python 业务引擎

助手：SwiftUI App → `scripts/pp-flowhub assistant`
      → 本地命令解析器 →（未命中时）有限 Agents SDK 结构化路由
      → Typed Tool Gateway → 本地审批状态机 → Python 业务引擎

Python 业务引擎 → Excel / SMB / Playwright / SQLite
```

这是当前已接入的有限结构化 Agent 路径。长期方向才是 SwiftUI App → Workflow Agent → 单一职责 Skills → 确定性 Python Engine → 外部适配；不要把规划中的层误写成已完成能力。

## 分层职责

| 层 | 责任 | 不负责 |
|---|---|---|
| App | 交互、语音转文字、预览、确认、队列 | 解析 Excel 业务规则 |
| 本地解析器 | 将常用语句转为类型化请求 | 写真实系统 |
| Agent | 模糊表达理解、路由、解释 | 直接读写 Excel/SMB/库存 |
| Skill | 稳定流程的域内步骤、规则和引用 | 复制 Python 代码或承载业务算法 |
| Gateway | 工具白名单、参数校验、审批边界 | 业务计算 |
| Python 引擎 | 确定性解析、计算、写入和复查 | 自然语言决策 |
| SQLite | 订单索引、商品主资料、审批、任务、审计、Token 用量 | 密码和登录状态 |

运行数据统一保存在 `~/Documents/pp-flowhub/data/`，该目录在 Git 中整体忽略。`workflow.sqlite3` 保存订单、材料、五金、同步、生产和出库等持久事实；缓存是辅助机制，不能与持久业务事实混为一谈。

## 设计约束

- 只保留一份现行数据契约；商品库首次运行可从既有 XLSX 一次性导入，之后不以 XLSX 作为查询源。具体来源和字段以 [数据模型](pp-flowhub-data-model.md) 为准。
- 常用命令零 Token；当前 Agent 只接收用户语句和一份精简动作契约，不接收订单文件或业务数据。模型和推理参数属于当前实现配置，不是长期架构契约。
- Agent 成功识别的表达按完全相同的规范化文本写入 SQLite；下次直接本地路由，不扩展成模糊通用规则。
- 商品主资料单独保存在 `data/workflow.sqlite3 的 products 表`；每次从库存系统导出 XLSX 后先校验，再事务替换商品表。`data/inventory/current-products.xlsx` 只保留最新一份原始导出备份，运行时查询不依赖 XLSX。
- App 使用单一串行任务队列并显示排队、执行、等待确认、写入和完成状态。排队、读取和等待确认阶段可以取消；文件或库存真实写入开始后不可取消。
- API Key 当前保存在 Git 忽略的 `.env.local`，不进入源码、SQLite 或日志；正式分发前再迁入 Keychain。
- 库存系统密码由 SwiftUI 通过 Security Framework 写入 macOS 登录钥匙串，CLI/Python 通过同项目编译的 `keychain-read` 辅助程序读取；不调用 `/usr/bin/security`，不保存明文或兼容回退。
- Traveler 不是订单查看、库存查询或出库的前置条件；App 的订单中心库存查询直接使用中央 SQLite 订单材料事实，默认仅查询板材和封边，仓库留空，空表按库存 0 处理。该路径不经过 Agent，也不需要审批。Traveler 的生成和独立检查见 [业务规则](../business-rules.md)。
- App 默认进入助手页，使用单一左侧领域导航切换生产文件、出库、待办和设置。页面共享布局与控件尺寸常量，不为不同页面维护独立视觉规则。

## 当前能力与长期边界

- Python 业务模块先承担确定性解析、校验、计算和外部调用；只有稳定、重复且输入输出明确的流程才提炼为 Skill。Skill 的描述应短而具体，引用资料按需读取。
- `traveler_assistant/wecom_service.py` 当前是隔离的 SmartSheet 读取实验，尚未接入 App、Agent 或自动同步；规划中的 SmartSheet 写入不属于当前能力。
- 外部 CLI 适配必须把非零退出、空输出、无效 JSON 和业务错误码转换成可诊断结果，校验输入并返回干净数据；这是开发要求，不代表所有适配器当前都已完成统一实现。
- 配置集中管理地址、表格标识和非敏感规则；不把凭据写入源码、SQLite 或日志。Node、Playwright 等版本按当前环境发现和构建验证，不在本架构文档中硬编码版本号。
- 扫描、预览、确认、刷新和真实写入是不同阶段。Server 扫描可以保存元数据或精确优化证据，不能直接替代材料/五金确认；详细边界见 [业务规则](../business-rules.md) 和 [发布验收](../release-testing.md)。
