from odoo import _, api, fields, models


class ShippingRules(models.Model):
    _name = 'rule.shipping'
    _description = 'rule.shipping'

    name = fields.Char(string='Rule Name', required=True)
    ship_station_code = fields.Char(string='ShipStation Code')
    visible_rule = fields.Boolean(string='Visible Rule')
    description = fields.Char(string='Description')
    conditional_weight = fields.Boolean(string='Conditional Weight')
    max_weight = fields.Float(string='If above this weight (kg)')
    shipping_rule_id = fields.Many2one('rule.shipping', string='Use this Rule')