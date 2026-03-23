import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

from moneypoly.cards import CardDeck

class TestCards(unittest.TestCase):
    def setUp(self):
        self.cards_data = [{"id": 1}, {"id": 2}, {"id": 3}]
        self.deck = CardDeck(self.cards_data)

    def test_init_and_len(self):
        self.assertEqual(len(self.deck), 3)
        self.assertEqual(repr(self.deck), "CardDeck(3 cards, next=0)")

    def test_draw_cycles(self):
        self.assertEqual(self.deck.draw()["id"], 1)
        self.assertEqual(self.deck.draw()["id"], 2)
        self.assertEqual(self.deck.draw()["id"], 3)
        self.assertEqual(self.deck.draw()["id"], 1) # Cycle repeats
        self.assertEqual(self.deck.index, 4)

    def test_draw_empty(self):
        deck = CardDeck([])
        self.assertIsNone(deck.draw())

    def test_peek(self):
        self.assertEqual(self.deck.peek()["id"], 1)
        self.assertEqual(self.deck.index, 0) # Index should not advance
        self.assertEqual(self.deck.peek()["id"], 1)

    def test_peek_empty(self):
        deck = CardDeck([])
        self.assertIsNone(deck.peek())

    def test_reshuffle(self):
        self.deck.draw() # Index = 1
        self.deck.reshuffle()
        self.assertEqual(self.deck.index, 0)
        self.assertEqual(len(self.deck), 3)

    def test_cards_remaining(self):
        self.assertEqual(self.deck.cards_remaining(), 3)
        self.deck.draw()
        self.assertEqual(self.deck.cards_remaining(), 2)
        self.deck.draw()
        self.deck.draw()
        self.assertEqual(self.deck.cards_remaining(), 3) # Cycles back to 3

    def test_chance_deck_valid(self):
        from moneypoly.cards import CHANCE_CARDS
        self.assertEqual(len(CHANCE_CARDS), 12)
        actions = set()
        for card in CHANCE_CARDS:
            self.assertIn("action", card)
            self.assertIn("value", card)
            self.assertIn("description", card)
            actions.add(card["action"])
        
        expected_actions = {
            "move_to", "collect", "jail", "pay", 
            "jail_free", "collect_from_all"
        }
        self.assertEqual(actions, expected_actions)

    def test_community_chest_deck_valid(self):
        from moneypoly.cards import COMMUNITY_CHEST_CARDS
        self.assertEqual(len(COMMUNITY_CHEST_CARDS), 12)
        actions = set()
        for card in COMMUNITY_CHEST_CARDS:
            self.assertIn("action", card)
            self.assertIn("value", card)
            self.assertIn("description", card)
            actions.add(card["action"])
        
        expected_actions = {
            "collect", "pay", "jail", "birthday", "jail_free"
        }
        self.assertEqual(actions, expected_actions)

    def test_repr(self):
        self.assertIn("CardDeck", repr(self.deck))
        self.assertIn("3 cards", repr(self.deck))

if __name__ == "__main__":
    unittest.main()
