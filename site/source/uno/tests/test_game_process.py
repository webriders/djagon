import unittest
from source.uno.card import Card
from source.uno.game import Game
from source.uno.game_states import NormalState
from source.uno.player import Player


class TestGameStart(unittest.TestCase):
    def setUp(self):
        self.game = Game("TEST_GAME")
        self.game.add_player(Player("Player1"))
        self.game.add_player(Player("Player2"))
        self.game.add_player(Player("Player3"))
        self.game.start_game()

    def test_5_cards_given_to_players(self):
        for player in self.game.players:
            if not player == self.game.current_player:
                assert len(player.cards) == 5, "There {0} cards, must be 5".format(len(player.cards))

    def test_one_card_opened(self):
        assert len(self.game.put_deck) == 1

    def tearDown(self):
        pass


class TestGameTurn(unittest.TestCase):
    def setUp(self):
        self.game = Game("TEST_GAME")

        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")

        self.player1._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "3"),
            Card.factory(self.game, "blue", "4")
        ]
        self.player2._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "3"),
            Card.factory(self.game, "blue", "4")
        ]
        self.player3._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "3"),
            Card.factory(self.game, "blue", "4")
        ]

        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)

        self.game._get_deck = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "3"),
            Card.factory(self.game, "blue", "4")
        ]
        self.game._put_deck = [
            Card.factory(self.game, "green", "2")
        ]

        self.game.state = NormalState(self.game)

    def test_basic_turn(self):
        self.game.move_to_player(self.player1)
        assert len(self.game.current_player.cards) == 3
        self.game.perform_turn(self.player1, self.player1.cards[0])
        assert len(self.player1.cards) == 2, "Player have {0} cards, must be 3".format(len(self.player1.cards))

    def test_wrong_turn(self):
        self.game.move_to_player(self.player1)
        assert len(self.game.current_player.cards) == 3
        self.game.perform_turn(self.player1, self.player1.cards[1])
        assert len(self.player1.cards) == 3, "Player have {0} cards, must be 3".format(len(self.player1.cards))

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()