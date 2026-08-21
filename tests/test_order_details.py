import sqlite3
import tempfile
import unittest
from pathlib import Path

from traveler_assistant.core import Config
from traveler_assistant.inventory import Product, _replace_product_database
from traveler_assistant.order_details import order_detail
from traveler_assistant.order_index import OrderIndexStore


class OrderDetailsTests(unittest.TestCase):
    def test_panel_projection_uses_one_color_image_identity_across_thicknesses(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(state_dir=Path(directory) / "state")
            config.prepare_storage()
            OrderIndexStore(config.workflow_database).close()
            _replace_product_database(config.workflow_database, [
                Product("Panel", "M0001", "Woodline 4", "19.1mm", "启用", brand="LIOHER"),
                Product("Panel", "M1001", "Woodline 4", "9mm", "启用", brand="LIOHER"),
            ])
            connection = sqlite3.connect(config.workflow_database)
            for thickness in ("19.1", "8"):
                connection.execute(
                    """
                    insert into material_items(
                        order_id, material_type, color, thickness, quantity, unit,
                        source_type, source_path, source_fingerprint, updated_at
                    ) values(?,?,?,?,?,?,?,?,?,?)
                    """,
                    ("PP0001", "panel", "Woodline 4", thickness, 1, "pcs", "aihouse", "", "", "now"),
                )
            connection.commit()
            connection.close()

            panels = [
                row for row in order_detail(config, "PP0001")["materials"]
                if row["material_type"] == "panel"
            ]
            self.assertEqual([row["product_code"] for row in panels], ["M0001", "M0001"])
            self.assertEqual({row["brand"] for row in panels}, {"LIOHER"})


if __name__ == "__main__":
    unittest.main()
