# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

import json
from collections import OrderedDict

from odoo.exceptions import ValidationError
from odoo.http import request
from psycopg2 import IntegrityError

from odoo import http
from odoo.addons.website_form.controllers.main import WebsiteForm


class WebsiteForm(WebsiteForm):

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
                ) for x in values.keys() if x != 'email_to'] + [
                                         ('email_to', values['email_to'])])
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
