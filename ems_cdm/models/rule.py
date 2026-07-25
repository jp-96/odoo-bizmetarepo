from odoo import models, fields


class Rule(models.Model):
    _name = 'ems.cdm.rule'
    _description = 'ルール'

    name = fields.Char(string='ルール名', required=True)
    description = fields.Text(string='概要')

    entity_id = fields.Many2one(
        'ems.cdm.entity',
        string='代表エンティティ',
        required=True
    )

    target_attribute_ids = fields.One2many(
        'ems.cdm.rule.target',
        'rule_id',
        string='対象属性'
    )
