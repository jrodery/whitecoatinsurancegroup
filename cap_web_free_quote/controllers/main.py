# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

from odoo.http import request

from odoo import http
from odoo.addons.website_form.controllers.main import WebsiteForm


class FreeQuoteWebsiteForm(WebsiteForm):
    # Check and insert values from the form on the model <model>
    @http.route('/insurance/estimate-form', type='json',
                auth="public", methods=['POST'])
    def estimate_form(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'create': False, 'res_id': False, 'total_insurance': 0.0}
        if kw.get('rec_id'):
            res = form_object.browse(int(kw.get('rec_id')))
            res.write(kw.get('input_args'))
            amount = res.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
        else:
            vals['create'] = True
            res = form_object.create(kw.get('input_args', {}))
            amount = res.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
            vals['res_id'] = res.id
        return vals

    # Set as done and send mail
    @http.route('/insurance/estimate-form-done', type='json',
                auth="public", methods=['POST'])
    def estimate_form_done(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'write': False, 'res_id': False, 'total_insurance': 0.0}
        if kw.get('rec_id'):
            form_obj = form_object.browse(int(kw.get('rec_id')))
            vals['write'] = form_obj.write({
                'state': 'done'
            })
            amount = form_obj.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
        return vals

    @http.route('/insurance/freequote-form', type='json',
                auth="public", methods=['POST'])
    def freequote_form(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'create': False, 'res_id': False, 'total_insurance': 0.0}
        if kw.get('rec_id'):
            res = form_object.browse(int(kw.get('rec_id')))
            res.write(kw.get('input_args'))
        else:
            vals['create'] = True
            vals['res_id'] = form_object.create(kw.get('input_args', {})).id
        return vals

    # Set as done and send mail
    @http.route('/insurance/freequote-form-done', type='json',
                auth="public", methods=['POST'])
    def freequote_form_done(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'write': False, 'res_id': False}
        if kw.get('rec_id'):
            form_obj = form_object.browse(int(kw.get('rec_id')))
            vals['write'] = form_obj.write({
                'state': 'done'
            })
        return vals
