from odoo import fields, models, api
class ResPartner(models.Model):
    _inherit = 'res.partner'

    vat = fields.Char(string="ICE")