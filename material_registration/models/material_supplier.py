# -*- coding: utf-8 -*-
from odoo import api, fields, models


class MaterialSupplier(models.Model):
    """Domain entity: a supplier that materials can be related to.

    Kept as a dedicated model (instead of reusing res.partner) so the
    module is self-contained and the ERD relation stays explicit.
    """
    _name = 'material.supplier'
    _description = 'Material Supplier'
    _order = 'name'

    name = fields.Char(string='Supplier Name', required=True)
    material_ids = fields.One2many(
        'material.material', 'supplier_id', string='Materials')
    material_count = fields.Integer(
        string='Material Count', compute='_compute_material_count')

    @api.depends('material_ids')
    def _compute_material_count(self):
        for supplier in self:
            supplier.material_count = len(supplier.material_ids)
