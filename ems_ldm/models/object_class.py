from odoo import models, fields

class ObjectClass(models.Model):
    _name = "ems.ldm.object_class"
    _description = "論理モデル：オブジェクトクラス"
    _order = "name"

    name = fields.Char(string="名称", required=True)

    system_id = fields.Many2one(
        "ems.ldm.logical_system",
        string="システム",
        required=True,
    )

    data_element_ids = fields.One2many(
        "ems.ldm.data_element",
        "object_class_id",
        string="データ要素"
    )

    constraint_ids = fields.One2many(
        "ems.ldm.constraint",
        "object_class_id",
        string="制約"
    )
