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
    filtre = fields.Many2many('product.attribute', string='Filtreler')
    grup = fields.Char("Filtre grubu")
    public = fields.Many2many('product.public.category', string="Web kategori")
    # product_ids = fields.One2many('product.template', 'termo_tip_id', string='Related Products')
    product_ids = fields.Many2many('product.template', string='Related Products', domain="[('termo_tip_id', '=', False)]")

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

class ProductTemplate(models.Model):
    _inherit = "product.attribute"


    ref = fields.Char(related="attribute_field_id.name")
    alt_sinir = fields.Integer(string="Filtre min deger")
    Ust_sinir = fields.Integer(string="Filtre max deger")
    delta_deger = fields.Integer(string="Filtre Artış deger")
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
            while min < max:
                alt = int(min / delta) * delta
                ust = alt + delta
                deger = str(alt) + " - " + str(ust)
                degerelr.append(deger)
                min = ust

            colors =['a','b']
            record.value_ids.unlink()
            self.env['product.attribute.value'].create([{'name': color, 'attribute_id': record.id} for color in degerelr])



