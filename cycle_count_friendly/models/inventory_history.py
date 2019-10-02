from datetime import datetime

from odoo import _, api, fields, models

class InventoryHistoty(models.Model):
    _name = 'inventory.history'
    _description = 'inventory.history'

    state = fields.Selection(string='State', selection=[
        ('new', 'New'),
        ('draft', 'Draft'),
        ('done', 'Done'),
    ])
    date = fields.Datetime(strint='Date', default=fields.Datetime.now)
    partner_id = fields.Many2one('res.partner', string='By')
    location_id = fields.Many2one('stock.location', string='Location')

    @api.model
    def action_save(self):
        self.date = datetime.now()
        self.state = 'draft'
    
    @api.model
    def action_finish(self):
        self.date = datetime.now()
        self.state = 'done'
    
    @api.multi
    def action_play(self):
        self.ensure_one()
        form_view_id = self.env.ref('cycle_count_friendly.view_stock_onhand_count_wizard').id
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
                "inventory_history_id": self.id
                },
            'res_model': 'cycle.count.wizard',
        }
