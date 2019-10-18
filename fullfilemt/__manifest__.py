{
    "name": "Fullfilemt",
    "version": "1.0",
    "category": "Sales",
    "description": """
    """,
    "depends": ['sale', 'fullfilemt_stage', 'sale_order_mode'],
    "data": [
        'security/ir.model.access.csv',
        'views/fullfilemt_views.xml',
        'views/sale_odrder_views.xml',
    ],
    "installable": True,
    'application': True,
}
