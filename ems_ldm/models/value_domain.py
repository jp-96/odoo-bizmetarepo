from odoo import models, fields

class ValueDomain(models.Model):
    _name = "ems.ldm.value_domain"
    _description = "論理モデル：値ドメイン"
    _order = "name"

    name = fields.Char(string="名称", required=True)

    data_element_ids = fields.One2many(
        "ems.ldm.data_element",
        "value_domain_id",
        string="データ要素"
    )
