from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace


@namespace('/game')
class GameNamespace(BaseNamespace):

    def on_join_game(self, game_id):
        self.session['game_id'] = game_id

