# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

from datetime import timedelta, date

from odoo import api, models, fields


class Lead(models.Model):
    _inherit = "crm.lead"

    stage_changed_date = fields.Date(string="Stage Changed At")
    iteration_scheduler = fields.Integer(string="Scheduler Iteration")
    stage_changed_sent_mail_date = fields.Date(string="Stage Changed Mail At")
    next_changed_sent_mail_date = fields.Date(string="Next Mail Send On")
    dont_send_emails = fields.Boolean(string="Do not send emails")

    @api.multi
    def write(self, vals):
        today = date.today()
        stage = False
        if 'stage_id' in vals:
            vals.update({
                'stage_changed_date': today,
                'iteration_scheduler': 0,
                'next_changed_sent_mail_date': False,
            })
            immediate_mail = False
            mail_mail = self.env['mail.mail'].search([
                ('model', '=', 'crm.lead'),
                ('res_id', '=', self.id),
                ('message_type', '=', 'email'),
                ('state', '=', 'outgoing')
            ])
            if mail_mail:
                for m in mail_mail:
                    m.unlink()
            stage = self.env['crm.stage'].browse(vals['stage_id'])
            interval_day = []
            if stage.mail_template_id and stage.scheduler_day_interval:
                interval_day = stage.scheduler_day_interval.split(',')
            if interval_day:
                day = int(interval_day[0])
                iteration_scheduler = 1
                if day == 0:
                    immediate_mail = True
                if day == 0 and len(interval_day) > 1:
                    day = int(interval_day[1])
                    iteration_scheduler += 1
                next_date = today + timedelta(days=day)
                vals.update({
                    'iteration_scheduler': iteration_scheduler,
                })
                if not self.dont_send_emails:
                    if immediate_mail:
                        stage.mail_template_id.send_mail(
                            self.id, force_send=True)
                    if day != 0 or len(interval_day) > 1:
                        vals.update({
                            'next_changed_sent_mail_date': next_date,
                        })
                        stage.mail_template_id.scheduled_date = next_date
                        stage.mail_template_id.send_mail(
                            self.id, force_send=False)
                        stage.mail_template_id.scheduled_date = False
        res = super(Lead, self).write(vals)
        if stage:
            if stage.define_stage_activity:
                vals = {
                    'user_id': stage.activity_user_id.id,
                    'summary': stage.activity_title,
                    'activity_type_id': stage.activity_type.id,
                    'date_deadline': today + timedelta(stage.due_date),
                    'state': 'today' if stage.due_date == 0 else 'planned',
                    'res_model': self._name,
                    'res_id': self.id,
                    'res_model_id': self.env['ir.model'].search([
                        ('model', '=', 'crm.lead')
                    ], limit=1).id,
                }
                self.env['mail.activity'].create(vals)
        return res

    @api.multi
    def send_mail_stage_change_activity(self):
        today = date.today()
        leads = self.env['crm.lead'].search([
            ('next_changed_sent_mail_date', '=', today)
        ])
        for lead in leads:
            if lead.dont_send_emails or not lead.stage_id.mail_template_id:
                continue
            int_days = [int(x) for x in lead.stage_id.scheduler_day_interval.split(',')]
            iteration = lead.iteration_scheduler
            iteration = iteration + 1 if iteration < len(int_days) else iteration
            if iteration > lead.iteration_scheduler:
                next_date = today if int_days[lead.iteration_scheduler] == 0 else today + timedelta(
                    days=int_days[lead.iteration_scheduler])
                lead.stage_id.mail_template_id.scheduled_date = next_date
                lead.stage_id.mail_template_id.send_mail(lead.id, force_send=False)
                lead.stage_id.mail_template_id.scheduled_date = False
                lead.write({
                    'iteration_scheduler': iteration,
                    'stage_changed_sent_mail_date': today,
                    'next_changed_sent_mail_date': next_date
                })
