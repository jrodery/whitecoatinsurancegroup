# -*- coding: utf-8 -*-
# Part of CAPTIVEA. Odoo 12 EE.

from datetime import timedelta, date

from odoo import api, models, fields


class CrmStageLineUpdate(models.TransientModel):
    _name = "crm.stage.line.update"
    _description = "Sent Mail Iteration"

    @api.multi
    def create_lines(self):
        line = self.env['next.mail.iteration'].create
        leads = self.env['crm.lead'].browse(self._context['active_ids'])
        for lead in leads:
            for act in lead.stage_id.mail_act_ids:
                line({
                    'stage_line': act.id or False,
                    'mail_template_id': act.mail_template_id.id or False,
                    'next_date': lead.next_changed_sent_mail_date or False,
                    'lead_id': lead.id or False,
                    'iteration': lead.iteration_scheduler or False
                })
