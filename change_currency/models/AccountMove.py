from odoo import models, fields, api
from datetime import timedelta


class AccountMove(models.Model):
    _inherit = "account.move"


    @api.onchange('currency_id', 'partner_id')
    def change_price(self):
        for record in self:

            for line in record.invoice_line_ids:

                line.price_unit = line.product_id.list_price * record.currency_id.rate

    @api.onchange('invoice_date')
    def calc_date_ech(self):
        for record in self:
            if record.invoice_date:
                record.invoice_date_due = record.invoice_date + timedelta(days=100)