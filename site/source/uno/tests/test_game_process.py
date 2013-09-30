import unittest
from source.uno.game import Game
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

        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)

    def test_one_turn(self):
        for x in range(10):
            self.game.start_game()
            for card in self.game.current_player.cards:
                if card.can_put_on(self.game.put_deck[-1]):
                    self.game.perform_turn(self.game.current_player, card)
                    assert len(self.game.previous_player.cards) == 4, "There {0} cards, must be 4".format(len(self.game.previous_player.cards))
                    return
            assert len(self.game.current_player.cards) == 5

    def tearDown(self):
        pass


if __name__ == '__main__':
    unittest.main()