# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from odoo import api, fields, models
# from user.barcode_custom.models.gateway import Gateway

class Location(models.Model):
    _inherit = "stock.location"

    def get_user_preferences(self):
        return self.env['user.preferences'].search([('user_id', '=', self.env.user.id)])

    @api.multi
    def print_location_barcode(self):
        # user preferences with printers information
        user_preferences = self.get_user_preferences()
        user_name = user_preferences.name
        printer_type = user_preferences.print_node_ids.printer_type
        printer_location = user_preferences.print_node_ids.printer_location
        printer_node_code = user_preferences.print_node_ids.printer_node_code

        # create session with PrintNode via API call 
        PrintNodeAPIKey = '6zToIF7u9bXIVGfYQMsVUrRqeO45M1iuyug4Lz-LRLk'        
        gateway=Gateway(url='https://api.printnode.com',apikey=PrintNodeAPIKey)
        # list of printers
        printers = gateway.printers(computer=None, printer=None)
        for i in printers:
            printer_id = i.id
            if int(printer_id) == int(printer_node_code):
                exact_printer_node_code = printer_id
        # printjobs = gateway.printjobs(printer=printer_node_code)

        # generate pdf file 
        REPORT_ID = 'barcode_custom.action_report_custom_location_barcode'
        pdf = self.env.ref(REPORT_ID).render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        # create PrintJob on printer
        # print(gateway.PrintJob(printer=printer_node_code,options={"copies":1},base64=b64_pdf))
        # get PrintJob ID on this printer
        # printjob_id = gateway.printjobs(printer=printer_node_code)[0].id
        # get state of PrintJob
        # print(gateway.states(printjob_id)[0][0].state)