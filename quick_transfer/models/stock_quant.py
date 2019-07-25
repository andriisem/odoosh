# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_show_quick_details(self):
        self.ensure_one()
        view = self.env.ref('quick_transfer.custom_view_picking_form')
        return {
            'name': _('Transfers'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'res_id': self.id,
            # 'context': self.env.context,
        }