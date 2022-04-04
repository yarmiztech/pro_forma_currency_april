# -*- coding: utf-8 -*-
{
    'name': "PRO FORMA CURRENCY",
    'author':
        'ENZAPPS',
    'summary': """
This module is for Making Multi Currency in Pro Forma Invoice.
""",

    'description': """
This module is for Making Multi Currency in Pro Forma Invoice.
    """,
    'website': "",
    'category': 'base',
    'version': '14.0',
    'depends': ['base', 'account', 'stock','mail','pro_forma_invoice','natcom_proforma'],
    "images": ['static/description/icon.png'],
    'data': [
        'views/pro_forma_invoice.xml',
    ],
    'demo': [
    ],
    'installable': True,
    'application': True,
}
