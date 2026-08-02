from odoo import models, fields

class ConstraintTarget(models.Model):
    _name = "ems.ldm.constraint_target"
    _description = "論理モデル：制約対象"
    _order = "sequence"

    sequence = fields.Integer(string="順番", default=10)

    constraint_id = fields.Many2one(
        "ems.ldm.constraint",
        string="制約",
        required=True,
        ondelete="cascade",
    )

    data_element_id = fields.Many2one(
        "ems.ldm.data_element",
        string="データ要素",
        required=True,
        ondelete="restrict",
    )
