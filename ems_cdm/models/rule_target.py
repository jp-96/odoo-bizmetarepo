from odoo import models, fields


class RuleTarget(models.Model):
    _name = 'ems.cdm.rule.target'
    _description = '概念モデル：ルール対象属性'
    _order = "sequence"

    sequence = fields.Integer(string="順番", default=10)

    rule_id = fields.Many2one(
        'ems.cdm.rule',
        string='ルール',
        required=True
    )

    attribute_id = fields.Many2one(
        'ems.cdm.attribute',
        string='属性',
        required=True
    )
