from odoo import api, fields, models, _


class ShipStationConfig(models.Model):
    _name = 'ship.station.config'

    name = fields.Char(string='Name')
    api_key = fields.Char(string='API Key')
    api_secret_key = fields.Char(string='API Secret Key')
