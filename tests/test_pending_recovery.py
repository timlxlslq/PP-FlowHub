"""隔离验证会话问题与持久操作恢复，不连接真实外部系统。"""
import json
import sqlite3
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from traveler_assistant.core import Config, RuleError
from traveler_assistant.inventory import (InventoryOperationJournal, InventorySyncStore,
    pending_inventory_operations, recover_inventory_operation)
from traveler_assistant.order_index import (OrderIndexStore, list_order_index,
    install_shared_workflow_connection, clear_shared_workflow_connection, recheck_current_issue)


class PendingRecoveryTests(unittest.TestCase):
    def setUp(self):
        """建立独立订单、工厂单和已有操作日志结构。"""
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        root = Path(self.temp.name)
        self.config = Config(state_dir=root/'state', backup_root=root/'backups', source_root=root/'server',
                             operation_log_enabled=False)
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.store.upsert_order('PP0099')
        self.store.upsert_factory('F100', order_id='PP0099', factory_name='PP0099 ROOM', ownership_status='已确认')
        self.store.commit()
        self.journal = InventoryOperationJournal(self.config.workflow_database)
        self.document = dict(remark='F100', kind='hardware', items=[dict(productCode='M1001', quantity=2)],
                             rawFingerprint='raw', mappedFingerprint='mapped', knownDocumentNumber='', changed=True)

    def operation(self, status='external_confirmed', documents=None):
        """写入测试操作，不提交任何外部库存动作。"""
        row = self.journal.prepare('shipment', 'PP0099', ['F100'],
            dict(documents=documents or [self.document], production_draft=None,
                 recovery_context=dict(source_type='database', source_path='database:PP0099')))
        self.journal.update(row['operation_id'], status,
            results=[dict(remark='F100', documentNumber='QTCK20260924001', saved=True)])
        return row['operation_id']

    def verify(self, config, action, **kwargs):
        """拒绝任何写库存动作，只模拟精确单据核对。"""
        self.assertEqual(action, 'verifyOutbound')
        self.assertEqual(kwargs['verification_document']['items'], self.document['items'])
        return dict(verified=True, remark=kwargs['order_name'], documentNumber='QTCK20260924001')

    def test_ordinary_issues_and_aimes_warnings_do_not_survive_restart(self):
        self.store.upsert_active_issue(issue_key='sample', kind='material_validation', message='仅本次检查')
        self.store.replace_aimes_review_rows([dict(ignore_key='factory:F100', factory_order='F100', reason='异常')])
        self.store.commit()
        self.assertEqual(len(self.store.active_issues()), 1)
        with sqlite3.connect(self.config.workflow_database) as disk:
            self.assertEqual(disk.execute('select count(*) from active_issues').fetchone()[0], 0)
            self.assertEqual(disk.execute('select count(*) from aimes_review_rows').fetchone()[0], 0)
            self.assertEqual(disk.execute("select count(*) from sqlite_master where name like 'pending_%'").fetchone()[0], 0)
        result = list_order_index(self.config)
        self.assertEqual(result['current_issues'], [])
        self.assertEqual(result['aimes_warnings'], [])

    def test_historical_persisted_problem_is_not_current(self):
        self.store.connection.execute("insert into active_issues values('old','material_validation','','','','old','open','old','old','')")
        self.store.commit()
        self.assertEqual(list_order_index(self.config)['current_issues'], [])
        self.assertEqual(self.store.connection.execute('select count(*) from active_issues').fetchone()[0], 1)

    def test_external_fix_is_rechecked_and_failure_does_not_clear(self):
        folder = self.config.source_root/'PP0099'; folder.mkdir(parents=True)
        install_shared_workflow_connection(self.config.workflow_database, self.store.connection)
        self.addCleanup(clear_shared_workflow_connection)
        self.store.upsert_active_issue(issue_key='missing', kind='server_missing_report', path=str(folder), message='缺少报表')
        self.store.commit()
        with patch('traveler_assistant.order_index._report_files', return_value=[]):
            with self.assertRaisesRegex(ValueError, '仍未找到'):
                recheck_current_issue(self.config, 'missing')
        self.assertEqual(len(self.store.active_issues()), 1)
        with patch('traveler_assistant.order_index._report_files', return_value=[(folder/'Report.xlsx','board')]):
            self.assertEqual(recheck_current_issue(self.config, 'missing')['current_issues'], [])

    def test_recovery_survives_restart_and_only_restores_local_once(self):
        key = self.operation()
        self.assertEqual(list_order_index(self.config)['current_issues'][0]['kind'], 'inventory_recovery')
        with patch('traveler_assistant.inventory.run_jdy', side_effect=self.verify) as browser:
            self.assertTrue(recover_inventory_operation(self.config, key)['syncRecorded'])
            self.assertTrue(recover_inventory_operation(self.config, key)['alreadyRecovered'])
            self.assertEqual(browser.call_count, 1)
        self.assertEqual(pending_inventory_operations(self.config.workflow_database), [])
        records = self.store.connection.execute('select document_number,items_json from outbound_documents').fetchall()
        self.assertEqual(len(records), 1)
        self.assertEqual(json.loads(records[0][1]), self.document['items'])
        self.assertEqual(self.store.connection.execute('select factory_order from outbound_document_factories').fetchall(), [('F100',)])

    def test_wrong_number_keeps_recovery_pending_and_changes_no_business_facts(self):
        key = self.operation()
        with patch('traveler_assistant.inventory.run_jdy', return_value=dict(verified=True, remark='F100', documentNumber='QTCK999')):
            with self.assertRaises(RuleError):
                recover_inventory_operation(self.config, key)
        self.assertEqual(self.store.connection.execute('select count(*) from outbound_documents').fetchone()[0], 0)
        self.assertEqual(len(pending_inventory_operations(self.config.workflow_database)), 1)
        with patch('traveler_assistant.inventory.run_jdy', side_effect=self.verify):
            self.assertTrue(recover_inventory_operation(self.config, key)['ok'])

    def test_partial_external_operation_requires_all_documents_verified(self):
        other = {**self.document, 'remark':'F200'}
        key = self.operation('partial_external_confirmed', [self.document, other])
        def check(config, action, **kwargs):
            if kwargs['order_name']=='F200':
                raise RuleError('verification', '没有找到单据，请外部核对')
            return self.verify(config, action, **kwargs)
        with patch('traveler_assistant.inventory.run_jdy', side_effect=check):
            with self.assertRaisesRegex(RuleError, '没有找到单据'):
                recover_inventory_operation(self.config, key)
        self.assertEqual(self.store.connection.execute('select count(*) from outbound_documents').fetchone()[0], 0)
        self.assertEqual(len(pending_inventory_operations(self.config.workflow_database)), 1)

    def test_local_failure_retains_durable_recovery(self):
        key = self.operation('verification_required')
        with patch('traveler_assistant.inventory.run_jdy', side_effect=self.verify), \
             patch.object(InventorySyncStore, 'save_success', side_effect=sqlite3.OperationalError('disk failure')):
            with self.assertRaises(sqlite3.OperationalError):
                recover_inventory_operation(self.config, key)
        self.assertEqual(len(pending_inventory_operations(self.config.workflow_database)), 1)
        self.assertEqual(self.store.connection.execute('select count(*) from outbound_documents').fetchone()[0], 0)

    def test_recovery_metadata_does_not_change_operation_identity(self):
        base = dict(documents=[self.document], production_draft=None)
        first = self.journal.prepare('shipment','PP0099',['F100'],base)
        second = self.journal.prepare('shipment','PP0099',['F100'],{**base,'recovery_context':{'source_type':'database'}})
        self.assertEqual(first['operation_id'],second['operation_id'])
    def completed_later_fixture(self):
        """模拟两张出库单中断、第二张后来单独完成，第一张本地也已留存。"""
        second = {**self.document, 'remark': 'F200'}
        self.store.upsert_factory('F200', order_id='PP0099', factory_name='PP0099 HALL', ownership_status='已确认')
        self.store.commit()
        key = self.operation('verification_required', [self.document, second])
        later = self.journal.prepare('shipment', 'PP0099', ['F200'], dict(documents=[second], production_draft=None))
        self.journal.update(later['operation_id'], 'local_committed',
            results=[dict(remark='F200', documentNumber='QTCK20260924002', saved=True)])
        c = self.store.connection
        c.execute("update inventory_operations set created_at='2026-09-24T10:00:00-07:00' where operation_id=?", (later['operation_id'],))
        c.execute("update inventory_operations set created_at='2026-09-23T10:00:00-07:00',factory_orders_json=? where operation_id=?", (json.dumps(['F100','F200']),key))
        for number, factory in [('QTCK20260924001', 'F100'), ('QTCK20260924002', 'F200')]:
            c.execute("""insert into outbound_documents(document_number,document_type,order_id,factory_order,status,items_json,updated_at)
                values(?, 'hardware','PP0099',?,'已出库',?,'2026-09-24T10:00:00-07:00')""", (number,factory,json.dumps(self.document['items'])))
            c.execute("insert into outbound_document_factories(document_number,order_id,factory_order,created_at,updated_at) values(?,'PP0099',?,'2026-09-24','2026-09-24')", (number,factory))
        c.commit()
        return key, later['operation_id']

    def test_later_completed_shipment_removes_stale_issue_without_writes(self):
        key, _ = self.completed_later_fixture()
        before = '\n'.join(self.store.connection.iterdump())
        with patch('traveler_assistant.inventory.run_jdy', side_effect=AssertionError('不得打开外部写入')):
            self.assertEqual(pending_inventory_operations(self.config.workflow_database), [])
            result = recover_inventory_operation(self.config, key)
            self.assertTrue(result['alreadyRecovered'])
            self.assertIn('后续操作', result['message'])
        self.assertEqual(before, '\n'.join(self.store.connection.iterdump()))
        self.assertEqual(self.store.connection.execute('select status from inventory_operations where operation_id=?',(key,)).fetchone()[0], 'verification_required')

    def test_incomplete_or_conflicting_local_evidence_keeps_old_issue(self):
        key, later = self.completed_later_fixture()
        c = self.store.connection
        mutations = [
            "delete from outbound_documents where document_number='QTCK20260924002'",
            "update outbound_documents set items_json='[]' where document_number='QTCK20260924001'",
            "update outbound_documents set document_type='production_materials' where document_number='QTCK20260924001'",
            "update outbound_documents set order_id='PP0001' where document_number='QTCK20260924001'",
            "delete from outbound_document_factories where factory_order='F200'",
            "update inventory_operations set status='external_confirmed' where operation_id=?",
            "update inventory_operations set created_at='2020-01-01T00:00:00-07:00' where operation_id=?",
        ]
        for statement in mutations:
            with self.subTest(statement=statement):
                c.execute('savepoint incomplete')
                c.execute(statement, (later,) if '?' in statement else ())
                pending = pending_inventory_operations(self.config.workflow_database, connection=c)
                self.assertIn('inventory_recovery:'+key, [item['issue_key'] for item in pending])
                c.execute('rollback to incomplete'); c.execute('release incomplete')
        for field, value in [('production_draft', {'request_id':'uncommitted'}), ('documents', [{'bad':'data'}])]:
            with self.subTest(field=field):
                c.execute('savepoint incomplete')
                payload = json.loads(c.execute('select payload_json from inventory_operations where operation_id=?',(key,)).fetchone()[0])
                payload[field] = value
                c.execute('update inventory_operations set payload_json=? where operation_id=?',(json.dumps(payload),key))
                self.assertEqual(len(pending_inventory_operations(self.config.workflow_database, connection=c)), 1)
                c.execute('rollback to incomplete'); c.execute('release incomplete')

    def test_ambiguous_later_document_keeps_old_issue(self):
        key, later = self.completed_later_fixture()
        c = self.store.connection
        payload = json.loads(c.execute('select payload_json from inventory_operations where operation_id=?',(later,)).fetchone()[0])
        payload['documents'][0]['rawFingerprint'] = 'another-operation'
        duplicate = self.journal.prepare('shipment','PP0099',['F200'],payload)
        self.journal.update(duplicate['operation_id'], 'local_committed',
            results=[dict(remark='F200',documentNumber='QTCK20260924003',saved=True)])
        c.execute("update inventory_operations set created_at='2026-09-24T11:00:00-07:00' where operation_id=?",(duplicate['operation_id'],))
        c.commit()
        self.assertEqual([r['issue_key'] for r in pending_inventory_operations(self.config.workflow_database)], ['inventory_recovery:'+key])

    def test_readonly_browser_failure_does_not_claim_outbound_failed(self):
        """真实入口的浏览器失败和超时均说明读取未完成，且没有持久化业务数据。"""
        import subprocess
        from types import SimpleNamespace
        from tests.test_inventory import _FakeNodeProcess
        from traveler_assistant.inventory import run_jdy
        for timeout in [None, subprocess.TimeoutExpired(['node'], 90)]:
            with self.subTest(timeout=bool(timeout)):
                process = _FakeNodeProcess(SimpleNamespace(returncode=1,stdout='',stderr='库存系统自动操作失败：页面未加载完成'), timeout=timeout)
                with patch('traveler_assistant.inventory._local_setting', return_value='test'), \
                     patch('traveler_assistant.inventory._find_existing_inventory_page', return_value={'url':'https://example.invalid'}), \
                     patch('traveler_assistant.inventory._resolve_jdy_runtime', return_value=(Path('/node'),Path('/modules'))), \
                     patch('traveler_assistant.inventory.subprocess.Popen', return_value=process), \
                     patch.object(InventorySyncStore, 'save_success', side_effect=AssertionError('只读核对不能保存')):
                    with self.assertRaises(RuleError) as caught:
                        run_jdy(self.config, 'verifyOutbound', order_name='F100',
                            verification_document={'orderName':'F100','items':self.document['items']})
                self.assertIn('本次自动核对未完成', str(caught.exception))
                self.assertNotIn('库存未确认成功', str(caught.exception))
                request = json.loads(process.stdin.value)
                self.assertEqual(request['action'], 'verifyOutbound')
                self.assertFalse(request['confirmSave'])

    def test_browser_verification_reads_only_and_rejects_missing_or_wrong_quantity(self):
        """用只提供读取接口的离线页面替身执行真实核对分支及明细校验。"""
        import subprocess
        source = (Path(__file__).resolve().parents[1]/'tools/jdy_inventory.mjs').read_text()
        helpers = source[source.index('const outboundMaterialRows ='):source.index('\nlet context;')]
        # 核对只需这两个既有表格读取函数；其后的浏览器导航由只读替身提供。
        helpers = helpers[:helpers.index('\n/**', helpers.index('const assertOutboundFormMatchesRequest'))] if '\n/**' in helpers[helpers.index('const assertOutboundFormMatchesRequest'):] else helpers
        start = source.index('  } else if (request.action === "verifyOutbound") {')
        end = source.index('  } else if (request.action === "findOutbound")', start)
        branch = source[start:end].split('{',1)[1]
        waiter = source[source.index('const waitForVisibleFrame ='):source.index('/** 检查框架中是否存在匹配元素')]

        script = r'''
const normalizeGridText = value => value.trim();
''' + helpers + r'''
let request, matchCount, quantity, captured, ticks, shownNumber;
const UI_STEP_TIMEOUT = 500;
''' + waiter + r'''
const row = {
  innerText: async () => 'QTCK20260924001 F100',
  dblclick: async () => {},
  locator: selector => selector.includes('grid_invNumber')
    ? {first(){return this},count:async()=>1,textContent:async()=> 'M1001'}
    : {innerText:async()=>String(quantity)}
};
const frame = {frameElement:async()=>({isVisible:async()=>true}), locator: selector => selector.startsWith('#number')
  ? {textContent:async()=>shownNumber}
  : selector.startsWith('thead')
  ? {allTextContents:async()=>['*数量'],nth:()=>({getAttribute:async()=> 'grid_qty'})}
  : {count:async()=>1,nth:()=>row}};
const wrongFrame = {};
const page = {url:()=> 'https://example.invalid/read-only',frames:()=>[frame,wrongFrame],mainFrame:()=>wrongFrame,waitForTimeout:async()=>{ticks+=1}};
const openOtherOutboundList = async () => ({});
const findExactOutboundRows = async () => Array(matchCount).fill(row);
const isOtherOutboundFormFrame = async candidate => candidate === frame && ticks > 1;
const process = {stdout:{write: value => captured=JSON.parse(value)}};
async function verify() {
''' + branch + r'''
}
for (const scenario of [0,1,2,3]) {
 request={orderName:'F100',knownDocumentNumber:'QTCK20260924001',items:[{productCode:'M1001',quantity:2}]};
 matchCount=scenario===1?0:1;quantity=scenario===2?3:2;captured=null;ticks=0;shownNumber=scenario===3?'QTCK999':'QTCK20260924001';
 let failed=false;
 try {await verify()} catch {failed=true}
 if (failed !== (scenario!==0)) throw Error('verification result mismatch');
 if (scenario===0 && !captured.verified) throw Error('missing verified result');
}
'''
        result = subprocess.run(['node','--input-type=module','-e',script],text=True,capture_output=True)
        self.assertEqual(result.returncode,0,result.stderr)
