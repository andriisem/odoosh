# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api

class Picking(models.Model):
    _inherit = 'stock.picking'

    custom_location_id = fields.Many2one(
        'stock.location', "Source Location",
        )
    custom_location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        )
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        index=True, required=True,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.", related="custom_location_id")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        index=True, required=True,
        help="Location where the system will stock the finished products.", related="custom_location_dest_id")