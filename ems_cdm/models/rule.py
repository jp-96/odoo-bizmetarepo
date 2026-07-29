from odoo import models, fields


class Rule(models.Model):
    _name = 'ems.cdm.rule'
    _description = '概念モデル：ルール'
    _order = "sequence, name"

    name = fields.Char(string='名称', required=True)
    sequence = fields.Integer(string="順番", default=10)
    description = fields.Text(string='説明')

    entity_id = fields.Many2one(
        'ems.cdm.entity',
        string='エンティティ',
        required=True
    )

    target_attribute_ids = fields.One2many(
        'ems.cdm.rule.target',
        'rule_id',
        string='対象属性'
    )
