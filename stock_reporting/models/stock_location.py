# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _

class Location(models.Model):
    _inherit = "stock.location"
    
    counted = fields.Char('Counted', compute="_compute_counted", default='No')

    @api.depends('write_date')
    def _compute_counted(self):
        context = self.env.context
        before_counting = datetime.strptime(context.get('before_counting'), '%Y-%m-%d %H:%M:%S')
        counting_day = datetime.strptime(context.get('counting_day'), '%Y-%m-%d %H:%M:%S')
        for record in self:
            if record.write_date > before_counting and record.write_date < counting_day:
                record.counted = 'YES'
            else:
                record.counted = 'NO'