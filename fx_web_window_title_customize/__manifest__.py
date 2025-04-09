{
    "name": "Customize Web Window Title",
    "summary": "The custom web window title",
    "description": """ Customize Title """,
    "version": "17.0.0.1.0",
    "author": "Doan Thanh Sang",
    "category": "Extra Tools",
    "depends": ["web", "base_setup"],
    "data": [
        "views/inherit_res_config_settings_view.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "fx_web_window_title_customize/static/src/js/web_window_title_customize.js",
        ],
    },
    "images": [
        'static/description/icon.png',
    ],
    "license": "LGPL-3",
    "installable": True,
    "auto_install": False,
    "application": True,
}
