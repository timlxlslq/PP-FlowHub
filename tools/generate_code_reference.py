#!/usr/bin/env python3
"""生成 PP FlowHub 的中文文件地图和源码符号索引。

本工具只读取源码并写入 ``docs/learning/05`` 至 ``08`` 四份文档，不会读取
Excel/SQLite/JSON 的业务内容。它使用静态分析整理函数签名和直接调用；动态分发、
闭包和运行时类型绑定仍应以人工维护的业务调用链文档为准。
"""

from __future__ import annotations

import ast
import re
import subprocess
from dataclasses import dataclass, field
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
LEARNING_DIR = ROOT / "docs" / "learning"

OUTPUTS = {
    "files": LEARNING_DIR / "05-file-map.md",
    "python": LEARNING_DIR / "06-python-symbol-reference.md",
    "swift": LEARNING_DIR / "07-swift-symbol-reference.md",
    "support": LEARNING_DIR / "08-support-test-symbol-reference.md",
}

EXCLUDED_SCAN_ROOTS = {".git", ".venv", "build", "runtime", "vendor"}
SIDE_EFFECT_WORDS = {
    "commit",
    "execute",
    "executemany",
    "save",
    "write",
    "replace",
    "unlink",
    "mkdir",
    "copy",
    "move",
    "run",
    "Popen",
    "Process",
    "launch",
    "open",
    "close",
    "outbound",
    "record",
    "insert",
    "update",
    "delete",
    "upsert",
    "set",
}
COMMON_CALL_NAMES = {
    "append",
    "compactMap",
    "contains",
    "enumerated",
    "filter",
    "flatMap",
    "forEach",
    "get",
    "items",
    "joined",
    "keys",
    "map",
    "max",
    "min",
    "next",
    "pop",
    "reduce",
    "reversed",
    "setdefault",
    "sorted",
    "split",
    "strip",
    "update",
    "values",
    "zip",
}

FILE_PURPOSES = {
    "AGENTS.md": "项目协作规则：规定判断、验证、发布和汇报要求。",
    "README.md": "项目总入口：介绍用途、安装、运行方式和文档导航。",
    ".gitignore": "Git 忽略规则：排除本地状态、构建产物和敏感配置。",
    "pyproject.toml": "Python 项目元数据、依赖和测试配置。",
    "macos/Info.plist": "macOS App 的权限声明、Bundle 配置和系统元数据。",
    "scripts/pp-flowhub": "统一命令入口：选择 Python 运行时并分发 assistant/order/inventory 子命令。",
    "scripts/build-app": "构建 PP FlowHub.app，组装 Swift、Python、资源和辅助工具。",
    "scripts/install-app": "签名、校验并把构建产物安装到 /Applications。",
    "scripts/test-release": "正式发布测试门禁：串联 Python、Swift UI 和工作簿测试。",
    "scripts/test-macos-ui": "编译并运行 Swift/macOS 源码契约与 UI 回归测试。",
    "scripts/test-workbook-e2e": "用固定样本执行 Traveler/材料工作簿端到端验证。",
    "tools/aimes_lookup.mjs": "通过浏览器自动化查询 AIMES 工厂单名称和近期订单。",
    "tools/jdy_inventory.mjs": "通过浏览器自动化读取库存、填单并执行金蝶云出库。",
    "tools/keychain_read.swift": "从 macOS Keychain 读取指定服务的凭据。",
    "tools/verify_workbook.mjs": "用 LibreOffice/Node 辅助校验工作簿可打开性与结构。",
    "tools/generate_code_reference.py": "静态扫描一方源码，生成中文文件地图和符号索引。",
    "traveler_assistant/__init__.py": "Python 包标识；不承载业务逻辑。",
    "traveler_assistant/agent_runner.py": "Agent 路由适配层：把模糊自然语言转换为结构化动作。",
    "traveler_assistant/assistant_cli.py": "助手 CLI 入口：选择本地解析、学习缓存或 Agent，再进入 Gateway。",
    "traveler_assistant/backup.py": "数据与配置备份、状态检查和保留策略。",
    "traveler_assistant/command_router.py": "常用中英文命令的确定性本地解析器。",
    "traveler_assistant/core.py": "共享配置、错误、进度、AIMES 查询和五金解析基础能力。",
    "traveler_assistant/costing.py": "订单成本计算、展示排序和 Excel 导出。",
    "traveler_assistant/database.py": "中央 SQLite 路径、Schema、迁移和通用缓存读写。",
    "traveler_assistant/fittings.py": "五金记录签名与最新来源选择规则。",
    "traveler_assistant/inventory.py": "库存需求、商品映射、预检、浏览器出库和出库留痕。",
    "traveler_assistant/operation_log.py": "JSONL 操作日志、脱敏和数据库语句记录。",
    "traveler_assistant/order_details.py": "从中央事实组装订单详情和 Panel 展示数据。",
    "traveler_assistant/order_index.py": "订单索引核心：AIMES、Server、问题、确认、状态与同步证据。",
    "traveler_assistant/order_workflow.py": "订单文件解析、预览、Traveler/材料工作簿生成与更新。",
    "traveler_assistant/production.py": "生产备料预览、生产完成记录和出货前置校验。",
    "traveler_assistant/runtime_store.py": "助手学习命令与 Agent Token 用量的 SQLite 存储。",
    "traveler_assistant/test_data.py": "创建隔离的本地测试订单和工作簿样本。",
    "traveler_assistant/tool_gateway.py": "Typed Tool Gateway：审批校验和确定性业务动作分发。",
    "macos/AssistantView.swift": "助手页面、语音输入、任务队列和业务进度轨道。",
    "macos/OperationLog.swift": "App 端操作日志读取、展示、脱敏和清理。",
    "macos/OrderDashboardView.swift": "订单看板、待处理中心、订单详情及生产/出库交互。",
    "macos/TravelerAssistant.swift": "App 入口与 AppModel：全局状态、页面、子进程和业务编排。",
}

