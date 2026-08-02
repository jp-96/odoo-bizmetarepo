from odoo import models, fields, api

class ValueDomain(models.Model):
    _inherit = "ems.ldm.value_domain"

    source_code = fields.Text(
            string="定義",
            help="値ドメインの実装コードを記述（例：fields.Char(string='名称', required=True)）"
        )
    