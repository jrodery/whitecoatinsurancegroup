# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

from odoo import models, fields


class StageMailActivity(models.Model):
    _name = "stage.mail.activity"
    _description = "CRM Stage Mail and Activity"
    _order = "sequence"

    sequence = fields.Integer("Sequence", required=True)
    define_stage_activity = fields.Boolean("Define Activity")
    due_date = fields.Integer(string="Due Date")
    activity_user_id = fields.Many2one('res.users', string="Task Sent to")
    activity_type = fields.Many2one('mail.activity.type', string="Activity")
    activity_title = fields.Char(string="Activity Title")
    mail_template_id = fields.Many2one(
        'mail.template', string='Email Template',
        domain=[('model', '=', 'crm.lead')],
        help="If set an email will be sent to the customer when the "
             "Lead/Opportunity reaches this step.")
    scheduler_day_interval = fields.Char(string="Scheduler Day Interval")
    immediate_mail = fields.Boolean("Immediate mail")
    stage_id = fields.Many2one('crm.stage', string="Stage")


class Stage(models.Model):
    _inherit = "crm.stage"

    define_stage_activity = fields.Boolean("Define Activity")
    due_date = fields.Integer(string="Due Date")
    activity_user_id = fields.Many2one('res.users', string="Task Sent to")
    activity_type = fields.Many2one('mail.activity.type', string="Activity")
    activity_title = fields.Char(string="Activity Title")
    mail_template_id = fields.Many2one(
        'mail.template', string='Email Template',
        domain=[('model', '=', 'crm.lead')],
        help="If set an email will be sent to the customer when the "
             "Lead/Opportunity reaches this step.")
    scheduler_day_interval = fields.Char(string="Scheduler Day Interval")
    mail_act_ids = fields.One2many("stage.mail.activity", "stage_id",
                                   string="Mail/Activity")
