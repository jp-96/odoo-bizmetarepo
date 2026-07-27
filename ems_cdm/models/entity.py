from odoo import models, fields


class Entity(models.Model):
    _name = "ems.cdm.entity"
    _description = "概念モデル：エンティティ"
    _order = "name"

    name = fields.Char(string="名称", required=True)

    subject_area_id = fields.Many2one(
        "ems.cdm.subject_area",
        string="サブジェクト領域",
    )

    attribute_ids = fields.One2many(
        "ems.cdm.attribute",
        "entity_id",
        string="属性",
    )

    rule_ids = fields.One2many(
        "ems.cdm.rule",
        "entity_id",
        string="ルール",
    )

    reference_ids = fields.One2many(
        "ems.cdm.entity_reference",
        "source_entity_id",
        string="参照リンク",
    )
