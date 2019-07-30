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
        view = self.env.ref('quick_transfer.custom_view_picking_form')
        context = dict(self.env.context)
        product_partner_id = self.product_id.company_id.partner_id.id
        product_location_id = self.location_id.id
        product_uom_qty = self.quantity
        product_reserved_quantity = self.reserved_quantity
        product_product = self.product_id.id
        product_product_name = self.product_id.display_name
        product_product_uom_id = self.product_uom_id.id
        product_scheduled_date = fields.Datetime.now(self)
        product_date_expected = fields.Datetime.now(self)
        state = 'done'
        for i in picking_types:
            if 'Internal' in i.name:
                product_picking_type_id = i.id
                break
        if pickings:
            for i in pickings:
                product_origin = i.origin
                product_location_dest_id = i.custom_location_dest_id.id
                product_picking_id = i.id
                # product_picking_type_id = i.picking_type_id.id

            # new_move = self.env['stock.move'].create({
            #         'name': _('New Move:') + product_product_name,
            #         'product_id': product_product,
            #         'product_uom_qty': product_uom_qty - product_reserved_quantity,
            #         'reserved_availability': product_reserved_quantity,
            #         'product_uom': product_product_uom_id,
            #         'location_id': product_location_id,
            #         'location_dest_id': product_location_dest_id,
            #         'picking_id': product_picking_id,
            #         'picking_type_id': product_picking_type_id,
            #        })
            new_move_list = [(0, 0, {
                    'name': _('New Move:') + product_product_name,
                    'product_id': product_product,
                    'product_uom_qty': product_uom_qty - product_reserved_quantity,
                    'reserved_availability': product_reserved_quantity,
                    'product_uom': product_product_uom_id,
                    'location_id': product_location_id,
                    'location_dest_id': product_location_dest_id,
                    'picking_id': product_picking_id,
                    'picking_type_id': product_picking_type_id,
                   })]
                # product_name = i.move_ids_without_package.name
                # product_quantity_done = i.move_ids_without_package.quantity_done
                
        # new_move = [(0, 0, {'name': product_name, 
        #                     'product_id': product_product,
        #                     'location_id': product_location_id,
        #                     'product_uom_qty': product_quantity - product_reserved_quantity,
        #                     'reserved_availability': product_reserved_quantity,
        #                     'quantity_done': product_quantity_done,
        #                     })]
        else:
            new_picking = self.env['stock.picking'].create({
                        'name': _('New Picking:') + product_product_name,
                        'product_id': product_product,
                        'location_id': product_location_id,
                        'location_dest_id': picking_types[0].default_location_dest_id.id,
                        'custom_location_id': product_location_id,
                        'custom_location_dest_id': picking_types[0].default_location_dest_id.id,
                        'picking_type_id': picking_types[0].id,
                        'state': state,
                        'date_expected': product_date_expected,
                       })      
            # new_move = self.env['stock.move'].create({
            #             'name': _('New Move:') + product_product_name,
            #             'product_id': product_product,
            #             'product_uom_qty': product_uom_qty - product_reserved_quantity,
            #             'reserved_availability': product_reserved_quantity,
            #             'product_uom': product_product_uom_id,
            #             'location_id': product_location_id,
            #             'location_dest_id': new_picking.custom_location_dest_id.id,
            #             'picking_id': new_picking.id,
            #             'picking_type_id': new_picking.picking_type_id.id,
            #             'state': state,
            #            })
            new_move_list = [(0, 0, {
                        'name': _('New Move:') + product_product_name,
                        'product_id': product_product,
                        'product_uom_qty': product_uom_qty - product_reserved_quantity,
                        'reserved_availability': product_reserved_quantity,
                        'product_uom': product_product_uom_id,
                        'location_id': product_location_id,
                        'location_dest_id': new_picking.custom_location_dest_id.id,
                        'picking_id': new_picking.id,
                        'picking_type_id': new_picking.picking_type_id.id,
                        'state': state,
                       })]
            product_origin = new_picking.origin
            product_location_dest_id = new_picking.custom_location_dest_id.id
            product_picking_id = new_picking.id
            # product_picking_type_id = new_picking.picking_type_id.id
        
        context.update({
            'default_picking_id': product_picking_id,
            'default_state': state,
            'default_picking_type_id': product_picking_type_id,
            'default_scheduled_date': product_scheduled_date,
            'default_date_expected': product_date_expected,
            'default_origin': product_origin,
            'default_move_ids_without_package':new_move_list,
            'default_partner_id': product_partner_id,
            'default_product_uom_id': product_product_uom_id,
            'default_reserved_availability': product_reserved_quantity,
            'default_product_uom_qty': product_uom_qty - product_reserved_quantity,
            'default_product_id': product_product,  
            'default_custom_location_id': product_location_id,
            'default_custom_location_dest_id': product_location_dest_id,
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