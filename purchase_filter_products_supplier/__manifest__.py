{
    "name": "Purchase filter products by supplier",
    "version": "1.0",
    "category": "Purchase",
    "author": 'Maksym Yankin | @yankinmax',
    "description": """
    	There two use cases for this module. In both products are sorted by vendor and all can be purchased.
    	1. If you have not a big amount of vendors and products. You can choose vendor and product directly from dropdown. "Show more" button is invisible in Odoo by default. 
    	2. If you have big amount of vendors and products. When you try to choose vendor and product, they are not shown in dropdown, but "Show more" button is visible in Odoo by default and you press it to choose preferable option. 
    	To add these parameter go to Configuration -> Technical -> Parameters -> System Parameters and add new parameter like:	
    	key -> web_m2x_options.limit
    	value -> 0
    """,
    "depends": ['purchase', 'web_m2x_options'],
    "installable": True,
}