from odoo import models, fields

class OdNamespace(models.Model):
    _name = "ems.ldm.odoo.namespace"
    _description = "odoo：モデル名前空間"
    _order = "sequence, name"

    name = fields.Char(string="名称", required=True)
    sequence = fields.Integer(string="順番", default=10)
    description = fields.Text(string="説明")

    odoo_namespace = fields.Char(string="名前空間", required=True)  # 例: ems, ems.cdm, ems.ldm
    
    object_class_ids = fields.One2many(
        "ems.ldm.object_class",
        "namespace_id",
        string="オブジェクトクラス"
    )
