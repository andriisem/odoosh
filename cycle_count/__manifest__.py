{
    "name": "Cycle Count",
    "version": "1.0",
    "category": "Inventory",
    "author": 'Maksym Yankin | @yankinmax',
    "description": """
    Cycle count inventory adjustment
    """,
    "depends": ['stock', 'product',],
    "data": [
        'views/stock_inventory_views.xml',
        'wizard/cycle_count_views.xml',
    ],
    "installable": True,
}