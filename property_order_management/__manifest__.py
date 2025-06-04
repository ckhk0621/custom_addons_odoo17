# -*- coding: utf-8 -*-
{
    'name': "Property Order Management",
    'summary': """
        Property Order Management System for E-Housing""",
    'description': """
        Property Order Management System with the following features:
        - Estate Management
        - Block/Building Management
        - Work Order Management
        - Contractor Management
    """,
    'author': "Your Company",
    'website': "https://www.yourcompany.com",
    'category': 'Services/Property',
    'version': '17.0.1.0.0',
    'depends': [
        'base',
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/property_order_sequence.xml',
        'views/property_order_views.xml',
        'views/property_estate_views.xml',
        'views/property_block_views.xml',
        'views/property_menus.xml',
    ],
    'demo': [],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}