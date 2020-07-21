# -*- coding: utf-8 -*-
{
    'name': "test",

    'summary': """
        test""",

    'description': """
        test
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",
    'application': True,
    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/12.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/address.xml',
        'views/echarts_templates.xml',
        'views/echarts_views.xml',
        'views/menu.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
