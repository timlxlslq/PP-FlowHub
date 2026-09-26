from __future__ import annotations

import fcntl
import json
import os
import re
import uuid
from datetime import datetime
from pathlib import Path
from types import TracebackType
from typing import Any
from urllib.parse import urlsplit, urlunsplit


OPERATION_LOG_ENV = "WORKFLOW_OPERATION_LOG"
OPERATION_LOG_ENABLED_ENV = "WORKFLOW_OPERATION_LOG_ENABLED"
OPERATION_SESSION_ENV = "WORKFLOW_OPERATION_SESSION_ID"
OPERATION_ID_ENV = "WORKFLOW_OPERATION_ID"

_SENSITIVE_KEY_PARTS = (
    "password",
    "passwd",
    "secret",
    "token",
    "api_key",
    "apikey",
    "authorization",
    "cookie",
    "keychain",
    "credential",
    "username",
    "user_name",
    "remarks",
    "query",
    "input_value",
)
_SENSITIVE_TEXT_RE = re.compile(r"(?i)(password|passwd|secret|token|api[_-]?key|authorization|cookie)\s*[:=]\s*[^\s,;]+")
_QUOTED_SECRET_RE = re.compile(r'(?i)"(?:password|passwd|secret|token|api[_-]?key|authorization|cookie|credential|username|user_name)"\s*:\s*"[^"]*"')
_AUTH_HEADER_RE = re.compile(r"(?i)\b(?:bearer|basic)\s+[A-Za-z0-9._~+/-]+")
_URL_RE = re.compile(r"(?i)https?://[^\s\"'<>]+")
_SQL_WRITE_RE = re.compile(r"^\s*(insert(?:\s+or\s+\w+)?\s+into|update|delete\s+from|replace\s+into)\s+([\"`\[]?\w+[\"`\]]?)", re.IGNORECASE)
_SAFE_CONTEXT_RE = re.compile(r"^[A-Za-z0-9_-]{1,64}$")
_SAFE_SYMBOL_RE = re.compile(r"^[A-Za-z_][A-Za-z0-9_.]{0,100}$")


def _is_sensitive_key(key: str) -> bool:
    """判断字段名 key 是否包含凭据或原始输入等敏感标记。"""
    lowered = key.replace("-", "_").lower()
    return any(part in lowered for part in _SENSITIVE_KEY_PARTS)


def _redact_url(match: re.Match[str]) -> str:
    """删除网址的查询参数和片段并保留末尾标点；match 为网址正则匹配结果。"""
    raw = match.group(0)
    trailing = ""
    while raw and raw[-1] in ".,;:!?)}":
        trailing = raw[-1] + trailing
        raw = raw[:-1]
    try:
        parsed = urlsplit(raw)
        # 网址的 userinfo 也可能含密码；只保留主机和端口。
        hostname = parsed.hostname or ""
        if not hostname:
            return "[URL_REDACTED]" + trailing
        host = f"[{hostname}]" if ":" in hostname else hostname
        netloc = host + (f":{parsed.port}" if parsed.port is not None else "")
        safe = urlunsplit((parsed.scheme, netloc, parsed.path, "", ""))
    except ValueError:
        return "[URL_REDACTED]"
    return (safe or "[URL_REDACTED]") + trailing


def _secret_variants(value: Any) -> set[str]:
    """生成敏感值 value 的原文及 JSON 转义形式，供日志替换使用。"""
    if value is None:
        return set()
    text = str(value)
    if not text:
        return set()
    variants = {text}
    for ensure_ascii in (False, True):
        encoded = json.dumps(text, ensure_ascii=ensure_ascii)
        if len(encoded) >= 2:
            variants.add(encoded[1:-1])
    return {item for item in variants if item}


def _redact_text(value: str, sensitive_values: tuple[str, ...] = ()) -> str:
    """清理日志文本；value 为原文，sensitive_values 为需额外遮蔽的已知敏感值。"""
    # 先替换可能含空格的已知凭据，再清理完整网址及其参数。
    for secret in sorted(
        {variant for value in sensitive_values for variant in _secret_variants(value)},
        key=len,
        reverse=True,
    ):
        value = value.replace(secret, "[REDACTED]")
    value = _URL_RE.sub(_redact_url, value)
    value = _QUOTED_SECRET_RE.sub("[REDACTED]", value)
    value = _AUTH_HEADER_RE.sub("[REDACTED]", value)
    value = _SENSITIVE_TEXT_RE.sub(lambda match: f"{match.group(1)}=[REDACTED]", value)
    # 保留文件定位信息，但不在持久日志中保存用户主目录的账户名。
    home = str(Path.home())
    if home:
        value = value.replace(home, "~")
    return value


