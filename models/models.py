# -*- coding: utf-8 -*-

from odoo import models, fields, api


class Renk(models.Model):
    _name = "termo.tip"
    _description = 'Ürün Tipi'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Ürün Tipi', required=True, translate=True)
    teknik_cizim = fields.Binary("Teknik Çizim", help="Teknik Ressim")


class ProductTemplate(models.Model):
    _inherit = "product.template"

    adamsaat = fields.Float (string = "Adam/Saat", default = 0.0, store=True)
    yuzey = fields.Float (string = "Yüzey", default = 0.0, store=True)
    boru_hacmi = fields.Float (string = "Boru Hacmi", default = 0.0, store=True)
    t1 = fields.Float (string = "To / Te -35°C/-40°C W", default = 0.0, store=True)
    t2 = fields.Float (string = "To / Te -40°C/-45°C W", default = 0.0, store=True)
    sc1 = fields.Float (string = "SC1 10°C/0°C W", default = 0.0, store=True)
    sc2 = fields.Float (string = "SC2 0°C/- 8°C W", default = 0.0, store=True)
    sc3 = fields.Float (string = "SC3 - 18°C/ - 25°C W", default = 0.0, store=True)
    sc4 = fields.Float (string = "SC4 - 25°C/ - 31°C W", default = 0.0, store=True)
    fan_adet = fields.Float (string = "Fan Adeti", default = 0.0, store=True)
    fan_cap = fields.Float (string = "Fan Çapı", default = 0.0, store=True)
    hava_debisi = fields.Float (string = "Hava Debisi m³/h", default = 0.0, store=True)
    H = fields.Float (string = "H", default = 0.0, store=True)
    L = fields.Float (string = "L", default = 0.0, store=True)
    W = fields.Float (string = "W", default = 0.0, store=True)
    H1 = fields.Float (string = "H", default = 0.0, store=True)
    L1 = fields.Float (string = "L1", default = 0.0, store=True)
    W1 = fields.Float (string = "W1", default = 0.0, store=True)
    W2 = fields.Float (string = "W2", default = 0.0, store=True)
    W3 = fields.Float (string = "W3", default = 0.0, store=True)
    LA = fields.Float (string = "LA", default = 0.0, store=True)
    lamel_aralik= fields.Integer(string = "Lamel Aralığı", default = 4, store=True)
    hatve= fields.Integer(string = "Hatve ", default = 6, store=True)
    kapasite = fields.Integer(string = "Kapasite ", default = 6, store=True)


    termo_tip = fields.Many2one('termo.tip', string="tEKNİK çİZİM")
    # termo_id = fields.Many2one('termo.tip', string="tEKNİK çİZİM")
    # image_1920 =  fields.Binary(related='termo_id.teknik_cizim',)


    kapasite = fields.Float(string = "Kapasite ", compute="_value_pc", default = 6, store=True)
    oda_sicakligi = fields.Float(string = "Oda Sıcaklığı ", compute="_value_pc", default = 6, store=True)
    evaporasyon_sicakligi = fields.Float(string = "Evaporasyon Sıcaklığı ", compute="_value_pc", default = 6, store=True)

    def get_teknik_cizim_name(self):
        for rec in self:
            rec.image_1920 = rec.termo_tip.teknik_cizim

    @api.depends('hatve', 'sc2', 'sc3', 'sc4')
    def _value_pc(self):
        for record in self:
            if record.hatve == 6:
                record.kapasite = record.sc2
                record.oda_sicakligi = 0
                record.evaporasyon_sicakligi = 8
            elif record.hatve == 8:
                record.kapasite = record.sc3
                record.oda_sicakligi = -18
                record.evaporasyon_sicakligi = 25
            elif record.hatve == 10:
                record.kapasite = record.sc4
                record.oda_sicakligi = -25
                record.evaporasyon_sicakligi = 31










#
# def _get_adamsaat_prices(self, pricelist):
#
#     partner_sudo = self.env.user.partner_id
#
#     # Try to fetch geoip based fpos or fallback on partner one
#     fpos_id = self.env['website']._get_current_fiscal_position_id(partner_sudo)
#     fiscal_position = self.env['account.fiscal.position'].sudo().browse(fpos_id)
#
#     sales_prices = pricelist._get_products_price(self, 1.0)
#
#     show_discount = pricelist.discount_policy == 'without_discount'
#
#     base_sales_prices = self.price_compute('list_price', currency=pricelist.currency_id)
#     print(base_sales_prices)
#
#     res = {}
#     for template in self:
#         price_reduce = sales_prices[template.id]
#
#         product_taxes = template.sudo().taxes_id.filtered(lambda t: t.company_id == t.env.company)
#         taxes = fiscal_position.map_tax(product_taxes)
#
#         price_reduce = self.env['account.tax']._fix_tax_included_price_company(
#             price_reduce, product_taxes, taxes, self.env.company)
#
#         tax_display = self.user_has_groups('account.group_show_line_subtotals_tax_excluded') and 'total_excluded' or 'total_included'
#         price_reduce = taxes.compute_all(price_reduce, pricelist.currency_id, 1, template, partner_sudo)[tax_display]
#
#         template_price_vals = {
#             'price_reduce': price_reduce
#         }
#         base_price = None
#         price_list_contains_template = price_reduce != base_sales_prices[template.id]
#
#         if template.compare_list_price:
#             # The base_price becomes the compare list price and the price_reduce becomes the price
#             base_price = template.compare_list_price
#             if not price_list_contains_template:
#                 price_reduce = base_sales_prices[template.id]
#                 template_price_vals.update(price_reduce=price_reduce)
#         elif show_discount and price_list_contains_template:
#             base_price = base_sales_prices[template.id]
#
#         if base_price and base_price != price_reduce:
#             base_price = self.env['account.tax']._fix_tax_included_price_company(
#                 base_price, product_taxes, taxes, self.env.company)
#             base_price = taxes.compute_all(base_price, pricelist.currency_id, 1, template, partner_sudo)[
#                 tax_display]
#             template_price_vals['base_price'] = base_price
#
#         res[template.id] = template_price_vals
#     print(res)
#     return res
# class termo(models.Model):
#     _name = 'termo.termo'
#     _description = 'termo.termo'

#     name = fields.Char()
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
