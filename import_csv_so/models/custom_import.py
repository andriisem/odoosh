import csv
import json

from io import StringIO
from datetime import datetime
from odoo import _, api, fields, models


class CustomImport(models.Model):
    _name = 'custom_csv.import'

    res_model = fields.Char('Model')
    file = fields.Binary('File', help="File to check and/or import, raw binary (not base64)")
    file_name = fields.Char('File Name')
    file_type = fields.Char('File Type')
    
    @api.model
    def get_fields(self, partner_id):
        partner_id = self.env['res.partner'].browse(partner_id)
        return {
            'csv_number_customer_po': partner_id.csv_number_customer_po,
            'csv_product_upc': partner_id.csv_product_upc,
            'csv_qty': partner_id.csv_qty,
            'csv_first_name': partner_id.csv_first_name,
            'csv_last_name': partner_id.csv_last_name,
            'csv_full_name': partner_id.csv_full_name,
            'csv_company': partner_id.csv_company,
            'csv_address_line_one': partner_id.csv_address_line_one,
            'csv_address_line_two': partner_id.csv_address_line_two,
            'csv_city': partner_id.csv_city,
            'csv_state': partner_id.csv_state,
            'csv_zip': partner_id.csv_zip,
            'csv_country': partner_id.csv_country,
            'csv_phone': partner_id.csv_phone,
        }
    
    @api.model
    def get_product(self, upc):
        return self.env['product.product'].search([('barcode', '=', upc)], limit=1)

    @api.multi
    def parse_preview(self, partner_id):
        self.ensure_one()
        try:
            all_data = []
            msg_error = ''
            error = False
            csv_number_customer_po = '' 
            fields = self.get_fields(partner_id)
            f = StringIO(self.file.decode("utf-8"))
            reader_list = csv.DictReader(f, delimiter=',')
            for row in reader_list:
                row_data = {}
                product_id = self.get_product(row.get(fields['csv_product_upc']))
                if not product_id:
                    error = True
                if not row.get(fields['csv_number_customer_po']):
                    continue
                if csv_number_customer_po != row.get(fields['csv_number_customer_po']):
                    row_data['csv_number_customer_po'] = row.get(fields['csv_number_customer_po'])
                    row_data['csv_first_name'] = row.get(fields['csv_first_name'])
                    row_data['csv_last_name'] = row.get(fields['csv_last_name'])
                    row_data['csv_full_name'] = row.get(fields['csv_full_name'])
                    row_data['csv_company'] = row.get(fields['csv_company'])
                    row_data['csv_address_line_one'] = row.get(fields['csv_address_line_one'])
                    row_data['csv_address_line_two'] = row.get(fields['csv_address_line_two'])
                    row_data['csv_city'] = row.get(fields['csv_city'])
                    row_data['csv_state'] = row.get(fields['csv_state'])
                    row_data['csv_zip'] = row.get(fields['csv_zip'])
                    row_data['csv_country'] = row.get(fields['csv_country'])
                    row_data['csv_phone'] = row.get(fields['csv_phone'])
                    order_line = {}
                    order_line['csv_product_upc'] = row.get(fields['csv_product_upc'])
                    order_line['csv_qty'] = row.get(fields['csv_qty'])
                    order_line['product_name'] = product_id.name
                    order_line['product_id'] = product_id.id
                    row_data['order_lines'] = [order_line]
                    all_data.append(row_data)
                else:
                    order_line = {}
                    order_line['csv_product_upc'] = row.get(fields['csv_product_upc'])
                    order_line['csv_qty'] = row.get(fields['csv_qty'])
                    order_line['product_name'] = product_id.name
                    order_line['product_id'] = product_id.id
                    all_data[len(all_data) - 1]['order_lines'].append(order_line)

                csv_number_customer_po = row.get(fields['csv_number_customer_po'])
        except Exception as e:
            error = True
            msg_error = e

        return {
            'fields': self.file,
            'preview': all_data,
            'error': error,
            'msg_error': msg_error,
            }
    
    @api.model
    def create_so(self, preview, partner_id):
        SaleOrder = self.env['sale.order']
        SaleOrderLine = self.env['sale.order.line']
        timestamp = int(datetime.now().timestamp())
        list_so = []
        for so in preview:
            sale_order_id = SaleOrder.create({
                'partner_id': partner_id.id,
                'csv_batch_number': timestamp,
                'csv_number_customer_po': so.get('csv_number_customer_po'),
                'csv_first_name': so.get('csv_first_name'),
                'csv_last_name': so.get('csv_last_name'),
                'csv_full_name': so.get('csv_full_name'),
                'csv_company': so.get('csv_company'),
                'csv_address_line_one': so.get('csv_address_line_one'),
                'csv_address_line_two': so.get('csv_address_line_two'),
                'csv_city': so.get('csv_city'),
                'csv_state': so.get('csv_state'),
                'csv_zip': so.get('csv_zip'),
                'csv_phone': so.get('csv_phone'),
            })
            list_so.append(sale_order_id.id)
            for line in so.get('order_lines'):
                product_id = self.env['product.product'].browse(line.get('product_id'))
                SaleOrderLine.create({
                    'name': product_id.name,
                    'product_id': product_id.id,
                    'product_uom_qty': line.get('csv_qty'),
                    'product_uom': product_id.uom_id.id,
                    'price_unit': product_id.list_price,
                    'order_id': sale_order_id.id,
                    'tax_id': [(6, 0, product_id.taxes_id.ids)],
                })
        return list_so

    @api.multi
    def csv_import_so(self, preview, partner):
        partner_id = self.env['res.partner'].browse(partner)
        list_so = self.create_so(preview.get('preview'), partner_id)
        return list_so
