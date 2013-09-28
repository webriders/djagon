from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from game.models import GameTable


@namespace('/game')
class GameNamespace(BaseNamespace):

    def on_join_game(self, game_id):
        game = GameTable.get_game(game_id)
        player = game.join_game()
        self.session['game_id'] = game_id
        self.session['player_id'] = player.id

