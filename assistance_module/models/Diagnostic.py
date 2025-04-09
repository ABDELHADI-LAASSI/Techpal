from odoo import models, fields, api

class Diagnostic(models.Model):
    _name = 'assistance.diagnostic'
    _description = 'Assistance Diagnostic'

    name = fields.Char(string="Nom")

    assistance_id = fields.Many2one('assistance', string='Assistance')

    diagnostic_line_ids = fields.One2many('assistance.diagnostic.line', 'diagnostic_id', string='Diagnostic Lines')
