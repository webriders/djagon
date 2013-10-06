from source.storage import id_generator


class Card(object):
    SCORE_PICTURES = 10
    SCORE_WILD = 20

    def __init__(self, color=None, value=None, action=None):
        self._id = id_generator.new_id()
        self.color = color
        self.value = value
        self.action = action

    @property
    def id(self):
        return self._id

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
    def card_score(cls, card):
        if card.value in ['reverse', 'skip', 'draw-two']:
            return cls.SCORE_PICTURES
        elif card.value in ['wild', 'draw-four']:
            return cls.SCORE_WILD
        else:
            return int(card.value)

    @classmethod
    def card_action(cls, game, card):
        if not card.color == "black":
            if card.value == 'reverse':
                return ReverseAction(game, card)
            elif card.value == 'skip':
                return TakeAndSkipAction(game, card, [{"skip": True}])
            elif card.value == 'draw-two':
                return TakeAndSkipAction(game, card, [{"cards_to_take": 2, "skip": False}])
            else:
                return DefaultCardAction(game, card)
        else:
            if card.value == 'draw-four':
                return TakeAndSkipAction(game, card, [{"cards_to_take": 4, "skip": False}])
            else:
                return DefaultCardAction(game, card)

    @classmethod
    def factory(cls, game, col, val, needed_col=None):
        if not col == "black":
            new_card = Card(col, val)
        else:
            new_card = BlackCard(value=val, needed_color=needed_col)

        new_card.action = cls.card_action(game, new_card)
        new_card.score = cls.card_score(new_card)
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
        cards.append(Card.factory(game, x["color"], x["value"]))

    for x in draw_four_cards:
        cards.append(Card.factory(game, x["color"], x["value"]))

    return cards

