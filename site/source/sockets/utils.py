from source.uno.game import Game
from source.uno.game_states import UnoState

EVENT_INITIAL_STATE = 'initial_state'
EVENT_GAME_RUNNING = 'game_running'
EVENT_USER_MESSAGE = 'user_message'
NS_NAME = '/game'


def card_data(card):
    return {
        "id": card.card_id,
        "color": card.color,
        "value": card.value
    }


def players_list(game, for_player_id):
    players = []
    for p in game.players:
        player_data = {
            "id": p.player_id,
            "name": p.name,
            "avatar": p.avatar,
            "lamp": p.lamp
        }
        if for_player_id == p.player_id:
            player_data["you"] = True
            player_data["cards"] = []
            for card in p.cards:
                player_data["cards"].append(card_data(card))
        else:
            player_data["cards"] = []
            for card in p.cards:
                player_data["cards"].append(card.card_id)

        players.append(player_data)

    return players


def game_state(game, player_id):
    assert isinstance(game, Game)

    data = {
        'player_id': player_id,
        'lead_player_id': game.current_player.player_id,
        'players_list': players_list(game, player_id),
    }

    if len(game.put_deck) > 0:
        data['top_card'] = card_data(game.put_deck[-1])

    # uno
    if isinstance(game.state, UnoState):
        for x in data['players_list']:
            if x['id'] == game.previous_player.player_id:
                x['uno'] = True

    return data


def initial_game_state(game, player_id):
    assert isinstance(game, Game)

    players = players_list(game, player_id)

    # don't show lamp when only one player in game
    if len(players) == 1:
        del players[0]["lamp"]

    return {
        'players_list': players,
    }


def send_game_initial_frontend(socket, game):
    for sessid, socket in socket.server.sockets.iteritems():
        if 'game_id' not in socket.session:
            continue
        if game.game_id == socket.session['game_id']:
            player_id = socket.session['player_id']
            data = initial_game_state(game, player_id)

            pkt = {
                "type": "event",
                "name": EVENT_INITIAL_STATE,
                "args": data,
                "endpoint": NS_NAME
            }
            socket.send_packet(pkt)


def send_game_state_frontend(socket, game):
    for sessid, socket in socket.server.sockets.iteritems():
        if 'game_id' not in socket.session:
            continue
        if game.game_id == socket.session['game_id']:
            player_id = socket.session['player_id']
            data = game_state(game, player_id)

            pkt = {
                "type": "event",
                "name": EVENT_GAME_RUNNING,
                "args": data,
                "endpoint": NS_NAME
            }
            socket.send_packet(pkt)
