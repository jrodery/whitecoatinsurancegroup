from odoo import api, fields, models, _
from odoo.exceptions import UserError
import datetime

class MailOpportunity(models.Model):
    _inherit = "crm.lead"

    def quote_comparison_email(self):
        mail_template = self.env['mail.template'].sudo().search([('id','=','21')], limit=1)

        if mail_template:
            body = mail_template.body_html
            body = body.replace('${object.partner_id.name}',self.partner_id.name)
            body = body.replace('${object.x_studio_quote_comparison_link}',self.x_studio_quote_comparison_link)
            mail_values = {
                'subject': mail_template.subject,
                'body_html': body,
                'email_to': self.partner_id.email,
                # 'email_from': "info@whitecoatinsurancegroup.com",
            }
            create_and_send_email = self.env['mail.mail'].create(mail_values).send()

            self.env['mail.message'].create({
              'author_id': self.user_id.id,
              'body': "[" + str(datetime.datetime.now()) + "] Quotations sent by email",
              'description': "Quotes Comparison",
              'message_type' : 'comment',
              'subtype_id': 2,
              'res_id' : self.id,
              'model' : 'crm.lead',
              'x_do_not_duplicate' : 1
            })
