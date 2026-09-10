# Pending center Tasks 1/2 handoff

## September 5 final review correction (supersedes list refresh below)

Final follow-up: state now also retains `completedNames: Set<String>` separately. Every request merges newly encountered names into remainingNames with case-insensitive deduplication while excluding completedNames, so multiple issues sharing one folder/item cannot hide one another's new mappings. Added executable test with grouped A/B issues, saved A, newly discovered C/D, and ignored B across close/reopen. Final rerun after this fix: `./scripts/test-macos-ui` exit 0, `macOS UI regression tests passed`; diff whitespace and both reverse-patch checks pass. Both patches include this final follow-up.

Applied directly in main, only TravelerAssistant.swift and test_macos_ui.swift. `review-fix.patch` is incremental from `review-baseline/`; `task-only.patch` has been regenerated from the original inherited baseline. Both are already applied and both pass `git apply --reverse --check`.

Removed the continuation's list-index command completely, with no replacement query. Read-only inspection confirms list_order_index invokes _reconcile_temporary_order_projections, which can update/delete durable order records. The successful continuation now validates the in-memory preview, stages pendingResumePreview, dismisses the mapping workspace, and presents the existing Server preview. Pending queue facts stay untouched in memory.

Added per-item session memory via `@Published private(set) var pendingMappingResumeStates: [String: PendingMappingResumeState]`. Values contain remainingNames and failureMessage. Keys are PendingCenterItem.id (normalized folder fallback when no queue item exists). Accessors: `pendingMappingResumeState(for:)`, `pendingMappingResumeMessage(for:) -> String`, and `activePendingMappingResumeState`. The mapping workspace displays its retained failure; parent owns pending-detail rendering in OrderDashboardView.swift.

Closing clears only the active presentation/continuation identity. Remaining names and failure survive reopening in the same AppModel. Saved or ignored mappings are removed from the stored remaining list, including saves completing after cancellation; stale callbacks cannot auto-restart preview. Success clears the prior failure and retains an empty remaining list, so reopening an old issue message cannot reintroduce saved mappings. This is UI model session memory, not disk persistence across App restarts.

Final command: `./scripts/test-macos-ui` from `/Users/lantian/Documents/pp-flowhub`, exit 0, `macOS UI regression tests passed`. Writable module cache remains supplied by the project script. Tests now assert no follow-up command after preview (including list-index), untouched original queue identity, failure/partial-save/preview-failure/success close-reopen behavior, ignored-item persistence, and late-save persistence without automatic continuation. `git diff --check` also passes. No full gate repeated here; parent will run final gate. No commits, agents, build, release, or install.

Workspace: `/Users/lantian/Documents/pp-flowhub` (changes already applied).

The original isolated worktree `/private/tmp/pp-flowhub-pending-tasks12` and its test process disappeared between September 4 and September 5. Continued in main under the user's explicit fallback authorization. No commits, index changes, build, release, installation, or agents were used for the resumed implementation. The earlier worktree branch was `codex/pending-tasks12` at `ff62d8a`; it contains no delivered commit.

## Artifacts and scope

- `task-only.patch`: diff against the inherited dirty September 5 baseline, containing only `macos/TravelerAssistant.swift` and `tests/test_macos_ui.swift`. Already applied in main; do not apply twice.
- `baseline/macos/TravelerAssistant.swift` and `baseline/tests/test_macos_ui.swift`: exact inherited source snapshots before resumed edits.
- Parent owns `macos/OrderDashboardView.swift`; this task did not modify it.
- All other inherited dirty files and untracked status icon resources were preserved.

## Implemented

- Four labels are 待处理, 处理失败, 待人工确认, 需人工处理. Both grouped and standalone mapping issues use `currentIssueRequiresInventoryMapping`, including real material_validation messages containing 未完成商品 SKU 处理. Standalone subtitle uses the same predicate.
- Private context retains normalized folder, original path/item, order/factory identity, operation kind, and unique request identity.
- Saves use one coordinator. Remaining named mappings block continuation. Mapping/ignore failures retain the original pending facts and context; explicit retry is visible in the mapping workspace.
- Server continuation invokes `preview-server-changes --server-folder <normalized source> --include-hardware true`, validates the returned preview belongs to that source, then calls `list-index`, preserves the original pending issue, and hands the in-memory payload to existing `presentServerWritePreview`.
- Actual sheet dismissal (`onDismiss`) triggers preview presentation. Cancellation, switching requests, stale save/preview/list callbacks, and old dismissal notifications cannot continue the old operation. Duplicate continuation attempts are gated. A busy order channel gives a retry message instead of silently dropping continuation.
- Normal inventory mapping outside pending retains its inventory preflight fallback; pending ignore operations share the same serial coordinator.
- Parent-requested root PendingCenterSheet minimum frame is now 980 x 620.

## Backend evidence (read only)

Inspected `traveler_assistant/order_index.py`: `process_server_folder` delegates to durable `sync_order_index`. `preview_server_changes` copies the central database into `sqlite3.connect(":memory:")`, performs selected-folder parsing/validation against the shadow connection, disables outbound reconciliation/temporary processing, and returns an in-memory payload. No Python source was changed or production command executed by this task.

## Verification

Working directory for commands: `/Users/lantian/Documents/pp-flowhub`.

- `./scripts/test-macos-ui`: compiled and passed after implementation. Script uses writable `/tmp/pp-flowhub-ui-test-module-cache` with both Swift and Clang module-cache flags, `-DTESTING`, and isolated test state. No artificial execution time limit.
- First new test run failed on standalone material_mapping category; corrected the omitted status predicate. Subsequent full script runs passed.
- Executable AppModel tests inject order/inventory runners and hold/release callbacks. Cover multiple mappings, save/ignore failure, malformed preview, normalized source, preview/list ordering, pending retention, real preview presentation after dismissal, cancellation during save/list, switching during preview, busy order channel, stale sheet dismissal, and absence of confirmation/write commands.
- UI source contracts cover category picker, selection/action targeting, 980 x 620 frames, close-only 稍后处理, pending action confirmation and Server write second confirmation.
- `git diff --check`: pass.
- `git apply --reverse --check .superpowers/tasks/pending-center-tasks12/task-only.patch`: pass; patch matches changes already applied to main.
- Final integration rerun of `./scripts/test-macos-ui` after parent UI review updates: exit 0, `macOS UI regression tests passed`. Parent's grouped-ignore, AIMES feedback, history confirmation, stable-selection, and escaping closure changes remain owned by the parent.
- Python suite was not duplicated. Parent reports 283 tests passed, 1 skipped; this is parent-supplied evidence.

## Limits / integration concerns

- No live SMB folder, business database write, inventory website, installed App flow, or native sheet animation was exercised. Tests prove command routing/state transitions and compilation, not installed-App acceptance.
- The pending source issue deliberately remains until separately confirmed business processing. Saving mappings or showing a preview does not resolve it.
- Preview validation errors and newly discovered hardware requirements are handed to the existing preview UI, whose write guard and separate confirmation remain authoritative.
- Main has concurrent parent UI changes. Review the task-only patch rather than attributing the entire git diff to Tasks 1/2. The `.superpowers` artifacts are local handoff material and should not be included in a product release without review.
