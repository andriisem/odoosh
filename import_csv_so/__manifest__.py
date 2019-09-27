{
    'name': 'Import SO from CSV',
    'summary': '',
    'description': '',
    'version': '1.0',
    'category': 'Print Category here',
    'license': 'OPL-1',
    'auto_install': False,
    'installable': True,
    'application': True,
    'depends': [
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'views/res_partner_view.xml',
        'views/sale_order_view.xml',
        'views/import_view.xml',
    ],
    'qweb': ['static/src/xml/custom_import.xml'],
}