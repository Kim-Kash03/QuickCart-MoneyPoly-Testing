import unittest
import sys
import os

# Add the code directory to the Python path so we can import moneypoly
sys.path.append(os.path.join(os.path.dirname(__file__), 'code', 'moneypoly'))

from moneypoly.bank import Bank
from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup

class TestBankWhiteBox(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.player = Player("Test")
        self.initial_funds = self.bank.get_balance()

    def test_pay_out_negative_amount(self):
        # Branch/Edge case: amount <= 0
        paid = self.bank.pay_out(0)
        self.assertEqual(paid, 0)
        self.assertEqual(self.bank.get_balance(), self.initial_funds)

    def test_pay_out_insufficient_funds(self):
        # Branch/Edge case: amount > self._funds
        with self.assertRaises(ValueError):
            self.bank.pay_out(self.initial_funds + 1)

    def test_pay_out_success(self):
        # Branch: normal payout execution
        amount = 500
        paid = self.bank.pay_out(amount)
        self.assertEqual(paid, amount)
        self.assertEqual(self.bank.get_balance(), self.initial_funds - amount)

    def test_give_loan_negative_amount(self):
        # Branch/Edge case: amount <= 0
        self.bank.give_loan(self.player, -100)
        self.assertEqual(self.player.balance, 1500) # Assuming default starting balance
        self.assertEqual(self.bank.get_balance(), self.initial_funds)

    def test_give_loan_success(self):
        # Branch: Give loan normal execution
        amount = 500
        self.bank.give_loan(self.player, amount)
        self.assertEqual(self.player.balance, 1500 + amount, "Player balance should increase")
        # Logical Issue test: The bank's funds MUST decrease when giving a loan.
        self.assertEqual(self.bank.get_balance(), self.initial_funds - amount, "Bank funds should decrease by loan amount")


class TestPlayerWhiteBox(unittest.TestCase):
    def setUp(self):
        self.player = Player("Test")

    def test_add_money_negative(self):
        # Branch/Edge case: amount < 0
        with self.assertRaises(ValueError):
            self.player.add_money(-50)
            
    def test_deduct_money_negative(self):
        # Branch/Edge case: amount < 0
        with self.assertRaises(ValueError):
            self.player.deduct_money(-50)

    def test_move_normal(self):
        # Branch: normal move without passing Go
        self.player.position = 5
        initial_balance = self.player.balance
        self.player.move(5)
        self.assertEqual(self.player.position, 10, "Position should be updated to 10")
        self.assertEqual(self.player.balance, initial_balance, "Balance should not change when not passing Go")

    def test_move_land_on_go(self):
        # Branch: move and land exactly on Go (position 0)
        self.player.position = 35
        initial_balance = self.player.balance
        self.player.move(5)  # 35 + 5 = 40 -> 0
        self.assertEqual(self.player.position, 0)
        from moneypoly.config import GO_SALARY
        self.assertEqual(self.player.balance, initial_balance + GO_SALARY, "Balance should increase by GO_SALARY when landing on Go")

    def test_move_pass_go(self):
        # Branch: move and pass Go (position wraps around to > 0)
        self.player.position = 38
        initial_balance = self.player.balance
        self.player.move(5)  # 38 + 5 = 43 -> 3
        self.assertEqual(self.player.position, 3)
        from moneypoly.config import GO_SALARY
        # Logical Issue test: Documentations states you get Go salary if you pass Go
        self.assertEqual(self.player.balance, initial_balance + GO_SALARY, "Balance should increase by GO_SALARY when passing Go")


class TestPropertyWhiteBox(unittest.TestCase):
    def setUp(self):
        self.group = PropertyGroup("Test Group", "blue")
        self.prop1 = Property("Prop 1", 1, 100, 10, self.group)
        self.prop2 = Property("Prop 2", 2, 100, 10, self.group)
        self.player = Player("Test")

    def test_all_owned_by_none(self):
        # Branch: player is None
        self.assertFalse(self.group.all_owned_by(None))

    def test_all_owned_by_none_owned(self):
        # Edge case: No properties owned by player
        self.assertFalse(self.group.all_owned_by(self.player))

    def test_all_owned_by_some(self):
        # Edge case: Only some properties owned by player
        self.prop1.owner = self.player
        # Logical Issue test: Should return False since prop2 is not owned by the player
        self.assertFalse(self.group.all_owned_by(self.player), "all_owned_by should return False if player only owns SOME properties in the group")

    def test_all_owned_by_all(self):
        # Branch/Variable state: All properties owned by player
        self.prop1.owner = self.player
        self.prop2.owner = self.player
        self.assertTrue(self.group.all_owned_by(self.player))

class TestDiceWhiteBox(unittest.TestCase):
    def setUp(self):
        from moneypoly.dice import Dice
        self.dice = Dice()

    def test_roll_and_total(self):
        # Branch: test that total equals die1 + die2 and streaks update
        total = self.dice.roll()
        self.assertEqual(total, self.dice.die1 + self.dice.die2)
        if self.dice.is_doubles():
            self.assertEqual(self.dice.doubles_streak, 1)
        else:
            self.assertEqual(self.dice.doubles_streak, 0)

    def test_reset(self):
        self.dice.die1 = 5
        self.dice.die2 = 5
        self.dice.doubles_streak = 2
        self.dice.reset()
        self.assertEqual(self.dice.die1, 0)
        self.assertEqual(self.dice.die2, 0)
        self.assertEqual(self.dice.doubles_streak, 0)


class TestBoardWhiteBox(unittest.TestCase):
    def setUp(self):
        from moneypoly.board import Board
        self.board = Board()

    def test_get_tile_type_special(self):
        # Branch/Edge case: exact match for a special tile
        tile = self.board.get_tile_type(0)
        self.assertEqual(tile, "go")

    def test_get_tile_type_property(self):
        # Branch/Edge case: match for a property tile
        tile = self.board.get_tile_type(1) # Mediterranean Ave
        self.assertEqual(tile, "property")

    def test_is_purchasable_unowned(self):
        # Branch: property is unowned and not mortgaged
        self.assertTrue(self.board.is_purchasable(1))

    def test_is_purchasable_owned(self):
        # Branch: property is owned
        prop = self.board.get_property_at(1)
        from moneypoly.player import Player
        player = Player("P1")
        prop.owner = player
        self.assertFalse(self.board.is_purchasable(1))

    def test_is_purchasable_special(self):
        # Branch: not a property so returning False
        self.assertFalse(self.board.is_purchasable(0))


class TestCardsWhiteBox(unittest.TestCase):
    def setUp(self):
        from moneypoly.cards import CardDeck
        self.deck = CardDeck([{"action": "test", "value": 1}])

    def test_draw_empty(self):
        from moneypoly.cards import CardDeck
        deck = CardDeck([])
        self.assertIsNone(deck.draw())

    def test_draw_cycle(self):
        card = self.deck.draw()
        self.assertEqual(card["action"], "test")
        # next draw wraps around
        card2 = self.deck.draw()
        self.assertEqual(card2["action"], "test")
        self.assertEqual(self.deck.index, 2)

    def test_peek(self):
        card = self.deck.peek()
        self.assertEqual(card["action"], "test")
        self.assertEqual(self.deck.index, 0)


class TestGameWhiteBox(unittest.TestCase):
    def setUp(self):
        from moneypoly.game import Game
        self.game = Game(["Player1", "Player2"])

    def test_current_player_and_advance_turn(self):
        p1 = self.game.current_player()
        self.assertEqual(p1.name, "Player1")
        self.game.advance_turn()
        p2 = self.game.current_player()
        self.assertEqual(p2.name, "Player2")
        self.assertEqual(self.game.turn_number, 1)

    def test_check_bankruptcy(self):
        # Edge case/Branch: player is bankrupt
        p1 = self.game.current_player()
        p1.balance = -10
        self.game._check_bankruptcy(p1)
        self.assertTrue(p1.is_eliminated)
        self.assertNotIn(p1, self.game.players)

    def test_find_winner_logical_issue(self):
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        p1.balance = 2000
        p2.balance = 1000
        # Logical Issue test: currently find_winner returns min instead of max
        winner = self.game.find_winner()
        self.assertEqual(winner.name, "Player1", "Logical Issue: find_winner uses min() instead of max()")


if __name__ == '__main__':
    unittest.main()
