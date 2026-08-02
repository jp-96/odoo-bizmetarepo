{
    'name': "ems_ldm_odoo",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base', 'ems', 'ems_ldm'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/object_class_views.xml',
        'views/data_element_views.xml',
        'views/value_domain_views.xml',
        'views/constraint_views.xml',
        'views/od_namespace_views.xml',
        'views/od_field_domain_views.xml',
        'views/od_field_views.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

