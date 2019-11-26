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
    state = fields.Selection([
        ('draft', 'Draft'),
        ('done', 'Done'),
    ], string='Status', default='draft')
    pick_location_id = fields.Many2one('stock.location', string='Pick Location')


class PackHistoryMove(models.Model):
    _name = 'pack.history.move'
    _description = 'Pack History'
    _order = "sequence asc"

    pick_location_id = fields.Many2one('stock.location', string='Pick Location')
    from_location_id = fields.Many2one('stock.location', string='From Location')
    product_id = fields.Many2one('product.product', string='Product')
    qty_needed = fields.Float(string='Quantity Needed') 
    qty_available = fields.Float(string='Quantity Available')
    qty_done = fields.Float(string='Quantity Done')
    history_id = fields.Many2one('pack.history', string='History')
    state = fields.Selection([
        ('draft', 'Draft'),
        ('not_available', 'Not Available'),
        ('done', 'Done'),
        ], string='Status')
    sequence = fields.Integer('Sequence', default=100)

