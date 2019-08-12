# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from datetime import datetime

class StockQuantityHistory(models.TransientModel):
    _inherit = 'stock.quantity.history'

    compute_at_date = fields.Selection([
        (0, 'Current Inventory'),
        (1, 'At a Specific Date'),
        (2, 'Count Inspection'),
    ], string="Compute", help="Choose to analyze the current inventory or from a specific date in the past.")

    counting_day = fields.Datetime('Counting Day', help="Choose a date to get the inventory at that date", default=fields.Datetime.now)
    before_counting = fields.Datetime('Before Counting', help="Choose a date to get the inventory at that date", default=fields.Datetime.now)
    
    def open_table(self):
        self.ensure_one()
        if self.compute_at_date:
            if self.compute_at_date != 2:
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
            else:
                tree_view_id = self.env.ref('stock_reporting.custom_view_stock_product_tree').id
                form_view_id = self.env.ref('stock.product_form_view_procurement_button').id
                search_view_id = self.env.ref('stock_reporting.custom_product_search_form_view').id
                # pivot_view_id = self.env.ref('stock_reporting.custom_view_stock_product_pivot').id

                action = {
                    'type': 'ir.actions.act_window',
                    # 'views': [(tree_view_id, 'tree'), (form_view_id, 'form'), (pivot_view_id, 'pivot')],
                    'views': [(tree_view_id, 'tree'), (form_view_id, 'form')],
                    'view_mode': 'tree,pivot,form',
                    'name': _('Products'),
                    'res_model': 'product.product',
                    'domain': "[('type', '=', 'product')]",
                    'search_view_id': search_view_id,
                    'context': dict(self.env.context, to_date=self.counting_day, counting_day=self.counting_day, before_counting=self.before_counting),
                }
            return action
        else:            
            self.env['stock.quant']._merge_quants()
            self.env['stock.quant']._unlink_zero_quants()
            return self.env.ref('stock.quantsact').read()[0]