# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class UserPreferences(models.Model):
    _name = 'user.preferences'

    user_id = fields.Many2one('res.users', string='User Name', track_visibility='onchange', default=lambda self: self.env.user)
    name = fields.Char('User Name', related='user_id.name', readonly=True)
    office = fields.Many2one('print.node', string='Office')
    document = fields.Many2one('print.node', string='Document')
    zebra = fields.Many2one('print.node', string='Zebra')
    dymo = fields.Many2one('print.node', string='Dymo')
    print_node_ids = fields.One2many('print.node', 'user_id', string='Print Nodes')

class PrintNode(models.Model):
    _name = 'print.node'

    name = fields.Char(string='Printer Name')
    printer_location = fields.Selection(string='Printer Location', selection=[
            ('hawtorne', 'Hawtorne, CA'),
            ('nyc', 'NYC'),
        ])
    printer_type = fields.Selection(string='Printer Type', selection=[
            ('zebra', 'Zebra 4×6'),
            ('dymo', 'Dymo 3×1'),
            ('office', 'Office Letter Size'),
        ])
    printer_node_code = fields.Char(string='Printer Node Code')
    user_id = fields.Many2one(
        'user.preferences', 'User Preferences',
        index=True, ondelete='cascade')

class ShippingRules(models.Model):
    _name = 'shipping.rules'

    name = fields.Char(string='Rule Name')
    description = fields.Char(string='Description')    
    carrier = fields.Selection(string='Carrier', selection=[
            ('fedex', 'FedEx'),
            ('ups', 'UPS'),
            ('usps', 'USPS'),
            ('dhl', 'DHL'),
        ])
    shipping_method = fields.Selection(string='Shipping Method', selection=[
            ('fedex_ground', 'FedEx Ground'),
            ('fedex_home_delivery', 'FedEx Home Delivery'),
            ('fedex_smart_post', 'FedEx Smart Post'),
            ('fedex_inter_economy', 'FedEx International Economy'),
            ('fedex_express_saver', 'FedEx Express Saver'),
            ('fedex_standard_overnight', 'FedEx Standard Overnight'),
            ('fedex_2nd_day', 'FedEx 2nd Day'),
            ('ups_ground', 'UPS Ground'),
            ('ups_sure_post', 'UPS SurePost'),
            ('ups_2day_delivery', 'UPS 2 DAY Delivery'),
            ('ups_overnight', 'UPS OVERNIGHT'),            
        ])
    third_party_account = fields.Char(string='3rd Party Account')
    third_party_account_zipcode = fields.Char(string='3rd Party Account Zipcode')
    conditional_weight = fields.Boolean(string='Conditional Weight', default=False)
    visible_rule = fields.Boolean(string='Visible Rule', default=False)    