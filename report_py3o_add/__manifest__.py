# -*- coding: utf-8 -*-
{
    'name': "report_add",

    'summary': """
        report_add""",

    'description': """
        report_add
    """,

    'author': "YJL",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'stock',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'report_py3o', 'stock_add'],

    # always loaded
    'data': [
        'report/stock_report.xml',
        'views/stock_picking_views.xml',
    ],
    # only loaded in demonstration mode
}
