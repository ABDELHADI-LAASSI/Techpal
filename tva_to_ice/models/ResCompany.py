from odoo import fields, models, api
class ResCompany(models.Model):
    _inherit = 'res.company'

    vat = fields.Char(string="ICE")