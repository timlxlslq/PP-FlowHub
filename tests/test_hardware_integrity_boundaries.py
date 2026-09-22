"""Isolated regression coverage for scoped reconciliation and manual decisions."""
import hashlib
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.inventory import Product, _replace_product_database
from traveler_assistant.order_index import OrderIndexStore, reconcile_outbound_statuses, list_order_index, sync_order_index
from traveler_assistant.hardware_facts import replace_factory_hardware, hardware_integrity_findings, audit_hardware_integrity
from traveler_assistant.hardware_source_decisions import preview_manual_handling, confirm_manual_handling, load_source_decisions
from traveler_assistant.fittings import select_latest_fittings
from traveler_assistant.report_read_context import report_read_session
from traveler_assistant.order_workflow import main
from tests.test_order_workflow import make_fittings


class IntegrityBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config(state_dir=Path(self.temp.name)/'state', source_root=Path(self.temp.name)/'server', operation_log_enabled=False)
        self.config.prepare_storage()
        _replace_product_database(self.config.workflow_database, [Product('Hardware','M1001','Hinge','','启用',unit='pcs')])
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.c = self.store.connection
        for order, factory in [('PP0008','F100'),('PP0064','F200')]:
            self.store.upsert_order(order, validation_status='正常')
            self.store.upsert_factory(factory, order_id=order, factory_name=order+'-ROOM',sales_order_name=order,name_source='AIMES',ownership_status='已确认')
        self.path=self.config.source_root/'PP0008'/'Report'/'Fittingslist.xlsx'
        self.path.parent.mkdir(parents=True)
        make_fittings(self.path,[('F100',2)])
        self.store.upsert_source_file(self.path,source_folder=self.path.parent.parent,kind='fittings',order_id='PP0008',factory_order='F100',changed_at='now')
        with report_read_session() as context:
            select_latest_fittings([self.path])
            self.decision=context.decision_proposals['F100']
        self.c.execute('insert into hardware_source_decisions values(?,?)',('F100',json.dumps(self.decision)))
        replace_factory_hardware(self.c,'F100',[dict(order_id='PP0008',factory_order='F100',product_code='M1001',quantity=2)],source_path=str(self.path))
        self.c.commit()

    def manual(self):
        preview=preview_manual_handling(self.config,'PP0008','F100')
        return confirm_manual_handling(self.config,'PP0008','F100',preview['token'])

    def test_outbound_does_not_audit_other_orders_and_maintenance_still_finds_them(self):
        self.c.execute("delete from hardware_items where factory_order='F100'")
        self.c.commit()
        with patch('traveler_assistant.order_index.audit_hardware_integrity',side_effect=AssertionError('global audit')), patch('traveler_assistant.order_index.audit_factory_hardware') as scoped:
            reconcile_outbound_statuses(self.config,self.store,order_ids=['PP0064'],factory_orders=['F200'])
            self.assertEqual([c.args[1] for c in scoped.call_args_list],['F200'])
            list_order_index(self.config)
        self.assertEqual(self.c.execute("select count(*) from active_issues where kind='hardware_integrity'").fetchone()[0],0)
        before=list(self.c.iterdump())
        sink={}
        self.assertEqual(main(['audit-hardware'],config_override=self.config,result_sink=sink,emit_result=False),0)
        self.assertEqual(sink['value']['findings'][0]['order_id'],'PP0008')
        self.assertIn(str(self.path),sink['value']['findings'][0]['message'])
        self.assertEqual(before,list(self.c.iterdump()))
        audit_hardware_integrity(self.c)
        self.assertEqual(self.c.execute("select path from active_issues where kind='hardware_integrity'").fetchone()[0],str(self.path))

    def test_manual_same_version_survives_restart_and_preserves_manual_hardware(self):
        self.c.execute("insert into hardware_items(order_id,factory_order,product_code,quantity,source_type,updated_at) values('PP0008','F100','M1001',3,'manual','old')")
        self.c.commit()
        self.manual()
        self.assertEqual(hardware_integrity_findings(self.c),[])
        self.assertEqual(self.c.execute('select source_type,quantity from hardware_items').fetchall(),[('manual',3.0)])
        with report_read_session() as context:
            context.locked_decisions=load_source_decisions(self.config)
            selected,*_=select_latest_fittings([self.path])
            self.assertIn('F100',context.keep_factories)
            self.assertEqual(selected['F100'].items,())
        self.assertNotEqual(self.c.execute("select stage from factory_orders where factory_order='F100'").fetchone()[0],'已出货')

    def test_changed_report_requires_new_choice_instead_of_permanent_manual_exemption(self):
        self.manual()
        make_fittings(self.path,[('F100',9)])
        with report_read_session() as context:
            context.locked_decisions=load_source_decisions(self.config)
            with self.assertRaises(RuleError) as caught:
                select_latest_fittings([self.path])
            candidate=caught.exception.context['conflicts'][0]['candidates'][0]
        with report_read_session({'F100':candidate['id']}) as context:
            context.locked_decisions=load_source_decisions(self.config)
            selected,*_=select_latest_fittings([self.path])
            self.assertEqual(selected['F100'].items[0].quantity,9)
            self.assertNotIn('handling',context.decision_proposals['F100'])
        self.store.upsert_source_file(self.path,source_folder=self.path.parent.parent,kind='fittings',changed_at='later')
        self.assertEqual(len(hardware_integrity_findings(self.c)),1)

    def test_manual_failure_rolls_back_all_tables(self):
        before=list(self.c.iterdump())
        with patch.object(OrderIndexStore, 'upsert_source_file', side_effect=sqlite3.IntegrityError('injected')):
            with self.assertRaises(sqlite3.IntegrityError): self.manual()
        self.assertEqual(before,list(self.c.iterdump()))

    def test_stale_manual_preview_rejected_without_writes(self):
        preview=preview_manual_handling(self.config,'PP0008','F100')
        make_fittings(self.path,[('F100',7)])
        before=list(self.c.iterdump())
        with self.assertRaises(RuleError): confirm_manual_handling(self.config,'PP0008','F100',preview['token'])
        self.assertEqual(before,list(self.c.iterdump()))

    def test_top_level_database_and_unknown_errors_are_not_excel_errors(self):
        for exception,code in [(sqlite3.OperationalError('database is locked'),'local_database_error'),(RuntimeError('injected'),'local_processing_error')]:
            sink={}
            with patch('traveler_assistant.order_details.order_detail',side_effect=exception):
                self.assertEqual(main(['detail','--order-id','PP0008'],config_override=self.config,result_sink=sink,emit_result=False),2)
            self.assertEqual(sink['value']['fatal']['code'],code)
            self.assertEqual(sink['value']['fatal']['order_id'],'PP0008')
            self.assertNotIn('Excel',sink['value']['fatal']['message'])

    def test_multifactory_report_identity_failure_rolls_back_facts_versions_and_choices(self):
        make_fittings(self.path,[('F100',9),('F200',8)])
        self.c.execute('delete from hardware_source_decisions')
        self.c.commit()
        tables=['hardware_items','hardware_source_versions','hardware_source_decisions']
        before={table:self.c.execute('select * from '+table).fetchall() for table in tables}
        resolution={'missing':[], 'accepted':[{'product_codes':['M1001']},{'product_codes':['M1001']}]}
        with patch.object(OrderIndexStore, 'update_source_file_identity', side_effect=sqlite3.IntegrityError('identity failure')), patch('traveler_assistant.inventory.resolve_inventory_items',return_value=resolution), patch('traveler_assistant.order_index.audit_hardware_integrity',side_effect=AssertionError('global audit')):
            sync_order_index(self.config,selected_folders=[self.path.parent.parent],full_refresh=True,refresh_outbound_statuses=False,reconcile_outbound=False)
        for table in tables:
            self.assertEqual(before[table],self.c.execute('select * from '+table).fetchall(),table)
        issue=self.c.execute("select message from active_issues where kind='report_error'").fetchone()[0]
        for value in ['本地数据库','PP0008','F100','F200',str(self.path),'identity failure']:
            self.assertIn(value,issue)

    def test_empty_outbound_scope_touches_no_factory(self):
        with patch('traveler_assistant.order_index.audit_factory_hardware') as audit:
            reconcile_outbound_statuses(self.config,self.store,factory_orders=[])
            audit.assert_not_called()

    def test_folder_local_read_of_one_confirmed_copy_does_not_reopen_manual_choice(self):
        other=self.path.parent/'Fittingslist-copy.xlsx'
        other.write_bytes(self.path.read_bytes())
        self.store.upsert_source_file(other,source_folder=self.path.parent.parent,kind='fittings',order_id='PP0008',factory_order='F100',changed_at='now')
        self.c.commit()
        self.manual()
        with report_read_session() as context:
            context.locked_decisions=load_source_decisions(self.config)
            selected,*_=select_latest_fittings([other])
            self.assertEqual(selected['F100'].items,())
        self.assertEqual(hardware_integrity_findings(self.c),[])
