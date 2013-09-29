from cards import generate_cards
import random


class UnoDeck(object):
    stack = None  # hidden cards
    deck = None  # shown cards

    def __init__(self):
        self.stack = generate_cards()
        self.deck = []
        random.shuffle(self.stack)

    def draw_cards(self, n):
        if len(self.stack) < n:
            self.turn_deck()
        cards = self.stack[-n:]
        self.stack = self.stack[:-n]
        return cards

    def draw_card(self):
        if not self.stack:
            self.turn_deck()
        return self.stack.pop()

    def put_card(self, card):
        self.deck.append(card)

    def turn_deck(self):
        top_card = self.deck.pop()
        self.deck.reverse()
        self.stack = self.deck + self.stack
        self.deck = [top_card]

    def get_top_card(self):
        return self.deck[-1]
