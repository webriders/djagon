import unittest
from source.uno.card import Card
from source.uno.game import Game
from source.uno.game_states import NormalState
from source.uno.player import Player

class TestCardsPutOn(unittest.TestCase):
    def test_basic_cards_rule(self):
        card1 = Card.factory(None, "green", "9")
        card2 = Card.factory(None, "red", "9")
        card3 = Card.factory(None, "blue", "3")
        card4 = Card.factory(None, "blue", "5")
        card5 = Card.factory(None, "red", "7")
        card6 = Card.factory(None, "black", "wild", "red")
        card7 = Card.factory(None, "black", "draw-four", "blue")

        assert card1.can_put_on(card2)
        assert not card1.can_put_on(card3)
        assert not card1.can_put_on(card4)
        assert not card1.can_put_on(card5)
        assert not card1.can_put_on(card6)
        assert not card1.can_put_on(card7)

        assert card2.can_put_on(card1)
        assert not card2.can_put_on(card3)
        assert not card2.can_put_on(card4)
        assert card2.can_put_on(card5)
        assert card2.can_put_on(card6)
        assert not card2.can_put_on(card7)

        assert not card3.can_put_on(card1)
        assert not card3.can_put_on(card2)
        assert card3.can_put_on(card4)
        assert not card3.can_put_on(card5)
        assert not card3.can_put_on(card6)
        assert card3.can_put_on(card7)

        assert not card4.can_put_on(card1)
        assert not card4.can_put_on(card2)
        assert card4.can_put_on(card3)
        assert not card4.can_put_on(card5)
        assert not card4.can_put_on(card6)
        assert card4.can_put_on(card7)

        assert not card5.can_put_on(card1)
        assert card5.can_put_on(card2)
        assert not card5.can_put_on(card3)
        assert not card5.can_put_on(card4)
        assert card5.can_put_on(card6)
        assert not card5.can_put_on(card7)

        assert card6.can_put_on(card1)
        assert card6.can_put_on(card2)
        assert card6.can_put_on(card3)
        assert card6.can_put_on(card4)
        assert card6.can_put_on(card5)
        assert card6.can_put_on(card7)

        assert card7.can_put_on(card1)
        assert card7.can_put_on(card2)
        assert card7.can_put_on(card3)
        assert card7.can_put_on(card4)
        assert card7.can_put_on(card5)
        assert card7.can_put_on(card6)


class TestTurnIn(unittest.TestCase):
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

    def test_correct_turn_in(self):
        self.game.move_to_player(self.player1)
        self.game.perform_turn(self.player2, self.player2.cards[0])
        assert len(self.player2.cards) == 2
        assert self.game.current_player == self.player3

    def test_incorrect_turn_in(self):
        self.game.move_to_player(self.player1)
        self.game.perform_turn(self.player2, self.player2.cards[0])
        assert len(self.player2.cards) == 2
        assert self.game.current_player == self.player3


class TestReverse(unittest.TestCase):
    def setUp(self):
        self.game = Game("TEST_GAME")

        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")

        self.player1._cards = [
            Card.factory(self.game, "green", "reverse"),
            Card.factory(self.game, "red", "3"),
            Card.factory(self.game, "blue", "4")
        ]
        self.player2._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "reverse"),
            Card.factory(self.game, "blue", "4")
        ]
        self.player3._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "3"),
            Card.factory(self.game, "blue", "reverse")
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

    def test_reverse_card(self):
        self.game.current_player = self.player1
        self.game.perform_turn(self.player1, self.player1.cards[0])
        assert len(self.game.put_deck) == 2
        assert self.game.current_player == self.player3
        self.game.perform_turn(self.player3, self.player3.cards[-1])
        assert self.game.current_player == self.player1


class TestBlackCards(unittest.TestCase):
    def setUp(self):
        self.game = Game("TEST_GAME")

        self.player1 = Player("Player1")
        self.player2 = Player("Player2")
        self.player3 = Player("Player3")

        self.player1._cards = [
            Card.factory(self.game, "black", "wild", "blue"),
            Card.factory(self.game, "black", "draw-four"),
            Card.factory(self.game, "blue", "4")
        ]
        self.player2._cards = [
            Card.factory(self.game, "green", "2"),
            Card.factory(self.game, "red", "reverse"),
            Card.factory(self.game, "blue", "4")
        ]

        self.game.add_player(self.player1)
        self.game.add_player(self.player2)

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

    def test_black_wild(self):
        self.game.perform_turn(self.player1, self.player1.cards[0])
        self.assertEqual(self.game.current_player, self.player2)
        self.assertEqual(len(self.player2.cards), 3)
        self.assertFalse(self.player2.cards[0].can_put_on(self.game.put_deck[-1]))
        self.assertFalse(self.player2.cards[1].can_put_on(self.game.put_deck[-1]))
        self.assertTrue(self.player2.cards[2].can_put_on(self.game.put_deck[-1]))


    def test_black_draw_four(self):
        self.game.perform_turn(self.player1, self.player1.cards[0])
        self.assertEqual(self.game.current_player, self.player2)
        self.assertEqual(len(self.player2.cards), 3)
        self.assertFalse(self.player2.cards[0].can_put_on(self.game.put_deck[-1]))
        self.assertFalse(self.player2.cards[1].can_put_on(self.game.put_deck[-1]))
        self.assertTrue(self.player2.cards[2].can_put_on(self.game.put_deck[-1]))


if __name__ == '__main__':
    unittest.main()