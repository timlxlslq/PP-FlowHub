# PP FlowHub 测试、脚本与工具全符号中文参考

> 本文件由 `tools/generate_code_reference.py` 生成。请不要手工修改。

## 如何阅读

- 范围：`tests/`、`scripts/`、`tools/` 和 `outputs/` 中的一方辅助代码，共登记 **448** 个类型、函数、方法、计算属性或脚本过程。
- “输入”来自静态签名；`self`/`cls` 不重复列出。未声明类型不代表运行时没有约束。
- “项目内下一跳”只表示源码中可静态确认的直接调用，不表示每个分支都会执行。
- `self.method()`、协议分发、闭包、Swift 重载和动态导入可能无法唯一解析；关键业务路径以 `09-user-operation-call-chains.md` 为准。
- “副作用提示”是保守提醒，不等于函数一定执行写入。确认真实行为时应继续阅读分支、日志和测试。

## `outputs/pp0018-material-cost/extract_pp0018.py`

历史诊断/交付过程的一次性辅助脚本，不属于正式运行链路。

- **L16 · 函数** `text(value) -> str` — 封装 `text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`value`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L20 · 函数** `parse_quantity(value) -> float` — 解析数量相关数据或步骤。
  - 输入：`value`
  - 返回：`float`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `text(value).replace`；是否真实写入仍取决于分支和参数。

- **L37 · 函数** `normalize_name(value: str) -> str` — 规范化名称相关数据或步骤。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `value.replace`；是否真实写入仍取决于分支和参数。

- **L43 · 函数** `material_rows(path: Path, sheet_name: str) -> list[dict]` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`sheet_name: str`
  - 返回：`list[dict]`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`；`outputs/pp0018-material-cost/extract_pp0018.py:37` `normalize_name`；`outputs/pp0018-material-cost/extract_pp0018.py:20` `parse_quantity`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.close`；是否真实写入仍取决于分支和参数。

- **L85 · 函数** `room_name(path: Path) -> str` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.close`；是否真实写入仍取决于分支和参数。

- **L93 · 函数** `load_prices() -> dict[str, dict]` — 读取与 `load_prices` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`dict[str, dict]`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:16` `text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.close`；是否真实写入仍取决于分支和参数。

- **L115 · 函数** `mapped_price(material_name: str, raw_remark: str, prices: dict[str, dict]) -> dict` — 封装 `mapped_price` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`material_name: str`；`raw_remark: str`；`prices: dict[str, dict]`
  - 返回：`dict`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:37` `normalize_name`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `normalize_name(material_name).replace`；是否真实写入仍取决于分支和参数。

- **L162 · 函数** `main() -> None` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`None`
  - 静态可确认的项目内下一跳：`outputs/pp0018-material-cost/extract_pp0018.py:93` `load_prices`；`outputs/pp0018-material-cost/extract_pp0018.py:85` `room_name`；`outputs/pp0018-material-cost/extract_pp0018.py:43` `material_rows`；`outputs/pp0018-material-cost/extract_pp0018.py:37` `normalize_name`；`outputs/pp0018-material-cost/extract_pp0018.py:115` `mapped_price`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `normalize_name(row['name']).replace`, `set`, `normalize_name(item['name']).replace`, `entry.update`, `OUTPUT_JSON.parent.mkdir`, `OUTPUT_JSON.write_text`；是否真实写入仍取决于分支和参数。

## `scripts/build-app`

构建 PP FlowHub.app，组装 Swift、Python、资源和辅助工具。

- **L1 · 脚本过程** `scripts/build-app "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/install-app`

签名、校验并把构建产物安装到 /Applications。

- **L1 · 脚本过程** `scripts/install-app "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/pp-flowhub`

统一命令入口：选择 Python 运行时并分发 assistant/order/inventory 子命令。

- **L1 · 脚本过程** `scripts/pp-flowhub "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/test-macos-ui`

编译并运行 Swift/macOS 源码契约与 UI 回归测试。

- **L1 · 脚本过程** `scripts/test-macos-ui "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/test-release`

正式发布测试门禁：串联 Python、Swift UI 和工作簿测试。

- **L1 · 脚本过程** `scripts/test-release "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `scripts/test-workbook-e2e`

用固定样本执行 Traveler/材料工作簿端到端验证。

- **L1 · 脚本过程** `scripts/test-workbook-e2e "$@"` — 封装 `<顶层入口>` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$@：命令行参数`
  - 返回：`进程退出码`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · Shell 函数** `search_text(位置参数)` — 封装 `search_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$1…：位置参数`
  - 返回：`进程状态`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L17 · Shell 函数** `search_text(位置参数)` — 封装 `search_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`$1…：位置参数`
  - 返回：`进程状态`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_command_router.py`

自动化测试：验证 `command_router` 模块或业务场景。

- **L14 · 类** `LocalCommandRouterTests` — 定义 `LocalCommandRouterTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 方法** `LocalCommandRouterTests.test_common_phrasings_are_zero_token_commands()` — 验证与 `test_common_phrasings_are_zero_token_commands` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L20 · 方法** `LocalCommandRouterTests.test_spoken_mixed_digits_are_normalized_before_routing()` — 验证与 `test_spoken_mixed_digits_are_normalized_before_routing` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L26 · 方法** `LocalCommandRouterTests.test_stock_comparison_has_priority_over_order_preview()` — 验证订单、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L32 · 方法** `LocalCommandRouterTests.test_write_commands_require_approval()` — 验证与 `test_write_commands_require_approval` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L56 · 方法** `LocalCommandRouterTests.test_manual_hardware_gateway_stops_at_preview_without_approval()` — 验证五金、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `execute_local_command`；是否真实写入仍取决于分支和参数。

- **L75 · 方法** `LocalCommandRouterTests.test_stock_comparison_uses_database_order_facts()` — 验证数据库、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `execute_local_command`；是否真实写入仍取决于分支和参数。

- **L88 · 方法** `LocalCommandRouterTests.test_cut_to_size_commands_use_the_cut_to_size_source()` — 验证来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pp_folder.mkdir`, `cs_folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L101 · 方法** `LocalCommandRouterTests.test_missing_order_reports_the_directory_actually_searched()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `root.mkdir`；是否真实写入仍取决于分支和参数。

- **L111 · 方法** `LocalCommandRouterTests.test_unrecognized_text_requests_agent()` — 验证与 `test_unrecognized_text_requests_agent` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L114 · 方法** `LocalCommandRouterTests.test_agent_factory_suffix_is_rebuilt_only_when_present_in_user_text()` — 验证工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L140 · 方法** `LocalCommandRouterTests.test_split_order_factory_name_is_not_mixed_into_base_order()` — 验证订单、工厂单、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L146 · 方法** `LocalCommandRouterTests.test_gateway_rejects_unknown_tools()` — 验证与 `test_gateway_rejects_unknown_tools` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `execute_local_command`；是否真实写入仍取决于分支和参数。

## `tests/test_core.py`

自动化测试：验证 `core` 模块或业务场景。

- **L19 · 类** `CoreTests` — 定义 `CoreTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L20 · 方法** `CoreTests.test_aimes_bulk_defaults_to_50_but_exact_lookup_has_no_bulk_limit()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L36 · 方法** `CoreTests.test_name_normalization()` — 验证名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L40 · 方法** `CoreTests.test_exact_aimes_verification_preserves_missing_rows_as_a_distinct_result()` — 验证AIMES 数据、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L59 · 方法** `CoreTests.test_recent_fetch_and_exact_verification_share_one_lookup_session()` — 验证与 `test_recent_fetch_and_exact_verification_share_one_lookup_session` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L98 · 方法** `CoreTests.test_settings_load_only_runtime_paths_and_cutoff()` — 验证设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L114 · 方法** `CoreTests.test_invalid_cutoff_date_is_rejected()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L122 · 方法** `CoreTests.test_server_profile_uses_production_paths_when_active_source_is_local()` — 验证Server 数据、生产、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L139 · 方法** `CoreTests.test_aimes_username_is_loaded_without_loading_a_password()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L148 · 方法** `CoreTests.test_local_profile_derives_all_isolated_paths()` — 验证与 `test_local_profile_derives_all_isolated_paths` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

- **L159 · 方法** `CoreTests.test_operation_log_setting_is_loaded_and_defaults_to_enabled()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'settings.json').write_text`；是否真实写入仍取决于分支和参数。

## `tests/test_costing.py`

自动化测试：验证 `costing` 模块或业务场景。

- **L14 · 类** `CostingTests` — 定义 `CostingTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 方法** `CostingTests._config(root: Path) -> Config` — 封装 `_config` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`root: Path`
  - 返回：`Config`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_replace_product_database`；是否真实写入仍取决于分支和参数。

- **L29 · 方法** `CostingTests.test_order_total_uses_order_material_summary_and_raw_quantities()` — 验证订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_costing.py:15` `CostingTests._config`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`, `workbook.close`；是否真实写入仍取决于分支和参数。

- **L66 · 方法** `CostingTests.test_missing_cost_price_is_not_treated_as_zero()` — 验证成本相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_costing.py:15` `CostingTests._config`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L84 · 方法** `CostingTests.test_display_lines_use_material_business_order_and_aggregate_hardware()` — 验证材料、订单、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_costing.py:85` `CostingTests.test_display_lines_use_material_business_order_and_aggregate_hardware.line`

- **L85 · 方法** `CostingTests.test_display_lines_use_material_business_order_and_aggregate_hardware.line(category, code, name, quantity, factory = '材料汇总', unit = 'pcs', price = 1.0)` — 封装 `line` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`category`；`code`；`name`；`quantity`；`factory = '材料汇总'`；`unit = 'pcs'`；`price = 1.0`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_inventory.py`

自动化测试：验证 `inventory` 模块或业务场景。

- **L66 · 类** `_FakeNodeInput` — 定义 `_FakeNodeInput` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L69 · 方法** `_FakeNodeInput.__init__()` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L73 · 方法** `_FakeNodeInput.write(value)` — 写入与 `write` 对应的数据或步骤。
  - 输入：`value`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L77 · 方法** `_FakeNodeInput.close()` — 关闭与 `close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L81 · 类** `_FakeNodeProcess` — 定义 `_FakeNodeProcess` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L84 · 方法** `_FakeNodeProcess.__init__(result = None, timeout = None)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`result = None`；`timeout = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:66` `_FakeNodeInput`

- **L94 · 方法** `_FakeNodeProcess.wait(timeout = None)` — 封装 `wait` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`timeout = None`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L100 · 方法** `_FakeNodeProcess.kill()` — 封装 `kill` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L114 · 函数** `make_traveler(path: Path, items)` — 创建Traveler相关数据或步骤。
  - 输入：`path: Path`；`items`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L171 · 函数** `make_catalog(path: Path)` — 创建商品目录相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L188 · 函数** `make_priced_catalog(path: Path)` — 创建商品目录相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L198 · 类** `InventoryTests` — 定义与库存相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L199 · 方法** `InventoryTests.test_database_outbound_blocks_multiple_base_server_material_sources()` — 验证数据库、出库、Server 数据、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L222 · 方法** `InventoryTests.test_shipment_without_hardware_marks_status_without_inventory_document()` — 验证五金、状态、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(config.state_dir / 'inventory').mkdir`, `store.connection.execute`, `store.commit`, `store.close`, `mark_no_hardware_outbound`, `sqlite3.connect(config.workflow_database).execute`；是否真实写入仍取决于分支和参数。

