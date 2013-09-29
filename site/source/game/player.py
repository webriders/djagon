import uuid
from django.utils.http import urlquote


class Player(object):
    AVATAR_URL = 'http://robohash.org/'

    def __init__(self, name="", sessid=None, hand=None):
        self.id = str(uuid.uuid4())[:6].upper()
        self.name = name
        self.hand = hand or []
        self.lamp = False
        self.sessid = sessid

    def draw_cards(self, cards):
        self.hand = self.hand + cards

    def remove_card_from_hand(self, card):
        for x in range(len(self.hand)):
            if self.hand[x]["id"] == card["id"]:
                del self.hand[x]
                return

    @property
    def cards_number(self):
        return len(self.hand)

    @property
    def avatar(self):
        return self.AVATAR_URL + urlquote(self.name)

    def get_data(self, player_id=None):
        data = {
            'id': self.id,
            'name': self.name,
            'avatar': self.avatar,
            'lamp': self.lamp
        }
        if self.id == player_id:
            data['cards'] = self.hand
            data['you'] = True
        else:
            data['cards'] = [card["id"] for card in self.hand]
        return data
