from collections import OrderedDict
from source.game.uno_deck import UnoDeck
from source.game.player import Player
from source.game.models import GameTable

import jsonpickle
import random
import uuid


class UnoGame(object):
    INIT_CARDS_NUMBER = 5
    DIRECTION_DIRECT = 1
    DIRECTION_REVERSE = -1

    players = OrderedDict()
    current_lead = None # index of current player

    def __init__(self):
        self.game_id  = str(uuid.uuid4())[:6].upper()
        self.direction = self.DIRECTION_DIRECT
        self.deck = UnoDeck()

    def save(self):
        game, created = GameTable.objects.get_or_create(game_id=self.game_id)
        game.state = jsonpickle.encode(self)
        game.save()

    def join_game(self):
        number = len(self.players) + 1
        default_name = "Player_%s" % number
        player = Player(name=default_name)
        self.players[player.id] = player
        self.save()
        return player

    def start(self):
        players_number = len(self.players)
        self.current_lead = random.randrange(players_number)
        for player in list(self.players):
            player.hand = self.deck.draw_cards(self.INIT_CARDS_NUMBER)
        self.save()

    def get_next_player(self):
        players_number = len(self.players)
        self.current_lead = (self.current_lead + self.direction) % players_number
        return self.players.values()[self.current_lead]

    def change_direction(self):
        self.direction = -self.direction
        self.save()
