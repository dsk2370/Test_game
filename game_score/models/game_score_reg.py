
from odoo import fields, models, api, _
from odoo.addons import decimal_precision as dp
from odoo.exceptions import UserError, ValidationError


class GameScoreReg(models.TransientModel):
    _name = "game.score.reg"
    _description= 'Register Result in game'
    
    game_result = fields.Selection([
    ('won', 'Won'),
    ('lost', 'Lost'),
    ('cancel', 'Canceled'),
    ], 'Game Result', copy=False, default='won')
    
    end = fields.Datetime("Game Endtime",
        copy=False)
    
    @api.multi
    def action_validate_game_score(self):
        context = dict(self._context or {})
        active_id = context.get('active_id', False)
        if active_id:
            game_obj = self.env['game.score'].browse(active_id)
            if game_obj:
                if self.game_result == 'cancel':
                    game_obj.cancel_game()
                else:
                    game_obj.game_result = self.game_result
                    game_obj.end = self.end
                    game_obj.state = 'finish'
                