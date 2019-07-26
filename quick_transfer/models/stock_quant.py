# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_show_quick_details(self):
        self.ensure_one()
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
        picking_types = self.env['stock.picking.type'].search([('warehouse_id', '=', warehouse.id)])
        pickings = self.env['stock.picking'].search([('location_id', '=', self.location_id.id)])
        if pickings:
            for i in pickings:
                if i.product_id.id == self.product_id.id:
                    product_scheduled_date = i.scheduled_date
                    product_origin = i.origin
        for i in picking_types:
            # if 'Internal' in i.name:
            if 'Delivery' in i.name:
                product_picking_type_id = i.id
                break
        view = self.env.ref('quick_transfer.custom_view_picking_form')
        context = dict(self.env.context)
        product_partner_id = self.product_id.company_id.partner_id.id
        product_location_id = self.location_id.id
        product_quantity = self.quantity
        product_reserved_quantity = self.reserved_quantity
        product_product = self.product_id.id
        context.update({
            'default_picking_type_id': product_picking_type_id,
            'default_product_id': product_product,
            'default_reserved_availability': product_reserved_quantity,
            'default_partner_id': product_partner_id, 
            'default_custom_location_id': product_location_id,
            'default_custom_location_dest_id': False,
            })
        
        return {
            'name': _('Transfers'),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'stock.picking',
            'views': [(view.id, 'form')],
            'view_id': view.id,
            'target': 'new',
            'context': context,
        }