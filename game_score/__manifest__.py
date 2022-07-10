# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'Minesweeper Game Score Management System',
    'version' : '12.0',
    'summary': 'Manage Score and Game data.',
    'description': """
        Manage Score and Game data with 1.
    """,
    'category': 'Other',
    'sequence': 20,
    'depends' : ['base','mail'],
    'demo' : [],
    'data' : [
        'security/game_score.xml',
        'views/game_score_views.xml',
        'views/game_score_reg.xml',
        'security/ir.model.access.csv',
        'data/game_score_data.xml',
        'views/res_partner.xml',
        'report/report_game_score.xml',
        'report/report_template.xml',
        
    ],
    'auto_install': False,
    'installable': True,
}
