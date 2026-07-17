# from odoo import http


# class Biz001(http.Controller):
#     @http.route('/biz001/biz001', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/biz001/biz001/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('biz001.listing', {
#             'root': '/biz001/biz001',
#             'objects': http.request.env['biz001.biz001'].search([]),
#         })

#     @http.route('/biz001/biz001/objects/<model("biz001.biz001"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('biz001.object', {
#             'object': obj
#         })

