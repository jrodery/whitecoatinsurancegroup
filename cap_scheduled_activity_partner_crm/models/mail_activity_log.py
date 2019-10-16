# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, fields, api


class MailActivityLog(models.Model):
    _name = "mail.activity.log"
    _description = 'Mail Activity Log'

    name = fields.Char('Document Name')
    activity_type_id = fields.Many2one('mail.activity.type', 'Activity')
    summary = fields.Char('Summary')
    date_deadline = fields.Date('Due Date')
    state = fields.Selection([
        ('planned', 'Planned'),
        ('today', 'Today'),
        ('overdue', 'Overdue'),
        ('done', 'Done'),
    ], 'State')
    res_model = fields.Char('Related Document Model')
    res_id = fields.Integer('Related Document ID')
    res_model_id = fields.Many2one('ir.model', 'Document Model')
    activity_id = fields.Many2one('mail.activity')
    user_id = fields.Many2one("res.users", string="User")
    partner_id = fields.Many2one("res.partner", string="Partner")

    @api.multi
    def action_redirect_to_record(self):
        view_id = self.env.ref(
            'crm.crm_case_form_view_oppor'
        ) if self.res_model == 'crm.lead' else self.env.ref(
            'base.view_partner_form')
        return {
            'res_model': self.res_model,
            'res_id': self.res_id,
            'view_id': view_id.id,
            'views': [(view_id.id, 'form')],
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'current'
        }
