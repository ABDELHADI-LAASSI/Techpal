from odoo import api, fields, models


class InheritResConfigSettings(models.TransientModel):
    _inherit = "res.config.settings"

    web_title = fields.Char(
        string="Window Title",
        help="Setup System Name,which replace Odoo",
        config_parameter="web_title",
    )

    @api.model
    def get_web_title(self):
        ir_config = self.env["ir.config_parameter"].sudo()
        web_title = ir_config.get_param("web_title", default="")
        return {"web_title": web_title}
