# -*- coding: utf-8 -*-
{
    'name': "gestiondesreclamation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "OTman",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'test',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'sale'],
    'application': True,


    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'data/sequence.xml',
        'data/creat_quotation_server_action.xml',
        'views/gestiondes_reclamtion_views.xml',
        'views/gestiondes_articles_views.xml',
        'security/gestiondesreservation_groups.xml',
        'views/users_view.xml',
        'views/sale_order_views.xml',
        'views/smart_button.xml',
        'views/menus/reporting_menus.xml',
        'views/menus/users_menu.xml',
        'views/menus/sales_menu.xml',
        'views/menus/reservation_menus.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'data/demo/demo.xml',
    ],
}
