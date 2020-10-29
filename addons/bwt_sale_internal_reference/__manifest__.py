# -*- coding: utf-8 -*-
{
    'name': 'Sale Internal Reference',
    'version': '13.0.1',
    'category': 'Sale',
    'description': """
        Add Internal Reference field to sale order and move Client Reference to general information
    """,

    'author': 'Blackware Technologies',
    'website': 'http://www.blackwaretech.com',

    'depends': ['sale_management'],
    'data': [
        'views/sale_order_views.xml',
    ],

    'installable': True,
    'auto_install': False
}
