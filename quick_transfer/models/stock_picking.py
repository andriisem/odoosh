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
        auto_join=False, index=False, required=False,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.", compute="_compute_location_id")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        auto_join=False, index=False, required=False,
        help="Location where the system will stock the finished products.", compute="_compute_location_dest_id")

    @api.depends('custom_location_id')
    def _compute_location_id(self):
        for record in self:
            record.location_id  = record.custom_location_id

    @api.depends('custom_location_dest_id')
    def _compute_location_dest_id(self):
        for record in self:
            record.location_dest_id  = record.custom_location_dest_id