# termo/controllers/urun_secme_prog.py

from odoo import http
from odoo.http import request

class TermoProductSelection(http.Controller):
    @http.route('/urun_secme_programi', type='http', auth='public', website=True)
    def urun_secme(self, **kwargs):
        categories = request.env['product.category'].search([])
        return request.render('termo.urun_secme_programi_template', {
            'categories': categories
        })
