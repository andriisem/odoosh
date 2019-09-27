from odoo import _, api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    csv_batch_number = fields.Char(string='CSV BATCH #')
    csv_number_customer_po = fields.Char(string='PO #')
    csv_first_name = fields.Char(string='First Name')
    csv_last_name = fields.Char(string='Last Name')
    csv_full_name = fields.Char(string='Full Name')
    csv_company = fields.Char(string='Company')
    csv_address_line_one = fields.Char(string='Address Line 1')
    csv_address_line_two = fields.Char(string='Address Line 2')
    csv_city = fields.Char(string='City')
    csv_state = fields.Char(string='State')
    csv_zip = fields.Char(string='Zip Code')
    csv_country = fields.Char(string='Country')
    csv_phone = fields.Char(string='Phone')
