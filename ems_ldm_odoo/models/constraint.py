from odoo import models, fields, api

class Constraint(models.Model):
    _inherit = "ems.ldm.constraint"

    source_code = fields.Text(
            string="定義",
            help="制約の実装コードを記述"
        )
    