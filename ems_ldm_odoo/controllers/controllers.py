# from odoo import http


# class EmsLdmOdoo(http.Controller):
#     @http.route('/ems_ldm_odoo/ems_ldm_odoo', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ems_ldm_odoo/ems_ldm_odoo/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ems_ldm_odoo.listing', {
#             'root': '/ems_ldm_odoo/ems_ldm_odoo',
#             'objects': http.request.env['ems_ldm_odoo.ems_ldm_odoo'].search([]),
#         })

#     @http.route('/ems_ldm_odoo/ems_ldm_odoo/objects/<model("ems_ldm_odoo.ems_ldm_odoo"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ems_ldm_odoo.object', {
#             'object': obj
#         })

