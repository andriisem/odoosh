# -*- coding: utf-8 -*-

from odoo import api, fields, models, _
from odoo.exceptions import Warning

class PurchaseOrderLine(models.Model):
    _inherit = 'purchase.order.line'

    # @api.multi
    @api.onchange('product_id', 'partner_id')
    def onchange_product_id(self):
        result = super(PurchaseOrderLine, self).onchange_product_id()

        supplier_infos = self.env['product.supplierinfo'].search([('name', '=', self.partner_id.id)])
        product_ids = self.env['product.product']
        for supplier_info in supplier_infos:
            product_ids += supplier_info.product_tmpl_id.product_variant_ids

        result.update({'domain': {'product_id': ['&', ('id', 'in', product_ids.ids), ('purchase_ok', '=', True)]}})

        return result