from odoo import models, fields, api
from odoo.exceptions import ValidationError

class OdFieldDomain(models.Model):
    _name = "ems.ldm.odoo.field_domain"
    _description = "odoo：odoo項目ドメイン"
    _order = "name"

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
        ],
        string="データ型（分類）",
        required=True,
    )

    relation_object_class_id = fields.Many2one(
        "ems.ldm.object_class",
        string="関係先オブジェクトクラス",
        help="データ型（分類）が 継承 / 関連 の場合、関係先のオブジェクトクラスを指定",
    )

    field_ids = fields.One2many(
        "ems.ldm.odoo.field",
        "field_domain_id",
        string="Odoo項目"
    )

    @api.constrains("data_type", "relation_object_class_id")
    def _check_relation_object_class_required(self):
        for rec in self:
            if rec.data_type in ("extended", "relation") and not rec.relation_object_class_id:
                raise ValidationError(
                    "「データ型（分類）」が「継承」「関連」の場合、関係先オブジェクトクラスは必須です。"
                )

    source_code = fields.Text(
            string="定義",
            help="odoo項目ドメインの実装コードを記述（例：fields.Char(string='名称', required=True)）"
        )
    