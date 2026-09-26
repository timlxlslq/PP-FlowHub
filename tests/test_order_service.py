import io
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from traveler_assistant import order_service


class OrderServiceTests(unittest.TestCase):
    # 验证确认操作响应不会覆盖订单列表索引缓存。
    # self：当前测试用例或测试替身实例。
    def test_confirmation_response_cannot_replace_list_index_cache(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            database = root / "workflow.sqlite3"
            config = SimpleNamespace(state_dir=root, workflow_database=database)
            calls = []
            events = []
            list_calls = 0

            class Logger:
                # 记录发送的事件位置参数和关键字参数。
                # self：当前测试用例或测试替身实例。
                # args：转发给被模拟接口的位置参数。
                # kwargs：转发给被模拟接口的关键字参数。
                def event(self, *args, **kwargs):
                    events.append((args, kwargs))

            # 模拟确认和列表命令的不同响应，跟踪列表读取次数。
            # arguments：模拟 CLI 的参数列表。
            # kwargs：转发给被模拟接口的关键字参数。
            def fake_main(arguments, **kwargs):
                nonlocal list_calls
                calls.append(list(arguments))
                if arguments[0] == "confirm-server-material-preview-memory":
                    kwargs["result_sink"]["value"] = {
                        "server_write_confirmed": True,
                        "orders": ["PP0062"],
                    }
                elif arguments[0] == "list-index":
                    list_calls += 1
                    kwargs["result_sink"]["value"] = {
                        "orders": [{"order_id": "PP0062", "stage": "已设计" if list_calls == 1 else "已优化"}],
                    }
                else:
                    raise AssertionError(arguments)
                return 0

            requests = [
                {"id": "list-0", "arguments": ["list-index"]},
                {"id": "confirm-1", "arguments": ["confirm-server-material-preview-memory"]},
                {"id": "list-1", "arguments": ["list-index"]},
                {"id": "list-2", "arguments": ["list-index"]},
                {"id": "shutdown", "command": "shutdown", "arguments": []},
            ]
            stdin = io.StringIO(
                "\n".join(json.dumps(item, ensure_ascii=False) for item in requests) + "\n"
            )
            stdout = io.StringIO()
            with patch.object(order_service, "_config", return_value=config), \
                 patch.object(order_service, "database_path", return_value=database), \
                 patch.object(order_service, "configure_operation_log", return_value=Logger()), \
                 patch.object(order_service, "main", side_effect=fake_main), \
                 patch.object(order_service, "install_shared_workflow_connection"), \
                 patch.object(order_service, "clear_shared_workflow_connection"), \
                 patch("sys.stdin", stdin), patch("sys.stdout", stdout):
                self.assertEqual(order_service.serve(), 0)

            responses = [json.loads(line) for line in stdout.getvalue().splitlines()]
            self.assertEqual(calls, [
                ["list-index"],
                ["confirm-server-material-preview-memory"],
                ["list-index"],
            ])
            self.assertEqual(responses[0]["orders"], [{"order_id": "PP0062", "stage": "已设计"}])
            self.assertEqual(responses[1]["orders"], ["PP0062"])
            self.assertEqual(responses[2]["orders"], [{"order_id": "PP0062", "stage": "已优化"}])
            self.assertEqual(responses[3], responses[2])
            self.assertTrue(any(args[0] == "backend.model.cache_hit" for args, _ in events))


if __name__ == "__main__":
    unittest.main()
