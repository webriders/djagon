from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from source.game.cards import get_card_by_id
from source.game.mechanics import GameMechanics
from source.storage.exceptions import GameDoesNotExist, PlayerDoesNotExist
from source.storage.models import StoredGame
from source.storage import utils
from source.uno.exceptions import WrongTurnException


@namespace('/game')
class GameNamespace(BaseNamespace):
    def recv_disconnect(self):
        if hasattr(self.session, 'game_id'):
            try:
                game, state = utils.fetch_game(self.session['game_id'])
                game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
                game_mechanics.on_leave_game()
            except GameDoesNotExist:
                pass
        self.disconnect(silent=True)

    def on_join_game(self, game_id, sessid):
        try:
            game, state = utils.fetch_game(game_id)

            game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
            game_mechanics.on_join_game(sessid)
        except GameDoesNotExist:
            pass

    def on_start_confirm(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.players[self.session['player_id']]
            player.lamp = True

            utils.save_game(game_id, game)

            game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)

            are_all_players_confirmed = True
            for x in game.players:
                if not game.players[x].lamp:
                    are_all_players_confirmed = False

            if not are_all_players_confirmed:
                game_mechanics._send_initial_game_state()
            else:
                game.start()
                game_mechanics._send_game_running()

        except GameDoesNotExist:
            pass

    def on_start_unconfirm(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.players[self.session['player_id']]
            player.lamp = False
            game.save()

            game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
            game_mechanics._send_initial_game_state()
        except GameDoesNotExist:
            pass

    def on_make_turn(self, game_id, card_id):
        try:
            game = StoredGame.get_game(game_id)
            if game is None:
                return

            player = game.players[self.session['player_id']]
            card = get_card_by_id(player.hand, card_id)
            if not card:
                card = get_card_by_id(game.deck.stack, card_id)

            game_mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
            game_mechanics.make_turn(player, card)

        except GameDoesNotExist:
            pass
        except WrongTurnException:
            pass

    def on_draw_card(self):
        try:
            game = StoredGame.get_game(self.session.get('game_id'))
            player = game.players.get(self.session.get('player_id'))

            if not player or not game:
                return

            mechanics = GameMechanics(game, self.socket, self.session, self.ns_name)
            mechanics.on_draw_card(player)
        except GameDoesNotExist:
            pass
        except PlayerDoesNotExist:
            pass
