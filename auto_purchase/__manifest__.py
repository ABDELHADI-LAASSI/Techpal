{
    'name': 'Auto Purchase',
    'description': 'Auto Purchase',
    'version': '1.0',
    'author': 'Abdelhadi',
    'category': '',
    'depends': ['web', 'base', 'mail', 'sale', 'purchase', 'sale_management', 'contacts', 'account'],
    'data': [
        'views/sale_report_inherit.xml',
        'views/external_layout_inherit.xml',
        'views/purchaseorder_report_inherit.xml',
        'views/invoice_report_inherit.xml'
    ],
    'assets': {
        'web.assets_backend': [],
        'web.assets_frontend': [],
        'web.report_assets_common': []
    },
    'installable': True,
    'application': False,
}