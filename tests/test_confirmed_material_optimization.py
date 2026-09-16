"""Server discovery must not be mistaken for a committed material write."""
import json
import os
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.order_index import (
    OrderIndexStore, preview_server_changes, scan_server_changes,
    confirm_server_material_preview_memory, confirm_server_preview_memory,
    list_order_index,
)
from tests.test_order_workflow import make_materials, make_board, make_product_catalog


class ConfirmedMaterialOptimizationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name).resolve()
        self.config = Config(state_dir=root / 'state', source_root=root / 'server', order_root=root / 'travelers')
        make_product_catalog(self.config.state_dir / 'inventory' / 'current-products.xlsx')
        self.config.prepare_storage()
        self.folder = self.config.source_root / 'PP9999'
        report = self.folder / 'Report'
        report.mkdir(parents=True)
        make_materials(self.folder / 'PP9999 materials.xlsx')
        make_board(report / 'pp-板材清单.xlsx', 'F100', 'PP9999-KITCHEN')
        self.xml = self.folder / 'Kitchen' / 'New Nesting' / 'Optimize file' / 'layout file' / 'nesting_result.xml'
        self.xml.parent.mkdir(parents=True)
        self.xml.write_text('<Nesting><BoardControl OrderID="F100" /></Nesting>')
        self.add_factory('F100', 'KITCHEN')

    def add_factory(self, factory, room):
        store = OrderIndexStore(self.config.workflow_database)
        store.upsert_aimes_factory(factory, order_id='PP9999', factory_name='PP9999-' + room,
                                  sales_order_name='PP9999', split_time='2026-09-15T08:00:00', seen_at='2026-09-15T08:00:00')
        store.summaries()
        store.commit()
        store.close()

    def state(self):
        with sqlite3.connect(self.config.workflow_database) as c:
            return {
                'factories': c.execute('select factory_order,optimized,optimization_source_path,optimization_first_completed_at,optimization_latest_completed_at from factory_orders order by factory_order').fetchall(),
                **{t: c.execute('select * from ' + t).fetchall() for t in (
                    'material_items', 'hardware_items', 'optimization_artifacts', 'server_scan_xml_state',
                    'manual_production_batches', 'outbound_documents')},
            }

    def preview(self):
        return preview_server_changes(self.config, [self.folder], include_hardware=False)['server_write_preview']

    def test_repeat_scan_and_cancel_preview_leave_no_optimization_information(self):
        before = self.state()
        first = scan_server_changes(self.config)
        self.assertTrue(first['server']['changed'])
        for _ in range(2):
            self.preview()  # Closing/abandoning the preview performs no confirmation.
            repeated = scan_server_changes(self.config)
            self.assertEqual(first['server']['changes'], repeated['server']['changes'])
            self.assertEqual(before, self.state())
        snapshot = json.loads(Path(first['server']['snapshot_path']).read_text())
        self.assertFalse(any(row['kind'].startswith('optimization') for row in snapshot['entries'].values()))
        self.assertEqual(first['orders'][0]['stage'], '已拆单待优化')

    def test_commit_is_atomic_and_survives_restart_without_duplicate_materials(self):
        payload = self.preview()
        before = self.state()
        with patch.object(OrderIndexStore, 'save_server_scan_xml_baseline', side_effect=RuntimeError('write failed')):
            with self.assertRaisesRegex(RuntimeError, 'write failed'):
                confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        self.assertEqual(before, self.state())
        self.assertTrue(scan_server_changes(self.config)['server']['changed'])
        result = confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        self.assertTrue(result['server_material_write_confirmed'])
        committed = self.state()
        self.assertTrue(committed['material_items'])
        self.assertEqual(committed['factories'][0][1], 1)
        self.assertEqual(len(committed['optimization_artifacts']), 1)
        self.assertTrue(committed['server_scan_xml_state'])
        self.assertFalse(scan_server_changes(self.config)['server']['changed'])
        self.assertEqual(committed, self.state())
        confirm_server_material_preview_memory(self.config, self.preview(), confirm_write=True)
        self.assertEqual(len(committed['material_items']), len(self.state()['material_items']))
        self.assertEqual(list_order_index(self.config)['orders'][0]['stage'], '已优化')
        self.assertEqual(self.state()['manual_production_batches'], [])
        self.assertEqual(self.state()['outbound_documents'], [])

    def test_material_confirmation_without_xml_can_complete_optimization(self):
        self.xml.unlink()
        payload = self.preview()
        confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        self.assertEqual(list_order_index(self.config)['orders'][0]['stage'], '已优化')
        self.assertEqual(self.state()['optimization_artifacts'], [])

    def test_new_aimes_factory_does_not_inherit_old_material_optimization(self):
        confirm_server_material_preview_memory(self.config, self.preview(), confirm_write=True)
        self.add_factory('F200', 'OFFICE')
        payload = self.preview()
        confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        states = {r[0]: r[1] for r in self.state()['factories']}
        self.assertEqual(states, {'F100': 1, 'F200': 0})
        self.assertEqual(list_order_index(self.config)['orders'][0]['stage'], '部分优化')

    def test_partial_factory_confirmation_keeps_remaining_file_pending(self):
        self.add_factory('F200', 'OFFICE')
        make_board(self.folder / 'Report' / 'pp-板材清单-office.xlsx', 'F200', 'PP9999-OFFICE')
        self.xml.write_text('<Nesting><BoardControl OrderID="F100" /><BoardControl OrderID="F200" /></Nesting>')
        payload = self.preview()
        confirm_server_preview_memory(self.config, payload, 'PP9999', 'F100', confirm_write=True)
        self.assertEqual({r[0]: r[1] for r in self.state()['factories']}, {'F100': 1, 'F200': 0})
        self.assertEqual(self.state()['server_scan_xml_state'], [])
        with sqlite3.connect(self.config.workflow_database) as c:
            self.assertEqual(c.execute("select stage from orders where order_id='PP9999'").fetchone()[0], '部分优化')
        self.assertTrue(scan_server_changes(self.config)['server']['changed'])
        confirm_server_preview_memory(self.config, payload, 'PP9999', 'F200', confirm_write=True)
        self.assertFalse(scan_server_changes(self.config)['server']['changed'])
        self.assertEqual(list_order_index(self.config)['orders'][0]['stage'], '已优化')

    def test_xml_changed_after_preview_is_not_accepted_as_confirmed_baseline(self):
        payload = self.preview()
        stamp = self.xml.stat()
        os.utime(self.xml, ns=(stamp.st_atime_ns, stamp.st_mtime_ns + 5_000_000_000))
        confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        changes = scan_server_changes(self.config)['server']['changes']
        self.assertTrue(any(c['path'] == str(self.xml) and c['change_type'] == 'modified' for c in changes))

    def test_factory_confirmation_cannot_claim_optimization_without_material_rows(self):
        payload = self.preview()
        payload['write_records']['material_items'] = []
        before = self.state()
        with self.assertRaises(RuleError) as error:
            confirm_server_preview_memory(self.config, payload, 'PP9999', 'F100', confirm_write=True)
        self.assertEqual(error.exception.code, 'missing_confirmed_material')
        self.assertEqual(before, self.state())


if __name__ == '__main__':
    unittest.main()
