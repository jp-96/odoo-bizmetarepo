from odoo import models, fields, api
from odoo.exceptions import ValidationError


class EntityReference(models.Model):
    _name = "ems.cdm.entity_reference"
    _description = "概念モデル：エンティティ参照"

    source_entity_id = fields.Many2one(
        "ems.cdm.entity",
        string="エンティティ",
        required=True,
    )

    target_entity_id = fields.Many2one(
        "ems.cdm.entity",
        string="参照先",
        required=True,
    )

    _sql_constraints = [
        (
            "unique_reference",
            "unique(source_entity_id, target_entity_id)",
            "同じ参照関係は重複できません。",
        ),
    ]

    @api.constrains("source_entity_id", "target_entity_id")
    def _check_self_reference(self):
        for rec in self:
            if rec.source_entity_id == rec.target_entity_id:
                raise ValidationError("自分自身への参照はできません。")