SYMBOL_PURPOSES = {
    "main": "解析命令行参数，建立运行配置并分发到对应业务动作。",
    "parse_local_command": "把常见自然语言命令解析为无副作用的结构化本地命令；无法确定时返回 None。",
    "execute_local_command": "校验结构化命令、审批状态和参数，再分发到确定性业务函数。",
    "route_with_agent": "调用 Agent，把本地解析器无法处理的文本转换为受约束的动作决定。",
    "preview_order": "读取一个订单文件夹，校验归属并组装材料、封边、工厂单和五金预览。",
    "generate_order_traveler": "根据订单预览和模板生成新的 Traveler，并在保存后重新打开校验。",
    "update_order_traveler": "备份并升级已有 Traveler，保留人工数据后写入最新业务事实。",
    "build_preview": "解析 Traveler 并结合商品目录/映射生成只读库存预检。",
    "build_database_preview": "从中央 SQLite 事实生成订单级库存/出库预检，不依赖 Traveler 作为事实源。",
    "check_stock": "调用库存读取流程并比较需求量、可用量与缺口。",
    "inventory_main": "库存 CLI 入口：解析子命令并调用查询、映射、预检或出库流程。",
    "sync_aimes_index": "刷新 AIMES 工厂单身份事实并更新订单索引；不隐式扫描 Server。",
    "scan_server_changes": "扫描候选 Server 文件夹和业务文件变化，返回待确认项与分阶段耗时。",
    "preview_server_changes": "在克隆数据库上演算 Server 变化，生成不会污染正式事实的确认预览。",
    "confirm_server_preview": "验证预览仍与当前文件一致后，把已确认 Server 事实写入中央数据库。",
    "mark_temporary_folder_manual": "登记临时 Server 文件夹已人工出库，并建立三天 XML 观察期。",
    "sync_order_index": "把 AIMES、Server 和本地事实同步为可供看板读取的订单索引。",
    "list_order_index": "读取订单、工厂单、问题和状态，生成看板列表 payload。",
    "reconcile_outbound_statuses": "依据工厂单范围与出库证据重新计算订单/工厂单出库状态。",
    "production_preview": "从中央数据库汇总尚需生产的材料并生成只读生产预览。",
    "prepare_production": "校验生产选择并保存本次生产准备范围。",
    "record_completed_production": "写入已完成生产事实并返回更新后的状态。",
    "calculate_order_cost": "从中央事实、商品编码和价格计算订单成本明细与汇总。",
    "export_order_cost": "把订单成本明细写入 Excel 并保持规定的展示顺序。",
    "runAssistantCommand": "把助手输入加入任务队列，并启动后续命令执行。",
    "executeAssistantTask": "启动助手子进程、消费输出并把结果映射为页面状态。",
    "startOrderDashboard": "启动订单中心初始化链路，加载缓存并安排 AIMES/Server 刷新。",
    "syncDashboardAimes": "从 App 发起 AIMES 同步，解析结果并衔接后续看板刷新。",
    "scanDashboardServer": "从 App 发起 Server 扫描并把变化、问题和耗时写入看板状态。",
    "processPendingServerChanges": "按当前选择为 Server 变化生成业务预览。",
    "confirmServerWrite": "确认并执行 Server 事实写入，然后只做所需的本地看板刷新。",
    "loadInventory": "加载可处理的库存/Traveler 列表及目录状态。",
    "previewSelectedInventory": "为当前选中对象串行生成库存需求和可用量预览。",
    "runInventory": "启动库存 CLI 子进程，持续消费进度和最终 JSON。",
    "runOrder": "启动订单 CLI 子进程，持续消费进度和最终 JSON。",
    "loadProductionPreview": "读取当前选择的生产材料预览并填充编辑草稿。",
    "prepareProduction": "从 App 提交生产准备参数并处理后端返回。",
    "startDirectProduction": "执行用户确认后的生产完成流程。",
    "startDirectOrderShipment": "执行用户确认后的订单出库流程。",
    "saveOrderAnnotations": "保存安装日期、安装人等订单人工备注并刷新详情。",
    "performBackup": "执行手动/计划备份并把结果映射为 App 状态。",
}

VERB_PURPOSES = [
    ("test", "验证"),
    ("load", "读取"),
    ("read", "读取"),
    ("list", "列出"),
    ("fetch", "获取"),
    ("save", "保存"),
    ("write", "写入"),
    ("set", "设置"),
    ("upsert", "新增或更新"),
    ("record", "记录"),
    ("add", "新增"),
    ("insert", "插入"),
    ("update", "更新"),
    ("delete", "删除"),
    ("remove", "移除"),
    ("clear", "清理"),
    ("restore", "恢复"),
    ("refresh", "刷新"),
    ("sync", "同步"),
    ("scan", "扫描"),
    ("preview", "预览"),
    ("build", "构建"),
    ("generate", "生成"),
    ("parse", "解析"),
    ("normalize", "规范化"),
    ("resolve", "解析并确定"),
    ("check", "检查"),
    ("validate", "校验"),
    ("assert", "强制校验"),
    ("calculate", "计算"),
    ("export", "导出"),
    ("import", "导入"),
    ("open", "打开"),
    ("close", "关闭"),
    ("run", "执行"),
    ("start", "启动"),
    ("finish", "结束并收口"),
    ("prepare", "准备并校验"),
    ("process", "处理"),
    ("consume", "消费并转换"),
    ("apply", "应用"),
    ("make", "创建"),
    ("create", "创建"),
    ("select", "选择"),
    ("match", "匹配"),
    ("find", "查找"),
    ("mark", "标记"),
    ("ignore", "忽略"),
    ("migrate", "迁移"),
    ("reconcile", "对账并重算"),
    ("format", "格式化"),
    ("sort", "排序"),
]

