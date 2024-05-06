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

    @http.route('/termo/termo/urunler', auth='public')
    def list(self, **kw):
        urunler = request.env['product.template'].sudo().search([])
        print("urunler")
        print(urunler)

        yuzeyler = {}
        for product in urunler:
            yuzeyler[product.id] = (product.yuzey)

        print(yuzeyler)


        return http.request.render('termo.listing', {
            'root': '/termo/termo',
            'yuzeyler': yuzeyler,
            'objects': http.request.env['product.template'].search([]),
        })

    @http.route('/termo/termo/objects/<model("product.template"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('termo.object', {
            'object': obj
        })
