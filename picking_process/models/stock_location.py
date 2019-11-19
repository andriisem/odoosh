# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models


class Stocklocation(models.Model):
    _inherit = 'stock.location'


    is_picking_location = fields.Boolean(string='Picking location')
