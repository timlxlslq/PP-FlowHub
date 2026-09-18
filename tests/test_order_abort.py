import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.order_index import OrderIndexStore, abort_order, _reconcile_temporary_order_projections
from traveler_assistant.production import production_preview, prepare_production, assert_shipment_allowed
from traveler_assistant.inventory import run_jdy
from traveler_assistant.order_workflow import main


class OrderAbortTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config(state_dir=Path(self.temp.name) / 'state')
        self.config.prepare_storage()
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.store.upsert_order('PP0100')
        self.store.connection.execute(
            """insert into factory_orders(factory_order, order_id, factory_name,
               ownership_status, stage, updated_at) values('F100','PP0100','Kitchen','已确认','已生产','before')"""
        )
        self.store.commit()

    def test_requires_confirmation_and_known_order(self):
        for order, confirmed in [('PP0100', False), ('PP9999', True), ('', True)]:
            with self.assertRaises(RuleError):
                abort_order(self.config, order, confirmed=confirmed)
        self.assertNotEqual(self.store.connection.execute("select stage from orders").fetchone()[0], '已中止')

    def test_terminal_decision_survives_refresh_upsert_restart_and_new_factory(self):
        before = self.store.connection.execute('select * from factory_orders').fetchall()
        result = abort_order(self.config, ' pp0100 ', confirmed=True)
        self.assertEqual(result['orders'][0]['stage'], '已中止')
        self.assertEqual(before, self.store.connection.execute('select * from factory_orders').fetchall())
        stamp = self.store.connection.execute('select updated_at from orders').fetchone()[0]
        abort_order(self.config, 'PP0100', confirmed=True)
        self.assertEqual(stamp, self.store.connection.execute('select updated_at from orders').fetchone()[0])
        self.store.upsert_order('PP0100', stage='已优化', aimes_seen='later')
        self.store.connection.execute(
            """insert into factory_orders(factory_order, order_id, factory_name,
               ownership_status, updated_at) values('F101','PP0100','Bath','已确认','later')"""
        )
        self.store.commit()
        reopened = OrderIndexStore(self.config.workflow_database)
        try:
            for persist in (False, True):
                self.assertEqual(reopened.summaries(persist=persist)[0]['stage'], '已中止')
        finally:
            reopened.close()

    def test_aborted_without_active_factories_remains_visible(self):
        abort_order(self.config, 'PP0100', confirmed=True)
        self.store.connection.execute("update factory_orders set aimes_status='deleted'")
        self.store.commit()
        self.assertEqual(self.store.summaries()[0]['stage'], '已中止')

    def test_aborted_temporary_order_is_not_removed_by_projection_cleanup(self):
        self.store.connection.execute("update orders set order_type='temporary'")
        self.store.commit()
        abort_order(self.config, 'PP0100', confirmed=True)
        _reconcile_temporary_order_projections(self.store)
        self.assertEqual(self.store.summaries()[0]['stage'], '已中止')

    def test_production_shipment_and_stale_request_blocked_before_external_access(self):
        abort_order(self.config, 'PP0100', confirmed=True)
        calls = [
            lambda: production_preview(self.config, 'PP0100', ['F100']),
            lambda: prepare_production(self.config, 'PP0100', ['F100'], []),
            lambda: assert_shipment_allowed(self.config, 'PP0100', ['F100']),
            lambda: run_jdy(self.config, 'outbound', order_id='PP0100', confirm_save=True,
                            production_request_id='old-request', production_materials=[]),
            lambda: run_jdy(self.config, 'outbound', order_id='PP0100', confirm_save=True,
                            shipment_only=True, selected_factory_orders=['F100']),
        ]
        with patch('traveler_assistant.inventory._find_existing_inventory_page', side_effect=AssertionError('external access')):
            for call in calls:
                with self.assertRaisesRegex(RuleError, '已中止'):
                    call()

    def test_cli_requires_confirmation(self):
        for confirmed in (False, True):
            sink = {}
            args = ['abort-order', '--order-id', 'PP0100'] + (['--confirm-write'] if confirmed else [])
            code = main(args, config_override=self.config, emit_result=False, result_sink=sink)
            self.assertEqual(code, 0 if confirmed else 2)
            if confirmed:
                self.assertEqual(sink['value']['stage'], '已中止')
