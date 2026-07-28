from odoo import models, fields

class Constraint(models.Model):
    _name = "ems.ldm.constraint"
    _description = "論理モデル：制約"
    _order = "sequence, name"

    name = fields.Char(string="名称", required=True)
    sequence = fields.Integer(string="表示順", default=10)
    description = fields.Text(string="説明")

    object_class_id = fields.Many2one(
        "ems.ldm.object_class",
        string="オブジェクトクラス",
        required=True,
        ondelete="cascade",
    )

    # ★ ルールは任意
    rule_id = fields.Many2one(
        "ems.cdm.rule",
        string="ルール",
        required=False,
        ondelete="restrict",
    )

    target_ids = fields.One2many(
        "ems.ldm.constraint_target",
        "constraint_id",
        string="制約対象"
    )