NOUN_TRANSLATIONS = {
    "aimes": "AIMES 数据",
    "server": "Server 数据",
    "inventory": "库存",
    "outbound": "出库",
    "production": "生产",
    "order": "订单",
    "factory": "工厂单",
    "traveler": "Traveler",
    "material": "材料",
    "hardware": "五金",
    "fitting": "五金",
    "database": "数据库",
    "cache": "缓存",
    "mapping": "映射",
    "catalog": "商品目录",
    "settings": "设置",
    "backup": "备份",
    "operation": "操作",
    "log": "日志",
    "dashboard": "看板",
    "issue": "待处理问题",
    "preview": "预览",
    "folder": "文件夹",
    "file": "文件",
    "status": "状态",
    "progress": "进度",
    "cost": "成本",
    "todo": "待办",
    "scope": "范围",
    "source": "来源",
    "row": "行数据",
    "item": "项目",
    "record": "记录",
    "result": "结果",
    "date": "日期",
    "time": "时间",
    "name": "名称",
    "path": "路径",
    "code": "编码",
    "color": "颜色",
    "quantity": "数量",
}


@dataclass
class Symbol:
    path: str
    line: int
    kind: str
    name: str
    qualified_name: str
    signature: str
    parameters: list[str] = field(default_factory=list)
    return_type: str = "未声明"
    raw_calls: list[str] = field(default_factory=list)
    project_calls: list[str] = field(default_factory=list)
    side_effects: list[str] = field(default_factory=list)


def tracked_files() -> list[str]:
    """返回当前 Git 追踪的文件列表。

    参数：无。
    """
    result = subprocess.run(
        ["git", "ls-files"], cwd=ROOT, check=True, capture_output=True, text=True
    )
    return sorted(line for line in result.stdout.splitlines() if line)


def split_words(name: str) -> list[str]:
    """把 snake_case 或 camelCase 标识符拆成便于翻译的词。

    参数：name：待拆分或翻译的代码标识符。
    """
    clean = name.strip("_")
    clean = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", clean)
    return [part.lower() for part in re.split(r"_+", clean) if part]


def translated_subject(name: str) -> str:
    """从标识符提取稳定、保守的中文业务主题。

    参数：name：待拆分或翻译的代码标识符。
    """
    words = split_words(name)
    translated: list[str] = []
    for word in words:
        value = NOUN_TRANSLATIONS.get(word)
        if value and value not in translated:
            translated.append(value)
    return "、".join(translated[:4]) or f"`{name}` 对应的数据或界面状态"


def symbol_purpose(symbol: Symbol) -> str:
    """为符号生成中文简要用途；关键入口使用人工维护的精确说明。

    参数：symbol：待说明或渲染的符号记录。
    """
    if symbol.name in SYMBOL_PURPOSES:
        return SYMBOL_PURPOSES[symbol.name]
    subject = translated_subject(symbol.name)
    fallback_subject = "`" in subject
    if symbol.kind in {"类", "结构体", "枚举", "协议", "扩展"}:
        if fallback_subject:
            return f"定义 `{symbol.name}` {symbol.kind}，集中保存该领域的数据和行为边界。"
        return f"定义与{subject}相关的{symbol.kind}，集中保存数据和行为边界。"
    if symbol.name in {"__init__", "init"}:
        return "初始化所属类型，把传入参数转换为后续方法可使用的状态。"
    if symbol.name in {"__enter__", "__exit__", "deinit"}:
        return "管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。"
    lower = symbol.name.strip("_").lower()
    for prefix, verb in VERB_PURPOSES:
        if lower.startswith(prefix):
            if fallback_subject:
                return f"{verb}与 `{symbol.name}` 对应的数据或步骤。"
            return f"{verb}{subject}相关数据或步骤。"
    if symbol.kind == "计算属性":
        return f"根据当前状态计算并返回{subject}。"
    if fallback_subject:
        return f"封装 `{symbol.name}` 对应的辅助逻辑，供所属模块或类型复用。"
    return f"封装{subject}相关的辅助逻辑，供所属模块或类型复用。"


def file_purpose(path: str) -> str:
    """返回每个项目文件的中文职责说明。

    参数：path：待读取或写入的文件路径。
    """
    if path in FILE_PURPOSES:
        return FILE_PURPOSES[path]
    if path.startswith("tests/test_"):
        return f"自动化测试：验证 `{Path(path).stem.removeprefix('test_')}` 模块或业务场景。"
    if path.startswith("docs/"):
        title = ""
        try:
            for line in (ROOT / path).read_text(encoding="utf-8", errors="replace").splitlines():
                if line.startswith("#"):
                    title = line.lstrip("# ").strip()
                    break
        except OSError:
            pass
        return f"项目文档：{title or Path(path).stem}。"
    if path.startswith("skills/"):
        if path.endswith("SKILL.md"):
            return "项目内业务 Skill 入口：规定 Agent 使用该业务能力时的步骤和边界。"
        if path.endswith("openai.yaml"):
            return "业务 Skill 的 Agent 展示名称、说明和默认提示配置。"
        return "项目内业务 Skill 的专项参考规则。"
    if path.startswith("assets/icon") or path.startswith("assets/icons"):
        return "App 图标或界面视觉候选资源。"
    if path.startswith("resources/panel-images/"):
        return "订单详情 Panel 材料的本地图片资源，文件名编码对应材料型号。"
    if path.startswith("resources/templates/"):
        return "受业务结构约束的 Excel 模板；生成流程在副本上写入。"
    if path.startswith("outputs/"):
        if path.endswith((".py", ".mjs")):
            return "历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。"
        return "历史诊断、工作簿或视觉核对产物，用于保留交付证据。"
    if path.startswith("vendor/openpyxl/"):
        return "第三方 openpyxl 源码文件；由上游库维护，项目只作为固定依赖打包。"
    if path.startswith("vendor/et_xmlfile/"):
        return "第三方 et_xmlfile 源码文件；由上游库维护，项目只作为固定依赖打包。"
    if path.startswith("bin/"):
        return "构建后/本地使用的辅助可执行文件。"
    if path.endswith(".swift"):
        return "Swift/macOS 源码或测试辅助文件。"
    if path.endswith(".py"):
        return "Python 源码或一次性辅助文件。"
    if path.endswith(".mjs"):
        return "Node.js ES Module 辅助脚本。"
    if path.endswith((".png", ".jpg", ".jpeg")):
        return "图片资源或视觉验证产物。"
    if path.endswith(".xlsx"):
        return "Excel 模板、样本或交付产物。"
    return "项目配置、资源或辅助文件。"


