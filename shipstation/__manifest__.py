{
    'name': 'Shipstation',
    'summary': '',
    'description': '',
    'version': '1.0',
    'license': 'OPL-1',
    'auto_install': False,
    'installable': True,
    'application': True,
    'depends': ['sale', 'sale_order_mode'],
    'data': [
        'security/ir.model.access.csv',
        'views/ship_station_config.xml',
        'views/sale_order_views.xml',
    ],
}
