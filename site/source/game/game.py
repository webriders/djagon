from source.game.deck import UnoDeck
from source.game.player import Player
from source.game.models import GameTable

import jsonpickle
import random
import uuid

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


class Game(object):
    INIT_CARDS_NUMBER = 5
    DIRECTION_DIRECT = 1
    PLAYERS_LIMIT = 7

    current_lead = 0  # index of current player

    last_turn_cheated = False

    def __init__(self):
        self.game_id = str(uuid.uuid4())[:6].upper()
        self.status = GameTable.STATUS_IDLE
        self.direction = self.DIRECTION_DIRECT
        self.deck = UnoDeck()
        self.players = OrderedDict()
        self.user_sessions = {}
        self._current_lead = None
        self._previous_lead = None

    @property
    def current_lead(self):
        return self._current_lead

    @property
    def previous_lead(self):
        return self._previous_lead

    @current_lead.setter
    def current_lead(self, x):
        self._previous_lead = self._current_lead
        self._current_lead = x

    def save(self):
        game, created = GameTable.objects.get_or_create(game_id=self.game_id)
        game.prev_state = game.state if self.last_turn_cheated else ""
        game.state = jsonpickle.encode(self)
        game.status = self.status
        game.players_number = self.players_number
        game.save()

    def over_players_limit(self):
        return self.players_number >= self.PLAYERS_LIMIT

    def join_game(self, sessid):
        if sessid in self.user_sessions:
            player_id = self.user_sessions[sessid]
            return self.players[player_id]
        self.status = GameTable.STATUS_OPEN
        default_name = "Player %s" % (self.players_number+1)
        player = Player(name=default_name)
        self.players[player.id] = player
        self.user_sessions[sessid] = player.id
        self.save()
        return player

    def user_is_member(self, sessid):
        return sessid in self.user_sessions

    def leave_game(self, player_id):
        try:
            player = self.players.pop(player_id)
            self.user_sessions.pop(player_id)
        except KeyError:
            return None
        if self.players_number == 0:
            self.status = GameTable.STATUS_CLOSED
        self.save()
        return player

    def start(self):
        self.status = GameTable.STATUS_ACTIVE
        self.current_lead = random.choice(self.players.keys())
        for player in list(self.players.values()):
            player.hand = self.deck.draw_cards(self.INIT_CARDS_NUMBER)
        self.save()

    def get_lead_player(self):
        return self.players[self.current_lead]

    def get_next_player(self):
        current_lead_index = self.players.keys().index(self.current_lead)
        player_index = (current_lead_index+self.direction) % self.players_number
        return self.players[self.players.keys()[player_index]]

    def _lead_to_next_player(self):
        self.current_lead = self.get_next_player().id
        return self.players[self.current_lead]

    def lead_to_next_player(self):
        next_player = self._lead_to_next_player()
        self.save()
        return next_player

    def change_direction(self):
        self.direction = -self.direction
        self.save()

    @property
    def players_number(self):
        return len(self.players)

    def is_active(self):
        return self.status == GameTable.STATUS_ACTIVE
