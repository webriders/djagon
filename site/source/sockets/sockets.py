from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from source.sockets.utils import send_game_state_frontend, send_user_message, send_game_score, remove_players_who_leave
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
        game = None
        try:
            if ("game_id" in self.session) and ("player_id" in self.session):
                game, state = utils.fetch_game(self.session["game_id"])
                player_to_remove = game.find_player_by_id(self.session["player_id"])
                game.remove_player(player_to_remove)
                game, state = remove_players_who_leave(self.socket, game, state)
                send_game_state_frontend(self.socket, game, state)
        except GameDoesNotExist:
            pass
        finally:
            if not game is None:
                utils.save_game(game, state)
            self.disconnect(silent=True)

    def on_join_game(self, game_id, sessid):
        game = None
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
                game.add_player(new_player)

            game, state = remove_players_who_leave(self.socket, game, state)
            send_game_state_frontend(self.socket, game, state)

        except GameDoesNotExist:
            pass
        finally:
            if not game is None:
                utils.save_game(game, state)

    def on_start_confirm(self, game_id):
        game = None
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            player.lamp = True

            are_all_players_confirmed = all([player.lamp for player in game.players])

            if are_all_players_confirmed:
                game.start_game()
                state = StoredGame.STATE_ACTIVE

            game, state = remove_players_who_leave(self.socket, game, state)
            send_game_state_frontend(self.socket, game, state)

        except (GameDoesNotExist, PlayerDoesNotExist):
            pass
        finally:
            if not game is None:
                utils.save_game(game, state)

    def on_start_unconfirm(self, game_id):
        game = None
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            player.lamp = True

            game, state = remove_players_who_leave(self.socket, game, state)
            send_game_state_frontend(self.socket, game, state)
        except (GameDoesNotExist, PlayerDoesNotExist):
            pass
        finally:
            if not game is None:
                utils.save_game(game, state)

    def on_make_turn(self, game_id, card_id):
        game = None
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            card = get_card_by_id(player.cards, card_id)

            game.perform_turn(player, card)

            if isinstance(game.state, EndState):
                send_game_score(self.socket, game)
                game.start_game()

            game, state = remove_players_who_leave(self.socket, game, state)
            send_game_state_frontend(self.socket, game, state)
        except WrongTurnException:
            send_user_message(self.socket, "error", "Move is not correct!")
        except (GameDoesNotExist, GameFinishedException):
            pass
        finally:
            if not game is None:
                utils.save_game(game, state)

    def on_draw_card(self, game_id):
        game = None
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            game.draw_card(player)

            game, state = remove_players_who_leave(self.socket, game, state)
            send_game_state_frontend(self.socket, game, state)
        except WrongTurnException:
            send_user_message(self.socket, "error", "It's not your turn")
        except (GameDoesNotExist, PlayerDoesNotExist):
            pass
        finally:
            if not game is None:
                utils.save_game(game, state)

