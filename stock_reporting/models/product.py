# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _

class ProductProduct(models.Model):
    _inherit = "product.product"

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
            if len(record.stock_quant_ids) == 0:
                record.locations_before = 0
            else:
                product_id = record.id
                self.env['stock.quant']._merge_quants()
                self.env['stock.quant']._unlink_zero_quants()
                domain=[["location_id.usage", "=", "internal"]]
                fields=["product_id", "location_id", "lot_id", "package_id", "owner_id", "reserved_quantity", "quantity", "product_uom_id", "company_id"]
                groupby=["product_id", "location_id"]
                recordset = self.env['stock.quant'].read_group(domain, fields, groupby)
                for i in recordset:
                    if i['product_id'][0] == product_id:                        
                        record.locations_before = i['product_id_count']

    def _compute_locations_after(self):        
        context = self.env.context
        to_date = datetime.strptime(context.get('to_date'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            if len(record.stock_quant_ids) == 0:
                record.locations_after = 0
            else:
                product_id = record.id
                self.env['stock.quant']._merge_quants()
                self.env['stock.quant']._unlink_zero_quants()
                domain=[["location_id.usage", "=", "internal"]]
                fields=["product_id", "location_id", "lot_id", "package_id", "owner_id", "reserved_quantity", "quantity", "product_uom_id", "company_id"]
                groupby=["product_id", "location_id"]
                recordset = self.env['stock.quant'].read_group(domain, fields, groupby)
                for i in recordset:
                    if i['product_id'][0] == product_id:
                        record.locations_after = i['product_id_count']

    def _compute_count_before(self):
        for record in self:
            record.count_before  = len(self)

    def _compute_count_after(self):
        for record in self:
            record.count_after  = len(self)

    def action_show_locations_before(self):
        self.ensure_one()
        context = dict(self.env.context)
        to_date = context.get('to_date')
        self.env['stock.quant']._merge_quants()
        self.env['stock.quant']._unlink_zero_quants()
        action = self.env.ref('stock.quantsact').read()[0]
        action['limit'] = 1
        action['domain'] = [('product_id', '=', self.id)]
        print(action)
        return action
        
    def action_show_locations_after(self):
        self.ensure_one()
        context = dict(self.env.context)
        to_date = context.get('to_date')
        self.env['stock.quant']._merge_quants()
        self.env['stock.quant']._unlink_zero_quants()
        action = self.env.ref('stock.quantsact').read()[0]
        action['limit'] = 1
        action['domain'] = [('product_id', '=', self.id)]
        print(action)
        return action