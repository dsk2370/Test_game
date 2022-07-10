# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError
from datetime import datetime, timedelta
class GameSizeModel(models.Model):
    _name = 'game.size'
    _description = 'Game size'

    x_size = fields.Integer("X-size",required=True)
    y_size = fields.Integer("Y-size",required=True)
    name = fields.Char(string='Game Reference',store=True, readonly=True,compute='_compute_name')

    @api.one
    @api.depends('x_size','y_size')
    def _compute_name(self):
        if self.x_size and self.y_size:
            self.name = str(self.x_size) + "x" + str(self.y_size)

    

class GameScore(models.Model):
    _name = 'game.score'
    _description = 'Game Sessions'
    _inherit = ['mail.thread']
    # _order = "date desc, id desc"

    
    name = fields.Char(string='Game Reference', required=True, copy=False, readonly=True, states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'))
    date = fields.Date("Date", readonly=True,required=True,
        index=True, states={'draft': [('readonly', False)]},
        copy=False, default=fields.Date.context_today)
    start = fields.Datetime("Start time", readonly=True,
        index=True, 
        copy=False)
    end = fields.Datetime("End time", readonly=True,
        index=True, 
        copy=False)
    game_size_id = fields.Many2one('game.size',string="Game Size",required=True,readonly=True,states={'draft': [('readonly', False)]})
    game_result = fields.Selection([
        ('won', 'Won'),
        ('lost', 'Lost'),
        ('cancel', 'Canceled'),
        ], 'Game Result', readonly=True, track_visibility='onchange', copy=False)
    narration = fields.Text('Notes', readonly=True, states={'draft': [('readonly', False)]}) 
    state = fields.Selection([
        ('draft', 'Draft'),
        ('inprogress', 'In Progress'),
        ('finish', 'Finished'),
        ('cancel', 'Canceled'),
        ], 'Status', readonly=True, track_visibility='onchange', copy=False, default='draft')
    duration = fields.Float(string="Game Duration",compute='_compute_duration',store=True)
    partner_id = fields.Many2one('res.partner', 'Player',required=1, change_default=1, readonly=True, states={'draft': [('readonly', False)]})
    
    @api.model
    def create(self, vals):
        if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('game.score') or _('New')
        result = super(GameScore, self).create(vals)
        return result
    
    @api.one
    @api.depends('start','end')
    def _compute_duration(self):
        if self.start and self.end:
            duration = self.end - self.start
            duration_in_s = duration.total_seconds() 
            self.duration = duration_in_s/3600
        else:
            self.duration = False


    @api.multi
    def start_game(self):
        for rec in self:
            rec.start = fields.datetime.now()
            rec.write({'state': 'inprogress'})

    @api.multi
    def cancel_game(self):
        for rec in self:
            rec.write({'state': 'cancel', 'game_result': 'cancel'})

    @api.multi
    def unlink(self):
        for rec in self:
            if rec.state not in ('draft'):
                raise UserError(_('Cannot delete game(s) which is not in draft.'))
        return super(GameScore, self).unlink()


    @api.multi
    def action_game_score(self):
        return {    
            'name': _("Finish Game"),
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'game.score.reg',
            'target': 'new',
            'context': {}
        }







