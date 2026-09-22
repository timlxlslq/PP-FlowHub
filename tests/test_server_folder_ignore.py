"""Review-only folder ignores, isolated from completion and inventory facts."""
import tempfile
import unittest
from datetime import datetime, timedelta
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config
from traveler_assistant.order_index import (
    OrderIndexStore, ignore_server_folder,
    scan_server_changes, sync_order_index, _server_folders_for_sync,
)


class ServerFolderIgnoreTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.config = Config(state_dir=root / 'state', source_root=root / 'source')
        self.folder = self.config.source_root / 'TEST_IGNORE'
        self.folder.mkdir(parents=True)
        self.report = self.folder / 'Fittingslist.xlsx'
        self.report.write_bytes(b'not a workbook; ignore must not parse it')
        self.xml = self.folder / 'Optimize file.xml'
        self.xml.write_text('<Root/>')
        self.addCleanup(patch.stopall)
        patch('traveler_assistant.inventory.run_jdy', side_effect=AssertionError('no inventory')).start()

    def row(self):
        store = OrderIndexStore(self.config.workflow_database)
        row = store.connection.execute('select * from server_folder_ignores where path=?', (str(self.folder),)).fetchone()
        store.close()
        return row

    def test_ignore_persists_without_business_baselines_or_rescan(self):
        store = OrderIndexStore(self.config.workflow_database)
        store.upsert_aimes_factory('F100', order_id='PP0008', factory_name='PP0008 Kitchen', sales_order_name='PP0008', split_time='2026-09-18T10:00:00', seen_at='2026-09-18T10:00:00')
        tables = ['orders', 'factory_orders', 'temporary_orders', 'source_files', 'server_scan_xml_state', 'material_items', 'hardware_items']
        before = {table: store.connection.execute(f'select * from {table}').fetchall() for table in tables}
        store.commit()
        store.close()
        with patch('traveler_assistant.order_index.scan_server_changes', side_effect=AssertionError('no full scan')):
            result = ignore_server_folder(self.config, self.folder)
        self.assertTrue(result['ok'])
        store = OrderIndexStore(self.config.workflow_database)
        self.assertEqual(before, {table: store.connection.execute(f'select * from {table}').fetchall() for table in tables})
        store.close()
        self.assertIsNotNone(self.row())
        self.assertEqual(scan_server_changes(self.config)['server']['changes'], [])
        self.assertEqual(scan_server_changes(self.config)['server']['changes'], [])
        _, folders = _server_folders_for_sync(self.config, None)
        self.assertNotIn(self.folder, folders)

    def test_repeat_keeps_original_record(self):
        ignore_server_folder(self.config, self.folder)
        first = self.row()
        with patch('traveler_assistant.order_index._now', return_value=(datetime.now()+timedelta(days=2)).isoformat()):
            self.assertTrue(ignore_server_folder(self.config, self.folder)['unchanged'])
        self.assertEqual(first, self.row())

    def test_changes_never_reopen_and_contents_are_not_observed(self):
        ignore_server_folder(self.config, self.folder)
        self.report.write_bytes(b'changed report')
        self.xml.unlink()
        (self.folder / 'nesting_result.xml').write_text('<New/>')
        with patch('traveler_assistant.order_index._report_files', side_effect=AssertionError('no report discovery')), \
             patch('traveler_assistant.order_index._server_optimization_monitor_files', side_effect=AssertionError('no XML watch')):
            self.assertEqual(scan_server_changes(self.config)['server']['changes'], [])
            _, folders = _server_folders_for_sync(self.config, None)
            self.assertNotIn(self.folder, folders)
        with patch('traveler_assistant.order_index._now', return_value=(datetime.now()+timedelta(days=60)).isoformat()):
            self.assertEqual(scan_server_changes(self.config)['server']['changes'], [])

    def test_scope_rejections(self):
        standard = self.config.source_root / 'PP0008'
        standard.mkdir()
        for folder in (standard, self.config.source_root, self.folder / 'nested', self.config.state_dir):
            with self.subTest(folder=folder), self.assertRaises(ValueError):
                ignore_server_folder(self.config, folder)
        self.assertIsNone(self.row())

    def test_reportless_mixed_can_be_ignored_but_reported_mixed_cannot(self):
        mixed = self.config.source_root / 'PP0008 PP0035'
        mixed.mkdir()
        ignore_server_folder(self.config, mixed)
        (mixed / 'Fittingslist.xlsx').write_bytes(b'report')
        with self.assertRaisesRegex(ValueError, '混单'):
            ignore_server_folder(self.config, mixed)

    def test_transaction_failure_rolls_back(self):
        with patch.object(OrderIndexStore, 'add_change', side_effect=RuntimeError('write failed')):
            with self.assertRaisesRegex(RuntimeError, 'write failed'):
                ignore_server_folder(self.config, self.folder)
        self.assertIsNone(self.row())

    def test_confirmed_baseline_does_not_reset_ignore(self):
        ignore_server_folder(self.config, self.folder)
        first = self.row()
        store = OrderIndexStore(self.config.workflow_database)
        store.save_server_scan_xml_baseline([self.folder], [], observed_at=datetime.now().isoformat())
        store.commit()
        store.close()
        self.assertEqual(self.row(), first)

    def test_old_scan_snapshot_cannot_reintroduce_ignored_folder(self):
        scan = scan_server_changes(self.config)
        snapshot = Path(scan['server']['snapshot_path'])
        ignore_server_folder(self.config, self.folder)
        with patch('traveler_assistant.order_index._server_folders_for_sync', side_effect=AssertionError('must reuse snapshot')), \
             patch('traveler_assistant.order_workflow.parse_fittings_groups', side_effect=AssertionError('ignored report must not be parsed')):
            result = sync_order_index(self.config, server_snapshot_path=snapshot,
                                      refresh_outbound_statuses=False, reconcile_outbound=False)
        self.assertTrue(result['index_stats']['server_snapshot_reused'])
        self.assertEqual(result['index_stats']['server_snapshot_entry_count'], 0)

    def test_only_target_issues_close_and_rollback_preserves_them(self):
        store = OrderIndexStore(self.config.workflow_database)
        for key, path in [('target', str(self.report)), ('other', str(self.folder)+'_OTHER/report.xlsx')]:
            store.upsert_active_issue(issue_key=key, kind='temporary_processing', path=path, message='failed')
        store.commit()
        store.close()
        with patch.object(OrderIndexStore, 'resolve_active_issue', side_effect=RuntimeError('resolve failed')):
            with self.assertRaises(RuntimeError):
                ignore_server_folder(self.config, self.folder)
        self.assertIsNone(self.row())
        result = ignore_server_folder(self.config, self.folder)
        self.assertEqual([item['issue_key'] for item in result['current_issues']], ['other'])

    def test_normalized_symlink_path_and_other_folder_stays_pending(self):
        link = Path(self.temp.name) / 'alias'
        link.symlink_to(self.config.source_root, target_is_directory=True)
        other = self.config.source_root / 'OTHER_TEST'
        other.mkdir()
        (other / 'Fittingslist.xlsx').write_bytes(b'other')
        ignore_server_folder(self.config, link / self.folder.name)
        self.assertEqual(self.row()[0], str(self.folder))
        changes = scan_server_changes(self.config)['server']['changes']
        self.assertTrue(changes)
        self.assertTrue(all(c['source_folder'] == str(other) for c in changes))


if __name__ == '__main__':
    unittest.main()
