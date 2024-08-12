# -*- coding: utf-8 -*-
from collections import defaultdict
from itertools import product as cartesian_product
import json
import logging
from datetime import datetime
from werkzeug.exceptions import Forbidden, NotFound
from werkzeug.urls import url_decode, url_encode, url_parse

from odoo import fields, http, SUPERUSER_ID, tools, _
from odoo.fields import Command
from odoo.http import request
from odoo.addons.base.models.ir_qweb_fields import nl2br
from odoo.addons.http_routing.models.ir_http import slug
from odoo.addons.payment import utils as payment_utils
from odoo.addons.payment.controllers import portal as payment_portal
from odoo.addons.payment.controllers.post_processing import PaymentPostProcessing
from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website.models.ir_http import sitemap_qs2dom
from odoo.exceptions import AccessError, MissingError, ValidationError
from odoo.addons.portal.controllers.portal import _build_url_w_params
from odoo.addons.website.controllers import main
from odoo.addons.website.controllers.form import WebsiteForm
from odoo.addons.sale.controllers import portal
from odoo.osv import expression
from odoo.tools import lazy
from odoo.tools.json import scriptsafe as json_scriptsafe


class Termo(http.Controller):
    @http.route('/termo/termo',  type="http", auth="public", website=True)
    def index(self, **kw):
        return "Hello, world"

    # @http.route('/termo/urunler', type='http', auth="public", website=True)
    # def list(self, **kw):
    #     urunler = request.env['product.template'].sudo().search([])
    #     return http.request.render('termo.listing', {
    #         'root': '/termo',
    #         'objects': urunler,
    #     })

    @http.route('/urun_secme_programi', type='http', auth="public", website=True)
    def urun_secme_programi(self, **post):
        products = request.env['product.template'].search([])
        values = {
            'products': products,
        }
        return http.request.render("termo.listing", values)

    @http.route( '/termo/termo/urunler', type='http', auth="public", website=True)
    def list(self, page=1, **kw):
        Product = request.env['product.template'].sudo()
        items_per_page = 50
        offset = (page - 1) * items_per_page
        total_products = Product.search_count([])
        urunler = Product.search([], limit=items_per_page, offset=offset)

        pager = request.website.pager(
            url='/termo/urunler',
            total=total_products,
            page=page,
            step=items_per_page
        )

        return http.request.render('termo.listing', {
            'objects': urunler,
            'pager': pager,
        })


    @http.route('/termo/termo/objects/<model("product.template"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('termo.object', {
            'object': obj
        })
