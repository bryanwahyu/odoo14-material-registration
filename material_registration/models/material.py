# -*- coding: utf-8 -*-
from odoo import api, fields, models
from odoo.exceptions import ValidationError

MIN_BUY_PRICE = 100.0

MATERIAL_TYPES = [
    ('fabric', 'Fabric'),
    ('jeans', 'Jeans'),
    ('cotton', 'Cotton'),
]


class Material(models.Model):
    """Domain entity: a material to be sold.

    Holds its own invariants (required fields, unique code, minimum buy
    price) so the domain rules are enforced regardless of the caller
    (backend UI, REST API, or unit test).
    """
    _name = 'material.material'
    _description = 'Material'
    _order = 'code'

    code = fields.Char(string='Material Code', required=True, index=True)
    name = fields.Char(string='Material Name', required=True)
    material_type = fields.Selection(
        selection=MATERIAL_TYPES, string='Material Type', required=True)
    buy_price = fields.Float(string='Material Buy Price', required=True)
    supplier_id = fields.Many2one(
        'material.supplier', string='Related Supplier',
        required=True, ondelete='restrict')

    _sql_constraints = [
        ('code_unique', 'unique(code)', 'Material Code must be unique.'),
    ]

    @api.constrains('buy_price')
    def _check_buy_price(self):
        """Invariant: buy price must not be lower than 100."""
        for material in self:
            if material.buy_price < MIN_BUY_PRICE:
                raise ValidationError(
                    'Material Buy Price cannot be less than %s.' % MIN_BUY_PRICE)
