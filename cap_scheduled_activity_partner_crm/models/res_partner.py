# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE

from odoo import models, api, fields


class ResPartner(models.Model):
    _inherit = 'res.partner'

    crm_activity_count = fields.Integer(string="Activities",
                                        compute='_compute_crm_activity_count')

    @api.multi
    def _compute_crm_activity_count(self):
        for res in self:
            res.crm_activity_count = self.env['mail.activity.log'].search_count([
                ('res_model', '=', 'crm.lead'),
                ('partner_id', '=', res.id),
                ('activity_id', '!=', False)
            ])

    @api.multi
    def crm_activity_log_details(self):
        ctx = self._context.copy() or {}
        ctx.update({
            'search_default_partner_id': self.id,
            'search_default_res_model': 'crm.lead'
        })
        action = self.env.ref(
            'cap_scheduled_activity_partner_crm.mail_activity_log_action'
        ).read()[0]
        action['context'] = ctx
        action['domain'] = [('state', '!=', 'done')]
        return action
