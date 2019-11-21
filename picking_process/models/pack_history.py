# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class PackHistory(models.Model):
    _name = 'pack.history'
    _description = 'Pack History'
    _rec_name = 'order_id'

    order_id = fields.Many2one('sale.order', string='Order')
    move_ids = fields.One2many('pack.history.move', 'history_id', string='Move')


class PackHistoryMove(models.Model):
    _name = 'pack.history.move'
    _description = 'Pack History'

    pick_location_id = fields.Many2one('stock.location', string='Pick Location')
    from_location_id = fields.Many2one('stock.location', string='From Location')
    product_id = fields.Many2one('product.product', string='Product')
    qty = fields.Float(string='Qty')
    history_id = fields.Many2one('pack.history', string='History')
