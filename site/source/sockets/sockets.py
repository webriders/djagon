from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from source.sockets.utils import send_game_state_frontend, send_user_message, send_broadcast_user_message, send_game_score
from source.storage.exceptions import GameDoesNotExist, PlayerDoesNotExist
from source.storage import utils
from source.storage.models import StoredGame
from source.uno.card import get_card_by_id
from source.uno.exceptions import WrongTurnException, GameFinishedException
from source.uno.game_states import EndState
from source.uno.player import Player


@namespace('/game')
class GameNamespace(BaseNamespace):
    def recv_disconnect(self):
        self.disconnect(silent=True)

    def on_join_game(self, game_id, sessid):
        try:
            game, state = utils.fetch_game(game_id)
            self.session["game_id"] = game.game_id

            try:
                player = game.find_player_by_session_id(sessid)
                self.session["player_id"] = player.player_id
            except PlayerDoesNotExist:
                new_player = Player("Player" + str(len(game.players) + 1))
                new_player.session_id = sessid
                self.session["player_id"] = new_player.player_id
                game.players.append(new_player)
                utils.save_game(game, state)

            send_game_state_frontend(self.socket, game, state)

        except GameDoesNotExist:
            pass

    def on_start_confirm(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            player.lamp = True

            utils.save_game(game, state)

            are_all_players_confirmed = all([player.lamp for player in game.players])

            if not are_all_players_confirmed:
                send_game_state_frontend(self.socket, game, state)
            else:
                game.start_game()
                utils.save_game(game, StoredGame.STATE_ACTIVE)
                send_game_state_frontend(self.socket, game, StoredGame.STATE_ACTIVE)

        except (GameDoesNotExist, PlayerDoesNotExist):
            pass

    def on_start_unconfirm(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            player.lamp = True

            utils.save_game(game, state)

            send_game_state_frontend(self.socket, game, state)
        except (GameDoesNotExist, PlayerDoesNotExist):
            pass

    def on_make_turn(self, game_id, card_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            card = get_card_by_id(player.cards, card_id)

            game.perform_turn(player, card)

            if isinstance(game.state, EndState):
                send_game_score(self.socket, game)
                game.start_game()

            utils.save_game(game, state)

            send_game_state_frontend(self.socket, game, state)
        except WrongTurnException:
            send_user_message(self.socket, "error", "Move is not correct!")
        except (GameDoesNotExist, GameFinishedException):
            pass

    def on_draw_card(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            game.draw_card(player)

            utils.save_game(game, state)

            send_game_state_frontend(self.socket, game, state)
        except WrongTurnException:
            send_user_message(self.socket, "error", "It's not your turn")
        except (GameDoesNotExist, PlayerDoesNotExist):
            pass

