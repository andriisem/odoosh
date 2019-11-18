# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def print_pick_process(self):
        return self.env.ref('picking_process.action_report_pick_list').report_action(self)
