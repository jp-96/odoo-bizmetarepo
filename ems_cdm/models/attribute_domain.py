from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AttributeDomain(models.Model):
    _name = "ems.cdm.attribute_domain"
    _description = "属性ドメイン"

    name = fields.Char(string="名称", required=True)
    description = fields.Text(string="説明")

    data_type = fields.Selection(
        [
            ("string", "文字列系"),
            ("number", "数値系"),
            ("date", "日付・時間系"),
            ("boolean", "真偽値"),
            ("selection", "選択肢系"),
            ("binary", "バイナリ系"),
            ("extended", "継承"),
            ("relation", "関連"),
            ("reference", "参照"),
        ],
        string="データ型（分類）",
        required=True,
    )

    relation_entity_id = fields.Many2one(
        "ems.cdm.entity",
        string="参照先エンティティ",
        help="データ型が 継承 / 関連 / 参照 の場合、参照するエンティティを指定",
    )

    attribute_ids = fields.One2many(
        "ems.cdm.attribute",
        "domain_id",
        string="関連属性",
    )

    @api.constrains("data_type", "relation_entity_id")
    def _check_relation_entity_required(self):
        for rec in self:
            if rec.data_type in ("extended", "relation", "reference") and not rec.relation_entity_id:
                raise ValidationError(
                    "データ型が「継承」「関連」「参照」の場合、参照先エンティティは必須です。"
                )
