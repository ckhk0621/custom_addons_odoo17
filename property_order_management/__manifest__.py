# -*- coding: utf-8 -*-
{
    'name': 'Property Management System (Odoo 17)',
    'version': '17.0.1.0.1', # 建議每次有較大修改時增加版本號
    'summary': 'Manage property estates and work orders for Odoo 17.',
    'description': """
Property Management System for Odoo 17
======================================
This module allows managing property estates and related work orders.
    """,
    'author': 'CK Lam',
    'website': 'https://ideastime.ltd',
    'category': 'Services/Property Management',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/property_order_sequence.xml',
        'views/res_partner_views.xml',
        'views/res_partner_views_inherited.xml',
        'views/property_contractor_views.xml',
        'views/property_estate_views.xml',
        'views/property_block_views.xml',
        'views/property_order_views.xml',
        'views/property_menus.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'license': 'LGPL-3',
    'icon': '/property_order_management/static/description/icon.png',
}