- **L253 · 方法** `InventoryTests.test_customer_supplied_outbound_marks_database_only_and_reopens_on_fact_change()` — 验证出库、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`, `database_outbound_fingerprint`, `mark_customer_supplied_outbound`, `connection.execute`, `_refresh_outbound_status`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L317 · 方法** `InventoryTests.test_hardware_scope_requires_actual_positive_hardware_facts()` — 验证五金、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `outbound_scope_decisions`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L338 · 方法** `InventoryTests.test_outbound_scope_read_returns_latest_relevant_saved_decision()` — 验证出库、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`, `outbound_scope_decisions`；是否真实写入仍取决于分支和参数。

- **L373 · 方法** `InventoryTests.test_cut_to_size_customer_supplied_material_stays_fact_but_is_not_outbound()` — 验证材料、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(config.state_dir / 'inventory').mkdir`, `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`, `sqlite3.connect(config.workflow_database).execute`；是否真实写入仍取决于分支和参数。

- **L415 · 方法** `InventoryTests.test_database_outbound_blocks_mismatched_factory_name_order_prefix()` — 验证数据库、出库、工厂单、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L438 · 方法** `InventoryTests.test_customer_supplied_scope_is_rejected_for_owned_order()` — 验证范围、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L452 · 方法** `InventoryTests.test_owned_order_rejects_even_normalized_outbound_scope_decision()` — 验证订单、出库、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.commit`, `store.close`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L466 · 方法** `InventoryTests.test_remainder_decision_allows_empty_order_without_opening_browser()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.commit`, `store.close`, `set_outbound_scope`；是否真实写入仍取决于分支和参数。

- **L483 · 方法** `InventoryTests.test_database_order_outbound_preview_maps_without_traveler_file()` — 验证数据库、订单、出库、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'inventory').mkdir`, `(state / 'inventory' / 'mappings.json').write_text`, `store.connection.execute`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L532 · 方法** `InventoryTests.test_order_context_source_no_longer_requires_traveler_gate()` — 验证订单、来源、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L612 · 方法** `InventoryTests.test_database_outbound_status_changes_when_persisted_order_data_changes()` — 验证数据库、出库、状态、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(state / 'inventory').mkdir`, `(state / 'inventory' / 'mappings.json').write_text`, `store.connection.execute`, `store.commit`, `store.close`, `_refresh_outbound_status`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L675 · 方法** `InventoryTests.test_inventory_page_detection_accepts_tenant_workbench_subdomain()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L686 · 方法** `InventoryTests.test_inventory_service_workbench_is_an_entry_page()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L692 · 方法** `InventoryTests.test_inventory_page_detection_still_rejects_login_and_non_inventory_urls()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L697 · 方法** `InventoryTests.test_jdy_cdp_cleanup_uses_playwright_browser_close()` — 验证与 `test_jdy_cdp_cleanup_uses_playwright_browser_close` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L707 · 方法** `InventoryTests.test_outbound_navigation_reuses_existing_list_and_opens_visible_menu_item()` — 验证出库、项目相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L752 · 方法** `InventoryTests.test_outbound_timeout_persists_completed_documents_before_retry()` — 验证出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L759 · 方法** `InventoryTests.test_jdy_outbound_uses_direct_edit_and_post_save_history_verification()` — 验证出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L771 · 方法** `InventoryTests.test_jdy_error_detail_explains_reused_page_menu_timeout()` — 验证与 `test_jdy_error_detail_explains_reused_page_menu_timeout` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L778 · 方法** `InventoryTests.test_outbound_preview_hides_bottom_write_note()` — 验证出库、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L782 · 方法** `InventoryTests.test_outbound_preview_rows_are_full_row_clickable_and_scroll_independently()` — 验证出库、预览、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L810 · 方法** `InventoryTests.test_order_dashboard_outbound_refresh_and_panel_color_layout_contract()` — 验证订单、看板、出库、颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L824 · 方法** `InventoryTests.test_server_hardware_choice_highlights_selected_action()` — 验证Server 数据、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L836 · 方法** `InventoryTests.test_inventory_chrome_success_result_has_no_hidden_login_prompt()` — 验证库存、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L842 · 方法** `InventoryTests.test_order_preview_materials_can_be_mapped_for_stock_check()` — 验证订单、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog.parent.mkdir`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L862 · 方法** `InventoryTests.test_jdy_runtime_uses_portable_overrides_and_rejects_missing_dependencies()` — 验证与 `test_jdy_runtime_uses_portable_overrides_and_rejects_missing_dependencies` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `node.parent.mkdir`, `(modules / 'playwright').mkdir`, `(modules / 'playwright-core').mkdir`；是否真实写入仍取决于分支和参数。

- **L889 · 方法** `InventoryTests.test_stock_requirements_default_to_materials_and_can_include_hardware()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L906 · 方法** `InventoryTests.test_stock_check_compares_required_and_available_quantities()` — 验证与 `test_stock_check_compares_required_and_available_quantities` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog.parent.mkdir`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L934 · 方法** `InventoryTests.test_cut_to_size_folder_status_can_be_reconciled()` — 验证文件夹、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L954 · 方法** `InventoryTests.test_online_catalog_update_exports_validates_and_installs()` — 验证商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_catalog_online`, `loaded.close`；是否真实写入仍取决于分支和参数。

- **L959 · 方法** `InventoryTests.test_online_catalog_update_exports_validates_and_installs.fake_export(_config, action, **kwargs)` — 封装 `fake_export` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_config`；`action`；`**kwargs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`

- **L977 · 方法** `InventoryTests.test_catalog_import_persists_cost_price_and_keeps_missing_price_null()` — 验证商品目录、成本相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:188` `make_priced_catalog`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.close`, `loaded.close`；是否真实写入仍取决于分支和参数。

- **L1000 · 方法** `InventoryTests.test_catalog_change_summary_reports_added_updated_and_removed_products()` — 验证商品目录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1015 · 方法** `InventoryTests.test_catalog_change_summary_detects_cost_price_change()` — 验证商品目录、成本相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1024 · 方法** `InventoryTests.test_close_inventory_chrome_uses_dedicated_cdp_action()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `close_inventory_chrome`；是否真实写入仍取决于分支和参数。

- **L1042 · 方法** `InventoryTests.test_lazy_traveler_listing_reports_existing_catalog_status()` — 验证Traveler、商品目录、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`

- **L1057 · 方法** `InventoryTests.test_catalog_refresh_keeps_only_latest_xlsx_backup()` — 验证商品目录、备份相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `inventory_dir.mkdir`, `old_backup.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1076 · 方法** `InventoryTests.test_runtime_product_search_uses_database_after_xlsx_is_removed()` — 验证数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `catalog.parent.mkdir`, `catalog.unlink`, `loaded.close`；是否真实写入仍取决于分支和参数。

- **L1090 · 方法** `InventoryTests.test_browser_error_preserves_specific_reason()` — 验证与 `test_browser_error_preserves_specific_reason` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1097 · 方法** `InventoryTests.test_multiline_browser_error_keeps_first_specific_reason()` — 验证与 `test_multiline_browser_error_keeps_first_specific_reason` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1105 · 方法** `InventoryTests.test_login_failure_hides_full_page_dump_and_explains_retry()` — 验证与 `test_login_failure_hides_full_page_dump_and_explains_retry` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1116 · 方法** `InventoryTests.test_security_challenge_error_explains_visible_login_recovery()` — 验证与 `test_security_challenge_error_explains_visible_login_recovery` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1125 · 方法** `InventoryTests.test_profile_lock_failure_is_reported_as_retryable()` — 验证与 `test_profile_lock_failure_is_reported_as_retryable` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1135 · 方法** `InventoryTests.test_browser_runtime_noise_does_not_hide_specific_export_timeout()` — 验证与 `test_browser_runtime_noise_does_not_hide_specific_export_timeout` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1146 · 方法** `InventoryTests.test_run_jdy_passes_attachable_chrome_endpoint()` — 验证与 `test_run_jdy_passes_attachable_chrome_endpoint` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:81` `_FakeNodeProcess`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1171 · 方法** `InventoryTests.test_run_jdy_reuses_existing_inventory_page_without_reading_keychain()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:81` `_FakeNodeProcess`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1200 · 方法** `InventoryTests.test_inventory_operation_journal_reuses_confirmed_production_across_retry_batch_numbers()` — 验证库存、操作、生产相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `journal.update`；是否真实写入仍取决于分支和参数。

- **L1235 · 方法** `InventoryTests.test_inventory_operation_journal_resumes_after_partial_document_confirmation()` — 验证库存、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `journal.update`；是否真实写入仍取决于分支和参数。

- **L1264 · 方法** `InventoryTests.test_open_inventory_chrome_launches_dedicated_profile_and_debug_port()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open_inventory_chrome`；是否真实写入仍取决于分支和参数。

- **L1282 · 方法** `InventoryTests.test_open_inventory_chrome_does_not_launch_second_browser_on_login_page()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `open_inventory_chrome`；是否真实写入仍取决于分支和参数。

- **L1295 · 方法** `InventoryTests.test_outbound_stops_before_browser_when_material_mapping_is_missing()` — 验证出库、材料、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `traveler.parent.mkdir`, `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1311 · 方法** `InventoryTests.test_database_shipped_factory_is_hard_blocked()` — 验证数据库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `assert_factory_orders_outbound_allowed`；是否真实写入仍取决于分支和参数。

- **L1335 · 方法** `InventoryTests.test_database_shipped_factory_with_changed_data_can_be_updated()` — 验证数据库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `assert_factory_orders_outbound_allowed`；是否真实写入仍取决于分支和参数。

- **L1363 · 方法** `InventoryTests.test_run_jdy_converts_browser_timeout_to_actionable_rule_error()` — 验证与 `test_run_jdy_converts_browser_timeout_to_actionable_rule_error` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:81` `_FakeNodeProcess`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run_jdy`；是否真实写入仍取决于分支和参数。

- **L1380 · 方法** `InventoryTests.test_keychain_timeout_is_reported_as_credentials_error()` — 验证与 `test_keychain_timeout_is_reported_as_credentials_error` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `helper.write_text`；是否真实写入仍取决于分支和参数。

- **L1395 · 方法** `InventoryTests.test_parse_dynamic_regions_and_zero()` — 验证与 `test_parse_dynamic_regions_and_zero` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`

- **L1404 · 方法** `InventoryTests.test_fixed_mapping_and_push_open_expansion()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1425 · 方法** `InventoryTests.test_factory_selection_keeps_order_materials_and_selected_hardware_only()` — 验证工厂单、订单、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`, `set`；是否真实写入仍取决于分支和参数。

- **L1452 · 方法** `InventoryTests.test_zero_quantity_items_are_not_outbound_rows()` — 验证数量、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1467 · 方法** `InventoryTests.test_unique_exact_inventory_name_maps_bls36()` — 验证库存、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1484 · 方法** `InventoryTests.test_ignored_material_requires_reason_and_is_visible()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1497 · 方法** `InventoryTests.test_edge_quantity_is_rounded_half_up_for_inventory()` — 验证数量、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1510 · 方法** `InventoryTests.test_manual_edge_mapping_also_rounds_quantity_for_inventory()` — 验证映射、数量、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1531 · 方法** `InventoryTests.test_edge_prefers_matching_color_abs_banding_with_24mm_suffix()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1552 · 方法** `InventoryTests.test_back_panel_8mm_and_9mm_are_bidirectional_aliases()` — 验证与 `test_back_panel_8mm_and_9mm_are_bidirectional_aliases` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`；`tests/test_inventory.py:114` `make_traveler`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `mappings.write_text`；是否真实写入仍取决于分支和参数。

