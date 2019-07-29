# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    date_expected = fields.Datetime(
        'Expected Date', index=False, required=False, auto_join=False,
        states={'done': [('readonly', True)]},
        help="Scheduled date for the processing of this move", compute="_compute_date_expected")
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        auto_join=False, index=False, required=False,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.", compute="_compute_location_id")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        auto_join=False, index=False, required=False,
        help="Location where the system will stock the finished products.", compute="_compute_location_dest_id")

    @api.depends('picking_id.scheduled_date')
    def _compute_date_expected(self):
        for record in self:
            record.date_expected  = record.picking_id.scheduled_date or fields.Datetime.now(self)

    @api.depends('picking_id.custom_location_id')
    def _compute_location_id(self):
        for record in self:
            record.location_id  = record.picking_id.custom_location_id

    @api.depends('picking_id.custom_location_dest_id')
    def _compute_location_dest_id(self):
        for record in self:
            record.location_dest_id  = record.picking_id.custom_location_dest_id

    @api.multi
    @api.constrains('product_uom_qty')
    def onchange_product_uom_qty(self):
        for record in self:
            child_locations = record.location_id
            initial_demand = record.product_uom_qty
            location_product_id = record.product_id.id
            for i in child_locations:
                child_quants = i.quant_ids    
                for z in child_quants:          
                    if location_product_id == z.product_id.id:
                        if initial_demand > (z.quantity - z.reserved_quantity):
                            raise UserError('''Quantity of product that is planned to be moved can't be greater
                                                than quantity what is available in the source location.''')
            return