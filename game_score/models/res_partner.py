# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _

import logging
_logger = logging.getLogger(__name__)
class ResPartnerInherited(models.Model):
    _inherit = 'res.partner'


    game_count = fields.Integer(string='Games',
         compute='_compute_game_count')
    win_count = fields.Integer(string='Wins',
       compute='_compute_wins_count')
    lose_count = fields.Integer(string='Loses',
        compute='_compute_loses_count')
    avg_game_dur = fields.Float(string="Average Game Duration",compute='_compute_avg')

    def _compute_game_count(self):
        for rec in self:
            all_games = self.env['game.score'].search([('partner_id','=',rec.id)])
            if all_games:
                rec.game_count = len(all_games)
            else:
                rec.game_count = 0

    
    def _compute_wins_count(self):
        for rec in self:
            all_games = self.env['game.score'].search([('game_result','=','won'),('partner_id','=',rec.id)])
            if all_games:
                rec.win_count = len(all_games)
            else:
                rec.win_count = 0

    def _compute_loses_count(self):
        for rec in self:
            all_games = self.env['game.score'].search([('game_result','=','lost'),('partner_id','=',rec.id)])
            if all_games:
                rec.lose_count = len(all_games)
            else:
                rec.lose_count = 0

    def _compute_avg(self):
        for rec in self:
            tot_dur = 0
            tot_games = 0
            all_games = self.env['game.score'].search([('state','=','finish'),('partner_id','=',rec.id)])
            if all_games:
                for game in all_games:
                    tot_dur += game.duration
                    tot_games +=1
                rec.avg_game_dur = (tot_dur/tot_games)
    
    def show_games(self):
        action = self.env.ref('game_score.action_game_score_receipt').read()[0]
        action['context'] = {}
        action['domain'] = [('partner_id', 'child_of', self.ids)]
        return action

    def show_wins(self):
        action = self.env.ref('game_score.action_game_score_receipt').read()[0]
        action['context'] = {}
        action['domain'] = [('game_result','=','won'),('partner_id', 'child_of', self.ids)]
        return action
    
    def show_loses(self):
        action = self.env.ref('game_score.action_game_score_receipt').read()[0]
        action['context'] = {}
        action['domain'] = [('game_result','=','lost'),('partner_id', 'child_of', self.ids)]
        return action

