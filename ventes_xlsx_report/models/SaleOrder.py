from odoo import fields, models

class SaleOrder(models.Model):
    _inherit = "sale.order"


    def xlsx_report(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/vente/excel/report',
            'target': 'new'
        }