- **L1569 · 方法** `InventoryTests.test_ignored_mapping_can_be_saved_and_removed()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_ignored`；是否真实写入仍取决于分支和参数。

- **L1581 · 方法** `InventoryTests.test_source_codes_are_not_treated_as_inventory_skus()` — 验证来源、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set_ignored_mapping`；是否真实写入仍取决于分支和参数。

- **L1602 · 方法** `InventoryTests.test_lower_rail_names_resolve_to_l_rail_sku()` — 验证与 `test_lower_rail_names_resolve_to_l_rail_sku` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1621 · 方法** `InventoryTests.test_repair_hardware_collapses_lower_rail_pair_rows()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `connection.executemany`, `connection.commit`, `connection.close`, `sqlite3.connect(config.workflow_database).execute`；是否真实写入仍取决于分支和参数。

- **L1655 · 方法** `InventoryTests.test_ignoring_hardware_removes_existing_database_facts()` — 验证五金、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.executemany`, `connection.commit`, `connection.close`, `set_ignored_mapping`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L1698 · 方法** `InventoryTests.test_manual_mapping_can_be_saved_and_replaces_ignore()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mappings.save_ignored`, `InventoryMappings(path).save_manual`；是否真实写入仍取决于分支和参数。

- **L1708 · 方法** `InventoryTests.test_manual_mapping_can_be_viewed_updated_and_removed()` — 验证映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `save_manual_mapping`, `update_manual_mapping`；是否真实写入仍取决于分支和参数。

- **L1722 · 方法** `InventoryTests.test_sync_status_changes_with_traveler_fingerprint()` — 验证状态、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mapping_path.write_text`, `store.save_success`；是否真实写入仍取决于分支和参数。

- **L1743 · 方法** `InventoryTests.test_order_material_outbound_links_only_selected_split_factories()` — 验证订单、材料、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`；`tests/test_inventory.py:1783` `InventoryTests.test_order_material_outbound_links_only_selected_split_factories.preview`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.connection.execute`, `store.commit`, `store.close`, `OutboundItem`, `sync.save_success`, `sqlite3.connect(config.workflow_database).execute`, `connection.execute`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L1783 · 方法** `InventoryTests.test_order_material_outbound_links_only_selected_split_factories.preview(factory_order)` — 预览预览相关数据或步骤。
  - 输入：`factory_order`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1869 · 方法** `InventoryTests.test_production_material_outbound_does_not_mark_factory_orders_shipped()` — 验证生产、材料、出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `OutboundItem`, `sync.save_success`, `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1949 · 方法** `InventoryTests.test_split_production_material_document_cleans_stale_factory_links()` — 验证生产、材料、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `OutboundItem`, `sync.save_success`, `connection.execute`, `connection.commit`, `connection.close`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L2046 · 方法** `InventoryTests.test_previous_hardware_block_becoming_empty_requires_manual_void()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`；`tests/test_inventory.py:171` `make_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `mapping_path.write_text`, `store.save_success`；是否真实写入仍取决于分支和参数。

- **L2072 · 方法** `InventoryTests.test_hardware_shipment_ignores_previous_order_material_document()` — 验证五金、订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sync_path.parent.mkdir`, `sync_path.write_text`, `OutboundItem`；是否真实写入仍取决于分支和参数。

- **L2119 · 方法** `InventoryTests.test_outbound_status_prefers_factory_hardware_over_order_material_record()` — 验证出库、状态、工厂单、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `_refresh_outbound_status`, `_has_factory_hardware_outbound_record`；是否真实写入仍取决于分支和参数。

- **L2153 · 方法** `InventoryTests.test_sqlite_outbound_record_uses_sync_kind_for_hardware_reconciliation()` — 验证出库、记录、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `connection.execute`, `connection.commit`, `connection.close`, `sync_path.write_text`, `_load_outbound_records`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L2237 · 方法** `InventoryTests.test_same_hardware_name_is_aggregated_within_factory()` — 验证五金、名称、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:114` `make_traveler`

## `tests/test_macos_ui.swift`

自动化测试：验证 `macos_ui` 模块或业务场景。

- **L4 · 类** `OperationLogHarnessModel` — 定义与操作、日志相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L7 · 初始化器** `init(steps: [InventoryStep])` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`steps: [InventoryStep]`
  - 返回：`所属类型`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L12 · 结构体** `OperationLogHarnessView` — 定义与操作、日志相关的结构体，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 类** `HeaderBoundaryProbeBox` — 定义 `HeaderBoundaryProbeBox` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L25 · 结构体** `HeaderBoundaryProbe` — 定义 `HeaderBoundaryProbe` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L28 · 方法** `func makeNSView(context: Context) -> NSView` — 创建与 `makeNSView` 对应的数据或步骤。
  - 输入：`context: Context`
  - 返回：`NSView`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L34 · 方法** `func updateNSView(_ nsView: NSView, context: Context)` — 更新与 `updateNSView` 对应的数据或步骤。
  - 输入：`_ nsView: NSView`；`context: Context`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L39 · 结构体** `PageLayoutHarness` — 定义 `PageLayoutHarness` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L43 · 计算属性** `var body: some View` — 根据当前状态计算并返回`body` 对应的数据或界面状态。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`some View`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:25` `HeaderBoundaryProbe`

- **L64 · 结构体** `MacOSUIRegressionTests` — 定义 `MacOSUIRegressionTests` 结构体，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L65 · 方法** `static func main()` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1183` `MacOSUIRegressionTests.testInventoryTravelerNewestFirst`；`tests/test_macos_ui.swift:104` `MacOSUIRegressionTests.testPushToTalkShortcut`；`tests/test_macos_ui.swift:110` `MacOSUIRegressionTests.testSpeechCommandCanonicalization`；`tests/test_macos_ui.swift:116` `MacOSUIRegressionTests.testAssistantOrderResultParsing`；`tests/test_macos_ui.swift:137` `MacOSUIRegressionTests.testAssistantCompactHelpAndCancelRules`；`tests/test_macos_ui.swift:145` `MacOSUIRegressionTests.testMaterialDisplayNames`；`tests/test_macos_ui.swift:217` `MacOSUIRegressionTests.testOrderDetailMaterialRows`；`tests/test_macos_ui.swift:245` `MacOSUIRegressionTests.testOrderDashboardRules`；`tests/test_macos_ui.swift:982` `MacOSUIRegressionTests.testPendingInventorySourceFolderPath`；`tests/test_macos_ui.swift:1000` `MacOSUIRegressionTests.testPendingMaterialMappingIssueRoute`；`tests/test_macos_ui.swift:1032` `MacOSUIRegressionTests.testOrderOutboundFactorySelection`；`tests/test_macos_ui.swift:1084` `MacOSUIRegressionTests.testProductionFeedbackAndDashboardProgress`；另有 23 个直接调用
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `testOrderOutboundFactorySelection`, `testServerWriteMaterialPreviewOrdering`, `testServerWriteHardwareChangeLayout`；是否真实写入仍取决于分支和参数。

- **L104 · 方法** `private static func testPushToTalkShortcut()` — 验证与 `testPushToTalkShortcut` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L110 · 方法** `private static func testSpeechCommandCanonicalization()` — 验证与 `testSpeechCommandCanonicalization` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L116 · 方法** `private static func testAssistantOrderResultParsing()` — 验证订单、结果相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L137 · 方法** `private static func testAssistantCompactHelpAndCancelRules()` — 验证与 `testAssistantCompactHelpAndCancelRules` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L145 · 方法** `private static func testMaterialDisplayNames()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`；`tests/test_macos_ui.swift:182` `MacOSUIRegressionTests.material`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `inventoryCatalogUpdateSuccessStatus`, `inventoryCatalogUpdateFailureStatus`, `Set`；是否真实写入仍取决于分支和参数。

- **L182 · 方法** `func material(_ kind: String, _ thickness: Double, _ color: String = "") -> OrderMaterialPreview` — 封装材料相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ kind: String`；`_ thickness: Double`；`_ color: String = ""`
  - 返回：`OrderMaterialPreview`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L217 · 方法** `private static func testOrderDetailMaterialRows()` — 验证订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L245 · 方法** `private static func testOrderDashboardRules()` — 验证订单、看板相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openRequestedOrderIfAvailable`, `openOrderDetail`, `Set`；是否真实写入仍取决于分支和参数。

- **L982 · 方法** `private static func testPendingInventorySourceFolderPath()` — 验证库存、来源、文件夹、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1000 · 方法** `private static func testPendingMaterialMappingIssueRoute()` — 验证材料、映射、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1032 · 方法** `private static func testOrderOutboundFactorySelection()` — 验证订单、出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Set`, `orderDashboardOutboundDisplay`, `orderDashboardNeedsOutboundUpdateSelection`, `orderDashboardOutboundActionTitle`；是否真实写入仍取决于分支和参数。

- **L1084 · 方法** `private static func testProductionFeedbackAndDashboardProgress()` — 验证生产、看板、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `refreshDashboardAfterServerWrite`；是否真实写入仍取决于分支和参数。

- **L1183 · 方法** `private static func testInventoryTravelerNewestFirst()` — 验证库存、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1853` `MacOSUIRegressionTests.traveler`；`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1196 · 方法** `private static func testSharedPageHeaderHeight()` — 验证与 `testSharedPageHeaderHeight` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1220 · 方法** `private static func testAssistantOrderTimelineContract()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `openOrderCenter`；是否真实写入仍取决于分支和参数。

- **L1341 · 方法** `private static func testGlassDatePickerContract()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1385 · 方法** `private static func testTodoTableHeaderRoundedCorners()` — 验证待办相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1408 · 方法** `private static func testSettingsDefaultWindowLayoutContract()` — 验证设置相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1498 · 方法** `private static func testInventoryActionLayoutRules()` — 验证库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`；`tests/test_macos_ui.swift:1514` `MacOSUIRegressionTests.preview`

- **L1514 · 方法** `func preview(_ name: String, _ section: String) -> InventoryPreviewRow` — 预览预览相关数据或步骤。
  - 输入：`_ name: String`；`_ section: String`
  - 返回：`InventoryPreviewRow`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1543 · 方法** `private static func testRunningProgressReusesOperationRow()` — 验证进度、操作、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1885` `MacOSUIRegressionTests.fail`；`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1557 · 方法** `private static func testDashboardInventoryProgressText()` — 验证看板、库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1579 · 方法** `private static func testInventoryProgressKeepsStageHistory()` — 验证库存、进度相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1590 · 方法** `private static func testDashboardSeparatesInventoryAndRefreshTiming()` — 验证看板、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1616 · 方法** `private static func testOrderOperationDurationFormatting()` — 验证订单、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1621 · 方法** `private static func testServerWriteMaterialPreviewOrdering()` — 验证Server 数据、材料、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `ServerWriteMaterialChange`, `sortedServerWriteMaterialChanges`；是否真实写入仍取决于分支和参数。

