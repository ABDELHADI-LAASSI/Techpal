{
    'name': 'Techpal Assistance Module',
    'description': 'Techpal Asistance Module',
    'version': '1.0',
    'author': 'Abdelhadi',
    'category': '',
    'depends': ['web', 'base', 'portal', 'mail', 'contacts'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/assistance_sequence.xml',
        'data/assistance_ntification.xml',  
        'views/base_view.xml',
        'views/assistance_view.xml',
        'views/assistance_tags_view.xml',
        'views/portal_view.xml',
        'report/assistance_report_template.xml',
    ],
    'assets': {
        'web.assets_backend': ['assistance_module/static/src/css/style.css'],
        'web.assets_frontend': ['assistance_module/static/src/css/portal.css'],
        'web.report_assets_common': ['assistance_module/static/src/css/fonts.css']
    },
    'installable': True,
    'application': False,
}