# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models

class Picking(models.Model):
    _inherit = 'stock.picking'

    custom_location_id = fields.Many2one(
        'stock.location', "Source Location",
        )
    custom_location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        )