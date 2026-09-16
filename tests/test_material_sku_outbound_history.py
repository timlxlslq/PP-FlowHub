import hashlib
import json
import re
import tempfile
import unittest
from pathlib import Path

from traveler_assistant.core import Config
from traveler_assistant.database import connect_database, ensure_schema
from traveler_assistant.inventory import (
    InventoryMappings,
    InventorySyncStore,
    build_database_preview,
    database_stock_requirements,
)
from traveler_assistant.order_index import OrderIndexStore


ORDER_ID = "PP0998"
SOURCE_NAME = "19.1mm--Contract Oak"
ORIGINAL_SKU = "M-PANEL-A"
OTHER_SKU = "M-PANEL-B"
ORIGINAL_QUANTITY = 4.0


def legacy_raw_fingerprint(name: str, quantity: float) -> str:
    """Reproduce the pre-SKU raw outbound fingerprint, independent of runtime code."""
    normalized_name = re.sub(r"[\s_-]+", "", name).upper()
    payload = {"items": [(normalized_name, float(quantity))]}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def mapped_fingerprint(product_code: str, quantity: float) -> str:
    payload = {"items": [(product_code.upper(), float(quantity))]}
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


class MaterialSkuOutboundHistoryTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary_directory.cleanup)
        root = Path(self.temporary_directory.name)
        self.config = Config(state_dir=root / "state")
        self.config.prepare_storage()
        ensure_schema(self.config.workflow_database)
        order_store = OrderIndexStore(self.config.workflow_database)
        order_store.close()

        connection = connect_database(self.config.workflow_database)
        try:
            connection.execute(
                "insert into orders(order_id, order_type, updated_at) values(?,?,?)",
                (ORDER_ID, "owned", "2026-09-15T10:00:00"),
            )
            products = [
                (ORIGINAL_SKU, "Contract Oak A"),
                (OTHER_SKU, "Contract Oak B"),
            ]
            connection.executemany(
                """insert into products(
                       category, code, name, spec, status, unit,
                       normalized_code, normalized_name, normalized_spec,
                       normalized_category, normalized_remark,
                       material_kind, material_color, material_thickness,
                       catalog_present
                   ) values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""",
                [
                    (
                        "Panel",
                        code,
                        product_name,
                        "19.1mm",
                        "启用",
                        "张",
                        re.sub(r"[\s_-]+", "", code).upper(),
                        re.sub(r"[\s_-]+", "", product_name).upper(),
                        "19.1MM",
                        "PANEL",
                        "",
                        "panel",
                        "Contract Oak",
                        "19.1",
                        1,
                    )
                    for code, product_name in products
                ],
            )
            connection.execute(
                """insert into material_items(
                       order_id, product_code, quantity, source_type, updated_at
                   ) values(?,?,?,?,?)""",
                (ORDER_ID, ORIGINAL_SKU, ORIGINAL_QUANTITY, "aihouse", "2026-09-15T10:00:00"),
            )
            connection.execute(
                """insert into outbound_documents(
                       document_number, document_type, order_id, factory_order,
                       status, source, issued_at, source_path, items_json,
                       raw_fingerprint, mapped_fingerprint, updated_at
                   ) values(?,?,?,?,?,?,?,?,?,?,?,?)""",
                (
                    "QTCK-LEGACY-MATERIAL",
                    "materials",
                    ORDER_ID,
                    ORDER_ID,
                    "已出库",
                    "金蝶",
                    "2026-09-14T09:00:00",
                    "legacy-traveler.xlsx",
                    json.dumps(
                        [{"productCode": ORIGINAL_SKU, "quantity": ORIGINAL_QUANTITY}],
                        ensure_ascii=False,
                        separators=(",", ":"),
                    ),
                    legacy_raw_fingerprint(SOURCE_NAME, ORIGINAL_QUANTITY),
                    mapped_fingerprint(ORIGINAL_SKU, ORIGINAL_QUANTITY),
                    "2026-09-14T09:00:00",
                ),
            )
            connection.commit()
        finally:
            connection.close()

        InventoryMappings(self.config.workflow_database).save_manual(
            SOURCE_NAME, ORIGINAL_SKU
        )
        self.sync_store = InventorySyncStore(
            root / "state" / "inventory-sync.json",
            root / "backups",
        )

    def preview(self):
        preview = build_database_preview(self.config, ORDER_ID)
        self.assertTrue(preview.ready)
        self.assertEqual(preview.missing_items, [])
        return preview

    def assert_unchanged(self, preview):
        self.assertEqual(
            self.sync_store.status_for(preview.traveler),
            ("已出库", "QTCK-LEGACY-MATERIAL"),
        )
        plans = self.sync_store.prepare_documents(preview)
        self.assertEqual(len(plans), 1)
        self.assertFalse(plans[0]["changed"])

    def assert_changed(self, preview):
        self.assertEqual(
            self.sync_store.status_for(preview.traveler),
            ("需要更新", "QTCK-LEGACY-MATERIAL"),
        )
        plans = self.sync_store.prepare_documents(preview)
        self.assertEqual(len(plans), 1)
        self.assertTrue(plans[0]["changed"])

    def update_material(self, *, product_code: str, quantity: float):
        connection = connect_database(self.config.workflow_database)
        try:
            connection.execute(
                """update material_items
                   set product_code=?, quantity=?, updated_at=?
                   where order_id=?""",
                (product_code, quantity, "2026-09-15T11:00:00", ORDER_ID),
            )
            connection.commit()
        finally:
            connection.close()

    def test_legacy_human_name_fingerprint_remains_unchanged_for_same_sku_and_quantity(self):
        preview = self.preview()

        self.assertEqual(preview.traveler.documents[ORDER_ID][0].name, SOURCE_NAME)
        self.assertEqual(preview.outbound_items[0].product_code, ORIGINAL_SKU)
        self.assert_unchanged(preview)

    def test_quantity_or_sku_change_still_requires_outbound_update(self):
        self.update_material(product_code=ORIGINAL_SKU, quantity=5)
        self.assert_changed(self.preview())

        self.update_material(product_code=OTHER_SKU, quantity=ORIGINAL_QUANTITY)
        preview = self.preview()
        self.assertEqual(preview.traveler.documents[ORDER_ID][0].name, SOURCE_NAME)
        self.assertEqual(preview.outbound_items[0].product_code, OTHER_SKU)
        self.assert_changed(preview)

    def test_mapping_change_does_not_rebind_saved_material_sku(self):
        InventoryMappings(self.config.workflow_database).save_manual(
            SOURCE_NAME, OTHER_SKU
        )

        preview = self.preview()

        self.assertEqual(preview.outbound_items[0].product_code, ORIGINAL_SKU)
        self.assert_unchanged(preview)

    def test_ignore_change_does_not_remove_confirmed_material_sku(self):
        InventoryMappings(self.config.workflow_database).save_ignored(
            SOURCE_NAME, "后续全局忽略同名的未确认来源材料"
        )

        preview = self.preview()
        order_id, requirements = database_stock_requirements(self.config, ORDER_ID)

        self.assertEqual(preview.ignored_items, [])
        self.assertEqual(
            [(item.product_code, item.quantity) for item in preview.outbound_items],
            [(ORIGINAL_SKU, ORIGINAL_QUANTITY)],
        )
        self.assertEqual(order_id, ORDER_ID)
        self.assertEqual(
            [
                (row["productCode"], row["requiredQuantity"])
                for row in requirements
            ],
            [(ORIGINAL_SKU, ORIGINAL_QUANTITY)],
        )
        self.assert_unchanged(preview)


if __name__ == "__main__":
    unittest.main()
