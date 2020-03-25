# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

{
    'name': 'Multi-form Assets',
    'summary': 'JS and CSS assets for multi-forms on website.',
    'author': 'Captivea LLC.',
    'category': 'CRM',
    'version': '1.2',
    'depends': [
        'website_form'
    ],
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/free_disability_quote_template.xml',
        'data/insurance_estimate_template.xml',
        'data/online_application_template.xml',
        'views/assets.xml',
        'views/life_insurance_estimate_form_views.xml',
        'views/web_life_insurance_estimate_form.xml',
        'views/free_quote_form_views.xml',
        'views/web_free_quote_form.xml',
        'views/insurance_data_display.xml',
        'views/online_insurance_application_views.xml',
        'views/web_online_insurance_application_form.xml'
    ],
    'installable': True,
    'application': False,
}
