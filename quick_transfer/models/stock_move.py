# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    @api.constrains('product_uom_qty')
    def onchange_product_uom_qty(self):
        for record in self:
            child_locations = record.location_id.child_ids
            initial_demand = record.product_uom_qty
            location_product_id = record.product_id.id
            for i in child_locations:
                child_quants = i.quant_ids    
                for z in child_quants:                    
                    if location_product_id == z.product_id.id:                  
                        if initial_demand > z.quantity:
                            raise UserError('''Quantity of product that is planned to be moved can't be greater
                                                than quantity what is available in the source location.''')
            return