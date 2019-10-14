# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

{
    'name': 'CRM Grant Portal',
    'summary': 'Portal access to the crm customer.',
    'description': 'To create user as portal user for CRM Lead/Opportunity',
    'category': 'CRM',
    'version': '1.0',
    'depends': [
        'crm',
        'portal'
    ],
    'data': [
        'data/portal_data.xml',
        'wizards/portal_wizard_view.xml',
    ],
    'installable': True,
    'application': False,
}
