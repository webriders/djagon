from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from source.game.mechanics import GameMechanics
from source.game.models import GameTable


@namespace('/game')
class GameNamespace(BaseNamespace):

    def on_join_game(self, game_id):
        game = GameTable.get_game(game_id)
        if game is None: return # temp

        game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
        game_mechanics.on_join_game()

