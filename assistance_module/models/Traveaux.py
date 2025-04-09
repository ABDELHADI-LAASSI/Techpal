from odoo import models, fields, api

class Traveaux(models.Model):
    _name = 'assistance.traveaux'

    name = fields.Char(required=True, string="Nom du traveaux")

    assistance_id = fields.Many2one('assistance', string='Assistance')

    traveaux_line_ids = fields.One2many('assistance.traveaux.line', 'traveaux_id', string='Traveaux Lines')