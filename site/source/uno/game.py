import random
from source.uno.card import generate_cards
from source.uno.game_states import StartState


class Game(object):
    CLOCK_WISE = 1
    COUNTER_CLOCK_WISE = -1

    def __init__(self, game_id):
        self._game_id = game_id
        self._current_player = None
        self._previous_player = None
        self._get_deck = []
        self._put_deck = []
        self._players = []
        self._state = None
        self._direction = self.CLOCK_WISE
        self._deck_reversed_times = 0

    @property
    def current_player(self):
        return self._current_player

    @property
    def previous_player(self):
        return self._previous_player

    @current_player.setter
    def current_player(self, new_current_player):
        self._previous_player = self._current_player
        self._current_player = new_current_player

    def is_current_player(self, player):
        return self.current_player == player

    @property
    def game_id(self):
        return self._game_id

    @property
    def state(self):
        return self._state

    @state.setter
    def state(self, new_state):
        self._state = new_state

    @property
    def put_deck(self):
        return self._put_deck

    @property
    def get_deck(self):
        return self._get_deck

    @property
    def players(self):
        return self._players

    def get_nth_next_player(self, nth):
        if self._direction == self.CLOCK_WISE:
            return self.players[(self.players.index(self.current_player) + nth) % len(self.players)]
        else:
            return self.players[(self.players.index(self.current_player) + len(self.players) - nth) % len(self.players)]

    def get_card_from_deck(self):
        if len(self.get_deck) == 0:
            top_card = self.put_deck.pop()
            self._get_deck = random.shuffle(self.put_deck)
            self._put_deck = [top_card]
            self._deck_reversed_times += 1
        return self.get_deck.pop()

    def move_to_next_nth_player(self, nth=1):
        self.current_player = self.get_nth_next_player(nth)

    def move_to_player(self, player):
        self._current_player = player

    def move_to_next_player(self):
        self.move_to_next_nth_player(1)

    def reverse(self):
        if self._direction == self.CLOCK_WISE:
            self._direction = self.COUNTER_CLOCK_WISE
        else:
            self._direction = self.CLOCK_WISE

    def add_player(self, player):
        self._players.append(player)

    def start_game(self):
        self.current_player = random.choice(self._players)
        self._put_deck = []
        self._get_deck = generate_cards(self)
        random.shuffle(self._get_deck)

        # give players cards
        for player in self.players:
            for x in range(5):
                card = self.get_card_from_deck()
                player.cards.append(card)

        self._state = StartState(self)
        self._direction = self.CLOCK_WISE
        self._deck_reversed_times = 0

        # first card
        card = self.get_card_from_deck()
        card.action.perform()

    # delegated
    def perform_turn(self, player, card):
        if self.is_current_player(player) and player.has_card(card) and card.can_put_on(self.put_deck[-1]):
            return self.state.perform_turn(player, card)

        if not self.is_current_player(player) and player.has_card(card) and (card == self.put_deck[-1]):
            self.move_to_player(player)
            return self.state.perform_turn(player, card)


