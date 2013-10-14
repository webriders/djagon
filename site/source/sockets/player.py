from source.uno.game import Game
from source.uno.player import Player


class SocketPlayer(object):
    """ Socket level player. It is bounded to some player of specified Game """

    def __init__(self, socket_player_id, game, player_name):
        assert isinstance(game, Game)

        self._socket_player_id = socket_player_id
        self._game = game

        self._player = Player(player_name)
        self._game.players.append(self._player)

    @property
    def socket_player_id(self):
        return self._socket_player_id

    @property
    def player(self):
        return self._player

    @property
    def game(self):
        return self._game

