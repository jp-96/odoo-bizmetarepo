from odoo import models, fields


class Entity(models.Model):
    _name = "ems.cdm.entity"
    _description = "エンティティ"

    name = fields.Char(string="名称", required=True)

    subject_area_id = fields.Many2one(
        "ems.cdm.subject_area",
        string="サブジェクト領域",
        required=False,
    )

    attribute_ids = fields.One2many(
        "ems.cdm.attribute",
        "entity_id",
        string="属性",
    )
