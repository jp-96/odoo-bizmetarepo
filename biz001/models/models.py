from odoo import models, fields

# ----------------------------
# データモデル
# ----------------------------
class DataModel(models.Model):
    _name = "biz001.data_model"
    _description = "biz001 データモデル"

    name = fields.Char(string="名称", required=True)

    item_ids = fields.One2many(
        "biz001.data_item",
        "model_id",
        string="データ項目",
    )


# ----------------------------
# データ項目
# ----------------------------
class DataItem(models.Model):
    _name = "biz001.data_item"
    _description = "biz001 データ項目"

    name = fields.Char(string="名称", required=True)

    data_type = fields.Selection(
        [
            ("char", "文字列"),
            ("integer", "整数"),
            ("float", "実数"),
            ("boolean", "真偽値"),
            ("date", "日付"),
            ("datetime", "日時"),
            ("selection", "選択肢（列挙型）"),
            ("relation", "関連（Many2one/One2many）"),
        ],
        string="データ型",
        required=True,
    )

    model_id = fields.Many2one(
        "biz001.data_model",
        string="データモデル",
        required=True,
    )

    domain_id = fields.Many2one(
        "biz001.data_domain",
        string="データドメイン",
    )


# ----------------------------
# データドメイン
# ----------------------------
class DataDomain(models.Model):
    _name = "biz001.data_domain"
    _description = "biz001 データドメイン"

    name = fields.Char(string="名称", required=True)
    description = fields.Text(string="説明")

    value_ids = fields.One2many(
        "biz001.data_domain_value",
        "domain_id",
        string="ドメイン値",
    )


# ----------------------------
# 列挙型ドメイン値
# ----------------------------
class DataDomainValue(models.Model):
    _name = "biz001.data_domain_value"
    _description = "biz001 データドメイン値（列挙型）"

    name = fields.Char(string="値", required=True)

    domain_id = fields.Many2one(
        "biz001.data_domain",
        string="データドメイン",
        required=True,
    )
