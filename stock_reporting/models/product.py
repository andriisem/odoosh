# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class ProductProduct(models.Model):
    _inherit = "product.product"
    _order = "difference asc"

    locations_before = fields.Integer('Locations Before', compute="_compute_locations_before", help='''Number of locations in the selected warehouse where this product existed in at the "compare to date"''')
    locations_after = fields.Integer('Locations After', compute="_compute_locations_after", help='''Number of locations in the selected warehouse where this product existed in at the "inventory date"''')
    count_before = fields.Integer('Count Before', compute="_compute_count_before", help='''The total of all the units of the products in all of the locations on the "compare to date"''')
    count_after = fields.Integer('Count After', compute="_compute_count_after", help='''The total of of all the units of the product in all of the locations on the "inventory date"''')
    difference = fields.Integer('Difference', help='''Count After minus Count Before''', default=0, store=True)
    counting_day = fields.Datetime('Counting Day', help="Choose a date to get the inventory at that date", default=fields.Datetime.now, store=True)
    before_counting = fields.Datetime('Before Counting', help="Choose a date to get the inventory at that date", default=fields.Datetime.now, store=True)

    def _compute_locations_before(self):
        for record in self:
            stock_quant_ids = record.with_context({'to_date': record.before_counting}).stock_quant_ids            
            if len(stock_quant_ids) == 0:
                record.locations_before = 0
            else:
                locations_list = []
                for i in stock_quant_ids:
                    if i.location_id.usage == 'internal':
                        locations_list.append(i.location_id)
                record.locations_before = len(set(locations_list))

    def _compute_locations_after(self):
        for record in self:
            stock_quant_ids = record.with_context({'to_date': record.counting_day}).stock_quant_ids            
            if len(stock_quant_ids) == 0:
                record.locations_after = 0
            else:
                locations_list = []
                for i in stock_quant_ids:
                    if i.location_id.usage == 'internal':
                        locations_list.append(i.location_id)
                record.locations_after = len(set(locations_list))

    def _compute_count_before(self):
        for record in self:
            record.count_before = record.with_context({'to_date': record.before_counting}).qty_available

    def _compute_count_after(self):
        for record in self:
            record.count_after = record.with_context({'to_date': record.counting_day}).qty_available

    def action_show_locations_before(self):
        self.ensure_one()
        for record in self:
            product_id = record.with_context({'to_date': record.before_counting})
        self.env['stock.quant']._merge_quants()
        self.env['stock.quant']._unlink_zero_quants()
        action = self.env.ref('stock.quantsact').read()[0]
        action['limit'] = 1
        action['domain'] = [('product_id', '=', product_id.id)]
        return action
        
    def action_show_locations_after(self):
        self.ensure_one()
        for record in self:
            product_id = record.with_context({'to_date': record.counting_day})
        self.env['stock.quant']._merge_quants()
        self.env['stock.quant']._unlink_zero_quants()
        action = self.env.ref('stock.quantsact').read()[0]
        action['limit'] = 1
        action['domain'] = [('product_id', '=', product_id.id)]
        return action