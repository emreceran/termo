# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons.http_routing.models.ir_http import slug, unslug
from odoo.addons.website.models import ir_http
from odoo.tools.translate import html_translate
from odoo.osv import expression

class ProductTemplate(models.Model):
    _inherit = [
        "product.template",
        "website.seo.metadata",
        'website.published.multi.mixin',
        'website.searchable.mixin',
        'rating.mixin',
    ]
    _name = 'product.template'
    _mail_post_access = 'read'
    _check_company_auto = True



    def _get_sales_prices(self, pricelist):
        pricelist.ensure_one()
        partner_sudo = self.env.user.partner_id

        # Try to fetch geoip based fpos or fallback on partner one
        fpos_id = self.env['website']._get_current_fiscal_position_id(partner_sudo)
        fiscal_position = self.env['account.fiscal.position'].sudo().browse(fpos_id)

        sales_prices = pricelist._get_products_price(self, 1.0)

        show_discount = pricelist.discount_policy == 'without_discount'

        base_sales_prices = self.price_compute('list_price', currency=pricelist.currency_id)
        print(base_sales_prices)

        res = {}
        for template in self:
            price_reduce = sales_prices[template.id]

            product_taxes = template.sudo().taxes_id.filtered(lambda t: t.company_id == t.env.company)
            taxes = fiscal_position.map_tax(product_taxes)

            price_reduce = self.env['account.tax']._fix_tax_included_price_company(
                price_reduce, product_taxes, taxes, self.env.company)

            tax_display = self.user_has_groups('account.group_show_line_subtotals_tax_excluded') and 'total_excluded' or 'total_included'
            price_reduce = taxes.compute_all(price_reduce, pricelist.currency_id, 1, template, partner_sudo)[tax_display]

            template_price_vals = {
                'price_reduce': price_reduce
            }
            base_price = None
            price_list_contains_template = price_reduce != base_sales_prices[template.id]

            if template.compare_list_price:
                # The base_price becomes the compare list price and the price_reduce becomes the price
                base_price = template.compare_list_price
                if not price_list_contains_template:
                    price_reduce = base_sales_prices[template.id]
                    template_price_vals.update(price_reduce=price_reduce)
            elif show_discount and price_list_contains_template:
                base_price = base_sales_prices[template.id]

            if base_price and base_price != price_reduce:
                base_price = self.env['account.tax']._fix_tax_included_price_company(
                    base_price, product_taxes, taxes, self.env.company)
                base_price = taxes.compute_all(base_price, pricelist.currency_id, 1, template, partner_sudo)[
                    tax_display]
                template_price_vals['base_price'] = base_price

            res[template.id] = template_price_vals
        print(res)
        return res