from odoo import models, fields

class OdField(models.Model):
    _name = "ems.ldm.odoo.field"
    _description = "odoo：odoo項目"
    _order = "sequence, name"

    name = fields.Char(string="名称", required=True)
    sequence = fields.Integer(string="順番", default=10)
    field_name = fields.Char(string="項目名", required=True)

    object_class_id = fields.Many2one(
        "ems.ldm.object_class",
        string="オブジェクトクラス",
        required=True,
    )

    field_domain_id = fields.Many2one(
        "ems.ldm.odoo.field_domain",
        string="odoo項目ドメイン",
        required=True,
    )
