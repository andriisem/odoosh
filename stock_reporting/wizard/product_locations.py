# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductLocationsBefore(models.TransientModel):
    _name = 'product.locations.before'

    def _compute_active_ids(self):
        active_product_id = self._context.get('active_model') == 'product.product' and self._context.get('active_ids') or []
        product = self.env['product.product'].browse(active_product_id)
        stock_quant_ids = product.with_context({'to_date': product.before_counting}).stock_quant_ids
        qty_available = product.with_context({'to_date': product.before_counting}).qty_available
        return [
            (0, 0, {'name': product.name,
                    'location_id': quant.id,
                    'complete_name': quant.location_id.complete_name,
                    'quantity': quant.quantity,
                    })
            for quant in stock_quant_ids if (quant.location_id.usage == 'internal' and quant.quantity > 0 and qty_available > 0)
        ]

    location_ids = fields.One2many('product.locations.detail.before', 'wizard_id', string='Locations', default=_compute_active_ids)   


class ProductLocationsDetailBefore(models.TransientModel):
    _name = 'product.locations.detail.before'

    wizard_id = fields.Many2one('product.locations.before', string='Wizard', readonly=True,)
    name = fields.Char('Name', index=True, required=True, translate=True)
    location_id = fields.Many2one(
        'stock.location', 'Location',
        auto_join=True, ondelete='restrict', readonly=True, required=True)
    complete_name = fields.Char("Full Location Name", readonly=True,)
    quantity = fields.Float(
        'Quantity',
        help='Quantity of products in this quant, in the default unit of measure of the product',
        readonly=True, required=True, oldname='qty')


class ProductLocationsAfter(models.TransientModel):
    _name = 'product.locations.after'

    def _compute_active_ids(self):
        active_product_id = self._context.get('active_model') == 'product.product' and self._context.get('active_ids') or []
        product = self.env['product.product'].browse(active_product_id)
        stock_quant_ids = product.with_context({'to_date': product.counting_day}).stock_quant_ids
        qty_available = product.with_context({'to_date': product.counting_day}).qty_available
        return [
            (0, 0, {'name': product.name,
                    'location_id': quant.id,
                    'complete_name': quant.location_id.complete_name,
                    'quantity': quant.quantity,
                    })
            for quant in stock_quant_ids if (quant.location_id.usage == 'internal' and quant.quantity > 0 and qty_available > 0)
        ]

    location_ids = fields.One2many('product.locations.detail.after', 'wizard_id', string='Locations', default=_compute_active_ids)   


class ProductLocationsDetailAfter(models.TransientModel):
    _name = 'product.locations.detail.after'

    wizard_id = fields.Many2one('product.locations.after', string='Wizard', readonly=True,)
    name = fields.Char('Name', index=True, required=True, translate=True)
    location_id = fields.Many2one(
        'stock.location', 'Location',
        auto_join=True, ondelete='restrict', readonly=True, required=True)
    complete_name = fields.Char("Full Location Name", readonly=True,)
    quantity = fields.Float(
        'Quantity',
        help='Quantity of products in this quant, in the default unit of measure of the product',
        readonly=True, required=True, oldname='qty')
        