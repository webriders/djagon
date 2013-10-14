import uuid
from django.utils.http import urlquote

from source.___old_game.cards import get_cards_score


class Player(object):
    AVATAR_URL = 'http://robohash.org/'

    def __init__(self, name="", sessid=None, hand=None):
        self.id = str(uuid.uuid4())[:6].upper()
        self.name = name
        self.hand = hand or []
        self.lamp = False
        self.sessid = sessid
        self.score = 0

    def draw_cards(self, cards):
        assert isinstance(cards, list)
        self.hand = self.hand + cards

    def draw_card(self, card):
        self.hand.append(card)

    def remove_card_from_hand(self, card):
        for x in range(len(self.hand)):
            if self.hand[x]["id"] == card["id"]:
                del self.hand[x]
                return

    def can_move(self, top_card):
        for card in self.hand:
            if card['color'] == 'black' or card['color'] == top_card['color'] or card['value'] == top_card['value']:
                return True
        return False

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
            'lamp': self.lamp,
            'score': self.score,
        }
        if self.id == player_id:
            data['cards'] = self.hand
            data['you'] = True
        else:
            data['cards'] = [card["id"] for card in self.hand]
        return data

    def count_score(self):
        for card in self.hand:
            self.score += get_cards_score(card)
