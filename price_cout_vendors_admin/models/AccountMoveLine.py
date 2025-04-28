from odoo import models, fields, api

class AccountMoveLine(models.Model):
    _inherit = "account.move.line"

    is_user = fields.Boolean(string='Is User', default=False, compute="_compute_is_user")

    @api.depends('price_unit')
    def _compute_is_user(self):
        is_user = self.env.user.has_group('price_cout_vendors_admin.price_user')
        for record in self:
            record.is_user = is_user