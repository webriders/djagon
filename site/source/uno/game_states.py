class GameState(object):
    _game = None

    def __init__(self, game):
        self._game = game

    @property
    def game(self):
        return self._game

    def perform_turn(self, player, card):
        pass

    def get_card_from_deck(self, player, card):
        pass


class StartState(object):
    def perform_turn(self, player, card):
        pass

    def get_card_from_deck(self, player, card):
        pass


class NormalState(object):
    def perform_turn(self, player, card):
        pass

    def get_card_from_deck(self, player, card):
        pass


class UnoState(object):
    def perform_turn(self, player, card):
        pass

    def get_card_from_deck(self, player, card):
        pass


class EndState(object):
    def perform_turn(self, player, card):
        pass

    def get_card_from_deck(self, player, card):
        pass
