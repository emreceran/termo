# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError, AccessError




class ProductTemplate(models.Model):
    _inherit = "product.template"


    yuzey = fields.Float(string = "Yüzey", default = 0, store=True)
    boru_hacmi = fields.Float(string = "Boru Hacmi", default = 0, store=True)
    fan_adet = fields.Integer(string="Fan Adeti", default=0, store=True)
    fan_cap = fields.Integer(string="Fan Çapı", default=0, store=True)

    #EVAPOATÖR FİELDS
    t1 = fields.Integer (string = "To / Te -35°C/-40°C W", default=None)
    t2 = fields.Integer (string = "To / Te -40°C/-45°C W", default = 0, store=True)
    sc1 = fields.Integer (string = "SC1 10°C/0°C W", default = 0, store=True)
    sc2 = fields.Float (string = "SC2 0°C/- 8°C W", default = 0, store=True)
    sc3 = fields.Integer (string = "SC3 - 18°C/ - 25°C W", default = 0, store=True)
    sc4 = fields.Integer (string = "SC4 - 25°C/ - 31°C W", default = 0, store=True)
    rezidans_t1 = fields.Char(string="REzidans T1 Batarya Coil")
    rezidans_t2_batarya = fields.Char(string="REzidans T2 Batarya Coil")
    rezidans_t2_tava = fields.Char(string="REzidans T2 Tva Drip Tray")
    hava_debisi = fields.Integer(string = "Hava Debisi m³/h", default = 0, store=True)

    #KONDENSER FİELDS
    kapasiteyuksek_devir = fields.Float(string="Kapasite YÜKSEK DEVİR(H) ", default=0, store=True)
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

    lamel_aralik= fields.Integer(string = "Lamel Aralığı", default = 4, store=True)
    hatve= fields.Integer(string = "Hatve ", default = 6, store=True)
    kapasite = fields.Integer(string = "Kapasite ", default = 6, store=True)


    termo_tip_id = fields.Many2one('termo.tip', string="Ürün Tipi")
    termo_filtre =fields.Many2many(related="termo_tip_id.filtre")
    public_categ_ids =fields.Many2many(related="termo_tip_id.public")
    # image_1920 =fields.Binary(related="termo_tip_id.gorsel")

    oda_sicakligi = fields.Float(string = "Oda Sıcaklığı ", compute="_value_pc", default = 6, store=True)
    evaporasyon_sicakligi = fields.Float(string = "Evaporasyon Sıcaklığı ", compute="_value_pc", default = 6, store=True)

    # @api.onchange('termo_tip_id')
    @api.depends('termo_tip_id')
    def onchange_termo_tip_id(self):
        for record in self:
            if record.termo_tip_id:
                if record.termo_tip_id.gorsel:
                    record.image_1920 = record.termo_tip_id.gorsel

                # if record.termo_tip_id.public:
                #     record.public_categ_ids = [(6, 0, [record.termo_tip_id.public.id])]
                # if record.termo_tip_id.filtre:
                #     record.termo_filtre = [(6, 0, [x.id for x in record.termo_tip_id.filtre])]


    # def onchange_termo_tip_id(self):
    #     for product in self:
    #         if product.termo_tip_id and product.termo_tip_id.gorsel and product.termo_tip_id.filtre_grubu_id:
    #             product.image_1920 = product.termo_tip_id.gorsel
    #             product.public_categ_ids = [(4, product.termo_tip_id.public)]
    #             product.termo_filtre = [(4, product.termo_tip_id.filtre)]

    # def write(self, vals):
    #     res = super(ProductTemplate, self).write(vals)
    #     if 'termo_tip_id' in vals:  # Eğer termo_tip_id alanı değiştirildiyse
    #         for product in self:
    #             if product.termo_tip_id:  # Eğer yeni bir termo tipi atanmışsa
    #                 product.image_1920 = product.termo_tip_id.gorsel
    #                 product.public_categ_ids = product.termo_tip_id.public
    #
    #             else:  # Eğer termo tipi kaldırılmışsa, varsayılan değerler atanabilir veya boş bırakılabilir.
    #                 pass  # İlgili işlemi burada yapabilirsiniz, eğer gerekiyorsa
    #     return res

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


    def gorev(self):
        for record in self:

            print(record.name)
            a =record.termo_filtre #üründeki filtreler

            for attrib in a: #filtre isimleri loop ör sc1_aralik


                self.env['product.template.attribute.line'].search(
                    [('product_tmpl_id', '=', record.id), ('attribute_id', '=', attrib.id)]).unlink()
                referans = attrib.ref #atribute reeras
                print(referans)
                urun_sc1_degeri = getattr(record, referans)
                urun_filtre_degeri = False
                print([urun_sc1_degeri, attrib.delta_deger])

                alt = int(urun_sc1_degeri - (urun_sc1_degeri % attrib.delta_deger))
                ust = int(alt + attrib.delta_deger)
                urun_filtre_degeri = str(alt) + " - " + str(ust)

                print(urun_filtre_degeri)

                attrib_value = attrib.value_ids
                print([x.name for x in attrib_value])
                deger = [x for x in attrib_value if x.name == urun_filtre_degeri][0]


                if deger:
                    self.env['product.template.attribute.line'].create({'product_tmpl_id': record.id,
                                                                        'attribute_id': attrib.id,
                                                                        'value_ids': [(4, deger.id)],
                                                                        })
                else:
                    raise UserError(
                        'Değiştirmye çalıştığınız %s ürününün %s filtresinde yer alan  %s  değeri geçersiz. Kontrol ediniz yada filtre değerlerine ekleyiniz.' % ( record.name, attrib.name, deger))

                # variant = self.env['product.attribute.value'].search(
                #     [('attribute_id', '=', attr_id.id), ('name', '=', sc1_aralik_deger,)])
                #
                # if variant:
                #     self.env['product.template.attribute.line'].create({'product_tmpl_id': record.id,
                #                                                         'attribute_id': attr_id.id,
                #                                                         'value_ids': [(4, variant.id)],
                #                                                         })
                # else:
                #     raise UserError(
                #         'Değiştirmye çalıştığınız %s ürününün %s filtresinde yer alan  %s  değeri geçersiz. Kontrol ediniz yada filtre değerlerine ekleyiniz.' % (
                #         record.name, attrib_name, sc1_aralik_deger))



    def tum_gorev(self):
        raise UserError(self.termo_tip_id)

        # tum_urunler = self.env['product.template'].search([])
        # for record in tum_urunler:
        #     if record.termo_tip_id != False:
        #         record.gorev()


    def gorev2(self):

        attr_id = self.env['product.attribute'].search([('name', '=', 'sc1_aralik')])
        values = self.env['product.attribute.value'].search([('attribute_id', '=', attr_id.id)])
        value_names =   [x.name for x in values]
        value_names =   [x.name for x in values if x.name=="0 - 5000"][0]
        for record in self:
            sc1_aralik = str(record.sc1_aralik)

        prints =  value_names == sc1_aralik
        print(value_names)
        print(sc1_aralik)

        raise UserError(prints)

        attrib_name = "sc1_aralik"
        attr_id = self.env['product.attribute'].search([('name', '=', attrib_name)])
        self.env['product.template.attribute.line'].search(
            [('product_tmpl_id', '=', record.id), ('attribute_id', '=', 93)]).unlink()


    def gorev3(self):
        a = self.termo_filtre
        attribs = [x.name for x in a]
        for i in attribs:

            attrib_name = i
            attr_id = self.env['product.attribute'].search([('name', '=', attrib_name)])

            for record in self:

                self.env['product.template.attribute.line'].search([('product_tmpl_id', '=', record.id), ('attribute_id', '=', attr_id.id)]).unlink()
                sc1_aralik_deger = getattr(record, attrib_name)

                if sc1_aralik_deger:
                    variant = self.env['product.attribute.value'].search([('attribute_id', '=', attr_id.id), ('name', '=', sc1_aralik_deger,)])

                    if variant:
                        self.env['product.template.attribute.line'].create({'product_tmpl_id': record.id,
                                                                            'attribute_id': attr_id.id,
                                                                            'value_ids': [(4, variant.id)],
                                                                            })
                    else:
                        raise UserError('Değiştirmye çalıştığınız %s ürününün %s filtresinde yer alan  %s  değeri geçersiz. Kontrol ediniz yada filtre değerlerine ekleyiniz.' % (record.name, attrib_name, sc1_aralik_deger))


        # for record in self:
        #     self.env['product.template.attribute.line'].search(
        #     [('product_tmpl_id', '=', record.id), ('attribute_id', '=', attr_id.id)]).unlink()



