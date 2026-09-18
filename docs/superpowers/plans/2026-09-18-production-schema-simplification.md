# 生产与订单数据库精简

目标：减少重复表和状态字段，以已确认事实为准，支持一次生产包含不同订单的工厂单。

状态：源码、回归、构建和正式安装已完成；正式库自动备份迁移及逐行核对通过。安装版订单列表和 PP0086 材料详情读取已验证，验收 App 已退出。工厂单展开控件受工具限制，Server 真实扫描未验证。

## 已确认边界

- 一个工厂单只能生产一次，暂不拆门板/柜体。特殊重复生产与临时优化文件夹规则另行处理。
- Panel、Plywood、封边分配到订单；自动及人工五金归工厂单。
- 混单逐来源、逐 SKU 分配合计必须等于优化材料总数，确认后按订单累计；重复确认不得累计两次。
- 来源批次不是生产事实，删除独立来源批次及唯一批次冲突判断；保留文件路径、指纹、优化证据和分配。
- 实际生产保留记录 ID、时间、来源及订单材料消耗；工厂单直接关联生产记录，取消独立关联表及 MP 编号。
- 主流程状态与导入预览错误分离。订单状态统一汇总，不把未确认文件的错误覆盖到已确认事实。
- 保留历史已确认材料，不能因 manual 来源标签删除 CS002 的既有 Panel。
- 保留所有既有工作树修改；不调用真实库存写入。

## 实施步骤

1. 核对依赖、现有数据和差异；保存改前源码与数据库备份。
2. 实现事务迁移及新数据库结构，清除来源批次，合并工厂单生产关联。
3. 更新生产、库存恢复、AIMES、材料预览和 UI 读写；统一流程状态。
4. 隔离测试迁移、数量守恒、一次生产约束及失败恢复；副本演练并比较事实。
5. 正式库备份迁移，完整发布门禁、一次串行构建、Aqua 签名安装和安装版验收。
6. 同步业务规则、数据模型、学习文档与交接记录。

## 验证

正式库通过只读连接核对；迁移副本比较工厂单生产/出货状态、各订单 SKU 数量、历史来源和时间、外部单据；完整性与外键检查。实际跨订单库存扣减不作为离线测试的一部分。

## 剩余决策

本次业务规则无待确认项。临时校验已与正式订单分离；跨订单批量库存操作界面未新增，现有单订单库存操作恢复保持原合同。

## 已完成与证据

- 删除来源批次两表与工厂单生产关联表；实际生产改为 production_records/production_materials；取消 MP 编号和表头 order_id。
- 工厂单 stage 取代 optimized/outbound_status；订单移除 validation_status/validation_message/material_status。预览校验使用 TEMP 内存结果，确认继续校验。
- 分配表保留；内存确认补齐逐来源/逐 SKU 总量守恒及分配事务落库，跨订单共享材料须整组确认。历史 manual 板材不删除。
- 事务记录支持跨订单工厂单及同 SKU 分订单数量。App 仍从当前订单启动生产，本次不新增跨订单库存批量操作 UI。
- 副本由 33 表/295 列变为 30 表/268 列；50 生产记录、66 工厂单关联、62 消耗明细逐行保留，其他业务事实逐行一致。
- 31 个订单迁移前后汇总阶段、生产数、出货数无差异；完整性与外键通过。
- 395 Python 测试通过（1 项跳过），SwiftUI、AIMES 离线、PP0067 文件专项及 diff 检查通过。
- 普通沙箱 Swift 宏进程被系统阻止；通过批准的普通执行环境重新运行完整门禁成功。
- Computer Use 明确拒绝 com.apple.Terminal，安全理由；不得绕过。正式库保持旧结构，避免旧安装版不能读取；新版本首次启动迁移前自动 Online Backup 到 schema-migration-backups。

## 尚未完成

Server 共享目录当前不可访问，真实扫描未验证；工厂单行展开控件的 UI 验收受窗口控制工具错误限制。临时文件夹特殊重复生产规则仍明确排除。

## 构建时证据（安装前历史快照）

- `/tmp/pp-flowhub-build/PP FlowHub.app` 一次串行构建成功，尚未签名安装。
- Bundle `com.pacificpride.ppflowhub`，版本 `0.4.1 (5)`，打包 Node `v24.19.0` 校验通过。
- 可执行文件 SHA-256：`021fae37ca89ec1c3599697849c0ca1988e941d17726965ce6b098ae859e5deb`。
- 打包 database.py/production.py/order_index.py/inventory.py 与当前源码逐字节一致。
- 正式库最后只读复核仍为旧结构（manual_production_batches 存在、production_records 不存在）；未发起真实库存、Server 写入或生产确认。
- 门禁日志 `/tmp/pp-schema-release-unsandboxed.log`；构建日志 `/tmp/pp-schema-build.log`；副本比对报告 `/tmp/pp-flowhub-schema-baseline/migration-report.json`。
- 安装前退出旧 App，在普通 Terminal 执行 `/Users/lantian/Documents/pp-flowhub/scripts/install-app`；安装后再打开新版触发带自动备份的原子迁移，并验收正式库和实际入口。

## 安装后验收（2026-09-17 23:10）

- 用户完成安装；安装包 Apple Development 签名时间 23:07:39，TeamIdentifier ZF64PZKWMD。普通执行环境 `codesign --verify --deep --strict` 通过；沙箱证书信任错误已通过该复验排除。
- 安装包四个核心 Python 模块与本次源码逐字节一致。
- 启动安装版自动迁移正式库至 30 表/268 列；备份位于 `data/schema-migration-backups/workflow-before-production-v1-20260917-231039-796319.sqlite3`。
- 正式库与该迁移前备份逐行核对：50 生产记录、66 工厂单关联、62 消耗明细完全一致；其余保留业务表无差异，orders/factory_orders/source_files 共用字段逐行一致。正式库及备份完整性通过，正式库无外键错误。
- 安装版订单中心可见 PP0087 已生产、PP0072 部分生产部分出货、PP0064 部分优化，读取成功。未执行生产确认或外部库存写入。
- Server `/Volumes/server/Optimized Orders` 不可访问；选择 PP0086 继续详情验收时工具报告 Mac 锁屏，需要解锁后续验。

## 解锁后验收收尾

- 在全部订单中打开 PP0086 详情：状态已出货，优化/生产/出货均为 2/2。Plywood 柜体板 12、抽屉板 1、背板 5；Panel White Oak 9；White Oak 封边 263.95 m。五金分别显示于 F2609140250 与 F2609140249 工厂单下。
- 工厂单展开箭头的 AX 点击未改变界面，坐标点击/激活窗口返回 `noWindowsAvailable`，因此不声称完成该控件验收。
- 已发送 Cmd-Q，随后工具应用清单确认 `com.pacificpride.ppflowhub isRunning=false`。未执行真实生产确认或库存扣减；未开启 Terminal。
