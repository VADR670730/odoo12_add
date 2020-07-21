# -*- coding: utf-8 -*-
{
    'name': "stock_add",

    'summary': """
        stock_add""",

    'description': """
        stock_add
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    # 'application': True,
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'module_add',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'stock', 'product_add'],

    # always loaded
    'data': [
        'views/stock_picking_views.xml',
        'wizards/stock_lot_wizard_views.xml',
        'wizards/stock_move_wizard_views.xml',
    ]
}
