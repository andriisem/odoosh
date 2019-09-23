from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_manual_order_mode = fields.Boolean(string='Manual Order Mode')
    sale_order_mode = fields.Selection(selection=[
        ('dtc', 'DTC'),
        ('mp', 'MP'),
        ('ws', 'WS'),
        ('sc', 'SC'),
    ], string='Sale Order Mode', related='partner_id.x_studio_sale_order_mode')
    sale_order_mode_manual = fields.Selection(selection=[
        ('dtc', 'DTC'),
        ('mp', 'MP'),
        ('ws', 'WS'),
        ('sc', 'SC'),
    ], string='Sale Order Mode')
    total_products = fields.Integer(string='Total Products', compute='_compute_total_product')
    total_qty = fields.Float(string='Total Quantitiy', compute='_compute_total_qty')
    dtc_type = fields.Selection(selection=[
        ('single', 'Single'),
        ('multi', 'Multi'),
        ('empty', 'Empty'),
    ], string="DTC Type", compute='_compute_dtc_type')
    dtc_note = fields.Char(string='DTC Note', compute='_compute_dtc_note')

    @api.multi
    @api.depends('order_line')
    def _compute_total_product(self):
        for order in self:
            order.total_products = len(self.order_line)

    @api.multi
    @api.depends('order_line.product_uom_qty')
    def _compute_total_qty(self):
        for order in self:
            qty = 0
            for line in order.order_line:
                qty += line.product_uom_qty
            order.total_qty = qty

    @api.multi
    @api.depends('total_products')
    def _compute_dtc_type(self):
        for order in self:
            if order.total_products == 0:
                order.dtc_type = 'empty'
            elif order.total_products == 1:
                order.dtc_type = 'single'
            else:
                order.dtc_type = 'multi'

    @api.multi
    @api.depends('dtc_type')
    def _compute_dtc_note(self):
        for order in self:
            if order.dtc_type == 'empty':
                order.dtc_note = 'Error'
            elif order.dtc_type == 'single':
                barcode = order.order_line[0].product_id.barcode or ''
                product_name = order.order_line[0].product_id.name
                templ = '[{}] [{}]' if barcode else '[{}]{}'
                order.dtc_note = templ.format(product_name, barcode)
            else:
                order.dtc_note = 'Multi Items'
