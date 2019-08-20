# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    compute_at_date = fields.Selection([
        (0, 'Current Inventory'),
        (1, 'At a Specific Date'),
        (2, 'Count Inspection'),
        (3, 'Location Inspection'),
    ], string="Compute", help="Choose to analyze the current inventory or from a specific date in the past.")

    counting_day = fields.Datetime('Counting Day', help="Choose a date to get the inventory at that date", default=fields.Datetime.now)
    before_counting = fields.Datetime('Before Counting', help="Choose a date to get the inventory at that date", default=fields.Datetime.now)
    
    def open_table(self):
        self.ensure_one()
        if self.compute_at_date:
            if self.compute_at_date == 1:
                tree_view_id = self.env.ref('stock.view_stock_product_tree').id
                form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
                action = {
                    'type': 'ir.actions.act_window',
                    'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                    'view_mode': 'tree,form',
                    'name': _('Products'),
                    'res_model': 'product.product',
                    'domain': "[('type', '=', 'product')]",
                    'context': dict(self.env.context, to_date=self.date),
                }
            elif self.compute_at_date == 2:
                tree_view_id = self.env.ref('stock_reporting.custom_view_stock_product_tree').id
                action = {
                    'type': 'ir.actions.act_window',                 
                    'views': [(tree_view_id, 'tree')],
                    'view_mode': 'tree',
                    'name': _('Products'),
                    'res_model': 'product.product',
                    'domain': "[('type', '=', 'product')]",                   
                    'context': dict(self.env.context, to_date=self.counting_day, counting_day=self.counting_day, before_counting=self.before_counting),
                }
                products = self.env['product.product'].search([])
                for record in products:
                    record.counting_day = self.counting_day
                    record.before_counting = self.before_counting
                    count_before = record.with_context({'to_date': self.before_counting}).qty_available
                    count_after = record.with_context({'to_date': self.counting_day}).qty_available
                    record.difference = count_after - count_before
            elif self.compute_at_date == 3:
                tree_view_id = self.env.ref('stock_reporting.custom_view_location_tree2').id
                action = {
                    'type': 'ir.actions.act_window',
                    'views': [(tree_view_id, 'tree')],
                    'view_mode': 'tree',
                    'name': _('Locations'),
                    'res_model': 'stock.location',
                    'context': dict(self.env.context, search_default_in_location=1, to_date=self.counting_day, counting_day=self.counting_day, before_counting=self.before_counting),
                }
                locations = self.env['stock.location'].search([])
                for record in locations:
                    move_ids_create_date_list = [i.create_date for i in record.move_ids]
                    result = list(filter(lambda x: x > self.before_counting and x < self.counting_day, move_ids_create_date_list))
                    if len(result) > 0:
                        record.counted = 'YES'
                        record.created_moves = len(result)
                    else:
                        record.counted = 'NO'
                        record.created_moves = 0
            return action
        else:            
            self.env['stock.quant']._merge_quants()
            self.env['stock.quant']._unlink_zero_quants()
            return self.env.ref('stock.quantsact').read()[0]