from source.game.packets import GameState, InitialGameState
from source.game.player import Player
from source.game.game import Game


class GameMechanics(object):

    SPECIFIC_CARD_HANDLERS = {
        #'7': 'handle_seven',
        'skip': 'handle_skip',
        'reverse': 'handle_reverse',
        'draw-two': 'handle_draw_two',
        'draw-four': 'handle_draw_four',
        'wild': 'handle_wild',

        'claim_unfair': 'handle_claim_unfair',
        'throw_in': 'handle_throw_in',
        'uno': 'handle_uno',
    }

    EVENT_INITIAL_STATE = 'initial_state'
    EVENT_GAME_RUNNING = 'game_running'
    EVENT_USER_MESSAGE = 'user_message'

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

    def _send_game_running(self):
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'game_id' not in socket.session:
                continue
            if self.game.game_id == socket.session['game_id']:
                player_id = socket.session['player_id']
                data = GameState(player_id, self.game)

                pkt = {
                    "type": "event",
                    "name": self.EVENT_GAME_RUNNING,
                    "args": data,
                    "endpoint": self.ns_name
                }
                socket.send_packet(pkt)

    def make_turn(self, player, card):
        assert isinstance(player, Player)
        if self.game.current_lead != player.id:
            self.handle_throw_in(player, card)
        else:
            self.handle_turn(player, card)

        self.handle_if_end_of_round()

    def handle_if_end_of_round(self):
        for x in self.game.players:
            if self.game.players[x].cards_number == 0:
                self.announce_score()
                self.game.start()
                self._send_game_running()

    def handle_throw_in(self, player, card):
        top_card = self.game.deck.get_top_card()
        if not (card['color'] == top_card['color'] and card['value'] == top_card['value']):
            self.send_user_message("error", "You cheat!")
            return # you cheat, guy

        player.hand.pop(card)
        self.game.deck.put_card(card)
        self.game.current_lead = player.id
        self.game.lead_to_next_player()
        self._send_game_running()

    def broadcast_user_message(self, message_type, message_content):
        for sessid, socket in self.socket.server.sockets.iteritems():
            self.send_user_message(message_type, message_content, socket)

    def send_user_message(self, message_type, message_content, socket=None):
        socket = socket or self.socket
        pkt = {
            "type": "event",
            "name": self.EVENT_USER_MESSAGE,
            "args": {
                "type": message_type,
                "msg": message_content
            },
            "endpoint": self.ns_name
        }
        socket.send_packet(pkt)

    def handle_turn(self, player, card):
        if not self.turn_is_fair(card):
            self.send_user_message("error", "Move is not correct!")
            return

        # anyway
        self.game.deck.put_card(card)
        player.remove_card_from_hand(card)
        #

        if card['value'] in self.SPECIFIC_CARD_HANDLERS.keys():
            spec_handler = getattr(self, self.SPECIFIC_CARD_HANDLERS[card['value']])
            spec_handler()
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
        return False if top_card else True

    def handle_skip(self):
        self.game._lead_to_next_player()

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

    def announce_score(self):
        self.game.summarize_score()
        for player in self.game.players.values():
            self.broadcast_user_message('info', 'Player %s scored %s points' % player.score)
