# -*- coding: utf-8 -*-
from odoo.exceptions import UserError, ValidationError
from odoo.tests.common import TransactionCase


class TestMaterialService(TransactionCase):
    """Unit tests for the material.service use cases.

    These exercise the same logic the REST controller runs, without an
    HTTP layer, so create/read/update/delete/filter are all covered.
    """

    def setUp(self):
        super().setUp()
        self.service = self.env['material.service']
        self.supplier = self.env['material.supplier'].create({'name': 'ACME'})
        self.other_supplier = self.env['material.supplier'].create(
            {'name': 'Globex'})

    def _payload(self, **overrides):
        payload = {
            'code': 'MAT-200',
            'name': 'Service Material',
            'material_type': 'cotton',
            'buy_price': 300.0,
            'supplier_id': self.supplier.id,
        }
        payload.update(overrides)
        return payload

    def test_create_and_serialize(self):
        data = self.service.create_material(self._payload())
        self.assertEqual(data['code'], 'MAT-200')
        self.assertEqual(data['supplier_name'], 'ACME')
        self.assertIn('id', data)

    def test_create_below_min_price_rejected(self):
        with self.assertRaises(ValidationError):
            self.service.create_material(self._payload(buy_price=10.0))

    def test_get_material(self):
        created = self.service.create_material(self._payload())
        fetched = self.service.get_material(created['id'])
        self.assertEqual(fetched['id'], created['id'])

    def test_get_missing_raises(self):
        with self.assertRaises(UserError):
            self.service.get_material(999999)

    def test_update_material(self):
        created = self.service.create_material(self._payload())
        updated = self.service.update_material(
            created['id'], {'name': 'Renamed', 'buy_price': 500.0})
        self.assertEqual(updated['name'], 'Renamed')
        self.assertEqual(updated['buy_price'], 500.0)

    def test_update_ignores_unknown_fields(self):
        created = self.service.create_material(self._payload())
        updated = self.service.update_material(
            created['id'], {'name': 'Clean', 'hacker': 'x'})
        self.assertEqual(updated['name'], 'Clean')

    def test_update_empty_payload_rejected(self):
        created = self.service.create_material(self._payload())
        with self.assertRaises(ValidationError):
            self.service.update_material(created['id'], {'nope': 1})

    def test_delete_material(self):
        created = self.service.create_material(self._payload())
        self.assertTrue(self.service.delete_material(created['id']))
        with self.assertRaises(UserError):
            self.service.get_material(created['id'])

    def test_list_and_filter_by_type(self):
        self.service.create_material(
            self._payload(code='C-1', material_type='cotton'))
        self.service.create_material(
            self._payload(code='F-1', material_type='fabric',
                          supplier_id=self.other_supplier.id))

        all_materials = self.service.list_materials()
        self.assertGreaterEqual(len(all_materials), 2)

        only_fabric = self.service.list_materials(material_type='fabric')
        self.assertTrue(only_fabric)
        self.assertTrue(
            all(m['material_type'] == 'fabric' for m in only_fabric))

    def test_list_invalid_type_rejected(self):
        with self.assertRaises(UserError):
            self.service.list_materials(material_type='silk')
