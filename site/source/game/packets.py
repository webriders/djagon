from source.game.game import Game


class GameState(dict):
    def __new__(cls, player_id, game):
        return {
            'player_id': player_id,
            'lead_player_id': game.get_lead_player().id,
            'players_list': [p.get_data(player_id) for p in game.players.values()]
        }

class InitialGameState(dict):

    def __new__(cls, player_id, game):
        assert isinstance(game, Game)
        players = [p.get_data(player_id) for p in game.players.values()]
        if len(players) == 1:
            del players[0]["lamp"]
        return {
            'players_list': players,
        }
