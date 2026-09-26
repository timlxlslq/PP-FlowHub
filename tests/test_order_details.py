import tempfile
import unittest
from pathlib import Path

from traveler_assistant.core import Config
from traveler_assistant.database import connect_database
from traveler_assistant.inventory import Product, _replace_product_database
from traveler_assistant.order_details import order_detail
from traveler_assistant.order_index import OrderIndexStore


class OrderDetailsTests(unittest.TestCase):
    # 验证五金详情采用商品目录属性，不被映射显示别名覆盖。
    # self：当前测试用例或测试替身实例。
    def test_hardware_detail_uses_catalog_not_mapping_display_alias(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = Config(state_dir=root / "state")
            config.prepare_storage()
            OrderIndexStore(config.workflow_database).close()
            _replace_product_database(config.workflow_database, [
                Product("Hardware", "M1001", "Unihopper Hinge", "", "启用"),
            ])
            connection = connect_database(config.workflow_database)
            connection.execute(
                """insert into orders(order_id, order_type, source_folder, updated_at)
                   values(?,?,?,?)""",
                ("PP0002", "owned", "", "now"),
            )
            connection.execute(
                "insert into factory_orders(factory_order,order_id,factory_name,updated_at,stage) select v.factory_order,v.order_id,v.factory_name,v.updated_at,case when v.outbound_status='已出库' then '已出货' when v.optimized then '已优化' else '已拆单' end from (select ? as factory_order,? as order_id,? as factory_name,? as optimized,? as outbound_status,? as updated_at) v",
                ("F0002", "PP0002", "工厂单", 0, "", "now"),
            )
            connection.execute(
                'insert into hardware_items(order_id,factory_order,scope,product_code,quantity,source_type,updated_at) values(?,?,?,?,?,?,?)',
                ('PP0002', 'F0002', 'factory_order', 'M1001', 2, 'aicnc', 'now'),
            )
            connection.commit()
            connection.close()

            from traveler_assistant.inventory import save_manual_mapping

            save_manual_mapping(config, "Hinge", "M1001", "柜门铰链")
            hardware = order_detail(config, "PP0002")["hardware"]
            self.assertEqual(hardware[0]["name"], "Unihopper Hinge")
            self.assertNotIn("source_code", hardware[0])
            self.assertEqual(hardware[0]["product_code"], "M1001")
            self.assertEqual(hardware[0]["display_name"], "Unihopper Hinge")
    # 验证不同厚度的同色饰面板投影使用相同的颜色图片标识。
    # self：当前测试用例或测试替身实例。
    def test_panel_projection_uses_one_color_image_identity_across_thicknesses(self):
        with tempfile.TemporaryDirectory() as directory:
            config = Config(state_dir=Path(directory) / "state")
            config.prepare_storage()
            OrderIndexStore(config.workflow_database).close()
            _replace_product_database(config.workflow_database, [
                Product("Panel", "M0001", "Woodline 4", "19.1mm", "启用", brand="LIOHER"),
                Product("Panel", "M1001", "Woodline 4", "9mm", "启用", brand="LIOHER"),
            ])
            connection = connect_database(config.workflow_database)
            for product_code in ("M0001", "M1001"):
                connection.execute(
                    """
                    insert into material_items(
                        order_id, product_code, quantity, source_type, source_path,
                        source_fingerprint, updated_at
                    ) values(?,?,?,?,?,?,?)
                    """,
                    ("PP0001", product_code, 1, "aihouse", "", "", "now"),
                )
            connection.commit()
            connection.close()

            panels = [
                row for row in order_detail(config, "PP0001")["materials"]
                if row["material_type"] == "panel"
            ]
            self.assertEqual([row["product_code"] for row in panels], ["M0001", "M1001"])
            self.assertEqual({row["brand"] for row in panels}, {"LIOHER"})


if __name__ == "__main__":
    unittest.main()
