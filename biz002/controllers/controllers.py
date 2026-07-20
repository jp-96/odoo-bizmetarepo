# from odoo import http


# class Biz002(http.Controller):
#     @http.route('/biz002/biz002', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/biz002/biz002/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('biz002.listing', {
#             'root': '/biz002/biz002',
#             'objects': http.request.env['biz002.biz002'].search([]),
#         })

#     @http.route('/biz002/biz002/objects/<model("biz002.biz002"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('biz002.object', {
#             'object': obj
#         })

