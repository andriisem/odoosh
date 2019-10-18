from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    backorders = fields.Boolean(string='Backorders')
    due_date = fields.Datetime(string='Due Date')
    stage_id = fields.Many2one('fullfilemt.stage', string='Stage', compute='_compute_stage', store=True) 

    @api.depends('order_line', 'backorders', 'dtc_type', 'sale_order_mode_manual', 'partner_id.sale_order_mode')
    def _compute_stage(self):
        for order in self:
            if order.backorders:
                order.stage_id = self.env.ref('fullfilemt_stage.backorders_stage')
            elif order.sale_order_mode in ('sc', 'mr') or order.sale_order_mode_manual in ('sc', 'mr'):
                order.stage_id = self.env.ref('fullfilemt_stage.samples_replacements_stage')
            elif order.sale_order_mode == 'ws' or order.sale_order_mode_manual == 'ws':
                order.stage_id = self.env.ref('fullfilemt_stage.wholesale_stage')
            elif (order.sale_order_mode == 'dtc' and order.dtc_type == 'single') or (order.sale_order_mode_manual == 'dtc' and order.dtc_type == 'single'):
                order.stage_id = self.env.ref('fullfilemt_stage.dtc_single_stage')
