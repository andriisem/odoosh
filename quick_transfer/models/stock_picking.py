# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api

class Picking(models.Model):
    _inherit = 'stock.picking'

    custom_location_id = fields.Many2one(
        'stock.location', "Source Location",
        )
    custom_location_dest_id = fields.Many2one(
        'stock.location', "Destination Location",
        )
    date_expected = fields.Datetime(
        'Expected Date', default=fields.Datetime.now, index=True, required=True,
        states={'done': [('readonly', True)]},
        help="Scheduled date for the processing of this move")
    location_id = fields.Many2one(
        'stock.location', 'Source Location',
        index=True, required=True,
        help="Sets a location if you produce at a fixed location. This can be a partner location if you subcontract the manufacturing operations.", related="custom_location_id")
    location_dest_id = fields.Many2one(
        'stock.location', 'Destination Location',
        index=True, required=True,
        help="Location where the system will stock the finished products.", related="custom_location_dest_id")

    # @api.depends('custom_location_id')
    # def _compute_location_id(self):
    #     for record in self:
    #         record.location_id  = record.custom_location_id

    # @api.depends('custom_location_dest_id')
    # def _compute_location_dest_id(self):
    #     for record in self:
    #         record.location_dest_id  = record.custom_location_dest_id

    # @api.multi
    # def write(self, values):
    #     res = super(Picking, self).write(values)
    #     context = self.env.context
    #     print(context)
    #     return res

    # @api.multi
    # def action_done(self, context):
    #     """Changes picking state to done by processing the Stock Moves of the Picking

    #     Normally that happens when the button "Done" is pressed on a Picking view.
    #     @return: True
    #     """
    #     # TDE FIXME: remove decorator when migration the remaining
    #     print(context)
    #     product_id = self.env['product.product'].search([('id', '=', context.get('default_product_id'))])
    #     product_uom_qty = context.get('default_product_uom_qty')
    #     location_id = context.get('default_location_id')
    #     location_dest_id = context.get('default_location_dest_id')
    #     picking_id = context.get('default_picking_id')
    #     picking_type_id = context.get('default_picking_type_id')
    #     product_uom_id = context.get('default_product_uom')
    #     new_move = self.env['stock.move'].create({
    #                         'name': _('New Move:') + product_id.display_name,
    #                         'product_id': product_id.id,
    #                         'product_uom_qty': product_uom_qty,
    #                         'product_uom': product_uom_id,
    #                         'location_id': location_id,
    #                         'location_dest_id': location_dest_id,
    #                         'picking_id': picking_id,
    #                         'picking_type_id': picking_type_id,
    #                        })
    #     print(new_move)
    #     # move_id = new_move.id
    #     # new_move._action_confirm()
    #     # todo_moves |= new_move
    #     #'qty_done': ops.qty_done})
    #     # todo_moves._action_done()
    #     # self.write({'date_done': fields.Datetime.now()})
    #     return True