from source.game.packets import GameState, InitialGameState
from source.game.player import Player
from source.game.game import Game
from source.game.cards import get_card_by_id


class GameMechanics(object):

    SPECIFIC_CARD_HANDLERS = {
        '7': 'handle_seven',
        'skip': 'handle_skip',
        'reverse': 'handle_reverse',
        'draw-two': 'handle_draw_two',
        'draw-four': 'handle_draw_four',
        'wild': 'handle_wild',

        'claim_unfair': 'handle_claim_unfair',
        'throw_in': 'handle_throw_in',
        'uno': 'handle_uno',
    }

    EVENT_UPDATE_STATE = 'update_state'
    EVENT_INITIAL_STATE = 'initial_state'
    EVENT_GAME_START = 'game_running'

    def __init__(self, game, socket, session, ns_name):
        assert isinstance(game, Game)
        self.game = game
        self.socket = socket
        self.session = session
        self.ns_name = ns_name
        self.player_id = self.session.get('player_id')

    def on_join_game(self, sessid):
        if not hasattr(self.session, 'game_id') or self.game.game_id != self.session['game_id']:
            player = self.game.join_game(sessid)
            self.session['game_id'] = self.game.game_id
            self.session['player_id'] = player.id
        if self.game.is_active():
            self._send_game_running()
        else:
            self._send_initial_game_state()

    def on_leave_game(self):
        player = self.game.leave_game(self.player_id)
        if player:
            self._send_game_running()
            self._send_game_state()

    def on_throw_in(self, card_id):
        player_id = self.session['player_id']
        player = self.game.players[player_id]
        card = get_card_by_id(self.player.hand, card_id)
        top_card = self.game.deck.get_top_card()

        if not (card['color'] == top_card['color'] and card['value'] == top_card['value']):
            return

        self.game.deck.put_card(card)
        self.game.current_lead = player_id
        self.game.lead_to_next_player()
        self._send_game_state()


    def _send_initial_game_state(self):
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'game_id' not in socket.session:
                continue
            if self.game.game_id == socket.session['game_id']:
                player_id = socket.session['player_id']
                data = InitialGameState(player_id, self.game)
                pkt = dict(type="event", name=self.EVENT_INITIAL_STATE,
                           endpoint=self.ns_name)
                pkt["args"] = data
                socket.send_packet(pkt)

    def _send_game_start(self):
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'game_id' not in socket.session:
                continue
            if self.game.game_id == socket.session['game_id']:
                player_id = socket.session['player_id']
                data = GameState(player_id, self.game)

                pkt = {
                    "type": "event",
                    "name": self.EVENT_GAME_START,
                    "args": data,
                    "endpoint": self.ns_name
                }
                socket.send_packet(pkt)

    def make_turn(self, player, card):
        assert isinstance(player, Player)
        self.handle_turn(player, card)

    def handle_turn(self, player, card):
        if not self.turn_is_fair(card):
            self.game.last_turn_cheated = True
        else:
            self.game.last_turn_cheated = False

        if card['value'] in self.SPECIFIC_CARD_HANDLERS.keys():
            spec_handler = getattr(self, self.SPECIFIC_CARD_HANDLERS[card['value']])
            spec_handler(self)
        else:
            self.game.lead_to_next_player()
        self._send_game_running()

    def turn_is_fair(self, card):
        top_card = self.game.deck.get_top_card()
        if top_card and top_card['color'] == card['color']:
            return True
        if top_card and top_card['value'] == card['value']:
            return True
        if card['color'] == 'black':
            return True
        return False

    def handle_skip(self):
        self.game._lead_to_next_player()
        self.game.lead_to_next_player()

    def handle_reverse(self):
        self.game.change_direction()
        self.game.lead_to_next_player()

    def handle_draw_two(self):
        next_player = self.game.lead_to_next_player()
        cards = self.game.deck.draw_cards(2)
        next_player.draw_cards(cards)

    def handle_draw_four(self):
        next_player = self.game.lead_to_next_player()
        cards = self.game.deck.draw_cards(4)
        next_player.draw_cards(cards)