- **L1638 · 方法** `private static func testServerWriteHardwareChangeLayout()` — 验证Server 数据、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1644 · 方法** `private static func testProductionOrderPaths()` — 验证生产、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1655 · 方法** `private static func testStockFailureKeepsManualRetryEnabled()` — 验证与 `testStockFailureKeepsManualRetryEnabled` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1670 · 方法** `private static func testExistingTravelerCanBeUpdatedAfterPreviewFailure()` — 验证Traveler、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderUpdateActionReady`；是否真实写入仍取决于分支和参数。

- **L1685 · 方法** `private static func testDashboardTravelerActionsUseDatabaseFacts()` — 验证看板、Traveler、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `orderTravelerOpenActionReady`；是否真实写入仍取决于分支和参数。

- **L1698 · 方法** `private static func testRelatedPreviewMissingMaterialIssue()` — 验证预览、材料、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1714 · 方法** `private static func testPP0067MissingMaterialShowsPrompt()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1885` `MacOSUIRegressionTests.fail`；`tests/test_macos_ui.swift:1877` `MacOSUIRegressionTests.pumpRunLoop`；`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`；是否真实写入仍取决于分支和参数。

- **L1735 · 方法** `private static func testFullPageHeaderBoundaryAlignment()` — 验证与 `testFullPageHeaderBoundaryAlignment` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1744` `MacOSUIRegressionTests.headerBoundaryY`；`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1744 · 方法** `private static func headerBoundaryY(flexibleContent: Bool) -> CGFloat` — 封装 `headerBoundaryY` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`flexibleContent: Bool`
  - 返回：`CGFloat`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:21` `HeaderBoundaryProbeBox`；`tests/test_macos_ui.swift:39` `PageLayoutHarness`；`tests/test_macos_ui.swift:1877` `MacOSUIRegressionTests.pumpRunLoop`；`tests/test_macos_ui.swift:1885` `MacOSUIRegressionTests.fail`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L1763 · 方法** `private static func testOperationLogScrollsAfterAppending()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1865` `MacOSUIRegressionTests.step`；`tests/test_macos_ui.swift:4` `OperationLogHarnessModel`；`tests/test_macos_ui.swift:12` `OperationLogHarnessView`；`tests/test_macos_ui.swift:1877` `MacOSUIRegressionTests.pumpRunLoop`；`tests/test_macos_ui.swift:1869` `MacOSUIRegressionTests.firstScrollView`；`tests/test_macos_ui.swift:1885` `MacOSUIRegressionTests.fail`；`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`；`tests/test_inventory.py:77` `_FakeNodeInput.close`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `pumpRunLoop`, `close`；是否真实写入仍取决于分支和参数。

- **L1814 · 方法** `private static func testOperationLogReader()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`

- **L1824 · 方法** `private static func testOperationLogMaintenance()` — 验证操作、日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_inventory.py:73` `_FakeNodeInput.write`；`tests/test_macos_ui.swift:1881` `MacOSUIRegressionTests.require`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write`；是否真实写入仍取决于分支和参数。

- **L1853 · 方法** `private static func traveler(_ name: String, folder: String, modifiedAt: String) -> InventoryTraveler` — 封装Traveler相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ name: String`；`folder: String`；`modifiedAt: String`
  - 返回：`InventoryTraveler`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1865 · 方法** `private static func step(_ index: Int) -> InventoryStep` — 封装 `step` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ index: Int`
  - 返回：`InventoryStep`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1869 · 方法** `private static func firstScrollView(in view: NSView) -> NSScrollView?` — 封装 `firstScrollView` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`in view: NSView`
  - 返回：`NSScrollView?`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1877 · 方法** `private static func pumpRunLoop(for seconds: TimeInterval)` — 封装 `pumpRunLoop` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`for seconds: TimeInterval`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `run`；是否真实写入仍取决于分支和参数。

- **L1881 · 方法** `private static func require(_ condition: @autoclosure () -> Bool, _ message: String)` — 封装 `require` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ condition: @autoclosure () -> Bool`；`_ message: String`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_macos_ui.swift:1885` `MacOSUIRegressionTests.fail`

- **L1885 · 方法** `private static func fail(_ message: String) -> Never` — 封装 `fail` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`_ message: String`
  - 返回：`Never`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_operation_log.py`

自动化测试：验证 `operation_log` 模块或业务场景。

- **L10 · 类** `OperationLogTests` — 定义与操作、日志相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L11 · 方法** `OperationLogTests.test_append_log_has_timestamp_and_never_stores_sensitive_values()` — 验证日志相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L26 · 方法** `OperationLogTests.test_disabled_logger_does_not_create_or_append_file()` — 验证文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_operation_log`；是否真实写入仍取决于分支和参数。

- **L32 · 方法** `OperationLogTests.test_database_trace_records_operation_shape_without_bound_values()` — 验证数据库、操作相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_order_details.py`

自动化测试：验证 `order_details` 模块或业务场景。

- **L12 · 类** `OrderDetailsTests` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L13 · 方法** `OrderDetailsTests.test_panel_projection_uses_one_color_image_identity_across_thicknesses()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `OrderIndexStore(config.workflow_database).close`, `_replace_product_database`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

## `tests/test_order_index.py`

自动化测试：验证 `order_index` 模块或业务场景。

- **L73 · 类** `OrderIndexTests` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L75 · 方法** `OrderIndexTests._set_permanent_server_policy(store, order_id, folder)` — 设置Server 数据相关数据或步骤。
  - 输入：`store`；`order_id`；`folder`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.save_server_scan_policy`；是否真实写入仍取决于分支和参数。

- **L84 · 方法** `OrderIndexTests.test_desktop_cs004_and_pp0072_are_offline_memory_preview_fixtures()` — 验证预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L107 · 方法** `OrderIndexTests.test_server_preview_summarizes_changes_and_excludes_shipped_factory_orders()` — 验证Server 数据、预览、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `current.upsert_order`, `current.upsert_factory`, `current.connection.execute`, `current.commit`, `current.close`, `preview.upsert_order`, `preview.upsert_factory`, `preview.connection.executemany`, `preview.connection.execute`；是否真实写入仍取决于分支和参数。

- **L211 · 方法** `OrderIndexTests.test_server_preview_requires_factory_confirmation_before_production_write()` — 验证Server 数据、预览、工厂单、生产相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `stale.upsert_order`, `stale.upsert_factory`, `stale.connection.execute`, `stale.commit`, `stale.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L281 · 方法** `OrderIndexTests.test_selected_server_folder_validation_does_not_touch_other_aimes_orders()` — 验证Server 数据、文件夹、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `store.upsert_order`, `store.connection.execute`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L338 · 方法** `OrderIndexTests.test_server_preview_uses_recut_board_as_increment_and_base_fittings_only()` — 验证Server 数据、预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `current.upsert_order`, `current.upsert_factory`, `current.connection.execute`, `current.commit`, `current.close`；是否真实写入仍取决于分支和参数。

- **L458 · 方法** `OrderIndexTests.test_server_confirmation_writes_materials_and_factory_hardware_after_mapping()` — 验证Server 数据、工厂单、五金、映射相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `current.upsert_order`, `current.upsert_factory`, `current.commit`, `current.close`, `InventoryMappings(config.workflow_database).save_manual`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L496 · 方法** `OrderIndexTests.test_server_confirmation_writes_materials_and_factory_hardware_after_mapping.resolve_items(current_config, pairs)` — 解析并确定与 `resolve_items` 对应的数据或步骤。
  - 输入：`current_config`；`pairs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L621 · 方法** `OrderIndexTests.test_cut_to_size_server_confirmation_can_skip_hardware_for_entire_order()` — 验证Server 数据、五金、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `current.upsert_order`, `current.commit`, `current.close`, `report.mkdir`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L652 · 方法** `OrderIndexTests.test_cut_to_size_server_confirmation_can_skip_hardware_for_entire_order.unresolved(current_config, pairs)` — 封装 `unresolved` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`current_config`；`pairs`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L715 · 方法** `OrderIndexTests.test_server_scan_blocks_material_preview_until_source_file_is_fixed()` — 验证Server 数据、材料、预览、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `material_path.write_bytes`；是否真实写入仍取决于分支和参数。

- **L777 · 方法** `OrderIndexTests.test_server_preview_validates_material_before_room_allocation()` — 验证Server 数据、预览、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L805 · 方法** `OrderIndexTests.test_server_material_allocation_splits_one_source_row_between_orders()` — 验证Server 数据、材料、来源、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.upsert_order`, `preview.upsert_factory`, `preview.connection.execute`, `preview.commit`, `preview.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L875 · 方法** `OrderIndexTests.test_server_material_allocation_ignores_stale_sqlite_row_ids()` — 验证Server 数据、材料、行数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `preview.upsert_order`, `preview.connection.execute`, `preview.commit`, `preview.close`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L947 · 方法** `OrderIndexTests.test_resolved_mapping_clears_stale_order_validation_error()` — 验证映射、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.connection.execute`, `set`, `store.close`；是否真实写入仍取决于分支和参数。

