"""零消耗生产使用隔离库，验证显式确认、事务边界及原有材料/五金事实保留。"""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.database import ensure_schema
from traveler_assistant.order_index import OrderIndexStore
from traveler_assistant.order_workflow import main
from traveler_assistant.production import confirm_production_without_materials, prepare_production, record_completed_production


class ZeroMaterialProductionTests(unittest.TestCase):
    def setUp(self):
        """为每个测试建立独立订单、工厂单及材料，不使用真实业务配置。"""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config(state_dir=Path(self.temp.name) / 'state')
        self.config.prepare_storage()
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.c = self.store.connection
        self.c.execute("insert into orders(order_id,order_type,updated_at) values('PP0100','owned','now')")
        for factory in ['F1', 'F2', 'F3']:
            self.store.upsert_factory(factory, order_id='PP0100', optimized=True, ownership_status='已确认')
        self.c.execute("insert into products(code,material_kind,unit) values('M1','panel','SHT')")
        self.c.execute("insert into material_items(order_id,product_code,quantity,source_type,source_path,source_fingerprint,updated_at) values('PP0100','M1',5,'aihouse','test','test','now')")
        self.c.commit()

    def confirm(self, **kwargs):
        """以明确确认和全零草稿调用本地生产入口，可覆盖参数验证错误边界。"""
        return confirm_production_without_materials(self.config, kwargs.pop('order_id', 'PP0100'),
            kwargs.pop('factories', ['F1','F2']), kwargs.pop('materials', [{'key':'M1','quantity':0}]),
            confirm=kwargs.pop('confirm', True))

    def test_zero_positive_and_missing_materials_all_require_explicit_choice(self):
        """三种订单材料余额都可显式确认零消耗生产，但普通入口不能提交空消耗。"""
        for situation, factory in zip(['positive','zero','missing'], ['F1','F2','F3']):
            with self.subTest(situation=situation):
                if situation == 'zero':
                    self.c.execute('update material_items set quantity=0')
                if situation == 'missing':
                    self.c.execute('delete from material_items')
                self.c.commit()
                with self.assertRaises(RuleError):
                    prepare_production(self.config, 'PP0100', [factory], [])
                with self.assertRaises(RuleError):
                    self.confirm(confirm=False, factories=[factory])
                result = self.confirm(factories=[factory])
                self.assertEqual(result['status'], 'completed')
        self.assertEqual(self.c.execute('select count(*) from production_materials').fetchone()[0], 0)

    def test_scoped_completion_preserves_materials_inventory_and_other_factory(self):
        """零消耗只改变所选生产状态；剩余材料、库存、五金与订单级出库范围不变。"""
        tables = ['material_items','hardware_items','outbound_documents','outbound_document_factories','inventory_operations','outbound_scope_decisions']
        before = {t: self.c.execute('select * from '+t).fetchall() for t in tables}
        with patch('traveler_assistant.inventory.run_jdy', side_effect=AssertionError('不应调用库存')):
            result = self.confirm()
        for t in tables:
            self.assertEqual(before[t], self.c.execute('select * from '+t).fetchall(), t)
        self.assertEqual(self.c.execute('select factory_order,stage from factory_orders order by factory_order').fetchall(),
            [('F1','已生产'),('F2','已生产'),('F3','已优化')])
        row = self.c.execute('select production_time from production_records').fetchone()
        self.assertTrue(row[0])
        with self.assertRaises(RuleError):
            self.confirm()
        self.assertEqual(self.c.execute('select count(*) from production_records').fetchone()[0], 1)
        summary = self.store.summaries(persist=False)[0]
        factory = next(f for f in summary['factories'] if f['factory_order'] == 'F1')
        self.assertTrue(factory['produced'])

    def test_invalid_selection_and_states_write_nothing(self):
        """错归属、未优化、已删除和已中止均不能记录生产。"""
        for kwargs in [dict(factories=[]), dict(factories='F1'), dict(factories=['UNKNOWN']), dict(order_id='PP9999')]:
            with self.assertRaises(RuleError):
                self.confirm(**kwargs)
        for column, value in [('stage','已拆单'), ('stage','已出货'), ('aimes_status','deleted')]:
            self.c.execute(f'update factory_orders set {column}=? where factory_order=?', (value,'F2'))
            self.c.commit()
            with self.assertRaises(RuleError):
                self.confirm()
            self.c.execute("update factory_orders set stage='已优化',aimes_status='active'")
            self.c.commit()
        self.c.execute("update orders set stage='已中止' where order_id='PP0100'")
        self.c.commit()
        with self.assertRaises(RuleError):
            self.confirm()
        self.assertEqual(self.c.execute('select count(*) from production_records').fetchone()[0], 0)

    def test_pending_external_operation_blocks_and_transaction_failure_rolls_back(self):
        """外部结果未核对先阻断；末步失败回滚生产记录和所有关联。"""
        self.c.execute("insert into inventory_operations(operation_id,operation_kind,order_id,payload_fingerprint,status,created_at,updated_at) values('op','production','PP0100','fp','external_confirmed','now','now')")
        self.c.commit()
        with self.assertRaisesRegex(RuleError, '尚待核对'):
            self.confirm()
        self.c.execute('delete from inventory_operations')
        self.c.commit()
        def fail_after_save(connection, draft):
            record_completed_production(connection, draft)
            raise RuntimeError('模拟末步失败')
        with patch('traveler_assistant.production.record_completed_production', side_effect=fail_after_save):
            with self.assertRaisesRegex(RuntimeError, '末步失败'):
                self.confirm()
        self.assertEqual(self.c.execute('select count(*) from production_records').fetchone()[0], 0)
        self.assertEqual(self.c.execute('select count(*) from factory_orders where production_record_id is not null').fetchone()[0], 0)

    def test_cli_requires_confirmation_and_returns_persisted_result(self):
        """从真实 CLI 分派入口验证确认参数与后端保存结果。"""
        args = ['confirm-production-without-materials','--order-id','PP0100','--factory-orders-json',json.dumps(['F1']), '--materials-json',json.dumps([{'key':'M1','quantity':0}])]
        sink = {}
        self.assertNotEqual(main(args, config_override=self.config, emit_result=False, result_sink=sink), 0)
        self.assertEqual(main(args+['--confirm-write'], config_override=self.config, emit_result=False, result_sink=sink), 0)
        self.assertEqual(sink['value']['status'], 'completed')

    def test_invalid_quantities_cannot_silently_skip_inventory(self):
        """正量、负量、非数、缺数量和坏输入不能绕过库存路径。"""
        for materials in [[{'quantity': q}] for q in [1, -1, 'bad', '', None, True, float('nan'), float('inf')]] + [[{}], [None], {}, 'broken']:
            with self.subTest(materials=materials), self.assertRaises(RuleError):
                self.confirm(materials=materials)
        self.assertEqual(self.c.execute('select count(*) from production_records').fetchone()[0], 0)

    def test_existing_consumption_and_schema_unchanged(self):
        """订单材料已领完时，新生产仅补工厂单记录，历史消耗和表结构不变。"""
        with self.c:
            record_completed_production(self.c, {'order_id':'PP0100','selected_factory_orders':['F3'],
                'materials':[{'product_code':'M1','quantity':5}]})
        schema = self.c.execute("select name,sql from sqlite_master where sql is not null order by name").fetchall()
        materials = self.c.execute('select * from production_materials').fetchall()
        record = self.c.execute('select * from production_records').fetchone()
        ensure_schema(self.config.workflow_database)
        self.confirm(materials=[])
        self.assertEqual(self.c.execute('select * from production_materials').fetchall(), materials)
        self.assertEqual(self.c.execute('select * from production_records where batch_id=?',(record[0],)).fetchone(), record)
        self.assertEqual(self.c.execute("select name,sql from sqlite_master where sql is not null order by name").fetchall(), schema)
        self.assertEqual(self.c.execute('pragma integrity_check').fetchone(), ('ok',))
        self.assertEqual(self.c.execute('pragma foreign_key_check').fetchall(), [])
