# 待处理中心工作流 Implementation Plan

> **历史计划参考（2026-09）**：本文记录当时的设计和执行步骤，不代表当前待办、授权或已交付能力。当前任务范围与实现以 [系统架构](../../architecture/system-architecture.md)、[业务规则](../../business-rules.md) 和 [发布流程](../../release-testing.md) 为准。

> 原计划曾要求使用特定 Superpowers 子技能逐项执行；该要求只属于当时的历史流程，当前不作为强制技能或授权条件。Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将待处理中心实现为一个尺寸适合二级界面的、按待处理类型显示专属详情和动作的 SwiftUI 页面，并在人工映射完成后自动续跑原操作至只读预览。

**Architecture:** 保留 `PendingCenterItem` 作为待处理中心的统一列表事实，但将用户界面状态映射为“待处理、处理失败、待人工确认、需人工处理”四类。`PendingCenterSheet` 负责列表、类型专属详情和公共“稍后处理”动作；`AppModel` 保存一次性的续跑上下文，在映射保存后串行执行必要的重新读取/校验，再把结果交给只读预览，绝不自动确认写入。

**Tech Stack:** macOS 26 SwiftUI、现有 `AppModel`、Typed Tool Gateway、本地 SQLite/Server 业务流程、Swift 源码合同测试、Python `unittest` 发布门禁。

**Spec:** `docs/superpowers/specs/2026-09-02-pending-center-workflow-design.md`

## Global Constraints

- 待处理中心是二级界面，使用项目现有二级 Sheet 的紧凑尺寸、浅色玻璃背景、`AppSurfaceCard` 和系统按钮语言。
- 顶部只显示待处理中心身份、说明、提醒/信息按钮和关闭入口，不显示订单中心、助手等主菜单。
- 用户可在四种待处理类型中使用“稍后处理”；它只关闭当前界面，不改变业务状态、不推进基线、不写入数据库。
- “待处理”表示扫描已完成且存在尚未进入预览的变化，不再向用户显示“待扫描处理”。
- 映射保存后只自动继续读取、解析、校验和生成只读预览；必须经过独立的“确认后写入”和二次确认才允许真实写入。
- 生产代码修改后必须运行完整发布门禁、重新构建、正式签名安装和安装版检查；本计划阶段不修改生产 App。

## 文件结构

- Modify: `macos/TravelerAssistant.swift` — 待处理状态映射、映射续跑上下文和续跑协调，不复制 Python 业务规则。
- Modify: `macos/OrderDashboardView.swift` — 紧凑二级 Sheet、左侧队列、类型专属右侧详情、关闭和公共动作。
- Modify: `tests/test_macos_ui.swift` — 待处理分类、二级界面布局、动作边界和续跑入口的源码/模型合同。
- Modify if needed: `traveler_assistant/order_index.py` — 仅在现有 `process-server-folder` 返回值不足以生成后续预览时，补充可恢复的业务结果；优先保持 Python 业务规则不变。
- Reference only: `docs/project-static-context.md`, `docs/learning/10-product-design-order-center-audit.md`。

### Task 1: Lock the four user-facing pending categories

**Files:**
- Modify: `macos/TravelerAssistant.swift:626-765`
- Modify: `tests/test_macos_ui.swift` pending-center tests around the existing `buildPendingCenterItems` contract

**Interfaces:**
- Consumes: existing `ServerFolderChangeGroup`, `CurrentIssue`, `AimesReviewItem`, `buildPendingCenterItems` inputs.
- Produces: stable user-facing statuses `待处理`, `处理失败`, `待人工确认`, `需人工处理`; existing issue kinds remain unchanged.

- [ ] **Step 1: Add a failing source-contract test**

  Add assertions that a Server change group without a current issue maps to `待处理`, an ownership/AIMES ambiguity maps to `待人工确认`, an unmapped-material issue maps to `需人工处理`, and a generic issue maps to `处理失败`. Add an assertion that no pending status equals `稍后处理`.

