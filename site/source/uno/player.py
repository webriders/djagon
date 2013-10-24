from django.utils.http import urlquote
from source.storage import id_generator


class Player(object):
    AVATAR_URL = 'http://robohash.org/'

    def __init__(self, name):
        self._player_id = id_generator.new_id()
        self._name = name
        self._cards = []
        self._lamp = False
        self._session_id = None

    # Sockets related
    @property
    def session_id(self):
        return self._session_id

    @session_id.setter
    def session_id(self, session_id):
        self._session_id = session_id

    @property
    def avatar(self):
        return self.AVATAR_URL + urlquote(self.name)

    # Uno related
    @property
    def player_id(self):
        return self._player_id

    def eq(self, other):
        return self.name == other.name

    @property
    def name(self):
        return self._name

    @property
    def cards(self):
        return self._cards

    @property
    def lamp(self):
        return self._lamp

    @lamp.setter
    def lamp(self, x):
        self._lamp = x

    def has_card(self, card):
        return card in self.cards

    def has_card_to_put_on(self, card):
        for x in self.cards:
            if x.can_put_on(card):
                return True
        return False

    def remove_card(self, card):
        self.cards.remove(card)
