from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    sale_order_mode = fields.Selection(selection=[
        ('dtc', 'DTC'),
        ('mp', 'MP'),
        ('ws', 'WS'),
        ('sc', 'SC'),
    ], string='Sale Order Mode')
    has_manual_shipping = fields.Boolean(string='Manual Shipping')
    dtc_rule = fields.Many2one('shipping.rule', string='DTC Rule')
    ws_rule = fields.Many2one('shipping.rule', string='WS Rule')
    mp_rule = fields.Many2one('shipping.rule', string='MP Rule')
    sc_rule = fields.Many2one('shipping.rule', string='SC Rule')
    
    has_do_not_crush = fields.Boolean(string='Do Not Crush')
    has_mixed = fields.Boolean(string='Mixed')
    has_box_content = fields.Boolean(string='Box Content')
    has_bag_content = fields.Boolean(string='Bag Content')
    has_box_label = fields.Boolean(string='Box Label')
    has_pallet_slip	 = fields.Boolean(string='Pallet Slip')
    has_bill_of_lading = fields.Boolean(string='Bill of Lading')
    has_packing_list = fields.Boolean(string='Packing List')
    has_commercial_invoice = fields.Boolean(string='Commercial Invoice')
