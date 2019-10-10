# -*- coding: utf-8 -*-


from odoo import models, api
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT, ustr


class ReportActivity(models.AbstractModel):
    _name = "report.cap_scheduled_activity_partner_crm.report_activity"
    _description = "Report Activity"

    def read_data_activity(self, data):
        details = []
        if not data:
            return details

        res_model = data['model_id']
        activity_type = data['type_id']
        status = data['state']
        start_date = data['start_date']
        end_date = data['end_date']

        mail_act = self.env['mail.activity']
        mail_msg = self.env['mail.message']

        act_domain = []
        msg_domain = []
        mail_msg_details = []
        mail_act_details = []
        # if status in ['done', 'all']:
        #     msg_domain.extend([
        #         ('message_type', '=', 'notification'),
        #         ('subtype_id.name', '=', 'Activities')
        #     ])
        #     if start_date:
        #         msg_domain.append(('date', '>=', start_date))
        #     if end_date:
        #         msg_domain.append(('date', '<=', end_date))
        #     if res_model:
        #         msg_domain.append(('model', '=', self.env['ir.model'].browse(
        #             res_model[0]).model))
        #     if activity_type:
        #         msg_domain.append(
        #             ('mail_activity_type_id', '=', activity_type[0]))
        #     mail_msg_details = mail_msg.search(msg_domain)
        # if status != 'done':
        if status != 'all':
            act_domain.append(('state', '=', status))
        if start_date:
            act_domain.append(('date_deadline', '>=', start_date))
        if end_date:
            act_domain.append(('date_deadline', '<=', end_date))
        if res_model:
            act_domain.append(('res_model_id', '=', res_model[0]))
        if activity_type:
            act_domain.append(('activity_type_id', '=', activity_type[0]))
        mail_act_details = mail_act.search(act_domain)

        for act in mail_act_details:
            details.append({
                'user': act.user_id.name,
                'date_deadline': act.date_deadline.strftime(DEFAULT_SERVER_DATE_FORMAT),
                'activity': act.activity_type_id.name,
                'summary': act.summary,
                'model': act.res_model_id.name,
                'doc_name': act.res_name,
                'status': act.state
            })

        # for msg in mail_msg_details:
        #     details.append({
        #         'user': msg.author_id.name,
        #         'date_deadline': msg.date.strftime(DEFAULT_SERVER_DATE_FORMAT),
        #         'activity': msg.mail_activity_type_id.name,
        #         'summary': msg.body,
        #         'model': self.env['ir.model'].search([(
        #             'model', '=', msg.model)], limit=1).name,
        #         'doc_name': msg.record_name,
        #         'status': 'Done'
        #     })
        return details

    @api.model
    def _get_report_values(self, docids, data=None):
        get_data = self.read_data_activity(data)
        print('\n\n\n', data)
        docargs = {
            'is_model': data['model_id'] or False,
            'is_activity': data['type_id'] or False,
            'is_state': data['state'] or False,
            'start_date': data['start_date'] or False,
            'end_date': data['end_date'] or False,
            'get_data': get_data
        }
        return docargs
