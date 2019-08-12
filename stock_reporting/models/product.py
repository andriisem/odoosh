# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _

class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "difference desc"

    locations_before = fields.Integer('Locations Before', compute="_compute_locations_before", help='''Number of locations in the selected warehouse where this product existed in at the "compare to date"''')
    locations_after = fields.Integer('Locations After', compute="_compute_locations_after", help='''Number of locations in the selected warehouse where this product existed in at the "inventory date"''')
    count_before = fields.Integer('Count Before', compute="_compute_count_before", help='''The total of all the units of the products in all of the locations on the "compare to date"''')
    count_after = fields.Integer('Count After', compute="_compute_count_after", help='''The total of of all the units of the product in all of the locations on the "inventory date"''')
    difference = fields.Integer('Difference', compute="_compute_difference", help='''Count After minus Count Before''')

    @api.depends('count_before', 'count_after')
    def _compute_difference(self):
        for record in self:      
            record.difference  = record.count_after - record.count_before

    def _compute_locations_before(self):
        context = self.env.context
        before_counting = datetime.strptime(context.get('before_counting'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            stock_quant_ids = record.with_context({'to_date': before_counting}).stock_quant_ids            
            if len(stock_quant_ids) == 0:
                record.locations_before = 0
            else:
                locations_list = []
                for i in stock_quant_ids:
                    if i.location_id.usage == 'internal':
                        locations_list.append(i.location_id)
                record.locations_before = len(set(locations_list))

    def _compute_locations_after(self):
        context = self.env.context
        counting_day = datetime.strptime(context.get('counting_day'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            stock_quant_ids = record.with_context({'to_date': counting_day}).stock_quant_ids            
            if len(stock_quant_ids) == 0:
                record.locations_after = 0
            else:
                locations_list = []
                for i in stock_quant_ids:
                    if i.location_id.usage == 'internal':
                        locations_list.append(i.location_id)
                record.locations_after = len(set(locations_list))

    def _compute_count_before(self):
        context = self.env.context
        before_counting = datetime.strptime(context.get('before_counting'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            record.count_before = record.with_context({'to_date': before_counting}).qty_available

    def _compute_count_after(self):
        context = self.env.context
        counting_day = datetime.strptime(context.get('counting_day'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            record.count_after = record.with_context({'to_date': counting_day}).qty_available

    def action_show_locations_before(self):
        self.ensure_one()
        context = dict(self.env.context)
        before_counting = datetime.strptime(context.get('before_counting'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            product_id = record.with_context({'to_date': before_counting})
        self.env['stock.quant']._merge_quants()
        self.env['stock.quant']._unlink_zero_quants()
        action = self.env.ref('stock.quantsact').read()[0]
        action['limit'] = 1
        action['domain'] = [('product_id', '=', product_id.id)]
        return action
        
    def action_show_locations_after(self):
        self.ensure_one()
        context = dict(self.env.context)
        counting_day = datetime.strptime(context.get('counting_day'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            product_id = record.with_context({'to_date': counting_day})
        self.env['stock.quant']._merge_quants()
        self.env['stock.quant']._unlink_zero_quants()
        action = self.env.ref('stock.quantsact').read()[0]
        action['limit'] = 1
        action['domain'] = [('product_id', '=', product_id.id)]
        return action