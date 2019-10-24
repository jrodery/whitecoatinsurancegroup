from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.multi
    def crm_lead_opportunities(self):
        ctx = self._context.copy() or {}
        ctx.update({
            'search_default_partner_id': self.id,
        })
        action = self.env.ref('crm.crm_lead_opportunities').read()[0]
        action['context'] = ctx
        return action
