# from odoo import models, fields, api


# class ems_ldm_odoo(models.Model):
#     _name = 'ems_ldm_odoo.ems_ldm_odoo'
#     _description = 'ems_ldm_odoo.ems_ldm_odoo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

