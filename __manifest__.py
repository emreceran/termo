# -*- coding: utf-8 -*-
{
    'name': "termo",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'web', 'website', 'website_sale'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
        # 'views/report.xml',
        'views/report_beraber.xml',
        # 'views/product_template.xml',
        'views/tip_configure.xml',
        'views/urun_detay.xml',
        # 'views/urun_liste.xml',
        'views/urun_liste_2.xml',
        'views/urun_secme_prod.xml',
        'views/custom_filter_page.xml',
        'views/urun_secme_prog.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],

    'images': ['static/description/termologo.png'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
