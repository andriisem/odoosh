{
    "name": "Stock reporting",
    "version": "1.0",
    "category": "Inventory",
    "author": 'Maksym Yankin | @yankinmax',
    "description": """
    Several custom inventory reports
    """,
    "depends": ['stock', 'product',],
    "data": [
        'wizard/stock_quantity_history.xml',
        'views/product_views.xml',
    ],
    "installable": True,
}