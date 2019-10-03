from odoo.exceptions import UserError
from odoo import api, fields, models, _
import uuid


class MailActivity(models.Model):
    _inherit = 'mail.activity'

    @api.multi
    def default_code(self):
      code = uuid.uuid1()
      while self.env['mail.activity'].search([('group_uuid', '=', code)], limit=1):
        code = uuid.uuid1()
      return code

    group_uuid = fields.Char(string='Group ID', size=48, default=default_code)
    grouped = fields.Boolean()

    # @api.multi
    # def create(self):
    #     code = uuid.uuid1()
    #
    #     while self.env['mail.activity'].search([('group_uuid', '=', code)], limit=1):
    #         code = uuid.uuid1()
    #     self['group_uuid'] = code
    #
    #     if self['grouped']:
    #         users = env['res.users'].search([('id','!=',self['user_id']['id'])])
    #
    #         for user in users:
    #           self.copy({
    #             'user_id': user['id'],
    #             'group_uuid': self['group_uuid'],
    #             'grouped': False
    #           })
    #     return super(MailActivity, self).create()


    # @api.multi
    # def unlink(self):
    #     if self['group_uuid']:
    #         rel_act_ids = self.env['mail.activity'].search([('group_uuid', '=', self['group_uuid'])])
    #         if rel_act_ids:
    #             for rel_act_id in rel_act_ids:
    #                 rel_act_id.unlink()
    #     return super(MailActivity, self).unlink()

    def action_feedback(self, feedback=False):
        message = self.env['mail.message']
        if feedback:
            self.write(dict(feedback=feedback))
        for activity in self:
            record = self.env[activity.res_model].browse(activity.res_id)
            record.message_post_with_view(
                'mail.message_activity_done',
                values={'activity': activity},
                subtype_id=self.env['ir.model.data'].xmlid_to_res_id('mail.mt_activities'),
                mail_activity_type_id=activity.activity_type_id.id,
            )
            message |= record.message_ids[0]

        if self['group_uuid']:
            rel_act_ids = self.env['mail.activity'].search([('group_uuid', '=', self['group_uuid']), ('id','!=', self['id'])])
            if rel_act_ids:
                for rel_act_id in rel_act_ids:
                    rel_act_id.unlink()

        self.unlink()
        return message.ids and message.ids[0] or False
