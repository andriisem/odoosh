# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime 
from odoo import api, fields, models, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError
from odoo.tools import float_utils, float_compare


class Inventory(models.Model):
    _inherit = "stock.inventory"
    _description = "Inventory"
    _order = "date desc, id desc"

    name = fields.Char(
        'Inventory Reference',
        readonly=True, required=True,
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