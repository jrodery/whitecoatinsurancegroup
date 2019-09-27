from odoo import api, fields, models, _
from odoo.exceptions import UserError

class MailOpportunity(models.Model):
    _inherit = "crm.lead"

    def quote_comparison_email(self):
      mail_template = self.env['mail.template'].sudo().search([('id','=','21')], limit=1)

      body = mail_template.body_html
      body=body.replace('${object.partner_id.name}',self.partner_id.name)    
      body=body.replace('${object.x_studio_quote_comparison_link}',self.x_studio_quote_comparison_link)   
    
      if mail_template:
       mail_values = {
        'subject': mail_template.subject,
        'body_html': body,
        'email_to': self.partner_id.email,
        'email_from': self.user_id.email,
       }
       create_and_send_email = self.env['mail.mail'].create(mail_values).send()
