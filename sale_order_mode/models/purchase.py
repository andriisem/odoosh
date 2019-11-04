from odoo import api, fields, models


class Purchase(models.Model):
    _inherit = 'purchase.order'

    total_qty = fields.Float(string='Total Qty', compute='_compute_total_qty', store=True)

    @api.multi
    @api.depends('order_line.product_uom_qty')
    def _compute_total_qty(self):
        for order in self:
            qty = 0
            for line in order.order_line:
                qty += line.product_qty
            order.total_qty = qty
