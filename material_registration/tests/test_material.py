# -*- coding: utf-8 -*-
from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests.common import TransactionCase
from odoo.tools import mute_logger


class TestMaterialModel(TransactionCase):
    """Unit tests for the Material domain entity and its invariants."""

    def setUp(self):
        super().setUp()
        self.Material = self.env['material.material']
        self.supplier = self.env['material.supplier'].create({'name': 'ACME'})

    def _values(self, **overrides):
        values = {
            'code': 'MAT-100',
            'name': 'Test Material',
            'material_type': 'fabric',
            'buy_price': 150.0,
            'supplier_id': self.supplier.id,
        }
        values.update(overrides)
        return values

    def test_create_valid_material(self):
        material = self.Material.create(self._values())
        self.assertEqual(material.code, 'MAT-100')
        self.assertEqual(material.supplier_id, self.supplier)

    def test_buy_price_below_100_rejected(self):
        with self.assertRaises(ValidationError):
            self.Material.create(self._values(buy_price=99.99))

    def test_buy_price_exactly_100_allowed(self):
        material = self.Material.create(self._values(buy_price=100.0))
        self.assertEqual(material.buy_price, 100.0)

    def test_write_below_100_rejected(self):
        material = self.Material.create(self._values())
        with self.assertRaises(ValidationError):
            material.buy_price = 50.0

    @mute_logger('odoo.sql_db')
    def test_code_must_be_unique(self):
        self.Material.create(self._values(code='DUP'))
        with self.assertRaises(IntegrityError):
            self.Material.create(self._values(code='DUP', name='Other'))
            self.Material.flush()

    def test_material_type_selection(self):
        keys = dict(self.Material._fields['material_type'].selection).keys()
        self.assertEqual(set(keys), {'fabric', 'jeans', 'cotton'})
