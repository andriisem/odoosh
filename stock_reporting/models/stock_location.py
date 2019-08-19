# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _

class Location(models.Model):
    _inherit = "stock.location"
    
    counted = fields.Char('Counted', compute="_compute_counted", default='NO')
    move_ids = fields.One2many(
        'stock.move', 'location_id', string='Created Moves')

    @api.depends('move_ids')
    def _compute_counted(self):
        context = self.env.context
        before_counting = datetime.strptime(context.get('before_counting'), '%Y-%m-%d %H:%M:%S')
        counting_day = datetime.strptime(context.get('counting_day'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            move_ids_create_date_list = [i.create_date for i in record.move_ids]
            result = list(filter(lambda x: x > before_counting and x < counting_day, move_ids_create_date_list))
            if len(result) > 0:
                record.counted = 'YES'
            else:
                record.counted = 'NO'