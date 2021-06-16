# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2020 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

{
    'name': 'Sprintit Module Management',
    'version': '1.0',
    'license': 'Other proprietary',
    'category': 'Hidden/Tools',
    'author': 'SprintIT',
    'maintainer': 'SprintIT',
    'website': 'http://www.sprintit.fi/in-english',
    'depends': [
        'mail',
    ],
    'data': [
        'security/ir.model.access.csv',
        'views/ir_module_views.xml',
        'views/ir_module_package_view.xml',
        'data/packages.xml',
    ],
    'demo': [
    ],
    'test': [
    ],
    "external_dependencies": { # python pip packages
    #     'python': ['suds', 'dateutil'],
    },
    'installable': True,
    'auto_install': True,
}
