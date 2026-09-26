"""日志诊断回归：临时文件及隔离服务，禁止外部业务调用。"""
import io
import json
import os
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from traveler_assistant import operation_log, order_service
from traveler_assistant.core import Config
from traveler_assistant.order_workflow import main as order_main


class LogDiagnosticsTests(unittest.TestCase):
    # 验证日志网址凭据已隐藏，同时保留安全的来源主机名。
    def test_url_credentials_are_removed_without_losing_source_host(self):
        text = operation_log.redact("https://private-user:private-password@example.com/report?token=private-token#private-fragment")
        self.assertEqual(text, "https://example.com/report")

    # 验证敏感输入先脱敏再截断，且 JSON 与 Authorization 凭据不会泄漏。
    def test_rule_error_redacts_before_truncating_known_long_input(self):
        private_input = "private-user-text" * 50
        text = operation_log.safe_rule_error_text(private_input, sensitive_values=(private_input,))
        self.assertNotIn("private-user-text", text)
        for message, secret in [('{"password": "private-json"}', "private-json"),
                                ("Authorization: Bearer private-bearer", "private-bearer")]:
            self.assertNotIn(secret, operation_log.safe_rule_error_text(message))

    # 验证订单命令失败后只记录安全的代码位置和业务身份。
    def test_order_failure_persists_safe_location_and_identity(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ):
            config = Config(state_dir=Path(temp))
            # 模拟详情读取失败；args 为订单详情命令的参数。
            def broken_detail(*args):
                raise RuntimeError("password=never-store-me")
            with patch("traveler_assistant.order_details.order_detail", side_effect=broken_detail):
                result = order_main(["detail", "--order-id", "PP0064", "--factory-order", "F2609020242"],
                                    config_override=config, emit_result=False)
            self.assertEqual(result, 2)
            text = (Path(temp) / "operation-log.jsonl").read_text()
            failed = [json.loads(line) for line in text.splitlines() if json.loads(line)["event"] == "backend.command.failed"]
            self.assertEqual(len(failed), 1)
            details = failed[0]["details"]
            self.assertEqual(details["exception_type"], "RuntimeError")
            self.assertEqual(details["order_id"], "PP0064")
            self.assertIn("broken_detail", json.dumps(details))
            self.assertNotIn("never-store-me", text)

    # 验证常驻服务按请求开关记录操作，包括缓存命中请求。
    def test_resident_requests_toggle_logging_including_cache_hits(self):
        with tempfile.TemporaryDirectory() as temp, patch.dict(os.environ):
            root = Path(temp)
            database = root / "workflow.sqlite3"
            config = SimpleNamespace(state_dir=root, operation_log_enabled=True)
            calls = []
            enabled_states = []

            # 模拟后台命令并记录日志开关；arguments 为命令参数，kwargs 为依赖注入上下文。
            def fake_main(arguments, **kwargs):
                calls.append(arguments[0])
                enabled_states.append(kwargs["config_override"].operation_log_enabled)
                kwargs["logger_override"].event("backend.command.completed", "测试请求")
                operation_log.log_database_statement(database, "UPDATE orders SET stage='fixture'")
                kwargs["result_sink"]["value"] = {"orders": []}
                return 0

            requests = [
                {"id": "off-cold", "arguments": ["list-index"], "operation_log_enabled": False},
                {"id": "on-cache", "arguments": ["list-index"], "operation_log_enabled": True},
                {"id": "off-cache", "arguments": ["list-index"], "operation_log_enabled": False},
                {"id": "on-work", "arguments": ["detail"], "operation_log_enabled": True},
                {"id": "off-work", "arguments": ["detail"], "operation_log_enabled": False},
                {"id": "end", "command": "shutdown"},
            ]
            with patch.object(order_service, "_config", return_value=config), \
                 patch.object(order_service, "main", side_effect=fake_main), \
                 patch("sys.stdin", io.StringIO("\n".join(map(json.dumps, requests)))), \
                 patch("sys.stdout", io.StringIO()):
                self.assertEqual(order_service.serve(), 0)
            rows = [json.loads(line) for line in (root / "operation-log.jsonl").read_text().splitlines()]
            self.assertEqual({row["operation_id"] for row in rows}, {"on-cache", "on-work"})
            self.assertTrue(any(row["event"] == "backend.model.cache_hit" for row in rows))
            self.assertTrue(any(row["event"] == "database.write" for row in rows))
            self.assertEqual(calls, ["list-index", "detail", "detail"])
            self.assertEqual(enabled_states, [False, True, False])

    # 验证异常摘要限制堆栈长度，并排除源码、局部变量和异常文本。
    def test_exception_context_is_bounded_and_omits_source_locals_and_message(self):
        # 构造含敏感局部值的失败调用，供摘要脱敏检查。
        def fail():
            private_value = "secret-local-value"
            raise RuntimeError("secret-exception-value " + private_value)

        try:
            fail()
        except RuntimeError as exc:
            details = operation_log.safe_exception_details(
                exc, action="detail", order_id="PP0064", factory_order="F2609020242"
            )
        encoded = json.dumps(details)
        self.assertEqual(details["exception_type"], "RuntimeError")
        self.assertIn("PP0064", encoded)
        self.assertIn("F2609020242", encoded)
        self.assertIn("fail", encoded)
        self.assertNotIn("secret-local-value", encoded)
        self.assertNotIn("secret-exception-value", encoded)
        self.assertNotIn("raise RuntimeError", encoded)
        self.assertLess(len(encoded), 5000)


if __name__ == "__main__":
    unittest.main()
