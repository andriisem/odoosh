from odoo import api, fields, models, _
from odoo.exceptions import UserError


class CycleCount(models.TransientModel):
    _name = 'cycle.count.wizard'
    _description = 'Cycle Count (Wizard)'

    product_id = fields.Many2one('product.product', string="Product")
    location_id = fields.Many2one('stock.location', string='Location', domain="[('usage', '!=', 'view')]")
    location_name = fields.Char(string='Loacation Name')
    quant_ids = fields.Many2many('stock.quant', string="Quants")
    active_camera = fields.Boolean(default=False)
    qty = fields.Float(strint="Qty", default=False)
    barcode = fields.Char('Barcode')
    inventory_history_ids = fields.Many2many('inventory.history', string='History', readonly=True)

    @api.multi
    def action_product_next_stage(self):
        self.ensure_one()
        product_id = self.product_id.search([('barcode', '=', self.barcode)])
        if product_id:
            self.product_id = product_id
        else:
            raise UserError(_('Product not found'))
        location_id = self.env['stock.location'].browse(self._context.get('location_id'))
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_enter_qry_product_wizard').id
        return {
            'name': _('Add New items to %s' % location_id.display_name),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'product_id': self.product_id.id},
            'res_model': 'cycle.count.wizard',
        }

    @api.multi
    def add_product(self):
        self.ensure_one()
        location_id = self.env['stock.location'].browse(self._context.get('location_id'))
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_add_product_wizard').id
        quant_ids = self.location_id.quant_ids.filtered(lambda x: x.quantity != 0)
        return {
            'name': _('Add New items to %s' % location_id.display_name),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_quant_ids': quant_ids.ids},
            'res_model': 'cycle.count.wizard',
        }
    
    @api.multi
    def cancel_inventory(self, product_id):
        Inventory = self.env['stock.inventory']
        inventory = Inventory.search([
            ('filter', '=', 'product'),
            ('product_id', '=', product_id.id),
            ('state', '=', 'confirm')
        ])
        inventory.action_cancel_draft()

    @api.multi
    def create_inventory(self):
        self.ensure_one()
        Inventory = self.env['stock.inventory']
        location_id = self.env['stock.location'].browse(self._context.get('location_id'))
        product_id = self.env['product.product'].browse(self._context.get('product_id'))
        self.cancel_inventory(product_id)
        inventory = Inventory.create({
            'name': product_id.name,
            'filter': 'product',
            'location_id': location_id.id,
            'product_id': product_id.id,
        })
        inventory.action_start()
        if not inventory.line_ids:
            self.env['stock.inventory.line'].create({
                'inventory_id': inventory.id,
                'product_id': product_id.id,
                'product_uom_id': product_id.uom_id.id,
                'product_qty': self.qty,
                'location_id': location_id.id,
            })
        inventory.line_ids.product_qty = self.qty
        inventory.action_validate()
        quant_ids = location_id.quant_ids.filtered(lambda x: x.quantity != 0)
        return self.with_context(
            {'default_quant_ids': quant_ids.ids,
             'location_id': location_id.id}).action_reopen_location()

    @api.multi
    def action_save(self):
        self.ensure_one()
        inventory_history_id = self.env['inventory.history'].browse(self._context['inventory_history_id'])
        inventory_history_id.action_save()
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_cycle_count_wizard').id
        quant_ids = self.location_id.quant_ids.filtered(lambda x: x.quantity != 0)
        
        return {
            'name': _('Cycle Count (Wizard)'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {'default_quant_ids': quant_ids.ids},
            'res_model': 'cycle.count.wizard',
        }
        
    @api.multi
    def action_finish(self):
        self.ensure_one()
        inventory_history_id = self.env['inventory.history'].browse(self._context['inventory_history_id'])
        inventory_history_id.action_finish()
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_cycle_count_wizard').id
        return {
            'name': _('Cycle Count (Wizard)'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'res_model': 'cycle.count.wizard',
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
        inventory_history = self.inventory_history_ids.create({
            'location_id': self.location_id.id,
            'partner_id': self.env.user.partner_id.id,
            'state': 'new',
        })
        quant_ids = self.location_id.quant_ids.filtered(lambda x: x.quantity != 0)
        return {
            'name': _('Items in %s' % self.location_id.display_name),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_quant_ids': quant_ids.ids,
                'location_id': self.location_id.id,
                "inventory_history_id": inventory_history.id
                },
            'res_model': 'cycle.count.wizard',
        }
    
    @api.multi
    def edit_qty_inventory(self):
        Inventory = self.env['stock.inventory']
        quant_id = self.env['stock.quant'].browse(self._context.get('quant'))
        product_id = quant_id.product_id
        location_id = quant_id.location_id
        self.cancel_inventory(product_id)
        inventory = Inventory.create({
            'name': product_id.name,
            'filter': 'product',
            'location_id': location_id.id,
            'product_id': product_id.id,
        })
        inventory.action_start()
        if not inventory.line_ids:
            self.env['stock.inventory.line'].create({
                'inventory_id': inventory.id,
                'product_id': product_id.id,
                'product_uom_id': product_id.uom_id.id,
                'product_qty': self.qty,
                'location_id': location_id.id,
            })
        inventory.line_ids.product_qty = self.qty
        inventory.action_validate()
        quant_ids = location_id.quant_ids.filtered(lambda x: x.quantity != 0)
        return self.with_context(
            {'default_quant_ids': quant_ids.ids,
             'location_id': location_id.id}).action_reopen_location()
    
    @api.multi
    def action_reopen_location(self):
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_onhand_count_wizard').id
        location_id = self.env['stock.location'].browse(self._context.get('location_id'))
        action = {
            'name': _('Items in %s' % location_id.display_name),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
            'res_model': 'cycle.count.wizard',
        }
        return action

    @api.multi
    def action_delate_yes(self):
        self.ensure_one()
        quant_id = self.env['stock.quant'].browse(self._context.get('quant'))
        quant_id.sudo().unlink()
        self._context['default_quant_ids'].remove(self._context.get('quant'))
        return self.action_reopen_location()

    @api.multi
    def action_delate_no(self):
        return self.action_reopen_location()

    @api.multi
    def action_open_history(self):
        form_view_id = self.env.ref('cycle_count_friendly.view_history_wizard').id
        inventory_history_ids = self.inventory_history_ids.search([('state', '=', 'draft')])
        return {
            'name': _('History'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': {
                'default_inventory_history_ids': inventory_history_ids.ids,
                'location_id': self.location_id.id
                },
            'res_model': 'cycle.count.wizard',
        }
