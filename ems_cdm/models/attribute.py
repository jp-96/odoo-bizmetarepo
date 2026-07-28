from odoo import models, fields


class Attribute(models.Model):
    _name = "ems.cdm.attribute"
    _description = "概念モデル：属性"
    _order = "sequence, name"

    name = fields.Char(string="名称", required=True)
    sequence = fields.Integer(string="順番", default=10)

    entity_id = fields.Many2one(
        "ems.cdm.entity",
        string="エンティティ",
        required=True,
    )

    domain_id = fields.Many2one(
        "ems.cdm.attribute_domain",
        string="属性ドメイン",
        required=True,
    )
