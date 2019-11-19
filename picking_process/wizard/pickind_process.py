# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PickingProcess(models.TransientModel):
    _name = 'picking.process'
    _description = 'Picking Process'

    picking_location_id = fields.Many2one('stock.location', string='Location', domain="[('usage', '!=', 'view'), ('is_picking_location', '=', True)]")
    location_id = fields.Many2one('stock.location', string='Location', domain="[('usage', '!=', 'view')]")
    location_name = fields.Char(string='Loacation Name')


    @api.multi
    def action_go_to(self):
        form_view_id = self.env.ref('picking_process.view_scan_location_location_wizard').id
        return {
            'name': _('Picking'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
            'res_model': 'picking.process',
        }

    @api.multi
    def action_find_location(self):
        self.ensure_one()
        location_id = self.location_id.search([('name', '=', self.location_name)])
        if location_id:
            self.location_id = location_id
        else:
            raise UserError(_('Location not found'))
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_onhand_count_wizard').id
    
        quant_ids = self.location_id.quant_ids.filtered(lambda x: x.quantity != 0)
        return {
            'name': _('Picking'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {},
            'res_model': 'picking.process',
        }
