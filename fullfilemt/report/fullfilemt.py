from odoo import tools
from odoo import _, api, fields, models


class Fullfilemt(models.Model):
    _name = 'fullfilemt'
    _auto = False
    _rec_name = 'id'
    _order = 'due_date'

    name = fields.Char(string='Name', readonly=True)
    product_name = fields.Char(string='Product Name')
    product_sku = fields.Char(string='Product SKU')
    product_upc = fields.Char(string='Product UPC')
    same_orders = fields.Integer(string='# of orders')
    color = fields.Char(string='Color', compute='_compute_color')
    total_products = fields.Integer(string='Total Products')
    total_qty = fields.Float(string='Total Quantitiy')
    number_customer_po = fields.Char(string='PO #')
    due_date = fields.Datetime(string='Due Date')
    partner_id = fields.Many2one('res.partner', string='Partner')
    stage_id = fields.Many2one('fullfilemt.stage', string='Stage', ondelete='restrict', track_visibility='onchange',
                               index=True, group_expand='_read_group_stage_ids', readonly=True)
    all_dtc_multi_orders = fields.Integer(
        string='#of orders', compute='_compute_dtc_multi_attrs')
    all_dtc_multi_product = fields.Integer(
        string='#of products', compute='_compute_dtc_multi_attrs')
    all_dtc_multi_qty = fields.Float(
        string='Total Quantity', compute='_compute_dtc_multi_attrs')
    dtc_multi_due_date = fields.Datetime(
        string='Due Date', compute='_compute_dtc_multi_attrs')

    def _compute_dtc_multi_attrs(self):
        for card in self:
            if card.name == 'multi':
                sale_ids = self.env['sale.order'].search([
                    ('backorders', '=', False),
                    ('state', '=', 'sale'),
                    ('dtc_type', '=', 'multi')
                ])
                due_date = sale_ids.filtered(
                    lambda r: r.due_date != False).mapped('due_date')
                card.all_dtc_multi_orders = len(sale_ids)
                all_dtc_multi_product = 0
                all_dtc_multi_qty = 0
                for order in sale_ids:
                    all_dtc_multi_product += order.total_products
                    all_dtc_multi_qty += order.total_qty
                card.all_dtc_multi_product = all_dtc_multi_product
                card.all_dtc_multi_qty = all_dtc_multi_qty
                card.dtc_multi_due_date = min(due_date) if due_date else False

    @api.model_cr
    def init(self):
        cr = self._cr
        tools.drop_view_if_exists(self.env.cr, self._table)
        cr.execute("""
            CREATE VIEW fullfilemt AS (
                SELECT
                    o.id,
                    o.name,
                    o.csv_number_customer_po as number_customer_po,
                    o.due_date,
                    o.partner_id,
                    o.total_products,
                    o.same_orders,
                    o.total_qty,
                    o.stage_id,
                    pt.name as product_name,
                    pt.sku as product_sku,
                    p.barcode as product_upc
                FROM
                    "sale_order" o
                    JOIN "fullfilemt_stage" s ON (o.stage_id = s.id)
                    JOIN "sale_order_line" l ON (o.id = l.order_id)
                    JOIN "product_product" p ON (l.product_id = p.id)
                    JOIN "product_template" pt ON (p.product_tmpl_id = pt.id) 
                        WHERE o.state = 'sale' AND o.stage_id = s.id
            UNION
                SELECT
                    m.id,
                    m.name,
                    m.number_customer_po,
                    m.due_date,
                    m.partner_id,
                    m.total_products,
                    m.same_orders,
                    m.total_qty,
                    m.stage_id,
                    m.product_name,
                    m.product_sku,
                    m.product_upc
                FROM
                    "fullfilemt_multi" m
                )""",)

    @api.multi
    def _compute_color(self):
        for card in self:
            if card.name != 'multi':
                sale_id = self.env['sale.order'].search(
                    [('name', '=', card.name)], limit=1)
                available_item = 0
                for line in sale_id.order_line:
                    available_item += line.product_id.qty_available
                if available_item == 0:
                    card.color = 'none'
                elif available_item > 0 and available_item < sale_id.total_qty:
                    card.color = 'middle'
                else:
                    card.color = 'full'

    @api.model
    def _read_group_stage_ids(self, states, domain, order):
        stage_ids = self.env['fullfilemt.stage'].search([])
        return stage_ids

    @api.model
    def action_check_availability(self):
        pass
