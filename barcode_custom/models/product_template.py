# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models, _
from odoo.exceptions import UserError

from ..printnodeapi import Gateway


class ProductTemplate(models.Model):
    _inherit = "product.template"

    sku = fields.Char('SKU')

    def get_user_preferences(self):
        return self.env['user.preferences'].search([('user_id', '=', self.env.user.id)])

    def get_api_key(self):
        apikey = self.env['ir.config_parameter'].sudo().get_param('printnode.api_key')
        if not apikey:
            raise UserError(_('''API key for PrintNode required.\n
                                Save this key in System Parameters with key: printnode.api_key, value: <your api key>
                                Visit https://app.printnode.com/apikeys for more information.
                            '''))
        return apikey

    @api.multi
    def print_bin_label(self):
        # user preferences with printers information
        apikey = self.get_api_key()
        user_preferences = self.get_user_preferences()
        zebra_code = int(user_preferences.zebra.printer_node_code)
        if not user_preferences and user_preferences.zebra:
            raise UserError(_('Printer code not found, check Preferences / Printers'))
        gateway = Gateway(url='https://api.printnode.com', apikey=apikey)
        try:
            printer = gateway.printers(printer=zebra_code)
        except LookupError:
            raise UserError(_('No printer with ID ' + str(zebra_code)))

        pdf_barcode = self.env.ref('barcode_custom.action_product_template_zebra').render_qweb_pdf(self.ids)
        print_job = gateway.PrintJob(printer=zebra_code, options={"copies":1}, binary=pdf_barcode[0])
        state = gateway.states(print_job.id)[0][0].state
        msg = """
            PrintJob: {} 
            Computer: {}
            Printer: {}
            State:{}
            """.format(print_job.id, printer.computer.name, printer.name, state)
        self.message_post(body=msg)
    
    @api.multi
    def print_custom_barcode(self):
        apikey = self.get_api_key()
        user_preferences = self.get_user_preferences()
        dymo_code = int(user_preferences.dymo.printer_node_code)
        if not user_preferences and user_preferences.dymo:
            raise UserError(_('Printer code not found, check  Preferences / Printers'))
        gateway = Gateway(url='https://api.printnode.com', apikey=apikey)

        try:
            printer = gateway.printers(printer=dymo_code)
        except LookupError:
            raise UserError(_('No printer with ID ' + str(dymo_code)))
        
        pdf_barcode = self.env.ref('barcode_custom.action_product_template_custom').render_qweb_pdf(self.ids)
        print_job = gateway.PrintJob(printer=dymo_code, options={"copies":1}, binary=pdf_barcode[0])
        state = gateway.states(print_job.id)[0][0].state
        msg = """
            PrintJob: {} 
            Computer: {}
            Printer: {}
            State:{}
            """.format(print_job.id, printer.computer.name, printer.name, state)
        self.message_post(body=msg)
