"""覆盖正式库污染、跨路径重复、空预览及出库事实回退。"""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.hardware_facts import assert_source_isolation, replace_factory_hardware, hardware_integrity_findings, preserve_confirmed_shipment
from traveler_assistant.order_index import OrderIndexStore, reconcile_outbound_statuses
from traveler_assistant.order_workflow import persist_preview


class HardwareFactsTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config(state_dir=Path(self.temp.name), operation_log_enabled=False)
        self.config.prepare_storage()
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.c = self.store.connection
        self.store.upsert_order('PP9999', validation_status='正常')
        self.store.upsert_factory('F100', order_id='PP9999', factory_name='PP9999-ROOM', sales_order_name='PP9999', name_source='AIMES', ownership_status='已确认')
        self.row = dict(order_id='PP9999', factory_order='F100', product_code='M1001', source_code='hinge', name='Hinge', quantity=24, unit='pcs')
        self.store.commit()

    def test_path_switch_repeat_and_restart_preserve_one_projection(self):
        replace_factory_hardware(self.c, 'F100', [self.row], source_path='/test/Fittingslist.xlsx')
        self.c.commit()
        for _ in range(2):
            replace_factory_hardware(self.c, 'F100', [self.row], source_path='/server/Fittingslist.xlsx')
        self.c.commit()
        with sqlite3.connect(self.config.workflow_database) as reopened:
            self.assertEqual(reopened.execute('select count(*),sum(quantity) from hardware_items').fetchone(), (1,24))
        self.assertEqual(self.c.execute("select count(*) from sync_changes where kind='hardware_projection_replaced'").fetchone()[0],1)

    def test_duplicate_legacy_paths_replaced_and_manual_preserved(self):
        for source in ['/test/a.xlsx','/server/a.xlsx']:
            self.c.execute("insert into hardware_items(order_id,factory_order,product_code,quantity,source_type,source_path,updated_at) values('PP9999','F100','M1001',24,'aicnc',?,'old')",(source,))
        self.c.execute("insert into hardware_items(order_id,factory_order,product_code,quantity,source_type,updated_at) values('PP9999','F100','M1093',1,'manual','old')")
        self.assertEqual(len(hardware_integrity_findings(self.c)),1)
        replace_factory_hardware(self.c,'F100',[self.row],source_path='/server/a.xlsx')
        self.assertEqual(self.c.execute('select count(*),sum(quantity) from hardware_items').fetchone(),(2,25))
        self.assertEqual(hardware_integrity_findings(self.c),[])

    def test_failed_insert_rolls_back_deletion_even_when_caller_commits(self):
        replace_factory_hardware(self.c,'F100',[self.row])
        self.c.commit()
        self.c.execute("create trigger reject_hardware before insert on hardware_items when new.quantity=25 begin select raise(abort,'test failure'); end")
        with self.assertRaises(sqlite3.IntegrityError):
            replace_factory_hardware(self.c,'F100',[{**self.row,'quantity':25}])
        self.c.commit()
        self.assertEqual(self.c.execute('select quantity from hardware_items').fetchone()[0],24)

    def test_material_only_preview_and_missing_factory_do_not_delete(self):
        replace_factory_hardware(self.c,'F100',[self.row])
        self.c.commit()
        preview=SimpleNamespace(order_id='PP9999',materials=[],edge_banding={},factories=[],include_hardware=False,folder=Path('/server'),materials_path=Path('/server/material.xlsx'))
        with patch('traveler_assistant.order_workflow._preview_inventory_resolution_items',return_value=[]), patch('traveler_assistant.order_workflow.resolve_inventory_items',return_value={'missing':[],'accepted':[]}):
            persist_preview(self.config,preview)
        self.assertEqual(self.c.execute('select quantity from hardware_items').fetchone()[0],24)
        self.assertFalse(replace_factory_hardware(self.c,'F100',[]))

    def test_test_source_cannot_target_production_database(self):
        production=Path.home()/'Documents/pp-flowhub/data/workflow.sqlite3'
        with self.assertRaises(RuleError):
            assert_source_isolation(production,['/data/server-test-fixtures/Optimized Orders'])
        assert_source_isolation(self.config.workflow_database,['/data/server-test-fixtures/Optimized Orders'])
        with patch('traveler_assistant.core.ensure_schema') as create:
            with self.assertRaises(RuleError):
                Config(source_root=Path('/data/server-test-fixtures')).prepare_storage()
            create.assert_not_called()

    def test_confirmed_shipment_survives_changed_missing_data_and_rename(self):
        self.c.execute("insert into outbound_documents(document_number,document_type,order_id,factory_order,status,issued_at,items_json,updated_at) values('DOC','hardware','PP9999','PP9999-ROOM','已出库','2026-08-26T09:08:30',?,'old')",(json.dumps([{'productCode':'M1001','quantity':24}]),))
        self.c.execute("insert into outbound_document_factories(document_number,order_id,factory_order,created_at,updated_at) values('DOC','PP9999','F100','old','old')")
        self.c.commit()
        replace_factory_hardware(self.c,'F100',[{**self.row,'quantity':48}])
        self.c.commit()
        reconcile_outbound_statuses(self.config,self.store)
        self.assertEqual(self.c.execute("select outbound_status,outbound_document from factory_orders where factory_order='F100'").fetchone(),('已出库','DOC'))
        self.assertEqual(self.c.execute("select count(*) from active_issues where kind='outbound_hardware_difference' and status='open'").fetchone()[0],1)
        self.c.execute("update factory_orders set outbound_status='未出库',outbound_completed_at=''")
        preserve_confirmed_shipment(self.c,'F100')
        self.assertEqual(self.c.execute("select outbound_status from factory_orders").fetchone()[0],'已出库')
        self.c.execute("delete from hardware_items")
        self.c.execute("update factory_orders set factory_name='P9999-RENAMED'")
        self.c.commit()
        reconcile_outbound_statuses(self.config,self.store)
        self.assertEqual(self.c.execute("select outbound_status from factory_orders").fetchone()[0],'已出库')
        replace_factory_hardware(self.c,'F100',[self.row])
        self.assertEqual(self.c.execute("select status from active_issues where kind='outbound_hardware_difference'").fetchone()[0],'resolved')

    def test_complete_empty_and_missing_source_have_distinct_meanings(self):
        replace_factory_hardware(self.c,'F100',[self.row])
        self.c.execute("insert into source_files(path,source_folder,kind,order_id,factory_order,modified_at,size,last_seen) values('/server/Fittingslist.xlsx','/server','fittings','PP9999','F100',0,0,'old')")
        self.assertFalse(replace_factory_hardware(self.c,'F100',[]))
        self.assertEqual(self.c.execute('select count(*) from hardware_items').fetchone()[0],1)
        replace_factory_hardware(self.c,'F100',[],allow_empty=True)
        self.assertEqual(self.c.execute('select count(*) from hardware_items').fetchone()[0],0)
        self.assertEqual(hardware_integrity_findings(self.c),[])
