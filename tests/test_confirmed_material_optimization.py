"""Server 文件发现结果不能被当作已确认的材料写入事实。"""
import json
import copy
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
    acknowledge_server_preview_memory,
)
from tests.test_order_workflow import make_materials, make_board, make_product_catalog


class ConfirmedMaterialOptimizationTests(unittest.TestCase):
    # 建立独立目录、材料报告及优化 XML，准备待确认工厂单。
    # self：当前测试用例或测试替身实例。
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

    # 写入指定房间的 AIMES 工厂单并刷新测试订单摘要。
    # self：当前测试用例或测试替身实例。
    # factory：目标工厂单编号。
    # room：工厂单所属房间名称。
    def add_factory(self, factory, room):
        store = OrderIndexStore(self.config.workflow_database)
        store.upsert_aimes_factory(factory, order_id='PP9999', factory_name='PP9999-' + room,
                                  sales_order_name='PP9999', split_time='2026-09-15T08:00:00', seen_at='2026-09-15T08:00:00')
        store.summaries()
        store.commit()
        store.close()

    # 读取优化状态及关联业务表快照，供变更前后对比。
    # self：当前测试用例或测试替身实例。
    def state(self):
        with sqlite3.connect(self.config.workflow_database) as c:
            return {
                'factories': c.execute("select factory_order,(stage<>'已拆单') as optimized,optimization_source_path,optimization_first_completed_at,optimization_latest_completed_at from factory_orders order by factory_order").fetchall(),
                **{t: c.execute('select * from ' + t).fetchall() for t in (
                    'material_items', 'hardware_items', 'optimization_artifacts', 'server_scan_xml_state',
                    'production_records', 'outbound_documents')},
            }

    # 生成当前测试文件夹的纯材料 Server 确认预览。
    # self：当前测试用例或测试替身实例。
    def preview(self):
        return preview_server_changes(self.config, [self.folder], include_hardware=False)['server_write_preview']

    def test_aborted_sibling_is_excluded_from_preview_and_confirmation(self):
        """共享目录里的已中止订单不阻断有效订单，也不随确认改写历史事实。"""
        make_board(self.folder / 'Report' / 'old-板材清单.xlsx', 'F200', 'PP8888-OLD')
        store = OrderIndexStore(self.config.workflow_database)
        store.upsert_order('PP8888', source_folder=str(self.folder), stage='已中止')
        store.upsert_factory('F200', order_id='PP8888', factory_name='PP8888-OLD',
                             ownership_status='已确认', source_folder=str(self.folder))
        store.commit()
        before = {
            table: store.connection.execute(f"select * from {table} where order_id='PP8888'").fetchall()
            for table in ('orders', 'factory_orders', 'material_items', 'hardware_items')
        }
        store.close()
        payload = self.preview()
        self.assertEqual([order['order_id'] for order in payload['orders']], ['PP9999'])
        self.assertEqual(payload['orders'][0]['validation_status'], '正常')
        for table in ('orders', 'factory_orders', 'material_items', 'hardware_items', 'server_material_allocations'):
            self.assertFalse(any(row.get('order_id') == 'PP8888' for row in payload['write_records'][table]))
        self.assertFalse(any('old-板材清单.xlsx' in row['path'] for row in payload['write_records']['source_files']))
        confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        store = OrderIndexStore(self.config.workflow_database)
        try:
            for table, rows in before.items():
                self.assertEqual(store.connection.execute(f"select * from {table} where order_id='PP8888'").fetchall(), rows)
            self.assertGreater(store.connection.execute("select count(*) from material_items where order_id='PP9999'").fetchone()[0], 0)
        finally:
            store.close()

    # 先确认材料，再仅修改 XML 时间，生成可确认无变化的预览。
    # self：当前测试用例或测试替身实例。
    def unchanged_preview(self):
        confirm_server_material_preview_memory(self.config, self.preview(), confirm_write=True)
        modified = self.xml.stat().st_mtime + 10
        os.utime(self.xml, (modified, modified))
        self.assertTrue(scan_server_changes(self.config)['server']['changed'])
        payload = preview_server_changes(self.config, [self.folder], include_hardware=True)['server_write_preview']
        self.assertTrue(payload['can_acknowledge_no_changes'])
        return payload

    # 读取确认流程涉及的业务表快照以校验回滚范围。
    # self：当前测试用例或测试替身实例。
    def all_business_tables(self):
        with sqlite3.connect(self.config.workflow_database) as connection:
            return {table: connection.execute('select * from ' + table).fetchall() for table in (
                'orders', 'factory_orders', 'material_items', 'hardware_items',
                'optimization_artifacts', 'source_files', 'hardware_source_decisions',
                'hardware_source_versions', 'server_material_allocations',
                'production_records', 'outbound_documents')}

    # 验证确认无变化仅更新预览基线，后续真实变化仍会提醒。
    # self：当前测试用例或测试替身实例。
    def test_acknowledge_updates_only_preview_baseline_and_future_changes_still_notify(self):
        payload = self.unchanged_preview()
        before = self.all_business_tables()
        for _ in range(2):
            result = acknowledge_server_preview_memory(self.config, payload, confirm_write=True)
            self.assertTrue(result['server_no_changes_confirmed'])
            self.assertEqual(before, self.all_business_tables())
        with patch('traveler_assistant.order_index._now', return_value='2099-01-01T00:00:00'):
            self.assertFalse(scan_server_changes(self.config)['server']['changed'])
        # 预览后的来源变化不得被静默接受，重试时也一样。
        modified = self.xml.stat().st_mtime + 10
        os.utime(self.xml, (modified, modified))
        with sqlite3.connect(self.config.workflow_database) as connection:
            connection.execute("update orders set updated_at='2099-01-01' where order_id='PP9999'")
        before = self.all_business_tables()
        acknowledge_server_preview_memory(self.config, payload, confirm_write=True)
        self.assertEqual(before, self.all_business_tables())
        self.assertTrue(scan_server_changes(self.config)['server']['changed'])

    # 验证确认基线写入失败时事务回滚，文件夹继续待处理。
    # self：当前测试用例或测试替身实例。
    def test_acknowledge_failure_rolls_back_and_keeps_folder_pending(self):
        payload = self.unchanged_preview()
        before = self.state()
        original = OrderIndexStore.save_server_scan_xml_baseline
        # 先执行原基线写入，再制造失败以验证事务回滚。
        # store：隔离测试库的订单索引存储对象。
        # args：转发给被模拟接口的位置参数。
        # kwargs：转发给被模拟接口的关键字参数。
        def fail_after_write(store, *args, **kwargs):
            original(store, *args, **kwargs)
            raise RuntimeError('baseline write failed')
        with patch.object(OrderIndexStore, 'save_server_scan_xml_baseline', fail_after_write):
            with self.assertRaisesRegex(RuntimeError, 'baseline write failed'):
                acknowledge_server_preview_memory(self.config, payload, confirm_write=True)
        self.assertEqual(before, self.state())
        self.assertTrue(scan_server_changes(self.config)['server']['changed'])

    # 验证部分优化的确认不会把未包含工厂单标为已优化。
    # self：当前测试用例或测试替身实例。
    def test_acknowledge_partial_optimization_does_not_optimize_unrepresented_factories(self):
        self.unchanged_preview()
        self.add_factory('F200', 'OFFICE')
        payload = preview_server_changes(self.config, [self.folder], include_hardware=True)['server_write_preview']
        self.assertTrue(payload['can_acknowledge_no_changes'])
        before = self.all_business_tables()
        acknowledge_server_preview_memory(self.config, payload, confirm_write=True)
        self.assertEqual(before, self.all_business_tables())
        self.assertEqual({row[0]: row[1] for row in self.state()['factories']}, {'F100': 1, 'F200': 0})
        self.assertFalse(scan_server_changes(self.config)['server']['changed'])
        # 新优化任务的 XML 出现时，文件夹仍应重新待处理。
        new_xml = self.folder / 'Office' / 'New Nesting' / 'Optimize file' / 'layout file' / 'nesting_result.xml'
        new_xml.parent.mkdir(parents=True)
        new_xml.write_text('<Nesting><BoardControl OrderID="F200" /></Nesting>')
        self.assertTrue(scan_server_changes(self.config)['server']['changed'])

    # 验证不完整、内容变化或过期的预览均不能确认基线。
    # self：当前测试用例或测试替身实例。
    def test_acknowledge_rejects_incomplete_changed_and_stale_previews(self):
        payload = self.unchanged_preview()
        before = self.state()
        with self.assertRaises(RuleError):
            acknowledge_server_preview_memory(self.config, payload)
        variants = []
        for key in ('material_changes', 'hardware_changes', 'factories'):
            changed = copy.deepcopy(payload)
            changed['orders'][0][key] = [{'quantity': 1}]
            changed['has_business_changes'] = False  # 汇总信息不能掩盖真实差异。
            variants.append(changed)
        for key, value in (
            ('include_hardware', False), ('validation_recomputed', False),
            ('hardware_mapping_requirements', [{'name': 'Hinge'}]),
            ('hardware_source_decisions', {'F100': {'new': 'source'}}),
            ('orders', []), ('source_folders', []),
        ):
            variants.append(dict(payload, **{key: value}))
        invalid = copy.deepcopy(payload)
        invalid['orders'][0]['validation_status'] = '数据异常'
        variants.append(invalid)
        for variant in variants:
            with self.subTest(variant=variant.keys()):
                with self.assertRaises(RuleError):
                    acknowledge_server_preview_memory(self.config, variant, confirm_write=True)
                self.assertEqual(before, self.state())
        with sqlite3.connect(self.config.workflow_database) as connection:
            connection.execute("update material_items set quantity=quantity+1 where order_id='PP9999'")
        with self.assertRaisesRegex(RuleError, '本地订单事实已变化'):
            acknowledge_server_preview_memory(self.config, payload, confirm_write=True)

    # 验证重复扫描和取消预览不会生成优化确认信息。
    # self：当前测试用例或测试替身实例。
    def test_repeat_scan_and_cancel_preview_leave_no_optimization_information(self):
        before = self.state()
        first = scan_server_changes(self.config)
        self.assertTrue(first['server']['changed'])
        for _ in range(2):
            self.preview()  # 关闭或放弃预览不执行确认。
            repeated = scan_server_changes(self.config)
            self.assertEqual(first['server']['changes'], repeated['server']['changes'])
            self.assertEqual(before, self.state())
        snapshot = json.loads(Path(first['server']['snapshot_path']).read_text())
        self.assertFalse(any(row['kind'].startswith('optimization') for row in snapshot['entries'].values()))
        self.assertEqual(first['orders'][0]['stage'], '已拆单待优化')

    # 验证确认写入具备原子性，重启后事实仍在且无重复材料。
    # self：当前测试用例或测试替身实例。
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
        self.assertEqual(self.state()['production_records'], [])
        self.assertEqual(self.state()['outbound_documents'], [])

    # 验证不带 XML 的材料确认也可使符合条件的订单完成优化。
    # self：当前测试用例或测试替身实例。
    def test_material_confirmation_without_xml_can_complete_optimization(self):
        self.xml.unlink()
        payload = self.preview()
        confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        self.assertEqual(list_order_index(self.config)['orders'][0]['stage'], '已优化')
        self.assertEqual(self.state()['optimization_artifacts'], [])

    # 验证新出现的 AIMES 工厂单不继承之前的材料优化状态。
    # self：当前测试用例或测试替身实例。
    def test_new_aimes_factory_does_not_inherit_old_material_optimization(self):
        confirm_server_material_preview_memory(self.config, self.preview(), confirm_write=True)
        self.add_factory('F200', 'OFFICE')
        payload = self.preview()
        confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        states = {r[0]: r[1] for r in self.state()['factories']}
        self.assertEqual(states, {'F100': 1, 'F200': 0})
        self.assertEqual(list_order_index(self.config)['orders'][0]['stage'], '部分优化')

    # 验证部分工厂单确认后，其余文件仍保持待处理。
    # self：当前测试用例或测试替身实例。
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

    # 验证预览后发生变化的 XML 不能被接受为确认基线。
    # self：当前测试用例或测试替身实例。
    def test_xml_changed_after_preview_is_not_accepted_as_confirmed_baseline(self):
        payload = self.preview()
        stamp = self.xml.stat()
        os.utime(self.xml, ns=(stamp.st_atime_ns, stamp.st_mtime_ns + 5_000_000_000))
        confirm_server_material_preview_memory(self.config, payload, confirm_write=True)
        changes = scan_server_changes(self.config)['server']['changes']
        self.assertTrue(any(c['path'] == str(self.xml) and c['change_type'] == 'modified' for c in changes))

    # 验证材料工作簿缺失时保留已经确认的材料事实。
    # self：当前测试用例或测试替身实例。
    def test_missing_material_workbook_preserves_confirmed_facts(self):
        from traveler_assistant.order_index import sync_order_index
        confirm_server_material_preview_memory(self.config, self.preview(), confirm_write=True)
        before = self.state()['material_items']
        self.assertTrue(before)
        (self.folder / 'PP9999 materials.xlsx').unlink()
        for _ in range(2):
            with patch('traveler_assistant.order_index.load_aimes_order_cache', return_value=[]):
                sync_order_index(self.config, include_hardware=False)
            self.assertEqual(self.state()['material_items'], before)

    # 验证没有材料记录时不能仅凭工厂单确认宣称已优化。
    # self：当前测试用例或测试替身实例。
    def test_factory_confirmation_cannot_claim_optimization_without_material_rows(self):
        payload = self.preview()
        payload['write_records']['material_items'] = []
        before = self.state()
        with self.assertRaises(RuleError) as error:
            confirm_server_preview_memory(self.config, payload, 'PP9999', 'F100', confirm_write=True)
        self.assertEqual(error.exception.code, 'material_allocation')
        self.assertEqual(before, self.state())


if __name__ == '__main__':
    unittest.main()
