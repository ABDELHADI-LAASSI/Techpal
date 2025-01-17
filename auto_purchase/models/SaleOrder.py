from odoo import models, fields, api

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    purchase_order_id = fields.Many2one('purchase.order', string="Linked Purchase Order")

    def action_confirm(self):
        # Call the parent method
        res = super(SaleOrder, self).action_confirm()

        # Get the company as the fallback vendor
        our_company = self.env.user.company_id.partner_id

        # Loop through each sale order line to create individual purchase orders
        for line in self.order_line:
            product = line.product_id
            qty = line.product_uom_qty

            # Find the vendor with the lowest price for the product
            vendor_info = product.seller_ids.sorted(lambda s: s.price if s.price > 0 else float('inf'))
            if vendor_info:
                vendor = vendor_info[0].partner_id  # The vendor (res.partner) is referenced by the 'partner_id'
                price = vendor_info[0].price
            else:
                # Fallback to our company as the vendor and set a default price
                vendor = our_company
                price = product.standard_price  # Use the product's cost price as the purchase price

            # Create the purchase order for the product with the selected vendor
            po_vals = {
                'partner_id': vendor.id,
                'order_line': [(0, 0, {
                    'product_id': product.id,
                    'name': product.name,
                    'product_qty': qty,
                    'product_uom': product.uom_id.id,
                    'price_unit': price,
                    'date_planned': fields.Datetime.now(),
                })],
            }

            # Create the purchase order
            purchase_order = self.env['purchase.order'].create(po_vals)

            # Link the created purchase order to the sale order
            self.purchase_order_id = purchase_order.id

            # Confirm the purchase order
            # purchase_order.button_confirm()

        return res
