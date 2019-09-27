import datetime
import base64

from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request
from odoo.addons.portal.controllers.portal import CustomerPortal

class CustomerPortal(CustomerPortal):

    

    @http.route(['/my/opportunity/<int:opportunity>'], type='http', auth="user", website=True)
    def opportunity_page(self, opportunity=None):
        opportunity = request.env['crm.lead'].browse([opportunity])
        
        return request.render("cap_crmlead_portal.opportunity_portal",{
            'opportunity': opportunity,
        })
    
    @http.route(['/my/offers_comparison/<string:key>'], type='http', auth="public", website=True)
    def offers_comparison(self, key=None):
        opportunity = request.env['crm.lead'].search([('x_key', '=', key)], limit=1)
        
        return request.render("cap_crmlead_portal.offers_comparison",{
            'opportunity': opportunity,
        })
    
    @http.route(['/x_document/addattachment'], type='http', auth="user", website=True)
    def upload_files(self, **post):
        values = {}
        opportunity_id = post.get('opportunity_id')
        document_id = post.get('document_id')
        document = request.env['x_document'].search([('id','=',document_id)])
        if post.get('attachment',False):
            Attachments = request.env['ir.attachment']
            attachment_list = request.httprequest.files.getlist('attachment')
            for att in attachment_list:
                name = att.filename
                attachment = att.read()
                attachment_id = Attachments.sudo().create({
                    'name':name,
                    'datas_fname': name,
                    'type': 'binary',   
                    'datas': base64.b64encode(attachment),
                })
                document.write({
                    'x_received_attachment_ids' : [(4, attachment_id.id, 0)]
                })
            
#             name = post.get('attachment').filename      
#             file = post.get('attachment')
            
#             attachment = file.read() 
#             attachment_id = Attachments.sudo().create({
#                 'name':name,
#                 'datas_fname': name,
#                 'type': 'binary',   
#                 'datas': base64.b64encode(attachment),
#             })
            
#             document.write({
#             'x_received_attachment_ids' : [(4, attachment_id.id, 0)]
#             })
        return request.redirect("/my/opportunity/" + str(opportunity_id))
       
    @http.route(['/x_document/reply'], type='http', auth="user", website=True)
    def reply(self, **post):
        values = {}
        opportunity_id = post.get('opportunity_id')
        document_id = post.get('document_id')
        document = request.env['x_document'].search([('id','=',document_id)])
        answer = post.get('answer')
        document.write({'x_studio_answer': answer})
        return request.redirect("/my/opportunity/" + str(opportunity_id))
   