def annotation_text(node: ast.expr | None) -> str:
    """把 Python 类型注解转成简洁文本。

    参数：node：待解析或访问的语法树节点。
    """
    if node is None:
        return "未声明"
    try:
        return ast.unparse(node)
    except Exception:
        return "无法解析"


def python_parameter_text(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]:
    """提取 Python 参数、类型和默认值。

    参数：node：待解析或访问的语法树节点。
    """
    args = node.args
    positional = [*args.posonlyargs, *args.args]
    default_offset = len(positional) - len(args.defaults)
    items: list[str] = []
    for index, argument in enumerate(positional):
        if argument.arg in {"self", "cls"}:
            continue
        text = argument.arg
        if argument.annotation is not None:
            text += f": {annotation_text(argument.annotation)}"
        if index >= default_offset:
            text += f" = {ast.unparse(args.defaults[index - default_offset])}"
        items.append(text)
    if args.vararg:
        items.append(f"*{args.vararg.arg}")
    for argument, default in zip(args.kwonlyargs, args.kw_defaults):
        text = argument.arg
        if argument.annotation is not None:
            text += f": {annotation_text(argument.annotation)}"
        if default is not None:
            text += f" = {ast.unparse(default)}"
        items.append(text)
    if args.kwarg:
        items.append(f"**{args.kwarg.arg}")
    return items


class DirectCallVisitor(ast.NodeVisitor):
    """只收集当前函数体的调用，不把嵌套函数的调用误算给外层。"""

    def __init__(self, root: ast.AST) -> None:
        """初始化直接调用收集器并记录需要遍历的根节点。

        参数：self：当前语法树访问器实例；root：限定调用收集范围的语法树根节点。
        """
        self.root = root
        self.calls: list[str] = []

    def visit_FunctionDef(self, node: ast.FunctionDef) -> None:
        """只遍历目标函数，避免混入嵌套函数的调用。

        参数：self：当前语法树访问器实例；node：待解析或访问的语法树节点。
        """
        if node is self.root:
            self.generic_visit(node)

    visit_AsyncFunctionDef = visit_FunctionDef

    def visit_Lambda(self, node: ast.Lambda) -> None:
        """跳过匿名函数，避免混入其内部调用。

        参数：self：当前语法树访问器实例；node：待解析或访问的语法树节点。
        """
        return

    def visit_ClassDef(self, node: ast.ClassDef) -> None:
        """仅在类为目标根节点时继续收集调用。

        参数：self：当前语法树访问器实例；node：待解析或访问的语法树节点。
        """
        if node is self.root:
            self.generic_visit(node)

    def visit_Call(self, node: ast.Call) -> None:
        """记录当前调用名称并继续遍历其子表达式。

        参数：self：当前语法树访问器实例；node：待解析或访问的语法树节点。
        """
        try:
            name = ast.unparse(node.func)
        except Exception:
            name = "<动态调用>"
        if name not in self.calls:
            self.calls.append(name)
        self.generic_visit(node)


def python_symbols(path: Path) -> list[Symbol]:
    """用 AST 提取一个 Python 文件里的类、函数和方法。

    参数：path：待读取或写入的文件路径。
    """
    relative = path.relative_to(ROOT).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    tree = ast.parse(source, filename=relative)
    symbols: list[Symbol] = []

    def walk(body: Iterable[ast.stmt], parents: list[str]) -> None:
        """递归遍历语句与控制块，登记带完整父级名称的类和函数。

        参数：body：需要递归扫描的语句列表；parents：外层类和函数的名称路径。
        """
        for node in body:
            if isinstance(node, ast.ClassDef):
                qualified = ".".join([*parents, node.name])
                symbols.append(
                    Symbol(relative, node.lineno, "类", node.name, qualified, node.name)
                )
                walk(node.body, [*parents, node.name])
            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                qualified = ".".join([*parents, node.name])
                parameters = python_parameter_text(node)
                async_prefix = "async " if isinstance(node, ast.AsyncFunctionDef) else ""
                signature = f"{async_prefix}{qualified}({', '.join(parameters)})"
                result = annotation_text(node.returns)
                if node.returns is not None:
                    signature += f" -> {result}"
                visitor = DirectCallVisitor(node)
                visitor.visit(node)
                symbols.append(
                    Symbol(
                        relative,
                        node.lineno,
                        "方法" if parents else "函数",
                        node.name,
                        qualified,
                        signature,
                        parameters,
                        result,
                        visitor.calls,
                    )
                )
                walk(node.body, [*parents, node.name])
            else:
                # 函数也可能定义在 if/try/with/match 等控制块中；这些仍是项目符号，
                # 不能因为不在当前 body 的第一层就漏掉。
                for _field_name, value in ast.iter_fields(node):
                    if isinstance(value, list) and value and all(isinstance(item, ast.stmt) for item in value):
                        walk(value, parents)

    walk(tree.body, [])
    return symbols


