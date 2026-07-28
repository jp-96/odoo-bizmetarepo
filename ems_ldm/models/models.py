# from odoo import models, fields, api


# class ems_ldm(models.Model):
#     _name = 'ems_ldm.ems_ldm'
#     _description = 'ems_ldm.ems_ldm'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100