- **L977 · 方法** `OrderIndexTests.test_unresolved_mapping_keeps_order_validation_error()` — 验证映射、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1007 · 方法** `OrderIndexTests.test_aimes_stage_durations_exclude_aggregate_and_account_for_backend_overhead()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1023 · 方法** `OrderIndexTests.test_order_annotations_store_single_actual_installation_start_date()` — 验证订单、日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `save_order_annotations`, `reopened.upsert_order`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L1076 · 方法** `OrderIndexTests.test_order_annotations_reject_multiple_actual_installation_dates()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.commit`, `store.save_order_annotations`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1095 · 方法** `OrderIndexTests.test_order_index_collapses_historical_actual_installation_dates()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.connection.execute`, `store.connection.executemany`, `store.connection.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L1130 · 方法** `OrderIndexTests.test_order_annotations_allow_missing_installer_but_reject_duplicate_dates()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.commit`, `store.save_order_annotations`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1172 · 方法** `OrderIndexTests.test_server_folder_rename_requires_unique_identical_report_signature()` — 验证Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1186 · 方法** `OrderIndexTests.test_server_material_replacement_collapses_old_source_path_rows()` — 验证Server 数据、材料、来源、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `current_path.parent.mkdir`, `current_path.write_bytes`, `store.connection.execute`, `_replace_server_material_facts`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1223 · 方法** `OrderIndexTests.test_server_material_scope_retires_rows_from_previous_server_root()` — 验证Server 数据、材料、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1264 · 方法** `OrderIndexTests.test_prepared_sync_can_resolve_material_mappings_before_fittings_import_path()` — 验证材料、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `material.parent.mkdir`, `material.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1293 · 方法** `OrderIndexTests.test_server_read_trace_is_grouped_by_folder_and_file_kind()` — 验证Server 数据、文件夹、文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1310 · 方法** `OrderIndexTests.test_server_read_trace_limits_folder_examples()` — 验证Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1322 · 方法** `OrderIndexTests.test_server_scan_covers_owned_and_cut_to_size_roots()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `owned.mkdir`, `cut_to_size.mkdir`, `(owned / 'PP9999 materials.xlsx').write_bytes`, `(cut_to_size / 'CS999 materials.xlsx').write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1358 · 方法** `OrderIndexTests.test_successful_cut_to_size_preview_does_not_claim_optimization_without_aicnc_evidence()` — 验证预览相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1382 · 方法** `OrderIndexTests.test_cut_to_size_optimization_artifact_marks_status_when_material_is_absent()` — 验证状态、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `artifact.parent.mkdir`, `report.write_bytes`, `artifact.write_text`；是否真实写入仍取决于分支和参数。

- **L1412 · 方法** `OrderIndexTests.test_order_is_optimized_only_after_every_active_factory_has_aicnc_evidence()` — 验证订单、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `first.parent.mkdir`, `first.write_text`, `second.parent.mkdir`, `second.write_text`, `evidence_connection.execute`, `evidence_connection.close`；是否真实写入仍取决于分支和参数。

- **L1469 · 方法** `OrderIndexTests.test_visible_server_scan_refreshes_aicnc_evidence_and_returns_updated_orders()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `artifact.parent.mkdir`, `artifact.write_text`, `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1503 · 方法** `OrderIndexTests.test_exact_standard_order_folder_wins_over_mixed_factory_report_folder()` — 验证订单、文件夹、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `(mixed_folder / 'Report').mkdir`, `(mixed_folder / 'Report' / '板材清单.xlsx').write_bytes`, `exact_folder.mkdir`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1543 · 方法** `OrderIndexTests.test_cut_to_size_fittings_are_not_persisted_as_hardware()` — 验证五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / 'CS999 materials.xlsx').write_bytes`, `(folder / 'Fittingslist.xlsx').write_bytes`, `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1573 · 方法** `OrderIndexTests.test_incremental_sync_reuses_unchanged_server_report_and_rechecks_changes()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`；是否真实写入仍取决于分支和参数。

- **L1615 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / f'{name} materials.xlsx').write_bytes`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1616 · 类** `TrackingExecutor` — 定义 `TrackingExecutor` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1617 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.__init__(max_workers)` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`max_workers`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1620 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.__enter__()` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1623 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.__exit__(exc_type, exc_value, traceback)` — 管理所属对象的资源生命周期，确保进入、退出或销毁时正确收口。
  - 输入：`exc_type`；`exc_value`；`traceback`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1626 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor.map(function, folders)` — 封装 `map` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`function`；`folders`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1639 · 方法** `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.make_executor(max_workers)` — 创建与 `make_executor` 对应的数据或步骤。
  - 输入：`max_workers`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:1616` `OrderIndexTests.test_server_snapshot_uses_bounded_read_only_workers_and_preserves_records.TrackingExecutor`

- **L1667 · 方法** `OrderIndexTests.test_sync_index_reuses_scan_snapshot_and_reports_phase_durations()` — 验证与 `test_sync_index_reuses_scan_snapshot_and_reports_phase_durations` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1704 · 方法** `OrderIndexTests.test_prebaseline_temporary_folder_is_excluded_and_stale_pending_cleared()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_source_file`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L1742 · 方法** `OrderIndexTests.test_named_mixed_folder_is_not_marked_as_temporary()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L1757 · 方法** `OrderIndexTests.test_fully_shipped_mixed_folder_is_watched_then_reopened_by_aimes()` — 验证文件夹、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `store.commit`, `store.close`, `reopened.upsert_aimes_factory`, `reopened.commit`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L1805 · 方法** `OrderIndexTests.test_shipped_server_order_becomes_permanent_after_seven_day_watch()` — 验证Server 数据、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / 'PP9999 materials.xlsx').write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1839 · 方法** `OrderIndexTests.test_initial_date_orders_are_marked_shipped_without_fabricating_documents()` — 验证日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `old_folder.mkdir`, `factory_folder.mkdir`, `store.upsert_aimes_factory`, `store.upsert_order`, `store.connection.execute`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1881 · 方法** `OrderIndexTests.test_mark_temporary_folder_manual_starts_three_day_xml_watch()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `xml_root.mkdir`, `(xml_root / 'Optimize file.xml').write_text`, `(xml_root / 'layout file').mkdir`, `(xml_root / 'layout file' / 'nesting_result.xml').write_text`, `(folder / 'manual materials.xlsx').write_bytes`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L1913 · 方法** `OrderIndexTests.test_reportless_mixed_folder_requires_review()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L1928 · 方法** `OrderIndexTests.test_processed_temporary_folder_uses_three_day_xml_watch_then_is_permanent()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `xml.parent.mkdir`, `xml.write_text`, `(folder / 'material.xlsx').write_bytes`, `store.upsert_temporary_order`, `store.save_server_scan_xml_baseline`, `store.commit`, `store.close`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L1987 · 方法** `OrderIndexTests.test_failed_temporary_processing_remains_in_pending_server_changes()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `(folder / 'material.xlsx').write_bytes`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2020 · 方法** `OrderIndexTests.test_temporary_fittings_report_is_deferred_until_user_approves_processing()` — 验证与 `test_temporary_fittings_report_is_deferred_until_user_approves_processing` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `fittings.parent.mkdir`, `fittings.write_bytes`；是否真实写入仍取决于分支和参数。

- **L2036 · 方法** `OrderIndexTests.test_manual_temporary_outbound_records_server_baseline_case_insensitively()` — 验证出库、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `(folder / 'INSERTHOOD CABINET OLD CNC materials.xlsx').write_bytes`, `(report / 'Fittingslist.xlsx').write_bytes`, `(report / 'pp-板材清单-new.xlsx').write_bytes`, `record_temporary_outbound`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2073 · 方法** `OrderIndexTests.test_shipped_temporary_folder_is_skipped_without_report_rescan()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`, `xml.parent.mkdir`, `xml.write_text`, `record_temporary_outbound`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2110 · 方法** `OrderIndexTests.test_old_temporary_folder_is_filtered_before_report_rescan()` — 验证文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.parent.mkdir`, `report.write_bytes`；是否真实写入仍取决于分支和参数。

- **L2132 · 方法** `OrderIndexTests.test_temporary_processing_generates_material_traveler_and_outbounds()` — 验证材料、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`

- **L2160 · 方法** `OrderIndexTests.test_temporary_processing_can_skip_hardware_in_traveler_and_outbound()` — 验证五金、Traveler、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`

- **L2191 · 方法** `OrderIndexTests.test_temporary_folder_without_aimes_identity_uses_folder_name_everywhere()` — 验证文件夹、AIMES 数据、名称相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.close`；是否真实写入仍取决于分支和参数。

- **L2233 · 方法** `OrderIndexTests.test_temporary_outbound_is_not_repeated_when_folder_content_is_unchanged()` — 验证出库、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`

- **L2258 · 方法** `OrderIndexTests.test_failed_outbound_reuses_unchanged_generated_traveler_on_retry()` — 验证出库、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`

- **L2292 · 方法** `OrderIndexTests.test_temporary_folder_uses_unique_aimes_review_match_when_available()` — 验证文件夹、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`；`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.replace_aimes_review_rows`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2334 · 方法** `OrderIndexTests.test_factory_order_initial_date_cutoff_uses_embedded_date()` — 验证工厂单、订单、日期相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2340 · 方法** `OrderIndexTests.test_initial_date_removes_stale_ownership_issue_and_does_not_recreate_it()` — 验证日期、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_factory`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L2381 · 方法** `OrderIndexTests.test_server_change_message_identifies_order_factory_and_data()` — 验证Server 数据、订单、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2387 · 方法** `OrderIndexTests.test_server_change_message_explains_action_and_path()` — 验证Server 数据、路径相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2400 · 方法** `OrderIndexTests.test_invalid_and_test_aimes_rows_are_warnings_only()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2446 · 方法** `OrderIndexTests.test_aimes_factory_name_order_prefix_mismatch_is_a_warning()` — 验证AIMES 数据、工厂单、名称、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L2467 · 方法** `OrderIndexTests.test_fittings_factory_order_uses_order_folder_hint()` — 验证工厂单、订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2482 · 方法** `OrderIndexTests.test_unowned_factory_uses_exact_aimes_name_to_derive_order()` — 验证工厂单、AIMES 数据、名称、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2503 · 方法** `OrderIndexTests.test_existing_database_factory_skips_exact_aimes_lookup()` — 验证数据库、工厂单、AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2541 · 方法** `OrderIndexTests.test_active_issue_is_persisted_and_resolved()` — 验证待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_active_issue`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2559 · 方法** `OrderIndexTests.test_deleted_aimes_factory_is_audit_only_and_not_in_summaries()` — 验证AIMES 数据、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_aimes_factory`, `store.commit`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2584 · 方法** `OrderIndexTests.test_invalid_aimes_rows_are_transient_warnings_only()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2612 · 方法** `OrderIndexTests.test_exactly_verified_aimes_factory_is_persisted_as_aimes_identity()` — 验证AIMES 数据、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L2660 · 方法** `OrderIndexTests.test_business_errors_are_actionable_and_hide_technical_details()` — 验证与 `test_business_errors_are_actionable_and_hide_technical_details` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2675 · 方法** `OrderIndexTests.test_old_status_is_migrated_and_validation_reason_is_persisted()` — 验证状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.connection.execute`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L2709 · 方法** `OrderIndexTests.test_schema_migration_resolves_legacy_warning_from_unique_order_folder()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `source_folder.mkdir`, `store.upsert_factory`, `store.connection.execute`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L2738 · 方法** `OrderIndexTests.test_aimes_owner_wins_over_stale_server_owner()` — 验证AIMES 数据、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2761 · 方法** `OrderIndexTests.test_aimes_order_validation_and_test_filter()` — 验证AIMES 数据、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2782 · 方法** `OrderIndexTests.test_historical_pp_server_paths_are_in_dashboard_scope()` — 验证Server 数据、看板、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L2791 · 方法** `OrderIndexTests.test_summary_aggregates_factory_status()` — 验证工厂单、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2830 · 方法** `OrderIndexTests.test_standard_outbound_status_reconciles_and_survives_reopen()` — 验证出库、状态相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `reconcile_outbound_statuses`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L2871 · 方法** `OrderIndexTests.test_fully_shipped_order_is_completed_even_if_optimization_evidence_is_missing()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L2896 · 方法** `OrderIndexTests.test_grouped_outbound_document_reconciles_all_factory_orders_after_reindex()` — 验证出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`, `connection.execute`, `connection.commit`, `connection.close`, `_load_outbound_records`, `reconcile_outbound_statuses`；是否真实写入仍取决于分支和参数。

