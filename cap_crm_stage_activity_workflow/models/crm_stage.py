# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

from odoo import models, fields


class Stage(models.Model):
    _inherit = "crm.stage"

    define_stage_activity = fields.Boolean("Define Activity")
    mail_template_id = fields.Many2one(
        'mail.template', string='Email Template',
        domain=[('model', '=', 'crm.lead')],
        help="If set an email will be sent to the customer when the "
             "Lead/Opportunity reaches this step.")
    activity_user_id = fields.Many2one('res.users', string="Task Sent to")
    activity_type = fields.Many2one('mail.activity.type', string="Activity")
    activity_title = fields.Char(string="Activity Title")
    scheduler_day_interval = fields.Char(string="Scheduler Day Interval")
    res_doc_id = fields.Integer(default=lambda x: x.env['ir.model'].search(
        [('model', '=', 'crm.lead')], limit=1).id)
