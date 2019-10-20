from odoo import tools
from odoo import _, api, fields, models
from odoo.exceptions import UserError


class FullfilemtCheckAavailability(models.Model):
    _name = 'fullfilemt.check.availability'
    _description = 'fullfilemt.check.availability'
    _auto = False
    _rec_name = 'id'

    name = fields.Char(string='Product Name')
    barcode = fields.Char(string='UPC')
    of_orders = fields.Float(string='For # of orders', compute='_compute_qty')
    qty_needed = fields.Float(string='Qty Needed', compute='_compute_qty')
    qty_in_stock = fields.Float(string='Qty in Stock', compute='_compute_qty')
    qty_on_order = fields.Float(string='Qty on Order', compute='_compute_qty')
    qty_requested = fields.Float(string='Qty Requested', compute='_compute_qty')
    missing_qty = fields.Float(string='Missing Qty', compute='_compute_qty')

    @api.model_cr
    def init(self):
        cr = self._cr
        tools.drop_view_if_exists(self.env.cr, self._table)
        cr.execute("""
            CREATE VIEW fullfilemt_check_availability AS (
                SELECT 
                    DISTINCT ON (name) l.name,
                    l.id,
                    p.barcode
                FROM
                    "sale_order_line" l
                    JOIN "sale_order" o  ON (l.order_id = o.id)
                    JOIN "product_product" p ON (l.product_id = p.id)
                    WHERE o.state = 'sale'
                GROUP BY l.id, l.name, p.barcode
                )""",)

    @api.multi
    def _compute_qty(self):
        for card in self:
            sale_ids = self.env['sale.order'].search([
                ('state', '=', 'sale'),
                ('order_line.name', '=', card.name)
            ])
            confirm_purchase_ids = self.env['purchase.order'].search([
                ('order_line.name', '=', card.name),
                ('state', '=', 'purchase')
            ])
            all_purchase_ids = self.env['purchase.order'].search([
                ('order_line.name', '=', card.name)
            ])
            qty_needed = 0
            for order in sale_ids:
                order_line = order.order_line.filtered(lambda x: x.name == card.name)
                qty_needed += order_line.product_uom_qty
                qty_in_stock = order_line.product_id.qty_available
            card.of_orders = len(sale_ids)
            card.qty_needed = qty_needed
            card.qty_in_stock = qty_in_stock
            card.qty_on_order = len(confirm_purchase_ids)
            card.qty_requested = len(all_purchase_ids)
            card.missing_qty = card.qty_needed - card.qty_in_stock - card.qty_requested

    @api.multi
    def action_request_po(self):
        Purchase = self.env['purchase.order']
        product_id = self.env['product.product'].search([
            ('name', '=', self.name),
            ('barcode', '=', self.barcode)
        ])
        if product_id and product_id.purchase_ok and product_id.seller_ids:
            supplierinfo = product_id.seller_ids[0]
        else:
            raise UserError(_("Product: %s doesn't have a seller") % (self.name))

        Purchase.create({
            'partner_id': supplierinfo.name.id,
            'order_line': [
                (0, 0, {
                    'name': product_id.name,
                    'product_id': product_id.id,
                    'product_qty': self.missing_qty,
                    'product_uom': product_id.uom_po_id.id,
                    'price_unit': supplierinfo.price,
                    'date_planned': fields.Datetime.now(),
                })]
        })

    @api.multi
    def action_request_all(self):
        fullfilemt = self.env['fullfilemt.check.availability'].search([])
        for line in fullfilemt:
            if line.missing_qty > 0:
                line.action_request_po()
