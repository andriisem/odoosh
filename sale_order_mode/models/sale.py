from odoo import _, api, fields, models

OUNCE = 35.274


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    has_manual_order_mode = fields.Boolean(string='Manual Order Mode')
    sale_order_mode = fields.Selection(selection=[
        ('dtc', 'DTC'),
        ('mp', 'MP'),
        ('ws', 'WS'),
        ('sc', 'SC'),
    ], string='Sale Order Mode', related='partner_id.sale_order_mode')
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
    order_total_weight_kg = fields.Float(string='Order Total Weight (KG)', 
        compute='_compute_order_total_weight_kg')
    order_total_weight_oz = fields.Float(string='Order Total Weight (OZ)', 
        compute='_compute_order_total_weight_oz')
    # order_shipping_rule = fields.Many2one('shipping.rule', string='Order Shipping Rule', compute='_compute_order_shipping_rule')
    # shipping_rule_code = fields.Char(string='Shipping Rule Code', related='order_shipping_rule.ship_station_code')


    # @api.depends('sale_order_mode', 'sale_order_mode_manual')
    # def _compute_order_shipping_rule(self):
    #     for order in self:
    #         if not order.partner_id.has_manual_shipping:
    #             if order.partner_id.sale_order_mode == 'dtc':
    #                 order.order_shipping_rule = order.partner_id.dtc_rule.id
    #             elif order.partner_id.sale_order_mode == 'mp':
    #                 order.order_shipping_rule = order.partner_id.mp_rule.id
    #             elif order.partner_id.sale_order_mode == 'ws':
    #                 order.order_shipping_rule = order.partner_id.ws_rule.id
    #             elif order.partner_id.sale_order_mode == 'sc':
    #                 order.order_shipping_rule = order.partner_id.sc_rule.id
    #         if order.order_shipping_rule and order.order_shipping_rule.max_weight < order.order_total_weight_kg:
    #             order.order_shipping_rule = order.order_shipping_rule.shipping_rule_id.id            

    @api.multi
    @api.depends('order_line')
    def _compute_order_total_weight_kg(self):
        for order in self:
            weight = 0
            for line in order.order_line:
                weight += (line.product_id.weight * line.product_uom_qty)
            order.order_total_weight_kg = weight
    
    @api.depends('order_total_weight_kg')
    def _compute_order_total_weight_oz(self):
        for order in self:
            order.order_total_weight_oz = order.order_total_weight_kg * OUNCE

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
