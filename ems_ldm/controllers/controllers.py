# from odoo import http


# class EmsLdm(http.Controller):
#     @http.route('/ems_ldm/ems_ldm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ems_ldm/ems_ldm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ems_ldm.listing', {
#             'root': '/ems_ldm/ems_ldm',
#             'objects': http.request.env['ems_ldm.ems_ldm'].search([]),
#         })

#     @http.route('/ems_ldm/ems_ldm/objects/<model("ems_ldm.ems_ldm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ems_ldm.object', {
#             'object': obj
#         })

