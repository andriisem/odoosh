# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

import base64
from odoo import api, fields, models
import json

import requests

from .auth import Auth, Unauthorized
from .model import ModelFactory
from .accounts import Accounts
from .computers import Computers
from .util import camel_to_underscore


class Gateway:

    URL = 'https://api.printnode.com'

    def __init__(self, **kwargs):
        url = kwargs.pop('url', self.URL)
        self._auth = Auth(url=url, **kwargs)
        self._factory = ModelFactory()
        self._accounts = Accounts(self._auth, self._factory)
        self._computers = Computers(self._auth, self._factory)

    @property
    def account(self):
        server_account = self._auth.get('whoami')
        return self._factory.create_account(server_account)

    @property
    def computers(self):
        return self._computers.get_computers

    @property
    def printers(self):
        return self._computers.get_printers

    @property
    def printjobs(self):
        return self._computers.get_printjobs

    @property
    def scales(self):
        return self._computers.get_scales

    @property
    def tag(self):
        return self._accounts.get_tag

    @property
    def api_key(self):
        return self._accounts.get_api_key

    @property
    def clientkey(self):
        return self._accounts.get_clientkey

    @property
    def clients(self):
        return self._accounts.get_clients

    @property
    def states(self):
        return self._computers.get_states

    def PrintJob(self, *args, **kwargs):
        printjob_id = self._computers.submit_printjob(*args, **kwargs)
        printjob = self.printjobs(printjob=printjob_id)
        return printjob

    def TestDataGenerate(self):
        self._auth.get('test/data/generate')

    def TestDataDelete(self):
        self._auth.delete('test/data/generate')

    def ModifyTag(self, tagname, tagvalue):
        tag = self._accounts.modify_tag(tagname, tagvalue)
        return tag

    def DeleteTag(self, tagname):
        tag = self._accounts.delete_tag(tagname)
        return tag

    def CreateAccount(self, **kwargs):
        acc_post = self._accounts.create_account(**kwargs)
        return acc_post

    def ModifyAccount(self, **kwargs):
        acc_id = self._accounts.modify_account(**kwargs)
        return self._factory.create_account(acc_id)

    def DeleteAccount(self, **kwargs):
        boolean = self._accounts.delete_account(**kwargs)
        return boolean

    def DeleteApiKey(self, api_key):
        key = self._accounts.delete_api_key(api_key)
        return key

    def CreateApiKey(self, api_key):
        key = self._accounts.create_api_key(api_key)
        return key

    def ModifyClientDownloads(self, client_id, enabled):
        clients = self._accounts.modify_client_downloads(client_id, enabled)
        return clients

Gateway = Gateway()

class ProductTemplate(models.Model):
    _inherit = "product.template"

    sku = fields.Char('SKU')

    def get_user_preferences(self):
        return self.env['user.preferences'].search([('user_id', '=', self.env.user.id)])

    @api.multi
    def print_bin_label(self):
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
        REPORT_ID = 'barcode_custom.action_product_template_zebra'
        pdf = self.env.ref(REPORT_ID).render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        # create PrintJob on printer
        # print(gateway.PrintJob(printer=printer_node_code,options={"copies":1},base64=b64_pdf))
        # get PrintJob ID on this printer
        # printjob_id = gateway.printjobs(printer=printer_node_code)[0].id
        # get state of PrintJob
        # print(gateway.states(printjob_id)[0][0].state)

    @api.multi
    def print_custom_barcode(self):
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
        print(printers)
        # printjobs = gateway.printjobs(printer=printer_node_code)

        # generate pdf file 
        REPORT_ID = 'barcode_custom.action_product_template_custom'
        pdf = self.env.ref(REPORT_ID).render_qweb_pdf(self.ids)
        b64_pdf = base64.b64encode(pdf[0])
        # create PrintJob on printer
        # print(gateway.PrintJob(printer=printer_node_code,options={"copies":1},base64=b64_pdf))
        # get PrintJob ID on this printer
        # printjob_id = gateway.printjobs(printer=printer_node_code)[0].id
        # get state of PrintJob
        # print(gateway.states(printjob_id)[0][0].state)


        
        # save pdf as attachment
        # ATTACHMENT_NAME = "My Attachment Name"
        # attachment = self.env['ir.attachment'].create({
        #     'name': ATTACHMENT_NAME,
        #     'type': 'binary',
        #     'datas': b64_pdf,
        #     'datas_fname': ATTACHMENT_NAME + '.pdf',
        #     'store_fname': ATTACHMENT_NAME,
        #     'res_model': self._name,
        #     'res_id': self.id,
        #     'mimetype': 'application/x-pdf'
        # })