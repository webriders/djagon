from socketio.mixins import RoomsMixin
from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace
from source.sockets.utils import send_game_state_frontend, send_game_initial_frontend
from source.storage.exceptions import GameDoesNotExist, PlayerDoesNotExist
from source.storage import utils
from source.storage.models import StoredGame
from source.uno.card import get_card_by_id
from source.uno.exceptions import WrongTurnException
from source.uno.game import Game
from source.uno.player import Player


class UnoRoomsMixin(RoomsMixin):
    def emit_to_room(self, room, event, *args):
        """This is sent to all in the room (in this particular Namespace)"""
        pkt = dict(type="event",
                   name=event,
                   args=args,
                   endpoint=self.ns_name)
        room_name = self._get_room_name(room)
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'rooms' not in socket.session:
                continue
            if room_name in socket.session['rooms']:
                socket.send_packet(pkt)


@namespace('/game')
class GameNamespace(BaseNamespace, UnoRoomsMixin):
    def recv_disconnect(self):
        self.disconnect(silent=True)

    def on_join_game(self, game_id, sessid):
        try:
            game, state = utils.fetch_game(game_id)
            self.session["game_id"] = game.game_id

            if not "player_id" in self.session:
                new_player = Player("Player" + str(len(game.players) + 1))
                new_player.session_id = sessid
                self.session["player_id"] = new_player.player_id
                try:
                    game.find_player_by_id(self.session["player_id"])
                except PlayerDoesNotExist:
                    game.players.append(new_player)

            utils.save_game(game, state)
            send_game_initial_frontend(self.socket, game)

        except GameDoesNotExist:
            pass

    def on_start_confirm(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            player.lamp = True

            utils.save_game(game, state)

            are_all_players_confirmed = True
            for player in game.players:
                if not player.lamp:
                    are_all_players_confirmed = False

            if not are_all_players_confirmed:
                send_game_initial_frontend(self.socket, game)
            else:
                game.start_game()
                utils.save_game(game, StoredGame.STATE_ACTIVE)
                send_game_state_frontend(self.socket, game)

        except GameDoesNotExist:
            pass
        except PlayerDoesNotExist:
            pass

    def on_start_unconfirm(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            player.lamp = True

            utils.save_game(game, state)

            send_game_initial_frontend(self.socket, game)
        except GameDoesNotExist:
            pass
        except PlayerDoesNotExist:
            pass

    def on_make_turn(self, game_id, card_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            card = get_card_by_id(player.cards, card_id)

            game.perform_turn(player, card)

            utils.save_game(game, state)

            send_game_state_frontend(self.socket, game)
        except GameDoesNotExist:
            pass
        except WrongTurnException:
            pass

    def on_draw_card(self, game_id):
        try:
            game, state = utils.fetch_game(game_id)

            player = game.find_player_by_id(self.session['player_id'])
            game.draw_card(player)

            utils.save_game(game, state)

            send_game_state_frontend(self.socket, game)
        except GameDoesNotExist:
            pass
        except PlayerDoesNotExist:
            pass
