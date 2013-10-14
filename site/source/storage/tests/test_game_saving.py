import unittest
from source.storage import utils
from source.storage.exceptions import GameDoesNotExist
from source.storage.models import StoredGame
from source.uno.card import Card
from source.uno.player import Player


class TestGameSave(unittest.TestCase):
    def test_empty_idle_game_save(self):
        game = utils.create_new_game("TEST_GAME")
        utils.save_game(game, StoredGame.STATE_IDLE)
        restored_game, restored_state = utils.fetch_game(game.game_id)
        self.assertEqual(game.game_id, restored_game.game_id)
        self.assertEqual(StoredGame.STATE_IDLE, restored_state)

    def test_filled_idle_game_save(self):
        game = utils.create_new_game("TEST_GAME")
        player1 = Player("Player1")
        player2 = Player("Player2")
        player3 = Player("Player3")
        player1._cards = [
            Card.factory(game, "green", "2"),
            Card.factory(game, "red", "3"),
            Card.factory(game, "blue", "4")
        ]
        player2._cards = [
            Card.factory(game, "green", "2"),
            Card.factory(game, "red", "3"),
            Card.factory(game, "blue", "4")
        ]
        player3._cards = [
            Card.factory(game, "green", "2"),
            Card.factory(game, "red", "3"),
            Card.factory(game, "blue", "4")
        ]
        game.add_player(player1)
        game.add_player(player2)
        game.add_player(player3)

        utils.save_game(game, StoredGame.STATE_IDLE)
        restored_game, restored_state = utils.fetch_game(game.game_id)
        self.assertEqual(game.game_id, restored_game.game_id)
        self.assertEqual(StoredGame.STATE_IDLE, restored_state)
        self.assertEqual(len(game.players), len(restored_game.players))
        self.assertEqual(len(game.players[0].cards), len(restored_game.players[0].cards))
        self.assertEqual(len(game.players[1].cards), len(restored_game.players[1].cards))
        self.assertEqual(len(game.players[2].cards), len(restored_game.players[2].cards))

    def test_fetch_fail(self):
        self.assertRaises(GameDoesNotExist, utils.fetch_game, "absent_game_id")


if __name__ == '__main__':
    unittest.main()