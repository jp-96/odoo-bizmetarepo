# from odoo import http


# class EmsCdm(http.Controller):
#     @http.route('/ems_cdm/ems_cdm', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ems_cdm/ems_cdm/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ems_cdm.listing', {
#             'root': '/ems_cdm/ems_cdm',
#             'objects': http.request.env['ems_cdm.ems_cdm'].search([]),
#         })

#     @http.route('/ems_cdm/ems_cdm/objects/<model("ems_cdm.ems_cdm"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ems_cdm.object', {
#             'object': obj
#         })

