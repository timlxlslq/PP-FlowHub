import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.database import connect_database
from traveler_assistant.order_index import OrderIndexStore
from traveler_assistant.manual_hardware import list_manual_hardware, save_manual_hardware
from traveler_assistant.order_workflow import main
from traveler_assistant.inventory import search_inventory_products


class ManualHardwareEditorTests(unittest.TestCase):
    # 建立两种人工五金商品及跨订单工厂单，供增删和权限测试。
    # self：当前测试用例或测试替身实例。
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.config = Config(state_dir=root / 'state', order_root=root / 'orders',
                             source_root=root / 'source', backup_root=root / 'backups')
        self.config.prepare_storage()
        store = OrderIndexStore(self.config.workflow_database)
        store.close()
        self.connection = connect_database(self.config.workflow_database)
        self.addCleanup(self.connection.close)
        for code, name, spec, unit in [('M2000', '抽屉拉手', '黑色', '个'), ('M2001', '抽屉拉手', '银色', '对')]:
            self.connection.execute(
                """insert into products(code,name,spec,unit,status,category,normalized_code,
                   normalized_name,normalized_spec,normalized_category,normalized_remark)
                   values(?,?,?,?, '启用','Hardware',?,?,?,'hardware','')""",
                (code, name, spec, unit, code, name, spec))
        for factory, order in [('F1', 'PP9999'), ('F2', 'PP9999'), ('F3', 'PP9998')]:
            self.connection.execute(
                """insert into factory_orders(factory_order,order_id,factory_name,aimes_status,updated_at)
                   values(?,?,?,'active','now')""", (factory, order, order + '-' + factory))
        self.connection.commit()

    # 读取当前测试订单的人工五金及版本快照。
    # self：当前测试用例或测试替身实例。
    def snapshot(self):
        return list_manual_hardware(self.config, 'PP9999')

    # 带版本和明确确认标记提交人工五金增删请求。
    # self：当前测试用例或测试替身实例。
    # additions：待新增的人工五金请求列表。
    # deletions：待删除的人工五金行标识列表。
    # version：并发校验版本，未指定时读取当前版本。
    def save(self, additions=None, deletions=None, version=None):
        return save_manual_hardware(self.config, 'PP9999', {
            'version': version or self.snapshot()['version'], 'additions': additions or [], 'deletions': deletions or []
        }, confirm_write=True)

    # 构造指定工厂单、SKU 和数量的人工五金新增请求。
    # self：当前测试用例或测试替身实例。
    # factory：目标工厂单编号。
    # code：商品 SKU 编码。
    # quantity：测试项目数量。
    def addition(self, factory='F1', code='M2000', quantity=2):
        return dict(factory_order=factory, product_code=code, quantity=quantity)

    # 直接插入一条测试五金事实，并返回新行标识。
    # self：当前测试用例或测试替身实例。
    # order：所属订单编号。
    # factory：目标工厂单编号。
    # source：五金事实的来源类型。
    def insert(self, order='PP9999', factory='F1', source='manual'):
        cursor = self.connection.execute(
            "insert into hardware_items(order_id,factory_order,product_code,quantity,source_type,updated_at) values(?,?,'M2000',3,?,'now')", (order, factory, source))
        self.connection.commit()
        return cursor.lastrowid

    # 验证人工五金增删与同 SKU 合并在同一事务完成，自动五金保持不变。
    # self：当前测试用例或测试替身实例。
    def test_transaction_add_delete_aggregate_units_and_auto_preservation(self):
        old = self.insert()
        automatic = self.insert(source='aicnc')
        result = self.save([self.addition(), self.addition(quantity=4), self.addition('F2', 'M2001', 3)], [old])
        self.assertTrue(result['saved'])
        self.assertEqual([(r['factory_order'], r['quantity'], r['unit']) for r in result['items']],
                         [('F1', 6, '个'), ('F2', 3, '对')])
        self.assertIsNone(self.connection.execute('select id from hardware_items where id=?', (old,)).fetchone())
        self.assertEqual(self.connection.execute('select quantity from hardware_items where id=?', (automatic,)).fetchone(), (3,))
        self.assertEqual(self.connection.execute('pragma foreign_key_check').fetchall(), [])

    # 验证跨订单工厂单、无效数量或停用商品导致整笔写入回滚。
    # self：当前测试用例或测试替身实例。
    def test_foreign_factory_invalid_quantity_and_disabled_product_roll_back(self):
        old = self.insert()
        for addition in [self.addition('F3'), self.addition(quantity=0), self.addition(quantity=1.5),
                         self.addition(quantity=True), self.addition(quantity='no'), self.addition(code='M404')]:
            before = self.snapshot()
            with self.assertRaises(RuleError):
                self.save([self.addition(), addition], [old])
            self.assertEqual(self.snapshot(), before)
        self.connection.execute("update products set status='停用' where code='M2001'")
        self.connection.commit()
        with self.assertRaises(RuleError):
            self.save([self.addition(code='M2001')], [old])
        self.assertEqual(len(self.snapshot()['items']), 1)

    # 验证删除操作只能移除当前订单的人工五金记录。
    # self：当前测试用例或测试替身实例。
    def test_delete_only_current_order_manual_rows(self):
        for item_id in [self.insert(source='aicnc'), self.insert('PP9998', 'F3'), 123456]:
            with self.assertRaises(RuleError) as error:
                self.save(deletions=[item_id])
            self.assertEqual(error.exception.code, 'manual_hardware_delete_scope')

    # 验证版本变化及重复提交均被拒绝，避免覆盖并发修改。
    # self：当前测试用例或测试替身实例。
    def test_concurrent_change_and_duplicate_submission_rejected(self):
        version = self.snapshot()['version']
        self.save([self.addition()], version=version)
        with self.assertRaises(RuleError) as error:
            self.save([self.addition()], version=version)
        self.assertEqual(error.exception.code, 'manual_hardware_conflict')
        self.assertEqual(self.snapshot()['items'][0]['quantity'], 2)
        version = self.snapshot()['version']
        self.connection.execute("update factory_orders set order_id='PP9998' where factory_order='F1'")
        self.connection.commit()
        with self.assertRaises(RuleError):
            self.save([self.addition()], version=version)

    # 验证已出货或已失效工厂单禁止编辑人工五金。
    # self：当前测试用例或测试替身实例。
    def test_shipped_or_inactive_factory_is_read_only(self):
        old = self.insert()
        for column, value in [('stage', '已出货'), ('aimes_status', 'removed')]:
            self.connection.execute(f'update factory_orders set {column}=? where factory_order=?', (value, 'F1'))
            self.connection.commit()
            self.assertFalse(self.snapshot()['factories'][0]['editable'])
            with self.assertRaises(RuleError): self.save([self.addition()])
            with self.assertRaises(RuleError): self.save(deletions=[old])

    # 验证中途写入失败时，先前删除及新增操作全部回滚。
    # self：当前测试用例或测试替身实例。
    def test_mid_write_failure_rolls_back_delete_and_add(self):
        old = self.insert()
        before = self.snapshot()
        self.connection.execute("""create trigger reject_second before insert on hardware_items
                                   when new.product_code='M2001' begin select raise(abort,'fixture failure'); end""")
        self.connection.commit()
        with self.assertRaises(Exception):
            self.save([self.addition(), self.addition('F2', 'M2001')], [old])
        self.assertEqual(self.snapshot(), before)

    # 验证保存必须获得明确确认，并校验请求数据结构。
    # self：当前测试用例或测试替身实例。
    def test_explicit_confirmation_and_payload_validation(self):
        with self.assertRaises(RuleError):
            save_manual_hardware(self.config, 'PP9999', {})
        for payload in [[], {'additions': {}, 'deletions': []}, {'additions': [], 'deletions': [True]}]:
            with self.assertRaises(RuleError):
                save_manual_hardware(self.config, 'PP9999', payload, confirm_write=True)

    # 验证被忽略的商品不能作为人工五金新增。
    # self：当前测试用例或测试替身实例。
    def test_ignored_product_is_rejected(self):
        from traveler_assistant.inventory import InventoryMappings
        mapping = InventoryMappings(self.config.workflow_database)
        mapping.save_ignored('抽屉拉手', '测试忽略')
        with self.assertRaises(RuleError) as error:
            self.save([self.addition()])
        self.assertEqual(error.exception.code, 'hardware_ignored')

    # 验证 CLI 从标准输入读取保存请求，并支持名称及 SKU 搜索。
    # self：当前测试用例或测试替身实例。
    def test_cli_stdin_save_and_name_sku_search(self):
        result = {}
        payload = dict(version=self.snapshot()['version'], additions=[self.addition()], deletions=[])
        self.assertEqual(main(['save-manual-hardware', '--order-id', 'PP9999', '--confirm-write'],
                              config_override=self.config, emit_result=False, result_sink=result,
                              stdin_text=json.dumps(payload)), 0)
        self.assertTrue(result['value']['saved'])
        with patch('traveler_assistant.inventory.bootstrap_product_database', return_value=self.config.workflow_database):
            self.assertEqual(len(search_inventory_products(self.config, '抽屉拉手')['products']), 2)
            self.assertEqual(search_inventory_products(self.config, 'M2001')['products'][0]['unit'], '对')

    # 在隔离测试库恢复旧有效标记字段及迁移标记。
    # self：当前测试用例或测试替身实例。
    def make_legacy_hardware(self):
        self.connection.execute('alter table hardware_items add column active integer not null default 1')
        self.connection.execute("delete from workflow_metadata where key='ensure_schema_production_simplification_v1'")
        self.connection.execute("insert or replace into workflow_metadata(key,value,updated_at) values('ensure_schema_material_sku_v1','ready','old')")
        self.connection.commit()

    # 验证旧版迁移删除墓碑记录、保留有效行，重复迁移结果不变。
    # self：当前测试用例或测试替身实例。
    def test_legacy_migration_removes_tombstones_preserves_rows_and_is_idempotent(self):
        from traveler_assistant.database import ensure_schema
        automatic = self.insert(source='aicnc')
        manual = self.insert(factory='F2')
        deleted = self.insert()
        before = self.connection.execute('select * from hardware_items where id in (?,?) order by id', (automatic, manual)).fetchall()
        self.make_legacy_hardware()
        self.connection.execute('update hardware_items set active=0 where id=?', (deleted,))
        self.connection.commit()
        ensure_schema(self.config.workflow_database)
        ensure_schema(self.config.workflow_database)
        self.assertNotIn('active', [r[1] for r in self.connection.execute('pragma table_info(hardware_items)')])
        self.assertEqual(self.connection.execute('select * from hardware_items order by id').fetchall(), before)
        self.assertEqual(self.connection.execute('pragma integrity_check').fetchone(), ('ok',))
        self.assertEqual(self.connection.execute('pragma foreign_key_check').fetchall(), [])
        with self.assertRaises(Exception):
            self.connection.execute("update hardware_items set product_code='M404' where id=?", (manual,))
        self.connection.rollback()

    # 验证结构变更失败时恢复已删除记录和旧字段。
    # self：当前测试用例或测试替身实例。
    def test_failed_schema_change_restores_deleted_rows_and_old_column(self):
        from traveler_assistant.database import ensure_schema
        old = self.insert()
        self.make_legacy_hardware()
        self.connection.execute('update hardware_items set active=0 where id=?', (old,))
        self.connection.execute('create view legacy_active_dependency as select active from hardware_items')
        self.connection.commit()
        with self.assertRaises(Exception):
            ensure_schema(self.config.workflow_database)
        self.assertEqual(self.connection.execute('select active from hardware_items where id=?', (old,)).fetchone(), (0,))
        self.assertIsNone(self.connection.execute("select 1 from workflow_metadata where key='ensure_schema_production_simplification_v1'").fetchone())

    # 验证异常失效的自动五金事实阻止迁移，避免静默丢失。
    # self：当前测试用例或测试替身实例。
    def test_unexpected_inactive_automatic_fact_blocks_migration(self):
        from traveler_assistant.database import ensure_schema
        old = self.insert(source='aicnc')
        self.make_legacy_hardware()
        self.connection.execute('update hardware_items set active=0 where id=?', (old,))
        self.connection.commit()
        with self.assertRaisesRegex(ValueError, '失效的自动五金'):
            ensure_schema(self.config.workflow_database)
        self.assertEqual(self.connection.execute('select active from hardware_items where id=?', (old,)).fetchone(), (0,))

    # 验证同一人工五金的重复行在迁移时实际合并为一行。
    # self：当前测试用例或测试替身实例。
    def test_duplicate_manual_rows_are_physically_merged(self):
        self.insert()
        self.insert()
        self.save([self.addition()])
        self.assertEqual(self.connection.execute("select quantity from hardware_items where source_type='manual'").fetchall(), [(8.0,)])