def redact(value: Any, key: str | None = None, *, sensitive_values: tuple[str, ...] = ()) -> Any:
    """递归脱敏并保留可诊断的上下文。

    参数：value 为待记录值；key 为可选字段名；sensitive_values 为额外敏感值。
    """
    if key is not None and _is_sensitive_key(key):
        return "[REDACTED]"
    if isinstance(value, dict):
        return {
            str(name): redact(item, str(name), sensitive_values=sensitive_values)
            for name, item in value.items()
        }
    if isinstance(value, (list, tuple)):
        return [redact(item, sensitive_values=sensitive_values) for item in value]
    if isinstance(value, str):
        return _redact_text(value, sensitive_values)
    if value is None or isinstance(value, (bool, int, float)):
        return value
    return _redact_text(str(value), sensitive_values)


def operation_log_enabled_from_environment() -> bool:
    """读取环境变量中的日志开关；无参数，未配置时默认启用。"""
    return os.environ.get(OPERATION_LOG_ENABLED_ENV, "1").strip().lower() not in {"0", "false", "no", "off"}


def safe_exception_details(
    exc: BaseException,
    *,
    action: str,
    order_id: str | None = "",
    factory_order: str | None = "",
) -> dict[str, Any]:
    """生成脱敏异常摘要；exc 为异常对象，action 为操作名，order_id 和 factory_order 为可选业务身份。只记录异常类型及最多八帧代码位置，不记录异常文字、源码或局部变量。"""
    details: dict[str, Any] = {"exception_type": type(exc).__name__}
    for key, value in (("action", action), ("order_id", order_id), ("factory_order", factory_order)):
        if isinstance(value, str) and _SAFE_CONTEXT_RE.fullmatch(value):
            details[key] = value
    frames: list[dict[str, Any]] = []
    traceback: TracebackType | None = exc.__traceback__
    while traceback is not None:
        code = traceback.tb_frame.f_code
        module = traceback.tb_frame.f_globals.get("__name__", "")
        if isinstance(module, str) and _SAFE_SYMBOL_RE.fullmatch(module) and _SAFE_SYMBOL_RE.fullmatch(code.co_name):
            frames.append({"module": module, "function": code.co_name, "line": traceback.tb_lineno})
        traceback = traceback.tb_next
    details["stack"] = frames[-8:]
    return details


def safe_rule_error_text(message: str, *, sensitive_values: tuple[str, ...] = ()) -> str:
    """返回截断后的脱敏业务错误；message 为错误文本，sensitive_values 为需额外隐藏的敏感值。"""
    return _redact_text(message, sensitive_values)[:500]


