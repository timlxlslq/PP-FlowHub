import tempfile
import unittest
from contextlib import redirect_stdout
from datetime import datetime
from io import StringIO
from pathlib import Path

from traveler_assistant.assistant_cli import main as assistant_main
from traveler_assistant.database import connect_database, ensure_schema
from traveler_assistant.runtime_store import RuntimeStore, TokenUsage, runtime_database_path


class RuntimeStoreTests(unittest.TestCase):
    # 验证运行状态数据库使用独立私有文件。
    # self：当前测试用例或测试替身实例。
    def test_runtime_database_uses_a_private_file(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            self.assertEqual(runtime_database_path(state), state / "assistant-runtime.sqlite3")

    # 验证遇到未知数据库版本时保留原文件，不自动删除。
    # self：当前测试用例或测试替身实例。
    def test_unknown_database_version_is_not_deleted(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "workflow.sqlite3"
            connection = __import__("sqlite3").connect(path)
            connection.execute("pragma user_version = 8")
            connection.commit()
            connection.close()
            with self.assertRaises(RuntimeError):
                RuntimeStore(path)
            self.assertTrue(path.exists())

    # 验证助手用量记录不会写入业务数据库。
    # self：当前测试用例或测试替身实例。
    def test_assistant_usage_does_not_touch_workflow_database(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp)
            workflow = state / "workflow.sqlite3"
            ensure_schema(workflow)
            connection = connect_database(workflow)
            connection.execute(
                """insert into products(
                       category,code,name,spec,status,unit,normalized_code,
                       normalized_name,normalized_spec,normalized_category,
                       normalized_remark,material_kind,material_color,
                       material_thickness,catalog_present
                   ) values('Panel','M-RUNTIME','Woodline 4','19.1mm','启用','pcs',
                            'MRUNTIME','WOODLINE4','191MM','PANEL','',
                            'panel','Woodline 4','19.1',1)"""
            )
            connection.execute(
                """insert into material_items(
                    order_id, product_code, quantity, source_type, source_path,
                    source_fingerprint, updated_at
                ) values(?,?,?,?,?,?,?)""",
                ("CS005", "M-RUNTIME", 4, "aihouse", "fixture.xlsx", "fp", "now"),
            )
            connection.commit()
            connection.close()

            with redirect_stdout(StringIO()):
                self.assertEqual(assistant_main(["--usage", "--state-dir", str(state)]), 0)

            connection = __import__("sqlite3").connect(workflow)
            self.assertEqual(connection.execute("select count(*) from material_items").fetchone()[0], 1)
            connection.close()
            self.assertTrue(runtime_database_path(state).exists())

    # 验证 Agent 用量可按周、月及累计范围汇总。
    # self：当前测试用例或测试替身实例。
    def test_agent_usage_has_week_month_and_total_summaries(self):
        with tempfile.TemporaryDirectory() as temp:
            store = RuntimeStore(Path(temp) / "workflow.sqlite3")
            store.record_agent_usage("test-model", TokenUsage(120, 30))
            self.assertEqual(
                store.token_summary(datetime.now()),
                {"week": 150, "month": 150, "total": 150},
            )

    # 验证 Agent 路由学习按标准化后的完整短语精确匹配。
    # self：当前测试用例或测试替身实例。
    def test_agent_route_is_learned_as_an_exact_normalized_phrase(self):
        with tempfile.TemporaryDirectory() as temp:
            store = RuntimeStore(Path(temp) / "workflow.sqlite3")
            store.remember_command("帮我瞅瞅pp0063", "preview_order", {"order_id": "PP0063"})
            self.assertEqual(
                store.learned_command("帮我瞅瞅pp0063"),
                ("preview_order", {"order_id": "PP0063"}),
            )
            self.assertIsNone(store.learned_command("帮我瞅瞅pp0064"))

    # 验证学习得到的命令保留结构化参数及其类型。
    # self：当前测试用例或测试替身实例。
    def test_learned_command_preserves_typed_arguments(self):
        with tempfile.TemporaryDirectory() as temp:
            store = RuntimeStore(Path(temp) / "workflow.sqlite3")
            arguments = {
                "order_id": "PP1234-2",
                "factory_name": "PP1234-2-LAUNDRY",
                "product_code": "M0144",
                "quantity": "2",
            }
            store.remember_command("洗衣房补两个", "add_manual_hardware", arguments)
            self.assertEqual(
                store.learned_command("洗衣房补两个"),
                ("add_manual_hardware", arguments),
            )


if __name__ == "__main__":
    unittest.main()