SWIFT_DECL_RE = re.compile(
    r"^[ \t]*(?:(?:private|fileprivate|internal|public|open|static|class|mutating|nonmutating|override|convenience|required|final)[ \t]+)*"
    r"(?P<kind>func|init|deinit|subscript)\b(?:\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*))?",
    re.MULTILINE,
)
SWIFT_TYPE_RE = re.compile(
    r"^[ \t]*(?:(?:private|fileprivate|internal|public|open|final|indirect)[ \t]+)*"
    r"(?P<kind>struct|class|enum|protocol|actor|extension)\s+(?P<name>[A-Za-z_][A-Za-z0-9_.<>]*)",
    re.MULTILINE,
)
SWIFT_PROPERTY_RE = re.compile(
    r"^[ \t]*(?:(?:@[A-Za-z_][^\n]*\n[ \t]*)|(?:(?:private|fileprivate|internal|public|open|static|class|lazy|override)[ \t]+))*"
    r"var\s+(?P<name>[A-Za-z_][A-Za-z0-9_]*)[^=\n]*\{",
    re.MULTILINE,
)


def line_number(source: str, offset: int) -> int:
    """把字符偏移转换为一基行号。

    参数：source：待分析的完整源码；offset：声明在源码中的字符偏移。
    """
    return source.count("\n", 0, offset) + 1


