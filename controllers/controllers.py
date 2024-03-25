# -*- coding: utf-8 -*-
from odoo import http


class Termo(http.Controller):
    @http.route('/termo/termo',  type="http", auth="public", website=True)
    def index(self, **kw):
        return "Hello, world"

    # @http.route('/termo/termo/objects', auth='public') ir.actions.report
    # def list(self, **kw):
    #     return http.request.render('termo.listing', {
    #         'root': '/termo/termo',
    #         'objects': http.request.env['termo.termo'].search([]),
    #     })
    #
    # @http.route('/termo/termo/objects/<model("termo.termo"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('termo.object', {
    #         'object': obj
    #     })
