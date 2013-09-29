from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from source.game.mechanics import GameMechanics
from source.game.models import GameTable


@namespace('/game')
class GameNamespace(BaseNamespace):

    def on_join_game(self, game_id):
        game = GameTable.get_game(game_id)
        if game is None: return # temp

        player = game.join_game()
        self.session['game_id'] = game_id
        self.session['player_id'] = player.id

        game_mechanics = GameMechanics(game, self.socket, self.ns_name)
        game_mechanics._send_initial_game_state()
