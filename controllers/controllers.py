# -*- coding: utf-8 -*-
# from odoo import http


# class Gestiondesreclamtion(http.Controller):
#     @http.route('/gestiondesreclamtion/gestiondesreclamtion', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/gestiondesreclamtion/gestiondesreclamtion/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('gestiondesreclamtion.listing', {
#             'root': '/gestiondesreclamtion/gestiondesreclamtion',
#             'objects': http.request.env['gestiondesreclamtion.gestiondesreclamtion'].search([]),
#         })

#     @http.route('/gestiondesreclamtion/gestiondesreclamtion/objects/<model("gestiondesreclamtion.gestiondesreclamtion"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('gestiondesreclamtion.object', {
#             'object': obj
#         })
