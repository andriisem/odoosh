# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    date_expected = fields.Datetime(
        'Expected Date', index=False, required=False, auto_join=True,
        states={'done': [('readonly', True)]},
        help="Scheduled date for the processing of this move", compute="_compute_date_expected")
    product_uom = fields.Many2one('uom.uom', 'Unit of Measure', required=True, compute="_compute_product_uom")
    reserved_availability = fields.Float(
        'Quantity Reserved', compute='_compute_reserved_availability_custom',
        digits=dp.get_precision('Product Unit of Measure'),
        readonly=True, help='Quantity that has already been reserved for this move')
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        auto_join=True, index=False, required=False, store=True,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.", compute="_compute_location_id")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        auto_join=True, index=False, required=False, store=True,
        help="Location where the system will stock the finished products.", compute="_compute_location_dest_id")

    @api.depends('picking_id.move_ids_without_package.product_uom')
    def _compute_product_uom(self):
        for record in self:
            context = self.env.context
            product_uom_id = context.get('default_product_uom_id')
            if isinstance(product_uom_id, int):
                record.product_uom  = self.env['uom.uom'].search([('id', '=', product_uom_id)])

    @api.depends('picking_id.move_ids_without_package.reserved_availability')
    def _compute_reserved_availability_custom(self):
        for record in self:
            context = self.env.context
            product_reserved_availability = context.get('default_reserved_availability')
            if isinstance(product_reserved_availability, int):
                record.reserved_availability  = product_reserved_availability

    @api.depends('picking_id.date_expected')
    def _compute_date_expected(self):
        for record in self:
            record.date_expected  = record.picking_id.date_expected or fields.Datetime.now(self)

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
            product_name = record.name.replace('New Move:', '')
            for i in child_locations:
                child_quants = i.quant_ids    
                for z in child_quants:
                    if product_name == z.product_id.display_name:
                        if initial_demand > (z.quantity - z.reserved_quantity):
                            raise UserError('''Quantity of product that is planned to be moved can't be greater
                                                than quantity what is available on hand and reserved in the source location.''')
            return

    @api.multi
    def write(self, values):        
        context = self.env.context        
        move_state = context.get('default_state')
        product_id = context.get('default_product_id')
        if 'product_id' not in values:
            values['product_id'] = product_id
        if 'state' not in values:
            values['state'] = move_state
        res = super(StockMove, self).write(values)
        return res