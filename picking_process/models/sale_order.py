# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models

_logger = logging.getLogger(__name__)


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    pack_history_id = fields.Many2one('pack.history', string='Pick History')
    short_history_id = fields.Many2one('pack.history', string='Short')

    @api.multi
    def print_pick_process(self):
        return self.env.ref('picking_process.action_report_pick_list').report_action(self)

    @api.multi
    def action_pick(self):
        form_view_id = self.env.ref('picking_process.view_picking_location_wizard').id
        _context = self._context.copy()
        _context['sale_order'] = self.id
        _context['default_picking_location_id'] =  self.pack_history_id.pick_location_id and self.pack_history_id.pick_location_id.id or False
        return {
            'name': _('Picking Process'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': _context,
            'res_model': 'picking.process',
        }

    @api.multi
    def aсtion_short_history(self):
        history_id = self.pack_history_id
        action = self.env.ref('picking_process.pack_history_form_action').read()[0]
        action['res_id'] = history_id.id
        return action