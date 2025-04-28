from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit="purchase.order"

    def button_confirm(self):
        for record in self:
            for line in record.order_line:

                # Normal Test With DH

                product = line.product_id

                cout_product_current_price = product.standard_price
                cout_product_purchase_price = line.price_unit

                product_new_price = (cout_product_purchase_price + cout_product_current_price) / 2

                product.standard_price = product_new_price