from odoo import models, fields


class SubjectArea(models.Model):
    _name = "ems.cdm.subject_area"
    _description = "サブジェクト領域"

    name = fields.Char(string="名称", required=True)

    entity_ids = fields.One2many(
        "ems.cdm.entity",
        "subject_area_id",
        string="エンティティ一覧",
    )
