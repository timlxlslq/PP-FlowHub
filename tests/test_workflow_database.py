import sqlite3
import tempfile
import unittest
from datetime import date, timedelta
from pathlib import Path

from traveler_assistant.backup import _apply_retention, backup_status, perform_backup
from traveler_assistant.core import Config
from traveler_assistant.database import ensure_schema, migrate_legacy_databases
from traveler_assistant.order_details import order_detail
from traveler_assistant.order_index import OrderIndexStore


class WorkflowDatabaseTests(unittest.TestCase):
    # 验证旧的合并出库单据迁移后保留每个工厂单的关联。
    # self：当前测试用例或测试替身实例。
    def test_grouped_outbound_document_migrates_to_factory_links(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "workflow.sqlite3"
            connection = sqlite3.connect(path)
            connection.executescript(
                """
                create table factory_orders(
                    factory_order text primary key,
                    order_id text not null default '',
                    factory_name text not null default '',
                    sales_order_name text not null default '',
                    aimes_status text not null default 'active'
                );
                create table outbound_documents(
                    id integer primary key,
                    document_number text not null unique,
                    document_type text not null default '',
                    order_id text not null default '',
                    factory_order text not null default '',
                    status text not null default 'recorded',
                    source text not null default '',
                    issued_at text not null default '',
                    source_path text not null default '',
                    updated_at text not null
                );
                insert into factory_orders(factory_order, order_id, factory_name, sales_order_name)
                    values
                    ('F100', 'PP9999', 'PP9999-MASTER', 'PP9999'),
                    ('F101', 'PP9999', 'PP9999-1ST', 'PP9999'),
                    ('F102', 'PP9999', 'PP9999-2ND', 'PP9999');
                insert into outbound_documents(
                    document_number, document_type, order_id, factory_order,
                    status, source, issued_at, updated_at
                ) values(
                    'QTCK-GROUPED', '库存出库单', 'PP9999', 'F100,F101,F102',
                    '已出库', 'user-confirmed-grouped', '2026-08-19', 'now'
                );
                """
            )
            connection.commit()
            connection.close()

            ensure_schema(path)

            connection = sqlite3.connect(path)
            links = connection.execute(
                "select factory_order from outbound_document_factories "
                "where document_number='QTCK-GROUPED' order by factory_order"
            ).fetchall()
            connection.close()

        self.assertEqual(links, [("F100",), ("F101",), ("F102",)])

    # 验证材料表迁移至订单层级后移除旧分配结构并保留材料事实。
    # self：当前测试用例或测试替身实例。
    def test_material_table_migrates_to_order_scope_and_removes_allocations(self):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "workflow.sqlite3"
            connection = sqlite3.connect(path)
            connection.executescript(
                """
                create table material_items(
                    id integer primary key,
                    order_id text not null default '',
                    factory_order text not null default '',
                    scope text not null default 'factory_order',
                    material_type text not null default '',
                    color text not null default '',
                    thickness text not null default '',
                    quantity real not null default 0,
                    unit text not null default '',
                    edge text not null default '',
                    source_type text not null default '',
                    source_path text not null default '',
                    source_fingerprint text not null default '',
                    updated_at text not null
                );
                create table products(
                    category text not null default '', code text primary key,
                    name text not null default '', spec text not null default '',
                    status text not null default '', brand text not null default '',
                    remark text not null default '', unit text not null default '',
                    cost_price real, normalized_code text not null,
                    normalized_name text not null, normalized_spec text not null,
                    normalized_category text not null, normalized_remark text not null
                );
                insert into products values(
                    'Panel','M-PANEL','White','19.1mm','启用','','','pcs',null,
                    'MPANEL','WHITE','191MM','PANEL',''
                );
                create table material_allocations(id integer primary key);
                insert into material_items(order_id, factory_order, scope, material_type, color, thickness, quantity, unit, updated_at)
                    values('PP9999', '', 'order', 'panel', 'White', '19.1', 4, 'pcs', 'now');
                insert into material_items(order_id, factory_order, scope, material_type, color, thickness, quantity, unit, updated_at)
                    values('PP9999', 'F100', 'factory_order', 'panel', 'White', '19.1', 2, 'pcs', 'now');
                """
            )
            connection.commit()
            connection.close()

            ensure_schema(path)

            connection = sqlite3.connect(path)
            columns = [row[1] for row in connection.execute("pragma table_info(material_items)")]
            self.assertNotIn("factory_order", columns)
            self.assertNotIn("scope", columns)
            self.assertEqual(columns, [
                "id", "order_id", "product_code", "quantity", "source_type",
                "source_path", "source_fingerprint", "updated_at",
            ])
            self.assertEqual(connection.execute("select quantity from material_items").fetchone()[0], 4)
            self.assertEqual(connection.execute("select product_code from material_items").fetchone()[0], "M-PANEL")
            self.assertIsNone(connection.execute("select 1 from sqlite_master where name='material_allocations'").fetchone())
            connection.close()

    # 验证旧订单数据库迁移不读取独立库存数据库。
    # self：当前测试用例或测试替身实例。
    def test_legacy_order_database_migrates_without_reading_inventory_database(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "state"
            state.mkdir()
            legacy_order = state / "order-index.sqlite3"
            connection = sqlite3.connect(legacy_order)
            connection.execute("create table orders(order_id text primary key, order_type text)")
            connection.execute("insert into orders values('PP9999','owned')")
            connection.commit(); connection.close()
            legacy_inventory = state / "inventory" / "inventory.sqlite3"
            legacy_inventory.parent.mkdir()
            connection = sqlite3.connect(legacy_inventory)
            connection.execute("create table products(code text primary key, name text)")
            connection.execute("insert into products values('M1','Test')")
            connection.commit(); connection.close()

            result = migrate_legacy_databases(state)
            central = state / "workflow.sqlite3"
            self.assertEqual(result["status"], "completed")
            connection = sqlite3.connect(central)
            self.assertEqual(connection.execute("select order_id from orders").fetchone()[0], "PP9999")
            self.assertIsNotNone(
                connection.execute(
                    "select 1 from sqlite_master where type='table' and name='products'"
                ).fetchone()
            )
            self.assertIsNone(connection.execute("select code from products where code='M1'").fetchone())
            connection.close()
            self.assertTrue(list((state / "migration-archives").rglob("*.sqlite3")))
            self.assertTrue(legacy_inventory.is_file())

    # 验证源批次信息不会凭空生成生产记录或业务冲突。
    # self：当前测试用例或测试替身实例。
    def test_source_batches_do_not_create_production_or_conflicts(self):
        with tempfile.TemporaryDirectory() as temp:
            store = OrderIndexStore(Path(temp) / 'workflow.sqlite3')
            store.upsert_aimes_factory("F1", order_id="PP9999", factory_name="PP9999-KITCHEN", sales_order_name="PP9999", split_time="", seen_at="now")
            for number in ('PC124429962607080001','PC124429962606270001'):
                store.update_source_file_identity(Path('/tmp') / number / 'report.xlsx', order_id='PP9999', factory_order='F1')
            self.assertIsNone(store.connection.execute("select production_record_id from factory_orders where factory_order='F1'").fetchone()[0])
            self.assertFalse(any(i['kind']=='batch_conflict' for i in store.active_issues()))
            self.assertFalse(store.connection.execute("select 1 from sqlite_master where name in ('production_batches','batch_evidence')").fetchall())
            store.close()

    # 验证没有成功备份记录时，备份状态提示用户执行操作。
    # self：当前测试用例或测试替身实例。
    def test_backup_status_requires_user_action_without_successful_record(self):
        with tempfile.TemporaryDirectory() as temp:
            config = Config(state_dir=Path(temp) / "state", backup_root=Path(temp) / "server" / "database-backups")
            config.prepare_storage()
            status = backup_status(config, date.today())
            self.assertTrue(status["requires_user_attention"])

    # 验证备份保留策略保留近期每日备份及周日周备份。
    # self：当前测试用例或测试替身实例。
    def test_retention_keeps_recent_daily_and_sunday_weekly_backups(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            today = date(2026, 8, 15)
            for day in (
                today - timedelta(days=1),
                today - timedelta(days=2),
                today - timedelta(days=3),
                today - timedelta(days=4),
                today - timedelta(days=20),
                today - timedelta(days=21),
                today - timedelta(days=100),
            ):
                (root / f"workflow-{day.isoformat()}.sqlite3").touch()
            _apply_retention(root, today)
            self.assertTrue((root / "workflow-2026-08-14.sqlite3").exists())
            self.assertTrue((root / "workflow-2026-08-12.sqlite3").exists())  # 该周最新一份备份
            self.assertFalse((root / "workflow-2026-08-11.sqlite3").exists())
            self.assertTrue((root / "workflow-2026-07-26.sqlite3").exists())  # 该周最新一份备份
            self.assertFalse((root / "workflow-2026-05-07.sqlite3").exists())

    # 验证备份执行结果存放在本地数据库备份目录中。
    # self：当前测试用例或测试替身实例。
    def test_perform_backup_uses_local_database_backup_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            state = Path(temp) / "state"
            config = Config(state_dir=state, backup_root=Path(temp) / "traveler-backups")
            config.prepare_storage()
            result = perform_backup(config)

            destination = Path(result["path"])
            self.assertEqual(destination.parent, state / "database-backups")
            self.assertTrue(destination.is_file())
            self.assertEqual(
                sqlite3.connect(destination).execute("pragma integrity_check").fetchone()[0],
                "ok",
            )


if __name__ == "__main__":
    unittest.main()
