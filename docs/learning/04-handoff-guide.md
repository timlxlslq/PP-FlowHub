# PP FlowHub 接手学习指南

本文面向已经了解项目业务流程、但还不熟悉 Python、SwiftUI、SQLite、命令行和 Excel 实现方式的开发者。

目标不是让读者记住每个文件，而是让读者能够回答以下问题：

1. 用户在 App 中做了一件事后，代码从哪里开始执行？
2. 哪一层负责解析、哪一层负责业务判断、哪一层负责写入？
3. 当前页面显示的数据来自哪个事实源？
4. 修改一个规则时，应该修改哪些代码、测试和文档？
5. 出错时，如何判断是界面状态、Python 进程、SQLite、Excel、Server 还是外部库存系统的问题？

## 一、推荐阅读顺序

建议按照下面的顺序阅读，不要一开始从最大的 Swift 或 Python 文件第一行读到最后一行。

| 顺序 | 文件或目录 | 学习目的 |
| --- | --- | --- |
| 1 | `README.md` | 了解项目定位、运行命令和依赖 |
| 2 | `docs/architecture/system-architecture.md` | 了解各层职责和边界 |
| 3 | `docs/architecture/pp-flowhub-data-model.md` | 了解中央 SQLite 和外部事实源 |
| 4 | `docs/business-rules.md` | 了解跨流程业务规则 |
| 5 | `docs/learning/01-complete-architecture-and-business-flow.md` | 按完整调用链学习主要功能 |
| 6 | 本文 | 使用入口函数和调试步骤阅读源码 |
| 7 | `tests/` | 用可执行测试确认自己的理解 |
| 8 | `docs/project-handoff-log.md` | 了解历史问题、修改原因和验证证据 |

`docs/learning/02-macos-code-signing-tcc.md` 和
`docs/learning/03-server-scan-performance-observation.md` 是专题材料，分别在阅读 macOS 集成和 Server 扫描时使用。

## 二、先建立一张“心智地图”

### 2.1 运行时结构

```text
用户输入文字或语音
        ↓
SwiftUI App
        ↓
scripts/pp-flowhub
        ↓
Python CLI 模块
        ↓
本地命令解析器 / Agent 路由
        ↓
Typed Tool Gateway
        ↓
确定性的 Python 业务函数
        ↓
SQLite、Excel、Server 文件夹、库存网页
```

这里的“层”可以理解为不同职责的边界：

- SwiftUI 是界面层：负责显示、输入、启动进程、接收进度和展示结果。
- `scripts/pp-flowhub` 是启动适配层：选择 Python、设置 `PYTHONPATH`，再转发到具体 CLI。
- 本地命令解析器负责把常用表达转换为结构化参数；它不应直接写真实系统。
- Agent 只处理本地解析器无法确定的模糊表达，并输出结构化路由。
- Gateway 是安全边界：检查动作、参数和审批状态，把请求分发到确定性业务函数。
- Python 业务模块负责真正的解析、计算、数据库操作和外部系统操作。
- SQLite 保存可恢复的业务事实和同步证据；它不是单纯的界面缓存。

### 2.2 最重要的边界

阅读任何函数时，都先问它属于下面哪一类：

| 类型 | 典型内容 | 修改时要关注 |
| --- | --- | --- |
| 展示状态 | SwiftUI 的 `@State`、列表、状态文字 | 是否只是显示，还是会触发真实操作 |
| 业务事实 | 订单、工厂单、材料、五金、出库记录 | 来源、身份、唯一性和持久化 |
| 外部证据 | AIMES、AICNC、金蝶、Server、库存网页 | 是否真的读取到，失败如何恢复 |
| 生成文件 | Traveler、材料工作簿、备份文件 | 模板结构、合并单元格、原子替换 |
| 用户意图 | 命令文本、Agent 结构化结果 | 不能直接当作已验证的业务事实 |

尤其不要把下面几件事混为一谈：

- 出库记录不等于生产记录。
- Traveler 是生成出来的工作文件，不是生产事实源。
- App 显示“完成”不等于外部库存系统已经成功写入。
- Agent 识别出的订单号或工厂单名称仍需本地代码重新校验。

## 三、按入口阅读源码

### 3.1 助手命令：最适合第一次跟读

