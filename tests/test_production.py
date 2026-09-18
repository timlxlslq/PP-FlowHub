import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from traveler_assistant.core import Config
from traveler_assistant.database import connect_database, ensure_schema
from traveler_assistant.order_index import OrderIndexStore
from traveler_assistant.production import (
    cumulative_production_materials,
    material_key,
    production_material_code,
    prepare_production,
    production_preview,
    record_completed_production,
)


class ProductionTransactionTests(unittest.TestCase):
    def test_app_material_identity_and_conflicting_sku(self):
        self.assertEqual(production_material_code({"key": "M0019"}), "M0019")
        self.assertEqual(production_material_code({"product_code": "M0019"}), "M0019")
        from traveler_assistant.core import RuleError
        for row in ({}, {"key": "M0019", "product_code": "M0020"}):
            with self.assertRaises(RuleError):
                production_material_code(row)

    @staticmethod
    def _seed_products(connection):
        connection.executemany(
            """insert into products(
                category, code, name, spec, status, unit,
                normalized_code, normalized_name, normalized_spec,
                normalized_category, normalized_remark,
                material_kind, material_color, material_thickness, catalog_present
            ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,1)""",
            [
                ("Panel", "M0019", "Woodline 4", "19.1*1220*2745mm", "启用", "SHT", "m0019", "woodline4", "19112202745mm", "panel", "", "panel", "Woodline 4", "19.1"),
                ("Edge band", "M0020", "Woodline 4 Edge Banding", "22mm*1mm*225m", "启用", "M", "m0020", "woodline4edgebanding", "22mm1mm225m", "edgeband", "", "edge", "Woodline 4", ""),
                ("Panel", "M-ROS", "Rosales 3", "19.1*1220*2745mm", "启用", "SHT", "mros", "rosales3", "19112202745mm", "panel", "", "panel", "Rosales 3", "19.1"),
            ],
        )

    def test_production_preview_aggregates_duplicate_order_material_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(state_dir=Path(directory) / "state")
            config.prepare_storage()
            ensure_schema(config.workflow_database)
            store = OrderIndexStore(config.workflow_database)
            connection = store.connection
            self._seed_products(connection)
            connection.execute(
                "insert into orders(order_id, order_type, updated_at) values(?,?,?)",
                ("PP010", "owned", "now"),
            )
            connection.execute(
                "insert into factory_orders(factory_order,order_id,factory_name,updated_at,stage) select v.factory_order,v.order_id,v.factory_name,v.updated_at,case when v.outbound_status='已出库' then '已出货' when v.optimized then '已优化' else '已拆单' end from (select ? as factory_order,? as order_id,? as factory_name,? as optimized,? as outbound_status,? as updated_at) v",
                ("F2010", "PP010", "PP010-KITCHEN", 1, "未查询", "now"),
            )
            connection.executemany(
                """insert into material_items(
                       order_id, product_code, quantity, source_type, source_path,
                       source_fingerprint, updated_at
                   ) values(?,?,?,?,?,?,?)""",
                [
                    ("PP010", "M-ROS", 8, "aihouse", "source-a", "source-a-fp", "now"),
                    ("PP010", "M-ROS", 10, "aihouse", "source-b", "source-b-fp", "now"),
                ],
            )
            store.commit()
            store.close()

            preview = production_preview(config, "PP010", ["F2010"])

            self.assertEqual(len(preview["materials"]), 1)
            self.assertEqual(preview["materials"][0]["total_quantity"], 18)
            self.assertEqual(preview["materials"][0]["remaining_quantity"], 18)

    def test_production_preview_deducts_legacy_inventory_materials(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(state_dir=Path(directory) / "state")
            config.prepare_storage()
            ensure_schema(config.workflow_database)
            store = OrderIndexStore(config.workflow_database)
            connection = store.connection
            self._seed_products(connection)
            connection.execute(
                "insert into orders(order_id, order_type, updated_at) values(?,?,?)",
                ("CS010", "cutToSize", "now"),
            )
            connection.executemany(
                "insert into factory_orders(factory_order,order_id,factory_name,updated_at,stage) select v.factory_order,v.order_id,v.factory_name,v.updated_at,case when v.outbound_status='已出库' then '已出货' when v.optimized then '已优化' else '已拆单' end from (select ? as factory_order,? as order_id,? as factory_name,? as optimized,? as outbound_status,? as updated_at) v",
                [
                    ("F1010", "CS010", "CS010-KITCHEN", 1, "已出库", "now"),
                    ("F1011", "CS010", "CS010-vanity", 1, "未查询", "now"),
                ],
            )
            connection.executemany(
                """insert into material_items(
                       order_id, product_code, quantity, source_type, source_path,
                       source_fingerprint, updated_at
                   ) values(?,?,?,?,?,?,?)""",
                [
                    ("CS010", "M0019", 5, "aihouse", "panel-source", "panel-fp", "now"),
                    ("CS010", "M0020", 158, "aihouse", "edge-source", "edge-fp", "now"),
                ],
            )
            connection.execute(
                """insert into production_records(
                       production_time, source, status, created_at, updated_at
                   ) values(?,?,?,?,?)""",
                ("", "legacy-outbound-migration", "completed", "now", "now"),
            )
            batch_id = connection.execute("select last_insert_rowid()").fetchone()[0]
            connection.execute(
                "update factory_orders set production_record_id=? where order_id=? and factory_order=?",
                (batch_id, "CS010", "F1010"),
            )
            connection.execute(
                """insert into outbound_documents(
                       document_number, document_type, order_id, factory_order,
                       status, source, items_json, updated_at
                   ) values(?,?,?,?,?,?,?,?)""",
                (
                    "QTCK-HISTORY", "materials", "CS010", "CS010", "已出库", "金蝶",
                    json.dumps([
                        {"productCode": "M0019", "quantity": 4},
                        {"productCode": "M0020", "quantity": 102},
                    ]),
                    "now",
                ),
            )
            connection.execute(
                """insert into outbound_document_factories(
                       document_number, order_id, factory_order, created_at, updated_at
                   ) values(?,?,?,?,?)""",
                ("QTCK-HISTORY", "CS010", "F1010", "now", "now"),
            )
            store.commit()
            store.close()

            preview = production_preview(config, "CS010", ["F1011"])
            remaining = {item["material_type"]: item["remaining_quantity"] for item in preview["materials"]}
            self.assertEqual(remaining["panel"], 1)
            self.assertEqual(remaining["edge"], 56)

            cumulative = cumulative_production_materials(
                config,
                "CS010",
                [
                    {
                        "product_code": "M0019",
                        "material_type": "panel", "color": "Woodline 4",
                        "thickness": "19.1", "edge": "", "unit": "SHT",
                        "quantity": 1,
                    },
                    {
                        "product_code": "M0020",
                        "material_type": "edge", "color": "Woodline 4",
                        "thickness": "", "edge": "Woodline 4", "unit": "M",
                        "quantity": 56,
                    },
                ],
            )
            cumulative_by_type = {item["material_type"]: item["quantity"] for item in cumulative}
            self.assertEqual(cumulative_by_type, {"edge": 158, "panel": 5})

            connection = connect_database(config.workflow_database)
            connection.execute(
                """insert into production_materials(
                       batch_id, order_id, product_code, quantity
                   ) values(?,?,?,?)""",
                (batch_id, "CS010", "M0019", 4),
            )
            connection.execute(
                """insert into production_materials(
                       batch_id, order_id, product_code, quantity
                   ) values(?,?,?,?)""",
                (batch_id, "CS010", "M0020", 102),
            )
            connection.commit()
            connection.close()

            preview = production_preview(config, "CS010", ["F1011"])
            remaining = {item["material_type"]: item["remaining_quantity"] for item in preview["materials"]}
            self.assertEqual(remaining["panel"], 1)
            self.assertEqual(remaining["edge"], 56)

    def test_prepare_production_is_read_only_until_inventory_succeeds(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(state_dir=Path(directory) / "state")
            config.prepare_storage()
            ensure_schema(config.workflow_database)
            store = OrderIndexStore(config.workflow_database)
            connection = store.connection
            self._seed_products(connection)
            connection.execute(
                "insert into orders(order_id, order_type, updated_at) values(?,?,?)",
                ("CS010", "cutToSize", "now"),
            )
            connection.execute(
                "insert into factory_orders(factory_order,order_id,factory_name,updated_at,stage) select v.factory_order,v.order_id,v.factory_name,v.updated_at,case when v.outbound_status='已出库' then '已出货' when v.optimized then '已优化' else '已拆单' end from (select ? as factory_order,? as order_id,? as factory_name,? as optimized,? as outbound_status,? as updated_at) v",
                ("F1010", "CS010", "CS010-KITCHEN", 1, "未出库", "now"),
            )
            connection.execute(
                """insert into material_items(
                       order_id, product_code, quantity, source_type, source_path,
                       source_fingerprint, updated_at
                   ) values(?,?,?,?,?,?,?)""",
                ("CS010", "M0019", 5, "aihouse", "panel-source", "panel-fp", "now"),
            )
            connection.commit()
            store.commit()
            store.close()

            key = material_key({
                "product_code": "M0019",
                "material_type": "panel",
                "color": "Woodline 4",
                "thickness": "19.1",
                "edge": "",
                "unit": "SHT",
            })
            draft = prepare_production(
                config,
                "CS010",
                ["F1010"],
                [{"key": key, "quantity": 2}],
            )

            connection = sqlite3.connect(config.workflow_database)
            self.assertEqual(
                connection.execute("select count(*) from production_records").fetchone()[0],
                0,
            )
            connection.close()
            self.assertEqual(draft["status"], "draft")
            self.assertEqual(draft["materials"][0]["quantity"], 2)

    def test_completed_production_can_share_the_local_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "workflow.sqlite3"
            ensure_schema(database)
            store = OrderIndexStore(database)
            connection = store.connection
            connection.execute("insert into factory_orders(factory_order,order_id,stage,updated_at) values('F1010','CS010','已优化','now')")
            self._seed_products(connection)
            result = record_completed_production(
                connection,
                {
                    "batch_number": "MP-TEST-001",
                    "order_id": "CS010",
                    "selected_factory_orders": ["F1010"],
                    "materials": [{
                        "product_code": "M0019",
                        "material_type": "panel",
                        "color": "Woodline 4",
                        "thickness": "19.1",
                        "edge": "",
                        "unit": "SHT",
                        "quantity": 2,
                    }],
                },
            )
            connection.commit()
            self.assertEqual(result["status"], "completed")
            self.assertEqual(
                connection.execute(
                    "select status from production_records where batch_id=?",
                    (result["production_record_id"],),
                ).fetchone()[0],
                "completed",
            )
            connection.close()


if __name__ == "__main__":
    unittest.main()
