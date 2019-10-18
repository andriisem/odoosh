from odoo import _, api, fields, models


class FullfilemtStage(models.Model):
    _name = 'fullfilemt.stage'

    name = fields.Char(string='Name')
    sequence = fields.Integer('Sequence', default=10)

class FullfilemtMulti(models.Model):
    _name = 'fullfilemt.multi'
    
    name = fields.Char(string='Name')
    stage_id = fields.Many2one('fullfilemt.stage', string='Stage')
    product_name = fields.Char(string='Product Name')
    product_sku = fields.Char(string='Product SKU')
    product_upc = fields.Char(string='Product UPC')
    same_orders = fields.Integer(string='# of orders')
    total_products = fields.Integer(string='Total Products')
    total_qty = fields.Float(string='Total Quantitiy')
    number_customer_po = fields.Char(string='PO #')
    due_date = fields.Datetime(string='Due Date')
    partner_id = fields.Many2one('res.partner', string='Partner')
    all_dtc_multi_orders = fields.Integer(string='#of orders')
    all_dtc_multi_product = fields.Integer(string='#of products')
    all_dtc_multi_qty = fields.Float(string='Total Quantity')
    dtc_multi_due_date = fields.Datetime(string='Due Date')
