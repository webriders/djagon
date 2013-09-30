class Player(object):

    def __init__(self, name):
        self._name = name
        self._cards = []

    def eq(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self._name

    @property
    def cards(self):
        return self._cards

    def has_card(self, card):
        return card in self.cards

    def has_card_to_put_on(self, card):
        for x in self.cards:
            if x.can_put_on(card):
                return True
        return False

    def remove_card(self, card):
        self.cards.remove(card)
