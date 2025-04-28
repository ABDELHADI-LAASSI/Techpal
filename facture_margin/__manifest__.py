{
    "name": "FACTURE MARGIN",
    "author": "Abdelhadi Laassi",
    "category": "",
    "version": "1.0",
    "license": "LGPL-3",
    
    "depends": ['account', 'purchase'],

    "data": [
        'views/account_move.xml',
        'views/purchase_order.xml'
    ],
    
    'installable': True,
    'application': True,
    'auto_install': False,
}