从以下顺序开始：

```text
macos/AssistantView.swift
  → macos/TravelerAssistant.swift: runAssistantCommand
  → scripts/pp-flowhub assistant
  → traveler_assistant/assistant_cli.py: main
  → command_router.py: parse_local_command
  → tool_gateway.py: execute_local_command
  → order_workflow.py 或 inventory.py
```

重点理解：

1. Swift 如何用 `Process` 启动 Python 子进程。
2. Python 如何把结果序列化为标准输出 JSON。
3. 为什么常用命令优先走本地解析，不消耗 Agent Token。
4. 为什么写入动作第一次只返回 `approval_required`。
5. 为什么确认后仍要由 Gateway 重新检查，而不能相信 Agent 的权限判断。

可以先运行只读命令：

```bash
./scripts/pp-flowhub assistant "列出订单"
./scripts/pp-flowhub order list
```

阅读命令输出时，重点看 `status`、`result_type`、`error.code` 和进度事件，不要只看最后一行的人类提示。

### 3.2 订单中心和 Server 扫描

建议阅读顺序：

```text
macos/OrderDashboardView.swift
  → macos/TravelerAssistant.swift 中的订单加载/刷新函数
  → scripts/pp-flowhub order
  → traveler_assistant/order_index.py
  → traveler_assistant/order_workflow.py
  → data/workflow.sqlite3
```

`order_index.py` 主要维护订单索引、AIMES 同步、Server 扫描、问题记录、出库状态和同步证据；`order_workflow.py` 主要负责订单文件预览、材料解析、五金解析和 Traveler 生成。

第一次阅读 `order_index.py` 时，只关注这些入口和概念：

- `OrderIndexStore`：SQLite 连接和订单索引操作。
- `sync_aimes_index()`：同步 AIMES 工厂单事实。
- `scan_server()` / `process_server_folder()`：发现 Server 文件变化。
- `reconcile_outbound_statuses()`：根据当前工厂单和出库证据重新计算状态。
- `active_issues()`：统一待处理问题的读取入口。

不要试图一次理解所有私有辅助函数。遇到一个具体问题时，再沿着入口向下追踪到对应解析函数。

### 3.3 Traveler 生成

Traveler 的学习重点不是“如何写 Excel API”，而是理解事实如何进入模板：

```text
Server/AIMES/SQLite 事实
  → OrderPreview / FactoryPreview
  → openpyxl 读取模板
  → 写入 Usage List / Picking List / Purchase List
  → 临时文件保存并重新打开校验
  → 备份旧文件并原子替换
```

重点阅读：

- `order_workflow.py` 中的 `OrderPreview`、`FactoryPreview` 和 `PreviewFitting`。
- `parse_order_materials()`、`parse_fittings_groups()`。
- `generate_order_traveler()`、`update_order_traveler()`。
- `_write_picking_list()` 及其合并单元格处理。
- `inventory.py` 中的 `parse_traveler()`，理解生成端和读取端如何互相约束。

每次修改 Traveler 都要同时检查：工作表名称和顺序、合并单元格、样式、公式、空集合情况，以及重新打开后的内容。

### 3.4 库存查询和出库

```text
Traveler 或中央 SQLite
  → parse_traveler / database_stock_requirements
  → ProductDatabase / InventoryMappings
  → 库存预检
  → 用户确认
  → Playwright 或库存系统写入
  → 出库结果写回 SQLite
```

重点区分：

- 库存查询是只读流程，可以不经过 Agent。
- 出库是外部写入，必须经过预检和审批。
- 商品名称到商品编码的映射是独立事实，不能靠模糊匹配直接写入。
- 外部页面操作成功后，还要检查系统返回的单号或结果，再更新本地状态。

## 四、如何读一段具体代码

推荐使用下面的五步法：

### 第一步：找调用者

用搜索找到函数在哪里被调用：

```bash
rg -n "函数名" macos traveler_assistant tests
```

先确认它是被 UI、CLI、测试还是另一个业务函数调用。

### 第二步：确定输入和输出

观察：

- 参数是用户输入、数据库行、文件路径还是另一个领域对象。
- 返回值是展示 payload、业务对象、文件路径还是错误。
- 是否通过异常返回业务失败。

