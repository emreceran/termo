from odoo import models, api
import logging

_logger = logging.getLogger(__name__)

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    @api.model
    def create_attribute_line_and_value(self, product_tmpl_id, attribute_id, attribute_value_id):
        # Adım 1: product_template_attribute_line tablosuna kayıt ekleme
        self.env.cr.execute("""
            INSERT INTO product_template_attribute_line (product_tmpl_id, attribute_id, value_count, create_uid, create_date, write_uid, write_date)
            VALUES (%s, %s, 1, %s, NOW(), %s, NOW())
            RETURNING id;
        """, (product_tmpl_id, attribute_id, self.env.uid, self.env.uid))
        attribute_line_id = self.env.cr.fetchone()[0]

        _logger.info('Inserted into product_template_attribute_line: %s', attribute_line_id)

        # Adım 2: product_template_attribute_value tablosuna kayıt ekleme
        self.env.cr.execute("""
            INSERT INTO product_template_attribute_value (attribute_line_id, product_attribute_value_id, create_uid, create_date, write_uid, write_date)
            VALUES (%s, %s, %s, NOW(), %s, NOW());
        """, (attribute_line_id, attribute_value_id, self.env.uid, self.env.uid))

        _logger.info('Inserted into product_template_attribute_value: attribute_line_id=%s, product_attribute_value_id=%s', attribute_line_id, attribute_value_id)

        return {
            'status': 'success',
            'attribute_line_id': attribute_line_id,
            'product_attribute_value_id': attribute_value_id
        }
