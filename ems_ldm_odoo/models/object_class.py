from odoo import models, fields, api

class ObjectClass(models.Model):
    _inherit = "ems.ldm.object_class"

    model_name = fields.Char(
        string="Odooモデル名",
        required=False,
    )

    namespace_id = fields.Many2one(
        "ems.ldm.odoo.namespace",
        string="Odoo名前空間",
        required=False,
    )

    technical_model_name = fields.Char(
        string="技術モデル名",
        compute="_compute_technical_model_name",
        store=True,
    )

    @api.depends("namespace_id", "namespace_id.odoo_namespace", "model_name")
    def _compute_technical_model_name(self):
        for rec in self:
            if rec.namespace_id and rec.model_name:
                rec.technical_model_name = f"{rec.namespace_id.odoo_namespace}.{rec.model_name}"
            else:
                rec.technical_model_name = False


    field_ids = fields.One2many(
        "ems.ldm.odoo.field",
        "object_class_id",
        string="Odooフィールド"
    )
