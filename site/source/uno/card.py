class Card(object):
    color = ""
    value = ""
    action = None

    def __init__(self, color, value, action):
        self.color = color
        self.value = value
        self.action = action


class DefaultCardAction(object):
    _game = None
    _card = None

    def __init__(self, game, card):
        self._game = game
        self._card = card

    def perform(self):
        self._game.put_deck.push(self._card)
        self._game.move_to_next_player()


class TakeAndSkipAction(DefaultCardAction):
    _punishment = []

    def __init__(self, game, card, punishment):
        super(TakeAndSkipAction, self).__init__(game, card)
        self._punishment = punishment

    def perform(self):
        self._game.put_deck.push(self._card)

        nth = 0
        for x in range(len(self._punishment)):
            player = self._game.get_nth_next_player(x + 1)
            for y in self._punishment[x]["cards_to_take"]:
                player.cards.append(self._game.get_card_from_deck())
            if self._punishment[x]["skip"]:
                nth += 1

        self._game.move_to_next_nth_player(nth)


class ReverseAction(DefaultCardAction):
    def perform(self):
        self._game.reverse()
        super(ReverseAction).perform()


def generate_cards(game):
    colors = ['red', 'green', 'blue', 'yellow']
    values = [str(x) for x in range(1, 10)] * 2 + ['0']
    special_values = ['reverse', 'skip', 'draw-two'] * 2

    wild_cards = [{
                      'color': 'black',
                      'value': 'wild',
                  }] * 4

    draw_four_cards = [{
                           'color': 'black',
                           'value': 'draw-four'
                       }] * 4

    cards = []
    for col in colors:
        for val in values:
            new_card = Card()
            new_card.color = col
            new_card.value = val
            new_card.action = DefaultCardAction(game, new_card)
            cards.append(new_card)

    for col in colors:
        for val in special_values:
            new_card = Card()
            new_card.color = col
            new_card.value = val
            if val == 'reverse':
                new_card.action = ReverseAction(game, new_card)
            elif val == 'skip':
                new_card.action = TakeAndSkipAction(game, new_card, [{"skip": True}])
            elif val == 'draw-two':
                new_card.action = TakeAndSkipAction(game, new_card, [{"cards_to_take": 2, "skip": False}])
            cards.append(new_card)

    for x in wild_cards:
        new_card = Card()
        new_card.color = wild_cards[x]["color"]
        new_card.value = wild_cards[x]["value"]
        cards.append(new_card)

    for x in draw_four_cards:
        new_card = Card()
        new_card.color = draw_four_cards[x]["color"]
        new_card.value = draw_four_cards[x]["value"]
        cards.append(new_card)

    return cards

