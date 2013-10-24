from source.uno.game import Game

EVENT_INITIAL_STATE = 'initial_state'
EVENT_GAME_RUNNING = 'game_running'
EVENT_USER_MESSAGE = 'user_message'
NS_NAME = '/game'


def game_state(game, player_id):
    data = {
        'player_id': player_id,
        'lead_player_id': game.current_player.player_id,
        'players_list': [p.player_id for p in game.players],
    }

    top_card = game.put_deck[-1]
    if top_card:
        data['top_card'] = game.deck.get_top_card()

    # uno
    if game.previous_lead and len(game.players[game.previous_lead].cards) == 1:
        for x in data['players_list']:
            if x['id'] == game.previous_lead:
                x['uno'] = True

    return data


def initial_game_state(game, player_id):
    assert isinstance(game, Game)

    players = []
    for p in game.players:
        players.append({
            "id": p.player_id,
            "name": p.name,
            "avatar": p.avatar,
            "lamp": p.lamp
        })

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
