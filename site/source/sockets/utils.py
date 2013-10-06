from source.uno.game import Game


def game_state(game, player_id):
    data = {
        'player_id': player_id,
        'lead_player_id': game.current_player.id,
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
    players = [p.get_data(player_id) for p in game.players.values()]
    if len(players) == 1:
        del players[0]["lamp"]
    return {
        'players_list': players,
    }


def game_state_frontend(game):
    for sessid, socket in socket.server.sockets.iteritems():
        if 'game_id' not in socket.session:
            continue
        if game.game_id == socket.session['game_id']:
            player_id = socket.session['player_id']
            data = GameState(player_id, game)

            pkt = {
                "type": "event",
                "name": self.EVENT_GAME_RUNNING,
                "args": data,
                "endpoint": self.ns_name
            }
            socket.send_packet(pkt)
