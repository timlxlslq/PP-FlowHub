# 订单材料以 SKU 关联商品主资料

- 目标：`material_items` 保存订单、SKU、数量及来源元数据，以真实外键关联 `products(code)`；颜色、材料类型、厚度、单位、封边等商品属性从商品层读取。同步调整确认写入、详情、生产、库存、成本和 Traveler。
- 状态：实现、独立副本验收、全部发布测试阶段和一次串行构建已完成；等待用户手动解锁 Mac 后执行正式签名安装、正式库备份/迁移与安装版验收。GPT-6 负责规划、审查、最终测试和安装验收；GPT-5.6 Sol / high 负责实现及开发回归。正式库仍为旧结构，尚未应用 White Oak 映射或 SKU 迁移，不能将本状态视为正式交付。
- 约束：保留开始时所有未提交修改；不重建真实数据库、不改变订单数量或生产/出货状态、不执行外部库存操作；迁移先在数据库副本演练，再备份并事务迁移正式库。无法唯一匹配时整体停止并给出逐项诊断。
- 步骤：审计商品属性与引用者 → 明确商品属性契约及迁移方案 → Sol 修改 schema、读写、关联和回归 → 主代理审查/独立验收 → 完整发布门禁 → 串行构建、正式签名安装及安装版读写验收。
- 验证：旧库迁移、幂等、失败回滚、非法 SKU/父商品删除被外键阻止；材料确认写入并重开读取；商品属性 JOIN；映射改变不重绑已确认材料；生产剩余量、Server 预览/取消/重复确认、目录更新、成本和 Traveler；真实库副本与迁移前后按订单/SKU/来源核对。
- 剩余决策：无待用户选择的材料映射；唯一未匹配的 White Oak 封边已由用户确认 M1170。剩余工作是实现、错误路径验证和正式交付，不把副本通过当作正式库或安装版验收。

## 已确认的设计要求

1. `material_items.product_code` 必填且不得为空，引用 `products.code`；保留 `id/order_id/quantity/source_type/source_path/source_fingerprint/updated_at`。商品字段从材料表物理移除，读取层输出需要的属性，Swift 可继续消费相同字段名。
2. `products` 当前只有 `category/name/spec/unit`，需在商品层提供可明确解释的结构化材料属性。原始商品名称和规格保持可追溯；工作流名义厚度与外部规格差异须明确区分，不能使 Traveler 列分类或历史消耗失效。
3. SKU 只在源文件解析/确认和一次性旧数据迁移时确定。已确认材料的库存/成本读取使用保存的 SKU；全局映射变化不会重绑已有订单材料。
4. SQLite 外键在每条相关应用连接建立时启用，必须在事务开始前执行。仅在 DDL 声明外键不足以保证约束。参考 <https://www.sqlite.org/foreignkeys.html>。
5. 商品同步不能继续 `DELETE FROM products` 后全量插入。采用按 SKU 更新/插入；被订单或历史消耗引用的缺失商品保留并标明不可用于新库存写入，历史详情仍可读取。具体缺失状态需与现有启用校验一致。
6. 生产消耗需要稳定的 SKU 关联。历史已完成批次数量、单据快照和业务时间必须保留；禁止因为颜色/单位/厚度改由商品提供而把消耗重新计入可用数量。
7. Server 预览身份、分配记录、确认指纹需要覆盖 SKU，旧预览不得静默写入已经移除的列或按新映射重绑旧结果。
8. 用户追加范围：一并处理其他材料明细缺少 SKU 外键的表。包括 `manual_production_batch_materials`、`server_material_allocations`、`hardware_items`、`inventory_resolution_rules`。当前商品属性集中到商品层；来源名称/编码、真实数量换算依据、已执行外部单据和审计快照继续保留其历史证据职责。

## 初始证据与保护

- 开始时工作树已有优化确认、独立人工文件夹、五金预览、学习文档及 WeCom 实验修改；本任务叠加修改，最终基于开始时文件快照审查。
- 开始时真实库 `material_items` 113 行，已完成生产材料表 48 行；副本 `integrity_check=ok`、`foreign_key_check` 无记录。
- 开始时源文件快照和 SQLite Online Backup 位于 `/tmp/pp-flowhub-material-sku.BSIt8J/`；正式迁移前另建项目本地可恢复备份。
- 现场属性差异包括 Plywood 5.4/14.5 与商品规格 5.2/15、商品单位 SHT/ea/M 与旧材料 pcs/m，以及历史 edge 字段与 color 不一致。映射以现行权威解析规则和 source color 为依据，不使用过时 edge 字段猜测商品。
- 独立旧版解析审计：112/113 材料和 48/48 生产记录可唯一匹配；PP0086 White Oak 封边原有映射缺失，用户明确选择 `M1170` 天然白橡木皮封边条（0.45*22mm），迁移保持 263.95 数量。
- 扩大审计：101 行五金和现有人工映射均可连接到商品主表，无孤儿 SKU；材料分配表 10 行需增加 SKU 并迁移旧来源身份。
- 21 个订单的旧版详情、成本、库存需求读取已在隔离副本记录于 `/tmp/pp-flowhub-material-sku.BSIt8J/old-reads.json`，用于新版独立对照。旧版 PP0086 库存需求存在上述映射缺失，不能误报为新回归。

## 隔离验收进展（2026-09-16，尚非最终发布）

