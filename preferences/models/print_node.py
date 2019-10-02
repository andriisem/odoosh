# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import models, fields, api

class UserPreferences(models.Model):
    _name = 'user.preferences'
    _description = 'user.preferences'

    user_id = fields.Many2one('res.users', string='User Name', track_visibility='onchange', default=lambda self: self.env.user)
    name = fields.Char('User Name', related='user_id.name', readonly=True)
    office = fields.Many2one('print.node', string='Office')
    document = fields.Many2one('print.node', string='Document')
    zebra = fields.Many2one('print.node', string='Zebra')
    dymo = fields.Many2one('print.node', string='Dymo')
    print_node_ids = fields.One2many('print.node', 'user_id', string='Print Nodes')

class PrintNode(models.Model):
    _name = 'print.node'
    _description = 'print.node'
    
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
