# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_show_quick_details(self):
        self.ensure_one()
        view = self.env.ref('stock.view_picking_form')
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
            # 'context': dict(
            #     self.env.context,
            #     show_lots_m2o=self.has_tracking != 'none' and (self.picking_type_id.use_existing_lots or self.state == 'done' or self.origin_returned_move_id.id),  # able to create lots, whatever the value of ` use_create_lots`.
            #     show_lots_text=self.has_tracking != 'none' and self.picking_type_id.use_create_lots and not self.picking_type_id.use_existing_lots and self.state != 'done' and not self.origin_returned_move_id.id,
            #     show_source_location=self.location_id.child_ids and self.picking_type_id.code != 'incoming',
            #     show_destination_location=self.location_dest_id.child_ids and self.picking_type_id.code != 'outgoing',
            #     show_package=not self.location_id.usage == 'supplier',
            #     show_reserved_quantity=self.state != 'done'
            # ),
        }