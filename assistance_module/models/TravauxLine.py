from odoo import models, fields, api

class TravauxLine(models.Model):
    _name = 'assistance.traveaux.line'
    _description = 'Traveaux'

    name = fields.Char(string="Nom du traveaux")

    traveaux_id = fields.Many2one('assistance.traveaux', string="Traveaux")