from source.game.game import Game


class PlayersGameStatePacketData(dict):
    def __new__(cls, player_id, game):
        return {
            'player_id': player_id,
            'own_hand': game.players[player_id].hand,
            'lead_player_id': game.get_lead_player().id,
            'cards_amount': {p.id: p.cards_number for p in game.players.values() },
        }


class GameInitialStatePacketData(dict):

    def __new__(cls, game):
        assert isinstance(game, Game)
        players = [p.get_data() for p in game.players.values()]
        return {
            'players_number': game.players_number,
            'players_list': players,
        }
