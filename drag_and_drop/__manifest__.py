# -*- coding: utf-8 -*-
{
    'name': "Drag and Drop",

    'summary': """
        D&D multi-files and screenshot upload
    """,

    'author': "Lennart Duncker",
    'website': "https://www.myodoodev.com",

    'category': 'Tools',
    'version': '1.0',
    'images': ['images/main_screenshot.png'],

    'price': 50.00,
    'currency': 'EUR',
    'license': 'OPL-1',

    # any module necessary for this one to work correctly
    'depends': [
        'base_setup'
    ],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'qweb': [
        'views/chatter.xml',
    ],
    # only loaded in demonstration mode
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True,
}