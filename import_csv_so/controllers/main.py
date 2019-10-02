
import json

from odoo import http
from odoo.http import request
from odoo.tools import misc


class ImportController(http.Controller):

    @http.route('/custom_csv_import/set_file', methods=['POST'])
    def set_file(self, file, import_id, customer, jsonp='callback'):
        import_id = int(import_id)

        written = request.env['custom_csv.import'].browse(import_id).write({
            'file': file.read(),
            'file_name': file.filename,
            'file_type': file.content_type,
        })

        return 'window.top.%s(%s)' % (misc.html_escape(jsonp), json.dumps({'result': written}))
