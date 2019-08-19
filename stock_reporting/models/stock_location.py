# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _

class Location(models.Model):
    _inherit = "stock.location"
    
    counted = fields.Char('Counted', default='NO', store=True)
    move_ids = fields.One2many(
        'stock.move', 'location_id', string='Created Moves')