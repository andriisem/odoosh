# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime 
from odoo import api, fields, models, _

class Inventory(models.Model):
    _inherit = "stock.inventory"
    _description = "Inventory"
    _order = "date desc, id desc"

    name = fields.Char(
        'Inventory Reference',
        readonly=True, required=False,
        states={'draft': [('readonly', False)]}, compute='_compute_cycle_count_name')

    cycle_count_name = fields.Char(
        'Inventory Reference',
        readonly=True, required=True,
        states={'draft': [('readonly', False)]}, default=lambda self: self.env.user.partner_id.name + datetime.now().strftime("%Y-%m-%d-%H:%M:%S"),)

    cycle_count_filter = fields.Selection(
        string='Inventory of', selection='_selection_filter_cycle_count',
        required=True,
        default='none',
        help="If you do an entire inventory, you can choose 'All Products' and it will prefill the inventory with the current stock.  If you only do some products  "
             "(e.g. Cycle Counting) you can choose 'Manual Selection of Products' and the system won't propose anything.  You can also let the "
             "system propose for a single product / lot /... ")

    location_id = fields.Many2one(
        'stock.location', 'Inventoried Location',
        readonly=True, required=True,
        states={'draft': [('readonly', False)]},
        default=None)

    def _compute_cycle_count_name(self):
        for record in self:
            record.name = record.cycle_count_name

    @api.model
    def _selection_filter_cycle_count(self):
        """ Get the list of filter allowed according to the options checked
        in 'Settings\Warehouse'. """
        res_filter = [
            ('none', _('All products')),]
        return res_filter

    @api.multi
    def cycle_count_action_start(self):
        for inventory in self.filtered(lambda x: x.state not in ('done','cancel')):
            vals = {'state': 'confirm', 'date': fields.Datetime.now()}
            if (inventory.filter != 'partial') and not inventory.line_ids:
                vals.update({'line_ids': [(0, 0, line_values) for line_values in inventory.cycle_count_get_inventory_lines_values()]})
            inventory.write(vals)
        tree_view_id = self.env.ref('stock.view_inventory_tree').id
        form_view_id = self.env.ref('cycle_count.cycle_count_view_inventory_form').id
        return {
            'name': _('Inventory Adjustments'),
            'type': 'ir.actions.act_window',
            'views': [(form_view_id, 'form'), (tree_view_id, 'tree'),],
            'view_mode': 'tree, form',
            'view_type': 'form',
            'target': 'current',
            'res_id': inventory.id,
            'res_model': 'stock.inventory',
            'context': {'form_view_initial_mode': 'edit', 'force_detailed_view': 'true'},
        }

    def cycle_count_get_inventory_lines_values(self):
        # TDE CLEANME: is sql really necessary ? I don't think so
        locations = self.env['stock.location'].search([('id', 'child_of', [self.location_id.id])])
        domain = ' location_id in %s AND quantity != 0 AND active = TRUE'
        args = (tuple(locations.ids),)

        vals = []
        Product = self.env['product.product']
        # Empty recordset of products available in stock_quants
        quant_products = self.env['product.product']
        # Empty recordset of products to filter
        products_to_filter = self.env['product.product']

        # case 0: Filter on company
        if self.company_id:
            domain += ' AND company_id = %s'
            args += (self.company_id.id,)

        #case 1: Filter on One owner only or One product for a specific owner
        if self.partner_id:
            domain += ' AND owner_id = %s'
            args += (self.partner_id.id,)
        #case 2: Filter on One Lot/Serial Number
        if self.lot_id:
            domain += ' AND lot_id = %s'
            args += (self.lot_id.id,)
        #case 3: Filter on One product
        if self.product_id:
            domain += ' AND product_id = %s'
            args += (self.product_id.id,)
            products_to_filter |= self.product_id
        #case 4: Filter on A Pack
        if self.package_id:
            domain += ' AND package_id = %s'
            args += (self.package_id.id,)
        #case 5: Filter on One product category + Exahausted Products
        if self.category_id:
            categ_products = Product.search([('categ_id', 'child_of', self.category_id.id)])
            domain += ' AND product_id = ANY (%s)'
            args += (categ_products.ids,)
            products_to_filter |= categ_products

        self.env.cr.execute("""SELECT product_id, sum(quantity) as product_qty, location_id, lot_id as prod_lot_id, package_id, owner_id as partner_id
            FROM stock_quant
            LEFT JOIN product_product
            ON product_product.id = stock_quant.product_id
            WHERE %s
            GROUP BY product_id, location_id, lot_id, package_id, partner_id """ % domain, args)

        for product_data in self.env.cr.dictfetchall():
            # replace the None the dictionary by False, because falsy values are tested later on
            for void_field in [item[0] for item in product_data.items() if item[1] is None]:
                product_data[void_field] = False
            product_data['theoretical_qty'] = product_data['product_qty']
            if product_data['product_id']:
                product_data['product_uom_id'] = Product.browse(product_data['product_id']).uom_id.id
                quant_products |= Product.browse(product_data['product_id'])
            vals.append(product_data)
        if self.exhausted:
            exhausted_vals = self._get_exhausted_inventory_line(products_to_filter, quant_products)
            vals.extend(exhausted_vals)
        cycle_count_values = []
        for i in vals:
            if i['theoretical_qty'] >= 1:
                i['product_qty'] = i['theoretical_qty']
                cycle_count_values.append(i)         
        return cycle_count_values