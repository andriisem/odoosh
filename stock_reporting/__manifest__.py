{
    "name": "Stock reporting",
    "version": "1.0",
    "category": "Inventory",
    "author": 'Maksym Yankin | @yankinmax',
    "description": """
    Several custom inventory reports
    """,
    "depends": ['stock', 'product', 'mail', 'base'],
    "data": [
        'wizard/stock_quantity_history.xml',
        'wizard/product_request_mismatch.xml',
        'wizard/product_locations.xml',
        'views/product_views.xml',
    ],
    "installable": True,
}