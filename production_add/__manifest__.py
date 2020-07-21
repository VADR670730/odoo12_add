# -*- coding: utf-8 -*-
{
    'name': "production_add",

    'summary': """
        production_add""",

    'description': """
        production_add
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
    'depends': ['base', 'mrp', 'stock_add'],

    # always loaded
    'data': [
        'views/mrp_production_views.xml',
        'views/mrp_workorder_views.xml',
    ]
}