- 冻结旧代码和旧数据库，加上用户批准的 White Oak → M1170 映射后，生成 `approved-baseline-audit.json` 和 `approved-old-reads.json`；未调用外部库存写入。
- `migration-rehearsal-v2/workflow.sqlite3` 首次迁移与重复初始化均通过独立核对：534 项断言零失败。核对覆盖五表 SKU 外键、三表属性列物理移除、113 行订单材料身份/数量/来源、48 行历史生产消耗和 10 行 Server 分配，以及订单/工厂单/出库单据/五金事实未变。534 是断言数量，不是测试用例数量。
- 21 个订单的新版公开详情、成本和库存需求均能读取；新旧对照 127 项断言零失败，逐订单成本总额、库存 SKU 与需求数量相同。
- 新增契约回归已发现并交由实现代理修复：零数量解析行不应要求匹配 SKU；存储初始化不能在已有写事务期间用独立连接争抢写锁；商品属性锁定不能仅依赖当前订单材料，而遗漏历史生产消耗及分配引用。
- 以上证据针对当时工作树与隔离副本。代码稳定后需重新运行契约回归、最终迁移演练和完整发布门禁；正式迁移前重新备份并核对现场数据漂移。

## 冻结代码后的验收与交付阻碍（2026-09-16）

- Sol 完成五表迁移与相关读写代码，并修复 Server 分配 INSERT 列数、预览属性提交、事务锁、后改名称忽略影响已确认材料，以及旧出库原始名称指纹的兼容问题。`TravelerItem.product_code` 为显式字段，`source_snapshot()` 保持原五字段来源结构。
- 主代理最终副本 `migration-final/workflow.sqlite3` 首次迁移及重复初始化通过；534 项迁移断言全部通过，另外 28 张不应改变的表逐行相同，包含 `inventory_operations` 的尚未完成操作记录。
- 对未补 White Oak 映射的真实旧库副本执行失败迁移：明确拒绝 PP0086 White Oak，完整 SQLite dump（schema + 数据）迁移前后完全相同，证实失败整体回滚。
- 21 个订单的详情、成本、库存需求独立对照 127 项通过；出库状态、待提交单据的 `changed`、raw/mapped 指纹均与旧版一致。PP0070、PP0077 的既有重复 SKU 警告仍保留，本轮不擅自修复历史业务问题。
- `./scripts/test-release` 的 Python 阶段：353 tests，OK（1 项既有 Desktop fixture 环境跳过）。后续 UI 阶段首次被沙盒拒绝启动 Swift 宏插件（`sandbox_apply: Operation not permitted`），没有据此修改 Swift 源码；在获准的普通 macOS 环境重新运行 `test-macos-ui` 通过，然后 `test-aimes-table` 与 `test-workbook-e2e` 通过，`git diff --check` 通过。各发布阶段均已通过，但不伪称原 wrapper 首次运行退出码为 0。
- 一次串行 `./scripts/build-app` 成功，未签名产物：`/tmp/pp-flowhub-build/PP FlowHub.app`；Bundle Identifier：`com.pacificpride.ppflowhub`；打包 Node：v24.19.0。可执行文件 SHA-256：`8d9c027ad4edaadd958931481fc080ad8d862937a179ab33c401db90a6f9aa60`。
- 打包的 Python runtime 和业务代码实际运行 15 项契约测试全部通过（11 项 SKU 材料契约 + 4 项历史出库契约，属于上述回归的打包环境复验，不作为另外 15 个不同测试累计）。已核对模块从未签名 App 包加载；打包业务源码与工作树一致。
- 生成器已更新 learning 05–08 源码索引；原有 WeCom 学习文件、`test1.py` 与本任务开始时 Swift 修改保持不变。
- 桌面工具报告 Mac 锁定且不能自动解锁，已向用户请求手动解锁。没有尝试绕过锁屏，没有执行 `install-app`，没有变更正式库。再次只读确认正式 `material_items` 仍 113 行且没有 `product_code` 列。
- 日志与可复现实验脚本位于 `/tmp/pp-flowhub-material-sku.BSIt8J/`：`release-gate.log`、`release-macos-ui.log`、`release-aimes.log`、`release-workbook.log`、`build-app.log`、`packaged-contract.log`、各 migration/read/outbound 审计脚本及 JSON。

### 解锁后的剩余步骤

1. 确认旧 App 已退出，保留当前通过门禁的构建产物；在普通 Terminal/Aqua 运行绝对路径 `scripts/install-app`，验证 Apple Development 签名、helper 和包一致性。不要用 ad-hoc 签名。
2. 正式迁移前重新读取现场状态并创建项目本地可恢复 SQLite Online Backup；冻结旧代码对新备份重新审计，在副本应用用户批准的 White Oak → M1170 并演练，不能假设旧审计期间现场无变化。
3. 正式库应用已批准的映射与事务迁移；核对五表 FK、数量/来源/生产消耗、其余业务事实、完整性与关键订单读层。不得执行真实库存扣减或确认新业务材料。
4. 用签名安装版查看 PP0086（M1170 封边 263.95）和有已完成生产的订单，验证材料/消耗投影。写入通过隔离夹具执行，不能把副本测试称为真实业务确认。
5. 验收结束退出本次 App 与安装 Terminal，更新本计划的正式证据和完成状态。
