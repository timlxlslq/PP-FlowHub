"""Typed command boundary between intent routing and business operations.

The gateway is intentionally inside the application rather than an external
MCP service.  It is the last common checkpoint before a command can generate
a Traveler or write central facts, so it must not trust an Agent-provided
approval decision or preview as authorization.
"""

from __future__ import annotations

from dataclasses import asdict
from pathlib import Path

from .command_router import LocalCommand
from .core import Config, RuleError
from .order_workflow import (
    add_manual_hardware,
    generate_order_traveler,
    list_order_folders,
    preview_manual_hardware,
    preview_order,
    preview_payload,
    resolve_source_root,
    update_order_traveler,
)


WRITE_ACTIONS = {"generate_traveler", "update_traveler", "add_manual_hardware"}


def _order_folder(config: Config, order_id: str) -> Path:
    # PP orders live in Optimized Orders, while CS orders live in its sibling
    # CUT TO SIZE directory. The production-files page already follows this
    # split; assistant commands must resolve the same business source.
    configured_root = (
        config.source_root.parent / "CUT TO SIZE"
        if order_id.upper().startswith("CS")
        else config.source_root
    )
    root = resolve_source_root(configured_root)
    matches = [path for path in root.iterdir() if path.is_dir() and path.name.upper() == order_id]
    if len(matches) != 1:
        raise RuleError(
            "order_not_found",
            f"在当前订单目录找不到唯一文件夹：{order_id}（{root}）",
            searched_root=str(root),
            match_count=len(matches),
        )
    return matches[0]


def execute_local_command(config: Config, command: LocalCommand, approved: bool = False) -> dict:
    """Validate and execute one typed command through the shared workflow.

    Read-only actions execute immediately.  Write actions first return an
    ``approval_required`` preview; only a later call with ``approved=True``
    performs the write.  The manual-hardware path writes central SQLite facts
    and deliberately does not require an existing Traveler.
    """
    if command.action == "add_manual_hardware":
        arguments = command.arguments
        preview = preview_manual_hardware(
            config,
            arguments["order_id"],
            arguments["factory_name"],
            arguments["product_code"],
            arguments["quantity"],
            arguments.get("remarks", ""),
        )
        if not approved:
            return {
                "status": "approval_required",
                "request": asdict(command),
                "preview": preview,
            }
        traveler, backup, saved = add_manual_hardware(
            config,
            arguments["order_id"],
            arguments["factory_name"],
            arguments["product_code"],
            arguments["quantity"],
            arguments.get("remarks", ""),
        )
        return {
            "status": "completed",
            **saved,
            "updated": str(traveler) if traveler != Path("") else "",
            "backup": str(backup) if backup != Path("") else "",
        }

    if command.action in WRITE_ACTIONS and not approved:
        preview = preview_order(config, _order_folder(config, command.arguments["order_id"]))
        return {
            "status": "approval_required",
            "request": asdict(command),
            "preview": preview_payload(config, preview),
        }

    if command.action == "list_orders":
        return {"status": "completed", "orders": list_order_folders(config)}

    if command.action == "check_inventory_stock":
        order_id = command.arguments["order_id"]
        from .inventory import check_database_stock
        comparison = check_database_stock(config, order_id)
        return {
            "status": "completed",
            "result_type": "stock_comparison",
            "order_id": order_id,
            **comparison,
        }

    if command.action not in {"preview_order", "generate_traveler", "update_traveler"}:
        raise RuleError("unknown_tool", f"不支持的本地工具：{command.action}")

    preview = preview_order(config, _order_folder(config, command.arguments["order_id"]))
    payload = preview_payload(config, preview)
    if command.action == "generate_traveler":
        payload["created"] = str(generate_order_traveler(config, preview))
    elif command.action == "update_traveler":
        updated, backup = update_order_traveler(config, preview)
        payload.update(updated=str(updated), backup=str(backup))
    return {"status": "completed", **payload}