def declaration_end(source: str, start: int) -> int:
    """找到 Swift 声明主体的第一个左花括号。

    参数：source：待分析的完整源码；start：声明起始字符偏移。
    """
    parens = 0
    brackets = 0
    in_string = False
    escaped = False
    for index in range(start, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
        elif char == "(":
            parens += 1
        elif char == ")":
            parens = max(0, parens - 1)
        elif char == "[":
            brackets += 1
        elif char == "]":
            brackets = max(0, brackets - 1)
        elif char == "{" and parens == 0 and brackets == 0:
            return index
        elif char == "\n" and parens == 0 and brackets == 0:
            snippet = source[start:index]
            if "{" not in snippet and not snippet.rstrip().endswith((",", "where")):
                # 多行 Swift 签名通常仍有未闭合括号；普通无主体声明在此结束。
                return index
    return min(len(source), start + 500)


def matching_brace(source: str, opening: int) -> int:
    """近似匹配 Swift/JS 的主体花括号，忽略字符串和行注释。

    参数：source：待分析的完整源码；opening：主体左花括号的位置。
    """
    if opening >= len(source) or source[opening] != "{":
        return opening
    depth = 0
    in_string = False
    escaped = False
    line_comment = False
    block_comment = 0
    index = opening
    while index < len(source):
        char = source[index]
        nxt = source[index + 1] if index + 1 < len(source) else ""
        if line_comment:
            if char == "\n":
                line_comment = False
            index += 1
            continue
        if block_comment:
            if char == "/" and nxt == "*":
                block_comment += 1
                index += 2
                continue
            if char == "*" and nxt == "/":
                block_comment -= 1
                index += 2
                continue
            index += 1
            continue
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            index += 1
            continue
        if char == "/" and nxt == "/":
            line_comment = True
            index += 2
            continue
        if char == "/" and nxt == "*":
            block_comment = 1
            index += 2
            continue
        if char == '"':
            in_string = True
        elif char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return index
        index += 1
    return len(source) - 1


def swift_parameter_list(signature: str) -> list[str]:
    """提取 Swift 声明的参数文本；保留外部参数名和默认值。

    参数：signature：完整声明签名文本。
    """
    opening = signature.find("(")
    if opening < 0:
        return []
    depth = 0
    parts: list[str] = []
    start = opening + 1
    for index, char in enumerate(signature[opening + 1 :], start=opening + 1):
        if char in "([<":
            depth += 1
        elif char in ")]>":
            if char == ")" and depth == 0:
                piece = signature[start:index].strip()
                if piece:
                    parts.append(piece)
                break
            depth = max(0, depth - 1)
        elif char == "," and depth == 0:
            parts.append(signature[start:index].strip())
            start = index + 1
    return [re.sub(r"\s+", " ", part) for part in parts if part]


def swift_return_type(signature: str, raw_kind: str) -> str:
    """读取参数列表之后的返回类型，避免把闭包参数的箭头误认为函数返回值。

    参数：signature：完整声明签名文本；raw_kind：Swift 原始声明类别。
    """
    opening = signature.find("(")
    if opening < 0:
        return "所属类型" if raw_kind == "init" else "未声明"
    depth = 0
    closing = -1
    for index in range(opening, len(signature)):
        char = signature[index]
        if char == "(":
            depth += 1
        elif char == ")":
            depth -= 1
            if depth == 0:
                closing = index
                break
    if raw_kind == "init":
        return "所属类型"
    if closing < 0:
        return "未声明"
    remainder = signature[closing + 1 :]
    result_match = re.search(r"->\s*(.+?)(?:\s+where\s+.*)?$", remainder)
    return result_match.group(1).strip() if result_match else "未声明"


def swift_symbols(path: Path) -> list[Symbol]:
    """静态提取 Swift 类型、函数、初始化器和重要计算属性。

    参数：path：待读取或写入的文件路径。
    """
    relative = path.relative_to(ROOT).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    symbols: list[Symbol] = []
    occupied: set[tuple[int, str]] = set()
    type_ranges: list[tuple[int, int, str]] = []
    for match in SWIFT_TYPE_RE.finditer(source):
        kind = {
            "struct": "结构体",
            "class": "类",
            "enum": "枚举",
            "protocol": "协议",
            "actor": "类",
            "extension": "扩展",
        }[match.group("kind")]
        name = match.group("name")
        symbols.append(Symbol(relative, line_number(source, match.start()), kind, name, name, name))
        opening = source.find("{", match.end(), min(len(source), match.end() + 500))
        if opening >= 0:
            type_ranges.append((opening, matching_brace(source, opening), name))

    def container_name(offset: int) -> str | None:
        """根据声明位置查找包围它的最内层 Swift 类型。

        参数：offset：声明在源码中的字符偏移。
        """
        containing = [item for item in type_ranges if item[0] < offset < item[1]]
        if not containing:
            return None
        return min(containing, key=lambda item: item[1] - item[0])[2]

    for match in SWIFT_DECL_RE.finditer(source):
        raw_kind = match.group("kind")
        name = match.group("name") or raw_kind
        opening = declaration_end(source, match.start())
        signature = re.sub(r"\s+", " ", source[match.start():opening].strip())
        end = matching_brace(source, opening)
        body = source[opening + 1 : end] if opening < len(source) and source[opening] == "{" else ""
        calls = []
        for call in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", body):
            if call not in {"if", "for", "while", "switch", "return", name} and call not in calls:
                calls.append(call)
        result = swift_return_type(signature, raw_kind)
        container = container_name(match.start())
        kind = ("方法" if container else "函数") if raw_kind == "func" else {"init": "初始化器", "deinit": "析构器", "subscript": "下标方法"}[raw_kind]
        qualified = f"{container}.{name}" if container else name
        line = line_number(source, match.start())
        occupied.add((line, name))
        symbols.append(
            Symbol(relative, line, kind, name, qualified, signature, swift_parameter_list(signature), result, calls)
        )
    for match in SWIFT_PROPERTY_RE.finditer(source):
        name = match.group("name")
        line = line_number(source, match.start())
        if (line, name) in occupied:
            continue
        opening = source.find("{", match.start(), match.end() + 1)
        if opening < 0:
            continue
        end = matching_brace(source, opening)
        body = source[opening + 1 : end]
        calls = []
        for call in re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\(", body):
            if call not in {"if", "for", "while", "switch", "return", name} and call not in calls:
                calls.append(call)
        signature = re.sub(r"\s+", " ", source[match.start():opening].strip())
        type_match = re.search(r":\s*([^\{]+)$", signature)
        result = type_match.group(1).strip() if type_match else "由表达式推断"
        container = container_name(match.start())
        qualified = f"{container}.{name}" if container else name
        symbols.append(Symbol(relative, line, "计算属性", name, qualified, signature, [], result, calls))
    return sorted(symbols, key=lambda item: (item.line, item.kind, item.name))


JS_FUNCTION_RE = re.compile(
    r"^(?:export\s+)?(?:(?:async\s+)?function\s+(?P<function>[A-Za-z_$][\w$]*)\s*\((?P<fargs>[^)]*)\)|"
    r"(?:const|let)\s+(?P<arrow>[A-Za-z_$][\w$]*)\s*=\s*(?:async\s*)?\((?P<aargs>[^)]*)\)\s*=>)",
    re.MULTILINE,
)
SHELL_FUNCTION_RE = re.compile(r"^\s*(?:function\s+)?(?P<name>[A-Za-z_][A-Za-z0-9_]*)\s*(?:\(\s*\))?\s*\{", re.MULTILINE)


def js_symbols(path: Path) -> list[Symbol]:
    """提取一方 Node.js 脚本里的命名函数。

    参数：path：待读取或写入的文件路径。
    """
    relative = path.relative_to(ROOT).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    symbols: list[Symbol] = []
    for match in JS_FUNCTION_RE.finditer(source):
        name = match.group("function") or match.group("arrow")
        args = match.group("fargs") if match.group("function") else match.group("aargs")
        opening = source.find("{", match.start(), min(len(source), match.end() + 10))
        end = matching_brace(source, opening) if opening >= 0 else match.end()
        body = source[opening + 1 : end] if opening >= 0 else ""
        calls = []
        for call in re.findall(r"\b([A-Za-z_$][\w$]*)\s*\(", body):
            if call != name and call not in calls:
                calls.append(call)
        parameters = [part.strip() for part in args.split(",") if part.strip()]
        symbols.append(
            Symbol(relative, line_number(source, match.start()), "函数", name, name, f"{name}({args.strip()})", parameters, "Promise/JavaScript 值", calls)
        )
    return symbols


def shell_symbols(path: Path) -> list[Symbol]:
    """提取 shell 函数，并登记脚本顶层过程。

    参数：path：待读取或写入的文件路径。
    """
    relative = path.relative_to(ROOT).as_posix()
    source = path.read_text(encoding="utf-8", errors="replace")
    symbols = [
        Symbol(relative, 1, "脚本过程", "<顶层入口>", "<顶层入口>", f'{relative} "$@"', ["$@：命令行参数"], "进程退出码")
    ]
    for match in SHELL_FUNCTION_RE.finditer(source):
        name = match.group("name")
        end = matching_brace(source, source.find("{", match.start(), match.end()))
        body = source[match.end() : end]
        calls = []
        for line in body.splitlines():
            token_match = re.match(r"\s*([A-Za-z_./][A-Za-z0-9_./-]*)", line)
            if token_match:
                call = token_match.group(1)
                if call not in calls:
                    calls.append(call)
        symbols.append(Symbol(relative, line_number(source, match.start()), "Shell 函数", name, name, f"{name}(位置参数)", ["$1…：位置参数"], "进程状态", calls))
    return symbols


def project_source_paths(files: list[str]) -> list[Path]:
    """选择需要做符号级索引的一方代码，明确排除第三方依赖。

    参数：files：Git 追踪文件的相对路径列表。
    """
    result: list[Path] = []
    for item in files:
        if item.startswith("vendor/"):
            continue
        if item.endswith((".py", ".swift", ".mjs")) or item.startswith("scripts/"):
            result.append(ROOT / item)
    return result


def collect_symbols(files: list[str]) -> list[Symbol]:
    """按语言调用对应静态分析器。

    参数：files：Git 追踪文件的相对路径列表。
    """
    symbols: list[Symbol] = []
    for path in project_source_paths(files):
        relative = path.relative_to(ROOT).as_posix()
        try:
            if path.suffix == ".py":
                symbols.extend(python_symbols(path))
            elif path.suffix == ".swift":
                symbols.extend(swift_symbols(path))
            elif path.suffix == ".mjs":
                symbols.extend(js_symbols(path))
            elif relative.startswith("scripts/"):
                symbols.extend(shell_symbols(path))
        except (OSError, SyntaxError) as exc:
            symbols.append(Symbol(relative, 1, "解析警告", "<无法静态解析>", "<无法静态解析>", str(exc)))
    return symbols


def resolve_calls(symbols: list[Symbol]) -> None:
    """把直接调用名称尽可能映射到项目文件；歧义项保留为待运行时确认。

    参数：symbols：已提取的项目符号列表。
    """
    by_name: dict[str, list[Symbol]] = {}
    for symbol in symbols:
        by_name.setdefault(symbol.name, []).append(symbol)
    for symbol in symbols:
        resolved: list[str] = []
        side_effects: list[str] = []
        if symbol.path.startswith("traveler_assistant/"):
            family = "python-production"
        elif symbol.path.startswith("macos/"):
            family = "swift-production"
        else:
            family = "support"
        for raw in symbol.raw_calls:
            simple = raw.rsplit(".", 1)[-1]
            if simple in COMMON_CALL_NAMES:
                candidates = []
            else:
                candidates = by_name.get(simple, [])
            if family == "python-production":
                candidates = [item for item in candidates if item.path.startswith("traveler_assistant/")]
            elif family == "swift-production":
                candidates = [item for item in candidates if item.path.startswith("macos/")]
            else:
                candidates = [
                    item
                    for item in candidates
                    if not item.path.startswith(("traveler_assistant/", "macos/"))
                ]
            same_file = [candidate for candidate in candidates if candidate.path == symbol.path]
            target: str | None = None
            if len(same_file) == 1:
                target = f"`{same_file[0].path}:{same_file[0].line}` `{same_file[0].qualified_name}`"
            elif len(candidates) == 1 and ("." not in raw or raw.startswith("self.")):
                target = f"`{candidates[0].path}:{candidates[0].line}` `{candidates[0].qualified_name}`"
            if target and target not in resolved:
                resolved.append(target)
            call_words = split_words(simple)
            if simple in SIDE_EFFECT_WORDS or any(word in SIDE_EFFECT_WORDS for word in call_words):
                if raw not in side_effects:
                    side_effects.append(raw)
        symbol.project_calls = resolved
        symbol.side_effects = side_effects


def markdown_escape(value: str) -> str:
    """避免签名破坏 Markdown 行内代码。

    参数：value：需要放入 Markdown 行内代码的签名文本。
    """
    return value.replace("`", "'").replace("\n", " ")


def render_symbol(symbol: Symbol) -> list[str]:
    """把一个符号渲染为稳定、可搜索的中文条目。

    参数：symbol：待说明或渲染的符号记录。
    """
    inputs = "；".join(f"`{markdown_escape(item)}`" for item in symbol.parameters) or "无显式参数（可能读取所属对象状态）"
    calls = "；".join(symbol.project_calls[:12]) or "未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发"
    if len(symbol.project_calls) > 12:
        calls += f"；另有 {len(symbol.project_calls) - 12} 个直接调用"
    lines = [
        f"- **L{symbol.line} · {symbol.kind}** `{markdown_escape(symbol.signature)}` — {symbol_purpose(symbol)}",
        f"  - 输入：{inputs}",
        f"  - 返回：`{markdown_escape(symbol.return_type)}`",
        f"  - 静态可确认的项目内下一跳：{calls}",
    ]
    if symbol.side_effects:
        lines.append("  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `" + "`, `".join(symbol.side_effects[:10]) + "`；是否真实写入仍取决于分支和参数。")
    return lines


def write_text(path: Path, lines: list[str]) -> None:
    """以 UTF-8 和统一末尾换行写入生成文档。

    参数：path：待读取或写入的文件路径；lines：按行组织的文档内容。
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def render_file_map(files: list[str], symbols: list[Symbol], git_tracked_count: int) -> None:
    """生成覆盖全部 Git 追踪文件及本地运行时文件的中文地图。

    参数：files：Git 追踪文件的相对路径列表；symbols：已提取的项目符号列表；git_tracked_count：Git 追踪文件总数。
    """
    counts: dict[str, int] = {}
    for symbol in symbols:
        counts[symbol.path] = counts.get(symbol.path, 0) + 1
    lines = [
        "# PP FlowHub 全文件中文地图",
        "",
        "> 本文件由 `tools/generate_code_reference.py` 从当前工作区生成。请不要手工修改；代码或文件结构变化后重新运行生成器。",
        "",
        "## 1. 覆盖范围",
        "",
        f"- 当前 Git 共追踪 **{git_tracked_count}** 个文件；连同本次新增但可能尚未进入 Git 索引的文档，共登记 **{len(files)}** 个文件。",
        "- `vendor/` 是固定打包的第三方依赖：保留逐文件登记，但不把其内部函数当作 PP FlowHub 业务代码解释。",
        "- `data/`、`.env.local`、构建目录和安装版属于本机运行状态，通常不受 Git 追踪；只登记文件用途，不读取其内容。",
        "- `outputs/` 是历史诊断或交付证据，不属于正式 App 运行链路。",
        "",
        "## 2. Git 追踪文件",
        "",
        "| 文件 | 中文职责 | 一方符号数 |",
        "| --- | --- | ---: |",
    ]
    for item in files:
        lines.append(f"| `{item}` | {file_purpose(item)} | {counts.get(item, 0)} |")
    lines.extend(["", "## 3. 本机运行时文件（不读取内容）", "", "| 文件 | 中文职责 |", "| --- | --- |"])
    runtime_purposes = {
        "aimes-orders.json": "AIMES 近期订单缓存。",
        "assistant-runtime.sqlite3": "助手学习命令与 Token 用量数据库。",
        "factory-names.json": "工厂单号到名称的本地缓存。",
        "inventory-outbound-records.json": "旧版/兼容出库记录。",
        "operation-log.jsonl": "脱敏后的操作审计和分阶段耗时日志。",
        "order-index.sqlite3": "旧版订单索引数据库；当前事实边界以 workflow.sqlite3 及迁移规则为准。",
        "server-scan-snapshot.json": "Server 扫描元数据快照。",
        "settings.json": "本机路径、账号名和功能设置；密码不应明文保存在这里。",
        "todo-items.json": "App 待办事项。",
        "workflow.sqlite3": "中央业务事实数据库。",
    }
    data_dir = ROOT / "data"
    if data_dir.exists():
        for path in sorted(item for item in data_dir.iterdir() if item.is_file() and not item.name.startswith(".")):
            lines.append(f"| `data/{path.name}` | {runtime_purposes.get(path.name, '本机运行生成的数据或缓存文件。')} |")
    lines.extend([
        "",
        "## 4. 不纳入逐文件表的本机目录",
        "",
        "- `.git/`：Git 内部对象与索引，不是项目业务代码。",
        "- `.venv/`：本机 Python 虚拟环境，可由依赖配置重建。",
        "- `build/`、`runtime/`：构建或打包产物，可由构建脚本重建。",
        "- `.env.local`：本机敏感/环境配置，只登记存在性，不输出内容。",
    ])
    write_text(OUTPUTS["files"], lines)


def reference_header(title: str, scope: str, count: int) -> list[str]:
    """生成符号索引的统一说明。

    参数：title：参考文档标题；scope：参考文档覆盖范围说明；count：本页登记的符号数量。
    """
    return [
        f"# {title}",
        "",
        "> 本文件由 `tools/generate_code_reference.py` 生成。请不要手工修改。",
        "",
        "## 如何阅读",
        "",
        f"- 范围：{scope}，共登记 **{count}** 个类型、函数、方法、计算属性或脚本过程。",
        "- “输入”来自静态签名；`self`/`cls` 不重复列出。未声明类型不代表运行时没有约束。",
        "- “项目内下一跳”只表示源码中可静态确认的直接调用，不表示每个分支都会执行。",
        "- `self.method()`、协议分发、闭包、Swift 重载和动态导入可能无法唯一解析；关键业务路径以 `09-user-operation-call-chains.md` 为准。",
        "- “副作用提示”是保守提醒，不等于函数一定执行写入。确认真实行为时应继续阅读分支、日志和测试。",
        "",
    ]


def render_reference(path: Path, title: str, scope: str, symbols: list[Symbol]) -> None:
    """按文件分组生成符号参考。

    参数：path：待读取或写入的文件路径；title：参考文档标题；scope：参考文档覆盖范围说明；symbols：已提取的项目符号列表。
    """
    lines = reference_header(title, scope, len(symbols))
    grouped: dict[str, list[Symbol]] = {}
    for symbol in symbols:
        grouped.setdefault(symbol.path, []).append(symbol)
    for file_path in sorted(grouped):
        lines.extend([f"## `{file_path}`", "", file_purpose(file_path), ""])
        for symbol in sorted(grouped[file_path], key=lambda item: (item.line, item.kind, item.qualified_name)):
            lines.extend(render_symbol(symbol))
            lines.append("")
    write_text(path, lines)


def main() -> int:
    """生成四份代码参考文档并打印覆盖统计。

    参数：无；使用脚本配置和命令行选项。
    """
    files = tracked_files()
    git_tracked_count = len(files)
    # 生成器本身在第一次运行前可能尚未进入 Git 索引，仍应纳入当前文档。
    current_documentation_files = [
        "tools/generate_code_reference.py",
        *(path.relative_to(ROOT).as_posix() for path in OUTPUTS.values()),
        "docs/learning/09-user-operation-call-chains.md",
    ]
    for current_path in current_documentation_files:
        if (ROOT / current_path).exists() and current_path not in files:
            files.append(current_path)
    files.sort()
    symbols = collect_symbols(files)
    resolve_calls(symbols)
    render_file_map(files, symbols, git_tracked_count)

    production_python = [item for item in symbols if item.path.startswith("traveler_assistant/")]
    production_swift = [item for item in symbols if item.path.startswith("macos/")]
    support = [item for item in symbols if item not in production_python and item not in production_swift]
    render_reference(
        OUTPUTS["python"],
        "PP FlowHub Python 全符号中文参考",
        "`traveler_assistant/` 一方生产代码",
        production_python,
    )
    render_reference(
        OUTPUTS["swift"],
        "PP FlowHub Swift/macOS 全符号中文参考",
        "`macos/` App 生产代码",
        production_swift,
    )
    render_reference(
        OUTPUTS["support"],
        "PP FlowHub 测试、脚本与工具全符号中文参考",
        "`tests/`、`scripts/`、`tools/` 和 `outputs/` 中的一方辅助代码",
        support,
    )
    print(
        f"generated files={len(files)} python={len(production_python)} "
        f"swift={len(production_swift)} support={len(support)}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
