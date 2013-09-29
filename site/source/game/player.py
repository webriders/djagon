import uuid


class Player(object):

    def __init__(self, name="", hand=None):
        self.id = str(uuid.uuid4())[:6].upper()
        self.name = name
        self.hand = hand or []
        self.lamp = False

    def draw_cards(self, cards):
        self.hand = self.hand + cards

    @property
    def cards_number(self):
        return len(self.hand)

    def get_data(self):
        return {
            'id': self.id,
            'name': self.name,
            'cards_number': self.cards_number,
            'lamp': self.lamp
        }
