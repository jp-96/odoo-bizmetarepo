from odoo import models, fields

class DataElement(models.Model):
    _name = "ems.ldm.data_element"
    _description = "論理モデル：データ要素"
    _order = "sequence, name"

    name = fields.Char(string="名称", required=True)
    sequence = fields.Integer(string="表示順", default=10)

    object_class_id = fields.Many2one(
        "ems.ldm.object_class",
        string="オブジェクトクラス",
        required=True,
    )

    value_domain_id = fields.Many2one(
        "ems.ldm.value_domain",
        string="値ドメイン",
        required=True,
    )

    attribute_id = fields.Many2one(
        "ems.cdm.attribute",
        string="属性",
        required=True,
    )
