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
    product_id = fields.Many2one('product.product', string="Product")
    qty = fields.Float(strint="Qty")
    barcode = fields.Char('Barcode')

    @api.multi
    def action_go_to(self):
        form_view_id = self.env.ref('picking_process.view_scan_location_location_wizard').id
        sale_order = self.env['sale.order'].browse(self._context['sale_order'])
        history_id = self.env['pack.history'].search([('order_id', '=', sale_order.id)])
        data = []
        for line in sale_order.order_line:
            for quant in line.product_id.stock_quant_ids:
                if quant.location_id.usage != 'inventory':
                    d = {
                        'product_id': quant.product_id,
                        'location_id': quant.location_id,
                        'location_name': quant.location_id.name,
                        'quantity': quant.quantity,
                        'qty_needed': line.product_uom_qty,
                    }
                    data.append(d)
        

        if not history_id:
            history_id = self.env['pack.history'].create({
                'order_id': sale_order.id,
                'pick_location_id': self.picking_location_id.id,
                'move_ids': [(0, 0, {
                    'product_id': line.get('product_id').id,
                    'qty_needed': line.get('qty_needed'),
                    'qty_available': line.get('quantity'),
                    'pick_location_id': self.picking_location_id.id,
                    'from_location_id': line.get('location_id').id,
                    'state': 'draft'
                }) for line in sorted(data, key=lambda i: i['location_name'])]
            })
            sale_order.pack_history_id = history_id.id
        # (location, product, qty_needed,)
        queue = [(d.from_location_id.name, d.product_id.id, d.qty_needed) for d in history_id.move_ids if d.state == 'draft']
        queue = [
            {
                'from_location_name': d.from_location_id.name,
                'from_location_id': d.from_location_id.id,
                'product_id': d.product_id.id, 
                'qty_needed': d.qty_needed
            } for d in history_id.move_ids if d.state == 'draft']
        if queue:
            _context = self._context.copy()
            _context['history_id'] = history_id.id
            _context['product_id'] = queue[0].get('product_id')
            _context['qty_needed'] = queue[0].get('qty_needed')
            _context['from_location_name'] = queue[0].get('from_location_name')
            _context['from_location_id'] = queue[0].get('from_location_id')
            location_name = queue[0].get('from_location_name')
        else:
            return {}
        return {
            'name': _('Go To: %s' % location_name),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': _context,
            'res_model': 'picking.process',
        }

    # TO DO
    @api.multi
    def action_find_location(self):
        self.ensure_one()
        location_id = self.location_id.search([('name', '=', self.location_name)])
        if location_id:
            self.location_id = location_id
        else:
            raise UserError(_('Location not found'))
        form_view_id = self.env.ref('picking_process.view_stock_add_product_wizard').id
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

    @api.multi
    def action_open_location(self):
        form_view_id = self.env.ref('picking_process.view_stock_add_product_wizard').id
        product_id = self.env['product.product'].browse(self._context.get('product_id'))
        return {
            'name': _('Find the Product: [%s] [%s]' % (product_id.name, product_id.barcode)),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {},
            'res_model': 'picking.process',
        }


    @api.multi
    def action_product_next_stage(self):
        self.ensure_one()
        # product_id = self.product_id.search([('barcode', '=', self.barcode)])
        # if product_id:
        #     self.product_id = product_id
        # else:
        #     raise UserError(_('Product not found'))
        # location_id = self.env['stock.location'].browse(self._context.get('location_id'))
        # form_view_id = self.env.ref('cycle_count_friendly.view_stock_enter_qry_product_wizard').id
        # return {
        #     'name': _('Add New items to %s' % location_id.display_name),
        #     'type': 'ir.actions.act_window',
        #     'views': [(form_view_id, 'form')],
        #     'view_mode': 'form',
        #     'view_type': 'form',
        #     'target': 'new',
        #     # 'context': {'product_id': self.product_id.id},
        #     'res_model': 'picking.process',
        # }


    @api.multi
    def action_open_product(self):
        form_view_id = self.env.ref('picking_process.view_stock_enter_qry_product_wizard').id
        qty_needed = self._context.get('qty_needed')

        return {
            'name': _(''),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_qty': qty_needed},
            'res_model': 'picking.process',
        }

    @api.multi
    def create_inventory(self):
        history_id = self.env['pack.history'].browse(self._context.get('history_id'))
        product_id = self.env['product.product'].browse(self._context.get('product_id'))
        from_location_id = self.env['stock.location'].browse(self._context.get('from_location_id'))
        move_id = history_id.move_ids.filtered(lambda x: x.product_id == product_id and x.from_location_id == from_location_id)
        move_id.state = 'done'
        return self.action_go_to()