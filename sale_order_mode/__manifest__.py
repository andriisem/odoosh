{
    'name': 'Sale Order Mode',
    'summary': '',
    'description': '',
    'version': '1.1',
    'auto_install': False,
    'installable': True,
    'application': True,

    'depends': [
        'sale',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/sale_order_view.xml',
        'views/res_partner_view.xml',
        'views/shipping_rule_views.xml',
    ],
}