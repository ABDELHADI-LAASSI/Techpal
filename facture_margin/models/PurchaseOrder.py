from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = "purchase.order"

    inv_margin = fields.Monetary(string="Margin", currency_field="currency_id", compute="compute_margin", store=True)

    @api.depends('order_line', 'currency_id', 'partner_id')
    def compute_margin(self):
        for record in self:
            revenue = 0
            cost = 0
            for line in record.order_line:
                cost += line.product_qty * line.price_unit
                revenue += line.product_qty * line.product_id.lst_price * record.currency_id.inverse_rate

            record.inv_margin = revenue - cost