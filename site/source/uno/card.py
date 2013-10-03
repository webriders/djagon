import uuid


class Card(object):
    id = 0
    color = ""
    value = ""
    action = None

    def __init__(self, color=None, value=None, action=None):
        self.id = str(uuid.uuid4())[-5:]
        self.color = color
        self.value = value
        self.action = action

    def is_identical(self, card):
        return self.id == card.id

    __eq__ = is_identical

    def is_equal(self, card):
        return (self.color == card.color) and (self.value == card.value)

    def can_put_on(self, card):
        return \
            (self.color == card.color) or (self.value == card.value) or \
            (self.color == 'black') or (hasattr(card, "needed_color") and self.color == card.needed_color)

    @classmethod
    def factory(cls, game, col, val, needed_col=None):
        if not col == "black":
            new_card = Card(col, val)

            if val == 'reverse':
                new_card.action = ReverseAction(game, new_card)
            elif val == 'skip':
                new_card.action = TakeAndSkipAction(game, new_card, [{"skip": True}])
            elif val == 'draw-two':
                new_card.action = TakeAndSkipAction(game, new_card, [{"cards_to_take": 2, "skip": False}])
            else:
                new_card.action = DefaultCardAction(game, new_card)
        else:
            new_card = BlackCard(col, val, needed_col)
            if val == 'draw-four':
                new_card.action = TakeAndSkipAction(game, new_card, [{"cards_to_take": 4, "skip": False}])
            else:
                new_card.action = DefaultCardAction(game, new_card)

        return new_card


class BlackCard(Card):
    def __init__(self, value=None, action=None, needed_color=None):
        super(BlackCard, self).__init__('black', value, action)
        self._needed_color = needed_color

    @property
    def needed_color(self):
        return self._needed_color

    @needed_color.setter
    def needed_color(self, color):
        self._needed_color = color


class DefaultCardAction(object):
    _game = None
    _card = None

    def __init__(self, game, card):
        self._game = game
        self._card = card

    def perform(self):
        self._game.move_to_next_player()


class TakeAndSkipAction(DefaultCardAction):
    _punishment = []

    def __init__(self, game, card, punishment):
        super(TakeAndSkipAction, self).__init__(game, card)
        self._punishment = punishment

    def perform(self):
        self._game.put_deck.append(self._card)

        nth = 0
        for x in range(len(self._punishment)):
            player = self._game.get_nth_next_player(x + 1)
            if "cards_to_take" in self._punishment[x]:
                for y in range(self._punishment[x]["cards_to_take"]):
                    player.cards.append(self._game.get_card_from_deck())
            if "skip" in self._punishment[x]:
                nth += 1

        self._game.move_to_next_nth_player(nth)


class ReverseAction(DefaultCardAction):
    def perform(self):
        self._game.reverse()
        super(ReverseAction, self).perform()


def generate_cards(game):
    colors = ['red', 'green', 'blue', 'yellow']
    values = [str(x) for x in range(1, 10)] * 2 + ['0']
    special_values = ['reverse', 'skip', 'draw-two'] * 2
    wild_cards = [{'color': 'black', 'value': 'wild'}] * 4
    draw_four_cards = [{'color': 'black', 'value': 'draw-four'}] * 4

    cards = []
    for col in colors:
        for val in values:
            cards.append(Card.factory(game, col, val))

    for col in colors:
        for val in special_values:
            cards.append(Card.factory(game, col, val))

    for x in wild_cards:
        new_card = Card(x["color"], x["value"])
        new_card.action = None
        cards.append(new_card)

    for x in draw_four_cards:
        new_card = Card(x["color"], x["value"])
        new_card.action = None
        cards.append(new_card)

    return cards