- **L2970 · 方法** `OrderIndexTests.test_order_level_outbound_record_is_not_broadcast_to_split_factories()` — 验证订单、出库、记录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `reconcile_outbound_statuses`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3003 · 方法** `OrderIndexTests.test_partial_factory_upsert_preserves_persisted_business_statuses()` — 验证工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_factory`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3035 · 方法** `OrderIndexTests.test_fully_shipped_aimes_order_is_not_a_server_scan_candidate()` — 验证AIMES 数据、订单、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_aimes_factory`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3061 · 方法** `OrderIndexTests.test_scan_does_not_parse_material_source_as_traveler_during_outbound_reconcile()` — 验证材料、来源、Traveler、出库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:75` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `workbook.save`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3111 · 方法** `OrderIndexTests.test_fully_shipped_folder_resolves_stale_material_validation_issue()` — 验证文件夹、材料、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:75` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `material_path.write_bytes`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3170 · 方法** `OrderIndexTests.test_fully_shipped_folder_resolves_stale_hardware_selection_issue()` — 验证文件夹、五金、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:75` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3228 · 方法** `OrderIndexTests.test_fully_shipped_folder_resolves_stale_order_validation_issue()` — 验证文件夹、订单、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:75` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`, `reopened.connection.execute`, `reopened.close`；是否真实写入仍取决于分支和参数。

- **L3286 · 方法** `OrderIndexTests.test_automatic_server_snapshot_skips_shipped_order_until_aimes_adds_factory()` — 验证Server 数据、订单、AIMES 数据、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `shipped_folder.mkdir`, `active_folder.mkdir`, `unindexed_folder.mkdir`, `(shipped_folder / 'PP9999 materials.xlsx').write_bytes`, `(active_folder / 'PP8888 materials.xlsx').write_bytes`, `(unindexed_folder / 'PP7777 materials.xlsx').write_bytes`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3352 · 方法** `OrderIndexTests.test_new_current_aimes_factory_reopens_server_scan_candidate()` — 验证AIMES 数据、工厂单、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `config.source_root.mkdir`, `(config.source_root / 'PP9999').mkdir`；是否真实写入仍取决于分支和参数。

- **L3378 · 方法** `OrderIndexTests.test_skipped_standard_order_does_not_resolve_its_old_issue()` — 验证订单、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_index.py:75` `OrderIndexTests._set_permanent_server_policy`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `config.source_root.mkdir`, `folder.mkdir`, `self._set_permanent_server_policy`, `store.upsert_active_issue`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3404 · 方法** `OrderIndexTests.test_orders_sort_by_latest_factory_split_time()` — 验证工厂单、时间相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3420 · 方法** `OrderIndexTests.test_summary_includes_confirmed_server_report_factory_assigned_to_normal_order()` — 验证Server 数据、工厂单、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_order`, `store.upsert_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3439 · 方法** `OrderIndexTests.test_aimes_if_needed_runs_once_per_day_after_success()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `config.source_root.mkdir`；是否真实写入仍取决于分支和参数。

- **L3472 · 方法** `OrderIndexTests.test_aimes_only_sync_reports_change_then_skips_after_daily_success()` — 验证AIMES 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L3501 · 方法** `OrderIndexTests.test_server_scan_is_non_mutating_until_full_processing()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `nesting.parent.mkdir`, `nesting.write_text`, `store.upsert_aimes_factory`, `store.commit`, `store.close`, `store.connection.execute`, `report.write_bytes`, `report.unlink`；是否真实写入仍取决于分支和参数。

- **L3612 · 方法** `OrderIndexTests.test_confirm_without_business_changes_only_updates_xml_scan_baseline()` — 验证与 `test_confirm_without_business_changes_only_updates_xml_scan_baseline` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `xml.parent.mkdir`, `xml.write_text`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3658 · 方法** `OrderIndexTests.test_server_scan_baseline_covers_both_server_roots()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `nesting.parent.mkdir`, `nesting.write_text`, `store.upsert_aimes_factory`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3698 · 方法** `OrderIndexTests.test_report_edits_are_ignored_by_xml_only_server_scan()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_aimes_factory`, `store.upsert_source_file`, `store.commit`, `store.close`, `materials.write_bytes`, `_record_generated_material_baseline`；是否真实写入仍取决于分支和参数。

- **L3743 · 方法** `OrderIndexTests.test_selected_server_folder_reuses_index_processing_for_one_folder()` — 验证Server 数据、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`, `store.upsert_order`, `store.commit`, `store.close`, `store.connection.execute`；是否真实写入仍取决于分支和参数。

- **L3771 · 方法** `OrderIndexTests.test_selected_non_order_folder_is_rejected_without_processing_children()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `child_order.mkdir`, `(child_order / 'material.xlsx').write_bytes`；是否真实写入仍取决于分支和参数。

- **L3786 · 方法** `OrderIndexTests.test_selected_non_order_folder_with_recognized_report_is_temporary_order()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `selected.mkdir`, `(selected / 'material.xlsx').write_bytes`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L3808 · 方法** `OrderIndexTests.test_scan_reports_unprocessed_non_order_folder_as_manual_only()` — 验证订单、文件夹相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `selected.mkdir`, `(selected / 'material.xlsx').write_bytes`；是否真实写入仍取决于分支和参数。

## `tests/test_order_workflow.py`

自动化测试：验证 `order_workflow` 模块或业务场景。

- **L45 · 函数** `make_materials(path: Path, order_id: str = 'PP9999', fractional: bool = False, edge: float = 12.5)` — 创建与 `make_materials` 对应的数据或步骤。
  - 输入：`path: Path`；`order_id: str = 'PP9999'`；`fractional: bool = False`；`edge: float = 12.5`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L67 · 函数** `make_board(path: Path, factory: str, name: str)` — 创建与 `make_board` 对应的数据或步骤。
  - 输入：`path: Path`；`factory: str`；`name: str`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L76 · 函数** `make_board_material_report(path: Path, factory: str = 'F100', name: str = 'PP9999-KITCHEN', plywood_qty: int = 2, panel_qty: int = 3, edge_qty: float = 12.5)` — 创建材料相关数据或步骤。
  - 输入：`path: Path`；`factory: str = 'F100'`；`name: str = 'PP9999-KITCHEN'`；`plywood_qty: int = 2`；`panel_qty: int = 3`；`edge_qty: float = 12.5`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `wb.save`；是否真实写入仍取决于分支和参数。

- **L101 · 函数** `make_fittings(path: Path, groups: list[tuple[str, float]])` — 创建与 `make_fittings` 对应的数据或步骤。
  - 输入：`path: Path`；`groups: list[tuple[str, float]]`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L122 · 函数** `make_rail_fittings(path: Path, left_quantity: float, right_quantity: float | None, left_name: str = 'Left Rail', right_name: str = 'Right Rail')` — 创建与 `make_rail_fittings` 对应的数据或步骤。
  - 输入：`path: Path`；`left_quantity: float`；`right_quantity: float | None`；`left_name: str = 'Left Rail'`；`right_name: str = 'Right Rail'`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L148 · 函数** `make_template(path: Path)` — 创建与 `make_template` 对应的数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L153 · 函数** `make_product_catalog(path: Path)` — 创建商品目录相关数据或步骤。
  - 输入：`path: Path`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L173 · 函数** `picking_layout_snapshot(sheet)` — 封装 `picking_layout_snapshot` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`sheet`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L200 · 类** `OrderWorkflowTests` — 定义与订单相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L201 · 方法** `OrderWorkflowTests.test_memory_server_confirmation_command_reads_json_from_stdin()` — 验证Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L223 · 方法** `OrderWorkflowTests.test_database_order_traveler_uses_sqlite_facts_without_source_material()` — 验证数据库、订单、Traveler、来源相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L291 · 方法** `OrderWorkflowTests.test_database_order_traveler_keeps_fifth_and_later_hardware_visible()` — 验证数据库、订单、Traveler、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.executemany`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L361 · 方法** `OrderWorkflowTests.test_database_order_traveler_writes_manual_hardware_to_accessory_section()` — 验证数据库、订单、Traveler、五金相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.connection.execute`, `store.connection.executemany`, `store.connection.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L443 · 方法** `OrderWorkflowTests.test_legacy_traveler_gets_usage_list_and_material_from_picking_list()` — 验证Traveler、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `local_order.mkdir`, `workbook.save`, `target.mkdir`；是否真实写入仍取决于分支和参数。

- **L495 · 方法** `OrderWorkflowTests.test_missing_material_can_be_generated_from_report_summary()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`

- **L528 · 方法** `OrderWorkflowTests.test_generated_material_color_table_aggregates_repeated_report_colors()` — 验证材料、颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`

- **L562 · 方法** `OrderWorkflowTests.test_complex_report_generation_requests_manual_material()` — 验证材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:76` `make_board_material_report`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L576 · 方法** `OrderWorkflowTests.test_local_test_source_is_repeatable_and_matches_server_layout()` — 验证来源、Server 数据相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sentinel.write_text`；是否真实写入仍取决于分支和参数。

- **L604 · 方法** `OrderWorkflowTests.test_usage_list_expands_and_rewrites_summary_formulas()` — 验证与 `test_usage_list_expands_and_rewrites_summary_formulas` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L649 · 方法** `OrderWorkflowTests.test_usage_list_normalizes_alias_color_before_color_table_formulas()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L686 · 方法** `OrderWorkflowTests.test_order_folders_are_sorted_by_modified_time_descending()` — 验证订单、时间相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `folder.mkdir`；是否真实写入仍取决于分支和参数。

- **L707 · 方法** `OrderWorkflowTests.test_cut_to_size_requires_materials_workbook()` — 验证与 `test_cut_to_size_requires_materials_workbook` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `order.mkdir`；是否真实写入仍取决于分支和参数。

- **L718 · 方法** `OrderWorkflowTests.test_cut_to_size_generates_materials_only_traveler()` — 验证Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:101` `make_fittings`；`tests/test_order_workflow.py:148` `make_template`；`tests/test_order_workflow.py:173` `picking_layout_snapshot`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `order.mkdir`, `untouched.save`, `set`；是否真实写入仍取决于分支和参数。

- **L790 · 方法** `OrderWorkflowTests.test_source_component_code_is_not_written_as_sku()` — 验证来源、编码相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:67` `make_board`；`tests/test_order_workflow.py:101` `make_fittings`；`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`；是否真实写入仍取决于分支和参数。

- **L818 · 方法** `OrderWorkflowTests.test_opt_out_hardware_omits_report_fittings_from_traveler()` — 验证五金、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:67` `make_board`；`tests/test_order_workflow.py:101` `make_fittings`；`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`；是否真实写入仍取决于分支和参数。

- **L848 · 方法** `OrderWorkflowTests.test_invalid_empty_dimension_returns_one_business_error()` — 验证与 `test_invalid_empty_dimension_returns_one_business_error` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `Workbook().save`, `payload.replace`；是否真实写入仍取决于分支和参数。

- **L864 · 方法** `OrderWorkflowTests.test_equal_rail_pair_is_collapsed_but_mismatch_stops_read()` — 验证与 `test_equal_rail_pair_is_collapsed_but_mismatch_stops_read` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:122` `make_rail_fittings`

- **L895 · 方法** `OrderWorkflowTests.test_equal_rail_pair_preview_consumes_canonical_quantity()` — 验证预览、数量相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:67` `make_board`；`tests/test_order_workflow.py:122` `make_rail_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`；是否真实写入仍取决于分支和参数。

- **L916 · 方法** `OrderWorkflowTests.test_single_color_materials_and_integer_validation()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`

- **L929 · 方法** `OrderWorkflowTests.test_single_color_materials_keep_edge_when_panel_is_zero()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L948 · 方法** `OrderWorkflowTests.test_repairs_empty_single_color_table_from_detail_rows_without_changing_details()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L993 · 方法** `OrderWorkflowTests.test_repairs_missing_color_table_colors_and_rebuilds_all_summary_formulas()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1033 · 方法** `OrderWorkflowTests.test_preview_includes_material_color_table_repair_warning()` — 验证预览、材料、颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `order.mkdir`, `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1056 · 方法** `OrderWorkflowTests.test_repair_aggregates_repeated_detail_color_rows()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1083 · 方法** `OrderWorkflowTests.test_existing_complete_color_table_mismatch_requires_manual_handling()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1101 · 方法** `OrderWorkflowTests.test_eight_color_table_is_read_without_seven_color_limit_error()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`, `set`；是否真实写入仍取决于分支和参数。

