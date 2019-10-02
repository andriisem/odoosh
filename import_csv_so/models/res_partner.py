from odoo import _, api, fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    has_full_name = fields.Boolean(string='Complete Full Name')
    csv_number_customer_po = fields.Char(string='Customer PO #', required=True)
    csv_product_upc = fields.Char(string='Product UPC', required=True)
    csv_qty = fields.Char(string='Qty', required=True)
    csv_first_name = fields.Char(string='First Name')
    csv_last_name = fields.Char(string='Last Name')
    csv_full_name = fields.Char(string='Full Name')
    csv_company = fields.Char(string='Company')
    csv_address_line_one = fields.Char(string='Address Line 1', required=True)
    csv_address_line_two = fields.Char(string='Address Line 2')
    csv_city = fields.Char(string='City', required=True)
    csv_state = fields.Char(string='State', required=True)
    csv_zip = fields.Char(string='Zip Code', required=True)
    has_country = fields.Boolean(string='Set Country')
    csv_country = fields.Char(string='Country', required=True)
    csv_phone = fields.Char(string='Phone')
