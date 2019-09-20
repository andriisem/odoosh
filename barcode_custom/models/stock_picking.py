from odoo import _, api, fields, models


class StockMove(models.Model):
    _inherit = 'stock.move'


    @api.multi
    def action_open_image(self):
        _id = self.product_id.product_tmpl_id.id
        menu_id = self.env.ref('stock.menu_stock_root').id
        base_url = self.env['ir.config_parameter'].get_param('web.base.url')
        record_url = base_url + "/web#id=" + str(_id) + "&view_type=form&model=product.template&menu_id=" + str(menu_id) + "&q=image"
        return {
            'name': _('Product'),
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': record_url,
        }

    @api.multi
    def action_print_custom_barcode(self):
        self.product_id.product_tmpl_id.print_custom_barcode()
