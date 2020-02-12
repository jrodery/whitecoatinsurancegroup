# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

import json
from collections import OrderedDict

from odoo.exceptions import ValidationError
from odoo.http import request
from psycopg2 import IntegrityError

from odoo import http
from odoo.addons.website_form.controllers.main import WebsiteForm


class FreeQuoteWebsiteForm(WebsiteForm):

    # Check and insert values from the form on the model <model>
    @http.route('/website_form/<string:model_name>', type='http',
                auth="public", methods=['POST'], website=True)
    def website_form(self, model_name, **kwargs):
        model_record = request.env['ir.model'].sudo().search(
            [('model', '=', model_name), ('website_form_access', '=', True)])
        if not model_record:
            return json.dumps(False)
        try:
            values = request.params.copy()
            if 'freequote' in values:
                del values['freequote']
                values = OrderedDict([(
                    '<span style="line-height: 1 !important;">%s</span>' % x,
                    '<span style="color: #1aa3ff; line-height: 1 !important; display: block;">%s</span>' % values[x]
                ) for x in values.keys() if x not in ['email_to', 'subject']] + [
                                         ('email_to', values['email_to']),
                                         ('subject', values['subject'])])
            data = self.extract_data(model_record, values)
        # If we encounter an issue while extracting data
        except ValidationError as e:
            # I couldn't find a cleaner way to pass data to an exception
            return json.dumps({'error_fields': e.args[0]})
        try:
            id_record = self.insert_record(
                request, model_record, data['record'],
                data['custom'], data.get('meta'))
            if id_record:
                self.insert_attachment(model_record, id_record,
                                       data['attachments'])
        # Some fields have additional SQL constraints
        # that we can't check generically
        # Ex: crm.lead.probability which is a float between 0 and 1
        # TODO: How to get the name of the erroneous field ?
        except IntegrityError:
            return json.dumps(False)
        request.session['form_builder_model_model'] = model_record.model
        request.session['form_builder_model'] = model_record.name
        request.session['form_builder_id'] = id_record
        return json.dumps({'id': id_record})

    # Check and insert values from the form on the model <model>
    @http.route('/insurance/estimate-form', type='json',
                auth="public", methods=['POST'])
    def estimate_form(self, **kw):
        estimate_form_obj = request.env['life.insurance.estimate']
        vals = {'create': False, 'res_id': False, 'total_insurance': 0.0}
        if kw.get('rec_id'):
            res = estimate_form_obj.browse(int(kw.get('rec_id')))
            res.write(kw.get('input_args'))
            amount = res.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
        else:
            vals['create'] = True
            res = estimate_form_obj.create(kw.get('input_args', {}))
            amount = res.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
            vals['res_id'] = res.id
        return vals

    # Set as done and send mail
    @http.route('/insurance/estimate-form-done', type='json',
                auth="public", methods=['POST'])
    def estimate_form_done(self, **kw):
        estimate_form_obj = request.env['life.insurance.estimate']
        vals = {'write': False, 'res_id': False, 'total_insurance': 0.0}
        if kw.get('rec_id'):
            form_obj = estimate_form_obj.browse(int(kw.get('rec_id')))
            vals['write'] = form_obj.write({
                'state': 'done'
            })
            amount = form_obj.total_insurance
            vals['total_insurance'] = amount if amount > 0 else 0.0
        return vals
