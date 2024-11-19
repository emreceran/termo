# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, AccessError


class Tip(models.Model):
    _name = "termo.tip"
    _description = 'Ürün Tipi'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Ürün Tipi', required=True, translate=True)
    teknik_cizim = fields.Binary("Teknik Çizim", help="Teknik Ressim")
    gorsel = fields.Binary("Ürün Görseli ", help="Bu tipte yer alacak ürübnlerin resimleri")
    filtre_grubu_id = fields.Many2one('termo.filtre_grubu')
    filtre = fields.Many2many(related="filtre_grubu_id.filtreler", string='Filtreler')
    grup = fields.Char(related="filtre_grubu_id.name")
    web_grubu_id = fields.Many2one('termo.web_grubu')
    urun_serisi_id = fields.Many2one('termo.seri')
    urun_serisi = fields.Char(related="urun_serisi_id.name")
    public = fields.Many2many(related="web_grubu_id.kategoriler", string='Web Kategori')
    # product_ids = fields.One2many('product.template', 'termo_tip_id', string='Related Products')
    # product_ids = fields.Many2many('product.template', string='Related Products', domain="[('termo_tip_id', '=', False)]")

    # def update_related_products(self):
    #     for tip in self:
    #         if tip.product_ids:
    #             tip.product_ids.write({
    #                 'gorsel': tip.gorsel,
    #                 'public': [(6, 0, tip.public.ids)]
    #             })
    #
    # @api.multi
    # def write(self, vals):
    #     res = super(Tip, self).write(vals)
    #     self.update_related_products()
    #     return res
class filtredegeri(models.Model):
    _name = "termo.filtre"
    _description = 'Ürün Filtresi'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Filtre Adı ', required=True, translate=True)
    min_deger = fields.Integer(string="Filtre min deger")
    max_deger = fields.Integer(string="Filtre max deger")
    delta_deger = fields.Integer(string="Filtre Artış deger")

class filtreler(models.Model):
    _name = "termo.filtreler"
    _description = 'Ürün Filtreleri'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Ürün Filtresi', required=True, translate=True)


class UrunSeri(models.Model):
    _name = "termo.seri"
    _description = 'Ürün Serisi'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Ürün Serisi', required=True, translate=True)


class filtregrubu(models.Model):
    _name = "termo.filtre_grubu"
    _description = 'Filtre Grupları'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Ürün Filtresi', required=True, translate=True)
    filtreler = fields.Many2many('product.attribute', string='Filtreler')


class webkategorigrup(models.Model):
    _name = "termo.web_grubu"
    _description = 'Web Kategori Grupları'

    active = fields.Boolean('Active', default=True)
    name = fields.Char(string='Ürün Filtresi', required=True, translate=True)
    kategoriler = fields.Many2many('product.public.category', string='Filtreler')


#
#
#
# class ResPartner(models.Model):
#     _inherit = 'res.partner'
#
#     ilgili_kontak = fields.Many2one(
#         'res.partner', string="İlgili Kontak")



class ProductTemplate(models.Model):
    _inherit = "product.attribute"

    att_type = fields.Selection(
        [("aralik", "Aralık"), ("sabit", "Sabit Değerler")],
        help="Attribute type",
        default="sabit",
    )
    ref = fields.Char(related="attribute_field_id.name")
    alt_sinir = fields.Integer(string="Filtre min deger")
    Ust_sinir = fields.Integer(string="Filtre max deger")
    delta_deger = fields.Integer(string="Filtre Artış deger")
    bos_deger = fields.Integer(string="Filtre Boş deger")
    attribute_field_id = fields.Many2one(
        'ir.model.fields',
        string="Attribute Field",
        domain="[('model_id.model', '=', 'product.template')]"
    )

    def gorev(self):

        for record in self:

            min = record.alt_sinir
            max = record.Ust_sinir
            delta = record.delta_deger
            degerelr = []
            if record.att_type == "aralik":
                while min < max:
                    alt = int(min / delta) * delta
                    ust = alt + delta
                    deger = str(alt) + " - " + str(ust)
                    degerelr.append(deger)
                    min = ust
            else:
                while min < max:
                    alt = int(min / delta) * delta
                    ust = alt + delta
                    deger = str(ust)
                    degerelr.append(deger)
                    min = ust


            colors =['a','b']
            record.value_ids.unlink()
            self.env['product.attribute.value'].create([{'name': color, 'attribute_id': record.id} for color in degerelr])

# class ProductImage(models.Model):
#     _inherit = 'product.image'
#     _description = "Product Image"
#
#     product_tmpl_id = fields.Many2one('product.template', "Product Template", index=True, ondelete='cascade')
#
#     image_1920 = fields.Image(compute='_compute_1920', store=True)
#
#
#     @api.depends('product_tmpl_id')
#     def _compute_1920(self):
#         for image in self:
#             image.image_1920 = image.product_tmpl_id.termo_tip_id.gorsel