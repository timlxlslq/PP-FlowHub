"""生产结构简化须保留业务事实，并阻止无效迁移。"""
import sqlite3
import tempfile
import unittest
from pathlib import Path

from traveler_assistant.database import ensure_schema, connect_database
from traveler_assistant.order_index import OrderIndexStore
from traveler_assistant.production import record_completed_production
from traveler_assistant.core import RuleError


class ProductionSchemaTests(unittest.TestCase):
    # 分配独立的临时数据库路径，供各迁移测试建立所需旧结构。
    # self：当前测试用例或测试替身实例。
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.path = Path(self.temp.name) / 'workflow.sqlite3'

    # 创建旧版生产数据及可选的重复关联，供迁移验证。
    # self：当前测试用例或测试替身实例。
    # duplicate：是否加入工厂单的重复生产关联。
    def legacy(self, duplicate=False):
        with sqlite3.connect(self.path) as c:
            c.executescript('''
                create table factory_orders(factory_order text primary key,order_id text,
                    optimized integer,outbound_status text,production_batch_id integer,updated_at text);
                insert into factory_orders values('F1','PP0001',1,'未出库',99,'old');
                create table orders(order_id text primary key,stage text,material_status text,
                    validation_status text,validation_message text);
                insert into orders values('PP0001','已生产','板材','正常','');
                create table production_batches(batch_id integer primary key,batch_number text);
                insert into production_batches values(99,'PC-IGNORED');
                create table batch_evidence(id integer primary key,batch_number text);
                insert into batch_evidence values(1,'PC-IGNORED');
                create table manual_production_batches(batch_id integer primary key,batch_number text unique,
                    order_id text,production_time text,source text,status text,created_at text,updated_at text);
                insert into manual_production_batches values(7,'MP-OLD','PP0001','','legacy-outbound-migration','completed','old','old');
                create table manual_production_batch_factories(batch_id integer,order_id text,factory_order text);
                insert into manual_production_batch_factories values(7,'PP0001','F1');
            ''')
            if duplicate:
                c.execute("insert into manual_production_batches values(8,'MP-SECOND','PP0001','','manual','completed','old','old')")
                c.execute("insert into manual_production_batch_factories values(8,'PP0001','F1')")

    # 验证迁移保留记录标识及历史，且不留下兼容表。
    # self：当前测试用例或测试替身实例。
    def test_migration_preserves_ids_history_and_has_no_compatibility_tables(self):
        self.legacy()
        ensure_schema(self.path)
        backups = list((self.path.parent / 'schema-migration-backups').glob('*.sqlite3'))
        self.assertEqual(len(backups), 1)
        with sqlite3.connect(backups[0]) as backup:
            self.assertEqual(backup.execute('select batch_number from manual_production_batches').fetchone()[0], 'MP-OLD')
        ensure_schema(self.path)
        self.assertEqual(len(list((self.path.parent / 'schema-migration-backups').glob('*.sqlite3'))), 1)
        with connect_database(self.path) as c:
            self.assertEqual(c.execute('select production_record_id,stage from factory_orders').fetchall(),[(7,'已生产')])
            self.assertEqual(c.execute('select production_time,source from production_records').fetchone(),('', 'legacy-outbound-migration'))
            tables={r[0] for r in c.execute("select name from sqlite_master where type in ('table','view')")}
            self.assertFalse(tables & {'production_batches','batch_evidence','manual_production_batches','manual_production_batch_factories','manual_production_batch_materials'})
            self.assertEqual({r[1] for r in c.execute('pragma table_info(orders)')},{'order_id','stage'})
            self.assertFalse(c.execute('pragma foreign_key_check').fetchall())
            self.assertEqual(c.execute('pragma integrity_check').fetchone(),('ok',))

    # 验证工厂单历史归属有歧义时回滚整次迁移。
    # self：当前测试用例或测试替身实例。
    def test_ambiguous_factory_history_rolls_back_whole_migration(self):
        self.legacy(duplicate=True)
        with self.assertRaisesRegex(ValueError,'多次生产'):
            ensure_schema(self.path)
        with sqlite3.connect(self.path) as c:
            self.assertEqual(c.execute('select count(*) from manual_production_batches').fetchone()[0],2)
            self.assertIn('optimized',{r[1] for r in c.execute('pragma table_info(factory_orders)')})
            self.assertFalse(c.execute("select 1 from sqlite_master where name='production_records'").fetchall())

    # 验证共享生产记录按订单区分同 SKU，并阻止重复生产。
    # self：当前测试用例或测试替身实例。
    def test_shared_record_keeps_same_sku_separate_by_order_and_blocks_repeat(self):
        store=OrderIndexStore(self.path)
        self.addCleanup(store.close)
        c=store.connection
        c.execute("insert into products(code) values('M1')")
        for order,factory in [('PP0001','F1'),('PP0002','F2')]:
            store.upsert_factory(factory,order_id=order,optimized=True)
        c.commit()
        draft={'selected_factory_orders':['F1','F2'],'materials':[
            {'order_id':'PP0001','product_code':'M1','quantity':6},
            {'order_id':'PP0002','product_code':'M1','quantity':4}]}
        with c:
            result=record_completed_production(c,draft)
        self.assertEqual(c.execute('select order_id,quantity from production_materials order by order_id').fetchall(),[('PP0001',6),('PP0002',4)])
        self.assertEqual(c.execute('select distinct production_record_id,stage from factory_orders').fetchall(),[(result['production_record_id'],'已生产')])
        with self.assertRaises(RuleError), c:
            record_completed_production(c,draft)
        self.assertEqual(c.execute('select count(*) from production_records').fetchone()[0],1)

    # 验证材料校验失败时回滚生产记录及工厂单关联。
    # self：当前测试用例或测试替身实例。
    def test_invalid_material_rolls_back_record_and_factory_links(self):
        store=OrderIndexStore(self.path)
        self.addCleanup(store.close)
        store.upsert_factory('F1',order_id='PP0001',optimized=True)
        store.commit()
        with self.assertRaises(sqlite3.IntegrityError), store.connection:
            record_completed_production(store.connection,{'order_id':'PP0001','selected_factory_orders':['F1'],
                'materials':[{'product_code':'UNKNOWN','quantity':1}]})
        self.assertEqual(store.connection.execute('select stage,production_record_id from factory_orders').fetchone(),('已优化',None))
        self.assertEqual(store.connection.execute('select count(*) from production_records').fetchone()[0],0)

    # 验证临时校验状态不会改写持久业务阶段。
    # self：当前测试用例或测试替身实例。
    def test_validation_is_temporary_and_never_changes_business_stage(self):
        store=OrderIndexStore(self.path)
        store.upsert_order('PP0001',stage='已生产')
        store.set_validation('PP0001','数据异常','Unknown SKU')
        self.assertEqual(store.connection.execute('select stage from orders').fetchone()[0],'已生产')
        self.assertEqual(store.connection.execute('select message from temp.preview_validation').fetchone()[0],'Unknown SKU')
        store.commit();store.close()
        store=OrderIndexStore(self.path)
        self.addCleanup(store.close)
        self.assertFalse(store.connection.execute('select * from temp.preview_validation').fetchall())
        self.assertFalse({'validation_status','validation_message','material_status'} & {r[1] for r in store.connection.execute('pragma table_info(orders)')})

    # 验证饰面板、夹板和封边的分配数量分别满足平衡约束。
    # self：当前测试用例或测试替身实例。
    def test_panel_plywood_and_edge_allocations_must_balance_independently(self):
        from traveler_assistant.order_index import _validated_memory_allocations
        import copy
        payload = {'materials': [
            {'source_path':'/mixed/material.xlsx','product_code':code,'material_type':kind,
             'source_quantity':total,'source_fingerprint':'version1'}
            for code,kind,total in [('P1','panel',10),('W1','plywood',8),('E1','edge',120.25)]]}
        records = {'material_items': [
            {'source_path':'/mixed/material.xlsx','product_code':code,'order_id':order,
             'quantity':quantity,'source_type':'aihouse'}
            for code,order,quantity in [('P1','PP0001',6),('P1','PP0002',4),
                ('W1','PP0001',3),('W1','PP0002',5),('E1','PP0001',50),('E1','PP0002',70.25)]]}
        self.assertEqual(len(_validated_memory_allocations(payload, records)),6)
        for index in (0,2,4):
            for value in (records['material_items'][index]['quantity']+0.005, -1, float('nan')):
                bad = copy.deepcopy(records)
                bad['material_items'][index]['quantity'] = value
                with self.assertRaises(RuleError):
                    _validated_memory_allocations(payload,bad)
