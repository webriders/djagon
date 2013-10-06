from source.uno.exceptions import GameFinishedException


class GameState(object):
    _game = None

    def __init__(self, game):
        self._game = game

    @property
    def game(self):
        return self._game

    def perform_turn(self, player, card):
        pass


class StartState(GameState):
    def perform_turn(self, player, card):
        self._game.put_deck.append(card)
        card.action.perform()
        self.game.state = NormalState(self.game)


class NormalState(GameState):
    def perform_turn(self, player, card):
        player.remove_card(card)
        self._game.put_deck.append(card)
        card.action.perform()
        if len(player.cards) == 1:
            self.game.state = UnoState(self.game)
        if len(player.cards) == 0:
            self.game.state = EndState(self.game)


class UnoState(NormalState):
    def perform_turn(self, player, card):
        super(UnoState, self).perform_turn(player, card)
        self.game.state = NormalState(self.game)


class EndState(GameState):
    def perform_turn(self, player, card):
        raise GameFinishedException()
