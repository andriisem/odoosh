{
    'name': 'Sale Order Mode',
    'summary': '',
    'description': '',
    'version': '1.0',
    'auto_install': False,
    'installable': True,
    'application': True,

    'depends': [
        'sale',
        'preferences',
    ],

    'data': [
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
    ],
}