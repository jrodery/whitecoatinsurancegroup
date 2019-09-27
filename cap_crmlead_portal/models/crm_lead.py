from odoo import api, fields, models, _
from odoo.exceptions import UserError

import uuid

class Lead(models.Model):
    _inherit = "crm.lead"
    
    @api.multi
    def generate_access_key(self):
        self.write({
			'x_key' : uuid.uuid4()
		})
        return True
