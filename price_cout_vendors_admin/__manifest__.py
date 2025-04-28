{
    'name': 'Price Cout Admin',
    'description': 'Price Cout Admin',
    'version': '1.0',
    'author': 'Abdelhadi',
    'category': '',
    'depends': ['base','purchase', 'sale_management', 'account'],
    'data': [
        'security/security.xml',
        'views/Sale_Order_Invoice.xml',
        'views/Product_Template.xml'
    ],
    'assets': {
        'web.assets_backend': [],
        'web.assets_frontend': [],
        'web.report_assets_common': []
    },
    'installable': True,
    'application': False,
}