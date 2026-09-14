import json
import os
import tempfile
import unittest
from pathlib import Path
from subprocess import CalledProcessError
from unittest.mock import patch

from traveler_assistant.core import (
    AIMES_BULK_FETCH_LIMIT,
    Config,
    RuleError,
    _normalize_name,
    _extract_aimes_failure,
    _aimes_failure_code,
    lookup_aimes_names,
    lookup_aimes_recent_orders,
    refresh_aimes_recent_orders_and_verify,
    verify_aimes_factory_orders,
)


class CoreTests(unittest.TestCase):
    def test_aimes_failure_parser_ignores_progress_and_prefers_final_error(self):
        stderr = "\n".join([
            json.dumps({"event": "progress", "message": "登录 AIMES 完成", "stage": "login"}, ensure_ascii=False),
            "AIMES 自动查询失败：AIMES 工厂订单表缺少必要列；当前页面：https://aimes.example/oms/factoryOrder?token=secret#fragment",
        ])
        self.assertEqual(_extract_aimes_failure(stderr), "AIMES 工厂订单表缺少必要列")
        self.assertEqual(_aimes_failure_code(_extract_aimes_failure(stderr)), "aimes_table_schema")
        self.assertNotEqual(_aimes_failure_code(_extract_aimes_failure(stderr)), "aimes_credentials")

    def test_aimes_table_not_ready_has_distinct_classification(self):
        error = "AIMES_TABLE_NOT_READY：AIMES 工厂订单表尚未加载完成；表头=；行数=0；可见加载状态=否"
        self.assertEqual(_aimes_failure_code(error), "aimes_table_not_ready")

    def test_aimes_table_schema_still_has_schema_classification(self):
        error = "AIMES 工厂订单表缺少必要列；当前表头：订单号 | 工厂名称"
        self.assertEqual(_aimes_failure_code(error), "aimes_table_schema")

    def test_aimes_failure_logs_final_error_with_credentials_and_url_redacted(self):
        username = 'qa"account'
        password = 'test fixture "password"'
        final_payload = json.dumps({"username": username, "password": password}, ensure_ascii=False)
        stderr = "\n".join([
            json.dumps({
                "event": "progress",
                "message": "登录 AIMES 完成",
                "stage": "login",
                "page_url": f"https://aimes.example/login?username={username}#session",
            }, ensure_ascii=False),
            f"AIMES 自动查询失败：AIMES 工厂订单表缺少必要列；payload={final_payload}；当前页面=https://aimes.example/oms/factoryOrder?password={password}#fragment",
        ])

        def fail_with_progress(command, *, input_text, env, timeout, on_stderr_line):
            for line in stderr.splitlines():
                on_stderr_line(line)
            raise CalledProcessError(1, command, stderr=stderr)

        with tempfile.TemporaryDirectory() as temp:
            log_path = Path(temp) / "operation-log.jsonl"
            config = Config(
                state_dir=Path(temp),
                aimes_username=username,
            )
            with patch.dict(os.environ, {
                "WORKFLOW_OPERATION_LOG": str(log_path),
                "WORKFLOW_OPERATION_LOG_ENABLED": "1",
            }, clear=False), patch(
                "traveler_assistant.core.subprocess.check_output",
                return_value=password,
            ), patch(
                "traveler_assistant.core.run_with_progress",
                side_effect=fail_with_progress,
            ):
                with self.assertRaises(RuleError) as raised:
                    lookup_aimes_names(config, ["F100"])

            self.assertEqual(raised.exception.code, "aimes_table_schema")
            content = log_path.read_text(encoding="utf-8")
            self.assertIn('"event": "backend.aimes.failed"', content)
            self.assertIn("AIMES 工厂订单表缺少必要列", content)
            self.assertNotIn(username, content)
            self.assertNotIn(password, content)
            self.assertNotIn(json.dumps(username, ensure_ascii=True)[1:-1], content)
            self.assertNotIn(json.dumps(password, ensure_ascii=True)[1:-1], content)
            self.assertNotIn("username=", content)
            self.assertNotIn("password=", content)
            self.assertNotIn("?token=", content)
            self.assertNotIn("#fragment", content)

    def test_aimes_real_credential_error_keeps_credential_classification(self):
        stderr = "\n".join([
            json.dumps({"event": "progress", "message": "登录 AIMES 完成", "stage": "login"}, ensure_ascii=False),
            "AIMES 自动查询失败：账号或密码错误",
        ])
        with tempfile.TemporaryDirectory() as temp:
            log_path = Path(temp) / "operation-log.jsonl"
            config = Config(state_dir=Path(temp), aimes_username="qa-account")
            with patch.dict(os.environ, {
                "WORKFLOW_OPERATION_LOG": str(log_path),
                "WORKFLOW_OPERATION_LOG_ENABLED": "1",
            }, clear=False), patch(
                "traveler_assistant.core.subprocess.check_output",
                return_value="password",
            ), patch(
                "traveler_assistant.core.run_with_progress",
                side_effect=CalledProcessError(1, ["node"], stderr=stderr),
            ):
                with self.assertRaises(RuleError) as raised:
                    lookup_aimes_names(config, ["F100"])
            self.assertEqual(raised.exception.code, "aimes_credentials")
            rows = [json.loads(line) for line in log_path.read_text(encoding="utf-8").splitlines()]
            failure = next(row for row in rows if row["event"] == "backend.aimes.failed")
            self.assertEqual(failure["details"]["code"], "aimes_credentials")

    def test_aimes_failure_log_respects_disabled_operation_logging(self):
        stderr = "AIMES 自动查询失败：账号或密码错误\n"
        with tempfile.TemporaryDirectory() as temp:
            log_path = Path(temp) / "operation-log.jsonl"
            config = Config(
                state_dir=Path(temp),
                aimes_username="qa-account",
                operation_log_enabled=False,
            )
            with patch.dict(os.environ, {
                "WORKFLOW_OPERATION_LOG": str(log_path),
                "WORKFLOW_OPERATION_LOG_ENABLED": "0",
            }, clear=False), patch(
                "traveler_assistant.core.subprocess.check_output",
                return_value="password",
            ), patch(
                "traveler_assistant.core.run_with_progress",
                side_effect=CalledProcessError(1, ["node"], stderr=stderr),
            ):
                with self.assertRaises(RuleError):
                    lookup_aimes_names(config, ["F100"])
            self.assertFalse(log_path.exists())
    def test_aimes_bulk_defaults_to_50_but_exact_lookup_has_no_bulk_limit(self):
        config = Config()
        with patch(
            "traveler_assistant.core._run_aimes_lookup",
            return_value={"rows": []},
        ) as lookup:
            lookup_aimes_recent_orders(config)
            self.assertEqual(lookup.call_args.kwargs["recent_limit"], AIMES_BULK_FETCH_LIMIT)

        with patch(
            "traveler_assistant.core._run_aimes_lookup",
            return_value={"F100": "PP0035-KITCHEN"},
        ) as lookup:
            self.assertEqual(lookup_aimes_names(config, ["F100"]), {"F100": "PP0035-KITCHEN"})
            self.assertEqual(lookup.call_args.kwargs["recent_limit"], 0)

    def test_name_normalization(self):
        self.assertEqual(_normalize_name("pp0047-kitchen"), "PP0047KITCHEN")
        self.assertEqual(_normalize_name("PP0047 kitchen"), "PP0047KITCHEN")

    def test_exact_aimes_verification_preserves_missing_rows_as_a_distinct_result(self):
        config = Config()
        with patch(
            "traveler_assistant.core._run_aimes_lookup",
            return_value={
                "rows": [{
                    "factory_order": "F100",
                    "factory_name": "PP0035-KITCHEN",
                    "sales_order_name": "PP0035",
                    "split_time": "2026-08-16 10:00:00",
                }],
                "missing": ["F101"],
            },
        ) as lookup:
            result = verify_aimes_factory_orders(config, ["F100", "F101"])
        self.assertEqual(result["rows"][0]["factory_order"], "F100")
        self.assertEqual(result["missing"], ["F101"])
        self.assertTrue(lookup.call_args.kwargs["verify_factory_orders"])

    def test_recent_fetch_and_exact_verification_share_one_lookup_session(self):
        config = Config()
        with patch(
            "traveler_assistant.core._run_aimes_lookup",
            return_value={
                "rows": [{
                    "factory_order": "F100",
                    "factory_name": "PP0035-KITCHEN",
                    "sales_order_name": "PP0035",
                    "split_time": "2026-08-16 10:00:00",
                }],
                "verify_rows": [{
                    "factory_order": "F099",
                    "factory_name": "PP0034-KITCHEN",
                    "sales_order_name": "PP0034",
                    "split_time": "",
                }],
                "missing": ["F101"],
                "_aimes_timings": [
                    {"stage": "login", "label": "登录 AIMES", "duration_seconds": 1.2},
                    {"stage": "attempt", "label": "获取 AIMES 数据成功，总计用时", "duration_seconds": 9.9},
                ],
            },
        ) as lookup:
            timings = []
            rows, verification = refresh_aimes_recent_orders_and_verify(
                config,
                50,
                ["F099", "F101"],
                timing_sink=timings,
            )
        self.assertEqual(rows[0]["factory_order"], "F100")
        self.assertEqual(verification["rows"][0]["factory_order"], "F099")
        self.assertEqual(verification["missing"], ["F101"])
        self.assertEqual(timings[0]["label"], "登录 AIMES")
        self.assertFalse(any("总计用时" in item["label"] for item in timings))
        self.assertEqual(lookup.call_args.kwargs["recent_limit"], 50)
        self.assertTrue(lookup.call_args.kwargs["verify_factory_orders"])

    def test_settings_load_only_runtime_paths_and_cutoff(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            (state / "settings.json").write_text(json.dumps({
                "initial_date": "2026-07-22",
                "source_root": "/tmp/orders",
                "template": "/tmp/old-template.xlsx",
                "obsolete_setting": "ignored",
            }))
            config = Config(state_dir=state)
            bundled_template = config.template
            config.load_settings()
            self.assertEqual(config.initial_date, "2026-07-22")
            self.assertEqual(config.source_root, Path("/tmp/orders"))
            self.assertEqual(config.template, bundled_template)

    def test_invalid_cutoff_date_is_rejected(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            (state / "settings.json").write_text('{"initial_date":"07/22/2026"}')
            with self.assertRaises(RuleError) as raised:
                Config(state_dir=state).load_settings()
            self.assertEqual(raised.exception.code, "settings_invalid")

    def test_server_profile_uses_production_paths_when_active_source_is_local(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            (state / "settings.json").write_text(json.dumps({
                "source_root": "/tmp/test/Optimized Orders",
                "order_root": "/tmp/test/Generated Travelers",
                "backup_root": "/tmp/test/Backups",
                "server_source_root": "/Volumes/server/Optimized Orders",
                "production_order_root": "/tmp/production/Order",
                "production_backup_root": "/tmp/production/Backups",
            }))
            config = Config(state_dir=state)
            config.load_settings(source_profile="server")
            self.assertEqual(config.source_root, Path("/Volumes/server/Optimized Orders"))
            self.assertEqual(config.order_root, Path("/tmp/production/Order"))
            self.assertEqual(config.backup_root, Path("/tmp/production/Backups"))

    def test_aimes_username_is_loaded_without_loading_a_password(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            (state / "settings.json").write_text(json.dumps({"aimes_username": "factory-user"}))
            config = Config(state_dir=state)
            config.load_settings()
            self.assertEqual(config.aimes_username, "factory-user")
            self.assertFalse(hasattr(config, "aimes_password"))

    def test_local_profile_derives_all_isolated_paths(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            local = state / "test-source"
            (state / "settings.json").write_text(json.dumps({"local_test_root": str(local)}))
            config = Config(state_dir=state)
            config.load_settings(source_profile="local")
            self.assertEqual(config.source_root, local / "Optimized Orders")
            self.assertEqual(config.order_root, local / "Generated Travelers")
            self.assertEqual(config.backup_root, local / "Backups")

    def test_operation_log_setting_is_loaded_and_defaults_to_enabled(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            self.assertTrue(Config(state_dir=state).operation_log_enabled)
            (state / "settings.json").write_text(json.dumps({"operation_log_enabled": False}))
            config = Config(state_dir=state)
            config.load_settings()
            self.assertFalse(config.operation_log_enabled)
            self.assertEqual(config.operation_log_file, state / "operation-log.jsonl")


if __name__ == "__main__":
    unittest.main()
