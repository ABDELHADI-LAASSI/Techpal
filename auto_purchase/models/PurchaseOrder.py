from odoo import models, fields, api

class PurchaseOrder(models.Model):
    _inherit = 'purchase.order'

    @api.onchange('partner_id')
    def _onchange_vendor(self):
        """
        This method recalculates the prices of the order lines when the vendor (partner)
        is changed in the purchase order.
        """
        for line in self.order_line:
            if line.product_id:
                # Correct search query to use partner_id instead of name
                vendor_info = self.env['product.supplierinfo'].search([
                    ('partner_id', '=', self.partner_id.id),  # Correct field for vendor
                    ('product_tmpl_id', '=', line.product_id.product_tmpl_id.id),
                ], limit=1)

                if vendor_info:
                    # If vendor-specific price is found, update the line price
                    line.price_unit = vendor_info.price
                else:
                    # If no vendor price, set the standard product price
                    line.price_unit = line.product_id.standard_price