- **L1133 · 方法** `OrderWorkflowTests.test_integer_display_format_uses_the_total_qty_values_excel_shows()` — 验证与 `test_integer_display_format_uses_the_total_qty_values_excel_shows` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L1157 · 方法** `OrderWorkflowTests.test_material_detail_quantity_requires_color()` — 验证材料、数量、颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1171 · 方法** `OrderWorkflowTests.test_total_qty_and_color_table_must_match_before_material_write()` — 验证颜色、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `workbook.save`；是否真实写入仍取决于分支和参数。

- **L1195 · 方法** `OrderWorkflowTests.test_formula_without_cached_values_uses_display_values_for_totals_and_color_table()` — 验证颜色相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L1223 · 方法** `OrderWorkflowTests.test_integer_display_format_is_also_used_for_room_rows()` — 验证与 `test_integer_display_format_is_also_used_for_room_rows` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `wb.save`；是否真实写入仍取决于分支和参数。

- **L1239 · 方法** `OrderWorkflowTests.test_room_section_factory_name_extracts_exact_order_and_rejects_ambiguous_rows()` — 验证工厂单、名称、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L1262 · 方法** `OrderWorkflowTests.test_related_update_reports_the_specific_order_error()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_related_orders`；是否真实写入仍取决于分支和参数。

- **L1278 · 方法** `OrderWorkflowTests.test_related_update_response_keeps_all_orders_and_factories()` — 验证与 `test_related_update_response_keeps_all_orders_and_factories` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `update_related_orders`；是否真实写入仍取决于分支和参数。

- **L1306 · 方法** `OrderWorkflowTests.test_duplicate_fittings_use_newest_and_tied_conflict_stops()` — 验证与 `test_duplicate_fittings_use_newest_and_tied_conflict_stops` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:101` `make_fittings`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `older.parent.mkdir`, `newer.parent.mkdir`；是否真实写入仍取决于分支和参数。

- **L1326 · 方法** `OrderWorkflowTests.test_empty_malformed_fittings_is_skipped_and_traveler_can_generate()` — 验证Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:67` `make_board`；`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `workbook.save`, `empty.save`；是否真实写入仍取决于分支和参数。

- **L1377 · 方法** `OrderWorkflowTests.test_global_ignore_and_generate_one_order_workbook()` — 验证订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:67` `make_board`；`tests/test_order_workflow.py:101` `make_fittings`；`tests/test_order_workflow.py:148` `make_template`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report_a.mkdir`, `report_b.mkdir`, `set_ignored`, `set_ignored_mapping`, `wb.save`, `materials_wb.save`, `update_order_traveler`；是否真实写入仍取决于分支和参数。

- **L1479 · 方法** `OrderWorkflowTests.test_ignored_hardware_is_not_persisted_when_order_is_rescanned()` — 验证五金、订单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:67` `make_board`；`tests/test_order_workflow.py:101` `make_fittings`；`tests/test_order_workflow.py:153` `make_product_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `connection.execute`, `connection.close`, `set_ignored`；是否真实写入仍取决于分支和参数。

- **L1514 · 方法** `OrderWorkflowTests.test_add_manual_hardware_writes_database_and_aggregates_same_sku()` — 验证五金、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:45` `make_materials`；`tests/test_order_workflow.py:67` `make_board`；`tests/test_order_workflow.py:101` `make_fittings`；`tests/test_order_workflow.py:153` `make_product_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `report.mkdir`, `index.connection.execute`, `index.connection.commit`, `index.close`, `traveler.parent.mkdir`, `traveler.write_text`, `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L1615 · 方法** `OrderWorkflowTests.test_manual_hardware_accepts_factory_number_without_traveler()` — 验证五金、工厂单、Traveler相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_order_workflow.py:153` `make_product_catalog`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `index.close`, `connection.close`；是否真实写入仍取决于分支和参数。

## `tests/test_production.py`

自动化测试：验证 `production` 模块或业务场景。

- **L19 · 类** `ProductionTransactionTests` — 定义与生产相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L21 · 方法** `ProductionTransactionTests._create_product_table(connection)` — 创建与 `_create_product_table` 对应的数据或步骤。
  - 输入：`connection`
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.executemany`；是否真实写入仍取决于分支和参数。

- **L45 · 方法** `ProductionTransactionTests.test_production_preview_aggregates_duplicate_order_material_rows()` — 验证生产、预览、订单、材料相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.executemany`, `store.commit`, `store.close`；是否真实写入仍取决于分支和参数。

- **L82 · 方法** `ProductionTransactionTests.test_production_preview_deducts_legacy_inventory_materials()` — 验证生产、预览、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：`tests/test_production.py:21` `ProductionTransactionTests._create_product_table`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.executemany`, `store.commit`, `store.close`, `(config.state_dir / 'inventory-outbound-records.json').write_text`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L205 · 方法** `ProductionTransactionTests.test_prepare_production_is_read_only_until_inventory_succeeds()` — 验证生产、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `store.commit`, `store.close`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L257 · 方法** `ProductionTransactionTests.test_completed_production_can_share_the_local_commit()` — 验证生产相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `record_completed_production`, `connection.commit`, `connection.execute`, `connection.close`；是否真实写入仍取决于分支和参数。

## `tests/test_runtime_store.py`

自动化测试：验证 `runtime_store` 模块或业务场景。

- **L13 · 类** `RuntimeStoreTests` — 定义 `RuntimeStoreTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L14 · 方法** `RuntimeStoreTests.test_runtime_database_uses_a_private_file()` — 验证数据库、文件相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L19 · 方法** `RuntimeStoreTests.test_unknown_database_version_is_not_deleted()` — 验证数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L30 · 方法** `RuntimeStoreTests.test_assistant_usage_does_not_touch_workflow_database()` — 验证数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.execute`, `connection.commit`, `connection.close`；是否真实写入仍取决于分支和参数。

- **L54 · 方法** `RuntimeStoreTests.test_agent_usage_has_week_month_and_total_summaries()` — 验证与 `test_agent_usage_has_week_month_and_total_summaries` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.record_agent_usage`；是否真实写入仍取决于分支和参数。

- **L63 · 方法** `RuntimeStoreTests.test_agent_route_is_learned_as_an_exact_normalized_phrase()` — 验证与 `test_agent_route_is_learned_as_an_exact_normalized_phrase` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L73 · 方法** `RuntimeStoreTests.test_learned_command_preserves_typed_arguments()` — 验证与 `test_learned_command_preserves_typed_arguments` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_security.py`

自动化测试：验证 `security` 模块或业务场景。

- **L14 · 类** `CredentialSafetyTests` — 定义 `CredentialSafetyTests` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 方法** `CredentialSafetyTests.test_repository_contains_no_likely_credentials()` — 验证与 `test_repository_contains_no_likely_credentials` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L45 · 方法** `CredentialSafetyTests.test_sensitive_local_files_are_gitignored()` — 验证与 `test_sensitive_local_files_are_gitignored` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

## `tests/test_workflow_database.py`

自动化测试：验证 `workflow_database` 模块或业务场景。

- **L14 · 类** `WorkflowDatabaseTests` — 定义与数据库相关的类，集中保存数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L15 · 方法** `WorkflowDatabaseTests.test_grouped_outbound_document_migrates_to_factory_links()` — 验证出库、工厂单相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.commit`, `connection.close`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L68 · 方法** `WorkflowDatabaseTests.test_material_table_migrates_to_order_scope_and_removes_allocations()` — 验证材料、订单、范围相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `connection.commit`, `connection.close`, `connection.execute`；是否真实写入仍取决于分支和参数。

- **L110 · 方法** `WorkflowDatabaseTests.test_legacy_order_database_migrates_without_reading_inventory_database()` — 验证订单、数据库、库存相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `state.mkdir`, `connection.execute`, `connection.commit`, `connection.close`, `legacy_inventory.parent.mkdir`；是否真实写入仍取决于分支和参数。

- **L140 · 方法** `WorkflowDatabaseTests.test_one_factory_order_gets_one_batch_and_conflict_raises_open_issue()` — 验证工厂单、订单、待处理问题相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `store.upsert_aimes_factory`, `store.update_source_file_identity`, `store.record_batch_evidence`, `store.commit`, `store.connection.execute`, `store.close`；是否真实写入仍取决于分支和参数。

- **L155 · 方法** `WorkflowDatabaseTests.test_backup_status_requires_user_action_without_successful_record()` — 验证备份、状态、记录相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L162 · 方法** `WorkflowDatabaseTests.test_retention_keeps_recent_daily_and_sunday_weekly_backups()` — 验证与 `test_retention_keeps_recent_daily_and_sunday_weekly_backups` 对应的数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L183 · 方法** `WorkflowDatabaseTests.test_perform_backup_uses_local_database_backup_directory()` — 验证备份、数据库相关数据或步骤。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `sqlite3.connect(destination).execute`；是否真实写入仍取决于分支和参数。

## `tools/aimes_lookup.mjs`

通过浏览器自动化查询 AIMES 工厂单名称和近期订单。

- **L9 · 函数** `safePageURL()` — 封装 `safePageURL` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L18 · 函数** `log(message, details = {})` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`message`；`details = {}`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L24 · 函数** `recordStage(stage, label, startedAt)` — 记录记录相关数据或步骤。
  - 输入：`stage`；`label`；`startedAt`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/aimes_lookup.mjs:18` `log`

## `tools/generate_code_reference.py`

静态扫描一方源码，生成中文文件地图和符号索引。

- **L269 · 类** `Symbol` — 定义 `Symbol` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L283 · 函数** `tracked_files() -> list[str]` — 封装 `tracked_files` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `subprocess.run`；是否真实写入仍取决于分支和参数。

- **L291 · 函数** `split_words(name: str) -> list[str]` — 封装 `split_words` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L298 · 函数** `translated_subject(name: str) -> str` — 封装 `translated_subject` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`name: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:291` `split_words`