### 第三步：标记副作用

看到以下操作就要提高警惕：

- `connection.execute()`、`commit()`、`rollback()`。
- `Path.write_text()`、`Workbook.save()`、文件替换。
- `Process()`、Playwright、SMB 路径访问。
- `UserDefaults`、Keychain 或 Swift 状态更新。

这些操作决定了函数是不是只读，也决定了需要什么验证。

### 第四步：找不变量

不变量是修改后仍必须成立的条件，例如：

- 一个工厂单只能归属于一个批次。
- 同一工厂单的相同 SKU 和规格只能保留一个有效人工五金事实。
- 已出库工厂单不能再次进入普通出库选择。
- 没有工厂单的材料类订单仍要保留合法的空白模板结构。

### 第五步：找到对应测试

```bash
rg -n "函数名|业务关键词|错误码" tests
```

如果没有测试，先把行为写成测试或记录为未验证假设，再考虑修改实现。

## 五、代码注释应该写什么

后续补充源码注释时，遵循三种注释层次：

### 5.1 模块注释

说明：

- 模块属于哪一层。
- 它拥有哪类职责。
- 它不应该负责什么。
- 主要入口是什么。
- 是否有数据库、文件或外部系统副作用。

### 5.2 函数和类型注释

说明：

- 参数的业务含义，而不只是类型。
- 返回值如何被调用者使用。
- 重要错误码。
- 写入、备份、事务或外部调用行为。
- 必须满足的不变量。

### 5.3 关键算法旁的注释

只解释代码本身看不出来的“为什么”，例如：

- 为什么不能只使用订单号匹配工厂单。
- 为什么要按文件内容指纹，而不能只看修改时间。
- 为什么 `openpyxl.insert_rows()` 后还要移动合并区域。
- 为什么人工五金先写 SQLite，Traveler 要等用户明确生成。
- 为什么 Agent 的结果必须经过 Gateway 二次校验。

不要写这种注释：

```python
# 把 quantity 加 1
quantity += 1
```

它只是重复代码。应该解释业务原因，例如“同一工厂单中相同 SKU 的人工五金合并为一个有效事实，避免重复显示和重复出库”。

## 六、安全的学习和修改流程

每次准备修改时：

1. 先查看 `git status` 和 `git diff`，确认没有覆盖现有工作。
2. 先用只读命令、测试夹具和 SQLite 查询验证当前行为。
3. 写下“已确认事实、合理推测、未验证假设”。
4. 只修改一个清晰的业务边界。
5. 同步更新对应测试和学习文档。
6. 运行项目要求的测试；如果修改了源码或 App，还要执行构建和正式安装门禁。
7. 区分测试通过、构建成功、安装成功和真实外部系统行为。

学习阶段优先使用 `traveler_assistant/test_data.py` 和临时目录，不要直接拿真实 Server 文件夹或库存订单做实验。

## 七、推荐的第一批练习

按难度递增：

1. 阅读并运行 `order list`，找出订单列表的 JSON 入口。
2. 追踪一个 `preview` 命令，标记所有只读文件和数据库访问。
3. 阅读 `parse_local_command()`，为一种新的只读表达补测试。
4. 阅读 `ProductDatabase`，查询一个商品的编码、名称和规格。
5. 追踪人工五金的“预览 → 确认 → SQLite 校验”链路，但使用测试数据库。
6. 生成一个测试 Traveler，比较生成前后的工作表结构和关键单元格。
7. 阅读一个失败测试，说明失败发生在 UI、CLI、业务规则还是外部系统边界。

完成这些练习后，再进入 `order_index.py` 和 `inventory.py` 的大段实现，会容易很多。

## 八、当前文档和代码的维护约定

- 业务规则变化：更新 `docs/business-rules.md` 或 `docs/inventory-outbound-rules.md`。
- 架构边界变化：更新 `docs/architecture/` 和本文对应章节。
- 新的故障、修复和验证证据：更新 `docs/project-handoff-log.md`。
- 代码实现变化：更新相关测试和函数注释。
- 只讨论但尚未决定的需求：明确标记为待确认，不写成已经实现的规则。

这份指南描述的是阅读和维护方法，不替代业务规则、发布门禁或当前动态交接记录。
