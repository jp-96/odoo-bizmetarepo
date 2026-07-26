from odoo import models, fields, api
from odoo.exceptions import ValidationError


# =========================================================
# biz002 データモデル（業務モデル定義）
# =========================================================
class DataModel(models.Model):
    _name = "biz002.data_model"
    _description = "biz002 データモデル"

    name = fields.Char(string="名称", required=True)

    item_ids = fields.One2many(
        "biz002.data_item",
        "model_id",
        string="データ項目",
    )


# =========================================================
# biz002 データ項目（項目定義：型は持たず、必須のみ）
# =========================================================
class DataItem(models.Model):
    _name = "biz002.data_item"
    _description = "biz002 データ項目"

    name = fields.Char(string="名称", required=True)

    required = fields.Boolean(string="必須", default=False)

    model_id = fields.Many2one(
        "biz002.data_model",
        string="データモデル",
        required=True,
    )

    domain_id = fields.Many2one(
        "biz002.data_domain",
        string="データドメイン",
        required=True,
    )


# =========================================================
# biz002 データドメイン（分類レベルのデータ型＋関連先モデル）
# =========================================================
class DataDomain(models.Model):
    _name = "biz002.data_domain"
    _description = "biz002 データドメイン"

    name = fields.Char(string="名称", required=True)
    description = fields.Text(string="説明")

    # 分類レベルのデータ型
    data_type = fields.Selection(
        [
            ("string", "文字列系"),
            ("number", "数値系"),
            ("date", "日付・時間系"),
            ("boolean", "真偽値"),
            ("selection", "選択肢系"),
            ("binary", "バイナリ系"),
            ("relation", "関連（結合）"),
            ("extended", "継承（派生）"),
            ("reference", "参照（依存）"),
        ],
        string="データ型（分類）",
        required=True,
    )

    # relation / extended の場合のみ必須
    relation_model_id = fields.Many2one(
        "biz002.data_model",
        string="参照先モデル",
        help="データ型が relation または extended の場合、参照するモデルを指定",
    )

    # このドメインを使っている項目一覧
    item_ids = fields.One2many(
        "biz002.data_item",
        "domain_id",
        string="関連データ項目",
    )

    # relation / extended の場合は参照先モデル必須
    @api.constrains("data_type", "relation_model_id")
    def _check_relation_model_required(self):
        for rec in self:
            if rec.data_type in ("relation", "extended") and not rec.relation_model_id:
                raise ValidationError(
                    "データ型が「関連」または「拡張」の場合、参照先モデルは必須です。"
                )
