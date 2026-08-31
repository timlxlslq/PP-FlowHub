"""Resident local order service used by the macOS dashboard.

The service keeps one prepared workflow database connection alive and handles
one order request at a time.  It deliberately uses a small newline-delimited
JSON protocol so Swift can receive results and progress without temporary
result files.  SQLite remains the durable source of truth; the resident
process is only the in-memory/read-model lifetime boundary.
"""

from __future__ import annotations

import base64
import json
import os
import sqlite3
import sys
from pathlib import Path

from .core import Config
from .database import database_path
from .operation_log import OPERATION_ID_ENV, configure_operation_log
from .order_index import (
    OrderIndexStore,
    clear_shared_workflow_connection,
    install_shared_workflow_connection,
)
from .order_workflow import main


def _config() -> Config:
    config = Config()
    if configured_state := os.environ.get("PP_FLOWHUB_STATE_DIR", "").strip():
        config.state_dir = Path(configured_state).expanduser()
    config.load_settings()
    # This is the one storage preparation point for the service lifetime.
    config.prepare_storage()
    config.reconcile_outbound_on_read = False
    return config


def serve() -> int:
    config = _config()
    database = database_path(config.state_dir).resolve()
    connection = sqlite3.connect(database)
    # ``ensure_schema`` owns shared business tables, while OrderIndexStore
    # owns the order-index tables and their one-time column upgrades. Run that
    # bootstrap exactly once before exposing the connection to requests.
    bootstrap = OrderIndexStore(database, connection=connection)
    bootstrap.close()
    install_shared_workflow_connection(database, connection)
    logger = configure_operation_log(config)
    order_model: dict | None = None
    order_model_stamp: int | None = None

    def database_stamp() -> int:
        try:
            return database.stat().st_mtime_ns
        except OSError:
            return 0

    try:
        for raw_line in sys.stdin:
            line = raw_line.strip()
            if not line:
                continue
            try:
                request = json.loads(line)
                if not isinstance(request, dict):
                    raise ValueError("请求格式必须是对象")
                request_id = str(request.get("id") or "")
                if not request_id:
                    raise ValueError("请求缺少 id")
                if request.get("command") == "shutdown":
                    return 0
                arguments = request.get("arguments", [])
                if not isinstance(arguments, list) or not all(isinstance(item, str) for item in arguments):
                    raise ValueError("请求 arguments 格式无效")
                stdin_text = None
                encoded_input = request.get("input_base64")
                if encoded_input:
                    stdin_text = base64.b64decode(str(encoded_input)).decode("utf-8")
                os.environ[OPERATION_ID_ENV] = request_id
                command = arguments[0] if arguments else ""
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
                if isinstance(payload, dict) and isinstance(payload.get("orders"), list):
                    order_model = payload
                    order_model_stamp = database_stamp()
            except Exception as exc:  # protocol errors must not kill the App service
                payload = {
                    "fatal": {
                        "code": "order_service_request",
                        "message": f"订单后台请求失败：{exc}",
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
