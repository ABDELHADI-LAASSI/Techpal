from odoo import models, fields, api


class PurchaseOrder(models.Model):
    _inherit = "purchase.order"


    @api.onchange('currency_id', 'partner_id')
    def change_purchase_price(self):
        for record in self:
            for line in record.order_line:
                line.price_unit = line.product_id.standard_price * record.currency_id.rate