{
    'name': 'Picking Process',
    'version': '1.0',
    'description': 'Picking Process',
    'summary': 'Picking Process',
    'author': 'Andrii Semko',
    'website': 'http://andriisem.github.io/',
    'license': 'LGPL-3',
    'category': 'Sale',
    'depends': [
        'sale'
    ],
    'data': [
        'security/ir.model.access.csv',
        'wizard/pickind_process_view.xml',
        'views/sale_order_views.xml',
        'views/pick_list_report_template.xml',
        'views/pick_list_report.xml',
        'views/stock_location_views.xml',
        'views/pack_history_view.xml',
    ],
    'auto_install': False,
    'application': True,
}
