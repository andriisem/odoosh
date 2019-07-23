# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError

class StockMove(models.Model):
    _inherit = "stock.move"

    @api.multi
    @api.depends('availability')
    @api.constrains('product_uom_qty')
    def onchange_product_uom_qty(self):
        for record in self:
            if record.product_uom_qty > record.availability:
                raise UserError('''Quantity of product that is planned to be moved can't be greater
                                    than quantity what is available in the source location.''')
        return