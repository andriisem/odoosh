# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
# from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    @api.onchange('product_uom_qty')
    # @api.constrains('product_uom_qty')
    def onchange_product_uom_qty(self):
        for record in self:
            location = record.location_id
            initial_demand = record.product_uom_qty
            location_product_id = record.product_id.id
            for i in location:
                child_quants = i.quant_ids    
                for z in child_quants:                    
                    if location_product_id == z.product_id.id:                  
                        if initial_demand > z.quantity:
                            message = _('''Quantity of product that is planned to be moved can't be greater
                                            than quantity what is available and reserved in the source location.''')
                            mess= {
                                    'title': _('Are you sure?'),
                                    'message' : message
                                    }
                            # raise UserError('''Quantity of product that is planned to be moved can't be greater
                            #                     than quantity what is available and reserved in the source location.''')
                            return {'warning': mess}
                        else:
                            return