- [ ] **Step 2: Run the focused UI test and verify the expected failure**

  Run: `xcrun swiftc -parse-as-library tests/test_macos_ui.swift macos/OperationLog.swift macos/TravelerAssistant.swift macos/AssistantView.swift macos/OrderDashboardView.swift -o /tmp/pending-center-ui-test -framework SwiftUI -framework AppKit -framework AVFoundation -framework Speech -framework Security && /tmp/pending-center-ui-test`

  Expected: the new status assertion fails because the current code still returns `待扫描处理` for an unprocessed Server change group.

- [ ] **Step 3: Implement the minimal status correction**

  Change only the user-facing mapping in `buildPendingCenterItems` from `待扫描处理` to `待处理`. Preserve `需人工确认`, `需人工处理`, and `处理失败` branch conditions and all source facts.

- [ ] **Step 4: Run the focused test again**

  Run the same compile-and-test command from Step 2.

  Expected: PASS for the four category assertions and no `稍后处理` status.

- [ ] **Step 5: Commit the category change**

  ```bash
  git add tests/test_macos_ui.swift macos/TravelerAssistant.swift
  git commit -m "feat: define pending center categories"
  ```

### Task 2: Add a resumable mapping continuation context

**Files:**
- Modify: `macos/TravelerAssistant.swift` around `pendingInventoryMappingFolder`, `requestInventoryMapping`, `saveInventoryMapping`, and `rereadPendingSourceFolder`
- Modify: `tests/test_macos_ui.swift` mapping and pending-center contracts

**Interfaces:**
- Consumes: `requestInventoryMapping(folderPath:message:)`, `saveInventoryMapping(travelerName:productCode:)`, existing `process-server-folder` and `list-index` routes.
- Produces: a private `PendingResumeContext` containing the pending item identifier, normalized source folder, order/factory identity when available, and the blocked operation kind; a single coordinator such as `resumePendingOperationAfterMapping()` that runs the remaining read/parse/validation path in order.

- [ ] **Step 1: Add a failing contract for continuation ordering**

  Assert in `tests/test_macos_ui.swift` that the mapping save path retains the pending source context, calls the re-read path, refreshes the pending list, and routes successful continuation to a read-only preview path. Assert that the path does not call a write-confirmation method or bypass a second confirmation.

- [ ] **Step 2: Run the focused test and verify it fails**

  Run the existing macOS UI test command.

  Expected: FAIL because the current callback starts `previewSelectedInventory()` and `rereadPendingSourceFolder()` directly without one explicit continuation context or a guaranteed return to the original pending preview.

- [ ] **Step 3: Implement the continuation context**

  Add a private value type and state property. Populate it in `requestInventoryMapping` before presenting the mapping workspace. Keep the source path normalized to the order folder and keep the original pending item identity so the UI can return to the same item.

- [ ] **Step 4: Implement the serial resume coordinator**

  Replace direct parallel callback launches with this sequence:

  ```swift
  save mapping
    -> re-read required order/Server files
    -> apply returned preview facts in memory
    -> refresh list-index / pending items
    -> present read-only preview for the saved context
  ```

  The coordinator must clear the continuation context only after success or a terminal, user-visible failure. It must leave the pending item active if re-reading or preview preparation fails.

- [ ] **Step 5: Run focused tests and inspect the source contract**

  Run the existing macOS UI test command and confirm the continuation sequence and write boundary pass.

- [ ] **Step 6: Commit the continuation change**

  ```bash
  git add tests/test_macos_ui.swift macos/TravelerAssistant.swift
  git commit -m "feat: resume pending operation after mapping"
  ```

### Task 3: Rebuild the Pending Center as a compact secondary Sheet

**Files:**
- Modify: `macos/OrderDashboardView.swift:3263-3500`
- Modify: `macos/TravelerAssistant.swift:7902-7913` for the pending Sheet frame if required
- Modify: `tests/test_macos_ui.swift` pending-center UI contracts

