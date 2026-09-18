# PP FlowHub Python 全符号中文参考

> 本文件由 `tools/generate_code_reference.py` 生成。请不要手工修改。

## 如何阅读

- 范围：`traveler_assistant/` 一方生产代码，共登记 **677** 个类型、函数、方法、计算属性或脚本过程。
- “输入”来自静态签名；`self`/`cls` 不重复列出。未声明类型不代表运行时没有约束。
- “项目内下一跳”只表示源码中可静态确认的直接调用，不表示每个分支都会执行。
- `self.method()`、协议分发、闭包、Swift 重载和动态导入可能无法唯一解析；关键业务路径以 `09-user-operation-call-chains.md` 为准。
- “副作用提示”是保守提醒，不等于函数一定执行写入。确认真实行为时应继续阅读分支、日志和测试。

## `traveler_assistant/agent_runner.py`

Agent 路由适配层：把模糊自然语言转换为结构化动作。

- **L19 · 类** `AgentDecision` — 定义 `AgentDecision` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L38 · 类** `AgentRouteResult` — 定义与结果相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L58 · 函数** `_load_api_key() -> None` — 读取与 `_load_api_key` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L64 · 函数** `async _run(text: str) -> AgentRouteResult` — 执行与 `_run` 对应的数据或步骤。
  - 输入：`text: str`
  - 返回：`AgentRouteResult`
  - 静态可确认的项目内下一跳：`traveler_assistant/agent_runner.py:58` `_load_api_key`；`traveler_assistant/agent_runner.py:38` `AgentRouteResult`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set_tracing_disabled`, `Runner.run`；是否真实写入仍取决于分支和参数。

- **L88 · 函数** `route_with_agent(text: str) -> AgentRouteResult` — 调用 Agent，把本地解析器无法处理的文本转换为受约束的动作决定。
  - 输入：`text: str`
  - 返回：`AgentRouteResult`
  - 静态可确认的项目内下一跳：`traveler_assistant/agent_runner.py:64` `_run`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `asyncio.run`, `_run`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/assistant_cli.py`

助手 CLI 入口：选择本地解析、学习缓存或 Agent，再进入 Gateway。

- **L24 · 函数** `_factory_name_belongs_to_order(order_id: str, factory_name: str) -> bool` — 封装工厂单、名称、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`order_id: str`；`factory_name: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L42 · 函数** `_learned_local_command(store: RuntimeStore, text: str) -> LocalCommand | None` — 封装 `_learned_local_command` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: RuntimeStore`；`text: str`
  - 返回：`LocalCommand | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/command_router.py:55` `normalize_command_text`；`traveler_assistant/command_router.py:35` `LocalCommand`

