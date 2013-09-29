from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from source.game.mechanics import GameMechanics
from source.game.models import GameTable


@namespace('/game')
class GameNamespace(BaseNamespace):

    def recv_disconnect(self):
        if hasattr(self.session, 'game_id'):
            game = GameTable.get_game(self.session['game_id'])
            if not game is None:
                game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
                game_mechanics.on_leave_game()
        self.disconnect(silent=True)

    def on_join_game(self, game_id):
        game = GameTable.get_game(game_id)
        if game is None: return

        game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
        game_mechanics.on_join_game()

