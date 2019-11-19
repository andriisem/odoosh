# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)



class PickingProcess(models.TransientModel):
    _name = 'picking.process'
    _description = 'Picking Process'

    picking_location_id = fields.Many2one('stock.location', string='Location', domain="[('usage', '!=', 'view'), ('is_picking_location', '=', True)]")


    @api.multi
    def action_go_to(self):
        form_view_id = self.env.ref('picking_process.view_picking_location_wizard').id
        return {
            'name': _('GO TO'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
            'res_model': 'picking.process',
        }
