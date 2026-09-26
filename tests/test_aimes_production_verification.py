"""AIMES 删除核验必须尊重已经完成的本地生产事实。"""
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config
from traveler_assistant.order_index import (
    OrderIndexStore, _active_aimes_factory_orders,
    _verify_missing_aimes_factories, sync_aimes_index,
)


class AimesProductionVerificationTests(unittest.TestCase):
    # 建立独立订单数据库和未完成生产的基础订单，注册资源清理。
    # self：当前测试用例或测试替身实例。
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config()
        self.config.state_dir = Path(self.temp.name) / "state"
        self.config.reconcile_outbound_on_read = False
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.store.upsert_order("PP0035", validation_status="正常")

    # 向测试数据库加入归属已确认的 AIMES 工厂单。
    # self：当前测试用例或测试替身实例。
    # number：测试工厂单编号。
    def factory(self, number):
        self.store.upsert_factory(
            number, order_id="PP0035", factory_name=f"PP0035-{number}",
            sales_order_name="PP0035", name_source="AIMES", ownership_status="已确认",
        )

    # 建立测试生产记录，并将指定工厂单关联到该记录。
    # self：当前测试用例或测试替身实例。
    # number：测试生产批次标识。
    # factories：需要关联生产记录的工厂单编号列表。
    # status：模拟生产记录状态。
    # order：所属订单编号。
    def batch(self, number, factories, status="completed", order="PP0035"):
        self.store.connection.execute(
            """insert into production_records
               (batch_id, status, created_at, updated_at)
               values (?, ?, '2026-09-17', '2026-09-17')""",
            (number, status),
        )
        self.store.connection.executemany(
            "update factory_orders set production_record_id=? where order_id=? and factory_order=?",
            [(number, order, factory) for factory in factories],
        )

    # 验证仅归属匹配且已完成的本地生产记录可排除精确核验候选。
    # self：当前测试用例或测试替身实例。
    def test_only_completed_matching_production_excludes_a_factory(self):
        for number in range(1, 7):
            self.factory(f"F{number:03}")
        self.batch(1, ["F001", "F002"])
        self.batch(2, ["F003"], status="prepared")
        self.batch(3, ["F004"], status="failed")
        self.batch(4, ["F005"], order="PP0036")
        self.assertEqual(_active_aimes_factory_orders(self.store),
                         ["F003", "F004", "F005", "F006"])
        produced = {f["factory_order"] for f in self.store.summaries()[0]["factories"] if f["produced"]}
        self.assertEqual(produced, {"F001", "F002"})

    # 验证 AIMES 查询缺失不能删除已经生产完成的工厂单。
    # self：当前测试用例或测试替身实例。
    def test_missing_result_cannot_delete_completed_factory(self):
        self.factory("F001")
        self.factory("F002")
        self.batch(1, ["F001"])
        count, error = _verify_missing_aimes_factories(
            self.config, self.store, [], verified_at="2026-09-17",
            verification_result={"rows": [], "missing": ["F001", "F002"]},
        )
        self.assertEqual((count, error), (1, ""))
        statuses = dict(self.store.connection.execute(
            "select factory_order, aimes_status from factory_orders"))
        self.assertEqual(statuses, {"F001": "active", "F002": "deleted"})
        self.assertEqual(self.store.connection.execute(
            "select status from production_records").fetchone()[0], "completed")

    # 验证最近页之外只对尚未生产的工厂单执行精确查询。
    # self：当前测试用例或测试替身实例。
    def test_fallback_queries_only_unproduced_outside_recent_page(self):
        for factory in ("F001", "F002", "F003"):
            self.factory(factory)
        self.batch(1, ["F001"])
        with patch("traveler_assistant.core.verify_aimes_factory_orders",
                   return_value={"rows": [], "missing": []}) as verify:
            _verify_missing_aimes_factories(
                self.config, self.store, [{"factory_order": "F003"}],
                verified_at="2026-09-17",
            )
        verify.assert_called_once_with(self.config, ["F002"])

    # 验证同步仅传递未生产候选，并保留已有生产事实。
    # self：当前测试用例或测试替身实例。
    def test_sync_passes_only_unproduced_candidates_and_keeps_production(self):
        self.factory("F001")
        self.factory("F002")
        self.batch(1, ["F001"])
        self.store.commit()
        recent = [{"factory_order": "F003", "factory_name": "PP0035-NEW",
                   "sales_order_name": "PP0035", "split_time": ""}]
        with patch("traveler_assistant.core.refresh_aimes_recent_orders_and_verify",
                   return_value=(recent, {"rows": [], "missing": ["F002"]})) as refresh:
            result = sync_aimes_index(self.config, force=True)
        self.assertTrue(result["aimes"]["succeeded"])
        self.assertEqual(refresh.call_args.args[1:], (50, ["F002"]))
        statuses = dict(self.store.connection.execute(
            "select factory_order, aimes_status from factory_orders"))
        self.assertEqual(statuses, {"F001": "active", "F002": "deleted", "F003": "active"})

    # 验证所有工厂单均已生产时仍读取最近页，但不执行精确查询。
    # self：当前测试用例或测试替身实例。
    def test_all_produced_still_reads_recent_page_without_exact_queries(self):
        self.factory("F001")
        self.batch(1, ["F001"])
        self.store.commit()
        with patch("traveler_assistant.core.refresh_aimes_recent_orders", return_value=[]) as recent, \
             patch("traveler_assistant.core.refresh_aimes_recent_orders_and_verify") as combined, \
             patch("traveler_assistant.core.verify_aimes_factory_orders") as exact:
            result = sync_aimes_index(self.config, force=True)
        self.assertTrue(result["aimes"]["succeeded"])
        recent.assert_called_once()
        self.assertEqual(recent.call_args.args[1], 50)
        combined.assert_not_called()
        exact.assert_not_called()
        self.assertEqual(self.store.connection.execute(
            "select aimes_status from factory_orders").fetchone()[0], "active")
