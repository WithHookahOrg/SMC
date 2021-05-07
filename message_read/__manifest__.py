# -*- coding: utf-8 -*-
{
    'name': "Read Receipt",

    'summary': """
       The purpose of this module is to track the message and email send from chatter. an icon will be shown if recipient has open the message or not.""",

    'description': """
        The purpose of this module is to track the message and email send from chatter. an icon will be shown if recipient has open the message or not
    """,

    'author': "ticinoWEB",
    'website': "https://ticinoweb.tech",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'mail',
    'version': '14.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'mail', 'contacts'],
    'license': "AGPL-3",

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'static/src/xml/thread.xml',
    ],
    'images': ['static/description/icon.png'],
    "price": 100,
    "currency": "EUR",
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
