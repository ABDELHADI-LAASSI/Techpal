{
    'name': 'Social Marketing Techpal',
    'description': 'Social Marketing Techpal',
    'version': '1.0',
    'author': 'Abdelhadi',
    'category': 'Social Marketing',
    'depends': ['web', 'base'],
    'data': [
        'security/ir.model.access.csv',
        'views/base_menu.xml',
        'views/social_view.xml',
        'views/Tags_view.xml'
    ],
    'assets': {
        'web.assets_backend': ['Techpal/static/src/css/style.css'],
    },
    'installable': True,
    'application': False,
}