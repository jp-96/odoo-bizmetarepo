from odoo import models, fields

class LogicalSystem(models.Model):
    _name = "ems.ldm.logical_system"
    _description = "論理モデル：システム"
    _order = "sequence, name"

    name = fields.Char(string="名称", required=True)
    sequence = fields.Integer(string="表示順", default=10)

    object_class_ids = fields.One2many(
        "ems.ldm.object_class",
        "system_id",
        string="オブジェクトクラス"
    )
