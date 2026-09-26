"""新版优化报表、分配、追加及库存恢复；仅使用隔离 SQLite 和伪库存。"""
import copy
import json
import tempfile
import unittest
from datetime import datetime
from pathlib import Path
from unittest.mock import patch

from openpyxl import Workbook
from traveler_assistant import aicnc_import as ai
from traveler_assistant.core import Config, RuleError
from traveler_assistant.inventory import Product, _replace_product_database
from traveler_assistant.order_index import OrderIndexStore, scan_server_changes


class AicncImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.config = Config(state_dir=self.root/'state', source_root=self.root/'Optimized Orders', operation_log_enabled=False)
        self.config.prepare_storage()
        _replace_product_database(self.config.workflow_database,[
            Product('Panel','P1','Test panel','','启用',unit='张'),
            Product('Edge','E1','Test edge','','启用',unit='米'),
            Product('Hardware','H1','Hinge','','启用',unit='pcs')])
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.c = self.store.connection
        ai.migrate(self.c,[])
        for order,factory in [('PP9001','F9001'),('PP9002','F9002')]:
            self.store.upsert_order(order)
            self.store.upsert_factory(factory,order_id=order,factory_name=order,ownership_status='已确认')
        self.store.commit()
        self.folder = self.config.source_root/'PP9001'/'PP9001_room-color-20260925120249'
        (self.folder/'Report').mkdir(parents=True)
        self.board(self.folder/'Report'/'pp-板材清单.xlsx')
        self.mapping = patch('traveler_assistant.inventory.resolve_inventory_items',side_effect=self.resolve)
        self.mapping.start(); self.addCleanup(self.mapping.stop)

    def resolve(self,config,pairs):
        return {'accepted':[{'product_codes':['E1' if 'Edge banding' in p[0].name else 'P1']} for p in pairs], 'missing':[], 'ignored':[]}

    def board(self,path,identities='F9001-PP9001-ROOM'):
        w=Workbook();s=w.active
        s.append(['订单号',identities]);s.append(['大板统计'])
        s.append(['颜色','规格','数量'])
        s.append(['19.1mm/White/MDF','2440*1220*19.1',10])
        s.append(['小板小计']);s.append(['误导小板数量',99999,12345])
        s.append(['封边汇总']);s.append(['颜色','封边条/米'])
        s.append(['White',12.25]);s.append(['White',7.75]);w.save(path)

    def preview(self):
        return ai.preview(self.config,self.folder)['aicnc_preview']

    def test_parse_sections_and_identity(self):
        result=ai.parse_board(self.folder/'Report'/'pp-板材清单.xlsx')
        self.assertEqual(result['factories'],[{'factory_order':'F9001','factory_name':'PP9001-ROOM'}])
        self.assertEqual([m['quantity'] for m in result['materials']],[10,20])
        self.assertEqual(ai.optimization_id(self.folder),'20260925120249')
        self.assertEqual(ai.optimization_id(Path('PP0072_20260923035817')),'20260923035817')
        with self.assertRaises(RuleError): ai.optimization_id(Path('PP0079_name_20260925120249'))

    def test_normal_append_and_duplicate_does_not_reopen(self):
        data=self.preview()
        self.assertEqual(data['factories'][0]['purpose'],'normal')
        ai.confirm(self.config,data,confirmed=True)
        self.assertEqual(self.c.execute("select stage from factory_orders where factory_order='F9001'").fetchone()[0],'已优化')
        self.assertEqual(self.c.execute("select stage from orders where order_id='PP9001'").fetchone()[0],'已优化')
        self.assertEqual(self.c.execute('select sum(quantity) from material_items').fetchone()[0],30)
        with patch.object(ai,'parse_board',side_effect=AssertionError('不能重读')):
            self.assertEqual(ai.discover(self.config,self.c),[])
            self.assertTrue(ai.confirm(self.config,data,confirmed=True)['already_processed'])
        renamed=self.folder.with_name('PP9001_new-description-20260925120249')
        self.folder.rename(renamed)
        self.assertEqual(ai.discover(self.config,self.c),[])
        self.assertEqual(self.c.execute('select count(*) from production_materials').fetchone()[0],0)

    def test_ignore_is_optimization_only(self):
        ai.ignore(self.config,self.folder)
        other=self.folder.with_name('PP9001_other-20260925120500');other.mkdir()
        changes=ai.discover(self.config,self.c)
        self.assertEqual([v['source_folder'] for v in changes],[str(other)])
        self.assertEqual(self.c.execute('select count(*) from material_items').fetchone()[0],0)
        with self.assertRaises(RuleError): ai.ignore(self.config,self.folder.parent)

    def test_mixed_normal_rework_external_then_atomic_materials(self):
        self.board(self.folder/'Report'/'pp-板材清单.xlsx','F9001-PP9001,F9002-PP9002')
        self.c.execute("update factory_orders set stage='已出货' where factory_order='F9002'");self.c.commit()
        data=self.preview()
        self.assertEqual([f['purpose'] for f in data['factories']],['normal','rework'])
        self.assertEqual(data['factories'][1]['hardware_choice'],'shipped')
        data['allocations']=[dict(order_id=o,purpose=p,product_code=code,quantity=q) for o,p,code,q in [
            ('PP9001','normal','P1',7),('PP9002','rework','P1',3),('PP9001','normal','E1',14),('PP9002','rework','E1',6)]]
        with patch('traveler_assistant.inventory._find_existing_inventory_page',return_value={'url':'mock'}), patch('traveler_assistant.inventory.run_jdy',return_value={'saved':True,'documentNumber':'QTCK123'}) as send:
            ai.confirm(self.config,data,confirmed=True)
        self.assertEqual(send.call_count,1)
        self.assertEqual(send.call_args.kwargs['verification_document']['items'],[{'productCode':'P1','quantity':3},{'productCode':'E1','quantity':6}])
        self.assertEqual(self.c.execute('select sum(quantity) from material_items').fetchone()[0],30)
        self.assertEqual(self.c.execute('select sum(quantity) from production_materials').fetchone()[0],9)
        self.assertEqual(self.c.execute("select stage from factory_orders where factory_order='F9002'").fetchone()[0],'已出货')
        self.assertEqual(self.c.execute('select count(*) from outbound_document_factories').fetchone()[0],0)

    def test_uncertain_save_requires_verify_and_never_resubmits(self):
        data=self.preview();data['factories'][0]['purpose']='rework'
        for a in data['allocations']: a['purpose']='rework'
        with patch('traveler_assistant.inventory._find_existing_inventory_page',return_value={'url':'mock'}), patch('traveler_assistant.inventory.run_jdy',side_effect=TimeoutError('可能已保存')):
            with self.assertRaises(TimeoutError): ai.confirm(self.config,data,confirmed=True)
        self.assertEqual(self.c.execute('select count(*) from material_items').fetchone()[0],0)
        remark=ai.documents_for(data)[0]['remark']
        with patch('traveler_assistant.inventory.run_jdy',return_value={'verified':True,'remark':remark,'documentNumber':'QTCK123'}) as verify:
            ai.confirm(self.config,data,confirmed=True)
            self.assertEqual(verify.call_args.args[1],'verifyOutbound')
        self.assertEqual(self.c.execute('select sum(quantity) from production_materials').fetchone()[0],30)
        ai.confirm(self.config,data,confirmed=True)
        self.assertEqual(self.c.execute('select count(*) from outbound_documents').fetchone()[0],1)

    def test_bad_allocation_fails_before_external(self):
        data=self.preview();data['allocations'][0]['quantity']=999
        with patch('traveler_assistant.inventory.run_jdy') as send:
            with self.assertRaises(RuleError): ai.confirm(self.config,data,confirmed=True)
            send.assert_not_called()
        self.assertEqual(self.c.execute('select count(*) from aicnc_optimizations').fetchone()[0],0)

    def test_new_discovery_does_not_read_contents_and_flags_root_misplacement(self):
        bad=self.config.source_root/'PP9003_name-20260925120501';bad.mkdir()
        with patch.object(ai,'parse_board',side_effect=AssertionError('扫描不得解析')):
            changes=ai.discover(self.config,self.c)
        self.assertEqual(len(changes),2)
        self.assertEqual(sum(c['handling_mode']=='layout_review' for c in changes),1)

    def test_shipped_skips_corrupt_fittings(self):
        self.c.execute("update factory_orders set stage='已出货' where factory_order='F9001'");self.c.commit()
        (self.folder/'Report'/'pp-Fittingslist.xlsx').write_text('invalid workbook')
        with patch.object(ai,'parse_fittings_groups',side_effect=AssertionError('已出货不读取五金')):
            self.assertEqual(self.preview()['factories'][0]['hardware_choice'],'shipped')

    def test_hardware_same_keep_replace_and_manual_preserved(self):
        from traveler_assistant.core import FittingItem
        from traveler_assistant.hardware_facts import replace_factory_hardware
        (self.folder/'Report'/'pp-Fittingslist.xlsx').touch()
        row=dict(order_id='PP9001',factory_order='F9001',product_code='H1',quantity=2)
        replace_factory_hardware(self.c,'F9001',[row])
        self.c.execute("insert into hardware_items(order_id,factory_order,product_code,quantity,source_type,updated_at) values('PP9001','F9001','H1',1,'manual','old')")
        self.c.commit()
        with patch.object(ai,'parse_fittings_groups',return_value=[('F9001',[FittingItem(name='Hinge',code='H1',size='',quantity=2,unit='pcs')])]), patch('traveler_assistant.inventory.resolve_inventory_items',side_effect=lambda config,pairs: {'accepted':[{'product_codes':['H1' if p[0].section=='五金' else 'E1' if 'Edge' in p[0].name else 'P1']} for p in pairs],'missing':[],'ignored':[]}):
            same=self.preview()
            self.assertEqual(same['factories'][0]['hardware_choice'],'same')
            with patch.object(ai,'parse_fittings_groups',return_value=[('F9001',[FittingItem(name='Hinge',code='H1',size='',quantity=3,unit='pcs')])]):
                changed=self.preview()
                self.assertEqual(changed['factories'][0]['hardware_choice'],'')
                with self.assertRaises(RuleError): ai.confirm(self.config,changed,confirmed=True)
                changed['factories'][0]['hardware_choice']='keep'
                ai.confirm(self.config,changed,confirmed=True)
                self.assertEqual(self.c.execute("select quantity from hardware_items where source_type='aicnc'").fetchone()[0],2)
                new=self.folder.with_name('PP9001_room-20260925130000')
                self.folder.rename(new);self.folder=new
                replacement=self.preview();replacement['factories'][0]['hardware_choice']='replace'
                ai.confirm(self.config,replacement,confirmed=True)
                self.assertEqual(self.c.execute("select quantity from hardware_items where source_type='aicnc'").fetchone()[0],3)
                self.assertEqual(self.c.execute("select quantity from hardware_items where source_type='manual'").fetchone()[0],1)

    def test_legacy_scope_retires_once_and_new_folders_never_join(self):
        self.c.execute('insert into aicnc_legacy_watch values(?,?,?)',(str(self.folder.parent),'[]',''))
        self.c.commit()
        with patch('traveler_assistant.order_index._server_folder_scan_allowed',return_value=False):
            ai.legacy_snapshot(self.config,self.store)
        self.c.commit()
        self.assertTrue(self.c.execute('select retired_at from aicnc_legacy_watch').fetchone()[0])
        with patch('traveler_assistant.order_index._server_folder_scan_allowed',side_effect=AssertionError('退出后不得重新加入')):
            self.assertEqual(ai.legacy_snapshot(self.config,self.store)[1],{})
        self.assertEqual(len(ai.discover(self.config,self.c)),1)
        self.assertEqual(self.c.execute('select count(*) from aicnc_legacy_watch').fetchone()[0],1)

    def test_legacy_discovery_never_enters_new_optimization(self):
        from traveler_assistant.order_index import _optimization_artifact_paths
        from traveler_assistant.report_read_context import directory_paths
        legacy=self.folder.parent/'Report';legacy.mkdir()
        (legacy/'old.xlsx').touch()
        actual_stat=Path.stat
        def checked_stat(path,*args,**kwargs):
            if self.folder in path.parents:
                raise AssertionError('旧监控不能触及新版优化内部')
            return actual_stat(path,*args,**kwargs)
        with patch.object(Path,'stat',checked_stat):
            paths=directory_paths(self.folder.parent)
            _optimization_artifact_paths(self.folder.parent)
        self.assertIn(legacy/'old.xlsx',paths)
        self.assertNotIn(self.folder/'Report',paths)

    def test_migration_preserves_all_existing_table_contents(self):
        original={r[0]:list(self.c.execute('select * from "'+r[0]+'"')) for r in self.c.execute("select name from sqlite_master where type='table'")}
        ai.migrate(self.c,[])
        for name,rows in original.items():
            self.assertEqual(list(self.c.execute('select * from "'+name+'"')),rows)
        self.assertEqual(self.c.execute('pragma integrity_check').fetchone()[0],'ok')
        self.assertEqual(self.c.execute('pragma foreign_key_check').fetchall(),[])

    def test_changed_business_facts_block_stale_confirmation(self):
        data=self.preview()
        self.c.execute("update factory_orders set stage='已生产' where factory_order='F9001'");self.c.commit()
        with self.assertRaisesRegex(RuleError,'重新预览'):
            ai.confirm(self.config,data,confirmed=True)
        self.assertEqual(self.c.execute('select count(*) from aicnc_optimizations').fetchone()[0],0)

    def test_mismatched_verification_never_records_materials(self):
        data=self.preview();data['factories'][0]['purpose']='rework'
        for a in data['allocations']: a['purpose']='rework'
        with patch('traveler_assistant.inventory._find_existing_inventory_page',return_value={'url':'mock'}), patch('traveler_assistant.inventory.run_jdy',side_effect=TimeoutError()):
            with self.assertRaises(TimeoutError):ai.confirm(self.config,data,confirmed=True)
        with patch('traveler_assistant.inventory.run_jdy',return_value={'verified':True,'remark':'其他订单','documentNumber':'QTCK123'}):
            with self.assertRaises(RuleError): ai.recover(self.config,data['optimization_id'])
        self.assertEqual(self.c.execute('select count(*) from material_items').fetchone()[0],0)

    def test_rework_consumption_not_added_to_later_standard_inventory_document(self):
        from traveler_assistant.production import cumulative_production_materials, production_preview
        from traveler_assistant.inventory import InventorySyncStore
        data=self.preview();data['factories'][0]['purpose']='rework'
        for a in data['allocations']:a['purpose']='rework'
        with patch('traveler_assistant.inventory._find_existing_inventory_page',return_value={'url':'mock'}), patch('traveler_assistant.inventory.run_jdy',return_value={'saved':True,'documentNumber':'QTCK123'}):
            ai.confirm(self.config,data,confirmed=True)
        self.assertEqual(cumulative_production_materials(self.config,'PP9001',[]),[])
        inventory=InventorySyncStore(self.config.state_dir/'inventory-sync.json',self.root/'backup')
        self.assertIsNone(inventory.record_for_document('PP9001','PP9001'))
        record=inventory.record_for_document('PP9001','PP9001 返工 20260925120249')
        self.assertEqual(record['document_number'],'QTCK123')

    def test_fresh_migration_failure_rolls_back_schema(self):
        import sqlite3
        other=sqlite3.connect(self.root/'fresh.sqlite3')
        try:
            duplicate=[{'path':'duplicate','files':[]},{'path':'duplicate','files':[]}]
            with self.assertRaises(sqlite3.IntegrityError): ai.migrate(other,duplicate)
            self.assertFalse(ai.enabled(other))
            self.assertEqual(other.execute("select name from sqlite_master where name like 'aicnc_%'").fetchall(),[])
        finally:other.close()

    def test_app_cleanup_reminder_after_all_legacy_retire(self):
        result=scan_server_changes(self.config)
        self.assertTrue(any(c.get('handling_mode')=='aicnc' for c in result['server']['changes']))
        issue=next(i for i in result['current_issues'] if i['issue_key']=='aicnc_legacy_retired')
        self.assertIn('清理旧版监控代码',issue['message'])
        self.assertTrue(any(i['issue_key']=='aicnc_legacy_retired' for i in self.store.active_issues()))
        self.c.execute("update aicnc_import_settings set value='1' where key='cleanup_dismissed'")
        self.c.commit()
        self.assertFalse(any(i['issue_key']=='aicnc_legacy_retired' for i in scan_server_changes(self.config)['current_issues']))

    def test_legacy_write_entry_cannot_bypass_new_confirmation(self):
        from traveler_assistant.order_index import _server_folders_for_sync
        for selected in (self.folder,self.folder.parent):
            with self.assertRaisesRegex(RuleError,'预览并确认'):
                _server_folders_for_sync(self.config,selected,store=self.store)

    def test_historical_archives_are_not_new_layout_errors(self):
        old=self.config.source_root/'old-mixed-order';old.mkdir()
        self.store.upsert_temporary_order(temporary_id='old',folder_name=old.name,source_folder=str(old),folder_created_at=0,content_fingerprint='',server_scan_policy='permanent')
        historical=self.folder.parent/'old-room';historical.mkdir()
        self.c.execute("insert into source_files(path,source_folder,kind,last_seen) values(?,?,'board','old')",(str(historical/'Report'/'old.xlsx'),str(self.folder.parent)))
        self.c.commit()
        self.assertEqual(len(ai.discover(self.config,self.c)),1)
        fresh=self.folder.parent/'misplaced';fresh.mkdir()
        self.assertEqual(sum(c['handling_mode']=='layout_review' for c in ai.discover(self.config,self.c)),1)

    def test_archived_order_auxiliary_directories_stay_quiet_but_new_ids_discovered(self):
        self.c.execute("update orders set source_folder=?,server_scan_policy='permanent' where order_id='PP9001'",(str(self.folder.parent),))
        self.c.commit()
        for name in ('Report','Import file','Auo-Label-CNC'):
            (self.folder.parent/name).mkdir()
        changes=ai.discover(self.config,self.c)
        self.assertEqual([(r['source_folder'],r['handling_mode']) for r in changes],[(str(self.folder),'aicnc')])

    def test_unregistered_historical_layout_is_not_rediscovered(self):
        cutoff = datetime.fromisoformat('2026-09-25T15:07:05-07:00').timestamp()
        self.c.execute("update aicnc_import_settings set value='2026-09-25T15:07:05-07:00' where key='enabled_at'")
        names = ('b12','b18 2cabinets','BLACKSMDOORS','pp001','pp006','pp0011bathroompanels','pp0016 GLENDALE')
        old = {self.config.source_root/name for name in names}
        old.add(self.folder.parent/'old-room')
        for folder in old:
            (folder/'Report').mkdir(parents=True)
            (folder/'Report'/'recently-edited.xlsx').touch()
        fresh = self.config.source_root/'new-misplaced';fresh.mkdir()
        fresh_child = self.folder.parent/'new-room';fresh_child.mkdir()
        # 有效新版目录即使生成于切换前，也要发现；错放在根层则仍须整理。
        misplaced = self.config.source_root/'PP9001_room-20260925100000';misplaced.mkdir()
        actual_iterdir = Path.iterdir
        def checked_iterdir(path):
            if any(folder == path or folder in path.parents for folder in old):
                raise AssertionError('不能进入历史目录')
            return actual_iterdir(path)
        def created_at(path):
            return cutoff - 60 if path in old or path in (misplaced,self.folder) else cutoff + 60
        before = list(self.c.execute('select * from aicnc_legacy_watch'))
        with patch('traveler_assistant.order_index._folder_created_at',side_effect=created_at), patch.object(Path,'iterdir',checked_iterdir):
            for _ in range(2):
                changes = ai.discover(self.config,self.c)
                self.assertEqual({r['source_folder'] for r in changes if r['handling_mode']=='layout_review'},
                                 {str(fresh),str(fresh_child),str(misplaced)})
                self.assertEqual([r['source_folder'] for r in changes if r['handling_mode']=='aicnc'],[str(self.folder)])
        self.assertEqual(list(self.c.execute('select * from aicnc_legacy_watch')),before)

    def test_historical_order_and_source_records_prevent_layout_review(self):
        mixed = self.config.source_root/'CS003 PP0047';mixed.mkdir()
        source = self.config.source_root/'old-source-only';source.mkdir()
        self.store.upsert_order('PP0047',source_folder=str(mixed))
        self.c.execute("update orders set server_scan_policy='permanent' where order_id='PP0047'")
        self.c.execute("insert into source_files(path,source_folder,kind,last_seen) values(?,?,'board','old')",
                       (str(source/'Report'/'old.xlsx'),str(source)))
        # 即使目录元数据改变，明确的历史来源事实仍优先，且无须读取创建时间。
        with patch('traveler_assistant.order_index._folder_created_at',side_effect=AssertionError('历史来源无需读取时间')):
            changes = ai.discover(self.config,self.c)
        self.assertEqual([r['source_folder'] for r in changes],[str(self.folder)])
