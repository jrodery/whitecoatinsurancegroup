# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, api


class MailActivity(models.Model):
    _inherit = 'mail.activity'
    _description = 'Activity'

    @api.model
    def create(self, values):
        res = super(MailActivity, self).create(values)
        partner_id = self.env['crm.lead'].browse(res.res_id)
        vals = {
            'activity_id': res.id,
            'user_id': res.user_id.id,
            'partner_id': partner_id and partner_id.partner_id.id or False,
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
