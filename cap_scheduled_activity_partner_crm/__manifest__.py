# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': "Scheduled Activity Report",
    'summary': 'Report on activity',
    'description': "User can get details for different activity for different Apps",
    'category': 'Report',
    'version': '1.0',
    'depends': [
        'mail'
    ],
    'data': [
        'security/ir.model.access.csv',
        'report/report_menu.xml',
        'report/report_activity.xml',
        'wizards/activity_report_wiz_view.xml',
        'views/mail_activity_log.xml',
        'views/view_res_partner.xml',
    ],
    'installable': True,
    'application': False,
}
