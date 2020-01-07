# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

from datetime import timedelta, date

from odoo import api, models, fields


class NextMailIteration(models.Model):
    _name = "next.mail.iteration"
    _description = "Sent Mail Iteration"
    _date = "next_date"

    stage_line = fields.Many2one("stage.mail.activity", string="Line")
    mail_template_id = fields.Many2one(
        'mail.template', string='Email Template',
        domain=[('model', '=', 'crm.lead')])
    next_date = fields.Date(string="Next Mail Send On")
    lead_id = fields.Many2one("crm.lead", string="CRM")
    iteration = fields.Integer(string="Iteration", default=1)


class Lead(models.Model):
    _inherit = "crm.lead"

    stage_changed_date = fields.Date(string="Stage Changed At")
    iteration_scheduler = fields.Integer(string="Scheduler Iteration")
    stage_changed_sent_mail_date = fields.Date(string="Stage Changed Mail At")
    next_changed_sent_mail_date = fields.Date(string="Next Mail Send On")
    dont_send_emails = fields.Boolean(string="Do not send emails")
    next_mail_iteration = fields.One2many("next.mail.iteration", 'lead_id',
                                          string="Next Mail Iteration")

    @api.multi
    def write(self, vals):
        today = date.today()
        if 'stage_id' in vals:
            vals.update({
                'stage_changed_date': today,
                'iteration_scheduler': 1,
                'next_changed_sent_mail_date': False,
            })
            mail_mail = self.env['mail.mail'].search([
                ('model', '=', 'crm.lead'),
                ('res_id', '=', self.id),
                ('message_type', '=', 'email'),
                ('state', '=', 'outgoing')
            ])
            if mail_mail:
                for m in mail_mail:
                    # related_message = self.env['mail.message'].search(
                    # [('message_id','=',m['message_id'])], limit=1)
                    # if related_message:
                    #   related_message.unlink()
                    m.unlink()
            for next_iteration in self.next_mail_iteration:
                next_iteration.unlink()
            stage = self.env['crm.stage'].browse(vals['stage_id'])
            act_obj = self.env['mail.activity'].create
            crm_model_id = self.env['ir.model'].search([
                ('model', '=', 'crm.lead')
            ], limit=1).id
            for line in stage.mail_act_ids:
                if line.define_stage_activity:
                    act_obj({
                        'user_id': line.activity_user_id.id,
                        'summary': line.activity_title,
                        'activity_type_id': line.activity_type.id,
                        'date_deadline': today + timedelta(line.due_date),
                        'state': 'today' if line.due_date == 0 else 'planned',
                        'res_model': self._name,
                        'res_id': self.id,
                        'res_model_id': crm_model_id,
                    })
                if not self.dont_send_emails and line.mail_template_id:
                    interval_day = []
                    if line.scheduler_day_interval:
                        interval_day = [
                            int(day) for day in line.scheduler_day_interval.split(
                                ',')]
                    if not line.immediate_mail and interval_day:
                        next_date = today + timedelta(days=interval_day[0])
                        self.create_mail_for_next(
                            line.id, line.mail_template_id, next_date)
                    else:
                        if line.immediate_mail:
                            line.mail_template_id.send_mail(
                                self.id, force_send=True)
                        if line.immediate_mail and len(interval_day) > 0:
                            next_date = today + timedelta(
                                days=interval_day[0])
                            self.create_mail_for_next(
                                line.id, line.mail_template_id, next_date)
        return super(Lead, self).write(vals)

    def create_mail_for_next(self, line, template_id, next_date):
        template_id.scheduled_date = next_date
        template_id.send_mail(self.id, force_send=False)
        template_id.scheduled_date = False
        self.env['next.mail.iteration'].create({
            'stage_line': line,
            'mail_template_id': template_id.id,
            'next_date': next_date,
            'lead_id': self.id
        })

    @api.multi
    def send_mail_stage_change_activity(self):
        today = date.today()
        lines = self.env['next.mail.iteration'].search([
            ('next_date', '=', today)
        ])
        for line in lines:
            if line.lead_id.dont_send_emails or not line.stage_line.scheduler_day_interval:
                continue
            interval = line.stage_line.scheduler_day_interval.split(",")
            iteration = line.iteration
            if iteration < len(interval):
                next_date = line.next_date + timedelta(days=int(
                    interval[iteration]))
                line.mail_template_id.scheduled_date = next_date
                line.mail_template_id.send_mail(
                    line.lead_id.id, force_send=False)
                line.mail_template_id.scheduled_date = False
                iteration += 1
                line.write({
                    'next_date': next_date,
                    'iteration': iteration
                })
                line.lead_id.write({
                    'iteration_scheduler': iteration,
                    'stage_changed_sent_mail_date': today,
                    'next_changed_sent_mail_date': next_date
                })
            else:
                line.unlink()
