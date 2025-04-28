from odoo import models, fields, api

class AccountMove(models.Model):
    _inherit = "account.move"

    inv_margin = fields.Monetary(string="Margin", currency_field="currency_id", compute="compute_margin", store=True)

    @api.depends('invoice_line_ids', 'currency_id', 'partner_id')
    def compute_margin(self):
        for record in self:
            revenue = 0
            cost = 0
            for line in record.invoice_line_ids:
                if line.product_id:
                    revenue += line.quantity * line.price_unit
                    cost += line.quantity * line.product_id.standard_price * record.currency_id.inverse_rate
            record.inv_margin = revenue - cost