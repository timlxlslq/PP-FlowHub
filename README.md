# PP FlowHub

这是一个本地优先的内部 Workflow Assistant。当前主产品是 SwiftUI 生产工作流 App，Python 业务模块和有限的结构化路由正在建设中；现有 Agent/Skills 资料不代表已经接入完整自动 Workflow Agent。应用从 Server 发现订单，按需生成或更新 Work Order Traveler，查询库存，并在用户确认后执行出库。

## 架构

订单中心和助手是两条当前入口，最终共用确定性的 Python 业务模块：

```text
SwiftUI App → scripts/pp-flowhub order / order-service → Python 业务引擎

SwiftUI App → scripts/pp-flowhub assistant
           → 本地命令解析器（常用命令零 Token）
           → 有限 Workflow Agent（仅模糊表达）
           → Typed Tool Gateway + 本地审批
           → Python 业务引擎

Python 业务引擎 → Excel / SMB / Playwright / SQLite
```

Agent 不直接修改 Excel、Server 或库存系统。Agent 不可用时，App 和 CLI 仍可执行本地可确定流程。助手路由只负责把模糊语句转换为结构化动作，Gateway 和 Python 仍负责参数校验、业务规则、审批和写入。

长期分层方向见 [系统架构](docs/architecture/system-architecture.md)。

## Agent 开发环境

Agent 使用 Python 3.10+，当前 macOS App 构建目标为 macOS 26.0。新电脑不要复制旧 `.venv`；请在本机重建环境，以免 Intel/Apple Silicon 原生扩展混用：

```bash
python3 -m venv .venv
.venv/bin/python3 -m pip install "openpyxl==3.1.5" "openai-agents==0.19.2"
```

API Key 保存在被 Git 忽略的 `.env.local`，不会写入源码或 SQLite。构建脚本会从 `.venv` 自动发现 Python 基础运行时，并按显式 `TRAVELER_NODE`、项目 `node_modules` 链接同根的 `bin/node`、PATH 的顺序发现 Node；构建前会拒绝非系统动态库依赖，并在打包后验证 App 内 Node 与 Playwright。必要时可用 `TRAVELER_PYTHON_BASE`、`TRAVELER_NODE` 和 `TRAVELER_NODE_MODULES` 覆盖。

库存系统的 Playwright 操作默认使用后台无头浏览器，不会弹出 Chrome 或抢占键盘、鼠标焦点。只有在处理登录、验证码或排查网页结构时，才临时设置 `TRAVELER_BROWSER_VISIBLE=1` 使用可见浏览器。

库存页面也支持在设置页点击“打开库存专用 Chrome”，打开 `https://www.jdy.com/login/`，由用户手工登录并完成安全验证。后续库存操作会优先复用该 Chrome 中已登录的 `www.jdy.com` 或 `service.jdy.com` 工作台页面；没有可复用页面时，才回退到原有 Playwright 登录流程。普通用户直接打开且没有 CDP 端口的 Chrome 不会被强行接管。

## CLI

```bash
./scripts/pp-flowhub assistant "在服务器上找一下 PP0063"
./scripts/pp-flowhub assistant "给 PP1234-2-LAUNDRY 添加人工五金 M0144 数量 2 备注现场增加"
./scripts/pp-flowhub order list
./scripts/pp-flowhub order preview --folder "/Volumes/server/Optimized Orders/PP0063"
./scripts/pp-flowhub inventory preview --traveler "/path/to/Work Order Traveler(PP0063).xlsx"
```

写入类助手命令首先返回 `approval_required`；确认后用同一命令加 `--approve`。人工五金命令只读取本地商品资料取得名称和规格，不连接实时库存。商品主资料运行时从 `data/workflow.sqlite3` 的 `products` 表查询；库存系统导出的最新原始 XLSX 仅保留为 `data/inventory/current-products.xlsx` 备份。本地解析失败时才转交 Agent。

## 开发验证

正式发布时由 Codex 按 [发布测试与安装流程](docs/release-testing.md) 完成完整门禁；`test-release` 已包含全量 Python、macOS UI、AIMES 离线表格、工作簿 E2E 和差异检查，不要再重复执行其中的子测试：

```bash
./scripts/test-release
./scripts/build-app
```

构建成功后，Codex 会通过可用的普通 macOS Terminal/Aqua 会话自动运行绝对路径 `/Users/lantian/Documents/pp-flowhub/scripts/install-app`，完成正式签名安装和安装版检查；详细规则见上述流程文档。

正式业务规则见 [docs/business-rules.md](docs/business-rules.md)，系统分层见 [docs/architecture/system-architecture.md](docs/architecture/system-architecture.md)。

版本变更见 [更新日志](CHANGELOG.md)。

学习和接手建议从以下入口开始：

- [接手学习指南](docs/learning/04-handoff-guide.md)：阅读顺序、数据边界和安全修改方法。
- [全文件中文地图](docs/learning/05-file-map.md)：逐文件说明职责。
- [Python 全符号中文参考](docs/learning/06-python-symbol-reference.md)：每个类型、函数、参数、返回和静态下一跳。
- [Swift/macOS 全符号中文参考](docs/learning/07-swift-symbol-reference.md)：每个 App 类型、过程、计算属性和静态下一跳。
- [测试、脚本与工具全符号中文参考](docs/learning/08-support-test-symbol-reference.md)：测试意图和辅助过程。
- [用户操作与业务调用链全解](docs/learning/09-user-operation-call-chains.md)：从页面入口到 CLI、Python、SQLite/Excel/外部系统的人工校验链路。
- [Product Design 订单中心审查](docs/learning/10-product-design-order-center-audit.md)：基于已安装 App 截图的真实页面状态、UX 问题和后续设计探索建议。
- [数据库与 WeCom 同步学习说明](docs/learning/11-database-guide.md)：中央 SQLite 路径、连接/事务边界、表关系和隔离教学示例。
- [数据库地图](docs/learning/12-database-map.md)：两个正式 SQLite 运行库的角色、表分层和完整字段入口。
- [2026-09-12 数据库字段历史快照](docs/learning/database-map/current-schema.md)：材料 SKU 外键迁移前两个运行库的表字段、约束和源码证据；现行结构以数据模型、当前源码和迁移后数据库 PRAGMA 为准。
