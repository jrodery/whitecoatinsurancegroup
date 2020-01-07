# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

{
    'name': 'CRM Scheduled Activity Workflow',
    'summary': 'Define activity For CRM',
    'description': 'Activity will be created when stage has changed, mail will be sent as per stage configuration.',
    'category': 'CRM',
    'version': '1.2',
    'depends': [
        'crm'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/scheduler.xml',
        'views/assets.xml',
        'views/crm_lead_views.xml',
        'views/crm_stage_views.xml',
        'views/res_partner.xml',
        'wizards/crm_stage_line_update.xml',
    ],
    'installable': True,
    'application': False,
}
