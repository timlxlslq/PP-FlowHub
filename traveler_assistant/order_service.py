"""为 macOS 看板提供常驻的本地订单服务。

复用已准备好的工作流数据库连接，逐个处理订单请求。通过逐行 JSON 协议
向 Swift 返回结果和进度，无需临时结果文件。SQLite 仍是持久事实来源，
常驻进程只管理内存和读取模型的生命周期。
"""

from __future__ import annotations

import base64
import json
import os
import sqlite3
import sys
from pathlib import Path

from .core import Config
from .database import connect_database, database_path
from .operation_log import OPERATION_ID_ENV, OPERATION_LOG_ENABLED_ENV, configure_operation_log, safe_exception_details
from .order_index import (
    OrderIndexStore,
    clear_shared_workflow_connection,
    install_shared_workflow_connection,
)
from .order_workflow import main


def _config() -> Config:
    """读取设置和可选状态目录环境变量，准备服务存储；无参数。"""
    config = Config()
    if configured_state := os.environ.get("PP_FLOWHUB_STATE_DIR", "").strip():
        config.state_dir = Path(configured_state).expanduser()
    config.load_settings()
    # 服务生命周期内只在此处准备存储。
    config.prepare_storage()
    config.reconcile_outbound_on_read = False
    return config


def serve() -> int:
    """逐行处理标准输入中的订单请求并输出 JSON；无参数，返回进程退出码。"""
    config = _config()
    database = database_path(config.state_dir).resolve()
    connection = connect_database(database)
    # ensure_schema 管理共享业务表，OrderIndexStore 管理订单索引表及一次性字段升级。
    # 向请求开放连接前，只执行一次初始化。
    bootstrap = OrderIndexStore(database, connection=connection)
    bootstrap.close()
    install_shared_workflow_connection(database, connection)
    logger = configure_operation_log(config)
    order_model: dict | None = None
    order_model_stamp: tuple[int, int] | None = None

    def database_stamp() -> tuple[int, int]:
        """返回主数据库及 WAL 的修改时间，供内存模型失效判断；无显式参数。"""
        stamps = []
        for path in (database, Path(f"{database}-wal")):
            try:
                stamps.append(path.stat().st_mtime_ns)
            except OSError:
                stamps.append(0)
        return tuple(stamps)

    try:
        for raw_line in sys.stdin:
            line = raw_line.strip()
            if not line:
                continue
            request_id = ""
            os.environ[OPERATION_ID_ENV] = ""
            try:
                request = json.loads(line)
                if not isinstance(request, dict):
                    raise ValueError("请求格式必须是对象")
                request_id = str(request.get("id") or "")
                if not request_id:
                    raise ValueError("请求缺少 id")
                if request.get("command") == "shutdown":
                    return 0
                enabled = request.get("operation_log_enabled")
                if isinstance(enabled, bool):
                    logger.enabled = enabled
                    config.operation_log_enabled = enabled
                    os.environ[OPERATION_LOG_ENABLED_ENV] = "1" if enabled else "0"
                arguments = request.get("arguments", [])
                if not isinstance(arguments, list) or not all(isinstance(item, str) for item in arguments):
                    raise ValueError("请求 arguments 格式无效")
                stdin_text = None
                encoded_input = request.get("input_base64")
                if encoded_input:
                    stdin_text = base64.b64decode(str(encoded_input)).decode("utf-8")
                os.environ[OPERATION_ID_ENV] = request_id
                command = arguments[0] if arguments else ""
                # 只有完整的 list-index 响应可填充常驻模型。其他命令可能修改数据库
                # 或返回不同结构，必须先使模型失效，即使主数据库时间未变（如使用 WAL）。
                if command != "list-index":
                    order_model = None
                    order_model_stamp = None
                current_stamp = database_stamp()
                if command == "list-index" and order_model is not None and current_stamp == order_model_stamp:
                    logger.event(
                        "backend.model.cache_hit",
                        "从常驻订单内存模型返回订单列表",
                        details={"action": command},
                        operation_id=request_id,
                    )
                    payload = order_model
                    sys.stdout.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
                    sys.stdout.flush()
                    continue
                result: dict = {}
                exit_code = main(
                    arguments,
                    config_override=config,
                    logger_override=logger,
                    emit_result=False,
                    result_sink=result,
                    stdin_text=stdin_text,
                )
                payload = result.get("value")
                if not isinstance(payload, dict):
                    payload = {
                        "fatal": {
                            "code": "service_missing_result",
                            "message": f"订单后台未返回有效结果（退出码 {exit_code}）",
                        }
                    }
                if command == "list-index" and isinstance(payload, dict) and isinstance(payload.get("orders"), list):
                    order_model = payload
                    order_model_stamp = database_stamp()
            except Exception as exc:  # 协议错误不能导致 App 的常驻服务退出。
                logger.event(
                    "backend.command.failed", "订单后台请求发生未预期错误",
                    details=safe_exception_details(exc, action="order-service"),
                    operation_id=request_id,
                )
                payload = {
                    "fatal": {
                        "code": "order_service_request",
                        "message": "订单后台请求失败，请重试或查看操作日志。",
                    }
                }
            sys.stdout.write(json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n")
            sys.stdout.flush()
    finally:
        clear_shared_workflow_connection()
        connection.close()
    return 0


if __name__ == "__main__":
    raise SystemExit(serve())
