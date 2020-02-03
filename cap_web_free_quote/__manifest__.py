# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

{
    'name': 'Multi-form Assets',
    'summary': 'JS and CSS assets for multi-forms on website.',
    'author': 'Captivea LLC.',
    'category': 'CRM',
    'version': '1.0',
    'depends': [
        'website_form'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        # 'views/web_free_quote_form.xml',
        'views/life_insurance_estimate_form_views.xml',
        'views/web_life_insurance_estimate_form.xml'
    ],
    'installable': True,
    'application': False,
}
