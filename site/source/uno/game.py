import random
from source.uno.card import generate_cards
from source.uno.game_states import StartState


class Game(object):
    CLOCK_WISE = 1
    COUNTER_CLOCK_WISE = -1

    def __init__(self, name):
        self._name = name
        self._current_player = None
        self._get_deck = []
        self._put_deck = []
        self._players = []
        self._state = None
        self._direction = self.CLOCK_WISE
        self._deck_reversed_times = 0

    @property
    def current_player(self):
        return self._current_player

    def is_current_player(self, player):
        return self.current_player == player

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def put_deck(self):
        return self._put_deck

    @property
    def get_deck(self):
        return self._get_deck

    @property
    def players(self):
        return self._players

    @property
    def get_nth_next_player(self, nth):
        if self._direction == self.CLOCK_WISE:
            return (self.players.index(self._current_player) + nth) % len(self.players)
        else:
            return (self.players.index(self._current_player) + len(self.players) - nth) % len(self.players)

    def get_card_from_deck(self):
        if len(self.get_deck) == 0:
            self.get_deck = random.shuffle(self.put_deck)
            self.put_deck = []
            self._deck_reversed_times += 1
        return self.get_deck.pop()

    def move_to_next_nth_player(self, nth=1):
        self._current_player = self.get_nth_next_player(nth)

    def move_to_player(self, player):
        self._current_player = player

    def reverse(self):
        if self._direction == self.CLOCK_WISE:
            self._direction = self.COUNTER_CLOCK_WISE
        else:
            self._direction = self.CLOCK_WISE

    def add_player(self, player):
        self._players.append(player)

    def start_game(self):
        self._current_player = random.choice(self._players)
        self._put_deck = []
        self._get_deck = random.shuffle(generate_cards(self))
        self._state = StartState(self)
        self._direction = self.CLOCK_WISE
        self._deck_reversed_times = 0

    # delegated
    def perform_turn(self, player, card):
        if self.is_current_player(player) and player.has_card(card):
            return self.state.perform_turn(player, card)

        if not self.is_current_player(player) and player.has_card(card) and (card == self.put_deck[-1]):
            self.move_to_player(player)
            return self.state.perform_turn(player, card)


