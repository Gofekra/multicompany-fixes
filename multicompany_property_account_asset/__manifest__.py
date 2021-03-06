# Copyright 2017 Creu Blanca
# Copyright 2017 Eficent Business and IT Consulting Services, S.L.
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Multi Company Account Asset',
    'version': '11.0.1.0.0',
    'summary': 'Account Asset Company Properties',
    'author': 'Creu Blanca, Eficent, Odoo Community Association (OCA)',
    'license': 'LGPL-3',
    'sequence': 30,
    'website': 'http://www.eficent.com',
    'depends': ['account_asset', 'multicompany_property_account'],
    'data': [
        'views/product.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': True,
}
