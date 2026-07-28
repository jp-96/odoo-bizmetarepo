# from odoo import http


# class EmsUml(http.Controller):
#     @http.route('/ems_uml/ems_uml', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ems_uml/ems_uml/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ems_uml.listing', {
#             'root': '/ems_uml/ems_uml',
#             'objects': http.request.env['ems_uml.ems_uml'].search([]),
#         })

#     @http.route('/ems_uml/ems_uml/objects/<model("ems_uml.ems_uml"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ems_uml.object', {
#             'object': obj
#         })