- **L50 · 函数** `_agent_command(store: RuntimeStore, text: str) -> tuple[LocalCommand | None, dict]` — 封装 `_agent_command` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: RuntimeStore`；`text: str`
  - 返回：`tuple[LocalCommand | None, dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/agent_runner.py:88` `route_with_agent`；`traveler_assistant/runtime_store.py:22` `TokenUsage`；`traveler_assistant/command_router.py:55` `normalize_command_text`；`traveler_assistant/assistant_cli.py:24` `_factory_name_belongs_to_order`；`traveler_assistant/command_router.py:35` `LocalCommand`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.record_agent_usage`, `arguments.update`；是否真实写入仍取决于分支和参数。

- **L110 · 函数** `main(argv: list[str] | None = None) -> int` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：`argv: list[str] | None = None`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:125` `Config`；`traveler_assistant/operation_log.py:192` `configure_operation_log`；`traveler_assistant/runtime_store.py:31` `RuntimeStore`；`traveler_assistant/runtime_store.py:16` `runtime_database_path`；`traveler_assistant/command_router.py:60` `parse_local_command`；`traveler_assistant/assistant_cli.py:42` `_learned_local_command`；`traveler_assistant/assistant_cli.py:50` `_agent_command`；`traveler_assistant/tool_gateway.py:52` `execute_local_command`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `execute_local_command`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/backup.py`

数据与配置备份、状态检查和保留策略。

- **L16 · 函数** `_fingerprint(path: Path) -> str` — 封装 `_fingerprint` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.open`, `digest.update`；是否真实写入仍取决于分支和参数。

- **L24 · 函数** `backup_status(config: Config, today: date | None = None) -> dict` — 封装备份、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`today: date | None = None`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:438` `ensure_schema`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L45 · 函数** `perform_backup(config: Config) -> dict` — 封装备份相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/backup.py:24` `backup_status`；`traveler_assistant/backup.py:16` `_fingerprint`；`traveler_assistant/backup.py:84` `_apply_retention`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `root.mkdir`, `os.close`, `target.close`, `connection.close`, `os.replace`, `temporary.unlink`, `connection.execute`, `connection.commit`；是否真实写入仍取决于分支和参数。

- **L84 · 函数** `_apply_retention(root: Path, today: date) -> None` — 应用与 `_apply_retention` 对应的数据或步骤。
  - 输入：`root: Path`；`today: date`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `keep.update`, `path.unlink`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/command_router.py`

常用中英文命令的确定性本地解析器。

- **L35 · 类** `LocalCommand` — 定义 `LocalCommand` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L41 · 函数** `normalize_spoken_order_ids(text: str) -> str` — 规范化订单相关数据或步骤。
  - 输入：`text: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L43 · 方法** `normalize_spoken_order_ids.replace(match: re.Match[str]) -> str` — 封装 `replace` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`match: re.Match[str]`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L55 · 函数** `normalize_command_text(text: str) -> str` — 规范化与 `normalize_command_text` 对应的数据或步骤。
  - 输入：`text: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/command_router.py:41` `normalize_spoken_order_ids`

- **L60 · 函数** `parse_local_command(text: str) -> LocalCommand | None` — 把常见自然语言命令解析为无副作用的结构化本地命令；无法确定时返回 None。
  - 输入：`text: str`
  - 返回：`LocalCommand | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/command_router.py:55` `normalize_command_text`；`traveler_assistant/command_router.py:35` `LocalCommand`

## `traveler_assistant/core.py`

共享配置、错误、进度、AIMES 查询和五金解析基础能力。

- **L44 · 类** `RuleError` — 定义 `RuleError` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L45 · 方法** `RuleError.__init__(code: str, message: str, **context)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`code: str`；`message: str`；`**context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:45` `RuleError.__init__`

- **L51 · 函数** `_extract_aimes_failure(stderr: str) -> str` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`stderr: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L80 · 函数** `_aimes_failure_code(error: str) -> str` — 封装AIMES 数据、编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`error: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L96 · 函数** `factory_name_order_prefix(factory_name: str) -> str` — 封装工厂单、名称、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`factory_name: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L102 · 函数** `factory_name_order_mismatch(factory_name: str, sales_order_name: str) -> tuple[str, str] | None` — 封装工厂单、名称、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`factory_name: str`；`sales_order_name: str`
  - 返回：`tuple[str, str] | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:96` `factory_name_order_prefix`

- **L118 · 函数** `progress(message: str, **details) -> None` — 封装进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`message: str`；`**details`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:201` `log_progress_payload`

- **L125 · 类** `Config` — 定义 `Config` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L151 · 方法** `Config.operation_log_file() -> Path` — 封装操作、日志、文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L155 · 方法** `Config.workflow_database() -> Path` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:43` `database_path`

- **L159 · 方法** `Config.database_backup_root() -> Path` — 封装数据库、备份相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L162 · 方法** `Config.prepare_storage() -> None` — 准备并校验与 `prepare_storage` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/hardware_facts.py:35` `assert_source_isolation`；`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:43` `database_path`

- **L176 · 方法** `Config.settings_file() -> Path` — 设置设置、文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L179 · 方法** `Config.load_settings(source_profile: str | None = None) -> None` — 读取设置相关数据或步骤。
  - 输入：`source_profile: str | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L235 · 方法** `Config.factory_names_file() -> Path` — 封装工厂单、文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L239 · 方法** `Config.aimes_orders_file() -> Path` — 封装AIMES 数据、文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L243 · 方法** `Config.material_assignments_file() -> Path` — 封装材料、文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L247 · 方法** `Config.node_path() -> str` — 封装路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L258 · 方法** `Config.playwright_node_modules() -> Path` — 封装 `playwright_node_modules` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L262 · 函数** `load_factory_name_cache(config: Config) -> dict[str, str]` — 读取工厂单、名称、缓存相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:1753` `read_cache`

- **L269 · 函数** `save_factory_name_cache(config: Config, values: dict[str, str]) -> None` — 保存工厂单、名称、缓存相关数据或步骤。
  - 输入：`config: Config`；`values: dict[str, str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:1767` `write_cache`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_cache`；是否真实写入仍取决于分支和参数。

- **L273 · 函数** `load_aimes_order_cache(config: Config) -> list[dict[str, str]]` — 读取AIMES 数据、订单、缓存相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`list[dict[str, str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:1753` `read_cache`

- **L289 · 函数** `save_aimes_order_cache(config: Config, values: list[dict[str, str]]) -> None` — 保存AIMES 数据、订单、缓存相关数据或步骤。
  - 输入：`config: Config`；`values: list[dict[str, str]]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:1767` `write_cache`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_cache`；是否真实写入仍取决于分支和参数。

- **L293 · 函数** `load_material_assignments(config: Config) -> dict[str, str]` — 读取材料相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:1753` `read_cache`

- **L298 · 函数** `save_material_assignment(config: Config, key: str, path: str) -> None` — 保存材料相关数据或步骤。
  - 输入：`config: Config`；`key: str`；`path: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:293` `load_material_assignments`；`traveler_assistant/database.py:1767` `write_cache`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_cache`；是否真实写入仍取决于分支和参数。

- **L304 · 函数** `_run_aimes_lookup(config: Config, factory_orders: list[str], recent_limit: int = 0, include_order_metadata: bool = False, verify_factory_orders: bool = False)` — 执行AIMES 数据相关数据或步骤。
  - 输入：`config: Config`；`factory_orders: list[str]`；`recent_limit: int = 0`；`include_order_metadata: bool = False`；`verify_factory_orders: bool = False`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:118` `progress`；`traveler_assistant/streaming_process.py:9` `run_with_progress`；`traveler_assistant/core.py:51` `_extract_aimes_failure`；`traveler_assistant/core.py:80` `_aimes_failure_code`；`traveler_assistant/operation_log.py:94` `redact`；`traveler_assistant/operation_log.py:221` `log_aimes_failure`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `os.environ.copy`, `run_with_progress`；是否真实写入仍取决于分支和参数。

- **L342 · 方法** `_run_aimes_lookup.consume_progress(stderr: str, attempt_timings: list[dict[str, object]]) -> None` — 消费并转换进度相关数据或步骤。
  - 输入：`stderr: str`；`attempt_timings: list[dict[str, object]]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:94` `redact`；`traveler_assistant/operation_log.py:201` `log_progress_payload`

- **L467 · 函数** `lookup_aimes_names(config: Config, factory_orders: list[str], recent_limit: int = 0) -> dict[str, str]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`factory_orders: list[str]`；`recent_limit: int = 0`
  - 返回：`dict[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:304` `_run_aimes_lookup`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_run_aimes_lookup`；是否真实写入仍取决于分支和参数。

- **L482 · 函数** `lookup_aimes_recent_orders(config: Config, limit: int = AIMES_BULK_FETCH_LIMIT, include_trace: bool = False) -> list[dict[str, str]] | tuple[list[dict[str, str]], list[dict[str, object]]]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`limit: int = AIMES_BULK_FETCH_LIMIT`；`include_trace: bool = False`
  - 返回：`list[dict[str, str]] | tuple[list[dict[str, str]], list[dict[str, object]]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:304` `_run_aimes_lookup`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:508` `_non_aggregate_aimes_timings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_run_aimes_lookup`；是否真实写入仍取决于分支和参数。

- **L508 · 函数** `_non_aggregate_aimes_timings(values: object) -> list[dict[str, object]]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`values: object`
  - 返回：`list[dict[str, object]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L520 · 函数** `verify_aimes_factory_orders(config: Config, factory_orders: list[str]) -> dict[str, list[dict[str, str]] | list[str]]` — 封装AIMES 数据、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`factory_orders: list[str]`
  - 返回：`dict[str, list[dict[str, str]] | list[str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:304` `_run_aimes_lookup`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_run_aimes_lookup`；是否真实写入仍取决于分支和参数。

- **L544 · 函数** `refresh_aimes_recent_orders_and_verify(config: Config, limit: int, factory_orders: list[str], timing_sink: list[dict[str, object]] | None = None) -> tuple[list[dict[str, str]], dict[str, list[dict[str, str]] | list[str]]]` — 刷新AIMES 数据相关数据或步骤。
  - 输入：`config: Config`；`limit: int`；`factory_orders: list[str]`；`timing_sink: list[dict[str, object]] | None = None`
  - 返回：`tuple[list[dict[str, str]], dict[str, list[dict[str, str]] | list[str]]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:304` `_run_aimes_lookup`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:508` `_non_aggregate_aimes_timings`；`traveler_assistant/core.py:565` `refresh_aimes_recent_orders_and_verify.normalize`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_run_aimes_lookup`；是否真实写入仍取决于分支和参数。

- **L565 · 方法** `refresh_aimes_recent_orders_and_verify.normalize(rows: list[object]) -> list[dict[str, str]]` — 规范化与 `normalize` 对应的数据或步骤。
  - 输入：`rows: list[object]`
  - 返回：`list[dict[str, str]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L585 · 函数** `refresh_aimes_recent_orders(config: Config, limit: int = AIMES_BULK_FETCH_LIMIT, persist: bool = True, timing_sink: list[dict[str, object]] | None = None) -> list[dict[str, str]]` — 刷新AIMES 数据相关数据或步骤。
  - 输入：`config: Config`；`limit: int = AIMES_BULK_FETCH_LIMIT`；`persist: bool = True`；`timing_sink: list[dict[str, object]] | None = None`
  - 返回：`list[dict[str, str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:482` `lookup_aimes_recent_orders`；`traveler_assistant/core.py:289` `save_aimes_order_cache`；`traveler_assistant/core.py:262` `load_factory_name_cache`；`traveler_assistant/core.py:269` `save_factory_name_cache`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save_aimes_order_cache`, `cache.update`, `save_factory_name_cache`；是否真实写入仍取决于分支和参数。

- **L615 · 函数** `refresh_aimes_recent_names(config: Config, limit: int = AIMES_BULK_FETCH_LIMIT) -> dict[str, str]` — 刷新AIMES 数据相关数据或步骤。
  - 输入：`config: Config`；`limit: int = AIMES_BULK_FETCH_LIMIT`
  - 返回：`dict[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:585` `refresh_aimes_recent_orders`

- **L626 · 类** `FittingItem` — 定义与五金、项目相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L634 · 函数** `_text(value) -> str` — 封装 `_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L638 · 函数** `_number(value) -> float` — 封装 `_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L647 · 函数** `_normalize_name(value: str) -> str` — 规范化名称相关数据或步骤。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L658 · 函数** `parse_fittings_groups(path: Path, allow_missing_factory: bool = False, fallback_factory: str = '') -> list[tuple[str, list[FittingItem]]]` — 解析与 `parse_fittings_groups` 对应的数据或步骤。
  - 输入：`path: Path`；`allow_missing_factory: bool = False`；`fallback_factory: str = ''`
  - 返回：`list[tuple[str, list[FittingItem]]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:634` `_text`；`traveler_assistant/core.py:626` `FittingItem`；`traveler_assistant/core.py:638` `_number`；`traveler_assistant/core.py:647` `_normalize_name`

## `traveler_assistant/costing.py`

订单成本计算、展示排序和 Excel 导出。

- **L27 · 函数** `_now() -> str` — 封装 `_now` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L31 · 函数** `_number(value) -> float` — 封装 `_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`float`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L38 · 函数** `_material_name(kind: str, thickness: str, color: str) -> str` — 封装材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`kind: str`；`thickness: str`；`color: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L46 · 函数** `_resolve_product(catalog, mappings, name: str, section: str, code: str = '')` — 解析并确定与 `_resolve_product` 对应的数据或步骤。
  - 输入：`catalog`；`mappings`；`name: str`；`section: str`；`code: str = ''`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/inventory.py:2336` `match_item`；`traveler_assistant/core.py:44` `RuleError`

- **L69 · 函数** `_line(category: str, factory_order: str, room_name: str, name: str, spec: str, quantity: float, unit: str, product_code: str, cost_price: float | None, source: str, missing: str = '') -> dict` — 封装 `_line` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`category: str`；`factory_order: str`；`room_name: str`；`name: str`；`spec: str`；`quantity: float`；`unit: str`；`product_code: str`；`cost_price: float | None`；`source: str`；`missing: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L100 · 函数** `_aggregate_material_rows(rows: list[sqlite3.Row]) -> list[dict]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`rows: list[sqlite3.Row]`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/costing.py:31` `_number`

- **L134 · 函数** `_display_cost_lines(lines: list[dict]) -> list[dict]` — 封装成本相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`lines: list[dict]`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L170 · 方法** `_display_cost_lines.sort_key(line: dict) -> tuple` — 排序与 `sort_key` 对应的数据或步骤。
  - 输入：`line: dict`
  - 返回：`tuple`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L194 · 函数** `calculate_order_cost(config: Config, order_id: str) -> dict` — 从中央事实、商品编码和价格计算订单成本明细与汇总。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/costing.py:100` `_aggregate_material_rows`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/costing.py:69` `_line`；`traveler_assistant/costing.py:31` `_number`；`traveler_assistant/costing.py:46` `_resolve_product`；`traveler_assistant/costing.py:134` `_display_cost_lines`；`traveler_assistant/costing.py:27` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L343 · 函数** `_excel_row(row: dict) -> list` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`list`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L360 · 函数** `_style_rows(sheet, header_row: int, last_row: int, widths: dict[str, float]) -> None` — 封装 `_style_rows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`sheet`；`header_row: int`；`last_row: int`；`widths: dict[str, float]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L380 · 函数** `export_order_cost(config: Config, order_id: str) -> dict` — 把订单成本明细写入 Excel 并保持规定的展示顺序。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/costing.py:194` `calculate_order_cost`；`traveler_assistant/costing.py:343` `_excel_row`；`traveler_assistant/costing.py:360` `_style_rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `output_dir.mkdir`, `set`, `workbook.save`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/database.py`

中央 SQLite 路径、Schema、迁移和通用缓存读写。

- **L20 · 函数** `enable_foreign_keys(connection: sqlite3.Connection) -> sqlite3.Connection` — 封装 `enable_foreign_keys` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`
  - 返回：`sqlite3.Connection`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L38 · 函数** `connect_database(path: Path, **kwargs) -> sqlite3.Connection` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`**kwargs`
  - 返回：`sqlite3.Connection`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:20` `enable_foreign_keys`

- **L43 · 函数** `database_path(state_dir: Path) -> Path` — 封装数据库、路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`state_dir: Path`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L48 · 函数** `_now() -> str` — 封装 `_now` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L63 · 函数** `_product_key(value: object) -> str` — 封装 `_product_key` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: object`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L67 · 函数** `catalog_material_attributes(category: object, name: object, spec: object, code: object = '') -> tuple[str, str, str]` — 封装商品目录、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`category: object`；`name: object`；`spec: object`；`code: object = ''`
  - 返回：`tuple[str, str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:63` `_product_key`

- **L116 · 函数** `_legacy_material_name(material_type: object, color: object, thickness: object) -> str` — 封装材料、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`material_type: object`；`color: object`；`thickness: object`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L127 · 函数** `server_material_identity_key(source_path: object, product_code: object) -> str` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`source_path: object`；`product_code: object`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L136 · 函数** `_has_product_foreign_key(connection: sqlite3.Connection, table: str) -> bool` — 封装 `_has_product_foreign_key` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`table: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L144 · 函数** `_resolve_legacy_material_code(connection: sqlite3.Connection, material_type: object, color: object, thickness: object) -> tuple[str, list[str]]` — 解析并确定材料、编码相关数据或步骤。
  - 输入：`connection: sqlite3.Connection`；`material_type: object`；`color: object`；`thickness: object`
  - 返回：`tuple[str, list[str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:116` `_legacy_material_name`；`traveler_assistant/inventory.py:2336` `match_item`；`traveler_assistant/database.py:163` `_resolve_legacy_material_code._MigrationCatalog`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:90` `TravelerItem`

- **L163 · 类** `_MigrationCatalog` — 定义与商品目录相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L165 · 方法** `_resolve_legacy_material_code._MigrationCatalog._product(row: tuple) -> Product` — 封装 `_product` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: tuple`
  - 返回：`Product`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:152` `Product`

- **L174 · 方法** `_resolve_legacy_material_code._MigrationCatalog.require_code(code: str) -> Product` — 封装编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`code: str`
  - 返回：`Product`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:63` `_product_key`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/database.py:165` `_resolve_legacy_material_code._MigrationCatalog._product`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L187 · 方法** `_resolve_legacy_material_code._MigrationCatalog.find(category = None, name = None, contains = None, spec_thickness = None)` — 查找与 `find` 对应的数据或步骤。
  - 输入：`category = None`；`name = None`；`contains = None`；`spec_thickness = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:165` `_resolve_legacy_material_code._MigrationCatalog._product`；`traveler_assistant/database.py:63` `_product_key`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L225 · 函数** `_outbound_factory_tokens(value: object) -> list[str]` — 封装出库、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: object`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L233 · 函数** `_outbound_document_factory_candidates(connection: sqlite3.Connection, document_number: str, order_id: str, factory_value: str) -> set[str]` — 封装出库、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`document_number: str`；`order_id: str`；`factory_value: str`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:225` `_outbound_factory_tokens`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `connection.execute`, `_outbound_factory_tokens`, `candidates.update`, `order_aliases.update`；是否真实写入仍取决于分支和参数。

- **L302 · 函数** `ensure_outbound_document_factory_links(connection: sqlite3.Connection, document_number: str, order_id: str, factory_value: str, updated_at: str | None = None) -> int` — 封装出库、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`document_number: str`；`order_id: str`；`factory_value: str`；`updated_at: str | None = None`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:233` `_outbound_document_factory_candidates`；`traveler_assistant/database.py:48` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_outbound_document_factory_candidates`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L346 · 函数** `_execute_schema_statements(connection: sqlite3.Connection, script: str) -> None` — 封装 `_execute_schema_statements` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`script: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L369 · 函数** `_simplify_production_schema(connection: sqlite3.Connection) -> None` — 封装生产相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L438 · 函数** `ensure_schema(path: Path) -> None` — 封装 `ensure_schema` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/database.py:233` `_outbound_document_factory_candidates`；`traveler_assistant/database.py:302` `ensure_outbound_document_factory_links`；`traveler_assistant/database.py:48` `_now`；`traveler_assistant/database.py:346` `_execute_schema_statements`；`traveler_assistant/database.py:67` `catalog_material_attributes`；`traveler_assistant/database.py:63` `_product_key`；`traveler_assistant/hardware_facts.py:47` `hardware_fingerprint`；`traveler_assistant/database.py:144` `_resolve_legacy_material_code`；`traveler_assistant/database.py:136` `_has_product_foreign_key`；`traveler_assistant/database.py:127` `server_material_identity_key`；`traveler_assistant/database.py:369` `_simplify_production_schema`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `connection.execute`, `_outbound_document_factory_candidates`, `ensure_outbound_document_factory_links`, `connection.commit`, `backup_directory.mkdir`, `backup.execute`, `backup.close`, `_execute_schema_statements`, `connection.executemany`；是否真实写入仍取决于分支和参数。

- **L1401 · 函数** `collapse_actual_installation_days(connection: sqlite3.Connection) -> int` — 封装 `collapse_actual_installation_days` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L1443 · 函数** `_normalize_inventory_rule_name(value: str) -> str` — 规范化库存、名称相关数据或步骤。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1459 · 函数** `migrate_inventory_mapping_file(state_dir: Path) -> dict[str, Any]` — 迁移库存、映射、文件相关数据或步骤。
  - 输入：`state_dir: Path`
  - 返回：`dict[str, Any]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:43` `database_path`；`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/database.py:48` `_now`；`traveler_assistant/database.py:1443` `_normalize_inventory_rule_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`, `archive.mkdir`, `shutil.move`；是否真实写入仍取决于分支和参数。

- **L1577 · 函数** `_copy_table(source: sqlite3.Connection, target: sqlite3.Connection, table: str) -> bool` — 封装 `_copy_table` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source: sqlite3.Connection`；`target: sqlite3.Connection`；`table: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `source.execute`, `target.execute`, `column.replace`, `target.executemany`；是否真实写入仍取决于分支和参数。

- **L1595 · 函数** `migrate_legacy_databases(state_dir: Path) -> dict[str, Any]` — 迁移与 `migrate_legacy_databases` 对应的数据或步骤。
  - 输入：`state_dir: Path`
  - 返回：`dict[str, Any]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:43` `database_path`；`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/database.py:48` `_now`；`traveler_assistant/database.py:302` `ensure_outbound_document_factory_links`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `source.execute`, `connection.execute`, `column.replace`, `source.close`, `ensure_outbound_document_factory_links`, `connection.commit`, `connection.close`, `archive.mkdir`, `shutil.move`；是否真实写入仍取决于分支和参数。

- **L1739 · 函数** `_cache_rows(path: Path, cache_name: str) -> dict[str, Any]` — 封装缓存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`cache_name: str`
  - 返回：`dict[str, Any]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1753 · 函数** `read_cache(path: Path, cache_name: str, legacy: Path | None = None, default: Any = None) -> Any` — 读取缓存相关数据或步骤。
  - 输入：`path: Path`；`cache_name: str`；`legacy: Path | None = None`；`default: Any = None`
  - 返回：`Any`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:1739` `_cache_rows`；`traveler_assistant/database.py:1767` `write_cache`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_cache`；是否真实写入仍取决于分支和参数。

- **L1767 · 函数** `write_cache(path: Path, cache_name: str, value: Any) -> None` — 写入缓存相关数据或步骤。
  - 输入：`path: Path`；`cache_name: str`；`value: Any`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/database.py:48` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/fittings.py`

五金记录签名与最新来源选择规则。

- **L24 · 函数** `is_fittings_report(path: Path) -> bool` — 封装 `is_fittings_report` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L33 · 函数** `fitting_signature(items: Iterable[FittingItem]) -> tuple` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: Iterable[FittingItem]`
  - 返回：`tuple`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L47 · 类** `SelectedFittings` — 定义 `SelectedFittings` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L54 · 函数** `select_latest_fittings(paths: Iterable[Path], allow_missing_factory: bool = False, fallback_factory: str = '', is_empty_report: Callable[[Path], bool] | None = None) -> tuple[dict[str, SelectedFittings], list[str], bool, list[Path]]` — 选择与 `select_latest_fittings` 对应的数据或步骤。
  - 输入：`paths: Iterable[Path]`；`allow_missing_factory: bool = False`；`fallback_factory: str = ''`；`is_empty_report: Callable[[Path], bool] | None = None`
  - 返回：`tuple[dict[str, SelectedFittings], list[str], bool, list[Path]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:658` `parse_fittings_groups`；`traveler_assistant/fittings.py:47` `SelectedFittings`；`traveler_assistant/fittings.py:33` `fitting_signature`；`traveler_assistant/report_read_context.py:36` `current_report_context`；`traveler_assistant/fittings.py:161` `fittings_candidate`；`traveler_assistant/fittings.py:174` `selected_from_candidate`；`traveler_assistant/core.py:44` `RuleError`

- **L161 · 函数** `fittings_candidate(source: SelectedFittings) -> dict` — 封装 `fittings_candidate` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source: SelectedFittings`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L174 · 函数** `selected_from_candidate(candidate)` — 选择与 `selected_from_candidate` 对应的数据或步骤。
  - 输入：`candidate`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:626` `FittingItem`；`traveler_assistant/fittings.py:47` `SelectedFittings`；`traveler_assistant/fittings.py:33` `fitting_signature`

## `traveler_assistant/hardware_facts.py`

Python 源码或一次性辅助文件。

- **L14 · 函数** `server_hardware_quantity(product_code, quantity, unit, factory_order = '', name = '')` — 封装Server 数据、五金、数量相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`product_code`；`quantity`；`unit`；`factory_order = ''`；`name = ''`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L35 · 函数** `assert_source_isolation(database, sources, test_mode = False)` — 强制校验来源相关数据或步骤。
  - 输入：`database`；`sources`；`test_mode = False`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L47 · 函数** `hardware_fingerprint(rows)` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`rows`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L56 · 函数** `replace_factory_hardware(connection, factory_order, rows, source_path = '', observed_at = '', reason = 'Server 五金同步', allow_empty = False)` — 封装工厂单、五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`；`factory_order`；`rows`；`source_path = ''`；`observed_at = ''`；`reason = 'Server 五金同步'`；`allow_empty = False`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/hardware_facts.py:35` `assert_source_isolation`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/hardware_facts.py:47` `hardware_fingerprint`；`traveler_assistant/hardware_facts.py:124` `audit_factory_hardware`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.executemany`；是否真实写入仍取决于分支和参数。

- **L124 · 函数** `audit_factory_hardware(connection, factory_order, now = None)` — 封装工厂单、五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`；`factory_order`；`now = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L157 · 函数** `hardware_integrity_findings(connection)` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L182 · 函数** `audit_hardware_integrity(connection)` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/hardware_facts.py:157` `hardware_integrity_findings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L198 · 函数** `preserve_confirmed_shipment(connection, factory_order)` — 封装 `preserve_confirmed_shipment` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`；`factory_order`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/hardware_source_decisions.py`

Python 源码或一次性辅助文件。

- **L7 · 函数** `decision_revision(value)` — 封装 `decision_revision` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L11 · 函数** `load_source_decisions(config)` — 读取来源相关数据或步骤。
  - 输入：`config`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L28 · 函数** `commit_source_decisions(connection, payload, factories, skipped_orders)` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection`；`payload`；`factories`；`skipped_orders`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/hardware_source_decisions.py:7` `decision_revision`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L51 · 函数** `with_source_decisions(function)` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`function`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L55 · 方法** `with_source_decisions.run(config, *args, **kwargs)` — 执行与 `run` 对应的数据或步骤。
  - 输入：`config`；`*args`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/report_read_context.py:36` `current_report_context`；`traveler_assistant/report_read_context.py:41` `report_read_session`；`traveler_assistant/hardware_source_decisions.py:11` `load_source_decisions`

## `traveler_assistant/inventory.py`

库存需求、商品映射、预检、浏览器出库和出库留痕。

- **L90 · 类** `TravelerItem` — 定义与Traveler、项目相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L98 · 方法** `TravelerItem.source_snapshot() -> dict` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`dict`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L115 · 函数** `_with_product_code(item: TravelerItem, product_code: str) -> TravelerItem` — 封装编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`item: TravelerItem`；`product_code: str`
  - 返回：`TravelerItem`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L128 · 类** `TravelerData` — 定义与Traveler相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L139 · 方法** `TravelerData.content_snapshot() -> dict` — 封装 `content_snapshot` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:98` `TravelerItem.source_snapshot`

- **L152 · 类** `Product` — 定义 `Product` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L169 · 类** `OutboundItem` — 定义与出库、项目相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L181 · 类** `InventoryPreview` — 定义与库存、预览相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L209 · 方法** `InventoryPreview.ready() -> bool` — 读取与 `ready` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L212 · 方法** `InventoryPreview.payload() -> dict` — 封装 `payload` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:257` `InventoryPreview.document_payloads`；`traveler_assistant/inventory.py:243` `InventoryPreview._selected_document_set`；`traveler_assistant/inventory.py:98` `TravelerItem.source_snapshot`；`traveler_assistant/core.py:647` `_normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self._selected_document_set`；是否真实写入仍取决于分支和参数。

- **L243 · 方法** `InventoryPreview._selected_document_set() -> set[str]` — 选择与 `_selected_document_set` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`

- **L253 · 方法** `InventoryPreview._document_is_selected(remark: str) -> bool` — 封装 `_document_is_selected` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`remark: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:243` `InventoryPreview._selected_document_set`；`traveler_assistant/core.py:647` `_normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self._selected_document_set`；是否真实写入仍取决于分支和参数。

- **L257 · 方法** `InventoryPreview.document_payloads() -> list[dict]` — 封装 `document_payloads` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:253` `InventoryPreview._document_is_selected`

- **L280 · 函数** `stock_requirements(preview: InventoryPreview, include_hardware: bool = False) -> list[dict]` — 封装 `stock_requirements` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`preview: InventoryPreview`；`include_hardware: bool = False`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:300` `_group_stock_requirements`

- **L300 · 函数** `_group_stock_requirements(items: Iterable[OutboundItem]) -> list[dict]` — 封装 `_group_stock_requirements` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: Iterable[OutboundItem]`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L316 · 函数** `database_stock_requirements(config: Config, order_id: str) -> tuple[str, list[dict]]` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`tuple[str, list[dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:634` `database_document_items`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:2336` `match_item`；`traveler_assistant/inventory.py:300` `_group_stock_requirements`

- **L344 · 函数** `order_stock_requirements(config: Config, order_folder: Path) -> tuple[str, list[dict]]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_folder: Path`
  - 返回：`tuple[str, list[dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:316` `database_stock_requirements`；`traveler_assistant/order_workflow.py:1682` `preview_order`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:2336` `match_item`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:300` `_group_stock_requirements`

- **L399 · 函数** `_database_factory_rows(config: Config, order_id: str) -> tuple[dict, dict[str, dict]]` — 封装数据库、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`tuple[dict, dict[str, dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_details.py:12` `order_detail`

- **L414 · 函数** `_usable_hardware_factory_orders(detail: dict) -> set[str]` — 封装五金、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`detail: dict`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L430 · 函数** `database_outbound_fingerprint(config: Config, order_id: str, factory_order: str) -> str` — 封装数据库、出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`；`factory_order: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:775` `outbound_scope_decisions`；`traveler_assistant/inventory.py:1297` `_fingerprint`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outbound_scope_decisions`；是否真实写入仍取决于分支和参数。

- **L455 · 函数** `mark_customer_supplied_outbound(config: Config, order_id: str, selected_factory_orders: Iterable[str] | None = None) -> dict` — 标记出库相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`selected_factory_orders: Iterable[str] | None = None`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/inventory.py:775` `outbound_scope_decisions`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:414` `_usable_hardware_factory_orders`；`traveler_assistant/inventory.py:430` `database_outbound_fingerprint`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outbound_scope_decisions`, `set`, `database_outbound_fingerprint`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L543 · 函数** `mark_no_hardware_outbound(config: Config, order_id: str, selected_factory_orders: Iterable[str] | None = None) -> dict` — 标记五金、出库相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`selected_factory_orders: Iterable[str] | None = None`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:414` `_usable_hardware_factory_orders`；`traveler_assistant/inventory.py:430` `database_outbound_fingerprint`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `database_outbound_fingerprint`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L634 · 函数** `database_document_items(config: Config, order_id: str, selected_factory_orders: Iterable[str] | None = None, production_request_id: str = '', production_materials: Iterable[dict] | None = None, shipment_only: bool = False) -> tuple[str, dict[str, list[TravelerItem]], list[TravelerItem], dict[str, dict]]` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`；`selected_factory_orders: Iterable[str] | None = None`；`production_request_id: str = ''`；`production_materials: Iterable[dict] | None = None`；`shipment_only: bool = False`
  - 返回：`tuple[str, dict[str, list[TravelerItem]], list[TravelerItem], dict[str, dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:102` `factory_name_order_mismatch`；`traveler_assistant/inventory.py:775` `outbound_scope_decisions`；`traveler_assistant/inventory.py:115` `_with_product_code`；`traveler_assistant/inventory.py:90` `TravelerItem`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `outbound_scope_decisions`；是否真实写入仍取决于分支和参数。

- **L775 · 函数** `outbound_scope_decisions(config: Config, order_id: str, selected_factory_orders: Iterable[str] | None = None) -> dict` — 封装出库、范围相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`；`selected_factory_orders: Iterable[str] | None = None`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`；`traveler_assistant/inventory.py:414` `_usable_hardware_factory_orders`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `rows.execute`, `rows.close`, `set`；是否真实写入仍取决于分支和参数。

- **L847 · 函数** `set_outbound_scope(config: Config, order_id: str, scope_type: str, requirement: str, factory_order: str = '', reason: str = '') -> dict` — 设置出库、范围相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`scope_type: str`；`requirement: str`；`factory_order: str = ''`；`reason: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/inventory.py:414` `_usable_hardware_factory_orders`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`；`traveler_assistant/inventory.py:775` `outbound_scope_decisions`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`, `outbound_scope_decisions`；是否真实写入仍取决于分支和参数。

- **L902 · 函数** `build_database_preview(config: Config, order_id: str, selected_factory_orders: Iterable[str] | None = None, production_request_id: str = '', production_materials: Iterable[dict] | None = None, shipment_only: bool = False) -> InventoryPreview` — 从中央 SQLite 事实生成订单级库存/出库预检，不依赖 Traveler 作为事实源。
  - 输入：`config: Config`；`order_id: str`；`selected_factory_orders: Iterable[str] | None = None`；`production_request_id: str = ''`；`production_materials: Iterable[dict] | None = None`；`shipment_only: bool = False`
  - 返回：`InventoryPreview`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1052` `_assert_single_server_material_source`；`traveler_assistant/inventory.py:634` `database_document_items`；`traveler_assistant/inventory.py:775` `outbound_scope_decisions`；`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:1579` `ProductCatalog`；`traveler_assistant/inventory.py:2115` `InventoryMappings.ignored_reason`；`traveler_assistant/inventory.py:98` `TravelerItem.source_snapshot`；`traveler_assistant/inventory.py:2336` `match_item`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`；另有 4 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outbound_scope_decisions`, `catalog_context.close`；是否真实写入仍取决于分支和参数。

- **L1052 · 函数** `_assert_single_server_material_source(config: Config, order_id: str) -> None` — 强制校验Server 数据、材料、来源相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1092 · 函数** `build_factory_room_preview(config: Config, order_id: str, factory_order: str) -> InventoryPreview` — 构建工厂单、预览相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`factory_order: str`
  - 返回：`InventoryPreview`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/order_workflow.py:1282` `parse_material_room_rows`；`traveler_assistant/inventory.py:1143` `build_factory_room_preview.material_identity`；`traveler_assistant/inventory.py:115` `_with_product_code`；`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/inventory.py:1166` `build_factory_room_preview.confirmed_material_code`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:1579` `ProductCatalog`；另有 7 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog_context.close`；是否真实写入仍取决于分支和参数。

- **L1143 · 方法** `build_factory_room_preview.material_identity(kind: str, color: str, thickness: object) -> tuple[str, str, float]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`kind: str`；`color: str`；`thickness: object`
  - 返回：`tuple[str, str, float]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`

- **L1166 · 方法** `build_factory_room_preview.confirmed_material_code(kind: str, color: str, thickness: object) -> str` — 封装材料、编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`kind: str`；`color: str`；`thickness: object`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1143` `build_factory_room_preview.material_identity`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L1273 · 函数** `changed_factory_orders_for_documents(config: Config, order_id: str, selected_factory_orders: Iterable[str], documents: Iterable[dict]) -> set[str]` — 封装工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`；`selected_factory_orders: Iterable[str]`；`documents: Iterable[dict]`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:399` `_database_factory_rows`；`traveler_assistant/core.py:647` `_normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L1297 · 函数** `_fingerprint(payload: dict) -> str` — 封装 `_fingerprint` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`payload: dict`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1302 · 函数** `_find_header(row: Iterable, label: str) -> int | None` — 查找与 `_find_header` 对应的数据或步骤。
  - 输入：`row: Iterable`；`label: str`
  - 返回：`int | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L1309 · 函数** `_order_name_candidates(ws) -> list[str]` — 封装订单、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1322 · 函数** `_normalized_label(value) -> str` — 规范化与 `_normalized_label` 对应的数据或步骤。
  - 输入：`value`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1326 · 函数** `_find_label_row(ws, label: str) -> int` — 查找行数据相关数据或步骤。
  - 输入：`ws`；`label: str`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1322` `_normalized_label`；`traveler_assistant/core.py:44` `RuleError`

- **L1334 · 函数** `_displayed_integer(cell, label: str) -> float` — 封装 `_displayed_integer` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`cell`；`label: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L1351 · 函数** `_nonnegative_number(cell, label: str) -> float` — 封装 `_nonnegative_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`cell`；`label: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L1363 · 函数** `_canonical_usage_color(value: str) -> str` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1370 · 函数** `_usage_list_items(ws, order_id: str) -> tuple[list[TravelerItem], list[TravelerItem]]` — 封装 `_usage_list_items` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`order_id: str`
  - 返回：`tuple[list[TravelerItem], list[TravelerItem]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1326` `_find_label_row`；`traveler_assistant/inventory.py:1322` `_normalized_label`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1392` `_usage_list_items.accumulate`；`traveler_assistant/inventory.py:1363` `_canonical_usage_color`；`traveler_assistant/inventory.py:90` `TravelerItem`

- **L1392 · 方法** `_usage_list_items.accumulate(row: int, name: str, value, integer: bool) -> None` — 封装 `accumulate` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: int`；`name: str`；`value`；`integer: bool`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L1446 · 函数** `parse_traveler(path: Path) -> TravelerData` — 解析Traveler相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`TravelerData`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1309` `_order_name_candidates`；`traveler_assistant/inventory.py:1322` `_normalized_label`；`traveler_assistant/inventory.py:1302` `_find_header`；`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:1370` `_usage_list_items`；`traveler_assistant/inventory.py:98` `TravelerItem.source_snapshot`；`traveler_assistant/inventory.py:128` `TravelerData`；`traveler_assistant/inventory.py:1297` `_fingerprint`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L1565 · 函数** `_catalog_cost_price(value, label: str) -> float | None` — 封装商品目录、成本相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`；`label: str`
  - 返回：`float | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L1579 · 类** `ProductCatalog` — 定义与商品目录相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1580 · 方法** `ProductCatalog.__init__(path: Path)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1586` `ProductCatalog._load`

- **L1586 · 方法** `ProductCatalog._load() -> None` — 读取与 `_load` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:152` `Product`；`traveler_assistant/inventory.py:1565` `_catalog_cost_price`

- **L1631 · 方法** `ProductCatalog.require_code(code: str) -> Product` — 封装编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`code: str`
  - 返回：`Product`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L1642 · 方法** `ProductCatalog.find(category: str | None = None, name: str | None = None, contains: str | None = None, spec_thickness: float | None = None) -> list[Product]` — 查找与 `find` 对应的数据或步骤。
  - 输入：`category: str | None = None`；`name: str | None = None`；`contains: str | None = None`；`spec_thickness: float | None = None`
  - 返回：`list[Product]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`

- **L1666 · 函数** `_ensure_product_cost_column(connection: sqlite3.Connection) -> None` — 封装成本相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`；是否真实写入仍取决于分支和参数。

- **L1676 · 函数** `_ensure_product_brand_column(connection: sqlite3.Connection) -> None` — 封装 `_ensure_product_brand_column` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`；是否真实写入仍取决于分支和参数。

- **L1686 · 类** `ProductDatabase` — 定义与数据库相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1689 · 方法** `ProductDatabase.__init__(path: Path)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1666` `_ensure_product_cost_column`；`traveler_assistant/inventory.py:1676` `_ensure_product_brand_column`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.set_trace_callback`, `self.connection.execute`, `self.connection.close`；是否真实写入仍取决于分支和参数。

- **L1715 · 方法** `ProductDatabase.close() -> None` — 关闭与 `close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.close`；是否真实写入仍取决于分支和参数。

- **L1718 · 方法** `ProductDatabase.__enter__() -> 'ProductDatabase'` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`'ProductDatabase'`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1721 · 方法** `ProductDatabase.__exit__(exc_type, exc_value, traceback) -> None` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：`exc_type`；`exc_value`；`traceback`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.close`；是否真实写入仍取决于分支和参数。

- **L1725 · 方法** `ProductDatabase._from_row(row: sqlite3.Row | tuple) -> Product` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: sqlite3.Row | tuple`
  - 返回：`Product`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:152` `Product`

- **L1743 · 方法** `ProductDatabase.products() -> list[Product]` — 封装 `products` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[Product]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1725` `ProductDatabase._from_row`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1753 · 方法** `ProductDatabase.count() -> int` — 封装 `count` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1756 · 方法** `ProductDatabase.require_code(code: str) -> Product` — 封装编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`code: str`
  - 返回：`Product`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1725` `ProductDatabase._from_row`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1776 · 方法** `ProductDatabase.find(category: str | None = None, name: str | None = None, contains: str | None = None, spec_thickness: float | None = None) -> list[Product]` — 查找与 `find` 对应的数据或步骤。
  - 输入：`category: str | None = None`；`name: str | None = None`；`contains: str | None = None`；`spec_thickness: float | None = None`
  - 返回：`list[Product]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:1725` `ProductDatabase._from_row`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1827 · 函数** `_create_product_database(path: Path) -> None` — 创建数据库相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1666` `_ensure_product_cost_column`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `connection.set_trace_callback`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1863 · 函数** `_replace_product_database(path: Path, products: list[Product]) -> None` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`products: list[Product]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1827` `_create_product_database`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/database.py:67` `catalog_material_attributes`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.set_trace_callback`, `connection.execute`, `set`, `referenced_codes.update`, `connection.executemany`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1983 · 类** `InventoryMappings` — 定义与库存相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1990 · 方法** `InventoryMappings.__init__(path: Path, connection: sqlite3.Connection | None = None)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`path: Path`；`connection: sqlite3.Connection | None = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/database.py:438` `ensure_schema`

- **L2020 · 方法** `InventoryMappings._rows(rule_type: str | None = None) -> list[sqlite3.Row]` — 封装 `_rows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`rule_type: str | None = None`
  - 返回：`list[sqlite3.Row]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2038 · 方法** `InventoryMappings.entries() -> tuple[list[dict], list[dict]]` — 封装 `entries` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`tuple[list[dict], list[dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2020` `InventoryMappings._rows`；`traveler_assistant/inventory.py:2072` `InventoryMappings._effective_display_name`

- **L2072 · 方法** `InventoryMappings._effective_display_name(product_code: str, source_name: str = '', stored_name: str = '') -> str` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`product_code: str`；`source_name: str = ''`；`stored_name: str = ''`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2098 · 方法** `InventoryMappings.display_name_for_product(product_code: str, source_name: str = '') -> str` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`product_code: str`；`source_name: str = ''`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2072` `InventoryMappings._effective_display_name`

- **L2101 · 方法** `InventoryMappings.display_name_for_hardware(product_code: str, source_name: str = '', source_code: str = '') -> str` — 封装名称、五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`product_code: str`；`source_name: str = ''`；`source_code: str = ''`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2072` `InventoryMappings._effective_display_name`；`traveler_assistant/core.py:647` `_normalize_name`

- **L2115 · 方法** `InventoryMappings.ignored_reason(name: str) -> str | None` — 忽略与 `ignored_reason` 对应的数据或步骤。
  - 输入：`name: str`
  - 返回：`str | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2130 · 方法** `InventoryMappings.manual_code(name: str) -> str | None` — 封装编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`
  - 返回：`str | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2145 · 方法** `InventoryMappings.save_ignored(name: str, reason: str) -> None` — 保存与 `save_ignored` 对应的数据或步骤。
  - 输入：`name: str`；`reason: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:2259` `InventoryMappings._save`；`traveler_assistant/inventory.py:2197` `InventoryMappings._upsert`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self._save`, `self._upsert`；是否真实写入仍取决于分支和参数。

- **L2156 · 方法** `InventoryMappings.save_manual(name: str, product_code: str, display_name: str = '') -> None` — 保存与 `save_manual` 对应的数据或步骤。
  - 输入：`name: str`；`product_code: str`；`display_name: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:2101` `InventoryMappings.display_name_for_hardware`；`traveler_assistant/inventory.py:2259` `InventoryMappings._save`；`traveler_assistant/inventory.py:2098` `InventoryMappings.display_name_for_product`；`traveler_assistant/inventory.py:2197` `InventoryMappings._upsert`；`traveler_assistant/inventory.py:2228` `InventoryMappings._set_product_display_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self._save`, `self._upsert`, `self._set_product_display_name`；是否真实写入仍取决于分支和参数。

- **L2181 · 方法** `InventoryMappings.remove_ignored(name: str) -> None` — 移除与 `remove_ignored` 对应的数据或步骤。
  - 输入：`name: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:2259` `InventoryMappings._save`；`traveler_assistant/inventory.py:2248` `InventoryMappings._delete`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self._save`, `self._delete`；是否真实写入仍取决于分支和参数。

- **L2189 · 方法** `InventoryMappings.remove_manual(name: str) -> None` — 移除与 `remove_manual` 对应的数据或步骤。
  - 输入：`name: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:2259` `InventoryMappings._save`；`traveler_assistant/inventory.py:2248` `InventoryMappings._delete`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self._save`, `self._delete`；是否真实写入仍取决于分支和参数。

- **L2197 · 方法** `InventoryMappings._upsert(rule_type: str, source_name: str, normalized: str, product_code: str | None, reason: str, display_name: str = '') -> None` — 新增或更新与 `_upsert` 对应的数据或步骤。
  - 输入：`rule_type: str`；`source_name: str`；`normalized: str`；`product_code: str | None`；`reason: str`；`display_name: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2228 · 方法** `InventoryMappings._set_product_display_name(product_code: str, display_name: str) -> None` — 设置名称相关数据或步骤。
  - 输入：`product_code: str`；`display_name: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2259` `InventoryMappings._save`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self._save`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2248 · 方法** `InventoryMappings._delete(normalized: str, rule_type: str) -> None` — 删除与 `_delete` 对应的数据或步骤。
  - 输入：`normalized: str`；`rule_type: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2259 · 方法** `InventoryMappings._save() -> None` — 保存与 `_save` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.path.parent.mkdir`, `temporary.write_text`, `temporary.replace`；是否真实写入仍取决于分支和参数。

- **L2288 · 函数** `ignored_hardware_reason(mappings: InventoryMappings, name: str = '', code: str = '', source_code: str = '') -> str | None` — 忽略五金相关数据或步骤。
  - 输入：`mappings: InventoryMappings`；`name: str = ''`；`code: str = ''`；`source_code: str = ''`
  - 返回：`str | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:2115` `InventoryMappings.ignored_reason`

- **L2325 · 函数** `_single(catalog: ProductCatalog, matches: list[Product], traveler_name: str, source: str) -> tuple[Product, str]` — 封装 `_single` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`catalog: ProductCatalog`；`matches: list[Product]`；`traveler_name: str`；`source: str`
  - 返回：`tuple[Product, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L2336 · 函数** `match_item(catalog: ProductCatalog, mappings: InventoryMappings, item: TravelerItem) -> list[OutboundItem]` — 匹配项目相关数据或步骤。
  - 输入：`catalog: ProductCatalog`；`mappings: InventoryMappings`；`item: TravelerItem`
  - 返回：`list[OutboundItem]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:2343` `match_item.edge_outbound`；`traveler_assistant/inventory.py:2337` `match_item.outbound`；`traveler_assistant/inventory.py:2115` `InventoryMappings.ignored_reason`；`traveler_assistant/inventory.py:2130` `InventoryMappings.manual_code`；`traveler_assistant/inventory.py:2325` `_single`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `edge_outbound`, `outbound`；是否真实写入仍取决于分支和参数。

- **L2337 · 方法** `match_item.outbound(product: Product, quantity: float, source: str) -> OutboundItem` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`product: Product`；`quantity: float`；`source: str`
  - 返回：`OutboundItem`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:169` `OutboundItem`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `OutboundItem`；是否真实写入仍取决于分支和参数。

- **L2343 · 方法** `match_item.edge_outbound(product: Product, source: str) -> OutboundItem` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`product: Product`；`source: str`
  - 返回：`OutboundItem`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2337` `match_item.outbound`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outbound`；是否真实写入仍取决于分支和参数。

- **L2430 · 函数** `resolve_inventory_items(config: Config, items: Iterable[tuple[TravelerItem, str]]) -> dict` — 解析并确定库存相关数据或步骤。
  - 输入：`config: Config`；`items: Iterable[tuple[TravelerItem, str]]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/command_router.py:43` `normalize_spoken_order_ids.replace`；`traveler_assistant/inventory.py:2288` `ignored_hardware_reason`；`traveler_assistant/inventory.py:2115` `InventoryMappings.ignored_reason`；`traveler_assistant/inventory.py:98` `TravelerItem.source_snapshot`；`traveler_assistant/inventory.py:2336` `match_item`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `replace`；是否真实写入仍取决于分支和参数。

- **L2506 · 函数** `resolved_product_code(resolution: dict, index: int) -> str` — 解析并确定编码相关数据或步骤。
  - 输入：`resolution: dict`；`index: int`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L2516 · 函数** `confirm_product_material_attributes(connection: sqlite3.Connection, product_code: str, material_kind: str, material_color: str = '', material_thickness: object = '') -> None` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`product_code: str`；`material_kind: str`；`material_color: str = ''`；`material_thickness: object = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:647` `_normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L2586 · 函数** `build_preview(path: Path, catalog_path: Path, mapping_path: Path, selected_document_remarks: Iterable[str] | None = None) -> InventoryPreview` — 解析 Traveler 并结合商品目录/映射生成只读库存预检。
  - 输入：`path: Path`；`catalog_path: Path`；`mapping_path: Path`；`selected_document_remarks: Iterable[str] | None = None`
  - 返回：`InventoryPreview`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1446` `parse_traveler`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:1579` `ProductCatalog`；`traveler_assistant/inventory.py:2115` `InventoryMappings.ignored_reason`；`traveler_assistant/inventory.py:98` `TravelerItem.source_snapshot`；`traveler_assistant/inventory.py:2336` `match_item`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`；`traveler_assistant/inventory.py:181` `InventoryPreview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog_context.close`；是否真实写入仍取决于分支和参数。

- **L2668 · 函数** `set_ignored_mapping(config: Config, name: str, ignored: bool, reason: str = '') -> dict` — 设置映射相关数据或步骤。
  - 输入：`config: Config`；`name: str`；`ignored: bool`；`reason: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:2145` `InventoryMappings.save_ignored`；`traveler_assistant/inventory.py:2181` `InventoryMappings.remove_ignored`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_ignored`；是否真实写入仍取决于分支和参数。

- **L2684 · 函数** `update_ignored_mapping(config: Config, old_name: str, name: str, reason: str = '') -> dict` — 更新映射相关数据或步骤。
  - 输入：`config: Config`；`old_name: str`；`name: str`；`reason: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:2181` `InventoryMappings.remove_ignored`；`traveler_assistant/inventory.py:2145` `InventoryMappings.save_ignored`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_ignored`；是否真实写入仍取决于分支和参数。

- **L2704 · 函数** `list_inventory_mappings(config: Config) -> dict` — 列出库存相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:2038` `InventoryMappings.entries`

- **L2715 · 函数** `search_inventory_products(config: Config, query: str) -> dict` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`query: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`

- **L2731 · 函数** `save_manual_mapping(config: Config, name: str, product_code: str, display_name: str = '') -> dict` — 保存映射相关数据或步骤。
  - 输入：`config: Config`；`name: str`；`product_code: str`；`display_name: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:2156` `InventoryMappings.save_manual`；`traveler_assistant/inventory.py:2101` `InventoryMappings.display_name_for_hardware`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_manual`；是否真实写入仍取决于分支和参数。

- **L2746 · 函数** `remove_manual_mapping(config: Config, name: str) -> dict` — 移除映射相关数据或步骤。
  - 输入：`config: Config`；`name: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:2189` `InventoryMappings.remove_manual`

- **L2752 · 函数** `update_manual_mapping(config: Config, old_name: str, name: str, product_code: str, display_name: str = '') -> dict` — 更新映射相关数据或步骤。
  - 输入：`config: Config`；`old_name: str`；`name: str`；`product_code: str`；`display_name: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:2189` `InventoryMappings.remove_manual`；`traveler_assistant/inventory.py:2156` `InventoryMappings.save_manual`；`traveler_assistant/inventory.py:2101` `InventoryMappings.display_name_for_hardware`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_manual`；是否真实写入仍取决于分支和参数。

- **L2774 · 类** `InventoryOperationJournal` — 定义与库存、操作相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2782 · 方法** `InventoryOperationJournal.__init__(database: Path)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`database: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:438` `ensure_schema`

- **L2787 · 方法** `InventoryOperationJournal._canonical(value: object) -> str` — 封装 `_canonical` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: object`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2790 · 方法** `InventoryOperationJournal.prepare(operation_kind: str, order_id: str, factory_orders: Iterable[str], payload: dict) -> dict` — 准备并校验与 `prepare` 对应的数据或步骤。
  - 输入：`operation_kind: str`；`order_id: str`；`factory_orders: Iterable[str]`；`payload: dict`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2787` `InventoryOperationJournal._canonical`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2860 · 方法** `InventoryOperationJournal.update(operation_id: str, status: str, results: Iterable[dict] | None = None, error: str = '', increment_attempt: bool = False) -> None` — 更新与 `update` 对应的数据或步骤。
  - 输入：`operation_id: str`；`status: str`；`results: Iterable[dict] | None = None`；`error: str = ''`；`increment_attempt: bool = False`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:2787` `InventoryOperationJournal._canonical`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2889 · 方法** `InventoryOperationJournal.decoded_payload(row: dict) -> dict` — 封装 `decoded_payload` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2897 · 方法** `InventoryOperationJournal.decoded_results(row: dict) -> list[dict]` — 封装 `decoded_results` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2905 · 类** `InventorySyncStore` — 定义与库存相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2906 · 方法** `InventorySyncStore.__init__(path: Path, backup_root: Path)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`path: Path`；`backup_root: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:438` `ensure_schema`

- **L2916 · 方法** `InventorySyncStore.key(order_id: str, remark: str) -> str` — 封装 `key` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`order_id: str`；`remark: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`

- **L2922 · 方法** `InventorySyncStore.raw_document_fingerprint(items: list[TravelerItem]) -> str` — 封装 `raw_document_fingerprint` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: list[TravelerItem]`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1297` `_fingerprint`；`traveler_assistant/core.py:647` `_normalize_name`

- **L2934 · 方法** `InventorySyncStore.mapped_document_fingerprint(items: list[OutboundItem]) -> str` — 封装 `mapped_document_fingerprint` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: list[OutboundItem]`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1297` `_fingerprint`

- **L2943 · 方法** `InventorySyncStore.canonical_document_fingerprint(items: list[TravelerItem]) -> str | None` — 封装 `canonical_document_fingerprint` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: list[TravelerItem]`
  - 返回：`str | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1297` `_fingerprint`

- **L2968 · 方法** `InventorySyncStore._records() -> list[dict]` — 记录与 `_records` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L3010 · 方法** `InventorySyncStore.record_for_document(order_id: str, remark: str) -> dict | None` — 记录记录相关数据或步骤。
  - 输入：`order_id: str`；`remark: str`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:2968` `InventorySyncStore._records`

- **L3022 · 方法** `InventorySyncStore.records_for_order(order_id: str) -> list[dict]` — 记录订单相关数据或步骤。
  - 输入：`order_id: str`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:2968` `InventorySyncStore._records`

- **L3029 · 方法** `InventorySyncStore.status_for(traveler: TravelerData) -> tuple[str, str]` — 封装状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`traveler: TravelerData`
  - 返回：`tuple[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3022` `InventorySyncStore.records_for_order`；`traveler_assistant/inventory.py:3010` `InventorySyncStore.record_for_document`；`traveler_assistant/inventory.py:2922` `InventorySyncStore.raw_document_fingerprint`；`traveler_assistant/inventory.py:2943` `InventorySyncStore.canonical_document_fingerprint`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `self.record_for_document`；是否真实写入仍取决于分支和参数。

- **L3067 · 方法** `InventorySyncStore.prepare_documents(preview: InventoryPreview) -> list[dict]` — 准备并校验与 `prepare_documents` 对应的数据或步骤。
  - 输入：`preview: InventoryPreview`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:243` `InventoryPreview._selected_document_set`；`traveler_assistant/inventory.py:3022` `InventorySyncStore.records_for_order`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:257` `InventoryPreview.document_payloads`；`traveler_assistant/inventory.py:169` `OutboundItem`；`traveler_assistant/inventory.py:3010` `InventorySyncStore.record_for_document`；`traveler_assistant/inventory.py:2934` `InventorySyncStore.mapped_document_fingerprint`；`traveler_assistant/inventory.py:2922` `InventorySyncStore.raw_document_fingerprint`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview._selected_document_set`, `OutboundItem`, `self.record_for_document`；是否真实写入仍取决于分支和参数。

- **L3131 · 方法** `InventorySyncStore.save_success(preview: InventoryPreview, results: list[dict], production_draft: dict | None = None, operation_id: str = '', commit_operation: bool = True, commit_production: bool = True) -> None` — 保存与 `save_success` 对应的数据或步骤。
  - 输入：`preview: InventoryPreview`；`results: list[dict]`；`production_draft: dict | None = None`；`operation_id: str = ''`；`commit_operation: bool = True`；`commit_production: bool = True`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3220` `InventorySyncStore._backup_current`；`traveler_assistant/inventory.py:3067` `InventorySyncStore.prepare_documents`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/database.py:302` `ensure_outbound_document_factory_links`；`traveler_assistant/production.py:383` `record_completed_production`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `ensure_outbound_document_factory_links`, `record_completed_production`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L3220 · 方法** `InventorySyncStore._backup_current() -> None` — 封装备份相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `backup_root.mkdir`, `destination.unlink`, `old.unlink`；是否真实写入仍取决于分支和参数。

- **L3250 · 函数** `_catalog_path(config: Config) -> Path` — 封装商品目录、路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3254 · 函数** `_database_path(config: Config) -> Path` — 封装数据库、路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3259 · 函数** `_catalog_info(config: Config) -> dict` — 封装商品目录相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3254` `_database_path`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3250` `_catalog_path`；`traveler_assistant/inventory.py:1753` `ProductDatabase.count`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `loaded.close`；是否真实写入仍取决于分支和参数。

- **L3279 · 函数** `_sync_path(config: Config) -> Path` — 同步路径相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3283 · 函数** `_persist_completed_outbound_results(config: Config, preview: InventoryPreview | None, confirm_save: bool, responses: list[dict]) -> list[str]` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`preview: InventoryPreview | None`；`confirm_save: bool`；`responses: list[dict]`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3131` `InventorySyncStore.save_success`；`traveler_assistant/inventory.py:2905` `InventorySyncStore`；`traveler_assistant/inventory.py:3279` `_sync_path`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `InventorySyncStore(_sync_path(config), config.backup_root).save_success`；是否真实写入仍取决于分支和参数。

- **L3314 · 函数** `_persist_single_outbound_result(config: Config, preview: InventoryPreview | None, result: dict, production_draft: dict | None = None) -> str` — 封装出库、结果相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`preview: InventoryPreview | None`；`result: dict`；`production_draft: dict | None = None`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:3131` `InventorySyncStore.save_success`；`traveler_assistant/inventory.py:2905` `InventorySyncStore`；`traveler_assistant/inventory.py:3279` `_sync_path`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `InventorySyncStore(_sync_path(config), config.backup_root).save_success`；是否真实写入仍取决于分支和参数。

- **L3341 · 函数** `bootstrap_catalog(config: Config) -> Path` — 封装商品目录相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3250` `_catalog_path`；`traveler_assistant/inventory.py:1579` `ProductCatalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `destination.parent.mkdir`；是否真实写入仍取决于分支和参数。

- **L3355 · 函数** `bootstrap_product_database(config: Config) -> Path` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3254` `_database_path`；`traveler_assistant/inventory.py:3341` `bootstrap_catalog`；`traveler_assistant/inventory.py:1715` `ProductDatabase.close`；`traveler_assistant/inventory.py:3489` `import_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L3385 · 函数** `reconcile_folder_status(config: Config, folder: str) -> dict` — 对账并重算文件夹、状态相关数据或步骤。
  - 输入：`config: Config`；`folder: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1446` `parse_traveler`；`traveler_assistant/inventory.py:3866` `run_jdy`；`traveler_assistant/inventory.py:2905` `InventorySyncStore`；`traveler_assistant/inventory.py:3279` `_sync_path`；`traveler_assistant/core.py:647` `_normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`, `set`；是否真实写入仍取决于分支和参数。

- **L3428 · 函数** `list_travelers(config: Config, include_history: bool = False) -> dict` — 列出与 `list_travelers` 对应的数据或步骤。
  - 输入：`config: Config`；`include_history: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:2905` `InventorySyncStore`；`traveler_assistant/inventory.py:3279` `_sync_path`；`traveler_assistant/inventory.py:1446` `parse_traveler`；`traveler_assistant/inventory.py:3029` `InventorySyncStore.status_for`；`traveler_assistant/inventory.py:3259` `_catalog_info`

- **L3458 · 函数** `list_traveler_names(config: Config) -> dict` — 列出Traveler相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2905` `InventorySyncStore`；`traveler_assistant/inventory.py:3279` `_sync_path`；`traveler_assistant/inventory.py:2968` `InventorySyncStore._records`；`traveler_assistant/inventory.py:3259` `_catalog_info`

- **L3489 · 函数** `import_catalog(config: Config, source: Path) -> dict` — 导入商品目录相关数据或步骤。
  - 输入：`config: Config`；`source: Path`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1579` `ProductCatalog`；`traveler_assistant/inventory.py:3250` `_catalog_path`；`traveler_assistant/inventory.py:1863` `_replace_product_database`；`traveler_assistant/inventory.py:3254` `_database_path`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `destination.parent.mkdir`, `_replace_product_database`, `os.replace`, `old.unlink`；是否真实写入仍取决于分支和参数。

- **L3506 · 函数** `_catalog_change_summary(previous: list[Product], current: list[Product]) -> dict[str, int]` — 封装商品目录相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`previous: list[Product]`；`current: list[Product]`
  - 返回：`dict[str, int]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:647` `_normalize_name`；`traveler_assistant/inventory.py:3507` `_catalog_change_summary.signature`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L3507 · 方法** `_catalog_change_summary.signature(product: Product) -> tuple[str, ...]` — 封装 `signature` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`product: Product`
  - 返回：`tuple[str, ...]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3539 · 函数** `_existing_catalog_products(config: Config) -> list[Product]` — 封装商品目录相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`list[Product]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3250` `_catalog_path`；`traveler_assistant/inventory.py:1579` `ProductCatalog`；`traveler_assistant/inventory.py:3254` `_database_path`；`traveler_assistant/inventory.py:1686` `ProductDatabase`

- **L3550 · 函数** `update_catalog_online(config: Config) -> dict` — 更新商品目录相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3250` `_catalog_path`；`traveler_assistant/core.py:118` `progress`；`traveler_assistant/inventory.py:3539` `_existing_catalog_products`；`traveler_assistant/inventory.py:3866` `run_jdy`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1579` `ProductCatalog`；`traveler_assistant/inventory.py:3506` `_catalog_change_summary`；`traveler_assistant/inventory.py:3489` `import_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `inventory_dir.mkdir`, `run_jdy`, `download.unlink`；是否真实写入仍取决于分支和参数。

- **L3574 · 函数** `_local_setting(config: Config, name: str) -> str` — 封装 `_local_setting` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`name: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3584 · 函数** `_inventory_cdp_endpoint() -> str` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3590 · 函数** `_inventory_cdp_pages(endpoint: str) -> list[dict]` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`endpoint: str`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3600 · 函数** `_find_existing_inventory_page(endpoint: str) -> dict | None` — 查找库存相关数据或步骤。
  - 输入：`endpoint: str`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3590` `_inventory_cdp_pages`；`traveler_assistant/inventory.py:3637` `_is_inventory_authenticated_url`；`traveler_assistant/inventory.py:3642` `_is_inventory_service_workbench_url`

- **L3612 · 函数** `_is_inventory_domain_url(url: str) -> bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`url: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3624 · 函数** `_is_inventory_login_or_global_url(url: str) -> bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`url: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3637 · 函数** `_is_inventory_authenticated_url(url: str) -> bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`url: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3612` `_is_inventory_domain_url`；`traveler_assistant/inventory.py:3624` `_is_inventory_login_or_global_url`

- **L3642 · 函数** `_is_inventory_service_workbench_url(url: str) -> bool` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`url: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3653 · 函数** `_inventory_chrome_profile(config: Config) -> Path` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3657 · 函数** `_inventory_chrome_executable() -> Path | None` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Path | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3672 · 函数** `open_inventory_chrome(config: Config) -> dict` — 打开库存相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3584` `_inventory_cdp_endpoint`；`traveler_assistant/inventory.py:3590` `_inventory_cdp_pages`；`traveler_assistant/inventory.py:3637` `_is_inventory_authenticated_url`；`traveler_assistant/inventory.py:3642` `_is_inventory_service_workbench_url`；`traveler_assistant/inventory.py:3612` `_is_inventory_domain_url`；`traveler_assistant/inventory.py:3657` `_inventory_chrome_executable`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:3653` `_inventory_chrome_profile`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `profile.mkdir`, `subprocess.Popen`；是否真实写入仍取决于分支和参数。

- **L3739 · 函数** `close_inventory_chrome(config: Config) -> dict` — 关闭库存相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3838` `_resolve_jdy_runtime`；`traveler_assistant/inventory.py:3584` `_inventory_cdp_endpoint`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `os.environ.copy`, `subprocess.run`；是否真实写入仍取决于分支和参数。

- **L3770 · 函数** `_keychain_password(account: str) -> str` — 封装 `_keychain_password` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`account: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `subprocess.run`；是否真实写入仍取决于分支和参数。

- **L3789 · 函数** `_jdy_error_detail(stderr: str) -> str` — 封装 `_jdy_error_detail` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`stderr: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3790` `_jdy_error_detail.concise`

- **L3790 · 方法** `_jdy_error_detail.concise(detail: str) -> str` — 封装 `concise` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`detail: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3838 · 函数** `_resolve_jdy_runtime(root: Path) -> tuple[Path, Path]` — 解析并确定与 `_resolve_jdy_runtime` 对应的数据或步骤。
  - 输入：`root: Path`
  - 返回：`tuple[Path, Path]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L3866 · 函数** `run_jdy(config: Config, action: str, traveler_path: Path | None = None, confirm_save: bool = False, download_path: Path | None = None, order_name: str = '', stock_items: list[dict] | None = None, selected_document_remarks: Iterable[str] | None = None, selected_factory_orders: Iterable[str] | None = None, order_id: str = '', room_material: bool = False, production_request_id: str = '', production_materials: Iterable[dict] | None = None, shipment_only: bool = False) -> dict` — 执行与 `run_jdy` 对应的数据或步骤。
  - 输入：`config: Config`；`action: str`；`traveler_path: Path | None = None`；`confirm_save: bool = False`；`download_path: Path | None = None`；`order_name: str = ''`；`stock_items: list[dict] | None = None`；`selected_document_remarks: Iterable[str] | None = None`；`selected_factory_orders: Iterable[str] | None = None`；`order_id: str = ''`；`room_material: bool = False`；`production_request_id: str = ''`；`production_materials: Iterable[dict] | None = None`；`shipment_only: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:118` `progress`；`traveler_assistant/production.py:212` `cumulative_production_materials`；`traveler_assistant/inventory.py:3574` `_local_setting`；`traveler_assistant/inventory.py:3584` `_inventory_cdp_endpoint`；`traveler_assistant/inventory.py:3600` `_find_existing_inventory_page`；`traveler_assistant/inventory.py:3642` `_is_inventory_service_workbench_url`；`traveler_assistant/inventory.py:3770` `_keychain_password`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1092` `build_factory_room_preview`；`traveler_assistant/inventory.py:902` `build_database_preview`；`traveler_assistant/inventory.py:2586` `build_preview`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；另有 21 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mark_no_hardware_outbound`, `mark_customer_supplied_outbound`, `assert_factory_orders_outbound_allowed`, `operation_journal.update`, `request.update`, `os.environ.copy`, `subprocess.Popen`, `process.stdin.write`, `process.stdin.close`, `_persist_completed_outbound_results`；是否真实写入仍取决于分支和参数。

- **L4194 · 方法** `run_jdy.forward_browser_progress() -> None` — 封装进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:201` `log_progress_payload`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sys.stderr.write`；是否真实写入仍取决于分支和参数。

- **L4407 · 函数** `_check_requirements_stock(config: Config, requirements: list[dict]) -> list[dict]` — 检查与 `_check_requirements_stock` 对应的数据或步骤。
  - 输入：`config: Config`；`requirements: list[dict]`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:3866` `run_jdy`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:647` `_normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`；是否真实写入仍取决于分支和参数。

- **L4442 · 函数** `check_stock(config: Config, traveler_path: Path, include_hardware: bool = False) -> dict` — 调用库存读取流程并比较需求量、可用量与缺口。
  - 输入：`config: Config`；`traveler_path: Path`；`include_hardware: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2586` `build_preview`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:280` `stock_requirements`；`traveler_assistant/inventory.py:4407` `_check_requirements_stock`

- **L4460 · 函数** `check_order_stock(config: Config, order_folder: Path) -> dict` — 检查订单相关数据或步骤。
  - 输入：`config: Config`；`order_folder: Path`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:344` `order_stock_requirements`；`traveler_assistant/inventory.py:4407` `_check_requirements_stock`

- **L4472 · 函数** `check_database_stock(config: Config, order_id: str) -> dict` — 检查数据库相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:316` `database_stock_requirements`；`traveler_assistant/inventory.py:4407` `_check_requirements_stock`

- **L4485 · 函数** `inventory_main(argv: list[str] | None = None) -> int` — 库存 CLI 入口：解析子命令并调用查询、映射、预检或出库流程。
  - 输入：`argv: list[str] | None = None`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:125` `Config`；`traveler_assistant/operation_log.py:192` `configure_operation_log`；`traveler_assistant/inventory.py:3428` `list_travelers`；`traveler_assistant/inventory.py:3458` `list_traveler_names`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:212` `InventoryPreview.payload`；`traveler_assistant/inventory.py:2586` `build_preview`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/inventory.py:902` `build_database_preview`；`traveler_assistant/inventory.py:775` `outbound_scope_decisions`；`traveler_assistant/inventory.py:847` `set_outbound_scope`；`traveler_assistant/inventory.py:3489` `import_catalog`；另有 13 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outbound_scope_decisions`, `set_outbound_scope`, `update_catalog_online`, `open_inventory_chrome`, `close_inventory_chrome`, `run_jdy`, `save_manual_mapping`, `update_manual_mapping`, `update_ignored_mapping`, `set_ignored_mapping`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/operation_log.py`

JSONL 操作日志、脱敏和数据库语句记录。

- **L41 · 函数** `_is_sensitive_key(key: str) -> bool` — 封装 `_is_sensitive_key` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`key: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `key.replace`；是否真实写入仍取决于分支和参数。

- **L46 · 函数** `_redact_url(match: re.Match[str]) -> str` — 封装 `_redact_url` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`match: re.Match[str]`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L60 · 函数** `_secret_variants(value: Any) -> set[str]` — 封装 `_secret_variants` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: Any`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L74 · 函数** `_redact_text(value: str, sensitive_values: tuple[str, ...] = ()) -> str` — 封装 `_redact_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: str`；`sensitive_values: tuple[str, ...] = ()`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:60` `_secret_variants`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `value.replace`；是否真实写入仍取决于分支和参数。

- **L94 · 函数** `redact(value: Any, key: str | None = None, sensitive_values: tuple[str, ...] = ()) -> Any` — 封装 `redact` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: Any`；`key: str | None = None`；`sensitive_values: tuple[str, ...] = ()`
  - 返回：`Any`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:41` `_is_sensitive_key`；`traveler_assistant/operation_log.py:94` `redact`；`traveler_assistant/operation_log.py:74` `_redact_text`

- **L112 · 函数** `operation_log_enabled_from_environment() -> bool` — 封装操作、日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L116 · 函数** `write_operation_log(path: Path, event: str, message: str, actor: str = 'app', component: str = 'python', details: dict[str, Any] | None = None, enabled: bool = True, session_id: str | None = None, operation_id: str | None = None, sensitive_values: tuple[str, ...] = ()) -> None` — 写入操作、日志相关数据或步骤。
  - 输入：`path: Path`；`event: str`；`message: str`；`actor: str = 'app'`；`component: str = 'python'`；`details: dict[str, Any] | None = None`；`enabled: bool = True`；`session_id: str | None = None`；`operation_id: str | None = None`；`sensitive_values: tuple[str, ...] = ()`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:94` `redact`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `os.open`, `os.write`, `os.close`；是否真实写入仍取决于分支和参数。

- **L163 · 类** `OperationLogger` — 定义与操作相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L164 · 方法** `OperationLogger.__init__(path: Path, enabled: bool = True, session_id: str | None = None)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`path: Path`；`enabled: bool = True`；`session_id: str | None = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L169 · 方法** `OperationLogger.event(event: str, message: str, actor: str = 'app', component: str = 'python', details: dict[str, Any] | None = None, operation_id: str | None = None) -> None` — 封装 `event` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`event: str`；`message: str`；`actor: str = 'app'`；`component: str = 'python'`；`details: dict[str, Any] | None = None`；`operation_id: str | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:116` `write_operation_log`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_operation_log`；是否真实写入仍取决于分支和参数。

- **L192 · 函数** `configure_operation_log(config: Any) -> OperationLogger` — 封装操作、日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Any`
  - 返回：`OperationLogger`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:163` `OperationLogger`

- **L201 · 函数** `log_progress_payload(payload: dict[str, Any], sensitive_values: tuple[str, ...] = ()) -> None` — 封装日志、进度相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`payload: dict[str, Any]`；`sensitive_values: tuple[str, ...] = ()`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:116` `write_operation_log`；`traveler_assistant/operation_log.py:112` `operation_log_enabled_from_environment`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_operation_log`；是否真实写入仍取决于分支和参数。

- **L221 · 函数** `log_aimes_failure(error: str, code: str, stage: str = '', enabled: bool = True, sensitive_values: tuple[str, ...] = ()) -> None` — 封装日志、AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`error: str`；`code: str`；`stage: str = ''`；`enabled: bool = True`；`sensitive_values: tuple[str, ...] = ()`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:116` `write_operation_log`；`traveler_assistant/operation_log.py:112` `operation_log_enabled_from_environment`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_operation_log`；是否真实写入仍取决于分支和参数。

- **L244 · 函数** `log_database_statement(path: Path, statement: str) -> None` — 封装日志、数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`statement: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/operation_log.py:116` `write_operation_log`；`traveler_assistant/operation_log.py:112` `operation_log_enabled_from_environment`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_operation_log`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/order_details.py`

从中央事实组装订单详情和 Panel 展示数据。

- **L12 · 函数** `order_detail(config: Config, order_id: str) -> dict` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/order_index.py`

订单索引核心：AIMES、Server、问题、确认、状态与同步证据。

- **L80 · 函数** `install_shared_workflow_connection(path: Path, connection: sqlite3.Connection) -> None` — 封装 `install_shared_workflow_connection` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`connection: sqlite3.Connection`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:20` `enable_foreign_keys`

- **L87 · 函数** `clear_shared_workflow_connection() -> None` — 清理与 `clear_shared_workflow_connection` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L93 · 函数** `_shared_workflow_connection(path: Path) -> sqlite3.Connection | None` — 封装 `_shared_workflow_connection` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`sqlite3.Connection | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L106 · 函数** `_now() -> str` — 封装 `_now` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L110 · 函数** `_order_id_from_factory_name(name: str) -> str` — 封装订单、工厂单、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L115 · 函数** `_order_type(order_id: str) -> str` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`order_id: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L119 · 函数** `_server_root_candidates(config: Config) -> list[Path]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L143 · 函数** `_available_server_roots(config: Config) -> list[Path]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:119` `_server_root_candidates`

- **L147 · 函数** `_server_root_order_type(root: Path) -> str` — 封装Server 数据、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`root: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L151 · 函数** `_server_folder_matches_root(folder: Path, root: Path, order_ids: set[str]) -> bool` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`；`root: Path`；`order_ids: set[str]`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:115` `_order_type`；`traveler_assistant/order_index.py:147` `_server_root_order_type`

- **L160 · 函数** `_is_standard_order_folder(name: str) -> bool` — 封装订单、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L165 · 函数** `_is_traveler_file(path: Path) -> bool` — 封装Traveler、文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L170 · 函数** `_folder_created_at(folder: Path) -> float` — 封装文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`float`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L176 · 函数** `_path_created_at(path: Path, stat = None) -> float` — 封装路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`stat = None`
  - 返回：`float`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L182 · 函数** `_display_timestamp(value: float) -> str` — 封装 `_display_timestamp` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: float`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L186 · 函数** `_mtime_marker(stat) -> int` — 封装 `_mtime_marker` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`stat`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L197 · 函数** `_file_content_fingerprint(path: Path) -> str` — 封装文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.open`, `digest.update`；是否真实写入仍取决于分支和参数。

- **L206 · 函数** `_material_source_fingerprint(store: 'OrderIndexStore', path: Path) -> str` — 封装材料、来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: 'OrderIndexStore'`；`path: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:197` `_file_content_fingerprint`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L221 · 函数** `_material_fact_fingerprint(source_fingerprint: str, product_code: str) -> str` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`source_fingerprint: str`；`product_code: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L230 · 函数** `_replace_server_material_facts(store: 'OrderIndexStore', order_id: str, path: Path, parsed_materials: list, parsed_edges: dict[str, float], mappings: InventoryMappings, observed_at: str) -> None` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: 'OrderIndexStore'`；`order_id: str`；`path: Path`；`parsed_materials: list`；`parsed_edges: dict[str, float]`；`mappings: InventoryMappings`；`observed_at: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2419` `_is_recut_material_source`；`traveler_assistant/order_index.py:263` `_insert_server_material_source_facts`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `_insert_server_material_source_facts`；是否真实写入仍取决于分支和参数。

- **L263 · 函数** `_insert_server_material_source_facts(store: 'OrderIndexStore', order_id: str, path: Path, parsed_materials: list, parsed_edges: dict[str, float], mappings: InventoryMappings, observed_at: str) -> None` — 插入Server 数据、材料、来源相关数据或步骤。
  - 输入：`store: 'OrderIndexStore'`；`order_id: str`；`path: Path`；`parsed_materials: list`；`parsed_edges: dict[str, float]`；`mappings: InventoryMappings`；`observed_at: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:206` `_material_source_fingerprint`；`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/order_workflow.py:2019` `_material_inventory_name`；`traveler_assistant/inventory.py:2336` `match_item`；`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:2516` `confirm_product_material_attributes`；`traveler_assistant/order_index.py:221` `_material_fact_fingerprint`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L319 · 函数** `_replace_server_incremental_material_facts(store: 'OrderIndexStore', order_id: str, path: Path, parsed_materials: list, parsed_edges: dict[str, float], mappings: InventoryMappings, observed_at: str) -> None` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: 'OrderIndexStore'`；`order_id: str`；`path: Path`；`parsed_materials: list`；`parsed_edges: dict[str, float]`；`mappings: InventoryMappings`；`observed_at: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:263` `_insert_server_material_source_facts`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `_insert_server_material_source_facts`；是否真实写入仍取决于分支和参数。

- **L340 · 函数** `_server_scan_baseline(config: Config) -> float` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`float`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L347 · 函数** `_valid_aimes_order_id(value: str) -> str` — 封装AIMES 数据、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L354 · 函数** `_normalize_split_time(value: str) -> str` — 规范化时间相关数据或步骤。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `str(value or '').strip().replace`；是否真实写入仍取决于分支和参数。

- **L371 · 函数** `_factory_order_date(factory_order: str) -> date | None` — 封装工厂单、订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`factory_order: str`
  - 返回：`date | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L382 · 函数** `_factory_order_before_initial_date(factory_order: str, split_time: str, initial_date: str) -> bool` — 封装工厂单、订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`factory_order: str`；`split_time: str`；`initial_date: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:371` `_factory_order_date`；`traveler_assistant/order_index.py:354` `_normalize_split_time`

- **L409 · 函数** `_aimes_order_fingerprint(store: 'OrderIndexStore', order_id: str) -> str` — 封装AIMES 数据、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: 'OrderIndexStore'`；`order_id: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L440 · 函数** `_order_is_before_initial_date(config: Config, store: 'OrderIndexStore', order_id: str, folder: Path) -> bool` — 封装订单、日期相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: 'OrderIndexStore'`；`order_id: str`；`folder: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:382` `_factory_order_before_initial_date`；`traveler_assistant/order_index.py:170` `_folder_created_at`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L468 · 函数** `_order_has_active_aimes_mapping(store: 'OrderIndexStore', order_id: str) -> bool` — 封装订单、AIMES 数据、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: 'OrderIndexStore'`；`order_id: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L482 · 函数** `_order_shipped_watch_until(store: 'OrderIndexStore', order_id: str, now: str) -> str` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: 'OrderIndexStore'`；`order_id: str`；`now: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L519 · 函数** `_datetime_timestamp(value: str) -> float` — 封装 `_datetime_timestamp` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L524 · 函数** `_visible_aimes_row(row: dict) -> dict | None` — 封装AIMES 数据、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:556` `_aimes_row_issue`；`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`；`traveler_assistant/order_index.py:354` `_normalize_split_time`

- **L541 · 函数** `_aimes_ignore_key(row: dict) -> str` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L556 · 函数** `_aimes_row_issue(row: dict) -> dict | None` — 封装AIMES 数据、行数据、待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:110` `_order_id_from_factory_name`；`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`；`traveler_assistant/core.py:102` `factory_name_order_mismatch`；`traveler_assistant/order_index.py:541` `_aimes_ignore_key`；`traveler_assistant/order_index.py:354` `_normalize_split_time`

- **L590 · 函数** `_partition_aimes_rows(rows: list[dict], ignored_keys: set[str], assignments: dict[str, str] | None = None) -> tuple[list[dict], list[dict]]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`rows: list[dict]`；`ignored_keys: set[str]`；`assignments: dict[str, str] | None = None`
  - 返回：`tuple[list[dict], list[dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:541` `_aimes_ignore_key`；`traveler_assistant/order_index.py:354` `_normalize_split_time`；`traveler_assistant/order_index.py:556` `_aimes_row_issue`；`traveler_assistant/order_index.py:524` `_visible_aimes_row`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L625 · 函数** `_merge_aimes_recent_and_verified_rows(recent_rows: list[dict], verification_result: dict | None, cached_rows: list[dict] | None = None) -> list[dict]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`recent_rows: list[dict]`；`verification_result: dict | None`；`cached_rows: list[dict] | None = None`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:643` `_merge_aimes_recent_and_verified_rows.retain_cached_split_time`

- **L643 · 方法** `_merge_aimes_recent_and_verified_rows.retain_cached_split_time(row: dict) -> dict` — 封装时间相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L668 · 函数** `_business_validation_message(exc: Exception) -> str` — 封装 `_business_validation_message` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`exc: Exception`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L685 · 函数** `_business_aimes_message(exc: Exception) -> str` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`exc: Exception`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L702 · 函数** `_business_server_message(exc: Exception) -> str` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`exc: Exception`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L711 · 函数** `_business_report_message(kind: str, path: Path) -> str` — 封装 `_business_report_message` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`kind: str`；`path: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L716 · 函数** `_source_path_in_dashboard_scope(root: Path, value: str) -> bool` — 封装来源、路径、看板、范围相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`root: Path`；`value: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`

- **L730 · 类** `OrderIndexStore` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L733 · 方法** `OrderIndexStore.__init__(path: Path, connection: sqlite3.Connection | None = None)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`path: Path`；`connection: sqlite3.Connection | None = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:93` `_shared_workflow_connection`；`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/database.py:20` `enable_foreign_keys`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/database.py:1401` `collapse_actual_installation_days`；`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1444` `OrderIndexStore.upsert_order`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `self.connection.execute`, `self.connection.set_trace_callback`, `self.connection.close`, `self.upsert_order`, `self.connection.commit`；是否真实写入仍取决于分支和参数。

- **L1122 · 方法** `OrderIndexStore.close() -> None` — 关闭与 `close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.close`；是否真实写入仍取决于分支和参数。

- **L1126 · 方法** `OrderIndexStore.temporary_order(source_folder: str) -> dict | None` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`source_folder: str`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1157 · 方法** `OrderIndexStore.upsert_temporary_order(temporary_id: str, folder_name: str, source_folder: str, folder_created_at: float, content_fingerprint: str, traveler_path: str = '', traveler_fingerprint: str = '', traveler_include_hardware: bool | None = None, traveler_status: str = '', traveler_generated_at: str = '', processing_status: str = '未处理', outbound_status: str = '未出库', outbound_document: str = '', processed_at: str = '', outbound_at: str = '', last_error: str = '', server_scan_policy: str = '', server_scan_watch_until: str = '', server_scan_policy_updated_at: str = '', handling_mode: str = '', reference_order_ids: list[str] | None = None) -> None` — 新增或更新订单相关数据或步骤。
  - 输入：`temporary_id: str`；`folder_name: str`；`source_folder: str`；`folder_created_at: float`；`content_fingerprint: str`；`traveler_path: str = ''`；`traveler_fingerprint: str = ''`；`traveler_include_hardware: bool | None = None`；`traveler_status: str = ''`；`traveler_generated_at: str = ''`；`processing_status: str = '未处理'`；`outbound_status: str = '未出库'`；`outbound_document: str = ''`；`processed_at: str = ''`；`outbound_at: str = ''`；`last_error: str = ''`；`server_scan_policy: str = ''`；`server_scan_watch_until: str = ''`；`server_scan_policy_updated_at: str = ''`；`handling_mode: str = ''`；`reference_order_ids: list[str] | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1243 · 方法** `OrderIndexStore.ignored_aimes_keys() -> set[str]` — 忽略AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1251 · 方法** `OrderIndexStore.ignored_aimes_factories() -> list[dict]` — 忽略AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1272 · 方法** `OrderIndexStore.aimes_assignments() -> dict[str, str]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`dict[str, str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1280 · 方法** `OrderIndexStore.assigned_aimes_factories() -> list[dict]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1303 · 方法** `OrderIndexStore.replace_aimes_review_rows(issues: list[dict]) -> None` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`issues: list[dict]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`, `self.connection.executemany`；是否真实写入仍取决于分支和参数。

- **L1329 · 方法** `OrderIndexStore.aimes_review_rows() -> list[dict]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1353 · 方法** `OrderIndexStore.aimes_review_row(ignore_key: str) -> dict | None` — 封装AIMES 数据、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`ignore_key: str`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1329` `OrderIndexStore.aimes_review_rows`

- **L1359 · 方法** `OrderIndexStore.remove_aimes_review_row(ignore_key: str) -> None` — 移除AIMES 数据、行数据相关数据或步骤。
  - 输入：`ignore_key: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1365 · 方法** `OrderIndexStore.assign_aimes_factory(issue: dict, order_id: str) -> None` — 封装AIMES 数据、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`issue: dict`；`order_id: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1359` `OrderIndexStore.remove_aimes_review_row`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1390 · 方法** `OrderIndexStore.restore_aimes_assignment(ignore_key: str) -> None` — 恢复AIMES 数据相关数据或步骤。
  - 输入：`ignore_key: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1405 · 方法** `OrderIndexStore.ignore_aimes_factory(issue: dict) -> None` — 忽略AIMES 数据、工厂单相关数据或步骤。
  - 输入：`issue: dict`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1359` `OrderIndexStore.remove_aimes_review_row`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1438 · 方法** `OrderIndexStore.restore_aimes_factory(ignore_key: str) -> None` — 恢复AIMES 数据、工厂单相关数据或步骤。
  - 输入：`ignore_key: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1444 · 方法** `OrderIndexStore.upsert_order(order_id: str, order_type: str | None = None, source_folder: str = '', source_folder_mtime: float | None = None, validation_status: str | None = None, stage: str | None = None, server_seen: str = '', aimes_seen: str = '') -> None` — 新增或更新订单相关数据或步骤。
  - 输入：`order_id: str`；`order_type: str | None = None`；`source_folder: str = ''`；`source_folder_mtime: float | None = None`；`validation_status: str | None = None`；`stage: str | None = None`；`server_seen: str = ''`；`aimes_seen: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:115` `_order_type`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1472` `OrderIndexStore.set_validation`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`, `self.set_validation`；是否真实写入仍取决于分支和参数。

- **L1472 · 方法** `OrderIndexStore.set_validation(order_id: str, status: str, message: str = '') -> None` — 设置与 `set_validation` 对应的数据或步骤。
  - 输入：`order_id: str`；`status: str`；`message: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1478 · 方法** `OrderIndexStore.server_scan_policy(order_id: str) -> dict | None` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`order_id: str`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1499 · 方法** `OrderIndexStore.save_server_scan_policy(order_id: str, policy: str, aimes_fingerprint: str, watch_until: str = '', updated_at: str = '') -> None` — 保存Server 数据相关数据或步骤。
  - 输入：`order_id: str`；`policy: str`；`aimes_fingerprint: str`；`watch_until: str = ''`；`updated_at: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1526 · 方法** `OrderIndexStore.save_order_annotations(order_id: str, user_note: str, planned_days: list[dict[str, str]], actual_days: list[dict[str, str]]) -> dict` — 保存订单相关数据或步骤。
  - 输入：`order_id: str`；`user_note: str`；`planned_days: list[dict[str, str]]`；`actual_days: list[dict[str, str]]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:2205` `OrderIndexStore.summaries`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`, `set`, `self.connection.executemany`, `self.connection.commit`；是否真实写入仍取决于分支和参数。

- **L1620 · 方法** `OrderIndexStore.upsert_factory(factory_order: str, order_id: str = '', factory_name: str = '', sales_order_name: str = '', split_time: str = '', name_source: str = '', source_folder: str = '', report_state: str | None = None, ownership_status: str | None = None, has_hardware: bool | None = None, optimized: bool | None = None, outbound_status: str | None = None, outbound_document: str | None = None, outbound_mode: str | None = None, outbound_fingerprint: str | None = None, server_seen: str = '', aimes_seen: str = '') -> None` — 新增或更新工厂单相关数据或步骤。
  - 输入：`factory_order: str`；`order_id: str = ''`；`factory_name: str = ''`；`sales_order_name: str = ''`；`split_time: str = ''`；`name_source: str = ''`；`source_folder: str = ''`；`report_state: str | None = None`；`ownership_status: str | None = None`；`has_hardware: bool | None = None`；`optimized: bool | None = None`；`outbound_status: str | None = None`；`outbound_document: str | None = None`；`outbound_mode: str | None = None`；`outbound_fingerprint: str | None = None`；`server_seen: str = ''`；`aimes_seen: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1729 · 方法** `OrderIndexStore.upsert_aimes_factory(factory_order: str, order_id: str, factory_name: str, sales_order_name: str, split_time: str, seen_at: str) -> None` — 新增或更新AIMES 数据、工厂单相关数据或步骤。
  - 输入：`factory_order: str`；`order_id: str`；`factory_name: str`；`sales_order_name: str`；`split_time: str`；`seen_at: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1784 · 方法** `OrderIndexStore.mark_aimes_deleted(factory_orders: list[str], verified_at: str) -> int` — 标记AIMES 数据相关数据或步骤。
  - 输入：`factory_orders: list[str]`；`verified_at: str`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1821 · 方法** `OrderIndexStore.upsert_source_file(path: Path, source_folder: Path, kind: str, order_id: str = '', factory_order: str = '', changed_at: str, metadata: dict | None = None) -> str` — 新增或更新来源、文件相关数据或步骤。
  - 输入：`path: Path`；`source_folder: Path`；`kind: str`；`order_id: str = ''`；`factory_order: str = ''`；`changed_at: str`；`metadata: dict | None = None`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:186` `_mtime_marker`；`traveler_assistant/order_index.py:197` `_file_content_fingerprint`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1905 · 方法** `OrderIndexStore.add_change(severity: str, kind: str, message: str, order_id: str = '', factory_order: str = '', path: str = '', observed_at: str | None = None) -> None` — 新增与 `add_change` 对应的数据或步骤。
  - 输入：`severity: str`；`kind: str`；`message: str`；`order_id: str = ''`；`factory_order: str = ''`；`path: str = ''`；`observed_at: str | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1924 · 方法** `OrderIndexStore.upsert_active_issue(issue_key: str, kind: str, order_id: str = '', factory_order: str = '', path: str = '', message: str, seen_at: str | None = None) -> None` — 新增或更新待处理问题相关数据或步骤。
  - 输入：`issue_key: str`；`kind: str`；`order_id: str = ''`；`factory_order: str = ''`；`path: str = ''`；`message: str`；`seen_at: str | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1964 · 方法** `OrderIndexStore.active_issues() -> list[dict]` — 封装 `active_issues` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1990 · 方法** `OrderIndexStore.delete_stale_factory_ownership_issues(initial_date: str) -> int` — 删除工厂单相关数据或步骤。
  - 输入：`initial_date: str`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:382` `_factory_order_before_initial_date`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2017 · 方法** `OrderIndexStore.resolve_active_issue(issue_key: str, resolved_at: str | None = None) -> None` — 解析并确定待处理问题相关数据或步骤。
  - 输入：`issue_key: str`；`resolved_at: str | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2023 · 方法** `OrderIndexStore.resolve_active_issues_not_in(issue_keys: set[str], scoped_folders: set[str] | None = None) -> None` — 解析并确定与 `resolve_active_issues_not_in` 对应的数据或步骤。
  - 输入：`issue_keys: set[str]`；`scoped_folders: set[str] | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2047 · 方法** `OrderIndexStore.clear_server_folder_pending_records(folders: set[str]) -> None` — 清理Server 数据、文件夹相关数据或步骤。
  - 输入：`folders: set[str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2064 · 方法** `OrderIndexStore.current_issue(issue_key: str) -> dict | None` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`issue_key: str`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1964` `OrderIndexStore.active_issues`

- **L2067 · 方法** `OrderIndexStore.update_source_file_identity(path: Path, order_id: str = '', factory_order: str = '') -> None` — 更新来源、文件相关数据或步骤。
  - 输入：`path: Path`；`order_id: str = ''`；`factory_order: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2078 · 方法** `OrderIndexStore.record_run(started: str, finished: str, aimes_attempted: bool, aimes_succeeded: bool, aimes_count: int, server_folder_count: int, error: str = '') -> None` — 记录记录相关数据或步骤。
  - 输入：`started: str`；`finished: str`；`aimes_attempted: bool`；`aimes_succeeded: bool`；`aimes_count: int`；`server_folder_count: int`；`error: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2088 · 方法** `OrderIndexStore.commit() -> None` — 封装 `commit` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.commit`；是否真实写入仍取决于分支和参数。

- **L2091 · 方法** `OrderIndexStore.latest_sync() -> dict` — 封装 `latest_sync` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`dict`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2107 · 方法** `OrderIndexStore.has_successful_aimes_sync_on(day: str) -> bool` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`day: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2114 · 方法** `OrderIndexStore.latest_change_id() -> int` — 封装 `latest_change_id` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2117 · 方法** `OrderIndexStore.server_scan_xml_state() -> list[dict[str, object]]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[dict[str, object]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2137 · 方法** `OrderIndexStore.save_server_scan_xml_baseline(folders: Iterable[Path], entries: Iterable[dict[str, object]], observed_at: str) -> None` — 保存Server 数据相关数据或步骤。
  - 输入：`folders: Iterable[Path]`；`entries: Iterable[dict[str, object]]`；`observed_at: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2181 · 方法** `OrderIndexStore.latest_changes(limit: int = 20, after_id: int | None = None) -> list[dict]` — 封装 `latest_changes` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`limit: int = 20`；`after_id: int | None = None`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2205 · 方法** `OrderIndexStore.summaries(persist: bool = True) -> list[dict]` — 封装 `summaries` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`persist: bool = True`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`, `self.connection.commit`；是否真实写入仍取决于分支和参数。

- **L2404 · 函数** `_report_files(folder: Path) -> list[tuple[Path, str]]` — 封装 `_report_files` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[tuple[Path, str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/report_read_context.py:63` `report_paths`；`traveler_assistant/fittings.py:24` `is_fittings_report`

- **L2419 · 函数** `_is_recut_material_source(path: Path) -> bool` — 封装材料、来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2427 · 函数** `_is_recut_server_report(path: Path, source_folder: Path) -> bool` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`source_folder: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2441 · 函数** `_reconcile_authoritative_server_material_sources(store: 'OrderIndexStore', folders_by_order: dict[str, set[str]]) -> set[str]` — 对账并重算Server 数据、材料相关数据或步骤。
  - 输入：`store: 'OrderIndexStore'`；`folders_by_order: dict[str, set[str]]`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7696` `_path_in_folders`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2498 · 函数** `_hardware_report_paths(paths: Iterable[Path], source_folder: Path) -> list[Path]` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`paths: Iterable[Path]`；`source_folder: Path`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2506 · 函数** `_selected_hardware_reports(source_rows: Iterable[tuple[str, str]]) -> dict` — 选择五金相关数据或步骤。
  - 输入：`source_rows: Iterable[tuple[str, str]]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/fittings.py:54` `select_latest_fittings`

- **L2512 · 函数** `_selected_hardware_report_paths(source_rows: Iterable[tuple[str, str]]) -> set[str]` — 选择五金相关数据或步骤。
  - 输入：`source_rows: Iterable[tuple[str, str]]`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2506` `_selected_hardware_reports`

- **L2530 · 函数** `_optimization_artifact_paths(folder: Path) -> tuple[list[Path], bool]` — 封装 `_optimization_artifact_paths` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`tuple[list[Path], bool]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2566 · 函数** `_optimization_artifacts(folder: Path) -> list[Path]` — 封装 `_optimization_artifacts` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2530` `_optimization_artifact_paths`

- **L2572 · 函数** `_optimization_result_artifacts(folder: Path) -> list[Path]` — 封装结果相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2566` `_optimization_artifacts`

- **L2577 · 函数** `_optimization_result_artifacts_checked(folder: Path) -> tuple[list[Path], bool]` — 封装结果相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`tuple[list[Path], bool]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2530` `_optimization_artifact_paths`

- **L2586 · 函数** `_server_optimization_monitor_files(folder: Path) -> list[tuple[Path, str]]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[tuple[Path, str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2566` `_optimization_artifacts`

- **L2599 · 函数** `_optimization_factory_orders(path: Path) -> set[str]` — 封装工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2610 · 函数** `_file_timestamp(value: float) -> str` — 封装文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: float`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2614 · 函数** `_canonical_source_folder(source_root: Path, folder_name: str) -> Path` — 封装来源、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`source_root: Path`；`folder_name: str`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2632 · 函数** `_record_server_baseline(store: OrderIndexStore, folder: Path, order_id: str = '') -> None` — 记录记录、Server 数据相关数据或步骤。
  - 输入：`store: OrderIndexStore`；`folder: Path`；`order_id: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1821` `OrderIndexStore.upsert_source_file`；`traveler_assistant/order_index.py:2404` `_report_files`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_source_file`；是否真实写入仍取决于分支和参数。

- **L2652 · 函数** `record_standard_outbound_baseline(config: Config, order_id: str) -> bool` — 记录记录、出库相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:2632` `_record_server_baseline`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `_record_server_baseline`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2672 · 函数** `_record_generated_material_baseline(store: OrderIndexStore, folder: Path, materials_path: Path, order_id: str = '') -> None` — 记录记录、材料相关数据或步骤。
  - 输入：`store: OrderIndexStore`；`folder: Path`；`materials_path: Path`；`order_id: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1821` `OrderIndexStore.upsert_source_file`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_source_file`；是否真实写入仍取决于分支和参数。

- **L2707 · 函数** `_direct_report_files(folder: Path) -> list[tuple[Path, str]]` — 封装 `_direct_report_files` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[tuple[Path, str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2404` `_report_files`

- **L2712 · 函数** `_merge_candidate(candidates: dict[str, dict], factory_order: str, name: str = '', source: str, order_id: str = '', sales_order_name: str = '', split_time: str = '', folder: str = '', has_hardware: bool = False, derive_order_from_name: bool = True, optimized: bool = False) -> None` — 封装 `_merge_candidate` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`candidates: dict[str, dict]`；`factory_order: str`；`name: str = ''`；`source: str`；`order_id: str = ''`；`sales_order_name: str = ''`；`split_time: str = ''`；`folder: str = ''`；`has_hardware: bool = False`；`derive_order_from_name: bool = True`；`optimized: bool = False`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:110` `_order_id_from_factory_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2744 · 函数** `_effective_factory_candidate(factory_order: str, candidate: dict) -> dict` — 封装工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`factory_order: str`；`candidate: dict`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2787 · 函数** `_merge_cached_server_candidate(store: OrderIndexStore, candidates: dict[str, dict], path: Path, folder: Path, folder_order_ids: list[str], manual_folder: bool) -> bool` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`candidates: dict[str, dict]`；`path: Path`；`folder: Path`；`folder_order_ids: list[str]`；`manual_folder: bool`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2712` `_merge_candidate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2857 · 函数** `_confirmed_material_folders(store: OrderIndexStore, folders: list[Path]) -> list[Path]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`folders: list[Path]`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2873 · 函数** `_refresh_cached_optimization_artifacts(store: OrderIndexStore, validation_rows: list[tuple[str, str]], timing_sink: list[dict[str, object]] | None = None) -> int` — 刷新与 `_refresh_cached_optimization_artifacts` 对应的数据或步骤。
  - 输入：`store: OrderIndexStore`；`validation_rows: list[tuple[str, str]]`；`timing_sink: list[dict[str, object]] | None = None`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:2577` `_optimization_result_artifacts_checked`；`traveler_assistant/order_index.py:2599` `_optimization_factory_orders`；`traveler_assistant/order_index.py:2610` `_file_timestamp`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L3050 · 函数** `_load_outbound_records(config: Config) -> list[dict]` — 读取出库相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L3105 · 函数** `_outbound_key(value: object) -> str` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: object`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3109 · 函数** `_outbound_exact_aliases(factory: dict) -> set[str]` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`factory: dict`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:3105` `_outbound_key`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_outbound_key`；是否真实写入仍取决于分支和参数。

- **L3117 · 函数** `_outbound_record_matches_factory(record: dict, factory: dict, allow_order_alias: bool) -> bool` — 封装出库、记录、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`record: dict`；`factory: dict`；`allow_order_alias: bool`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:3105` `_outbound_key`；`traveler_assistant/order_index.py:3109` `_outbound_exact_aliases`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_outbound_key`, `_outbound_exact_aliases`；是否真实写入仍取决于分支和参数。

- **L3133 · 函数** `_has_factory_hardware_outbound_record(factory: dict, records: Iterable[dict]) -> bool` — 封装工厂单、五金、出库、记录相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`factory: dict`；`records: Iterable[dict]`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:3117` `_outbound_record_matches_factory`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_outbound_record_matches_factory`；是否真实写入仍取决于分支和参数。

- **L3146 · 函数** `_factory_outbound_metadata(config: Config, factory: dict) -> tuple[str, str]` — 封装工厂单、出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`factory: dict`
  - 返回：`tuple[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L3168 · 函数** `_refresh_outbound_status(config: Config, factory: dict, records: list[dict] | None = None, factory_group: list[dict] | None = None) -> tuple[str, str]` — 刷新出库、状态相关数据或步骤。
  - 输入：`config: Config`；`factory: dict`；`records: list[dict] | None = None`；`factory_group: list[dict] | None = None`
  - 返回：`tuple[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:3050` `_load_outbound_records`；`traveler_assistant/order_index.py:3146` `_factory_outbound_metadata`；`traveler_assistant/order_index.py:3109` `_outbound_exact_aliases`；`traveler_assistant/order_index.py:3105` `_outbound_key`；`traveler_assistant/inventory.py:430` `database_outbound_fingerprint`；`traveler_assistant/inventory.py:634` `database_document_items`；`traveler_assistant/order_index.py:165` `_is_traveler_file`；`traveler_assistant/inventory.py:1446` `parse_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_load_outbound_records`, `_factory_outbound_metadata`, `_outbound_exact_aliases`, `_outbound_key`, `database_outbound_fingerprint`；是否真实写入仍取决于分支和参数。

- **L3318 · 函数** `assert_factory_orders_outbound_allowed(config: Config, order_id: str, factory_orders: Iterable[str], changed_factory_orders: Iterable[str] | None = None) -> None` — 强制校验工厂单、出库相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`factory_orders: Iterable[str]`；`changed_factory_orders: Iterable[str] | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:3393` `reconcile_outbound_statuses`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `reconcile_outbound_statuses`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3393 · 函数** `reconcile_outbound_statuses(config: Config, store: OrderIndexStore | None = None) -> int` — 依据工厂单范围与出库证据重新计算订单/工厂单出库状态。
  - 输入：`config: Config`；`store: OrderIndexStore | None = None`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:3050` `_load_outbound_records`；`traveler_assistant/order_index.py:3105` `_outbound_key`；`traveler_assistant/hardware_facts.py:124` `audit_factory_hardware`；`traveler_assistant/order_index.py:3168` `_refresh_outbound_status`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/hardware_facts.py:182` `audit_hardware_integrity`；`traveler_assistant/order_index.py:3901` `_resolve_fully_shipped_server_issues`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_load_outbound_records`, `store.connection.execute`, `_outbound_key`, `_refresh_outbound_status`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3527 · 函数** `_orders_requiring_server_scan(config: Config, store: OrderIndexStore, aimes_rows: list[dict] | None = None) -> set[str]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`aimes_rows: list[dict] | None = None`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:3560` `_aimes_factory_records`；`traveler_assistant/order_index.py:3050` `_load_outbound_records`；`traveler_assistant/order_index.py:3168` `_refresh_outbound_status`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_load_outbound_records`, `set`, `_refresh_outbound_status`；是否真实写入仍取决于分支和参数。

- **L3560 · 函数** `_aimes_factory_records(store: OrderIndexStore, aimes_rows: list[dict] | None = None) -> dict[str, dict]` — 封装AIMES 数据、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`aimes_rows: list[dict] | None = None`
  - 返回：`dict[str, dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L3607 · 函数** `_server_order_scan_allowed(config: Config, store: OrderIndexStore, order_id: str, folder: Path, requires_scan: set[str], now: str) -> bool` — 封装Server 数据、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`order_id: str`；`folder: Path`；`requires_scan: set[str]`；`now: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1478` `OrderIndexStore.server_scan_policy`；`traveler_assistant/order_index.py:1444` `OrderIndexStore.upsert_order`；`traveler_assistant/order_index.py:115` `_order_type`；`traveler_assistant/order_index.py:409` `_aimes_order_fingerprint`；`traveler_assistant/order_index.py:440` `_order_is_before_initial_date`；`traveler_assistant/order_index.py:468` `_order_has_active_aimes_mapping`；`traveler_assistant/order_index.py:482` `_order_shipped_watch_until`；`traveler_assistant/order_index.py:1499` `OrderIndexStore.save_server_scan_policy`；`traveler_assistant/order_index.py:519` `_datetime_timestamp`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.save_server_scan_policy`；是否真实写入仍取决于分支和参数。

- **L3684 · 函数** `_server_folder_scan_allowed(config: Config, store: OrderIndexStore, folder: Path, aimes_rows: list[dict] | None = None) -> bool` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`folder: Path`；`aimes_rows: list[dict] | None = None`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:4399` `_server_folder_handling_mode`；`traveler_assistant/order_index.py:4426` `_temporary_folder_is_candidate`；`traveler_assistant/order_index.py:3839` `_server_folder_order_ids`；`traveler_assistant/order_index.py:3527` `_orders_requiring_server_scan`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:3607` `_server_order_scan_allowed`

- **L3711 · 函数** `_finalize_server_scan_policies(config: Config, store: OrderIndexStore, folders: Iterable[Path], scanned_at: str) -> None` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`folders: Iterable[Path]`；`scanned_at: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:3527` `_orders_requiring_server_scan`；`traveler_assistant/order_index.py:4399` `_server_folder_handling_mode`；`traveler_assistant/order_index.py:3839` `_server_folder_order_ids`；`traveler_assistant/order_index.py:1478` `OrderIndexStore.server_scan_policy`；`traveler_assistant/order_index.py:409` `_aimes_order_fingerprint`；`traveler_assistant/order_index.py:440` `_order_is_before_initial_date`；`traveler_assistant/order_index.py:468` `_order_has_active_aimes_mapping`；`traveler_assistant/order_index.py:482` `_order_shipped_watch_until`；`traveler_assistant/order_index.py:1499` `OrderIndexStore.save_server_scan_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.save_server_scan_policy`；是否真实写入仍取决于分支和参数。

- **L3754 · 函数** `_mark_initial_orders_shipped(config: Config, store: OrderIndexStore) -> int` — 标记与 `_mark_initial_orders_shipped` 对应的数据或步骤。
  - 输入：`config: Config`；`store: OrderIndexStore`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:143` `_available_server_roots`；`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:115` `_order_type`；`traveler_assistant/order_index.py:147` `_server_root_order_type`；`traveler_assistant/order_index.py:440` `_order_is_before_initial_date`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1444` `OrderIndexStore.upsert_order`；`traveler_assistant/order_index.py:1472` `OrderIndexStore.set_validation`；`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`；`traveler_assistant/order_index.py:1499` `OrderIndexStore.save_server_scan_policy`；`traveler_assistant/order_index.py:409` `_aimes_order_fingerprint`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.connection.execute`, `store.set_validation`, `store.save_server_scan_policy`, `store.commit`；是否真实写入仍取决于分支和参数。

- **L3839 · 函数** `_server_folder_order_ids(folder: Path) -> set[str]` — 封装Server 数据、文件夹、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`；`traveler_assistant/order_index.py:4562` `_folder_order_ids`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L3848 · 函数** `_server_folder_is_fully_shipped(config: Config, store: OrderIndexStore, folder: Path, aimes_rows: list[dict] | None = None) -> bool` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`folder: Path`；`aimes_rows: list[dict] | None = None`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:4399` `_server_folder_handling_mode`；`traveler_assistant/order_index.py:3839` `_server_folder_order_ids`；`traveler_assistant/order_index.py:3560` `_aimes_factory_records`；`traveler_assistant/order_index.py:1478` `OrderIndexStore.server_scan_policy`；`traveler_assistant/order_index.py:3527` `_orders_requiring_server_scan`

- **L3886 · 函数** `_server_folder_for_issue(issue_path: str) -> Path | None` — 封装Server 数据、文件夹、待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`issue_path: str`
  - 返回：`Path | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`

- **L3901 · 函数** `_resolve_fully_shipped_server_issues(config: Config, store: OrderIndexStore) -> int` — 解析并确定Server 数据相关数据或步骤。
  - 输入：`config: Config`；`store: OrderIndexStore`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1964` `OrderIndexStore.active_issues`；`traveler_assistant/order_index.py:3886` `_server_folder_for_issue`；`traveler_assistant/order_index.py:3848` `_server_folder_is_fully_shipped`；`traveler_assistant/order_index.py:2017` `OrderIndexStore.resolve_active_issue`

- **L3938 · 函数** `_resolve_stale_produced_material_issues(store: OrderIndexStore) -> int` — 解析并确定材料相关数据或步骤。
  - 输入：`store: OrderIndexStore`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1964` `OrderIndexStore.active_issues`；`traveler_assistant/order_index.py:3886` `_server_folder_for_issue`；`traveler_assistant/order_index.py:3839` `_server_folder_order_ids`；`traveler_assistant/order_index.py:519` `_datetime_timestamp`；`traveler_assistant/order_index.py:2017` `OrderIndexStore.resolve_active_issue`；`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`；`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `set`；是否真实写入仍取决于分支和参数。

- **L4042 · 函数** `_aimes_row_signature(rows: list[dict]) -> list[tuple[str, str, str, str]]` — 封装AIMES 数据、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`rows: list[dict]`
  - 返回：`list[tuple[str, str, str, str]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4054 · 函数** `_persist_valid_aimes_mapping(config: Config, rows: list[dict], warnings: list[dict], cached_rows: list[dict] | None = None) -> None` — 封装AIMES 数据、映射相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`rows: list[dict]`；`warnings: list[dict]`；`cached_rows: list[dict] | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:273` `load_aimes_order_cache`；`traveler_assistant/core.py:289` `save_aimes_order_cache`；`traveler_assistant/core.py:262` `load_factory_name_cache`；`traveler_assistant/core.py:269` `save_factory_name_cache`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save_aimes_order_cache`, `names.update`, `save_factory_name_cache`；是否真实写入仍取决于分支和参数。

- **L4100 · 函数** `_active_aimes_factory_orders(store: OrderIndexStore) -> list[str]` — 封装AIMES 数据、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L4130 · 函数** `_verify_missing_aimes_factories(config: Config, store: OrderIndexStore, fetched_rows: list[dict], verified_at: str, verification_result: dict | None = None) -> tuple[int, str]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`fetched_rows: list[dict]`；`verified_at: str`；`verification_result: dict | None = None`
  - 返回：`tuple[int, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:4100` `_active_aimes_factory_orders`；`traveler_assistant/core.py:520` `verify_aimes_factory_orders`；`traveler_assistant/order_index.py:1784` `OrderIndexStore.mark_aimes_deleted`

- **L4167 · 函数** `sync_aimes_index(config: Config, force: bool = False, if_needed: bool = False) -> dict` — 刷新 AIMES 工厂单身份事实并更新订单索引；不隐式扫描 Server。
  - 输入：`config: Config`；`force: bool = False`；`if_needed: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:3393` `reconcile_outbound_statuses`；`traveler_assistant/core.py:273` `load_aimes_order_cache`；`traveler_assistant/order_index.py:590` `_partition_aimes_rows`；`traveler_assistant/order_index.py:1243` `OrderIndexStore.ignored_aimes_keys`；`traveler_assistant/order_index.py:1272` `OrderIndexStore.aimes_assignments`；`traveler_assistant/order_index.py:1329` `OrderIndexStore.aimes_review_rows`；`traveler_assistant/order_index.py:2107` `OrderIndexStore.has_successful_aimes_sync_on`；`traveler_assistant/order_index.py:2205` `OrderIndexStore.summaries`；`traveler_assistant/order_index.py:1251` `OrderIndexStore.ignored_aimes_factories`；`traveler_assistant/order_index.py:1280` `OrderIndexStore.assigned_aimes_factories`；另有 18 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `reconcile_outbound_statuses`, `store.close`, `store.record_run`, `store.commit`, `store.upsert_order`, `store.upsert_aimes_factory`, `store.replace_aimes_review_rows`；是否真实写入仍取决于分支和参数。

- **L4394 · 函数** `_folder_name_order_ids(folder: Path) -> list[str]` — 封装文件夹、名称、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L4399 · 函数** `_server_folder_handling_mode(store: OrderIndexStore, folder: Path, aimes_rows: list[dict] | None = None) -> str` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`folder: Path`；`aimes_rows: list[dict] | None = None`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:4394` `_folder_name_order_ids`；`traveler_assistant/order_index.py:3560` `_aimes_factory_records`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L4426 · 函数** `_temporary_folder_is_candidate(config: Config, store: OrderIndexStore, folder: Path) -> bool` — 封装文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`folder: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:170` `_folder_created_at`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:4659` `_temporary_xml_baseline_matches`；`traveler_assistant/order_index.py:340` `_server_scan_baseline`；`traveler_assistant/order_index.py:2586` `_server_optimization_monitor_files`；`traveler_assistant/order_index.py:1157` `OrderIndexStore.upsert_temporary_order`；`traveler_assistant/order_index.py:4569` `_temporary_order_id`；`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.upsert_temporary_order`；是否真实写入仍取决于分支和参数。

- **L4528 · 函数** `_temporary_folders_before_server_baseline(config: Config, root: Path) -> set[str]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`root: Path`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:340` `_server_scan_baseline`；`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`；`traveler_assistant/order_index.py:170` `_folder_created_at`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L4547 · 函数** `_clear_stale_server_pending_state(config: Config, store: OrderIndexStore) -> Path | None` — 清理Server 数据相关数据或步骤。
  - 输入：`config: Config`；`store: OrderIndexStore`
  - 返回：`Path | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:143` `_available_server_roots`；`traveler_assistant/order_index.py:4528` `_temporary_folders_before_server_baseline`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:2047` `OrderIndexStore.clear_server_folder_pending_records`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `stale_folders.update`, `store.commit`；是否真实写入仍取决于分支和参数。

- **L4562 · 函数** `_folder_order_ids(folder: Path) -> list[str]` — 封装文件夹、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:141` `related_order_ids`

- **L4569 · 函数** `_temporary_order_id(folder: Path) -> str` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:170` `_folder_created_at`

- **L4576 · 函数** `_reconcile_temporary_order_projections(store: OrderIndexStore) -> int` — 对账并重算订单相关数据或步骤。
  - 输入：`store: OrderIndexStore`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:115` `_order_type`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`；是否真实写入仍取决于分支和参数。

- **L4639 · 函数** `_temporary_folder_fingerprint(folder: Path) -> str` — 封装文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.open`, `digest.update`；是否真实写入仍取决于分支和参数。

- **L4659 · 函数** `_temporary_xml_baseline_matches(store: OrderIndexStore, folder: Path) -> bool` — 封装 `_temporary_xml_baseline_matches` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`folder: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5262` `_server_scan_xml_entries`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L4676 · 函数** `_temporary_aimes_match(store: OrderIndexStore, folder: Path) -> dict | None` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`folder: Path`
  - 返回：`dict | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L4707 · 函数** `_is_mixed_order_folder(folder: Path) -> bool` — 封装订单、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`

- **L4723 · 函数** `_temporary_folder_layout_error(folder: Path) -> str` — 封装文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2404` `_report_files`

- **L4742 · 函数** `record_temporary_outbound(config: Config, traveler_path: Path, outbound: dict) -> None` — 记录记录、出库相关数据或步骤。
  - 输入：`config: Config`；`traveler_path: Path`；`outbound: dict`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`；`traveler_assistant/order_index.py:2614` `_canonical_source_folder`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:2586` `_server_optimization_monitor_files`；`traveler_assistant/order_index.py:1157` `OrderIndexStore.upsert_temporary_order`；`traveler_assistant/order_index.py:4569` `_temporary_order_id`；`traveler_assistant/order_index.py:170` `_folder_created_at`；`traveler_assistant/order_index.py:4639` `_temporary_folder_fingerprint`；`traveler_assistant/order_index.py:2632` `_record_server_baseline`；另有 5 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_temporary_order`, `_record_server_baseline`, `store.save_server_scan_xml_baseline`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4794 · 函数** `mark_temporary_folder_manual(config: Config, folder: Path, reference_order_ids: list[str] | None = None, outbound_document: str = '') -> dict` — 登记临时 Server 文件夹已人工出库，并建立三天 XML 观察期。
  - 输入：`config: Config`；`folder: Path`；`reference_order_ids: list[str] | None = None`；`outbound_document: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:143` `_available_server_roots`；`traveler_assistant/order_workflow.py:237` `resolve_source_root`；`traveler_assistant/order_index.py:6077` `_path_is_within`；`traveler_assistant/order_index.py:4394` `_folder_name_order_ids`；`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:2586` `_server_optimization_monitor_files`；`traveler_assistant/order_index.py:4639` `_temporary_folder_fingerprint`；`traveler_assistant/order_index.py:5262` `_server_scan_xml_entries`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:4399` `_server_folder_handling_mode`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；另有 11 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.upsert_temporary_order`, `_record_server_baseline`, `store.save_server_scan_xml_baseline`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L4893 · 函数** `_temporary_order_ids(folder: Path) -> list[str]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:4562` `_folder_order_ids`

- **L4901 · 函数** `_process_temporary_folder(config: Config, folder: Path, store: OrderIndexStore, include_hardware: bool = True) -> dict` — 处理文件夹相关数据或步骤。
  - 输入：`config: Config`；`folder: Path`；`store: OrderIndexStore`；`include_hardware: bool = True`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:4639` `_temporary_folder_fingerprint`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:2586` `_server_optimization_monitor_files`；`traveler_assistant/order_index.py:4659` `_temporary_xml_baseline_matches`；`traveler_assistant/order_index.py:4569` `_temporary_order_id`；`traveler_assistant/order_index.py:1157` `OrderIndexStore.upsert_temporary_order`；`traveler_assistant/order_index.py:170` `_folder_created_at`；`traveler_assistant/order_index.py:4723` `_temporary_folder_layout_error`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:4893` `_temporary_order_ids`；`traveler_assistant/order_workflow.py:1159` `generate_material_from_reports`；`traveler_assistant/order_index.py:4676` `_temporary_aimes_match`；另有 6 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_temporary_order`, `update_order_traveler`, `run_jdy`；是否真实写入仍取决于分支和参数。

- **L5085 · 函数** `_server_snapshot_folder(folder: Path | tuple[Path, bool]) -> tuple[dict[str, dict], dict[str, object]]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path | tuple[Path, bool]`
  - 返回：`tuple[dict[str, dict], dict[str, object]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`；`traveler_assistant/order_index.py:4562` `_folder_order_ids`；`traveler_assistant/order_index.py:2586` `_server_optimization_monitor_files`；`traveler_assistant/order_index.py:2404` `_report_files`；`traveler_assistant/order_index.py:186` `_mtime_marker`；`traveler_assistant/order_index.py:176` `_path_created_at`

- **L5188 · 函数** `_server_snapshot(config: Config, store: OrderIndexStore, timing_sink: list[dict[str, object]] | None = None) -> tuple[Path, dict[str, dict]]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`store: OrderIndexStore`；`timing_sink: list[dict[str, object]] | None = None`
  - 返回：`tuple[Path, dict[str, dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:3754` `_mark_initial_orders_shipped`；`traveler_assistant/order_index.py:143` `_available_server_roots`；`traveler_assistant/order_workflow.py:237` `resolve_source_root`；`traveler_assistant/order_index.py:4399` `_server_folder_handling_mode`；`traveler_assistant/order_index.py:4426` `_temporary_folder_is_candidate`；`traveler_assistant/order_index.py:115` `_order_type`；`traveler_assistant/order_index.py:147` `_server_root_order_type`；`traveler_assistant/order_index.py:3684` `_server_folder_scan_allowed`；`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:4394` `_folder_name_order_ids`；`traveler_assistant/order_index.py:1157` `OrderIndexStore.upsert_temporary_order`；另有 2 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_temporary_order`, `snapshot.update`；是否真实写入仍取决于分支和参数。

- **L5262 · 函数** `_server_scan_xml_entries(folders: Iterable[Path]) -> list[dict[str, object]]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folders: Iterable[Path]`
  - 返回：`list[dict[str, object]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5085` `_server_snapshot_folder`

- **L5275 · 函数** `_server_scan_snapshot_path(config: Config) -> Path` — 封装Server 数据、路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5279 · 函数** `_write_server_scan_snapshot(config: Config, root: Path, roots: list[Path], scanned_at: str, entries: dict[str, dict]) -> Path` — 写入Server 数据相关数据或步骤。
  - 输入：`config: Config`；`root: Path`；`roots: list[Path]`；`scanned_at: str`；`entries: dict[str, dict]`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5275` `_server_scan_snapshot_path`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `draft.write_text`, `os.replace`；是否真实写入仍取决于分支和参数。

- **L5302 · 函数** `_load_server_scan_snapshot(config: Config, snapshot_path: Path | None) -> tuple[Path, list[Path], dict[str, dict]] | None` — 读取Server 数据相关数据或步骤。
  - 输入：`config: Config`；`snapshot_path: Path | None`
  - 返回：`tuple[Path, list[Path], dict[str, dict]] | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:143` `_available_server_roots`

- **L5336 · 函数** `_server_change_message(change_type: str, item: dict, path: str) -> str` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`change_type: str`；`item: dict`；`path: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5489` `_source_file_data_label`

- **L5363 · 函数** `_server_folder_rename_pairs(previous: dict[str, dict], current: dict[str, dict]) -> list[tuple[str, str]]` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`previous: dict[str, dict]`；`current: dict[str, dict]`
  - 返回：`list[tuple[str, str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5370` `_server_folder_rename_pairs.folders`；`traveler_assistant/order_index.py:5403` `_server_folder_rename_pairs.content_matches`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L5370 · 方法** `_server_folder_rename_pairs.folders(entries: dict[str, dict], previous_entries: bool) -> dict[str, set[str]]` — 封装 `folders` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`entries: dict[str, dict]`；`previous_entries: bool`
  - 返回：`dict[str, set[str]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L5403 · 方法** `_server_folder_rename_pairs.content_matches(old_folder: str, new_folder: str) -> bool` — 封装 `content_matches` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`old_folder: str`；`new_folder: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:197` `_file_content_fingerprint`

- **L5432 · 函数** `_rebase_server_folder_paths(store: 'OrderIndexStore', pairs: list[tuple[str, str]]) -> None` — 封装Server 数据、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: 'OrderIndexStore'`；`pairs: list[tuple[str, str]]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L5469 · 函数** `_server_data_change_message(change_type: str, order_ids: list[str], factory_order: str, data_label: str, path: str = '') -> str` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`change_type: str`；`order_ids: list[str]`；`factory_order: str`；`data_label: str`；`path: str = ''`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5489` `_source_file_data_label`

- **L5489 · 函数** `_source_file_data_label(kind: str) -> str` — 封装来源、文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`kind: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5499 · 函数** `_summarize_server_read_items(items: list[tuple[str, str, str]]) -> str` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: list[tuple[str, str, str]]`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5545 · 函数** `_trace_rows(rows: list[dict]) -> tuple[int, int]` — 封装 `_trace_rows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`rows: list[dict]`
  - 返回：`tuple[int, int]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5562 · 函数** `_flat_aimes_stage_durations(values: object) -> list[dict[str, object]]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`values: object`
  - 返回：`list[dict[str, object]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5575 · 函数** `_complete_aimes_stage_durations(values: object, total_seconds: float) -> list[dict[str, object]]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`values: object`；`total_seconds: float`
  - 返回：`list[dict[str, object]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5562` `_flat_aimes_stage_durations`

- **L5595 · 函数** `_aimes_trace(config: Config, source: str, rows: list[dict], wrote_cache: bool, error: str = '', warnings: list[dict] | None = None, elapsed_seconds: float | None = None, stage_durations: list[dict] | None = None) -> list[str]` — 封装AIMES 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`source: str`；`rows: list[dict]`；`wrote_cache: bool`；`error: str = ''`；`warnings: list[dict] | None = None`；`elapsed_seconds: float | None = None`；`stage_durations: list[dict] | None = None`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:5545` `_trace_rows`

- **L5647 · 函数** `_server_scan_trace(stats: dict[str, int | float], roots: list[str] | None = None, folder_timings: list[dict[str, object]] | None = None) -> list[str]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`stats: dict[str, int | float]`；`roots: list[str] | None = None`；`folder_timings: list[dict[str, object]] | None = None`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L5692 · 函数** `scan_server_changes(config: Config) -> dict` — 扫描候选 Server 文件夹和业务文件变化，返回待确认项与分阶段耗时。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:4547` `_clear_stale_server_pending_state`；`traveler_assistant/order_index.py:5188` `_server_snapshot`；`traveler_assistant/order_index.py:3901` `_resolve_fully_shipped_server_issues`；`traveler_assistant/order_index.py:3938` `_resolve_stale_produced_material_issues`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:143` `_available_server_roots`；`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:1126` `OrderIndexStore.temporary_order`；`traveler_assistant/order_index.py:2117` `OrderIndexStore.server_scan_xml_state`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`；另有 13 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.commit`, `store.connection.execute`, `store.upsert_active_issue`, `store.close`, `_write_server_scan_snapshot`；是否真实写入仍取决于分支和参数。

- **L6077 · 函数** `_path_is_within(path: Path, root: Path) -> bool` — 封装路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`root: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L6085 · 函数** `_server_folders_for_sync(config: Config, selected_folder: Path | None, selected_folders: list[Path] | None = None, store: OrderIndexStore | None = None, aimes_rows: list[dict] | None = None) -> tuple[Path, list[Path]]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`selected_folder: Path | None`；`selected_folders: list[Path] | None = None`；`store: OrderIndexStore | None = None`；`aimes_rows: list[dict] | None = None`
  - 返回：`tuple[Path, list[Path]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:143` `_available_server_roots`；`traveler_assistant/order_workflow.py:237` `resolve_source_root`；`traveler_assistant/order_index.py:6099` `_server_folders_for_sync.containing_root`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:160` `_is_standard_order_folder`；`traveler_assistant/order_index.py:2404` `_report_files`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:115` `_order_type`；`traveler_assistant/order_index.py:147` `_server_root_order_type`；`traveler_assistant/order_index.py:3684` `_server_folder_scan_allowed`；`traveler_assistant/order_index.py:4707` `_is_mixed_order_folder`；`traveler_assistant/order_index.py:4426` `_temporary_folder_is_candidate`；另有 2 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`；是否真实写入仍取决于分支和参数。

- **L6099 · 方法** `_server_folders_for_sync.containing_root(candidate: Path) -> Path | None` — 封装 `containing_root` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`candidate: Path`
  - 返回：`Path | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:6077` `_path_is_within`

- **L6172 · 函数** `_clear_stale_mapping_validation_status(store: OrderIndexStore, order_ids: set[str], current_issue_keys: set[str], seen_at: str) -> int` — 清理映射、状态相关数据或步骤。
  - 输入：`store: OrderIndexStore`；`order_ids: set[str]`；`current_issue_keys: set[str]`；`seen_at: str`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1472` `OrderIndexStore.set_validation`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.set_validation`；是否真实写入仍取决于分支和参数。

- **L6198 · 函数** `_exact_resolve_unowned_factories(config: Config, candidates: dict[str, dict]) -> str` — 封装 `_exact_resolve_unowned_factories` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`candidates: dict[str, dict]`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:467` `lookup_aimes_names`；`traveler_assistant/order_index.py:2712` `_merge_candidate`

- **L6233 · 函数** `_merge_database_factory_candidates(store: OrderIndexStore, candidates: dict[str, dict]) -> set[str]` — 封装数据库、工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`candidates: dict[str, dict]`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2712` `_merge_candidate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L6273 · 函数** `_preview_fittings_groups(path: Path, cache: dict | None = None) -> list` — 预览预览相关数据或步骤。
  - 输入：`path: Path`；`cache: dict | None = None`
  - 返回：`list`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:658` `parse_fittings_groups`

- **L6288 · 函数** `sync_order_index(config: Config, refresh_aimes: bool = False, aimes_if_needed: bool = False, selected_folder: Path | None = None, selected_folders: list[Path] | None = None, process_temporary: bool = False, include_hardware: bool = True, full_refresh: bool = False, validate_selected_orders: bool = True, refresh_outbound_statuses: bool = True, reconcile_outbound: bool = True, server_snapshot_path: Path | None = None, fittings_cache: dict | None = None) -> dict` — 把 AIMES、Server 和本地事实同步为可供看板读取的订单索引。
  - 输入：`config: Config`；`refresh_aimes: bool = False`；`aimes_if_needed: bool = False`；`selected_folder: Path | None = None`；`selected_folders: list[Path] | None = None`；`process_temporary: bool = False`；`include_hardware: bool = True`；`full_refresh: bool = False`；`validate_selected_orders: bool = True`；`refresh_outbound_statuses: bool = True`；`reconcile_outbound: bool = True`；`server_snapshot_path: Path | None = None`；`fittings_cache: dict | None = None`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:3754` `_mark_initial_orders_shipped`；`traveler_assistant/order_index.py:4576` `_reconcile_temporary_order_projections`；`traveler_assistant/order_index.py:3393` `reconcile_outbound_statuses`；`traveler_assistant/order_index.py:4547` `_clear_stale_server_pending_state`；`traveler_assistant/order_index.py:1990` `OrderIndexStore.delete_stale_factory_ownership_issues`；`traveler_assistant/order_index.py:2114` `OrderIndexStore.latest_change_id`；`traveler_assistant/core.py:273` `load_aimes_order_cache`；`traveler_assistant/order_index.py:590` `_partition_aimes_rows`；`traveler_assistant/order_index.py:1243` `OrderIndexStore.ignored_aimes_keys`；另有 103 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `reconcile_outbound_statuses`, `store.delete_stale_factory_ownership_issues`, `store.replace_aimes_review_rows`, `store.upsert_order`, `set`, `store.upsert_temporary_order`, `store.upsert_active_issue`, `server_order_ids.update`, `store.upsert_source_file`；是否真实写入仍取决于分支和参数。

- **L6330 · 方法** `sync_order_index.finish_phase(name: str) -> None` — 结束并收口与 `finish_phase` 对应的数据或步骤。
  - 输入：`name: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7626 · 函数** `process_server_folder(config: Config, folder: Path, include_hardware: bool = True, process_temporary: bool = False) -> dict` — 处理Server 数据、文件夹相关数据或步骤。
  - 输入：`config: Config`；`folder: Path`；`include_hardware: bool = True`；`process_temporary: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:6085` `_server_folders_for_sync`；`traveler_assistant/order_index.py:6288` `sync_order_index`

- **L7646 · 函数** `_server_preview_directory(config: Config) -> Path` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `directory.mkdir`；是否真实写入仍取决于分支和参数。

- **L7652 · 函数** `_server_preview_path(config: Config, token: str) -> Path` — 封装Server 数据、预览、路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`token: str`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7646` `_server_preview_directory`

- **L7662 · 函数** `_clone_workflow_database(config: Config, destination: Path) -> None` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`destination: Path`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `destination.parent.mkdir`, `target.close`, `source.close`；是否真实写入仍取决于分支和参数。

- **L7678 · 函数** `_preview_config(config: Config, state_dir: Path) -> Config` — 预览预览相关数据或步骤。
  - 输入：`config: Config`；`state_dir: Path`
  - 返回：`Config`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:125` `Config`

- **L7696 · 函数** `_path_in_folders(path: str, folders: list[str]) -> bool` — 封装路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: str`；`folders: list[str]`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7708 · 函数** `_server_material_allocation_rows(store: OrderIndexStore, source_path: str, material_key: str) -> list[dict]` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`source_path: str`；`material_key: str`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L7731 · 函数** `_server_material_preview_row(store: OrderIndexStore, row: dict) -> dict` — 封装Server 数据、材料、预览、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`row: dict`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:127` `server_material_identity_key`；`traveler_assistant/order_index.py:7708` `_server_material_allocation_rows`

- **L7757 · 函数** `_server_material_source_rows(store: OrderIndexStore | sqlite3.Connection, folder_paths: list[str]) -> list[dict]` — 封装Server 数据、材料、来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore | sqlite3.Connection`；`folder_paths: list[str]`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7696` `_path_in_folders`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L7787 · 函数** `_server_material_sort_key(item: dict) -> tuple` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`item: dict`
  - 返回：`tuple`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7802 · 函数** `_server_change_key(*values) -> tuple[str, ...]` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`*values`
  - 返回：`tuple[str, ...]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7806 · 函数** `_sqlite_table_exists(connection: sqlite3.Connection, table_name: str) -> bool` — 封装 `_sqlite_table_exists` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`table_name: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L7813 · 函数** `_server_material_change_rows(current: sqlite3.Connection, preview: sqlite3.Connection, order_id: str, folder_paths: list[str]) -> list[dict]` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`current: sqlite3.Connection`；`preview: sqlite3.Connection`；`order_id: str`；`folder_paths: list[str]`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7757` `_server_material_source_rows`；`traveler_assistant/order_index.py:7802` `_server_change_key`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L7820 · 方法** `_server_material_change_rows.grouped(connection: sqlite3.Connection, source_paths: list[str]) -> dict[tuple[str, ...], dict]` — 封装 `grouped` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`source_paths: list[str]`
  - 返回：`dict[tuple[str, ...], dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7806` `_sqlite_table_exists`；`traveler_assistant/order_index.py:7802` `_server_change_key`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L7894 · 函数** `_server_hardware_changes(current: sqlite3.Connection, preview: sqlite3.Connection, factory_order: str) -> list[dict]` — 封装Server 数据、五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`current: sqlite3.Connection`；`preview: sqlite3.Connection`；`factory_order: str`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L7899 · 方法** `_server_hardware_changes.grouped(connection: sqlite3.Connection) -> dict[tuple[str, ...], dict]` — 封装 `grouped` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`
  - 返回：`dict[tuple[str, ...], dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7806` `_sqlite_table_exists`；`traveler_assistant/order_index.py:7802` `_server_change_key`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L7945 · 函数** `_refresh_server_preview_hardware(config: Config, preview_path: Path | None, folder_paths: list[str], skip_hardware_order_ids: Iterable[str] = (), preview_store: OrderIndexStore | None = None, fittings_cache: dict | None = None) -> list[dict]` — 刷新Server 数据、预览、五金相关数据或步骤。
  - 输入：`config: Config`；`preview_path: Path | None`；`folder_paths: list[str]`；`skip_hardware_order_ids: Iterable[str] = ()`；`preview_store: OrderIndexStore | None = None`；`fittings_cache: dict | None = None`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:7696` `_path_in_folders`；`traveler_assistant/order_index.py:2506` `_selected_hardware_reports`；`traveler_assistant/order_index.py:6273` `_preview_fittings_groups`；`traveler_assistant/report_read_context.py:36` `current_report_context`；`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/inventory.py:2430` `resolve_inventory_items`；`traveler_assistant/order_index.py:7802` `_server_change_key`；`traveler_assistant/inventory.py:2506` `resolved_product_code`；`traveler_assistant/hardware_facts.py:14` `server_hardware_quantity`；`traveler_assistant/hardware_facts.py:56` `replace_factory_hardware`；`traveler_assistant/order_index.py:106` `_now`；另有 2 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.connection.execute`, `set`, `replace_factory_hardware`, `preview.commit`, `preview.close`；是否真实写入仍取决于分支和参数。

- **L8107 · 函数** `_server_preview_payload(config: Config, preview_path: Path | None, token: str, folders: list[Path], include_hardware: bool, preview_store: OrderIndexStore | None = None) -> dict` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`preview_path: Path | None`；`token: str`；`folders: list[Path]`；`include_hardware: bool`；`preview_store: OrderIndexStore | None = None`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/order_index.py:7696` `_path_in_folders`；`traveler_assistant/order_index.py:7757` `_server_material_source_rows`；`traveler_assistant/order_index.py:7731` `_server_material_preview_row`；`traveler_assistant/order_index.py:7806` `_sqlite_table_exists`；`traveler_assistant/order_index.py:7894` `_server_hardware_changes`；`traveler_assistant/order_index.py:7813` `_server_material_change_rows`；`traveler_assistant/order_index.py:8314` `_server_preview_payload.table_records`；`traveler_assistant/order_index.py:8419` `_server_business_revision`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:106` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `store.connection.execute`, `order_ids.update`, `current.execute`, `current.close`, `store.close`；是否真实写入仍取决于分支和参数。

- **L8314 · 方法** `_server_preview_payload.table_records(table: str, where: str, params: tuple = ()) -> list[dict]` — 封装 `table_records` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`table: str`；`where: str`；`params: tuple = ()`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L8406 · 函数** `_server_preview_has_business_changes(payload: dict) -> bool` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`payload: dict`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8419 · 函数** `_server_business_revision(connection: sqlite3.Connection, order_ids: list[str]) -> str` — 封装Server 数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`order_ids: list[str]`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/hardware_source_decisions.py:7` `decision_revision`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L8444 · 函数** `_server_preview_can_acknowledge(payload: dict) -> bool` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`payload: dict`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/hardware_source_decisions.py:7` `decision_revision`

- **L8462 · 函数** `acknowledge_server_preview_memory(config: Config, payload: dict, confirm_write: bool = False) -> dict` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`payload: dict`；`confirm_write: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:8835` `_memory_preview_records`；`traveler_assistant/order_index.py:8444` `_server_preview_can_acknowledge`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:8419` `_server_business_revision`；`traveler_assistant/order_index.py:2137` `OrderIndexStore.save_server_scan_xml_baseline`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `set`, `store.save_server_scan_xml_baseline`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L8500 · 函数** `_server_preview_hardware_source_items(preview_store: OrderIndexStore, folder_paths: list[str], fittings_cache: dict | None = None) -> list[dict]` — 封装Server 数据、预览、五金、来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`preview_store: OrderIndexStore`；`folder_paths: list[str]`；`fittings_cache: dict | None = None`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7696` `_path_in_folders`；`traveler_assistant/order_index.py:2506` `_selected_hardware_reports`；`traveler_assistant/order_index.py:6273` `_preview_fittings_groups`；`traveler_assistant/report_read_context.py:36` `current_report_context`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview_store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L8560 · 函数** `preview_server_changes(config: Config, selected_folders: list[Path], include_hardware: bool = True, hardware_source_choices: dict[str, str] | None = None) -> dict` — 在克隆数据库上演算 Server 变化，生成不会污染正式事实的确认预览。
  - 输入：`config: Config`；`selected_folders: list[Path]`；`include_hardware: bool = True`；`hardware_source_choices: dict[str, str] | None = None`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:6085` `_server_folders_for_sync`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:4399` `_server_folder_handling_mode`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/report_read_context.py:36` `current_report_context`；`traveler_assistant/hardware_source_decisions.py:11` `load_source_decisions`；`traveler_assistant/core.py:118` `progress`；`traveler_assistant/order_index.py:2404` `_report_files`；`traveler_assistant/fittings.py:54` `select_latest_fittings`；`traveler_assistant/order_index.py:8580` `preview_server_changes.finish_timing_stage`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；另有 11 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `routing_store.close`, `source.close`, `preview_store.connection.execute`, `preview_store.connection.executemany`, `preview_store.commit`, `preview_store.close`, `memory.close`；是否真实写入仍取决于分支和参数。

- **L8580 · 方法** `preview_server_changes.finish_timing_stage(stage: str, label: str) -> None` — 结束并收口与 `finish_timing_stage` 对应的数据或步骤。
  - 输入：`stage: str`；`label: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8734 · 函数** `allocate_server_material(config: Config, token: str, material_id: int, order_id: str, quantity: float) -> dict` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`token: str`；`material_id: int`；`order_id: str`；`quantity: float`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:7652` `_server_preview_path`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/database.py:127` `server_material_identity_key`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:7731` `_server_material_preview_row`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.connection.execute`, `preview.connection.commit`, `preview.close`；是否真实写入仍取决于分支和参数。

- **L8835 · 函数** `_memory_preview_records(payload: dict) -> dict[str, list[dict]]` — 封装预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`payload: dict`
  - 返回：`dict[str, list[dict]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L8847 · 函数** `_memory_factory_selection(payload: dict, order_id: str = '', factory_order: str = '') -> list[tuple[str, str]]` — 封装工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`payload: dict`；`order_id: str = ''`；`factory_order: str = ''`
  - 返回：`list[tuple[str, str]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L8893 · 函数** `_server_preview_order_validation_errors(orders: Iterable[dict], selected_order_ids: set[str] | None = None, require_recomputed: bool = False) -> list[str]` — 封装Server 数据、预览、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`orders: Iterable[dict]`；`selected_order_ids: set[str] | None = None`；`require_recomputed: bool = False`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L8927 · 函数** `_require_valid_server_preview_orders(orders: Iterable[dict], selected_order_ids: set[str] | None = None, require_recomputed: bool = False) -> None` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`orders: Iterable[dict]`；`selected_order_ids: set[str] | None = None`；`require_recomputed: bool = False`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:8893` `_server_preview_order_validation_errors`；`traveler_assistant/core.py:44` `RuleError`

- **L8946 · 函数** `_insert_memory_records(connection: sqlite3.Connection, table: str, rows: list[dict]) -> None` — 插入与 `_insert_memory_records` 对应的数据或步骤。
  - 输入：`connection: sqlite3.Connection`；`table: str`；`rows: list[dict]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L8964 · 函数** `_upsert_memory_optimization_artifacts(connection: sqlite3.Connection, rows: list[dict]) -> None` — 新增或更新与 `_upsert_memory_optimization_artifacts` 对应的数据或步骤。
  - 输入：`connection: sqlite3.Connection`；`rows: list[dict]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L9003 · 函数** `_materialize_memory_hardware(config: Config, payload: dict, records: dict[str, list[dict]], selected_factory_ids: set[str], skipped_orders: set[str]) -> None` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`payload: dict`；`records: dict[str, list[dict]]`；`selected_factory_ids: set[str]`；`skipped_orders: set[str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/inventory.py:2430` `resolve_inventory_items`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:2506` `resolved_product_code`；`traveler_assistant/hardware_facts.py:14` `server_hardware_quantity`；`traveler_assistant/order_index.py:106` `_now`

- **L9085 · 函数** `_validated_memory_allocations(payload: dict, records: dict) -> list[dict]` — 校验与 `_validated_memory_allocations` 对应的数据或步骤。
  - 输入：`payload: dict`；`records: dict`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/database.py:127` `server_material_identity_key`；`traveler_assistant/order_index.py:106` `_now`

- **L9121 · 函数** `_confirm_memory_preview(config: Config, payload: dict, order_id: str = '', factory_order: str = '', skip_hardware_order_ids: Iterable[str] = (), confirm_write: bool = False) -> dict` — 封装预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`payload: dict`；`order_id: str = ''`；`factory_order: str = ''`；`skip_hardware_order_ids: Iterable[str] = ()`；`confirm_write: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:8835` `_memory_preview_records`；`traveler_assistant/order_index.py:9085` `_validated_memory_allocations`；`traveler_assistant/order_index.py:8847` `_memory_factory_selection`；`traveler_assistant/order_index.py:8927` `_require_valid_server_preview_orders`；`traveler_assistant/order_index.py:8406` `_server_preview_has_business_changes`；`traveler_assistant/hardware_source_decisions.py:7` `decision_revision`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:8964` `_upsert_memory_optimization_artifacts`；`traveler_assistant/order_index.py:2137` `OrderIndexStore.save_server_scan_xml_baseline`；`traveler_assistant/order_index.py:2857` `_confirmed_material_folders`；`traveler_assistant/order_index.py:106` `_now`；另有 9 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `production.connection.execute`, `_upsert_memory_optimization_artifacts`, `production.save_server_scan_xml_baseline`, `production.commit`, `production.close`, `commit_source_decisions`, `_insert_memory_records`, `replace_factory_hardware`, `existing_orders.update`, `production.connection.commit`；是否真实写入仍取决于分支和参数。

- **L9477 · 函数** `confirm_server_preview_memory(config: Config, payload: dict, order_id: str, factory_order: str, confirm_write: bool = False) -> dict` — 封装Server 数据、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`payload: dict`；`order_id: str`；`factory_order: str`；`confirm_write: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:9121` `_confirm_memory_preview`

- **L9494 · 函数** `confirm_server_material_preview_memory(config: Config, payload: dict, confirm_write: bool = False, skip_hardware_order_ids: Iterable[str] = ()) -> dict` — 封装Server 数据、材料、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`payload: dict`；`confirm_write: bool = False`；`skip_hardware_order_ids: Iterable[str] = ()`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:9121` `_confirm_memory_preview`

- **L9512 · 函数** `confirm_server_material_allocations(config: Config, token: str, confirm_write: bool = False, skip_hardware_order_ids: Iterable[str] = ()) -> dict` — 封装Server 数据、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`token: str`；`confirm_write: bool = False`；`skip_hardware_order_ids: Iterable[str] = ()`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:7652` `_server_preview_path`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:7945` `_refresh_server_preview_hardware`；`traveler_assistant/order_index.py:8107` `_server_preview_payload`；`traveler_assistant/order_index.py:8927` `_require_valid_server_preview_orders`；`traveler_assistant/order_index.py:7757` `_server_material_source_rows`；`traveler_assistant/database.py:127` `server_material_identity_key`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:7696` `_path_in_folders`；`traveler_assistant/inventory.py:2516` `confirm_product_material_attributes`；`traveler_assistant/hardware_facts.py:198` `preserve_confirmed_shipment`；另有 3 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.connection.execute`, `set`, `production.connection.execute`, `replace_factory_hardware`, `production.connection.executemany`, `existing_orders.update`, `production.connection.commit`, `production.close`, `preview.close`；是否真实写入仍取决于分支和参数。

- **L9977 · 函数** `confirm_server_material_preview(config: Config, token: str, confirm_write: bool = False, skip_hardware_order_ids: Iterable[str] = ()) -> dict` — 封装Server 数据、材料、预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`token: str`；`confirm_write: bool = False`；`skip_hardware_order_ids: Iterable[str] = ()`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:9512` `confirm_server_material_allocations`

- **L9996 · 函数** `confirm_server_preview(config: Config, token: str, order_id: str, factory_order: str, confirm_write: bool = False) -> dict` — 验证预览仍与当前文件一致后，把已确认 Server 事实写入中央数据库。
  - 输入：`config: Config`；`token: str`；`order_id: str`；`factory_order: str`；`confirm_write: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_index.py:7652` `_server_preview_path`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.connection.execute`, `preview.close`, `production.connection.execute`, `production.connection.executemany`, `production.connection.commit`, `production.close`, `verification.execute`, `verification.close`；是否真实写入仍取决于分支和参数。

- **L10128 · 函数** `process_server_changes(config: Config, selected_folders: list[Path] | None = None, include_hardware: bool = True) -> dict` — 处理Server 数据相关数据或步骤。
  - 输入：`config: Config`；`selected_folders: list[Path] | None = None`；`include_hardware: bool = True`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:6288` `sync_order_index`

- **L10143 · 函数** `_confirm_current_factory_issue(store: OrderIndexStore, issue: dict, order_id: str, factory_name: str = '') -> None` — 封装工厂单、待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`store: OrderIndexStore`；`issue: dict`；`order_id: str`；`factory_name: str = ''`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`；`traveler_assistant/order_index.py:1620` `OrderIndexStore.upsert_factory`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1444` `OrderIndexStore.upsert_order`；`traveler_assistant/order_index.py:2017` `OrderIndexStore.resolve_active_issue`；`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.upsert_factory`, `store.upsert_order`；是否真实写入仍取决于分支和参数。

- **L10182 · 函数** `auto_resolve_current_issue(config: Config, issue_key: str) -> dict` — 封装待处理问题相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`issue_key: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:2064` `OrderIndexStore.current_issue`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:2017` `OrderIndexStore.resolve_active_issue`；`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:10251` `list_order_index`；`traveler_assistant/order_workflow.py:141` `related_order_ids`；`traveler_assistant/core.py:467` `lookup_aimes_names`；`traveler_assistant/order_index.py:110` `_order_id_from_factory_name`；`traveler_assistant/order_index.py:1924` `OrderIndexStore.upsert_active_issue`；`traveler_assistant/order_index.py:10143` `_confirm_current_factory_issue`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`, `store.commit`, `store.upsert_active_issue`；是否真实写入仍取决于分支和参数。

- **L10234 · 函数** `resolve_current_issue(config: Config, issue_key: str, order_id: str = '', factory_name: str = '') -> dict` — 解析并确定待处理问题相关数据或步骤。
  - 输入：`config: Config`；`issue_key: str`；`order_id: str = ''`；`factory_name: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:2064` `OrderIndexStore.current_issue`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:10143` `_confirm_current_factory_issue`；`traveler_assistant/order_index.py:2017` `OrderIndexStore.resolve_active_issue`；`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:10251` `list_order_index`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`, `store.commit`；是否真实写入仍取决于分支和参数。

- **L10251 · 函数** `list_order_index(config: Config) -> dict` — 读取订单、工厂单、问题和状态，生成看板列表 payload。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:4576` `_reconcile_temporary_order_projections`；`traveler_assistant/order_index.py:3393` `reconcile_outbound_statuses`；`traveler_assistant/core.py:273` `load_aimes_order_cache`；`traveler_assistant/order_index.py:590` `_partition_aimes_rows`；`traveler_assistant/order_index.py:1243` `OrderIndexStore.ignored_aimes_keys`；`traveler_assistant/order_index.py:1272` `OrderIndexStore.aimes_assignments`；`traveler_assistant/order_index.py:1329` `OrderIndexStore.aimes_review_rows`；`traveler_assistant/order_index.py:2205` `OrderIndexStore.summaries`；`traveler_assistant/order_index.py:2181` `OrderIndexStore.latest_changes`；`traveler_assistant/order_index.py:1964` `OrderIndexStore.active_issues`；`traveler_assistant/order_index.py:2091` `OrderIndexStore.latest_sync`；另有 4 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `reconcile_outbound_statuses`, `store.close`；是否真实写入仍取决于分支和参数。

- **L10293 · 函数** `save_order_annotations(config: Config, order_id: str, user_note: str, planned_days: list[dict[str, str]], actual_days: list[dict[str, str]]) -> dict` — 保存订单相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`user_note: str`；`planned_days: list[dict[str, str]]`；`actual_days: list[dict[str, str]]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.save_order_annotations`, `store.close`；是否真实写入仍取决于分支和参数。

- **L10313 · 函数** `ignore_aimes_factories(config: Config, ignore_keys: list[str]) -> dict` — 忽略AIMES 数据相关数据或步骤。
  - 输入：`config: Config`；`ignore_keys: list[str]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:590` `_partition_aimes_rows`；`traveler_assistant/core.py:273` `load_aimes_order_cache`；`traveler_assistant/order_index.py:1243` `OrderIndexStore.ignored_aimes_keys`；`traveler_assistant/order_index.py:1272` `OrderIndexStore.aimes_assignments`；`traveler_assistant/order_index.py:1329` `OrderIndexStore.aimes_review_rows`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:1405` `OrderIndexStore.ignore_aimes_factory`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:10251` `list_order_index`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`, `store.commit`；是否真实写入仍取决于分支和参数。

- **L10336 · 函数** `restore_aimes_factories(config: Config, ignore_keys: list[str]) -> dict` — 恢复AIMES 数据相关数据或步骤。
  - 输入：`config: Config`；`ignore_keys: list[str]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:1438` `OrderIndexStore.restore_aimes_factory`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:10251` `list_order_index`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L10345 · 函数** `assign_aimes_factory_order(config: Config, ignore_key: str, order_id: str) -> dict` — 封装AIMES 数据、工厂单、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`ignore_key: str`；`order_id: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:347` `_valid_aimes_order_id`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:1243` `OrderIndexStore.ignored_aimes_keys`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:1353` `OrderIndexStore.aimes_review_row`；`traveler_assistant/core.py:273` `load_aimes_order_cache`；`traveler_assistant/order_index.py:541` `_aimes_ignore_key`；`traveler_assistant/order_index.py:556` `_aimes_row_issue`；`traveler_assistant/order_index.py:1365` `OrderIndexStore.assign_aimes_factory`；`traveler_assistant/order_index.py:106` `_now`；`traveler_assistant/order_index.py:1444` `OrderIndexStore.upsert_order`；`traveler_assistant/order_index.py:1729` `OrderIndexStore.upsert_aimes_factory`；另有 3 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`, `store.upsert_order`, `store.upsert_aimes_factory`, `store.commit`；是否真实写入仍取决于分支和参数。

- **L10390 · 函数** `restore_aimes_order_assignment(config: Config, ignore_key: str) -> dict` — 恢复AIMES 数据、订单相关数据或步骤。
  - 输入：`config: Config`；`ignore_key: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:1272` `OrderIndexStore.aimes_assignments`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`；`traveler_assistant/order_index.py:1390` `OrderIndexStore.restore_aimes_assignment`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:10251` `list_order_index`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`, `store.commit`；是否真实写入仍取决于分支和参数。

- **L10401 · 函数** `add_manual_factory(config: Config, order_id: str, factory_order: str, factory_name: str) -> dict` — 新增工厂单相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`factory_order: str`；`factory_name: str`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:1444` `OrderIndexStore.upsert_order`；`traveler_assistant/order_index.py:1620` `OrderIndexStore.upsert_factory`；`traveler_assistant/order_index.py:1905` `OrderIndexStore.add_change`；`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`；`traveler_assistant/order_index.py:10251` `list_order_index`；`traveler_assistant/order_index.py:1122` `OrderIndexStore.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/order_service.py`

Python 源码或一次性辅助文件。

- **L30 · 函数** `_config() -> Config` — 封装 `_config` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Config`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:125` `Config`

- **L41 · 函数** `serve() -> int` — 封装 `serve` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_service.py:30` `_config`；`traveler_assistant/database.py:43` `database_path`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/order_index.py:730` `OrderIndexStore`；`traveler_assistant/order_index.py:80` `install_shared_workflow_connection`；`traveler_assistant/operation_log.py:192` `configure_operation_log`；`traveler_assistant/order_service.py:55` `serve.database_stamp`；`traveler_assistant/order_index.py:87` `clear_shared_workflow_connection`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `bootstrap.close`, `sys.stdout.write`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L55 · 方法** `serve.database_stamp() -> tuple[int, int]` — 封装数据库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`tuple[int, int]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `traveler_assistant/order_workflow.py`

订单文件解析、预览、Traveler/材料工作簿生成与更新。

- **L71 · 类** `MaterialItem` — 定义与材料、项目相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L80 · 类** `PreviewFitting` — 定义与预览、五金相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L92 · 类** `FactoryPreview` — 定义与工厂单、预览相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L100 · 类** `OrderPreview` — 定义与订单、预览相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L117 · 函数** `_text(value) -> str` — 封装 `_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L121 · 函数** `_factory_name_belongs_to_order(order_id: str, factory_name: str) -> bool` — 封装工厂单、名称、订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`order_id: str`；`factory_name: str`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L137 · 函数** `_order_ids_in_text(value: str) -> set[str]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: str`
  - 返回：`set[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L141 · 函数** `related_order_ids(folder: Path) -> list[str]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:137` `_order_ids_in_text`；`traveler_assistant/report_read_context.py:63` `report_paths`；`traveler_assistant/order_workflow.py:1373` `parse_board_identity`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `found.update`；是否真实写入仍取决于分支和参数。

- **L165 · 函数** `_number(value, field: str) -> float` — 封装 `_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`；`field: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L174 · 函数** `_display_number(value, number_format: str, field: str) -> float` — 封装 `_display_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`；`number_format: str`；`field: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:117` `_text`

- **L202 · 函数** `_integer(value, field: str) -> float` — 封装 `_integer` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`；`field: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/core.py:44` `RuleError`

- **L211 · 函数** `_integer_cell(cell, field: str) -> float` — 封装 `_integer_cell` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`cell`；`field: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:174` `_display_number`

- **L222 · 函数** `_fmt(value: float) -> str` — 封装 `_fmt` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: float`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L226 · 函数** `_normalized_label(value) -> str` — 规范化与 `_normalized_label` 对应的数据或步骤。
  - 输入：`value`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L230 · 函数** `_canonical_color(value: str) -> str` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L237 · 函数** `resolve_source_root(configured: Path) -> Path` — 解析并确定来源相关数据或步骤。
  - 输入：`configured: Path`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L243 · 函数** `list_order_folders(config: Config) -> list[dict]` — 列出订单相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:237` `resolve_source_root`

- **L259 · 函数** `_find_label_row(ws, label: str) -> int` — 查找行数据相关数据或步骤。
  - 输入：`ws`；`label: str`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/core.py:44` `RuleError`

- **L267 · 函数** `_label_column(ws, row: int, label: str) -> int` — 封装 `_label_column` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`row: int`；`label: str`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/core.py:44` `RuleError`

- **L275 · 函数** `_copy_column_style(ws, source_col: int, target_col: int) -> None` — 封装 `_copy_column_style` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`source_col: int`；`target_col: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copy.copy`；是否真实写入仍取决于分支和参数。

- **L296 · 函数** `repair_material_color_table(path: Path) -> dict` — 封装材料、颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:259` `_find_label_row`；`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:275` `_copy_column_style`；`traveler_assistant/order_workflow.py:222` `_fmt`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `_copy_column_style`, `os.close`, `wb.save`, `os.replace`, `draft.unlink`, `values_wb.close`, `wb.close`；是否真实写入仍取决于分支和参数。

- **L449 · 函数** `parse_order_materials(order_id: str, path: Path) -> tuple[str, list[MaterialItem], dict[str, float]]` — 解析订单相关数据或步骤。
  - 输入：`order_id: str`；`path: Path`
  - 返回：`tuple[str, list[MaterialItem], dict[str, float]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:259` `_find_label_row`；`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:492` `parse_order_materials.required_integer`；`traveler_assistant/order_workflow.py:71` `MaterialItem`；`traveler_assistant/order_workflow.py:174` `_display_number`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:515` `parse_order_materials.required_color_table_integer`；`traveler_assistant/order_workflow.py:539` `parse_order_materials.required_color_table_number`；`traveler_assistant/order_workflow.py:557` `parse_order_materials.optional_total_number`；`traveler_assistant/order_workflow.py:222` `_fmt`；另有 1 个直接调用

- **L473 · 方法** `parse_order_materials.detail_sum(column: int, source_color: str | None = None) -> float` — 封装 `detail_sum` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`column: int`；`source_color: str | None = None`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/order_workflow.py:174` `_display_number`

- **L489 · 方法** `parse_order_materials.cell_label(row: int, column: int, label: str) -> str` — 封装 `cell_label` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: int`；`column: int`；`label: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L492 · 方法** `parse_order_materials.required_integer(row: int, column: int, label: str) -> float` — 封装 `required_integer` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: int`；`column: int`；`label: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:489` `parse_order_materials.cell_label`；`traveler_assistant/order_workflow.py:473` `parse_order_materials.detail_sum`；`traveler_assistant/order_workflow.py:174` `_display_number`；`traveler_assistant/order_workflow.py:211` `_integer_cell`

- **L515 · 方法** `parse_order_materials.required_color_table_integer(row: int, column: int, label: str, source_color: str) -> float` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: int`；`column: int`；`label: str`；`source_color: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:489` `parse_order_materials.cell_label`；`traveler_assistant/order_workflow.py:473` `parse_order_materials.detail_sum`；`traveler_assistant/order_workflow.py:174` `_display_number`；`traveler_assistant/order_workflow.py:211` `_integer_cell`

- **L539 · 方法** `parse_order_materials.required_color_table_number(row: int, column: int, label: str, source_color: str) -> float` — 封装颜色相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: int`；`column: int`；`label: str`；`source_color: str`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:489` `parse_order_materials.cell_label`；`traveler_assistant/order_workflow.py:473` `parse_order_materials.detail_sum`；`traveler_assistant/order_workflow.py:174` `_display_number`

- **L557 · 方法** `parse_order_materials.optional_total_number(row: int, column: int, label: str, integer: bool) -> float | None` — 封装 `optional_total_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: int`；`column: int`；`label: str`；`integer: bool`
  - 返回：`float | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:489` `parse_order_materials.cell_label`；`traveler_assistant/order_workflow.py:211` `_integer_cell`；`traveler_assistant/order_workflow.py:174` `_display_number`

- **L741 · 函数** `_board_report_materials(path: Path, order_id: str, allow_unscoped: bool = False, fallback_name: str = '') -> dict` — 封装 `_board_report_materials` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`order_id: str`；`allow_unscoped: bool = False`；`fallback_name: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:1373` `parse_board_identity`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:121` `_factory_name_belongs_to_order`；`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:202` `_integer`；`traveler_assistant/order_workflow.py:165` `_number`

- **L854 · 函数** `_legacy_traveler_factory_name(path: Path, workbook) -> str` — 封装Traveler、工厂单、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`workbook`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:226` `_normalized_label`

- **L867 · 函数** `_material_item_from_traveler_name(name: str, quantity: float, room_name: str) -> MaterialItem | None` — 封装材料、项目、Traveler、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`；`quantity: float`；`room_name: str`
  - 返回：`MaterialItem | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:71` `MaterialItem`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/core.py:44` `RuleError`

- **L897 · 函数** `_legacy_picking_material_items(path: Path, workbook, order_id: str) -> list[MaterialItem]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`workbook`；`order_id: str`
  - 返回：`list[MaterialItem]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:854` `_legacy_traveler_factory_name`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:867` `_material_item_from_traveler_name`

- **L941 · 函数** `_traveler_material_items(path: Path, order_id: str) -> list[MaterialItem]` — 封装Traveler、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`order_id: str`
  - 返回：`list[MaterialItem]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1446` `parse_traveler`；`traveler_assistant/order_workflow.py:867` `_material_item_from_traveler_name`；`traveler_assistant/order_workflow.py:897` `_legacy_picking_material_items`

- **L956 · 函数** `_aggregate_traveler_material_details(items: list[MaterialItem]) -> tuple[list[list[object]], list[str]]` — 封装Traveler、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: list[MaterialItem]`
  - 返回：`tuple[list[list[object]], list[str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L994 · 函数** `_write_generated_material_workbook(destination: Path, order_id: str, details: list[list[object]], colors: list[str]) -> Path` — 写入材料相关数据或步骤。
  - 输入：`destination: Path`；`order_id: str`；`details: list[list[object]]`；`colors: list[str]`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:275` `_copy_column_style`；`traveler_assistant/order_workflow.py:449` `parse_order_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_copy_column_style`, `wb.save`, `temporary.replace`, `temporary.unlink`；是否真实写入仍取决于分支和参数。

- **L1046 · 函数** `_usage_rows_for_traveler(items: list[MaterialItem], room_name: str) -> list[list[object]]` — 封装Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`items: list[MaterialItem]`；`room_name: str`
  - 返回：`list[list[object]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:956` `_aggregate_traveler_material_details`

- **L1054 · 函数** `_update_legacy_traveler_usage_list(config: Config, path: Path, order_id: str, items: list[MaterialItem]) -> Path | None` — 更新Traveler相关数据或步骤。
  - 输入：`config: Config`；`path: Path`；`order_id: str`；`items: list[MaterialItem]`
  - 返回：`Path | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:854` `_legacy_traveler_factory_name`；`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:2387` `_restore_template_usage_list`；`traveler_assistant/order_workflow.py:1046` `_usage_rows_for_traveler`；`traveler_assistant/order_workflow.py:2246` `_expand_usage_detail_rows`；`traveler_assistant/order_workflow.py:259` `_find_label_row`；`traveler_assistant/order_workflow.py:2397` `_write_merged`；`traveler_assistant/order_workflow.py:2283` `_write_usage_formulas`；`traveler_assistant/order_workflow.py:2964` `_backup_traveler`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1446` `parse_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_write_merged`, `_write_usage_formulas`, `workbook.save`, `os.replace`, `draft.unlink`；是否真实写入仍取决于分支和参数。

- **L1104 · 函数** `generate_material_from_travelers(config: Config, folder: Path, order_id: str, confirm_write: bool = False) -> dict` — 生成材料相关数据或步骤。
  - 输入：`config: Config`；`folder: Path`；`order_id: str`；`confirm_write: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:941` `_traveler_material_items`；`traveler_assistant/order_workflow.py:956` `_aggregate_traveler_material_details`；`traveler_assistant/order_workflow.py:994` `_write_generated_material_workbook`；`traveler_assistant/order_workflow.py:1054` `_update_legacy_traveler_usage_list`；`traveler_assistant/order_workflow.py:449` `parse_order_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_write_generated_material_workbook`, `_update_legacy_traveler_usage_list`；是否真实写入仍取决于分支和参数。

- **L1159 · 函数** `generate_material_from_reports(folder: Path, order_id: str) -> Path` — 生成材料相关数据或步骤。
  - 输入：`folder: Path`；`order_id: str`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/report_read_context.py:63` `report_paths`；`traveler_assistant/order_workflow.py:141` `related_order_ids`；`traveler_assistant/order_workflow.py:1373` `parse_board_identity`；`traveler_assistant/order_workflow.py:121` `_factory_name_belongs_to_order`；`traveler_assistant/order_workflow.py:741` `_board_report_materials`；`traveler_assistant/order_workflow.py:275` `_copy_column_style`；`traveler_assistant/order_workflow.py:449` `parse_order_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `_copy_column_style`, `wb.save`, `temporary.replace`, `temporary.unlink`；是否真实写入仍取决于分支和参数。

- **L1282 · 函数** `parse_material_room_rows(path: Path) -> list[tuple[str, list[MaterialItem], dict[str, float]]]` — 解析材料相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`list[tuple[str, list[MaterialItem], dict[str, float]]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:259` `_find_label_row`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:211` `_integer_cell`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:71` `MaterialItem`；`traveler_assistant/order_workflow.py:174` `_display_number`

- **L1340 · 函数** `_aggregate_material_sources(order_id: str, paths: list[Path])` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`order_id: str`；`paths: list[Path]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:449` `parse_order_materials`；`traveler_assistant/order_workflow.py:1282` `parse_material_room_rows`

- **L1364 · 函数** `_next_value_on_row(ws, row: int, col: int) -> str` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`row: int`；`col: int`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L1373 · 函数** `parse_board_identity(path: Path) -> tuple[str, str]` — 解析与 `parse_board_identity` 对应的数据或步骤。
  - 输入：`path: Path`
  - 返回：`tuple[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:1364` `_next_value_on_row`；`traveler_assistant/core.py:44` `RuleError`

- **L1392 · 函数** `_has_positive_fitting_quantity(path: Path) -> bool | None` — 封装五金、数量相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`bool | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1412 · 函数** `_fittings_report_is_empty(path: Path) -> bool` — 封装 `_fittings_report_is_empty` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L1437 · 函数** `_choose_fittings(folder: Path, allow_missing_factory: bool = False, fallback_factory: str = '') -> tuple[dict[str, list[FittingItem]], list[str]]` — 封装 `_choose_fittings` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`；`allow_missing_factory: bool = False`；`fallback_factory: str = ''`
  - 返回：`tuple[dict[str, list[FittingItem]], list[str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/report_read_context.py:63` `report_paths`；`traveler_assistant/fittings.py:24` `is_fittings_report`；`traveler_assistant/fittings.py:54` `select_latest_fittings`

- **L1466 · 函数** `_ignored_key(name: str, code: str, size: str, unit: str) -> str` — 忽略与 `_ignored_key` 对应的数据或步骤。
  - 输入：`name: str`；`code: str`；`size: str`；`unit: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L1472 · 函数** `_normalize_fittings(items: list[FittingItem], mappings: InventoryMappings) -> list[PreviewFitting]` — 规范化与 `_normalize_fittings` 对应的数据或步骤。
  - 输入：`items: list[FittingItem]`；`mappings: InventoryMappings`
  - 返回：`list[PreviewFitting]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:1466` `_ignored_key`；`traveler_assistant/order_workflow.py:80` `PreviewFitting`

- **L1500 · 函数** `_factory_names(config: Config, folder: Path, factories: set[str], order_id: str, allow_unscoped: bool = False, fallback_name: str = '', fallback_factory: str = '') -> tuple[dict[str, str], list[str]]` — 封装工厂单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`folder: Path`；`factories: set[str]`；`order_id: str`；`allow_unscoped: bool = False`；`fallback_name: str = ''`；`fallback_factory: str = ''`
  - 返回：`tuple[dict[str, str], list[str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/report_read_context.py:63` `report_paths`；`traveler_assistant/order_workflow.py:1373` `parse_board_identity`；`traveler_assistant/order_workflow.py:121` `_factory_name_belongs_to_order`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:262` `load_factory_name_cache`；`traveler_assistant/core.py:467` `lookup_aimes_names`；`traveler_assistant/core.py:269` `save_factory_name_cache`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `connection.execute`, `connection.close`, `names.update`, `cache.update`, `save_factory_name_cache`；是否真实写入仍取决于分支和参数。

- **L1579 · 函数** `_room_matches_order(room: str, order_id: str, names: dict[str, str]) -> bool` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`room: str`；`order_id: str`；`names: dict[str, str]`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:121` `_factory_name_belongs_to_order`

- **L1591 · 函数** `_room_order_ids(room: str) -> list[str]` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`room: str`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L1595 · 函数** `_room_has_explicit_order_identity(rows) -> bool` — 封装订单相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`rows`
  - 返回：`bool`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:1591` `_room_order_ids`

- **L1599 · 函数** `_select_room_materials(rows, order_id: str, names: dict[str, str], known_order_ids: set[str] | None = None)` — 选择与 `_select_room_materials` 对应的数据或步骤。
  - 输入：`rows`；`order_id: str`；`names: dict[str, str]`；`known_order_ids: set[str] | None = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:1591` `_room_order_ids`；`traveler_assistant/order_workflow.py:1579` `_room_matches_order`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:71` `MaterialItem`

- **L1682 · 函数** `preview_order(config: Config, folder: Path, requested_order_id: str | None = None, include_hardware: bool = True, temporary_factory_order: str = '', temporary_factory_name: str = '', persist_facts: bool = True) -> OrderPreview` — 读取一个订单文件夹，校验归属并组装材料、封边、工厂单和五金预览。
  - 输入：`config: Config`；`folder: Path`；`requested_order_id: str | None = None`；`include_hardware: bool = True`；`temporary_factory_order: str = ''`；`temporary_factory_name: str = ''`；`persist_facts: bool = True`
  - 返回：`OrderPreview`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:141` `related_order_ids`；`traveler_assistant/report_read_context.py:63` `report_paths`；`traveler_assistant/core.py:293` `load_material_assignments`；`traveler_assistant/core.py:298` `save_material_assignment`；`traveler_assistant/order_workflow.py:1340` `_aggregate_material_sources`；`traveler_assistant/order_workflow.py:100` `OrderPreview`；`traveler_assistant/order_workflow.py:1893` `persist_preview`；`traveler_assistant/order_workflow.py:1437` `_choose_fittings`；`traveler_assistant/order_workflow.py:1500` `_factory_names`；`traveler_assistant/order_workflow.py:1599` `_select_room_materials`；`traveler_assistant/order_workflow.py:1591` `_room_order_ids`；另有 4 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save_material_assignment`, `set`；是否真实写入仍取决于分支和参数。

- **L1851 · 函数** `_traveler_path(config: Config, order_id: str) -> Path` — 封装Traveler、路径相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1855 · 函数** `find_existing_traveler(config: Config, order_id: str) -> Path | None` — 查找Traveler相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`Path | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:1851` `_traveler_path`

- **L1860 · 函数** `preview_payload(config: Config, preview: OrderPreview) -> dict` — 预览预览相关数据或步骤。
  - 输入：`config: Config`；`preview: OrderPreview`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:1855` `find_existing_traveler`；`traveler_assistant/inventory.py:1983` `InventoryMappings`

- **L1893 · 函数** `persist_preview(config: Config, preview: OrderPreview) -> None` — 封装预览相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`preview: OrderPreview`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2050` `_preview_inventory_resolution_items`；`traveler_assistant/inventory.py:2430` `resolve_inventory_items`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/database.py:20` `enable_foreign_keys`；`traveler_assistant/order_workflow.py:2029` `_preview_material_source_fingerprint`；`traveler_assistant/order_workflow.py:2019` `_material_inventory_name`；`traveler_assistant/inventory.py:2506` `resolved_product_code`；`traveler_assistant/inventory.py:2516` `confirm_product_material_attributes`；`traveler_assistant/order_workflow.py:2040` `_preview_material_fact_fingerprint`；`traveler_assistant/inventory.py:2288` `ignored_hardware_reason`；另有 2 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `replace_factory_hardware`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2019 · 函数** `_material_inventory_name(kind: str, thickness: float, color: str = '') -> str` — 封装材料、库存、名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`kind: str`；`thickness: float`；`color: str = ''`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2029 · 函数** `_preview_material_source_fingerprint(path: Path) -> str` — 预览预览、材料、来源相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.open`, `digest.update`；是否真实写入仍取决于分支和参数。

- **L2040 · 函数** `_preview_material_fact_fingerprint(source_fingerprint: str, product_code: str) -> str` — 预览预览、材料相关数据或步骤。
  - 输入：`source_fingerprint: str`；`product_code: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `digest.update`；是否真实写入仍取决于分支和参数。

- **L2050 · 函数** `_preview_inventory_resolution_items(preview: OrderPreview) -> list[tuple[TravelerItem, str]]` — 预览预览、库存相关数据或步骤。
  - 输入：`preview: OrderPreview`
  - 返回：`list[tuple[TravelerItem, str]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:90` `TravelerItem`；`traveler_assistant/order_workflow.py:2019` `_material_inventory_name`

- **L2087 · 函数** `preview_related_orders(config: Config, folder: Path, include_hardware: bool = True) -> dict` — 预览预览相关数据或步骤。
  - 输入：`config: Config`；`folder: Path`；`include_hardware: bool = True`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:141` `related_order_ids`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:1860` `preview_payload`；`traveler_assistant/order_workflow.py:1682` `preview_order`

- **L2131 · 函数** `update_related_orders(config: Config, folder: Path, generate: bool = False, include_hardware: bool = True) -> dict` — 更新与 `update_related_orders` 对应的数据或步骤。
  - 输入：`config: Config`；`folder: Path`；`generate: bool = False`；`include_hardware: bool = True`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2087` `preview_related_orders`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:1682` `preview_order`；`traveler_assistant/order_workflow.py:3093` `generate_order_traveler`；`traveler_assistant/order_workflow.py:3318` `update_order_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_order_traveler`；是否真实写入仍取决于分支和参数。

- **L2179 · 函数** `set_ignored(config: Config, name: str, ignored: bool) -> None` — 设置与 `set_ignored` 对应的数据或步骤。
  - 输入：`config: Config`；`name: str`；`ignored: bool`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:2668` `set_ignored_mapping`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set_ignored_mapping`；是否真实写入仍取决于分支和参数。

- **L2188 · 函数** `_copy_cell(source, target) -> None` — 封装 `_copy_cell` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source`；`target`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copy.copy`；是否真实写入仍取决于分支和参数。

- **L2202 · 函数** `_copy_worksheet(source, target_wb, title: str, index: int)` — 封装 `_copy_worksheet` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source`；`target_wb`；`title: str`；`index: int`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2188` `_copy_cell`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_copy_cell`, `copy.copy`；是否真实写入仍取决于分支和参数。

- **L2222 · 函数** `_shift_merges_for_insert(ws, row: int, count: int) -> None` — 封装 `_shift_merges_for_insert` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`row: int`；`count: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ws.insert_rows`；是否真实写入仍取决于分支和参数。

- **L2246 · 函数** `_expand_usage_detail_rows(ws, required_rows: int) -> None` — 封装 `_expand_usage_detail_rows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`required_rows: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:259` `_find_label_row`；`traveler_assistant/order_workflow.py:2222` `_shift_merges_for_insert`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_shift_merges_for_insert`, `copy.copy`；是否真实写入仍取决于分支和参数。

- **L2283 · 函数** `_write_usage_formulas(ws) -> None` — 写入与 `_write_usage_formulas` 对应的数据或步骤。
  - 输入：`ws`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:259` `_find_label_row`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:275` `_copy_column_style`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `_copy_column_style`；是否真实写入仍取决于分支和参数。

- **L2339 · 函数** `_fill_usage_list(source_path: Path, wb, order_id: str, allowed_rooms: set[str] | None = None) -> None` — 封装 `_fill_usage_list` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source_path: Path`；`wb`；`order_id: str`；`allowed_rooms: set[str] | None = None`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:259` `_find_label_row`；`traveler_assistant/order_workflow.py:2246` `_expand_usage_detail_rows`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:2397` `_write_merged`；`traveler_assistant/order_workflow.py:2283` `_write_usage_formulas`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_write_merged`, `_write_usage_formulas`；是否真实写入仍取决于分支和参数。

- **L2377 · 函数** `_restore_template_picking_list(config: Config, wb) -> None` — 恢复与 `_restore_template_picking_list` 对应的数据或步骤。
  - 输入：`config: Config`；`wb`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:2202` `_copy_worksheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_copy_worksheet`；是否真实写入仍取决于分支和参数。

- **L2387 · 函数** `_restore_template_usage_list(config: Config, wb) -> None` — 恢复与 `_restore_template_usage_list` 对应的数据或步骤。
  - 输入：`config: Config`；`wb`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:2202` `_copy_worksheet`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_copy_worksheet`；是否真实写入仍取决于分支和参数。

- **L2397 · 函数** `_write_merged(ws, row: int, col: int, value) -> None` — 写入与 `_write_merged` 对应的数据或步骤。
  - 输入：`ws`；`row: int`；`col: int`；`value`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2408 · 函数** `_write_initial_traveler_date(ws) -> None` — 写入Traveler、日期相关数据或步骤。
  - 输入：`ws`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:226` `_normalized_label`；`traveler_assistant/order_workflow.py:2397` `_write_merged`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_write_merged`；是否真实写入仍取决于分支和参数。

- **L2426 · 函数** `_snapshot_rows(ws, first: int, last: int) -> dict` — 封装 `_snapshot_rows` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`first: int`；`last: int`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copy.copy`；是否真实写入仍取决于分支和参数。

- **L2446 · 函数** `_paste_snapshot(ws, snapshot: dict, destination_row: int) -> None` — 封装 `_paste_snapshot` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`snapshot: dict`；`destination_row: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2188` `_copy_cell`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_copy_cell`；是否真实写入仍取决于分支和参数。

- **L2459 · 函数** `_style_merged_row(ws, row: int, last_col: int, color: str) -> None` — 封装行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`row: int`；`last_col: int`；`color: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copy.copy`；是否真实写入仍取决于分支和参数。

- **L2488 · 函数** `_style_picking_list_title(ws, last_col: int) -> None` — 封装 `_style_picking_list_title` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`last_col: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copy.copy`；是否真实写入仍取决于分支和参数。

- **L2505 · 函数** `_clear_picking_list_business_data(ws) -> None` — 清理与 `_clear_picking_list_business_data` 对应的数据或步骤。
  - 输入：`ws`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L2521 · 函数** `_prepare_picking_list(wb, preview: OrderPreview) -> None` — 准备并校验与 `_prepare_picking_list` 对应的数据或步骤。
  - 输入：`wb`；`preview: OrderPreview`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2505` `_clear_picking_list_business_data`；`traveler_assistant/order_workflow.py:2426` `_snapshot_rows`；`traveler_assistant/order_workflow.py:2488` `_style_picking_list_title`；`traveler_assistant/order_workflow.py:2446` `_paste_snapshot`；`traveler_assistant/order_workflow.py:2222` `_shift_merges_for_insert`；`traveler_assistant/order_workflow.py:2188` `_copy_cell`；`traveler_assistant/order_workflow.py:2397` `_write_merged`；`traveler_assistant/order_workflow.py:2459` `_style_merged_row`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:2826` `_restore_manual_hardware`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ws.delete_rows`, `ws.insert_rows`, `_shift_merges_for_insert`, `_copy_cell`, `_write_merged`；是否真实写入仍取决于分支和参数。

- **L2636 · 函数** `_purchase_material_rows(preview: OrderPreview) -> list[tuple[str, str, float]]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`preview: OrderPreview`
  - 返回：`list[tuple[str, str, float]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2663 · 函数** `_purchase_hardware_rows(preview: OrderPreview) -> list[tuple[str, str, float, str]]` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`preview: OrderPreview`
  - 返回：`list[tuple[str, str, float, str]]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2679 · 函数** `_insert_purchase_rows(ws, insertion_row: int, count: int, template_row: int) -> None` — 插入与 `_insert_purchase_rows` 对应的数据或步骤。
  - 输入：`ws`；`insertion_row: int`；`count: int`；`template_row: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2222` `_shift_merges_for_insert`；`traveler_assistant/order_workflow.py:2188` `_copy_cell`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_shift_merges_for_insert`, `_copy_cell`；是否真实写入仍取决于分支和参数。

- **L2691 · 函数** `_prepare_purchase_list(wb, preview: OrderPreview) -> None` — 准备并校验与 `_prepare_purchase_list` 对应的数据或步骤。
  - 输入：`wb`；`preview: OrderPreview`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2636` `_purchase_material_rows`；`traveler_assistant/order_workflow.py:2663` `_purchase_hardware_rows`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:2397` `_write_merged`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:2679` `_insert_purchase_rows`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_write_merged`, `_insert_purchase_rows`；是否真实写入仍取决于分支和参数。

- **L2759 · 函数** `_manual_hardware(ws) -> dict[str, list[dict]]` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`
  - 返回：`dict[str, list[dict]]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L2798 · 函数** `_manual_hardware_block(ws, factory: str) -> tuple[int, list[int], int] | None` — 封装五金相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`ws`；`factory: str`
  - 返回：`tuple[int, list[int], int] | None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`

- **L2826 · 函数** `_restore_manual_hardware(ws, hardware: dict[str, list[dict]]) -> None` — 恢复五金相关数据或步骤。
  - 输入：`ws`；`hardware: dict[str, list[dict]]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:2798` `_manual_hardware_block`；`traveler_assistant/order_workflow.py:2222` `_shift_merges_for_insert`；`traveler_assistant/order_workflow.py:2188` `_copy_cell`；`traveler_assistant/order_workflow.py:2397` `_write_merged`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ws.delete_rows`, `_shift_merges_for_insert`, `_copy_cell`, `_write_merged`；是否真实写入仍取决于分支和参数。

- **L2898 · 函数** `_positive_hardware_quantity(value) -> int` — 封装五金、数量相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/core.py:44` `RuleError`

- **L2905 · 函数** `_resolve_manual_hardware_factory(config: Config, order_id: str, factory_name: str) -> tuple[str, str]` — 解析并确定五金、工厂单相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`factory_name: str`
  - 返回：`tuple[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L2938 · 函数** `preview_manual_hardware(config: Config, order_id: str, factory_name: str, product_code: str, quantity, remarks: str = '') -> dict` — 预览预览、五金相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`factory_name: str`；`product_code: str`；`quantity`；`remarks: str = ''`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/inventory.py:1686` `ProductDatabase`；`traveler_assistant/inventory.py:3355` `bootstrap_product_database`；`traveler_assistant/order_workflow.py:2905` `_resolve_manual_hardware_factory`；`traveler_assistant/order_workflow.py:2898` `_positive_hardware_quantity`；`traveler_assistant/order_workflow.py:117` `_text`

- **L2964 · 函数** `_backup_traveler(config: Config, traveler: Path, order_id: str, label: str = 'backup') -> Path` — 封装备份、Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`traveler: Path`；`order_id: str`；`label: str = 'backup'`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `backup_dir.mkdir`；是否真实写入仍取决于分支和参数。

- **L2973 · 函数** `add_manual_hardware(config: Config, order_id: str, factory_name: str, product_code: str, quantity, remarks: str = '') -> tuple[Path, Path, dict]` — 新增五金相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`factory_name: str`；`product_code: str`；`quantity`；`remarks: str = ''`
  - 返回：`tuple[Path, Path, dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2938` `preview_manual_hardware`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/database.py:38` `connect_database`；`traveler_assistant/inventory.py:1983` `InventoryMappings`；`traveler_assistant/inventory.py:2288` `ignored_hardware_reason`；`traveler_assistant/order_workflow.py:2898` `_positive_hardware_quantity`；`traveler_assistant/order_workflow.py:117` `_text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.executemany`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L3093 · 函数** `generate_order_traveler(config: Config, preview: OrderPreview) -> Path` — 根据订单预览和模板生成新的 Traveler，并在保存后重新打开校验。
  - 输入：`config: Config`；`preview: OrderPreview`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:1851` `_traveler_path`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:2408` `_write_initial_traveler_date`；`traveler_assistant/order_workflow.py:2339` `_fill_usage_list`；`traveler_assistant/order_workflow.py:2521` `_prepare_picking_list`；`traveler_assistant/order_workflow.py:2691` `_prepare_purchase_list`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `destination_dir.mkdir`, `set`, `_write_initial_traveler_date`, `wb.save`, `os.replace`；是否真实写入仍取决于分支和参数。

- **L3127 · 函数** `_database_material_template(config: Config) -> Path` — 封装数据库、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L3137 · 函数** `_write_database_material_workbook(config: Config, destination: Path, order_id: str, material_rows: list[dict]) -> None` — 写入数据库、材料相关数据或步骤。
  - 输入：`config: Config`；`destination: Path`；`order_id: str`；`material_rows: list[dict]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:3127` `_database_material_template`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:275` `_copy_column_style`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `values.update`, `_copy_column_style`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L3219 · 函数** `generate_database_order_traveler(config: Config, order_id: str) -> Path` — 生成数据库、订单、Traveler相关数据或步骤。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_details.py:12` `order_detail`；`traveler_assistant/order_workflow.py:117` `_text`；`traveler_assistant/order_workflow.py:165` `_number`；`traveler_assistant/order_workflow.py:230` `_canonical_color`；`traveler_assistant/order_workflow.py:71` `MaterialItem`；`traveler_assistant/order_workflow.py:80` `PreviewFitting`；`traveler_assistant/order_workflow.py:92` `FactoryPreview`；`traveler_assistant/order_workflow.py:3137` `_write_database_material_workbook`；`traveler_assistant/order_workflow.py:100` `OrderPreview`；`traveler_assistant/order_workflow.py:3093` `generate_order_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `_write_database_material_workbook`, `copy.copy`, `material_workbook.unlink`；是否真实写入仍取决于分支和参数。

- **L3310 · 函数** `generate_temporary_traveler(config: Config, preview: OrderPreview) -> Path` — 生成Traveler相关数据或步骤。
  - 输入：`config: Config`；`preview: OrderPreview`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:3093` `generate_order_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copy.copy`；是否真实写入仍取决于分支和参数。

- **L3318 · 函数** `update_order_traveler(config: Config, preview: OrderPreview) -> tuple[Path, Path]` — 备份并升级已有 Traveler，保留人工数据后写入最新业务事实。
  - 输入：`config: Config`；`preview: OrderPreview`
  - 返回：`tuple[Path, Path]`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:1855` `find_existing_traveler`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:1851` `_traveler_path`；`traveler_assistant/order_workflow.py:2964` `_backup_traveler`；`traveler_assistant/order_workflow.py:2759` `_manual_hardware`；`traveler_assistant/order_workflow.py:2387` `_restore_template_usage_list`；`traveler_assistant/order_workflow.py:2377` `_restore_template_picking_list`；`traveler_assistant/order_workflow.py:2339` `_fill_usage_list`；`traveler_assistant/order_workflow.py:2521` `_prepare_picking_list`；`traveler_assistant/order_workflow.py:2691` `_prepare_purchase_list`；`traveler_assistant/order_workflow.py:2826` `_restore_manual_hardware`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`, `wb.save`, `os.replace`；是否真实写入仍取决于分支和参数。

- **L3355 · 函数** `_config_from_args(args, base_config: Config | None = None) -> Config` — 封装 `_config_from_args` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`args`；`base_config: Config | None = None`
  - 返回：`Config`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/core.py:125` `Config`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `copy.copy`；是否真实写入仍取决于分支和参数。

- **L3381 · 函数** `main(argv: list[str] | None = None, config_override: Config | None = None, logger_override = None, emit_result: bool = True, result_sink: dict | None = None, stdin_text: str | None = None) -> int` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：`argv: list[str] | None = None`；`config_override: Config | None = None`；`logger_override = None`；`emit_result: bool = True`；`result_sink: dict | None = None`；`stdin_text: str | None = None`
  - 返回：`int`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:3355` `_config_from_args`；`traveler_assistant/operation_log.py:192` `configure_operation_log`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/test_data.py:84` `create_local_test_source`；`traveler_assistant/order_workflow.py:243` `list_order_folders`；`traveler_assistant/order_index.py:10251` `list_order_index`；`traveler_assistant/order_details.py:12` `order_detail`；`traveler_assistant/production.py:282` `production_preview`；`traveler_assistant/production.py:334` `prepare_production`；`traveler_assistant/production.py:430` `migrate_legacy_production_state`；`traveler_assistant/costing.py:380` `export_order_cost`；`traveler_assistant/costing.py:194` `calculate_order_cost`；另有 39 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save_order_annotations`, `set_ignored`, `save_manual_hardware`, `save_material_assignment`, `_record_generated_material_baseline`, `baseline_store.commit`, `baseline_store.close`, `update_related_orders`, `update_order_traveler`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/production.py`

生产备料预览、生产完成记录和出货前置校验。

- **L20 · 函数** `_now() -> str` — 封装 `_now` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L24 · 函数** `_normal(value: object) -> str` — 封装 `_normal` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: object`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L28 · 函数** `material_key(row: dict) -> str` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/core.py:44` `RuleError`

- **L38 · 函数** `production_material_code(row: dict) -> str` — 封装生产、材料、编码相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: dict`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/production.py:28` `material_key`

- **L47 · 函数** `_material_row(row: sqlite3.Row | dict) -> dict` — 封装材料、行数据相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`row: sqlite3.Row | dict`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/production.py:28` `material_key`

- **L56 · 函数** `_connect(config: Config) -> sqlite3.Connection` — 封装 `_connect` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`
  - 返回：`sqlite3.Connection`
  - 静态可确认的项目内下一跳：`traveler_assistant/database.py:438` `ensure_schema`；`traveler_assistant/database.py:38` `connect_database`

- **L63 · 函数** `_selected_factory_rows(connection: sqlite3.Connection, order_id: str, factory_orders: Iterable[str]) -> list[sqlite3.Row]` — 选择工厂单相关数据或步骤。
  - 输入：`connection: sqlite3.Connection`；`order_id: str`；`factory_orders: Iterable[str]`
  - 返回：`list[sqlite3.Row]`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `set`；是否真实写入仍取决于分支和参数。

- **L82 · 函数** `_consumed(connection: sqlite3.Connection, order_id: str) -> dict[str, float]` — 消费并转换与 `_consumed` 对应的数据或步骤。
  - 输入：`connection: sqlite3.Connection`；`order_id: str`
  - 返回：`dict[str, float]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L94 · 函数** `_order_material_rows(connection: sqlite3.Connection, order_id: str) -> list[dict]` — 封装订单、材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`order_id: str`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:47` `_material_row`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`；是否真实写入仍取决于分支和参数。

- **L110 · 函数** `_historical_material_product_codes(connection: sqlite3.Connection, materials: list[dict]) -> dict[str, str]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`connection: sqlite3.Connection`；`materials: list[dict]`
  - 返回：`dict[str, str]`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`

- **L127 · 函数** `_legacy_inventory_consumed(config: Config, connection: sqlite3.Connection, order_id: str) -> dict[str, float]` — 封装库存相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`connection: sqlite3.Connection`；`order_id: str`
  - 返回：`dict[str, float]`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:94` `_order_material_rows`；`traveler_assistant/production.py:110` `_historical_material_product_codes`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `set`；是否真实写入仍取决于分支和参数。

- **L212 · 函数** `cumulative_production_materials(config: Config, order_id: str, current_materials: Iterable[dict]) -> list[dict]` — 封装生产相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`；`current_materials: Iterable[dict]`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/production.py:56` `_connect`；`traveler_assistant/production.py:94` `_order_material_rows`；`traveler_assistant/production.py:82` `_consumed`；`traveler_assistant/production.py:127` `_legacy_inventory_consumed`；`traveler_assistant/production.py:38` `production_material_code`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.close`；是否真实写入仍取决于分支和参数。

- **L282 · 函数** `production_preview(config: Config, order_id: str, factory_orders: Iterable[str]) -> dict` — 从中央数据库汇总尚需生产的材料并生成只读生产预览。
  - 输入：`config: Config`；`order_id: str`；`factory_orders: Iterable[str]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/production.py:56` `_connect`；`traveler_assistant/production.py:63` `_selected_factory_rows`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/production.py:82` `_consumed`；`traveler_assistant/production.py:127` `_legacy_inventory_consumed`；`traveler_assistant/production.py:94` `_order_material_rows`；`traveler_assistant/production.py:20` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L323 · 函数** `_decode_materials(value: object) -> list[dict]` — 封装 `_decode_materials` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value: object`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:44` `RuleError`

- **L334 · 函数** `prepare_production(config: Config, order_id: str, factory_orders: Iterable[str], materials: object) -> dict` — 校验生产选择并保存本次生产准备范围。
  - 输入：`config: Config`；`order_id: str`；`factory_orders: Iterable[str]`；`materials: object`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:282` `production_preview`；`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/production.py:28` `material_key`；`traveler_assistant/production.py:323` `_decode_materials`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/production.py:20` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L383 · 函数** `record_completed_production(connection: sqlite3.Connection, draft: dict) -> dict` — 写入已完成生产事实并返回更新后的状态。
  - 输入：`connection: sqlite3.Connection`；`draft: dict`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/production.py:38` `production_material_code`；`traveler_assistant/production.py:20` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `set`；是否真实写入仍取决于分支和参数。

- **L430 · 函数** `migrate_legacy_production_state(config: Config) -> dict` — 迁移生产相关数据或步骤。
  - 输入：`config: Config`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:56` `_connect`；`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/production.py:20` `_now`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L475 · 函数** `assert_shipment_allowed(config: Config, order_id: str, factory_orders: Iterable[str]) -> None` — 强制校验与 `assert_shipment_allowed` 对应的数据或步骤。
  - 输入：`config: Config`；`order_id: str`；`factory_orders: Iterable[str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/production.py:24` `_normal`；`traveler_assistant/production.py:56` `_connect`；`traveler_assistant/production.py:63` `_selected_factory_rows`；`traveler_assistant/core.py:44` `RuleError`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/report_read_context.py`

Python 源码或一次性辅助文件。

- **L17 · 类** `ReportReadContext` — 定义 `ReportReadContext` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L36 · 函数** `current_report_context()` — 封装 `current_report_context` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L41 · 函数** `report_read_session(choices = None)` — 封装 `report_read_session` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`choices = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/report_read_context.py:17` `ReportReadContext`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_current.set`；是否真实写入仍取决于分支和参数。

- **L50 · 函数** `preview_read_session(function)` — 预览预览相关数据或步骤。
  - 输入：`function`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L52 · 方法** `preview_read_session.run(*args, **kwargs)` — 执行与 `run` 对应的数据或步骤。
  - 输入：`*args`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/report_read_context.py:41` `report_read_session`

- **L63 · 函数** `report_paths(folder: Path)` — 封装 `report_paths` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`folder: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L73 · 函数** `cached_report(function)` — 封装 `cached_report` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`function`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L76 · 方法** `cached_report.read(*args, **kwargs)` — 读取与 `read` 对应的数据或步骤。
  - 输入：`*args`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `traveler_assistant/runtime_store.py`

助手学习命令与 Agent Token 用量的 SQLite 存储。

- **L16 · 函数** `runtime_database_path(state_dir: Path) -> Path` — 执行数据库、路径相关数据或步骤。
  - 输入：`state_dir: Path`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L22 · 类** `TokenUsage` — 定义 `TokenUsage` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L27 · 方法** `TokenUsage.total_tokens() -> int` — 封装 `total_tokens` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L31 · 类** `RuntimeStore` — 定义 `RuntimeStore` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L32 · 方法** `RuntimeStore.__init__(path: Path)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `self.connection.set_trace_callback`, `self.connection.execute`, `self.connection.close`, `self.connection.commit`；是否真实写入仍取决于分支和参数。

- **L63 · 方法** `RuntimeStore.record_agent_usage(model: str, usage: TokenUsage) -> None` — 记录记录相关数据或步骤。
  - 输入：`model: str`；`usage: TokenUsage`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`, `self.connection.commit`；是否真实写入仍取决于分支和参数。

- **L70 · 方法** `RuntimeStore.remember_command(normalized_text: str, action: str, arguments: dict[str, str]) -> None` — 封装 `remember_command` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`normalized_text: str`；`action: str`；`arguments: dict[str, str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_index.py:2088` `OrderIndexStore.commit`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`, `self.connection.commit`；是否真实写入仍取决于分支和参数。

- **L89 · 方法** `RuntimeStore.learned_command(normalized_text: str) -> tuple[str, dict[str, str]] | None` — 封装 `learned_command` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`normalized_text: str`
  - 返回：`tuple[str, dict[str, str]] | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

- **L104 · 方法** `RuntimeStore.token_summary(now: datetime | None = None) -> dict[str, int]` — 封装 `token_summary` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`now: datetime | None = None`
  - 返回：`dict[str, int]`
  - 静态可确认的项目内下一跳：`traveler_assistant/runtime_store.py:110` `RuntimeStore.token_summary.total_since`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `week_start.replace`, `now.replace`；是否真实写入仍取决于分支和参数。

- **L110 · 方法** `RuntimeStore.token_summary.total_since(start: datetime | None) -> int` — 封装 `total_since` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`start: datetime | None`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `self.connection.execute`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/streaming_process.py`

Python 源码或一次性辅助文件。

- **L9 · 函数** `run_with_progress(command, input_text, env, timeout, on_stderr_line)` — 执行进度相关数据或步骤。
  - 输入：`command`；`input_text`；`env`；`timeout`；`on_stderr_line`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `subprocess.Popen`, `process.stdin.write`, `process.stdin.close`, `selector.close`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/test_data.py`

创建隔离的本地测试订单和工作簿样本。

- **L14 · 函数** `_atomic_save(workbook: Workbook, destination: Path) -> None` — 封装 `_atomic_save` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`workbook: Workbook`；`destination: Path`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `destination.parent.mkdir`, `workbook.save`, `os.replace`, `draft.unlink`；是否真实写入仍取决于分支和参数。

- **L27 · 函数** `_materials(path: Path, order_id: str, color: str, panel_qty: int, edge_qty: float) -> None` — 封装 `_materials` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`order_id: str`；`color: str`；`panel_qty: int`；`edge_qty: float`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/test_data.py:14` `_atomic_save`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_atomic_save`；是否真实写入仍取决于分支和参数。

- **L54 · 函数** `_board(path: Path, factory: str, name: str) -> None` — 封装 `_board` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`factory: str`；`name: str`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/test_data.py:14` `_atomic_save`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_atomic_save`；是否真实写入仍取决于分支和参数。

- **L63 · 函数** `_fittings(path: Path, groups: list[tuple[str, int]]) -> None` — 封装 `_fittings` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`groups: list[tuple[str, int]]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`traveler_assistant/test_data.py:14` `_atomic_save`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_atomic_save`；是否真实写入仍取决于分支和参数。

- **L84 · 函数** `create_local_test_source(target_root: Path) -> dict` — 创建来源相关数据或步骤。
  - 输入：`target_root: Path`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/core.py:118` `progress`；`traveler_assistant/test_data.py:27` `_materials`；`traveler_assistant/test_data.py:54` `_board`；`traveler_assistant/test_data.py:63` `_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `target_root.mkdir`, `temporary.write_text`, `os.replace`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/tool_gateway.py`

Typed Tool Gateway：审批校验和确定性业务动作分发。

- **L31 · 函数** `_order_folder(config: Config, order_id: str) -> Path` — 封装订单、文件夹相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`config: Config`；`order_id: str`
  - 返回：`Path`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:237` `resolve_source_root`；`traveler_assistant/core.py:44` `RuleError`

- **L52 · 函数** `execute_local_command(config: Config, command: LocalCommand, approved: bool = False) -> dict` — 校验结构化命令、审批状态和参数，再分发到确定性业务函数。
  - 输入：`config: Config`；`command: LocalCommand`；`approved: bool = False`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`traveler_assistant/order_workflow.py:2938` `preview_manual_hardware`；`traveler_assistant/order_workflow.py:2973` `add_manual_hardware`；`traveler_assistant/order_workflow.py:1682` `preview_order`；`traveler_assistant/tool_gateway.py:31` `_order_folder`；`traveler_assistant/order_workflow.py:1860` `preview_payload`；`traveler_assistant/order_workflow.py:243` `list_order_folders`；`traveler_assistant/inventory.py:4472` `check_database_stock`；`traveler_assistant/core.py:44` `RuleError`；`traveler_assistant/order_workflow.py:3093` `generate_order_traveler`；`traveler_assistant/order_workflow.py:3318` `update_order_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_order_traveler`, `payload.update`；是否真实写入仍取决于分支和参数。

## `traveler_assistant/wecom_service.py`

Python 源码或一次性辅助文件。

- **L14 · 函数** `_run_wecom_command(args)` — 执行与 `_run_wecom_command` 对应的数据或步骤。
  - 输入：`args`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `subprocess.run`；是否真实写入仍取决于分支和参数。

- **L31 · 函数** `get_smartsheet_info(doc_url)` — 封装 `get_smartsheet_info` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`doc_url`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/wecom_service.py:14` `_run_wecom_command`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_run_wecom_command`；是否真实写入仍取决于分支和参数。

- **L47 · 函数** `get_records(doc_url, sheet_id)` — 封装 `get_records` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`doc_url`；`sheet_id`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`traveler_assistant/wecom_service.py:14` `_run_wecom_command`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_run_wecom_command`；是否真实写入仍取决于分支和参数。

- **L87 · 函数** `get_text(values, field_name)` — 封装 `get_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`values`；`field_name`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L111 · 类** `WeComRepository` — 定义 `WeComRepository` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L114 · 方法** `WeComRepository.__init__(state_dir: Path)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`state_dir: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L122 · 方法** `WeComRepository._get_connection() -> sqlite3.Connection` — 封装 `_get_connection` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`sqlite3.Connection`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `conn.execute`；是否真实写入仍取决于分支和参数。

- **L129 · 方法** `WeComRepository.get_db_order_status(order_id: str) -> list[tuple]` — 封装订单、状态相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`order_id: str`
  - 返回：`list[tuple]`
  - 静态可确认的项目内下一跳：`traveler_assistant/wecom_service.py:122` `WeComRepository._get_connection`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `conn.execute`, `conn.close`；是否真实写入仍取决于分支和参数。

- **L149 · 方法** `WeComRepository.update_wecom_order_status(order_id: str) -> list[tuple]` — 更新订单、状态相关数据或步骤。
  - 输入：`order_id: str`
  - 返回：`list[tuple]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
