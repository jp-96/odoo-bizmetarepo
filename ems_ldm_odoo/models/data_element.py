from odoo import models, fields, api

class DataElement(models.Model):
    _inherit = "ems.ldm.data_element"

    field_name = fields.Char(string="項目名", required=False)
