# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _


class CycleCount(models.TransientModel):
    _name = 'cycle.count'
    _description = 'Cycle Count'

    def open_table(self):
        self.ensure_one()
        
        form_view_id = self.env.ref('cycle_count.cycle_count_view_inventory_form').id
        # We pass `to_date` in the context so that `qty_available` will be computed across
        # moves until date.
        action = {
            'name': _('Cycle Count'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'res_model': 'stock.inventory',
        }
        return action
       