**Interfaces:**
- Consumes: `model.pendingCenterItems`, existing issue details, mapping route, Server preview route, and `model.showPendingCenterPrompt`.
- Produces: a compact two-column `PendingCenterSheet` with a selected item, type-specific detail view, item-level “稍后处理”, explicit close action, and type-appropriate primary actions.

- [ ] **Step 1: Add failing layout and action contracts**

  Assert that the pending sheet has a close action, does not contain the primary top-level navigation labels, exposes “稍后处理” for every pending type, and keeps “确认后写入” only on a previewable/manual-confirmation path. Assert that the sheet frame is smaller than the current 900×640 minimum and uses the shared `LiquidGlassPreviewBackdrop`/`AppSurfaceCard` style.

- [ ] **Step 2: Run the focused test and verify it fails**

  Run the existing macOS UI test command.

  Expected: FAIL because the current production sheet is a single full-width list with footer-only “稍后处理”, no selected right-hand detail panel, and no compact secondary-sheet frame contract.

- [ ] **Step 3: Implement the shared secondary-sheet shell**

  Keep the title and explanatory subtitle once at the top. Add a trailing “关闭” action that dismisses the sheet. Use the existing project surface/background/button styles and a compact frame around `980×620` or the smallest size that keeps the type-specific content readable.

- [ ] **Step 4: Implement the left queue**

  Add search/filter controls, category counts, selected-row treatment, and concise rows showing order/folder identity, type, problem summary, and update time. Do not show “稍后处理” as a status or category.

- [ ] **Step 5: Implement the four right-hand detail formats**

  - `待处理`: source changes, affected scope, “选择并预览”, and read-only boundary.
  - `处理失败`: failed stage, user-readable cause, path/impact, “检查并确认重试”, and “稍后处理”; no write button.
  - `待人工确认`: current/suggested values, candidate choice, read-only preview, “确认后写入”, and “稍后处理”.
  - `需人工处理`: source name/spec/SKU gap, “处理映射”, mapping result/continuation feedback, and “稍后处理”.

- [ ] **Step 6: Wire close and item-level “稍后处理”**

  “稍后处理” closes the current pending center presentation without resolving or deleting the item. The close button performs the same dismissal intentionally but has separate copy and placement so the user can distinguish returning from deferring.

- [ ] **Step 7: Run focused tests and compile the preview path**

  Run the existing macOS UI test command and `git diff --check`.

- [ ] **Step 8: Commit the UI change**

  ```bash
  git add tests/test_macos_ui.swift macos/OrderDashboardView.swift macos/TravelerAssistant.swift
  git commit -m "feat: redesign pending center secondary sheet"
  ```

### Task 4: Verify the complete production change and release gate

**Files:**
- Modify only if verification reveals a defect: files from Tasks 1–3
- Review: `docs/project-static-context.md`, `docs/release-testing.md`, `docs/project-handoff-log.md`

**Interfaces:**
- Consumes: the completed pending-center workflow and continuation behavior.
- Produces: tested, signed, installed App evidence; no external Server or inventory write during verification unless separately authorized.

- [ ] **Step 1: Run the full release test gate**

  Run: `./scripts/test-release`

  Expected: all applicable Python tests, macOS UI regression, workbook E2E, and `git diff --check` pass.

- [ ] **Step 2: Build a fresh App**

  Run: `./scripts/build-app`

  Expected: a new `/tmp/pp-flowhub-build/PP FlowHub.app` is produced; do not reuse a previous build.

- [ ] **Step 3: Install from ordinary Aqua Terminal**

  Run: `./scripts/install-app`

  Expected: Apple Development identity, bundle identifier, signature, helper, and atomic installation checks pass.

- [ ] **Step 4: Perform installed-App read-only acceptance**

  Confirm the compact Pending Center opens as a secondary interface, the close action returns to the main page, each of the four types shows the correct right panel, and mapping completion returns to a read-only preview without automatically writing business facts.

- [ ] **Step 5: Record evidence and finish**

  Update `docs/project-handoff-log.md` with the verified source/test/build/install/visible-UI boundaries. Quit the App and Terminal after verification, as required by the project release procedure.
