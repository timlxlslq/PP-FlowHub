"""Hardware stores canonical quantities, not copies of report/catalog labels."""
import sqlite3
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from traveler_assistant.core import Config, RuleError
from traveler_assistant.database import connect_database, ensure_schema
from traveler_assistant.hardware_facts import replace_factory_hardware
from traveler_assistant.inventory import Product, _replace_product_database, InventoryMappings, set_ignored_mapping
from traveler_assistant.manual_hardware import list_manual_hardware, save_manual_hardware
from traveler_assistant.order_details import order_detail
from traveler_assistant.order_index import OrderIndexStore


class HardwareSkuContractTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.config = Config(state_dir=Path(self.temp.name))
        self.config.prepare_storage()
        self.products = [Product('Hardware', 'M1094', 'Catalog rail', 'catalog model', '启用', unit='Sets'),
                         Product('Hardware', 'M2001', 'Other', '', '启用', unit='ea')]
        _replace_product_database(self.config.workflow_database, self.products)
        self.store = OrderIndexStore(self.config.workflow_database)
        self.addCleanup(self.store.close)
        self.c = self.store.connection
        self.store.upsert_order('PP9999')
        self.store.upsert_factory('F100', order_id='PP9999', factory_name='PP9999-KITCHEN')
        self.store.commit()
        self.row = dict(order_id='PP9999', factory_order='F100', product_code='M1094', quantity=6)

    def add_auto(self):
        replace_factory_hardware(self.c, 'F100', [self.row])
        self.c.commit()

    def legacy_columns(self):
        # Model the immediately preceding on-disk schema and migration marker.
        for column in ('source_code', 'name', 'spec', 'unit'):
            self.c.execute(f"alter table hardware_items add column {column} text not null default ''")
        self.c.execute("update hardware_items set source_code='RAW',name='Raw rail',spec='raw size',unit='pcs/个'")
        self.c.execute("delete from workflow_metadata where key='ensure_schema_production_simplification_v1'")
        self.c.execute("insert or replace into workflow_metadata(key,value,updated_at) values('ensure_schema_hardware_delete_v2','ready','old')")
        self.c.commit()

    def test_catalog_labels_are_live_but_confirmed_sku_and_quantity_are_stable(self):
        self.add_auto()
        before = self.c.execute('select * from hardware_items').fetchall()
        InventoryMappings(self.config.workflow_database).save_manual('Raw rail', 'M2001')
        set_ignored_mapping(self.config, 'Raw rail', True)
        _replace_product_database(self.config.workflow_database,
                                  [replace(self.products[0], name='Renamed product', spec='new model'), self.products[1]])
        hardware = order_detail(self.config, 'PP9999')['hardware'][0]
        self.assertEqual((hardware['product_code'],hardware['name'],hardware['spec'],hardware['unit'],hardware['quantity']),
                         ('M1094','Renamed product','new model','Sets',6))
        self.assertEqual(self.c.execute('select * from hardware_items').fetchall(), before)
        self.assertFalse({'source_code','name','spec','unit','active'} & {r[1] for r in self.c.execute('pragma table_info(hardware_items)')})

    def test_bad_or_disabled_sku_cannot_replace_confirmed_hardware(self):
        self.add_auto()
        for code in ('', 'RAW-UNMAPPED', 'M2001'):
            if code == 'M2001':
                self.c.execute("update products set status='停用' where code='M2001'")
                self.c.commit()
            with self.assertRaises(RuleError):
                replace_factory_hardware(self.c, 'F100', [{**self.row,'product_code':code}])
            self.assertEqual(self.c.execute('select product_code,quantity from hardware_items').fetchall(), [('M1094',6)])

    def test_manual_rail_quantity_is_already_in_catalog_units(self):
        snapshot = list_manual_hardware(self.config, 'PP9999')
        saved = save_manual_hardware(self.config,'PP9999',dict(version=snapshot['version'],deletions=[],
            additions=[dict(factory_order='F100',product_code='M1094',quantity=3)]),confirm_write=True)
        self.assertEqual((saved['items'][0]['quantity'], saved['items'][0]['unit']), (3,'Sets'))

    def test_unit_update_rejects_entire_catalog_import_and_direct_update(self):
        self.add_auto()
        before = self.c.execute('select * from products order by code').fetchall()
        with self.assertRaises(RuleError) as error:
            _replace_product_database(self.config.workflow_database,
                                      [replace(self.products[0],unit='Piece'),replace(self.products[1],name='Should roll back')])
        self.assertEqual(error.exception.code, 'hardware_product_unit_locked')
        self.assertEqual(self.c.execute('select * from products order by code').fetchall(), before)
        with self.assertRaises(sqlite3.IntegrityError):
            self.c.execute("update products set unit='Piece' where code='M1094'")
        self.c.rollback()

    def test_missing_catalog_sku_is_retained_for_display_and_blocks_new_writes(self):
        self.add_auto()
        _replace_product_database(self.config.workflow_database,[self.products[1]])
        self.assertEqual(order_detail(self.config,'PP9999')['hardware'][0]['name'],'Catalog rail')
        with self.assertRaises(RuleError):
            replace_factory_hardware(self.c, 'F100', [{**self.row,'quantity':8}])
        self.assertEqual(self.c.execute('select quantity from hardware_items').fetchone(),(6,))

    def test_migration_preserves_quantities_and_ids_and_rebases_fingerprint_once(self):
        self.add_auto()
        before = self.c.execute('select * from hardware_items').fetchall()
        self.legacy_columns()
        self.c.execute("update hardware_source_versions set fingerprint='old-source-label-fingerprint'")
        self.c.commit()
        ensure_schema(self.config.workflow_database)
        ensure_schema(self.config.workflow_database)
        self.assertEqual(self.c.execute('select * from hardware_items').fetchall(),before)
        self.assertFalse(replace_factory_hardware(self.c,'F100',[self.row]))
        self.assertEqual(self.c.execute('pragma foreign_key_check').fetchall(),[])
        self.assertEqual(self.c.execute('pragma integrity_check').fetchone(),('ok',))

    def test_migration_failure_restores_all_retired_columns(self):
        self.add_auto()
        self.legacy_columns()
        before = self.c.execute('select * from hardware_items').fetchall()
        self.c.execute('create view blocked_hardware_drop as select unit from hardware_items')
        self.c.commit()
        with self.assertRaises(sqlite3.OperationalError):
            ensure_schema(self.config.workflow_database)
        self.assertEqual(self.c.execute('select * from hardware_items').fetchall(),before)
        self.assertTrue({'source_code','name','spec','unit'} <= {r[1] for r in self.c.execute('pragma table_info(hardware_items)')})
