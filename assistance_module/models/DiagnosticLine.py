from odoo import models, fields, api

class DiagnosticLine(models.Model):
    _name = 'assistance.diagnostic.line'
    _description = 'Assistance Diagnostic Line'

    name = fields.Char(string="Nom")

    diagnostic_id = fields.Many2one('assistance.diagnostic', string="Diagnostic")