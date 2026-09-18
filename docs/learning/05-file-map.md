# PP FlowHub 全文件中文地图

> 本文件由 `tools/generate_code_reference.py` 从当前工作区生成。请不要手工修改；代码或文件结构变化后重新运行生成器。

## 1. 覆盖范围

- 当前 Git 共追踪 **400** 个文件；连同本次新增但可能尚未进入 Git 索引的文档，共登记 **400** 个文件。
- `vendor/` 是固定打包的第三方依赖：保留逐文件登记，但不把其内部函数当作 PP FlowHub 业务代码解释。
- `data/`、`.env.local`、构建目录和安装版属于本机运行状态，通常不受 Git 追踪；只登记文件用途，不读取其内容。
- `outputs/` 是历史诊断或交付证据，不属于正式 App 运行链路。

## 2. Git 追踪文件

| 文件 | 中文职责 | 一方符号数 |
| --- | --- | ---: |
| `"docs/\350\277\201\347\247\273\351\241\271\347\233\256\345\210\260Cursor\346\214\207\345\215\227.md"` | 项目配置、资源或辅助文件。 | 0 |
| `"outputs/pp0018-material-cost/previews/\344\273\267\346\240\274\344\270\216\346\235\245\346\272\220.png"` | 项目配置、资源或辅助文件。 | 0 |
| `"outputs/pp0018-material-cost/previews/\346\235\220\346\226\231\346\210\220\346\234\254\346\261\207\346\200\273.png"` | 项目配置、资源或辅助文件。 | 0 |
| `.gitignore` | Git 忽略规则：排除本地状态、构建产物和敏感配置。 | 0 |
| `.superpowers/tasks/pending-center-tasks12/REPORT.md` | 项目配置、资源或辅助文件。 | 0 |
| `.superpowers/tasks/pending-center-tasks12/baseline/macos/TravelerAssistant.swift` | Swift/macOS 源码或测试辅助文件。 | 397 |
| `.superpowers/tasks/pending-center-tasks12/baseline/tests/test_macos_ui.swift` | Swift/macOS 源码或测试辅助文件。 | 61 |
| `.superpowers/tasks/pending-center-tasks12/review-baseline/macos/TravelerAssistant.swift` | Swift/macOS 源码或测试辅助文件。 | 401 |
| `.superpowers/tasks/pending-center-tasks12/review-baseline/tests/test_macos_ui.swift` | Swift/macOS 源码或测试辅助文件。 | 63 |
| `.superpowers/tasks/pending-center-tasks12/review-fix.patch` | 项目配置、资源或辅助文件。 | 0 |
| `.superpowers/tasks/pending-center-tasks12/task-only.patch` | 项目配置、资源或辅助文件。 | 0 |
| `AGENTS.md` | 项目协作规则：规定判断、验证、发布和汇报要求。 | 0 |
| `CHANGELOG.md` | 项目配置、资源或辅助文件。 | 0 |
| `README.md` | 项目总入口：介绍用途、安装、运行方式和文档导航。 | 0 |
| `assets/icon-candidates/app-icon-previous-backup.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icon-candidates/work-assistant-1-blue-check.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icon-candidates/work-assistant-2-flow-ribbon.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icon-candidates/work-assistant-3-teal-spark-refined-v2.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icon-candidates/work-assistant-3-teal-spark.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icons/AppIcon.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icons/workflow-blueprint.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icons/workflow-high-contrast-selected.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icons/workflow-materials-selected.png` | App 图标或界面视觉候选资源。 | 0 |
| `assets/icons/workflow-route.png` | App 图标或界面视觉候选资源。 | 0 |
| `docs/architecture/decisions/001-simple-single-path.md` | 项目文档：ADR-001：只保留单一现行路径。 | 0 |
| `docs/architecture/pp-flowhub-data-model.md` | 项目文档：PP FlowHub 数据模型与边界。 | 0 |
| `docs/architecture/system-architecture.md` | 项目文档：系统架构。 | 0 |
| `docs/business-rules.md` | 项目文档：已确认业务规则。 | 0 |
| `docs/diagnostics/pp0008-rail-pair-repair-20260910-085146.json` | 项目文档：pp0008-rail-pair-repair-20260910-085146。 | 0 |
| `docs/diagnostics/scan-server-app-trace-2026-08-14.md` | 项目文档：工作流程助手真实启动扫描 Server 追踪（2026-08-14）。 | 0 |
| `docs/diagnostics/scan-server-trace-2026-08-14.md` | 项目文档：`scan-server` 实际运行追踪（2026-08-14）。 | 0 |
| `docs/inventory-outbound-rules.md` | 项目文档：库存查询与出库契约。 | 0 |
| `docs/learning/00-architecture-overview.md` | 项目文档：学习：为什么是 App + Agent + Skills。 | 0 |
| `docs/learning/01-complete-architecture-and-business-flow.md` | 项目文档：PP FlowHub：完整技术架构与业务流程。 | 0 |
| `docs/learning/02-macos-code-signing-tcc.md` | 项目文档：macOS Code Signing、Bundle Identifier 与 TCC 权限。 | 0 |
| `docs/learning/03-server-scan-performance-observation.md` | 项目文档：Server 扫描性能观测。 | 0 |
| `docs/learning/04-handoff-guide.md` | 项目文档：PP FlowHub 接手学习指南。 | 0 |
| `docs/learning/05-file-map.md` | 项目文档：PP FlowHub 全文件中文地图。 | 0 |
| `docs/learning/06-python-symbol-reference.md` | 项目文档：PP FlowHub Python 全符号中文参考。 | 0 |
| `docs/learning/07-swift-symbol-reference.md` | 项目文档：PP FlowHub Swift/macOS 全符号中文参考。 | 0 |
| `docs/learning/08-support-test-symbol-reference.md` | 项目文档：PP FlowHub 测试、脚本与工具全符号中文参考。 | 0 |
| `docs/learning/09-user-operation-call-chains.md` | 项目文档：PP FlowHub 用户操作与业务调用链全解。 | 0 |
| `docs/learning/10-product-design-order-center-audit.md` | 项目文档：Product Design 审查：订单中心主流程。 | 0 |
| `docs/learning/10-visual-architecture-map.md` | 项目文档：PP FlowHub 结构图与入口调用链。 | 0 |
| `docs/learning/11-database-guide.md` | 项目文档：学习：把外部数据保存到 PP FlowHub 的 SQLite。 | 0 |
| `docs/learning/12-database-map.md` | 项目文档：数据库地图：当前文件、角色与 SKU 关系。 | 0 |
| `docs/learning/database-map/current-schema.md` | 项目文档：2026-09-12 数据库字段历史快照。 | 0 |
| `docs/learning/pending-center-preview/PendingCenterPreview.swift` | 项目文档：PendingCenterPreview。 | 36 |
| `docs/learning/product-design-audit/01-order-center-loading.jpeg` | 项目文档：8#f#�#�#�$$M$|$�$�%	%8%h%�%�%�&'&W&�&�&�''I'z'�'�(。 | 0 |
| `docs/learning/product-design-audit/02-order-center-loaded.jpeg` | 项目文档：8#f#�#�#�$$M$|$�$�%	%8%h%�%�%�&'&W&�&�&�''I'z'�'�(。 | 0 |
| `docs/learning/product-design-audit/03-order-detail.jpeg` | 项目文档：8#f#�#�#�$$M$|$�$�%	%8%h%�%�%�&'&W&�&�&�''I'z'�'�(。 | 0 |
| `docs/learning/product-design-audit/04-pending-center.jpeg` | 项目文档：8#f#�#�#�$$M$|$�$�%	%8%h%�%�%�&'&W&�&�&�''I'z'�'�(。 | 0 |
| `docs/learning/product-design-audit/05-inventory-comparison-loading.jpeg` | 项目文档：8#f#�#�#�$$M$|$�$�%	%8%h%�%�%�&'&W&�&�&�''I'z'�'�(。 | 0 |
| `docs/learning/product-design-audit/06-order-row-actions.jpeg` | 项目文档：8#f#�#�#�$$M$|$�$�%	%8%h%�%�%�&'&W&�&�&�''I'z'�'�(。 | 0 |
| `docs/operation-logging.md` | 项目文档：操作日志。 | 0 |
| `docs/order-dashboard-prototype-spec.md` | 项目文档：订单看板界面与操作原型规格。 | 0 |
| `docs/project-handoff-log.md` | 项目文档：项目交接记录。 | 0 |
| `docs/project-static-context.md` | 项目文档：PP FlowHub 静态上下文。 | 0 |
| `docs/release-testing.md` | 项目文档：发布测试与安装验收。 | 0 |
| `docs/superpowers/plans/2026-09-02-pending-center-workflow-plan.md` | 项目文档：待处理中心工作流 Implementation Plan。 | 0 |
| `docs/superpowers/plans/2026-09-14-folder-manual-handling.md` | 项目文档：临时及混合补单文件夹人工登记。 | 0 |
| `docs/superpowers/plans/2026-09-15-confirmed-material-optimization.md` | 项目文档：材料确认写入后才完成优化。 | 0 |
| `docs/superpowers/plans/2026-09-15-material-sku-normalization.md` | 项目文档：订单材料以 SKU 关联商品主资料。 | 0 |
| `docs/superpowers/specs/2026-09-02-pending-center-workflow-design.md` | 项目文档：待处理中心工作流设计。 | 0 |
| `macos/AssistantView.swift` | 助手页面、语音输入、任务队列和业务进度轨道。 | 75 |
| `macos/Info.plist` | macOS App 的权限声明、Bundle 配置和系统元数据。 | 0 |
| `macos/OperationLog.swift` | App 端操作日志读取、展示、脱敏和清理。 | 23 |
| `macos/OrderDashboardView.swift` | 订单看板、待处理中心、订单详情及生产/出库交互。 | 286 |
| `macos/TravelerAssistant.swift` | App 入口与 AppModel：全局状态、页面、子进程和业务编排。 | 434 |
| `outputs/019fe269-fc5a-7fa2-aa70-62173698f0c7/PP0067-material-final/Sheet1.png` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019fe269-fc5a-7fa2-aa70-62173698f0c7/build_material_template.mjs` | 历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。 | 0 |
| `outputs/019fe269-fc5a-7fa2-aa70-62173698f0c7/material-reference/manual-material-reference.png` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019fe269-fc5a-7fa2-aa70-62173698f0c7/material-template/Order Materials.png` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019fe269-fc5a-7fa2-aa70-62173698f0c7/material-template/Order Materials.xlsx` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019fe269-fc5a-7fa2-aa70-62173698f0c7/material-template/Order Materials.xlsx.inspect.ndjson` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019fe269-fc5a-7fa2-aa70-62173698f0c7/render_material_reference.mjs` | 历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。 | 0 |
| `outputs/019ff173-07cd-75d3-a5e7-5ef8c8ec6992/PP0035-2-material-after.png` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019ff173-07cd-75d3-a5e7-5ef8c8ec6992/PP0035-2-material-after.xlsx` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019ff173-07cd-75d3-a5e7-5ef8c8ec6992/PP0035-2-material-before.png` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/019ff173-07cd-75d3-a5e7-5ef8c8ec6992/inspect_repaired_material.mjs` | 历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。 | 0 |
| `outputs/019ff173-07cd-75d3-a5e7-5ef8c8ec6992/inspect_server_material.mjs` | 历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。 | 0 |
| `outputs/019ff173-07cd-75d3-a5e7-5ef8c8ec6992/test_server_material_repair.py` | 历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。 | 0 |
| `outputs/pp0018-material-cost/PP0018_material_cost_by_room.xlsx` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/pp0018-material-cost/PP0018_material_cost_by_room.xlsx.inspect.ndjson` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `outputs/pp0018-material-cost/build_pp0018.mjs` | 历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。 | 0 |
| `outputs/pp0018-material-cost/extract_pp0018.py` | 历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。 | 8 |
| `outputs/pp0018-material-cost/material_data.json` | 历史诊断、工作簿或视觉核对产物，用于保留交付证据。 | 0 |
| `pyproject.toml` | Python 项目元数据、依赖和测试配置。 | 0 |
| `resources/panel-images/M0005_Olmo_3.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0007_Frappe_1.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0009_Cross_Metal_Champagne.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0011_Textil_Plata.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0013_Ida_1.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0015_Ida_2.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0017_Woodline_3.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0019_Woodline_4.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0021_Rosales_3.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0023_Nocce_1.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0027_Nocce_3.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0029_Como_Ash_2.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0031_Como_Ash_3.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0033_Picasso_1.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0035_Picasso_2.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0037_Picasso_3.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0039_Gris_Plomo_HG.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0041_Blanco_HG.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0043_Blanco_Polar_HG.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0045_Black_HG.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0047_Azul_Indigo_HG.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0049_Cashmere_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0051_Verde_Salvia_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0053_Gris_Nube_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0055_Blanco_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0057_Black_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0059_Azul_Marino_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0061_Agave_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0063_Blanco_Polar_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0065_Basalto_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M0067_Antracita_SM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M1028_Nocce_1_8mm.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M1105_Como_Ash_2_8mm.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M1107_Cashmere_SM-8MM.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M1109_Ida_1_9mm.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M1134_Rosales_3_8mm.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/panel-images/M1143_Frappe_3.jpg` | 订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。 | 0 |
| `resources/status-icons/status-icon-optimization.png` | 图片资源或视觉验证产物。 | 0 |
| `resources/status-icons/status-icon-production.png` | 图片资源或视觉验证产物。 | 0 |
| `resources/status-icons/status-icon-split.png` | 图片资源或视觉验证产物。 | 0 |
| `resources/templates/Order Materials.xlsx` | 受业务结构约束的 Excel 模板；生成流程在副本上写入。 | 0 |
| `resources/templates/Work Order Traveler.xlsx` | 受业务结构约束的 Excel 模板；生成流程在副本上写入。 | 0 |
| `scripts/build-app` | 构建 PP FlowHub.app，组装 Swift、Python、资源和辅助工具。 | 1 |
| `scripts/install-app` | 签名、校验并把构建产物安装到 /Applications。 | 1 |
| `scripts/pp-flowhub` | 统一命令入口：选择 Python 运行时并分发 assistant/order/inventory 子命令。 | 1 |
| `scripts/test-aimes-table` | 项目配置、资源或辅助文件。 | 1 |
| `scripts/test-macos-ui` | 编译并运行 Swift/macOS 源码契约与 UI 回归测试。 | 1 |
| `scripts/test-release` | 正式发布测试门禁：串联 Python、Swift UI 和工作簿测试。 | 1 |
| `scripts/test-workbook-e2e` | 用固定样本执行 Traveler/材料工作簿端到端验证。 | 3 |
| `skills/inventory-management/SKILL.md` | 项目内业务 Skill 入口：规定 Agent 使用该业务能力时的步骤和边界。 | 0 |
| `skills/inventory-management/agents/openai.yaml` | 业务 Skill 的 Agent 展示名称、说明和默认提示配置。 | 0 |
| `skills/inventory-management/references/outbound.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `skills/inventory-management/references/stock-check.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `skills/order-management/SKILL.md` | 项目内业务 Skill 入口：规定 Agent 使用该业务能力时的步骤和边界。 | 0 |
| `skills/order-management/agents/openai.yaml` | 业务 Skill 的 Agent 展示名称、说明和默认提示配置。 | 0 |
| `skills/order-management/references/discovery.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `skills/order-management/references/mixed-orders.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `skills/traveler-management/SKILL.md` | 项目内业务 Skill 入口：规定 Agent 使用该业务能力时的步骤和边界。 | 0 |
| `skills/traveler-management/agents/openai.yaml` | 业务 Skill 的 Agent 展示名称、说明和默认提示配置。 | 0 |
| `skills/traveler-management/references/create.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `skills/traveler-management/references/manual-hardware.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `skills/traveler-management/references/update.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `skills/traveler-management/references/workbook-contract.md` | 项目内业务 Skill 的专项参考规则。 | 0 |
| `tests/test_aimes_table.mjs` | 自动化测试：验证 `aimes_table` 模块或业务场景。 | 3 |
| `tests/test_command_router.py` | 自动化测试：验证 `command_router` 模块或业务场景。 | 13 |
| `tests/test_confirmed_material_optimization.py` | 自动化测试：验证 `confirmed_material_optimization` 模块或业务场景。 | 20 |
| `tests/test_core.py` | 自动化测试：验证 `core` 模块或业务场景。 | 18 |
| `tests/test_costing.py` | 自动化测试：验证 `costing` 模块或业务场景。 | 6 |
| `tests/test_folder_manual_handling.py` | 自动化测试：验证 `folder_manual_handling` 模块或业务场景。 | 18 |
| `tests/test_hardware_facts.py` | 自动化测试：验证 `hardware_facts` 模块或业务场景。 | 10 |
| `tests/test_inventory.py` | 自动化测试：验证 `inventory` 模块或业务场景。 | 98 |
| `tests/test_legacy_fittings.py` | 自动化测试：验证 `legacy_fittings` 模块或业务场景。 | 2 |
| `tests/test_macos_ui.swift` | 自动化测试：验证 `macos_ui` 模块或业务场景。 | 75 |
| `tests/test_material_sku_contract.py` | 自动化测试：验证 `material_sku_contract` 模块或业务场景。 | 22 |
| `tests/test_material_sku_outbound_history.py` | 自动化测试：验证 `material_sku_outbound_history` 模块或业务场景。 | 12 |
| `tests/test_operation_log.py` | 自动化测试：验证 `operation_log` 模块或业务场景。 | 4 |
| `tests/test_order_details.py` | 自动化测试：验证 `order_details` 模块或业务场景。 | 3 |
| `tests/test_order_index.py` | 自动化测试：验证 `order_index` 模块或业务场景。 | 129 |
| `tests/test_order_service.py` | 自动化测试：验证 `order_service` 模块或业务场景。 | 5 |
| `tests/test_order_workflow.py` | 自动化测试：验证 `order_workflow` 模块或业务场景。 | 56 |
| `tests/test_production.py` | 自动化测试：验证 `production` 模块或业务场景。 | 7 |
| `tests/test_report_selection.py` | 自动化测试：验证 `report_selection` 模块或业务场景。 | 10 |
| `tests/test_runtime_store.py` | 自动化测试：验证 `runtime_store` 模块或业务场景。 | 7 |
| `tests/test_security.py` | 自动化测试：验证 `security` 模块或业务场景。 | 3 |
| `tests/test_server_rail_units.py` | 自动化测试：验证 `server_rail_units` 模块或业务场景。 | 11 |
| `tests/test_workflow_database.py` | 自动化测试：验证 `workflow_database` 模块或业务场景。 | 8 |
| `tools/aimes_lookup.mjs` | 通过浏览器自动化查询 AIMES 工厂单名称和近期订单。 | 4 |
| `tools/aimes_table.mjs` | Node.js ES Module 辅助脚本。 | 3 |
| `tools/generate_code_reference.py` | 静态扫描一方源码，生成中文文件地图和符号索引。 | 35 |
| `tools/jdy_inventory.mjs` | 通过浏览器自动化读取库存、填单并执行金蝶云出库。 | 24 |
| `tools/keychain_read.swift` | 从 macOS Keychain 读取指定服务的凭据。 | 0 |
| `tools/repair_hardware_history.py` | Python 源码或一次性辅助文件。 | 5 |
| `tools/verify_workbook.mjs` | 用 LibreOffice/Node 辅助校验工作簿可打开性与结构。 | 0 |
| `traveler_assistant/__init__.py` | Python 包标识；不承载业务逻辑。 | 0 |
| `traveler_assistant/agent_runner.py` | Agent 路由适配层：把模糊自然语言转换为结构化动作。 | 5 |
| `traveler_assistant/assistant_cli.py` | 助手 CLI 入口：选择本地解析、学习缓存或 Agent，再进入 Gateway。 | 4 |
| `traveler_assistant/backup.py` | 数据与配置备份、状态检查和保留策略。 | 4 |
| `traveler_assistant/command_router.py` | 常用中英文命令的确定性本地解析器。 | 5 |
| `traveler_assistant/core.py` | 共享配置、错误、进度、AIMES 查询和五金解析基础能力。 | 40 |
| `traveler_assistant/costing.py` | 订单成本计算、展示排序和 Excel 导出。 | 12 |
| `traveler_assistant/database.py` | 中央 SQLite 路径、Schema、迁移和通用缓存读写。 | 28 |
| `traveler_assistant/fittings.py` | 五金记录签名与最新来源选择规则。 | 6 |
| `traveler_assistant/hardware_facts.py` | Python 源码或一次性辅助文件。 | 8 |
| `traveler_assistant/hardware_source_decisions.py` | Python 源码或一次性辅助文件。 | 5 |
| `traveler_assistant/inventory.py` | 库存需求、商品映射、预检、浏览器出库和出库留痕。 | 154 |
| `traveler_assistant/operation_log.py` | JSONL 操作日志、脱敏和数据库语句记录。 | 14 |
| `traveler_assistant/order_details.py` | 从中央事实组装订单详情和 Panel 展示数据。 | 1 |
| `traveler_assistant/order_index.py` | 订单索引核心：AIMES、Server、问题、确认、状态与同步证据。 | 234 |
| `traveler_assistant/order_service.py` | Python 源码或一次性辅助文件。 | 3 |
| `traveler_assistant/order_workflow.py` | 订单文件解析、预览、Traveler/材料工作簿生成与更新。 | 101 |
| `traveler_assistant/production.py` | 生产备料预览、生产完成记录和出货前置校验。 | 18 |
| `traveler_assistant/report_read_context.py` | Python 源码或一次性辅助文件。 | 8 |
| `traveler_assistant/runtime_store.py` | 助手学习命令与 Agent Token 用量的 SQLite 存储。 | 10 |
| `traveler_assistant/streaming_process.py` | Python 源码或一次性辅助文件。 | 1 |
| `traveler_assistant/test.json` | 项目配置、资源或辅助文件。 | 0 |
| `traveler_assistant/test1.py` | Python 源码或一次性辅助文件。 | 0 |
| `traveler_assistant/test_data.py` | 创建隔离的本地测试订单和工作簿样本。 | 5 |
| `traveler_assistant/tool_gateway.py` | Typed Tool Gateway：审批校验和确定性业务动作分发。 | 2 |
| `traveler_assistant/wecom_service.py` | Python 源码或一次性辅助文件。 | 9 |
| `vendor/et_xmlfile/__init__.py` | 第三方 et_xmlfile 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/et_xmlfile/incremental_tree.py` | 第三方 et_xmlfile 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/et_xmlfile/xmlfile.py` | 第三方 et_xmlfile 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/_constants.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/cell/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/cell/_writer.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/cell/cell.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/cell/read_only.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/cell/rich_text.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/cell/text.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/_3d.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/area_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/axis.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/bar_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/bubble_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/chartspace.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/data_source.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/descriptors.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/error_bar.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/label.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/layout.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/legend.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/line_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/marker.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/picture.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/pie_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/pivot.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/plotarea.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/print_settings.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/radar_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/reader.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/reference.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/scatter_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/series.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/series_factory.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/shapes.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/stock_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/surface_chart.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/text.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/title.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/trendline.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chart/updown_bars.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/chartsheet.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/custom.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/properties.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/protection.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/publish.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/relation.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/chartsheet/views.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/comments/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/comments/author.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/comments/comment_sheet.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/comments/comments.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/comments/shape_writer.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/compat/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/compat/abc.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/compat/numbers.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/compat/product.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/compat/singleton.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/compat/strings.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/base.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/container.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/excel.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/namespace.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/nested.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/sequence.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/serialisable.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/descriptors/slots.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/colors.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/connector.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/drawing.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/effect.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/fill.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/geometry.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/graphic.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/image.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/line.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/picture.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/properties.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/relation.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/spreadsheet_drawing.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/text.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/drawing/xdr.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/formatting/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/formatting/formatting.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/formatting/rule.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/formula/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/formula/tokenizer.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/formula/translate.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/core.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/custom.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/extended.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/interface.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/manifest.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/relationship.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/packaging/workbook.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/pivot/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/pivot/cache.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/pivot/fields.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/pivot/record.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/pivot/table.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/reader/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/reader/drawings.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/reader/excel.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/reader/strings.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/reader/workbook.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/alignment.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/borders.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/builtins.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/cell_style.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/colors.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/differential.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/fills.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/fonts.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/named_styles.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/numbers.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/protection.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/proxy.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/styleable.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/stylesheet.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/styles/table.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/bound_dictionary.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/cell.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/dataframe.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/datetime.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/escape.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/exceptions.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/formulas.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/indexed_list.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/inference.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/protection.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/utils/units.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/_writer.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/child.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/defined_name.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/external_link/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/external_link/external.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/external_reference.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/function_group.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/properties.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/protection.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/smart_tags.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/views.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/web.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/workbook/workbook.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/_read_only.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/_reader.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/_write_only.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/_writer.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/cell_range.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/cell_watch.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/controls.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/copier.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/custom.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/datavalidation.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/dimensions.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/drawing.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/errors.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/filters.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/formula.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/header_footer.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/hyperlink.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/merge.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/ole.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/page.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/pagebreak.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/picture.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/print_settings.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/properties.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/protection.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/related.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/scenario.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/smart_tag.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/table.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/views.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/worksheet/worksheet.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/writer/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/writer/excel.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/writer/theme.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/xml/__init__.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/xml/constants.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |
| `vendor/openpyxl/xml/functions.py` | 第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。 | 0 |

## 3. 本机运行时文件（不读取内容）

| 文件 | 中文职责 |
| --- | --- |
| `data/assistant-runtime.sqlite3` | 助手学习命令与 Token 用量数据库。 |
| `data/operation-log.jsonl` | 脱敏后的操作审计和分阶段耗时日志。 |
| `data/order-index.sqlite3` | 旧版订单索引数据库；当前事实边界以 workflow.sqlite3 及迁移规则为准。 |
| `data/server-scan-snapshot.json` | Server 扫描元数据快照。 |
| `data/settings.json` | 本机路径、账号名和功能设置；密码不应明文保存在这里。 |
| `data/todo-items.json` | App 待办事项。 |
| `data/workflow.sqlite3` | 中央业务事实数据库。 |

## 4. 不纳入逐文件表的本机目录

- `.git/`：Git 内部对象与索引，不是项目业务代码。
- `.venv/`：本机 Python 虚拟环境，可由依赖配置重建。
- `build/`、`runtime/`：构建或打包产物，可由构建脚本重建。
- `.env.local`：本机敏感/环境配置，只登记存在性，不输出内容。
