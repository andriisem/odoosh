# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

class StockQuant(models.Model):
    _inherit = 'stock.quant'

    def action_show_quick_details(self):
        self.ensure_one()
        context = dict(self.env.context)
        product_partner_id = self.product_id.company_id.partner_id.id
        product_location_id = self.location_id.id
        product_uom_qty = self.quantity
        product_reserved_quantity = self.reserved_quantity
        product_product = self.product_id.id
        product_product_name = self.product_id.display_name
        product_product_uom_id = self.product_uom_id.id
        product_scheduled_date = fields.Datetime.now(self)
        product_date_expected = fields.Datetime.now(self).strftime("%Y-%m-%d %H:%M:%S")
        warehouse = self.env['stock.warehouse'].search([('company_id', '=', self.env.user.company_id.id)])
        picking_types = self.env['stock.picking.type'].search([('warehouse_id', '=', warehouse.id)])
        pickings = self.env['stock.picking'].search([('product_id', '=', product_product)])
        view = self.env.ref('quick_transfer.custom_view_picking_form')
        for i in picking_types:
            if 'Internal' in i.name:
                product_picking_type_id = i.id
                product_location_dest_id = i.default_location_dest_id.id,
                break
        
        new_picking = self.env['stock.picking'].create({                    
                    'partner_id': product_partner_id,
                    'product_id': product_product,
                    'location_id': product_location_id,
                    'location_dest_id': False,
                    'immediate_transfer': False,
                    'owner_id': False,
                    'move_type': 'direct', 
                    'company_id': self.env.user.company_id.id,
                    'is_locked': True,
                    'partner_id': product_partner_id,
                    'picking_type_id': product_picking_type_id,
                    'move_ids_without_package': 
                    [[0, 'virtual_94', 
                        {'date_expected': product_date_expected, 
                        'state': 'draft', 
                        'picking_type_id': product_picking_type_id, 
                        'location_id': product_location_id,
                        'location_dest_id': product_location_dest_id, 
                        'additional': False,
                        'product_uom_qty': product_uom_qty - product_reserved_quantity, 
                        'name': _('') + product_product_name, 
                        'product_id': product_product, 
                        'product_uom': product_product_uom_id}]], 
                    'priority': False, 
                    'note': False, 
                    'message_attachment_count': 0,                    
                    })

        product_picking_id = new_picking.id
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
            'res_id': product_picking_id
        }