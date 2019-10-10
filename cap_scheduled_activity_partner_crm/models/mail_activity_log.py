# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE


from odoo import models, fields


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
