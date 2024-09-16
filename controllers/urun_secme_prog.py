# termo/controllers/urun_secme_prog.py

from odoo import http
from odoo.http import request

class TermoProductSelection(http.Controller):

    @http.route('/urun_secme_programi', type='http', auth='public', website=True)
    def urun_secme(self, **kwargs):
        categories = request.env['product.public.category'].search([])
        return request.render('termo.urun_secme_programi_template', {
            'categories': categories
        })

    @http.route('/urun_secme_programi/get_subcategories/<int:category_id>', type='json', auth='public')
    def get_subcategories(self, category_id):
        subcategories = request.env['product.public.category'].search([('parent_id', '=', category_id)])
        if not subcategories:
            return {'subcategories': []}
        subcategories_data = [{'id': sub.id, 'name': sub.name} for sub in subcategories]
        return {'subcategories': subcategories_data}
