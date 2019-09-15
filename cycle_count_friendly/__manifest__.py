{
    'name': 'Cycle Count Friendly Responsive Interface',
    'summary': '',
    'description': '',
    'version': '1.0',
    'author': '',
    'license': 'OPL-1',
    'auto_install': False,
    'installable': True,
    'application': True,
    "depends": [
        'stock',
        'product',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/assets.xml',
        'wizard/cycle_count_views.xml',
    ],
}