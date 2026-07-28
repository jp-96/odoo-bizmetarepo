from odoo import models, fields


class SubjectArea(models.Model):
    _name = "ems.cdm.subject_area"
    _description = "概念モデル：サブジェクト領域"
    _order = "sequence, name"

    name = fields.Char(string="名称", required=True)
    sequence = fields.Integer(string="順番", default=10)

    entity_ids = fields.One2many(
        "ems.cdm.entity",
        "subject_area_id",
        string="エンティティ一覧",
    )
