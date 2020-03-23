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
            res.sudo().write(kw.get('input_args'))
            amount = res.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
        else:
            vals['create'] = True
            res = form_object.sudo().create(kw.get('input_args', {}))
            amount = res.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
            vals['res_id'] = res.id
            vals['ref_code'] = res.ref_code
        return vals

    # Set as done and send mail
    @http.route('/insurance/estimate-form-done', type='json',
                auth="public", methods=['POST'])
    def estimate_form_done(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'write': False, 'res_id': False, 'total_insurance': 0.0}
        if kw.get('rec_id'):
            form_obj = form_object.browse(int(kw.get('rec_id')))
            vals['write'] = form_obj.sudo().write({
                'state': 'done'
            })
            amount = form_obj.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
        return vals

    @http.route('/insurance/freequote-form', type='json',
                auth="public", methods=['POST'])
    def freequote_form(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'create': False, 'res_id': False}
        if kw.get('rec_id'):
            res = form_object.browse(int(kw.get('rec_id')))
            res.sudo().write(kw.get('input_args'))
        else:
            vals['create'] = True
            vals['res_id'] = form_object.sudo().create(kw.get('input_args', {})).id
        return vals

    # Set as done and send mail
    @http.route('/insurance/freequote-form-done', type='json',
                auth="public", methods=['POST'])
    def freequote_form_done(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'write': False, 'res_id': False}
        if kw.get('rec_id'):
            form_obj = form_object.browse(int(kw.get('rec_id')))
            vals['write'] = form_obj.sudo().write({
                'state': 'done'
            })
        return vals

    # Life Insurance Data
    @http.route('/life/insurance-done', type='http', auth="public",
                methods=['POST', 'GET'], csrf=False, website=True)
    def insurance_done(self, **kw):
        res = request.env['life.insurance.estimate'].browse(
            int(kw.get('rec_id'))
        )
        return request.render(
            'cap_web_free_quote.life_insurance_data_display_template',
            {"insurance_data": res}
        )

    @http.route('/insurance/insurance-application', type='json',
                auth="public", methods=['POST'])
    def insurance_application(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'create': False, 'res_id': False}
        if kw.get('rec_id'):
            res = form_object.browse(int(kw.get('rec_id')))
            res.write(kw.get('input_args'))
        else:
            vals['create'] = True
            vals['res_id'] = form_object.create(kw.get('input_args', {})).id
        return vals

    @http.route('/insurance/insurance-application-done', type='json',
                auth="public", methods=['POST'])
    def insurance_application_done(self, **kw):
        form_object = request.env[kw['store_data_model']]
        vals = {'write': False, 'res_id': False}
        if kw.get('rec_id'):
            form_obj = form_object.browse(int(kw.get('rec_id')))
            vals['write'] = form_obj.sudo().write({
                'state': 'done'
            })
        return vals

    @http.route('/life/insurance-done', type='http', auth="public",
                methods=['POST', 'GET'], csrf=False, website=True)
    def insurance_done(self, **kw):
        res = request.env['life.insurance.estimate'].search([
            ('ref_code', '=', kw.get('reference'))
        ], limit=1)

        currency_id = request.env['res.company'].browse(1).currency_id
        return request.render(
            'cap_web_free_quote.life_insurance_data_display_template',
            {
                "insurance_data": res,
                "currency_id": currency_id
            }
        )

    @http.route('/thankyou/request_quote', type='json', auth="public",
                methods=['POST', 'GET'], csrf=False, website=True)
    def request_quote(self, **kw):
        res = request.env['life.insurance.estimate'].search([
            ('ref_code', '=', kw.get('reference')),
        ], limit=1)
        kw.update({'state': 'requested_quote'})
        return {
            'thank_you_request_quote': res.sudo().write(kw)
        }

    @http.route('/thankyou/request_quote', type='http', auth="public",
                methods=['POST', 'GET'], csrf=False, website=True)
    def redirect_ty_page(self, **kw):
        return request.redirect("/thank-you-page-life-calculator")
