# -*- coding: utf-8 -*-
from odoo import models
from odoo.exceptions import UserError, ValidationError

from .material import MATERIAL_TYPES

_VALID_TYPES = {key for key, _ in MATERIAL_TYPES}


class MaterialService(models.AbstractModel):
    """Application layer: material use-cases.

    One place for the operations the client needs (list/filter, create,
    read, update, delete). Both the REST controller and the tests call
    these methods, so the rules live here once instead of being copied
    into every caller (SRP + DRY).
    """
    _name = 'material.service'
    _description = 'Material Use Cases'

    # --- serialization -----------------------------------------------------
    def serialize(self, material):
        """Turn a material record into a plain dict for the API."""
        return {
            'id': material.id,
            'code': material.code,
            'name': material.name,
            'material_type': material.material_type,
            'buy_price': material.buy_price,
            'supplier_id': material.supplier_id.id,
            'supplier_name': material.supplier_id.name,
        }

    # --- use cases ---------------------------------------------------------
    def list_materials(self, material_type=None):
        """Return all materials, optionally filtered by material type."""
        domain = []
        if material_type:
            if material_type not in _VALID_TYPES:
                raise UserError('Unknown material type: %s' % material_type)
            domain.append(('material_type', '=', material_type))
        materials = self.env['material.material'].search(domain)
        return [self.serialize(m) for m in materials]

    def get_material(self, material_id):
        material = self._get_or_raise(material_id)
        return self.serialize(material)

    def create_material(self, values):
        material = self.env['material.material'].create(self._clean(values))
        return self.serialize(material)

    def update_material(self, material_id, values):
        material = self._get_or_raise(material_id)
        material.write(self._clean(values))
        return self.serialize(material)

    def delete_material(self, material_id):
        material = self._get_or_raise(material_id)
        material.unlink()
        return True

    # --- helpers -----------------------------------------------------------
    def _get_or_raise(self, material_id):
        material = self.env['material.material'].browse(int(material_id)).exists()
        if not material:
            raise UserError('Material %s not found.' % material_id)
        return material

    def _clean(self, values):
        """Keep only writable material fields from an untrusted payload."""
        allowed = {'code', 'name', 'material_type', 'buy_price', 'supplier_id'}
        cleaned = {k: v for k, v in (values or {}).items() if k in allowed}
        if not cleaned:
            raise ValidationError('No valid material fields provided.')
        return cleaned
