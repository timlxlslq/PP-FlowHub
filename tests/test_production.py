import json
import sqlite3
import tempfile
import unittest
from pathlib import Path

from traveler_assistant.core import Config
from traveler_assistant.database import ensure_schema
from traveler_assistant.order_index import OrderIndexStore
from traveler_assistant.production import (
    cumulative_production_materials,
    material_key,
    prepare_production,
    production_preview,
    record_completed_production,
)


class ProductionTransactionTests(unittest.TestCase):
    @staticmethod
    def _create_product_table(connection):
        connection.execute(
            """create table products(
                category text not null default '', code text primary key,
                name text not null default '', spec text not null default '',
                status text not null default '', brand text not null default '',
                remark text not null default '', unit text not null default '',
                cost_price real, normalized_code text not null,
                normalized_name text not null, normalized_spec text not null,
                normalized_category text not null, normalized_remark text not null
            )"""
        )
        connection.executemany(
            """insert into products(
                category, code, name, spec, status, unit,
                normalized_code, normalized_name, normalized_spec,
                normalized_category, normalized_remark
            ) values(?,?,?,?,?,?,?,?,?,?,?)""",
            [
                ("Panel", "M0019", "Woodline 4", "19.1*1220*2745mm", "启用", "SHT", "m0019", "woodline4", "19112202745mm", "panel", ""),
                ("Edge band", "M0020", "Woodline 4 Edge Banding", "22mm*1mm*225m", "启用", "M", "m0020", "woodline4edgebanding", "22mm1mm225m", "edgeband", ""),
            ],
        )

    def test_production_preview_aggregates_duplicate_order_material_rows(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(state_dir=Path(directory) / "state")
            config.prepare_storage()
            ensure_schema(config.workflow_database)
            store = OrderIndexStore(config.workflow_database)
            connection = store.connection
            connection.execute(
                "insert into orders(order_id, order_type, updated_at) values(?,?,?)",
                ("PP010", "owned", "now"),
            )
            connection.execute(
                """insert into factory_orders(
                       factory_order, order_id, factory_name, optimized,
                       outbound_status, updated_at
                   ) values(?,?,?,?,?,?)""",
                ("F2010", "PP010", "PP010-KITCHEN", 1, "未查询", "now"),
            )
            connection.executemany(
                """insert into material_items(
                       order_id, material_type, color, thickness, quantity,
                       unit, edge, source_type, source_path, updated_at
                   ) values(?,?,?,?,?,?,?,?,?,?)""",
                [
                    ("PP010", "panel", "Rosales 3", "19.1", 8, "pcs", "", "aihouse", "source-a", "now"),
                    ("PP010", "panel", "Rosales 3", "19.1", 10, "pcs", "", "aihouse", "source-b", "now"),
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
            self._create_product_table(connection)
            connection.execute(
                "insert into orders(order_id, order_type, updated_at) values(?,?,?)",
                ("CS010", "cutToSize", "now"),
            )
            connection.executemany(
                """insert into factory_orders(
                       factory_order, order_id, factory_name, optimized,
                       outbound_status, updated_at
                   ) values(?,?,?,?,?,?)""",
                [
                    ("F1010", "CS010", "CS010-KITCHEN", 1, "已出库", "now"),
                    ("F1011", "CS010", "CS010-vanity", 1, "未查询", "now"),
                ],
            )
            connection.executemany(
                """insert into material_items(
                       order_id, material_type, color, thickness, quantity,
                       unit, edge, source_type, updated_at
                   ) values(?,?,?,?,?,?,?,?,?)""",
                [
                    ("CS010", "panel", "Woodline 4", "19.1", 5, "pcs", "", "aihouse", "now"),
                    ("CS010", "edge", "Woodline 4", "", 158, "m", "Woodline 4", "aihouse", "now"),
                ],
            )
            connection.execute(
                """insert into manual_production_batches(
                       batch_number, order_id, production_time, source, status, created_at, updated_at
                   ) values(?,?,?,?,?,?,?)""",
                ("LEGACY-F1010", "CS010", "", "legacy-outbound-migration", "completed", "now", "now"),
            )
            batch_id = connection.execute("select last_insert_rowid()").fetchone()[0]
            connection.execute(
                "insert into manual_production_batch_factories(batch_id, order_id, factory_order) values(?,?,?)",
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
                        "material_type": "panel", "color": "Woodline 4",
                        "thickness": "19.1", "edge": "", "unit": "pcs",
                        "quantity": 1,
                    },
                    {
                        "material_type": "edge", "color": "Woodline 4",
                        "thickness": "", "edge": "Woodline 4", "unit": "m",
                        "quantity": 56,
                    },
                ],
            )
            cumulative_by_type = {item["material_type"]: item["quantity"] for item in cumulative}
            self.assertEqual(cumulative_by_type, {"edge": 158, "panel": 5})

            connection = sqlite3.connect(config.workflow_database)
            connection.execute(
                """insert into manual_production_batch_materials(
                       batch_id, order_id, material_type, color, thickness, edge, unit, quantity
                   ) values(?,?,?,?,?,?,?,?)""",
                (batch_id, "CS010", "panel", "Woodline 4", "19.1", "", "pcs", 4),
            )
            connection.execute(
                """insert into manual_production_batch_materials(
                       batch_id, order_id, material_type, color, thickness, edge, unit, quantity
                   ) values(?,?,?,?,?,?,?,?)""",
                (batch_id, "CS010", "edge", "Woodline 4", "", "Woodline 4", "m", 102),
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
            connection.execute(
                "insert into orders(order_id, order_type, updated_at) values(?,?,?)",
                ("CS010", "cutToSize", "now"),
            )
            connection.execute(
                """insert into factory_orders(
                       factory_order, order_id, factory_name, optimized,
                       outbound_status, updated_at
                   ) values(?,?,?,?,?,?)""",
                ("F1010", "CS010", "CS010-KITCHEN", 1, "未出库", "now"),
            )
            connection.execute(
                """insert into material_items(
                       order_id, material_type, color, thickness, quantity,
                       unit, source_type, updated_at
                   ) values(?,?,?,?,?,?,?,?)""",
                ("CS010", "panel", "Woodline 4", "19.1", 5, "pcs", "aihouse", "now"),
            )
            connection.commit()
            store.commit()
            store.close()

            key = material_key({
                "material_type": "panel",
                "color": "Woodline 4",
                "thickness": "19.1",
                "edge": "",
                "unit": "pcs",
            })
            draft = prepare_production(
                config,
                "CS010",
                ["F1010"],
                [{"key": key, "quantity": 2}],
            )

            connection = sqlite3.connect(config.workflow_database)
            self.assertEqual(
                connection.execute("select count(*) from manual_production_batches").fetchone()[0],
                0,
            )
            connection.close()
            self.assertEqual(draft["status"], "draft")
            self.assertEqual(draft["materials"][0]["quantity"], 2)

    def test_completed_production_can_share_the_local_commit(self):
        with tempfile.TemporaryDirectory() as directory:
            database = Path(directory) / "workflow.sqlite3"
            ensure_schema(database)
            connection = sqlite3.connect(database)
            result = record_completed_production(
                connection,
                {
                    "batch_number": "MP-TEST-001",
                    "order_id": "CS010",
                    "selected_factory_orders": ["F1010"],
                    "materials": [{
                        "material_type": "panel",
                        "color": "Woodline 4",
                        "thickness": "19.1",
                        "edge": "",
                        "unit": "pcs",
                        "quantity": 2,
                    }],
                },
            )
            connection.commit()
            self.assertEqual(result["status"], "completed")
            self.assertEqual(
                connection.execute(
                    "select status from manual_production_batches where batch_number=?",
                    ("MP-TEST-001",),
                ).fetchone()[0],
                "completed",
            )
            connection.close()


if __name__ == "__main__":
    unittest.main()
