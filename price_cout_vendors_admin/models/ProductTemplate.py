from odoo import models, fields, api

class ProductTemplate(models.Model):
    _inherit = "product.template"

    is_user = fields.Boolean(string='', default=False, compute="_compute_is_user")

    @api.depends('name')
    def _compute_is_user(self):
        is_user = self.env.user.has_group('price_cout_vendors_admin.price_user')
        for record in self:
            record.is_user = is_user

    