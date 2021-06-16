# -*- coding: utf-8 -*-
##############################################################################
#
#    ODOO Open Source Management Solution
#
#    ODOO Addon module by Sprintit Ltd
#    Copyright (C) 2019 Sprintit Ltd (<http://sprintit.fi>).
#
##############################################################################

{
    'name': 'Finnish Company Information',
    'version': '0.2',
    'category': 'Accounting/Localization',
    'license': 'LGPL-3',
    'description': 'Company information additional fields, standard for Finnish companies',
    'author': 'SprintIT',
    'maintainer': 'SprintIT',
    'website': 'http://www.sprintit.fi',
    'depends': [
      'base',
    ],
    'data': [
      'view/res_partner_view.xml',
    ],
    'images': ['static/description/cover.jpg',],
    'demo': [
    ],
    'test': [
    ],
    'installable': True,
    'auto_install': False,
    'demo': [
        'demo/testing_configuration.xml',
    ],
    'price': 0.0,
    'currency': 'EUR',
 }
