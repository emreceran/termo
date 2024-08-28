# -*- coding: utf-8 -*-
import time
import logging
from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError, AccessError
import json


_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = "product.template"


    yuzey = fields.Float(string = "Yüzey", default = 0, store=True)
    boru_hacmi = fields.Float(string = "Boru Hacmi", default = 0, store=True)
    fan_adet = fields.Integer(string="Fan Adeti", default=0, store=True)
    fan_cap = fields.Integer(string="Fan Çapı", default=0, store=True)

    product_top_type = fields.Selection([
        ('e', 'Evaporatör'),
        ('k', 'Kondanser'),
        ('v', 'Vitrin Evaporatör'),
        ('o', 'Özel Ürün')
    ], string="Ürün Üst Tipi")

    #EVAPOATÖR FİELDS
    t1 = fields.Float(string = "To / Te -35°C/-40°C W", default=None)
    t2 = fields.Float(string = "To / Te -40°C/-45°C W", default = 0, store=True)
    sc1 = fields.Float(string = "SC1 10°C/0°C W", default = 0, store=True)
    sc2 = fields.Float(string = "SC2 0°C/- 8°C W", default = 0, store=True)
    sc3 = fields.Float(string = "SC3 - 18°C/ - 25°C W", default = 0, store=True)
    sc4 = fields.Float(string = "SC4 - 25°C/ - 31°C W", default = 0, store=True)
    rezidans_t1 = fields.Char(string="REzidans T1 Batarya Coil")
    rezidans_t2_batarya = fields.Char(string="REzidans T2 Batarya Coil")
    rezidans_t2_tava = fields.Char(string="REzidans T2 Tva Drip Tray")
    hava_debisi = fields.Float(string = "Hava Debisi m³/h", default = 0, store=True)

    #KONDENSER FİELDS
    kapasite_yuksek_devir = fields.Float(string="Kapasite YÜKSEK DEVİR(H) ", default=0, store=True)
    kapasite_dusuk_devir = fields.Float(string="KapasiteDÜŞÜK DEVİR (L) ", default=0, store=True)
    hava_debisi_yuksek_devir = fields.Float(string="YÜKSEK DEVİR HAVA DEBİSİ m3/h", default=0, store=True)
    hava_debisi_dusuk_devir = fields.Float(string="Düşük DEVİR HAVA DEBİSİ m3/h", default=0, store=True)
    kondenser_giris_cap = fields.Char(string="KONDENSER  GİRİŞ  KOLLEKTÖR  ÇAPI mm / inc")
    kondenser_cikis_cap = fields.Char(string="KONDENSER  ÇIKIŞ KOLLEKTÖR  ÇAPI mm / inc")


    #ORTAK FİELDS
    H = fields.Integer(string = "H", default = 0, store=True)
    L = fields.Integer(string = "L", default = 0, store=True)
    W = fields.Integer(string = "W", default = 0, store=True)
    H1 = fields.Integer(string = "H1", default = 0, store=True)
    H2 = fields.Integer(string = "H2", default = 0, store=True)
    L1 = fields.Integer(string = "L1", default = 0, store=True)
    W1 = fields.Integer(string = "W1", default = 0, store=True)
    W2 = fields.Integer(string = "W2", default = 0, store=True)
    W3 = fields.Integer(string = "W3", default = 0, store=True)
    LA = fields.Integer(string = "LA", default = 0, store=True)

    lamel_aralik= fields.Float(string = "Lamel Aralığı", default = 4, store=True)
    hatve= fields.Float(string = "Hatve ", default = 6, store=True)
    kapasite = fields.Integer(string = "Kapasite ", default = 6, store=True)
    sutluk_uzunluk = fields.Char(string="Sütlük Uzunluk")
    yan_uzunluk = fields.Char(string="Yan Uzunluk")
    boru_sayisi = fields.Char(string="Boru Sayısı")
    sutluk_tip = fields.Char(string = "Sütlük Tipi")
    sutluk_geometri = fields.Char(string = "Sütlük Geometri")


    termo_tip_id = fields.Many2one('termo.tip', string="Ürün Tipi")
    termo_seri_id = fields.Many2one('termo.seri', string="Ürün Serisi")
    termo_filtre =fields.Many2many(related="termo_tip_id.filtre")
    public_categ_ids =fields.Many2many(related="termo_tip_id.public")
    filtre_grubu_id =fields.Many2one(related="termo_tip_id.filtre_grubu_id")
    image_1920 =fields.Image(related="termo_tip_id.gorsel")
    image_128 =fields.Image(related="termo_tip_id.gorsel")

    oda_sicakligi = fields.Integer(string = "Oda Sıcaklığı ", compute="_value_pc", default = 6, store=True)
    evaporasyon_sicakligi = fields.Integer(string = "Evaporasyon Sıcaklığı ", compute="_value_pc", default = 6, store=True)

    precomputed_values = fields.Text(string="Precomputed Values")
    website_parent_categ = fields.Char(string = "Ürün Üst Kategorisi ", compute="_compute_parent_categ", store=True )

    termo_group = fields.Char(string="Termo Grup", compute="_compute_termo_group", store=True)

    @api.depends('termo_tip_id.grup')
    def _compute_termo_group(self):
        for record in self:
            if record.termo_tip_id.grup in ['1', '2', '3']:
                record.termo_group = 'Evaporator'
            elif record.termo_tip_id.grup in ['4', '5']:
                record.termo_group = 'Kondenser'
            else:
                record.termo_group = 'Vitrin'


    def _get_suitable_image_size(self, columns, x_size, y_size):
        if x_size == 1 and y_size == 1 and columns >= 3:
            return 'image_512'
        return 'image_1024'

    @api.depends('public_categ_ids')
    def _compute_parent_categ(self):
        for record in self:
            liste = [record.public_categ_ids][0]
            if liste.parent_id:
                record.website_parent_categ = liste.parent_id.name
            else:
                record.website_parent_categ = liste.name


    def write_precomputed_values(self):
        for record in self:
            a = record.termo_filtre
            precomputed_values = { }
            for attrib in a:
                referans = attrib.ref  # atribute reeras
                urun_sc1_degeri = getattr(record, referans)
                if urun_sc1_degeri == attrib.bos_deger:
                    deger = False
                    precomputed_values.update({attrib.ref: [deger]})
                else:
                    if attrib.att_type == "aralik":
                        alt = int(urun_sc1_degeri - (urun_sc1_degeri % attrib.delta_deger))
                        ust = int(alt + attrib.delta_deger)
                        deger = str(alt) + " - " + str(ust)
                    else:
                        deger = str(urun_sc1_degeri)

                    precomputed_values.update({attrib.ref: [deger]})
            record.precomputed_values = json.dumps(precomputed_values)
            print(record.precomputed_values)

    def clear_existing_variants(self):
        for record in self:
            # Önce product_variant_combination kayıtlarını sil
            combination_delete_query = """
                DELETE FROM product_variant_combination 
                WHERE product_template_attribute_value_id IN (
                    SELECT ptav.id 
                    FROM product_template_attribute_value ptav
                    JOIN product_template_attribute_line ptal ON ptav.attribute_line_id = ptal.id
                    WHERE ptal.product_tmpl_id = %s
                )
            """
            self.env.cr.execute(combination_delete_query, (record.id,))

            # Sonra product_template_attribute_value kayıtlarını sil
            value_delete_query = """
                DELETE FROM product_template_attribute_value 
                WHERE attribute_line_id IN (
                    SELECT id FROM product_template_attribute_line 
                    WHERE product_tmpl_id = %s
                )
            """
            self.env.cr.execute(value_delete_query, (record.id,))

            # Son olarak product_template_attribute_line kayıtlarını sil
            line_delete_query = """
                DELETE FROM product_template_attribute_line 
                WHERE product_tmpl_id = %s
            """
            self.env.cr.execute(line_delete_query, (record.id,))

            self.env.cr.commit()

    def update_precomputed_values(self):
        for record in self:
            attribute_lines_to_create = []
            attribute_values_cache = {}
            product_tmpl_id = record.id

            if record.precomputed_values:
                precomputed_values = json.loads(record.precomputed_values)
                termo_filtre_attributes = record.termo_filtre

                for attrib in termo_filtre_attributes:
                    referans = attrib.ref  # attribute referansı
                    urun_field_degeri = getattr(record, referans)

                    urun_filtre_degeri = precomputed_values.get(referans, [None])[0]
                    print(referans, urun_field_degeri, urun_filtre_degeri)

                    if urun_field_degeri != attrib.bos_deger:
                        # Cache'de attribute value kontrolü
                        if (attrib.id, urun_filtre_degeri) in attribute_values_cache:
                            deger = attribute_values_cache[(attrib.id, urun_filtre_degeri)]
                        else:
                            deger = self.env['product.attribute.value'].search(
                                [('name', '=', urun_filtre_degeri), ('attribute_id', '=', attrib.id)], limit=1)
                            attribute_values_cache[(attrib.id, urun_filtre_degeri)] = deger

                        if deger:
                            attribute_lines_to_create.append((product_tmpl_id, attrib.id, deger.id))
                        else:
                            raise UserError(
                                _('Değiştirmeye çalıştığınız %s ürününün %s alanında yer alan %s değeri geçersiz. Kontrol ediniz ya da filtre değerlerine ekleyiniz.') % (
                                    record.name, referans, urun_field_degeri))

            # Mevcut product_variant_combination kayıtlarını silme
            self._cr.execute("""
                DELETE FROM product_variant_combination WHERE product_product_id IN (
                    SELECT id FROM product_product WHERE product_tmpl_id = %s
                )
            """, (product_tmpl_id,))

            # Mevcut product_product kayıtlarını silme
            self._cr.execute("""
                DELETE FROM product_product WHERE product_tmpl_id = %s
            """, (product_tmpl_id,))

            # Mevcut attribute line ve attribute value kayıtlarını temizleme
            self._cr.execute("""
                DELETE FROM product_attribute_value_product_template_attribute_line_rel
                WHERE product_template_attribute_line_id IN (
                    SELECT id FROM product_template_attribute_line WHERE product_tmpl_id = %s
                )
            """, (product_tmpl_id,))
            self._cr.execute("""
                DELETE FROM product_template_attribute_line WHERE product_tmpl_id = %s
            """, (product_tmpl_id,))

            # SQL ile attribute_line ve attribute_value kayıtlarını ekleme
            for pt_id, attr_id, val_id in attribute_lines_to_create:
                # Yeni attribute line oluşturma
                self._cr.execute("""
                    INSERT INTO product_template_attribute_line (product_tmpl_id, attribute_id)
                    VALUES (%s, %s) RETURNING id
                """, (pt_id, attr_id))
                new_line_id = self._cr.fetchone()[0]
                relation_table = 'product_attribute_value_product_template_attribute_line_rel'
                self._cr.execute(f"""
                    INSERT INTO {relation_table} (product_template_attribute_line_id, product_attribute_value_id)
                    VALUES (%s, %s)
                """, (new_line_id, val_id))
                print(f"Created new attribute line: {new_line_id}, value: {val_id}")

            # Product.product varyantlarını ORM ile oluşturma
            product_variant_obj = self.env['product.product']
            for pt_id, attr_id, val_id in attribute_lines_to_create:
                product_variant_obj.create({
                    'product_tmpl_id': pt_id,
                    'product_template_attribute_value_ids': [(6, 0, [val_id])]
                })
                print(f"Created product variant for product_tmpl_id: {pt_id} with attribute_value_ids: {val_id}")

            # Veritabanı işlemlerini commit etmek
            self._cr.commit()

            # Cache temizliği ve flush işlemleri
            self.clear_and_reload_cache()
            self.env['product.template.attribute.line'].flush()
            self.env['product.template'].flush()
            self.env['product.attribute.value'].flush()
            self.env['product.product'].flush()
            self.invalidate_cache()

            # Ürünü yeniden yükleme
            self.browse(product_tmpl_id).read()



    def read_precomputed_values(self):
        for record in self:
            precomputed_values = {}
            attribute_lines_to_create = []
            attribute_values_cache = {}
            value_lines_to_create = []

            product_tmpl_id = record.id
            if record.precomputed_values:
                precomputed_values = json.loads(record.precomputed_values)
                termo_filtre_attributes = record.termo_filtre

                for attrib in termo_filtre_attributes:
                    referans = attrib.ref  # attribute referansı
                    urun_field_degeri = getattr(record, referans)

                    urun_filtre_degeri = precomputed_values.get(referans, [None])[0]
                    print(referans, urun_field_degeri, urun_filtre_degeri)

                    if urun_field_degeri != attrib.bos_deger:
                        # Cache'de attribute value kontrolü
                        if (attrib.id, urun_filtre_degeri) in attribute_values_cache:
                            deger = attribute_values_cache[(attrib.id, urun_filtre_degeri)]
                        else:
                            deger = self.env['product.attribute.value'].search(
                                [('name', '=', urun_filtre_degeri), ('attribute_id', '=', attrib.id)], limit=1)
                            attribute_values_cache[(attrib.id, urun_filtre_degeri)] = deger

                        if deger:
                            attribute_lines_to_create.append((product_tmpl_id, attrib.id, deger.id))
                        else:
                            raise UserError(
                                _('Değiştirmeye çalıştığınız %s ürününün %s alanında yer alan %s değeri geçersiz. Kontrol ediniz ya da filtre değerlerine ekleyiniz.') % (
                                    record.name, referans, urun_field_degeri))

            # ORM ile attribute_line ve attribute_value kayıtlarını ekleme
            if attribute_lines_to_create:
                self.env['product.template.attribute.line'].create([
                    {
                        'product_tmpl_id': pt_id,
                        'attribute_id': attr_id,
                        'value_ids': [(4, val_id)],
                    }
                    for pt_id, attr_id, val_id in attribute_lines_to_create
                ])

    def check_precomputed_values(self):
        attribute_lines_to_create = []
        attribute_values_cache = {}

        for record in self:
            precomputed_values = json.loads(record.precomputed_values)
            termo_filtre_attributes = record.termo_filtre

            product_tmpl_id = record.id

            for attrib in termo_filtre_attributes:
                referans = attrib.ref  # attribute referansı
                urun_field_degeri = getattr(record, referans)
                urun_filtre_degeri = precomputed_values.get(referans, [None])[0]

                if urun_field_degeri != attrib.bos_deger:
                    # Cache'de attribute value kontrolü
                    if (attrib.id, urun_filtre_degeri) in attribute_values_cache:
                        deger = attribute_values_cache[(attrib.id, urun_filtre_degeri)]
                    else:
                        deger = self.env['product.attribute.value'].search(
                            [('name', '=', urun_filtre_degeri), ('attribute_id', '=', attrib.id)], limit=1)
                        attribute_values_cache[(attrib.id, urun_filtre_degeri)] = deger

                    if not deger:
                        raise UserError(
                            _('Değiştirmeye çalıştığınız %s ürününün %s alanında yer alan %s değeri geçersiz. Kontrol ediniz ya da filtre değerlerine ekleyiniz.') % (
                                record.name, referans, urun_field_degeri))

                    attribute_lines_to_create.append((product_tmpl_id, attrib.id, deger.id))

        return attribute_lines_to_create

    def direct_write_precomputed_values(self):
        attribute_lines_to_create = self.check_precomputed_values()

        if attribute_lines_to_create:
            self.env['product.template.attribute.line'].create([
                {
                    'product_tmpl_id': pt_id,
                    'attribute_id': attr_id,
                    'value_ids': [(4, val_id)],
                }
                for pt_id, attr_id, val_id in attribute_lines_to_create
            ])


    # @api.onchange('termo_tip_id')
    # @api.depends('termo_tip_id')
    def onchange_termo_tip_id(self):
        for record in self:
            record.image_1920 = record.termo_tip_id.gorsel

    # def _get_image_holder(self):
    # #     """Returns the holder of the image to use as default representation.
    # #     If the product template has an image it is the product template,
    # #     otherwise if the product has variants it is the first variant
    # #
    # #     :return: this product template or the first product variant
    # #     :rtype: recordset of 'product.template' or recordset of 'product.product'
    # #     """
    # #     # self.ensure_one()
    # #     # if self.termo_tip_id.gorsel:
    # #     #     print("asasa")
    # #     #     return self.termo_tip_id.gorsel
    # #     # variant = self.env['product.product'].browse(self._get_first_possible_variant_id())
    # #     # # if the variant has no image anyway, spare some queries by using template
    # #     # return variant if variant.image_variant_128 else self
    # #
    #     for record in self:
    #         if record.termo_tip_id:
    #             return record.termo_tip_id.gorsel


    def _get_images(self):
        """Return a list of records implementing `image.mixin` to
        display on the carousel on the website for this template.

        This returns a list and not a recordset because the records might be
        from different models (template and image).

        It contains in this order: the main image of the template and the
        Template Extra Images.
        """
        self.ensure_one()
        # iamges=[]
        # for record in self:
        #     iamges.append(record.termo_tip_id.gorsel)

        return [self] + list(self.product_template_image_ids)


    @api.depends('hatve', 'sc2', 'sc3', 'sc4')
    def _value_pc(self):
        for record in self:
            if record.hatve == 6:
                record.kapasite = record.sc2
                record.oda_sicakligi = 0
                record.evaporasyon_sicakligi = -8
            elif record.hatve == 8:
                record.kapasite = record.sc3
                record.oda_sicakligi = -18
                record.evaporasyon_sicakligi = 25
            elif record.hatve == 10:
                record.kapasite = record.sc4
                record.oda_sicakligi = -18
                record.evaporasyon_sicakligi = 25
            elif record.hatve == 4:
                record.kapasite = record.sc1
                record.oda_sicakligi = 0
                record.evaporasyon_sicakligi = -8

