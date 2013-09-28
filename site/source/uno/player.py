class Player(object):
    _name = ""
    _cards = []

    def __init__(self, name, cards):
        self._name = name
        self._cards = cards

    @property
    def name(self):
        return self._name

    @property
    def cards(self):
        return self._cards

    def has_card(self, card):
        return card in self.cards
