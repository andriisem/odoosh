# -*- coding: utf-8 -*-

import logging

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class PickingProcess(models.TransientModel):
    _name = 'picking.process'
    _description = 'Picking Process'

    picking_location_id = fields.Many2one(
        'stock.location', string='Location', domain="[('usage', '!=', 'view'), ('is_picking_location', '=', True)]")
    location_id = fields.Many2one(
        'stock.location', string='Location', domain="[('usage', '!=', 'view')]")
    
    location_name = fields.Char(string='Loacation Name')
    product_id = fields.Many2one('product.product', string="Product")
    qty = fields.Float(strint="Qty")
    barcode = fields.Char('Barcode')

    @api.multi
    def action_go_to(self):
        form_view_id = self.env.ref(
            'picking_process.view_scan_location_location_wizard').id
        sale_order = self.env['sale.order'].browse(self._context['sale_order'])
        history_id = self.env['pack.history'].search(
            [('order_id', '=', sale_order.id)])
        data = []
        for line in sale_order.order_line:
            if line.product_id.stock_quant_ids:
                a = 0
                total_qty = 0
                for quant in line.product_id.stock_quant_ids.sorted(lambda o: o.location_id.name):
                    if quant.location_id.usage != 'inventory' and quant.quantity and total_qty != line.product_uom_qty:
                        if quant.quantity < line.product_uom_qty:
                            quantity = quant.quantity
                            a += quantity 
                        else:
                            quantity = line.product_uom_qty - a
                        total_qty += quantity
                        data.append(
                            {
                                'product_id': quant.product_id,
                                'location_id': quant.location_id,
                                'location_name': quant.location_id.name,
                                'quantity': quant.quantity,
                                'qty_needed': quantity,
                                'state': 'draft',
                            }
                        )
                if total_qty != line.product_uom_qty:
                    data.append(
                    {
                        'product_id': line.product_id,
                        'location_name': 'w',
                        'qty_needed': line.product_uom_qty - total_qty,
                        'state': 'not_available',
                    }
                )

            else:
                data.append(
                    {
                        'product_id': line.product_id,
                        'location_name': 'w',
                        'qty_needed': line.product_uom_qty,
                        'state': 'not_available',
                    }
                )

        if not history_id:
            history_id = self.env['pack.history'].create({
                'order_id': sale_order.id,
                'pick_location_id': self.picking_location_id.id,
                'move_ids': [(0, 0, {
                    'product_id': line.get('product_id').id,
                    'qty_needed': line.get('qty_needed'),
                    'qty_available': line.get('quantity'),
                    'pick_location_id': self.picking_location_id.id,
                    'from_location_id': line.get('location_id') and line.get('location_id').id or False,
                    'state': line.get('state'),
                }) for line in sorted(data, key=lambda i: i['location_name'])]
            })
            for history in history_id.move_ids:
                if history.product_id.id in history_id.move_ids.ids:
                    pass
                else:
                    pass
                
            sale_order.pack_history_id = history_id.id

        queue = [
            {
                'from_location_name': d.from_location_id.name,
                'from_location_id': d.from_location_id.id,
                'product_id': d.product_id.id,
                'qty_needed': d.qty_needed,
                'state': d.state
            } for d in history_id.move_ids if d.state in ('draft')]
        if queue:
            _context = self._context.copy()
            _context['history_id'] = history_id.id
            _context['state'] = queue[0].get('state')
            _context['product_id'] = queue[0].get('product_id')
            _context['qty_needed'] = queue[0].get('qty_needed')
            _context['from_location_name'] = queue[0].get('from_location_name')
            _context['from_location_id'] = queue[0].get('from_location_id')
            location_name = queue[0].get('from_location_name')
        else:
            done_item = history_id.move_ids.filtered(lambda x: x.state == 'done')
            if len(done_item) != len(history_id.move_ids):
                sale_order.short_history_id = history_id.id    
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

    @api.multi
    def action_skip(self):
        history_id = self.env['pack.history'].browse(
            self._context.get('history_id'))
        product_id = self.env['product.product'].browse(
            self._context.get('product_id'))
        from_location_id = self.env['stock.location'].browse(
            self._context.get('from_location_id'))
        move_id = history_id.move_ids.filtered(
            lambda x: x.product_id == product_id and x.from_location_id == from_location_id)
        qty = self._context.get('qty')
        move_id.state = 'checked_not_avaliable'
        self.product_id = product_id.id
        self.location_id = from_location_id.id
        self.qty = qty

        template_id = self.env.ref('picking_process.email_template', False) 
        template_id.email_from = self.env.user.email 
        template_id.email_to = 'adir@macoci.com'
        template_id.send_mail(self.id, force_send=True) 

        return self.action_go_to()

    @api.multi
    def action_find_location(self):
        self.ensure_one()
        location_from_context = self._context.get('from_location_name')
        location_id = self.location_id.search(
            [('name', '=', self.location_name)])
        if location_id:
            self.location_id = location_id
        else:
            raise UserError(_('Location not found'))
        
        if location_id.name == location_from_context:
            form_view_id = self.env.ref(
                'picking_process.view_stock_add_product_wizard').id
            product_id = self.env['product.product'].browse(
                self._context.get('product_id'))
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
        else:
            raise UserError(_('Go To %s location' % location_from_context))

    @api.multi
    def action_open_location(self):
        form_view_id = self.env.ref(
            'picking_process.view_stock_add_product_wizard').id
        product_id = self.env['product.product'].browse(
            self._context.get('product_id'))
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
        product_id = self.product_id.search([('barcode', '=', self.barcode)])
        product_from_cobtext = self.env['product.product'].browse(self._context.get('product_id'))
        if product_id:
            self.product_id = product_id
        else:
            raise UserError(_('Product not found'))

        if product_id.id == self._context.get('product_id'):
            form_view_id = self.env.ref(
                'picking_process.view_stock_enter_qry_product_wizard').id
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
        else:
            raise UserError(_('Find the Product: [%s] [%s]' % (product_from_cobtext.name, product_from_cobtext.barcode)))


    @api.multi
    def action_open_product(self):
        form_view_id = self.env.ref(
            'picking_process.view_stock_enter_qry_product_wizard').id
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
        history_id = self.env['pack.history'].browse(
            self._context.get('history_id'))
        product_id = self.env['product.product'].browse(
            self._context.get('product_id'))
        from_location_id = self.env['stock.location'].browse(
            self._context.get('from_location_id'))
        move_id = history_id.move_ids.filtered(
            lambda x: x.product_id == product_id and x.from_location_id == from_location_id)

        StockPicking = self.env['stock.picking']
        stock_picking_type_id = self.env['stock.picking.type'].search([('code', '=', 'internal')], limit=1)

        picking = StockPicking.create({
            'picking_type_id': stock_picking_type_id.id,
            'location_id': move_id.from_location_id.id,
            'location_dest_id': move_id.pick_location_id.id,
        })

        move = self.env['stock.move'].create({
            'name': move_id.product_id.name,
            'product_id': move_id.product_id.id,
            'product_uom_qty': self.qty,
            'product_uom': move_id.product_id.product_tmpl_id.uom_id.id,
            'picking_id': picking.id,
            'location_id': move_id.from_location_id.id,
            'location_dest_id': move_id.pick_location_id.id,
            'procure_method': 'make_to_stock',
            'state': 'draft',
        })
        move._action_confirm()
        picking.action_assign()
        move.write({
            'quantity_done': self.qty,
        })
        picking.button_validate()
        move_id.state = 'done'
        move_id.qty_done = self.qty

        if move_id.qty_needed > self.qty:
            form_view_id = self.env.ref('picking_process.view_stock_select_other_location').id  
            return {
                'name': _(''),
                'type': 'ir.actions.act_window',
                'views': [(form_view_id, 'form')],
                'view_mode': 'form',
                'view_type': 'form',
                'target': 'new',
                'context': {'qty': self.qty},
                'res_model': 'picking.process',
            }
        elif move_id.qty_needed < self.qty:
            raise UserError(_('You entered more than necessary'))
        return self.action_go_to()


    @api.multi
    def action_confirm_other_stock(self):
        product_id = self._context.get('product_id')
        history_id = self.env['pack.history'].browse(
            self._context.get('history_id'))
        qty_needed = self._context.get('qty_needed')
        qty = self._context.get('qty')
        aval = self.location_id.quant_ids.filtered(lambda x: x.product_id.id == product_id)
        if aval and sum(aval.mapped('quantity')):
            history_id.write({
                'move_ids': [(0, 0, {
                    'product_id': self._context.get('product_id'),
                    'qty_needed': qty_needed - qty,
                    'qty_available': sum(aval.mapped('quantity')),
                    'pick_location_id': history_id.pick_location_id.id,
                    'from_location_id': self.location_id.id,
                    'state': 'draft',
                })]
            })
            return self.action_go_to()
        else:
            raise UserError(_('Not Exist'))
