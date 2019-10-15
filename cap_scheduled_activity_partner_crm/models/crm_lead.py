# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, api, fields


class Lead(models.Model):
    _inherit = 'crm.lead'

    crm_partner_activity_count = fields.Integer(
        string="Activities", compute='_compute_crm_parnter_activity_count')

    @api.multi
    def _compute_crm_parnter_activity_count(self):
        for res in self:
            res.crm_partner_activity_count = self.env['mail.activity.log'].search_count([
                ('partner_id', '=', res.partner_id.id),
            ])

    @api.multi
    def crm_partner_activity_log_details(self):
        ctx = self._context.copy() or {}
        ctx.update({
            'search_default_partner_id': self.partner_id.id,
        })
        action = self.env.ref(
            'cap_scheduled_activity_partner_crm.mail_activity_log_action'
        ).read()[0]
        action['context'] = ctx
        return action
