# -*- coding: utf-8 -*-
import json
import logging

from odoo import http
from odoo.http import request
from odoo.exceptions import UserError, ValidationError

_logger = logging.getLogger(__name__)


def _json_response(payload, status=200):
    return request.make_response(
        json.dumps(payload),
        headers=[('Content-Type', 'application/json')],
        status=status,
    )


def _read_body():
    raw = request.httprequest.get_data()
    if not raw:
        return {}
    try:
        return json.loads(raw)
    except ValueError:
        raise ValidationError('Request body is not valid JSON.')


def _handle(func):
    """Run a use-case call and map domain errors to HTTP status codes.

    Keeps every route body free of try/except boilerplate (SRP: the
    controller only translates HTTP <-> use case, nothing else).
    """
    try:
        return _json_response({'success': True, 'data': func()})
    except ValidationError as err:
        return _json_response({'success': False, 'error': str(err)}, status=400)
    except UserError as err:
        return _json_response({'success': False, 'error': str(err)}, status=404)
    except Exception as err:  # pragma: no cover - safety net
        _logger.exception('Unhandled error in material API')
        return _json_response({'success': False, 'error': str(err)}, status=500)


class MaterialController(http.Controller):
    """HTTP adapter. Holds no business logic; forwards to material.service."""

    def _service(self):
        return request.env['material.service']

    @http.route('/api/materials', type='http', auth='user',
                methods=['GET'], csrf=False)
    def list_materials(self, material_type=None, **kwargs):
        return _handle(
            lambda: self._service().list_materials(material_type=material_type))

    @http.route('/api/materials', type='http', auth='user',
                methods=['POST'], csrf=False)
    def create_material(self, **kwargs):
        body = _read_body()
        return _handle(lambda: self._service().create_material(body))

    @http.route('/api/materials/<int:material_id>', type='http', auth='user',
                methods=['GET'], csrf=False)
    def get_material(self, material_id, **kwargs):
        return _handle(lambda: self._service().get_material(material_id))

    @http.route('/api/materials/<int:material_id>', type='http', auth='user',
                methods=['PUT'], csrf=False)
    def update_material(self, material_id, **kwargs):
        body = _read_body()
        return _handle(
            lambda: self._service().update_material(material_id, body))

    @http.route('/api/materials/<int:material_id>', type='http', auth='user',
                methods=['DELETE'], csrf=False)
    def delete_material(self, material_id, **kwargs):
        return _handle(lambda: self._service().delete_material(material_id))
