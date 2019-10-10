# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo.exceptions import ValidationError

from odoo import models, fields, api, _


class ActivityPeportWiz(models.TransientModel):
    _name = 'activity.report.wiz'
    _description = 'Wizard Activity Report'

    model_id = fields.Many2one('ir.model', string="Model",
                               domain=[('transient', '=', False)])
    type_id = fields.Many2one("mail.activity.type", string="Type")
    state = fields.Selection([
        ('all', 'All'),
        ('planned', 'Planned'), ('today', 'Today'),
        ('overdue', 'Overdue'), ('Done', 'Done'),
    ], string="Status", default="all")
    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    @api.multi
    def print_report(self):
        start_date = fields.Date.from_string(self.start_date)
        end_date = fields.Date.from_string(self.end_date)
        if start_date and end_date and start_date > end_date:
            raise ValidationError(
                _("End Date cannot be set before Start Date."))
        else:
            data = self.read([
                'model_id', 'type_id', 'state', 'start_date', 'end_date'
            ])[0]
            report = self.env.ref(
                'cap_scheduled_activity_partner_crm.action_report_activity'
            )
            return report.report_action(self, data=data)
