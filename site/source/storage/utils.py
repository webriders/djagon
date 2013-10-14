import jsonpickle
from source.storage.exceptions import GameDoesNotExist, NoOpenedGames
from source.storage.models import StoredGame
from source.uno.game import Game


def create_new_game(game_name):
    game = Game(game_name)
    save_game(game, StoredGame.STATE_IDLE)
    return game


def save_game(game, state=None):
    stored_game, created = StoredGame.objects.get_or_create(game_id=game.game_id)
    stored_game.game_jsoned = jsonpickle.encode(game)
    if state:
        stored_game.game_state = state
    stored_game.save()


def fetch_any_game():
    try:
        game_id = StoredGame.objects.filter(
            game_state=StoredGame.STATE_OPEN
        ).order_by('?')[0].game_id
    except IndexError:
        raise NoOpenedGames()

    return fetch_game(game_id)


def fetch_game(game_id):
    try:
        stored_game = StoredGame.objects.get(game_id=game_id)
        json = stored_game.game_jsoned
        state = stored_game.game_state
    except StoredGame.DoesNotExist:
        raise GameDoesNotExist()

    return jsonpickle.decode(json), state

