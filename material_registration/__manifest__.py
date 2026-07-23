# -*- coding: utf-8 -*-
{
    'name': 'Material Registration',
    'version': '14.0.1.0.0',
    'summary': 'Register materials to be sold, with REST API access',
    'description': """
Material Registration
=====================
Manage materials (code, name, type, buy price, supplier) with:
- Selection material type: Fabric, Jeans, Cotton
- Buy price constraint (must be >= 100)
- Backend views (list / filter by type / update / delete)
- REST API (JSON) for list-with-filter, create, read, update, delete
""",
    'author': 'Bryan Wahyu',
    'category': 'Inventory',
    'license': 'LGPL-3',
    'depends': ['base'],
    'data': [
        'security/ir.model.access.csv',
        'views/material_supplier_views.xml',
        'views/material_views.xml',
    ],
    'demo': [
        'data/material_supplier_demo.xml',
    ],
    'installable': True,
    'application': True,
}
