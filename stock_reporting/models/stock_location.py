# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _

class Location(models.Model):
    _inherit = "stock.location"
    _order = "counted asc"
    
    counted = fields.Char('Counted', default='NO', store=True)
    created_moves = fields.Integer(string='Created Moves', default=0, store=True)
    inventory_ids = fields.One2many(
        'stock.inventory', 'location_id', string='Inventory Adjustmnets')