def write_operation_log(
    path: Path,
    event: str,
    message: str,
    *,
    actor: str = "app",
    component: str = "python",
    details: dict[str, Any] | None = None,
    enabled: bool = True,
    session_id: str | None = None,
    operation_id: str | None = None,
    sensitive_values: tuple[str, ...] = (),
) -> None:
    """加锁追加一条脱敏 JSON 日志；磁盘或权限错误不阻断业务操作。

    参数：path 为日志路径；event 为事件名；message 为说明；actor 为执行者；
    component 为来源组件；details 为补充信息；enabled 为写入开关；
    session_id、operation_id 为会话和操作标识；sensitive_values 为额外敏感值。
    """
    if not enabled:
        return
    payload = {
        "timestamp": datetime.now().astimezone().isoformat(timespec="milliseconds"),
        "event": event,
        "actor": actor,
        "component": component,
        "message": redact(message, sensitive_values=sensitive_values),
        "session_id": session_id or os.environ.get(OPERATION_SESSION_ENV, ""),
        "operation_id": operation_id or os.environ.get(OPERATION_ID_ENV, ""),
        "details": redact(details or {}, sensitive_values=sensitive_values),
    }
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        line = (json.dumps(payload, ensure_ascii=False, sort_keys=True) + "\n").encode("utf-8")
        fd = os.open(path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
        try:
            fcntl.flock(fd, fcntl.LOCK_EX)
            os.write(fd, line)
            os.fsync(fd)
        finally:
            try:
                fcntl.flock(fd, fcntl.LOCK_UN)
            finally:
                os.close(fd)
    except (OSError, ValueError):
        return


class OperationLogger:
    def __init__(self, path: Path, enabled: bool = True, session_id: str | None = None):
        """建立日志器；path 为文件路径，enabled 为开关，session_id 省略时读取环境或生成。"""
        self.path = path
        self.enabled = enabled
        self.session_id = session_id or os.environ.get(OPERATION_SESSION_ENV) or str(uuid.uuid4())

    def event(
        self,
        event: str,
        message: str,
        *,
        actor: str = "app",
        component: str = "python",
        details: dict[str, Any] | None = None,
        operation_id: str | None = None,
    ) -> None:
        """使用当前日志器记录事件。

        参数：event 为事件名；message 为说明；actor 为执行者；component 为来源组件；
        details 为补充信息；operation_id 为可选操作标识。
        """
        write_operation_log(
            self.path,
            event,
            message,
            actor=actor,
            component=component,
            details=details,
            enabled=self.enabled,
            session_id=self.session_id,
            operation_id=operation_id,
        )


def configure_operation_log(config: Any) -> OperationLogger:
    """建立日志器并设置子进程可继承的环境变量；config 提供状态目录和日志开关。"""
    logger = OperationLogger(config.state_dir / "operation-log.jsonl", bool(config.operation_log_enabled))
    os.environ[OPERATION_LOG_ENV] = str(logger.path)
    os.environ[OPERATION_LOG_ENABLED_ENV] = "1" if logger.enabled else "0"
    os.environ[OPERATION_SESSION_ENV] = logger.session_id
    os.environ.setdefault(OPERATION_ID_ENV, str(uuid.uuid4()))
    return logger


def log_progress_payload(payload: dict[str, Any], *, sensitive_values: tuple[str, ...] = ()) -> None:
    """保存 Playwright 进度且不重复输出；payload 为进度对象，sensitive_values 为额外敏感值。"""
    message = payload.get("message")
    if not isinstance(message, str) or not message:
        return
    details = {key: value for key, value in payload.items() if key not in {"event", "message"}}
    path_text = os.environ.get(OPERATION_LOG_ENV, "").strip()
    if not path_text:
        return
    write_operation_log(
        Path(path_text),
        "backend.progress",
        message,
        component="playwright",
        details=details,
        enabled=operation_log_enabled_from_environment(),
        sensitive_values=sensitive_values,
    )


def log_aimes_failure(
    *,
    error: str,
    code: str,
    stage: str = "",
    enabled: bool = True,
    sensitive_values: tuple[str, ...] = (),
) -> None:
    """启用日志时记录脱敏后的 AIMES 查询失败。

    参数：error 为错误说明；code 为错误码；stage 为阶段；enabled 为开关；
    sensitive_values 为额外敏感值。
    """
    path_text = os.environ.get(OPERATION_LOG_ENV, "").strip()
    if not path_text:
        return
    write_operation_log(
        Path(path_text),
        "backend.aimes.failed",
        "AIMES 数据获取失败",
        component="aimes",
        details={"code": code, "error": error, "stage": stage},
        enabled=enabled and operation_log_enabled_from_environment(),
        sensitive_values=sensitive_values,
    )


def log_database_statement(path: Path, statement: str) -> None:
    """只记录数据库写入的操作类别和表名，不记录绑定值。

    参数：path 为数据库路径；statement 为待识别的 SQL 语句。
    """
    match = _SQL_WRITE_RE.match(statement)
    if not match:
        return
    table = match.group(2).strip('"`[]')
    log_path_text = os.environ.get(OPERATION_LOG_ENV, "").strip()
    if not log_path_text:
        return
    write_operation_log(
        Path(log_path_text),
        "database.write",
        "写入本地数据库",
        component="sqlite",
        details={"database": str(path), "operation": match.group(1).lower(), "table": table},
        enabled=operation_log_enabled_from_environment(),
    )
