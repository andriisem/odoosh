# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from odoo import api, fields, models, _

class ProductRequestMismatch(models.TransientModel):
    _name = 'product.request.mismatch'

    def _compute_active_ids(self):
        active_product_ids = self._context.get('active_model') == 'product.product' and self._context.get('active_ids') or []
        return [
            (0, 0, {'product_id': product.id, 
                    'name': product.name,
                    'barcode': product.barcode,
                    'sku': product.sku,
                    'locations_before': product.locations_before,
                    'locations_after': product.locations_after,
                    'count_before': product.count_before,
                    'count_after': product.count_after,
                    'difference': product.difference,
                    })
            for product in self.env['product.product'].browse(active_product_ids)
        ]

    user_id = fields.Many2one('res.users', string='Salesperson', track_visibility='onchange', default=lambda self: self.env.user)
    user_email = fields.Char('User Email', related='user_id.email', readonly=False)
    partner_id = fields.Many2one('res.partner', string='Partner', track_visibility='onchange', default=lambda self: self.env.user.partner_id)
    partner_email = fields.Char('Partner Email', related='partner_id.email', readonly=False)
    product_ids = fields.One2many('product.request.mismatch.product', 'wizard_id', string='Products', default=_compute_active_ids)
    partner_emails = fields.Char('Partner Emails', help="Comma-separated email addresses", readonly=False)   

    @api.multi
    def send_email(self):
        self.ensure_one()
        template_obj = self.env['mail.mail']
        subject = 'Mismatch Investigation Request-' + datetime.now().strftime("%Y-%m-%d-%H:%M:%S")
        
        for record in self:
            email_from = record.user_email
            products = record.product_ids
            if record.partner_emails:
                email_to = record.partner_emails
            else:
                email_to = record.partner_email

        message_body = '''
            <style type="text/css">
                .tg  {border-collapse:collapse;border-spacing:0;border-color:#aabcfe;}
                .tg td{font-family:Arial, sans-serif;font-size:14px;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#aabcfe;color:#669;background-color:#e8edff;}
                .tg th{font-family:Arial, sans-serif;font-size:14px;font-weight:normal;padding:10px 5px;border-style:solid;border-width:1px;overflow:hidden;word-break:normal;border-color:#aabcfe;color:#039;background-color:#b9c9fe;}
                .tg .tg-hmp3{background-color:#D2E4FC;text-align:left;vertical-align:top}
                .tg .tg-baqh{text-align:center;vertical-align:top}
                .tg .tg-mb3i{background-color:#D2E4FC;text-align:right;vertical-align:top}
                .tg .tg-lqy6{text-align:right;vertical-align:top}
                .tg .tg-0lax{text-align:left;vertical-align:top}
                </style>
                <table class="tg">
                  <tr>
                    <th class="tg-baqh" colspan="9">Products</th>
                  </tr>
                  <tr>
                    <td class="tg-hmp3">No</td>
                    <td class="tg-hmp3">Barcode</td>
                    <td class="tg-hmp3">SKU</td>
                    <td class="tg-hmp3">Name</td>
                    <td class="tg-hmp3">Locations Before</td>
                    <td class="tg-hmp3">Locations After</td>
                    <td class="tg-hmp3">Count Before</td>
                    <td class="tg-hmp3">Count After</td>
                    <td class="tg-hmp3">Difference</td>
                  </tr>
        '''
        number = 0
        text = ''
        for product in products:
            number += 1
            if (number % 2) > 0:
                text_row = f'''
                <tr>
                    <td class="tg-0lax">{number}</td>
                    <td class="tg-0lax">{product.barcode}</td>
                    <td class="tg-lqy6">{product.sku}</td>
                    <td class="tg-lqy6">{product.name}</td>
                    <td class="tg-lqy6">{product.locations_before}</td>
                    <td class="tg-lqy6">{product.locations_after}</td>
                    <td class="tg-lqy6">{product.count_before}</td>
                    <td class="tg-lqy6">{product.count_after}</td>
                    <td class="tg-lqy6">{product.difference}</td>
                </tr>
                '''
            else:
                text_row = f'''
                <tr>
                    <td class="tg-hmp3">{number}</td>
                    <td class="tg-hmp3">{product.barcode}</td>
                    <td class="tg-mb3i">{product.sku}</td>
                    <td class="tg-mb3i">{product.name}</td>
                    <td class="tg-mb3i">{product.locations_before}</td>
                    <td class="tg-mb3i">{product.locations_after}</td>
                    <td class="tg-mb3i">{product.count_before}</td>
                    <td class="tg-mb3i">{product.count_after}</td>
                    <td class="tg-mb3i">{product.difference}</td>                    
                </tr>
                '''
            text += text_row
        text += '</table>'
        message_body += text
        template_data = {
                        'subject': subject,
                        'body_html': message_body,
                        'email_from': email_from,
                        'email_to': email_to,
                        }
        template_id = template_obj.create(template_data)        
        template_obj.send(template_id)       

class ProductRequestMismatchProduct(models.TransientModel):
    _name = 'product.request.mismatch.product'

    wizard_id = fields.Many2one('product.request.mismatch', string='Wizard', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Product', required=True,)
    name = fields.Char('Name', index=True, required=True, translate=True)
    barcode = fields.Char(
        'Barcode', copy=False, oldname='ean13',
        help="International Article Number used for product identification.")
    sku = fields.Char('SKU')
    locations_before = fields.Integer('Locations Before')
    locations_after = fields.Integer('Locations After')
    count_before = fields.Integer('Count Before')
    count_after = fields.Integer('Count After')
    difference = fields.Integer('Difference')
        