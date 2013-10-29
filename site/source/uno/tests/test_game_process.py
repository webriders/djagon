import unittest
from source.uno.card import Card
from source.uno.exceptions import WrongTurnException
from source.uno.game import Game
from source.uno.game_states import NormalState, EndState, UnoState
from source.uno.player import Player


class TestGameStart(unittest.TestCase):
    def setUp(self):
        self.game = Game("TEST_GAME")
        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")
        self.player4 = Player("Player3")
        self.player5 = Player("Player3")
        self.game.add_player(self.player1)
        self.game.add_player(self.player2)
        self.game.add_player(self.player3)
        self.game.add_player(self.player4)
        self.game.add_player(self.player5)
        self.game.start_game()

    def test_5_cards_given_to_players(self):
        self.assertEqual(len(self.game.previous_player.cards), 4)
        self.assertEqual(len(self.game.get_nth_next_player(1).cards), 5)
        self.assertEqual(len(self.game.get_nth_next_player(2).cards), 5)

    def test_5_cards_given_to_players_on_game_restart(self):
        self.game.start_game()
        self.assertEqual(len(self.game.previous_player.cards), 4)
        self.assertEqual(len(self.game.get_nth_next_player(1).cards), 5)
        self.assertEqual(len(self.game.get_nth_next_player(2).cards), 5)

    def test_one_card_opened(self):
        self.assertEqual(len(self.game.put_deck), 1)


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
        self.assertEqual(len(self.game.current_player.cards), 3)
        self.game.perform_turn(self.player1, self.player1.cards[0])
        self.assertEqual(len(self.player1.cards), 2, "Player have {0} cards, must be 3".format(len(self.player1.cards)))

    def test_wrong_turn(self):
        self.game.move_to_player(self.player1)
        self.assertEqual(len(self.game.current_player.cards), 3)

        self.assertRaises(WrongTurnException, self.game.perform_turn, self.player1, self.player1.cards[1])


class TestGameFinish(unittest.TestCase):
    def setUp(self):
        self.game = Game("TEST_GAME")

        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")

        self.player1._cards = [
            Card.factory(self.game, "green", "2"),
        ]
        self.player2._cards = [
            Card.factory(self.game, "green", "2"),
        ]
        self.player3._cards = [
            Card.factory(self.game, "green", "2"),
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

    def test_game_finish(self):
        self.game.current_player = self.player1
        self.game.perform_turn(self.player1, self.player1.cards[0])
        self.assertIsInstance(self.game.state, EndState)


class TestUnoState(unittest.TestCase):
    def setUp(self):
        self.game = Game("TEST_GAME")

        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")

        self.player1._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "2"),
        ]
        self.player2._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "2"),
        ]
        self.player3._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "2"),
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

    def test_enter_uno_state(self):
        self.game.current_player = self.player1
        self.game.perform_turn(self.player1, self.player1.cards[0])
        self.assertIsInstance(self.game.state, UnoState)

    def test_enter_uno_state(self):
        self.game.current_player = self.player1
        self.game.perform_turn(self.player1, self.player1.cards[0])
        self.assertIsInstance(self.game.state, UnoState)


class TestDrawCard(unittest.TestCase):

    def setUp(self):
        self.game = Game("TEST_GAME")
        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")

        self.player1._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "2"),
        ]
        self.player2._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "2"),
        ]
        self.player3._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "2"),
        ]

        self.game._get_deck = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "3"),
            Card.factory(self.game, "blue", "4")
        ]
        self.game._put_deck = [
            Card.factory(self.game, "green", "2")
        ]

        self.game.state = NormalState(self.game)
        self.game.current_player = self.player1

    def test_take_card_when_current(self):
        self.game.draw_card(self.player1)
        self.assertEqual(len(self.player1.cards), 3)
        self.assertEqual(len(self.game.get_deck), 2)

    def test_take_card_when_not_current_fails(self):
        self.assertRaises(WrongTurnException, self.game.draw_card, self.player2)
        self.assertEqual(len(self.player2.cards), 2)
        self.assertEqual(len(self.game.get_deck), 3)

if __name__ == '__main__':
    unittest.main()