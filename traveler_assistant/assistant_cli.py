"""助手命令入口及本地解析、Agent 路由策略。

依次尝试确定性解析、已学习命令的精确匹配和 Agent 后备路由。
所有结果都进入同一类型化网关，在本地重新检查批准状态和业务条件。
"""

from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path

from .command_router import LocalCommand, ORDER_ID_RE, normalize_command_text, parse_local_command
from .core import Config, RuleError
from .runtime_store import RuntimeStore, TokenUsage, runtime_database_path
from .operation_log import configure_operation_log, safe_exception_details, safe_rule_error_text
from .tool_gateway import WRITE_ACTIONS, execute_local_command


def _factory_name_belongs_to_order(order_id: str, factory_name: str) -> bool:
    """检查完整工厂单名称的订单归属；order_id 为订单号，factory_name 为完整名称。"""
    order = order_id.strip().upper()
    factory = factory_name.strip().upper()
    if not order:
        return False
    match = re.match(rf"^{re.escape(order)}(?:-|\s+)(.+)$", factory)
    if not match:
        return False
    remainder = match.group(1).strip()
    if not remainder:
        return False
    # PP0035-2-MASTER 属于分单 PP0035-2，不属于主单 PP0035。
    if re.fullmatch(r"PP\d{4}", order) and re.match(r"^\d+(?:-|\s|$)", remainder):
        return False
    return True


def _learned_local_command(store: RuntimeStore, text: str) -> LocalCommand | None:
    """读取已学习动作并重新确定审批要求；store 为运行记录库，text 为用户命令。"""
    learned = store.learned_command(normalize_command_text(text))
    if learned is None:
        return None
    action, arguments = learned
    return LocalCommand(action, arguments, action in WRITE_ACTIONS)


def _agent_command(store: RuntimeStore, text: str) -> tuple[LocalCommand | None, dict]:
    """调用 Agent、校验参数并保存可用命令及用量；store 为运行记录库，text 为用户命令。"""
    from .agent_runner import MODEL, route_with_agent

    routed = route_with_agent(text)
    usage = TokenUsage(routed.input_tokens, routed.output_tokens)
    store.record_agent_usage(MODEL, usage)
    decision = routed.decision
    metadata = {
        "source": "agent",
        "model": MODEL,
        "explanation": decision.explanation,
        "token_usage": {
            "input": usage.input_tokens,
            "output": usage.output_tokens,
            "total": usage.total_tokens,
        },
    }
    if decision.action == "unsupported":
        return None, metadata
    order_id = decision.order_id.upper() if decision.order_id else None
    if decision.action != "list_orders" and (
        order_id is None or ORDER_ID_RE.fullmatch(order_id) is None
    ):
        return None, metadata
    arguments = {"order_id": order_id} if order_id else {}
    if decision.action == "add_manual_hardware":
        factory_name = decision.factory_name.strip().upper() if decision.factory_name else ""
        product_code = decision.product_code.strip().upper() if decision.product_code else ""
        normalized_input = normalize_command_text(text)
        if (
            factory_name
            and not _factory_name_belongs_to_order(order_id or "", factory_name)
            and normalize_command_text(factory_name) in normalized_input
            and normalize_command_text(order_id) in normalized_input
        ):
            factory_name = f"{order_id}-{factory_name.lstrip('-')}"
        if (
            not factory_name
            or not _factory_name_belongs_to_order(order_id or "", factory_name)
            or re.fullmatch(r"[A-Z]\d+", product_code) is None
            or decision.quantity is None
            or decision.quantity <= 0
        ):
            return None, metadata
        arguments.update(
            factory_name=factory_name,
            product_code=product_code,
            quantity=str(decision.quantity),
        )
        if decision.remarks and decision.remarks.strip():
            arguments["remarks"] = decision.remarks.strip()
    command = LocalCommand(
        decision.action,
        arguments,
        decision.action in WRITE_ACTIONS,
    )
    store.remember_command(normalize_command_text(text), command.action, command.arguments)
    return command, metadata


def main(argv: list[str] | None = None) -> int:
    """执行助手命令并输出 JSON 结果；argv 为命令行参数，省略时读取进程参数，返回退出码。"""
    parser = argparse.ArgumentParser(prog="pp-flowhub assistant")
    parser.add_argument("text", nargs="?")
    parser.add_argument("--usage", action="store_true")
    parser.add_argument("--approve", action="store_true")
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--order-root", type=Path)
    parser.add_argument("--template", type=Path)
    parser.add_argument("--backup-root", type=Path)
    parser.add_argument("--state-dir", type=Path)
    args = parser.parse_args(argv)
    config = Config()
    if configured_state := os.environ.get("PP_FLOWHUB_STATE_DIR", "").strip():
        config.state_dir = Path(configured_state).expanduser()
    # 助手用于正式业务，不继承旧版本遗留的本地测试来源设置。
    config.load_settings(source_profile="server")
    for name in ("source_root", "order_root", "template", "backup_root", "state_dir"):
        value = getattr(args, name)
        if value is not None:
            setattr(config, name, value)
    config.prepare_storage()

    logger = configure_operation_log(config)
    store = RuntimeStore(runtime_database_path(config.state_dir))
    if args.usage:
        logger.event("backend.command.completed", "读取 Agent 用量", details={"command": "assistant --usage"})
        print(json.dumps({"status": "completed", "usage": store.token_summary()}, ensure_ascii=False))
        return 0
    if not args.text:
        parser.error("text is required unless --usage is provided")

    logger.event("backend.command.started", "开始处理助手命令", details={"command": "assistant"})

    command = parse_local_command(args.text)
    metadata = {"source": "local", "token_usage": {"input": 0, "output": 0, "total": 0}}
    if command is None:
        command = _learned_local_command(store, args.text)
        if command is not None:
            metadata["source"] = "learned_local"
        else:
            try:
                command, metadata = _agent_command(store, args.text)
            except Exception as exc:
                logger.event("backend.command.failed", "助手命令路由失败", details={"stage": "agent_route", **safe_exception_details(exc, action="assistant")})
                print(json.dumps({"status": "agent_failed", "error": {"message": "助手命令路由发生未预期错误，请查看操作日志。"}}, ensure_ascii=False))
                return 3
            if command is None:
                logger.event("backend.command.completed", "助手命令不受支持", details={"result": "unsupported"})
                print(json.dumps({"status": "unsupported", **metadata}, ensure_ascii=False, indent=2))
                return 3
    try:
        result = execute_local_command(config, command, args.approve)
        logger.event(
            "backend.command.completed",
            "助手命令执行完成",
            details={"action": command.action, "approved": args.approve, "status": result.get("status", "")},
        )
        print(json.dumps({**result, **metadata}, ensure_ascii=False, indent=2))
        return 0
    except RuleError as exc:
        logger.event(
            "backend.command.failed",
            "助手命令执行失败",
            details={"action": "assistant", "code": exc.code, "error": safe_rule_error_text(str(exc), sensitive_values=(args.text,))},
        )
        print(json.dumps({"status": "failed", "error": {"code": exc.code, "message": str(exc), **exc.context}}, ensure_ascii=False, indent=2))
        return 2
    except Exception as exc:
        logger.event("backend.command.failed", "助手命令执行发生未预期错误", details=safe_exception_details(exc, action="assistant"))
        print(json.dumps({"status": "failed", "error": {"code": "assistant_processing_error", "message": "助手处理发生未预期错误，请查看操作日志。"}}, ensure_ascii=False))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
