"""Independent folder completion: no production inventory or order facts are rewritten."""
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.order_index import (
    OrderIndexStore, _server_folder_handling_mode, mark_temporary_folder_manual,
    preview_server_changes, scan_server_changes, sync_order_index,
)


class FolderManualHandlingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.config = Config(state_dir=root / 'state', source_root=root / 'source')
        self.config.source_root.mkdir()
        self.inventory = patch('traveler_assistant.inventory.run_jdy', side_effect=AssertionError('inventory must not be called')).start()
        self.addCleanup(patch.stopall)

    def folder(self, name='PP0008-GLASSCABINET AND PP0035 PANELS'):
        folder = self.config.source_root / name
        xml = folder / 'New Nesting' / 'Optimize file'
        (xml / 'layout file').mkdir(parents=True)
        (xml / 'Optimize file.xml').write_text('<Optimize />')
        (xml / 'layout file' / 'nesting_result.xml').write_text('<Nesting />')
        (folder / 'Report').mkdir()
        # Invalid workbook proves manual completion/metadata scanning does not parse Excel.
        (folder / 'Report' / 'Fittingslist.xlsx').write_bytes(b'not-an-excel-file')
        return folder

    def seed(self):
        store = OrderIndexStore(self.config.workflow_database)
        store.connection.executemany(
            """insert into products(
                   category,code,name,spec,status,unit,normalized_code,
                   normalized_name,normalized_spec,normalized_category,
                   normalized_remark,material_kind,material_color,
                   material_thickness,catalog_present
               ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
            [
                ("Panel", "M-WHITE", "White", "19mm", "启用", "pcs",
                 "MWHITE", "WHITE", "19MM", "PANEL", "", "panel", "White", "19"),
                ("Hardware", "HINGE", "Hinge", "", "启用", "pcs",
                 "HINGE", "HINGE", "", "HARDWARE", "", "", "", ""),
            ],
        )
        for order, factory in [('PP0008', 'F100'), ('PP0035', 'F101')]:
            store.upsert_aimes_factory(factory, order_id=order, factory_name=order+' KITCHEN', sales_order_name=order, split_time='2026-09-01T08:00:00', seen_at='2026-09-01T08:00:00')
            store.connection.execute("update factory_orders set outbound_status='已出库', outbound_document='OLD-DOC', outbound_completed_at='2026-09-10T10:00:00' where factory_order=?", (factory,))
            store.save_server_scan_policy(order, policy='permanent', aimes_fingerprint='', updated_at='2026-09-10T10:00:00')
        store.connection.execute("insert into material_items(order_id,product_code,quantity,source_type,source_path,source_fingerprint,updated_at) values('PP0008','M-WHITE',2,'aihouse','/old/report','old','2026-09-10')")
        store.connection.execute("insert into hardware_items(order_id,factory_order,product_code,name,spec,quantity,unit,source_type,source_path,active,updated_at) values('PP0008','F100','HINGE','Hinge','',2,'pcs','aicnc','/old/fittings',1,'2026-09-10')")
        store.connection.execute("insert into manual_production_batches(batch_id,batch_number,order_id,production_time,source,status,created_at,updated_at) values(1,'MP-OLD','PP0008','2026-09-10','manual','completed','2026-09-10','2026-09-10')")
        store.connection.execute("insert into manual_production_batch_factories(batch_id,order_id,factory_order) values(1,'PP0008','F100')")
        store.commit(); store.close()

    def record(self, folder):
        store = OrderIndexStore(self.config.workflow_database)
        result = store.temporary_order(str(folder))
        store.close()
        return result

    def facts(self):
        store = OrderIndexStore(self.config.workflow_database)
        result = {name: store.connection.execute('select * from '+name).fetchall() for name in [
            'orders', 'factory_orders', 'material_items', 'hardware_items',
            'manual_production_batches', 'manual_production_batch_factories', 'outbound_documents',
        ]}
        store.close()
        return result

    def change_xml(self, folder):
        path = folder / 'New Nesting' / 'Optimize file' / 'Optimize file.xml'
        path.write_text('<Optimize changed="true" />')
        os.utime(path, (path.stat().st_atime, path.stat().st_mtime + 2))

    def test_shipped_mixed_supplement_is_independent_and_can_have_no_references(self):
        folder = self.folder(); self.seed()
        before = self.facts()
        scan = scan_server_changes(self.config)
        self.assertTrue(scan['server']['changes'])
        self.assertTrue(all(row['handling_mode'] == 'supplemental' and row['manual_only'] for row in scan['server']['changes']))
        self.assertEqual(before, self.facts())
        result = mark_temporary_folder_manual(self.config, folder, reference_order_ids=[], outbound_document='EXTERNAL-ONLY')
        self.assertEqual(result['reference_order_ids'], [])
        record = self.record(folder)
        self.assertEqual(record['handling_mode'], 'external_manual')
        self.assertEqual(record['outbound_document'], 'EXTERNAL-ONLY')
        self.assertEqual(before, self.facts())
        self.assertFalse(scan_server_changes(self.config)['server']['changes'])
        self.assertEqual(before, self.facts())
        self.inventory.assert_not_called()

    def test_new_aimes_factory_or_unknown_owner_prevents_mixed_supplement(self):
        folder = self.folder(); self.seed()
        scan_server_changes(self.config)  # A later AIMES row must invalidate pending classification.
        store = OrderIndexStore(self.config.workflow_database)
        store.upsert_aimes_factory('F102', order_id='PP0035', factory_name='PP0035 NEW', sales_order_name='PP0035', split_time='2026-09-14T11:00:00', seen_at='2026-09-14T11:00:00')
        store.commit()
        self.assertEqual(_server_folder_handling_mode(store, folder), 'mixed')
        store.close()
        with self.assertRaisesRegex(ValueError, '补单要求'):
            mark_temporary_folder_manual(self.config, folder)
        unknown = self.folder('PP0008 AND PP9999')
        store = OrderIndexStore(self.config.workflow_database)
        self.assertEqual(_server_folder_handling_mode(store, unknown), 'mixed')
        store.close()

    def test_plain_folder_optional_references_and_duplicate_time(self):
        folder = self.folder('临时柜子')
        with patch('traveler_assistant.order_index._now', return_value='2026-09-14T10:00:00'):
            mark_temporary_folder_manual(self.config, folder, reference_order_ids=['PP0008', 'CS003'])
        first = self.record(folder)
        with patch('traveler_assistant.order_index._now', return_value='2026-09-15T10:00:00'):
            result = mark_temporary_folder_manual(self.config, folder, reference_order_ids=[])
        second = self.record(folder)
        self.assertTrue(result['unchanged'])
        for key in ['processed_at', 'outbound_at', 'server_scan_watch_until', 'server_scan_policy_updated_at']:
            self.assertEqual(first[key], second[key])
        self.assertEqual(second['reference_order_ids'], [])
        self.assertEqual(self.facts()['orders'], [])

    def test_xml_change_remains_pending_past_deadline_then_new_completion(self):
        folder = self.folder(); self.seed()
        mark_temporary_folder_manual(self.config, folder)
        self.change_xml(folder)
        self.assertTrue(scan_server_changes(self.config)['server']['changes'])
        self.assertEqual(self.record(folder)['server_scan_policy'], 'manual_pending')
        store = OrderIndexStore(self.config.workflow_database)
        store.connection.execute("update temporary_orders set server_scan_watch_until='2000-01-01T00:00:00'")
        store.commit(); store.close()
        self.assertTrue(scan_server_changes(self.config)['server']['changes'])
        result = mark_temporary_folder_manual(self.config, folder)
        self.assertFalse(result['unchanged'])
        self.assertEqual(self.record(folder)['server_scan_policy'], 'watching')
        self.assertFalse(scan_server_changes(self.config)['server']['changes'])

    def test_unchanged_folder_expires_independently_of_parent_orders(self):
        folder = self.folder(); self.seed()
        mark_temporary_folder_manual(self.config, folder)
        store = OrderIndexStore(self.config.workflow_database)
        store.connection.execute("update temporary_orders set server_scan_watch_until='2000-01-01T00:00:00'")
        store.commit(); store.close()
        self.assertFalse(scan_server_changes(self.config)['server']['changes'])
        self.assertEqual(self.record(folder)['server_scan_policy'], 'permanent')

    def test_manual_route_blocks_preview_and_auto_outbound(self):
        folder = self.folder(); self.seed()
        mark_temporary_folder_manual(self.config, folder)
        before = self.facts()
        with self.assertRaisesRegex(RuleError, '独立人工处理'):
            preview_server_changes(self.config, [folder])
        sync_order_index(self.config, selected_folders=[folder], process_temporary=True, refresh_outbound_statuses=False, reconcile_outbound=False, validate_selected_orders=False)
        self.assertEqual(before, self.facts())
        self.inventory.assert_not_called()

    def test_failure_rolls_back_completion_and_baseline(self):
        folder = self.folder(); self.seed()
        before = self.facts()
        with patch.object(OrderIndexStore, 'save_server_scan_xml_baseline', side_effect=RuntimeError('test failure')):
            with self.assertRaisesRegex(RuntimeError, 'test failure'):
                mark_temporary_folder_manual(self.config, folder)
        self.assertIsNone(self.record(folder))
        self.assertEqual(before, self.facts())

    def test_additive_migration_preserves_existing_temporary_record(self):
        folder = self.folder('普通临时任务')
        mark_temporary_folder_manual(self.config, folder, reference_order_ids=[])
        original = self.record(folder)
        store = OrderIndexStore(self.config.workflow_database)
        store.connection.execute('alter table temporary_orders drop column handling_mode')
        store.connection.execute('alter table temporary_orders drop column reference_order_ids')
        store.commit(); store.close()
        restored = self.record(folder)
        self.assertEqual(original['outbound_at'], restored['outbound_at'])
        self.assertEqual(restored['reference_order_ids'], [])
        self.assertEqual(restored['outbound_status'], '已出库')

    def test_single_order_supplement_and_fresh_aimes_rows(self):
        folder = self.folder('PP0008-replacement'); self.seed()
        store = OrderIndexStore(self.config.workflow_database)
        self.assertEqual(_server_folder_handling_mode(store, folder), 'supplemental')
        fresh = [{'factory_order':'F102', 'factory_name':'PP0008 NEW', 'sales_order_name':'PP0008'}]
        self.assertNotEqual(_server_folder_handling_mode(store, folder, fresh), 'supplemental')
        store.upsert_source_file(folder, source_folder=folder, kind='folder', order_id='PP0008', changed_at='2026-09-14T10:00:00')
        self.assertNotEqual(_server_folder_handling_mode(store, folder), 'supplemental')
        store.close()

    def test_xml_deletion_reopens_manual_task(self):
        folder = self.folder('补件'); mark_temporary_folder_manual(self.config, folder)
        for path in folder.rglob('*.xml'):
            path.unlink()
        changes = scan_server_changes(self.config)['server']['changes']
        self.assertTrue(any(row['change_type'] == 'removed' for row in changes))
        self.assertEqual(self.record(folder)['server_scan_policy'], 'manual_pending')

    def test_sync_discovers_supplement_without_parsing_or_projecting_it(self):
        folder = self.folder(); self.seed()
        before = self.facts()
        sync_order_index(self.config, selected_folders=[folder], process_temporary=True,
                         refresh_outbound_statuses=False, reconcile_outbound=False,
                         validate_selected_orders=False)
        self.assertEqual(before, self.facts())
        self.assertEqual(self.record(folder)['handling_mode'], 'supplemental')
        self.inventory.assert_not_called()
