# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductRequestMismatch(models.TransientModel):
    _name = 'product.request.mismatch'

    def _compute_active_ids(self):
        active_product_ids = self._context.get('active_model') == 'product.product' and self._context.get('active_ids') or []
        return [
            (0, 0, {'product_id': product.id, 
                    'name': product.name,
                    'barcode': product.barcode,
                    'sku': product.sku,
                    'locations_before': product.locations_before,
                    'locations_after': product.locations_after,
                    'count_before': product.count_before,
                    'count_after': product.count_after,
                    'difference': product.difference,
                    })
            for product in self.env['product.product'].browse(active_product_ids)
        ]

    product_ids = fields.One2many('product.request.mismatch.product', 'wizard_id', string='Products', default=_compute_active_ids)   

    @api.multi
    def send_email(self):
        self.ensure_one()        
        print('send email')        

class ProductRequestMismatchProduct(models.TransientModel):
    _name = 'product.request.mismatch.product'

    wizard_id = fields.Many2one('product.request.mismatch', string='Wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True,)
    name = fields.Char('Name', index=True, required=True, translate=True)
    barcode = fields.Char(
        'Barcode', copy=False, oldname='ean13',
        help="International Article Number used for product identification.")
    sku = fields.Char('SKU')
    locations_before = fields.Integer('Locations Before')
    locations_after = fields.Integer('Locations After')
    count_before = fields.Integer('Count Before')
    count_after = fields.Integer('Count After')
    difference = fields.Integer('Difference')
        