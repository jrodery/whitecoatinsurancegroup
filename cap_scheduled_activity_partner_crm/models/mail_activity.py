# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, api


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = 'Activity'

    @api.model
    def create(self, values):
        res = super(MailActivity, self).create(values)
        partner_id = False
        if res.res_model == 'crm.lead':
            partner_id = self.env['crm.lead'].browse(res.res_id).partner_id.id
        elif res.res_model == 'res.partner':
            partner_id = res.res_id
        vals = {
            'activity_id': res.id,
            'user_id': res.user_id.id,
            'partner_id': partner_id,
            'name': res.res_name,
            'activity_type_id': res.activity_type_id.id,
            'summary': res.summary,
            'date_deadline': res.date_deadline,
            'state': res.state,
            'res_model': res.res_model,
            'res_id': res.res_id,
            'res_model_id': res.res_model_id.id,
        }
        self.env['mail.activity.log'].create(vals)
        return res

    @api.multi
    def unlink(self):
        for res in self:
            log = self.env['mail.activity.log'].search([
                ('activity_id', '=', res.id)
            ], limit=1)
            if log:
                log.state = 'done'
        return super(MailActivity, self.sudo()).unlink()

    @api.multi
    def write(self, vals):
        res = super(MailActivity, self).write(vals)
        log = self.env['mail.activity.log'].search([
            ('activity_id', '=', self.id)
        ])
        if not log:
            return res
        update_log = {}
        if 'activity_type_id' in vals:
            update_log.update({'activity_type_id': self.activity_type_id.id})
        if 'date_deadline' in vals:
            update_log.update({'date_deadline': self.date_deadline})
        if 'summary' in vals:
            update_log.update({'summary': self.summary})
        if 'user_id' in vals:
            update_log.update({'user_id': self.user_id.id})
        log.write(update_log)
        return res
