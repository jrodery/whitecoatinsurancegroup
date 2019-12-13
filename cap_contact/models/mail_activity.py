# -*- coding: utf-8 -*-
# © 2016 Serpent Consulting Services Pvt. Ltd. (support@serpentcs.com)
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from dateutil.relativedelta import relativedelta

class MailActivity(models.Model):
    _inherit = "mail.activity"

    @api.multi
    def action_view_partner(self):
        if self.res_model == 'res.partner':
            return {
                    'res_model':'res.partner',
                    'res_id':self.res_id,
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref('base.view_partner_form').id,
                    'target':'current',
                }
        if self.res_model == 'crm.lead':
            lead_id = self.env['crm.lead'].browse(self.res_id)
            return {
                    'res_model':'res.partner',
                    'res_id': lead_id.partner_id.id,
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref('base.view_partner_form').id,
                    'target':'current',
                }
        return True

    @api.multi
    def action_view_case(self):
        if self.res_model == 'crm.lead':
            lead_id = self.env['crm.lead'].browse(self.res_id)
            return {
                    'res_model':'crm.lead',
                    'res_id': lead_id.id,
                    'type': 'ir.actions.act_window',
                    'view_type': 'form',
                    'view_mode': 'form',
                    'view_id': self.env.ref('crm.crm_case_form_view_oppor').id,
                    'target':'current',
                }
        return True

    @api.multi
    def action_show_partner_cases(self):
        if self.res_model == 'res.partner':
            action = self.env.ref('crm.crm_lead_opportunities').read()[0]
            partner = self.env['res.partner'].browse(self.res_id)
            action['domain'] = [('id', 'in', partner.lead_ids.ids), ('type', '=', 'opportunity')]
            return action
        if self.res_model == 'crm.lead':
            lead_id = self.env['crm.lead'].browse(self.res_id)
            action = self.env.ref('crm.crm_lead_opportunities').read()[0]
            action['domain'] = [('id', 'in', lead_id.partner_id.lead_ids.ids), ('type', '=', 'opportunity')]
            return action
