# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.multi
    def print_pick_process(self):
        return self.env.ref('picking_process.action_report_pick_list').report_action(self)

    @api.multi
    def action_pick(self):
        form_view_id = self.env.ref('picking_process.view_picking_location_wizard').id
        return {
            'name': _('Picking Process'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
            'res_model': 'picking.process',
        }
