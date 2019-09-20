from odoo import _, api, fields, models


class StockQuant(models.Model):
    _inherit = 'stock.quant'

    @api.multi
    def action_reopen_location(self):
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_onhand_count_wizard').id
        return {
            'name': _('Items in %s' % self.location_id.display_name),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': self._context,
            'res_model': 'cycle.count.wizard',
        }

    @api.multi
    def action_delate(self):
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_confirm_delate_wizard').id
        _context = self._context.copy()
        _context['quant'] = self.id
        return {
            'name': _('Are you sure you want remove [%s] from location [%s]' % (self.display_name, self.location_id.display_name)),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': _context,
            'res_model': 'cycle.count.wizard',
        }
    
    @api.multi
    def compute_qty(self):
        self.ensure_one()
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_edit_qty_product_wizard').id
        _context = self._context.copy()
        _context['quant'] = self.id
        return {
            'name': _('[%s] in [%s]' % (self.product_id.name, self.location_id.display_name)),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form')],
            'view_mode': 'form',
            'view_type': 'form',
            'target': 'new',
            'context': _context,
            'res_model': 'cycle.count.wizard',
        }
