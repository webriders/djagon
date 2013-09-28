from source.game.player import Player
from source.game.uno_game import UnoGame


class UnoMechanics(object):

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

    EVENT_UPDATE_GAME_STATE = 'update_game_state'

    def __init__(self, game, socket, ns_name):
        assert isinstance(game, UnoGame)
        self.game = game
        self.socket = socket
        self.ns_name = ns_name

    def _send_game_state(self):
        for sessid, socket in self.socket.server.sockets.iteritems():
            if 'game_id' not in socket.session:
                continue
            if self.game.game_id == socket.session['game_id']:
                player_id = socket['player_id']
                pkt = self._form_user_packet(player_id, self.EVENT_UPDATE_GAME_STATE)
                socket.send_packet(pkt)

    def _form_user_packet(self, player_id, event):
        args = { p.id: p.cards_number for p in self.game.players }
        args['my_hand'] = self.game.players[player_id].hand
        pkt = dict(type="event", name=event, args=args, endpoint=self.ns_name)
        return pkt

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
        self._send_game_state()

    def turn_is_fair(self, card):
        top_card = self.game.deck.get_top_card()
        if top_card['color'] == card['color']:
            return True
        if top_card['value'] == card['value']:
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