- **L309 · 函数** `symbol_purpose(symbol: Symbol) -> str` — 封装 `symbol_purpose` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`symbol: Symbol`
  - 返回：`str`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:298` `translated_subject`

- **L336 · 函数** `file_purpose(path: str) -> str` — 封装文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L387 · 函数** `annotation_text(node: ast.expr | None) -> str` — 封装 `annotation_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.expr | None`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L397 · 函数** `python_parameter_text(node: ast.FunctionDef | ast.AsyncFunctionDef) -> list[str]` — 封装 `python_parameter_text` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.FunctionDef | ast.AsyncFunctionDef`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:387` `annotation_text`

- **L426 · 类** `DirectCallVisitor` — 定义 `DirectCallVisitor` 类，集中保存该领域的数据和行为边界。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`未声明`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L429 · 方法** `DirectCallVisitor.__init__(root: ast.AST) -> None` — 初始化所属类型，把传入参数转换为后续方法可使用的状态。
  - 输入：`root: ast.AST`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L433 · 方法** `DirectCallVisitor.visit_FunctionDef(node: ast.FunctionDef) -> None` — 封装 `visit_FunctionDef` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.FunctionDef`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L439 · 方法** `DirectCallVisitor.visit_Lambda(node: ast.Lambda) -> None` — 封装 `visit_Lambda` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.Lambda`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L442 · 方法** `DirectCallVisitor.visit_ClassDef(node: ast.ClassDef) -> None` — 封装 `visit_ClassDef` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.ClassDef`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L446 · 方法** `DirectCallVisitor.visit_Call(node: ast.Call) -> None` — 封装 `visit_Call` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`node: ast.Call`
  - 返回：`None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L456 · 函数** `python_symbols(path: Path) -> list[Symbol]` — 封装 `python_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:463` `python_symbols.walk`

- **L463 · 方法** `python_symbols.walk(body: Iterable[ast.stmt], parents: list[str]) -> None` — 封装 `walk` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`body: Iterable[ast.stmt]`；`parents: list[str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:463` `python_symbols.walk`；`tools/generate_code_reference.py:397` `python_parameter_text`；`tools/generate_code_reference.py:387` `annotation_text`；`tools/generate_code_reference.py:426` `DirectCallVisitor`

- **L523 · 函数** `line_number(source: str, offset: int) -> int` — 封装 `line_number` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source: str`；`offset: int`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L528 · 函数** `declaration_end(source: str, start: int) -> int` — 封装 `declaration_end` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`source: str`；`start: int`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L564 · 函数** `matching_brace(source: str, opening: int) -> int` — 匹配与 `matching_brace` 对应的数据或步骤。
  - 输入：`source: str`；`opening: int`
  - 返回：`int`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L622 · 函数** `swift_parameter_list(signature: str) -> list[str]` — 封装 `swift_parameter_list` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`signature: str`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L646 · 函数** `swift_return_type(signature: str, raw_kind: str) -> str` — 封装 `swift_return_type` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`signature: str`；`raw_kind: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L671 · 函数** `swift_symbols(path: Path) -> list[Symbol]` — 封装 `swift_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:523` `line_number`；`tools/generate_code_reference.py:564` `matching_brace`；`tools/generate_code_reference.py:528` `declaration_end`；`tools/generate_code_reference.py:646` `swift_return_type`；`tools/generate_code_reference.py:693` `swift_symbols.container_name`；`tools/generate_code_reference.py:622` `swift_parameter_list`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `set`；是否真实写入仍取决于分支和参数。

- **L693 · 方法** `swift_symbols.container_name(offset: int) -> str | None` — 封装名称相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`offset: int`
  - 返回：`str | None`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L750 · 函数** `js_symbols(path: Path) -> list[Symbol]` — 封装 `js_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:564` `matching_brace`；`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:523` `line_number`

- **L772 · 函数** `shell_symbols(path: Path) -> list[Symbol]` — 封装 `shell_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:269` `Symbol`；`tools/generate_code_reference.py:564` `matching_brace`；`tools/generate_code_reference.py:523` `line_number`

- **L794 · 函数** `project_source_paths(files: list[str]) -> list[Path]` — 封装来源相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`files: list[str]`
  - 返回：`list[Path]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L805 · 函数** `collect_symbols(files: list[str]) -> list[Symbol]` — 封装 `collect_symbols` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`files: list[str]`
  - 返回：`list[Symbol]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:794` `project_source_paths`；`tools/generate_code_reference.py:456` `python_symbols`；`tools/generate_code_reference.py:671` `swift_symbols`；`tools/generate_code_reference.py:750` `js_symbols`；`tools/generate_code_reference.py:772` `shell_symbols`；`tools/generate_code_reference.py:269` `Symbol`

- **L824 · 函数** `resolve_calls(symbols: list[Symbol]) -> None` — 解析并确定与 `resolve_calls` 对应的数据或步骤。
  - 输入：`symbols: list[Symbol]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:291` `split_words`

- **L870 · 函数** `markdown_escape(value: str) -> str` — 标记与 `markdown_escape` 对应的数据或步骤。
  - 输入：`value: str`
  - 返回：`str`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `value.replace('`', "'").replace`, `value.replace`；是否真实写入仍取决于分支和参数。

- **L875 · 函数** `render_symbol(symbol: Symbol) -> list[str]` — 封装 `render_symbol` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`symbol: Symbol`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:870` `markdown_escape`；`tools/generate_code_reference.py:309` `symbol_purpose`

- **L892 · 函数** `write_text(path: Path, lines: list[str]) -> None` — 写入与 `write_text` 对应的数据或步骤。
  - 输入：`path: Path`；`lines: list[str]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:892` `write_text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `path.parent.mkdir`, `path.write_text`；是否真实写入仍取决于分支和参数。

- **L898 · 函数** `render_file_map(files: list[str], symbols: list[Symbol], git_tracked_count: int) -> None` — 封装文件相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`files: list[str]`；`symbols: list[Symbol]`；`git_tracked_count: int`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:336` `file_purpose`；`tools/generate_code_reference.py:892` `write_text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_text`；是否真实写入仍取决于分支和参数。

- **L951 · 函数** `reference_header(title: str, scope: str, count: int) -> list[str]` — 封装 `reference_header` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`title: str`；`scope: str`；`count: int`
  - 返回：`list[str]`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L969 · 函数** `render_reference(path: Path, title: str, scope: str, symbols: list[Symbol]) -> None` — 封装 `render_reference` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`path: Path`；`title: str`；`scope: str`；`symbols: list[Symbol]`
  - 返回：`None`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:951` `reference_header`；`tools/generate_code_reference.py:336` `file_purpose`；`tools/generate_code_reference.py:875` `render_symbol`；`tools/generate_code_reference.py:892` `write_text`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `write_text`；是否真实写入仍取决于分支和参数。

- **L983 · 函数** `main() -> int` — 解析命令行参数，建立运行配置并分发到对应业务动作。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`int`
  - 静态可确认的项目内下一跳：`tools/generate_code_reference.py:283` `tracked_files`；`tools/generate_code_reference.py:805` `collect_symbols`；`tools/generate_code_reference.py:824` `resolve_calls`；`tools/generate_code_reference.py:898` `render_file_map`；`tools/generate_code_reference.py:969` `render_reference`

## `tools/jdy_inventory.mjs`

通过浏览器自动化读取库存、填单并执行金蝶云出库。

- **L13 · 函数** `safePageURL()` — 封装 `safePageURL` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：无显式参数（可能读取所属对象状态）
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L22 · 函数** `log(message, details = {})` — 封装日志相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`message`；`details = {}`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L29 · 函数** `timed(label, operation)` — 封装 `timed` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`label`；`operation`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:22` `log`

- **L49 · 函数** `timedWait(page, milliseconds, label)` — 封装 `timedWait` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`milliseconds`；`label`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L52 · 函数** `exact(page, text)` — 封装 `exact` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L60 · 函数** `clickVisibleText(page, text)` — 封装 `clickVisibleText` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L71 · 函数** `clickVisibleTextAcrossFrames(page, text)` — 封装 `clickVisibleTextAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:60` `clickVisibleText`

- **L77 · 函数** `visibleTextLocatorsAcrossFrames(page, text)` — 封装 `visibleTextLocatorsAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L88 · 函数** `visibleLeftNavigationLocators(page, text)` — 封装 `visibleLeftNavigationLocators` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L97 · 函数** `waitForVisibleLeftNavigationItem(page, text, timeoutMs = UI_STEP_TIMEOUT)` — 封装项目相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`；`timeoutMs = UI_STEP_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:88` `visibleLeftNavigationLocators`

- **L112 · 函数** `waitForVisibleTextAcrossFrames(page, text, timeoutMs = UI_STEP_TIMEOUT)` — 封装 `waitForVisibleTextAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`text`；`timeoutMs = UI_STEP_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:77` `visibleTextLocatorsAcrossFrames`

- **L121 · 函数** `visiblePatternLocatorsAcrossFrames(page, pattern)` — 封装 `visiblePatternLocatorsAcrossFrames` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`pattern`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L132 · 函数** `waitForVisiblePatternToDisappear(page, pattern, timeoutMs = UI_STEP_TIMEOUT)` — 封装 `waitForVisiblePatternToDisappear` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`pattern`；`timeoutMs = UI_STEP_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:121` `visiblePatternLocatorsAcrossFrames`

- **L140 · 函数** `moveAndClick(label, locator)` — 封装 `moveAndClick` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`label`；`locator`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:29` `timed`

- **L144 · 函数** `waitForVisibleFrame(page, predicate, timeoutMs = 15000)` — 封装 `waitForVisibleFrame` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`predicate`；`timeoutMs = 15000`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L156 · 函数** `hasVisibleLocator(frame, selector)` — 封装 `hasVisibleLocator` 对应的辅助逻辑，供所属模块或类型复用。
  - 输入：`frame`；`selector`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L190 · 函数** `outboundSaveControlDiagnostics(currentPage, preferredFrame)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`currentPage`；`preferredFrame`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `visibleOutboundSaveControls`, `isOutboundSaveControlDisabled`；是否真实写入仍取决于分支和参数。

- **L214 · 函数** `waitForOutboundSaveControl(currentPage, preferredFrame, documentNumber)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`currentPage`；`preferredFrame`；`documentNumber`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:190` `outboundSaveControlDiagnostics`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `visibleOutboundSaveControls`, `isOutboundSaveControlDisabled`, `outboundSaveControlDiagnostics`；是否真实写入仍取决于分支和参数。

- **L308 · 函数** `assertOutboundFormMatchesRequest(frame, items, quantityColumnId)` — 强制校验出库相关数据或步骤。
  - 输入：`frame`；`items`；`quantityColumnId`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `outboundMaterialRows`, `replace`；是否真实写入仍取决于分支和参数。

- **L345 · 函数** `waitForOtherOutboundListFrame(page, timeoutMs = PAGE_NAVIGATION_TIMEOUT)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`timeoutMs = PAGE_NAVIGATION_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `hasOtherOutboundListControls`；是否真实写入仍取决于分支和参数。

- **L355 · 函数** `waitForOtherOutboundFormFrame(page, timeoutMs = PAGE_NAVIGATION_TIMEOUT)` — 封装出库相关的辅助逻辑，供所属模块或类型复用。
  - 输入：`page`；`timeoutMs = PAGE_NAVIGATION_TIMEOUT`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `isOtherOutboundFormFrame`；是否真实写入仍取决于分支和参数。

- **L392 · 函数** `openOtherOutboundMenuItem(page, label = "其他出库单")` — 打开出库、项目相关数据或步骤。
  - 输入：`page`；`label = "其他出库单"`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:97` `waitForVisibleLeftNavigationItem`；`tools/jdy_inventory.mjs:77` `visibleTextLocatorsAcrossFrames`

- **L473 · 函数** `applyOutboundDate(input, value)` — 应用出库、日期相关数据或步骤。
  - 输入：`input`；`value`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：未静态识别到一方函数调用；可能只做计算、调用系统/第三方 API，或通过动态类型分发

- **L482 · 函数** `findExactOutboundRows(listFrame, remark)` — 查找出库相关数据或步骤。
  - 输入：`listFrame`；`remark`
  - 返回：`Promise/JavaScript 值`
  - 静态可确认的项目内下一跳：`tools/jdy_inventory.mjs:473` `applyOutboundDate`
  - 副作用提示：检测到可能写库、写文件、启动进程或操作外部系统的调用 `applyOutboundDate`, `replace`；是否真实写入仍取决于分支和参数。
