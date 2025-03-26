from odoo import models, fields, api

class Attachement(models.Model):
    _inherit = 'ir.attachment'
    
    public = fields.Boolean('Is public document', default=True)