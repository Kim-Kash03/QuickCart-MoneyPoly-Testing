import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

from moneypoly.player import Player
from moneypoly.property import Property, PropertyGroup

class TestPlayer(unittest.TestCase):
    def setUp(self):
        self.player = Player("Alice")
        self.group = PropertyGroup("Test", "blue")
        self.prop1 = Property.create("Prop 1", 1, 100, 10, self.group)
        self.prop2 = Property.create("Prop 2", 2, 200, 20, self.group)

    def test_init(self):
        self.assertEqual(self.player.name, "Alice")
        self.assertEqual(self.player.balance, 1500)
        self.assertEqual(self.player.position, 0)
        self.assertFalse(self.player.in_jail)

    def test_add_money(self):
        self.player.add_money(500)
        self.assertEqual(self.player.balance, 2000)

    def test_add_money_negative(self):
        with self.assertRaises(ValueError):
            self.player.add_money(-100)

    def test_deduct_money(self):
        self.player.deduct_money(500)
        self.assertEqual(self.player.balance, 1000)

    def test_deduct_money_negative(self):
        with self.assertRaises(ValueError):
            self.player.deduct_money(-100)

    def test_move_normal(self):
        self.player.move(5)
        self.assertEqual(self.player.position, 5)
        self.assertEqual(self.player.balance, 1500)

    def test_move_land_exactly_on_go(self):
        # Branch/Edge case: land exactly on Go
        self.player.position = 35
        self.player.move(5)
        self.assertEqual(self.player.position, 0)
        # Should collect GO_SALARY
        self.assertEqual(self.player.balance, 1700)

    def test_move_wrap_around(self):
        # Branch/Edge case: pass Go
        self.player.position = 38
        self.player.move(4)
        self.assertEqual(self.player.position, 2)
        # BUG: The logic should add GO_SALARY. 
        # User requested to use the correct expected value (1700) to verify potential fixes.
        self.assertEqual(self.player.balance, 1700)

    def test_go_to_jail(self):
        # Branch/Edge case: go to jail
        self.player.go_to_jail()
        self.assertEqual(self.player.position, 10)
        self.assertTrue(self.player.in_jail)

    def test_property_management(self):
        # Branch: add/remove properties
        self.player.add_property(self.prop1)
        self.player.add_property(self.prop2)
        self.assertIn(self.prop1, self.player.properties)
        self.assertEqual(len(self.player.properties), 2)
        
        self.player.remove_property(self.prop1)
        self.assertNotIn(self.prop1, self.player.properties)
        self.assertEqual(len(self.player.properties), 1)

    def test_net_worth(self):
        # Branch/Variable state: net worth calculation
        self.player.add_property(self.prop1)
        # BUG: net_worth does not aggregate property value. Stays at 1500.
        # Intended: 1600 (1500 balance + 100 property price from setUp)
        self.assertEqual(self.player.net_worth(), 1600)

    def test_is_bankrupt(self):
        # Branch/Edge case: bankruptcy check
        self.assertFalse(self.player.is_bankrupt())
        self.player.deduct_money(1500)
        self.assertTrue(self.player.is_bankrupt())

    def test_count_properties(self):
        # Branch: coverage for count_properties
        self.assertEqual(self.player.count_properties(), 0)
        self.player.add_property(self.prop1)
        self.assertEqual(self.player.count_properties(), 1)

    def test_status_line(self):
        # Branch: coverage for status_line
        status = self.player.status_line()
        self.assertIn("Alice", status)
        self.assertIn("1500", status)
        self.assertIn("pos=0", status)
        self.player.go_to_jail()
        status_jail = self.player.status_line()
        self.assertIn("[JAILED]", status_jail)

    def test_jail_status_properties(self):
        # Branch: coverage for JailStatus properties
        self.assertEqual(self.player.jail_turns, 0)
        self.assertEqual(self.player.get_out_of_jail_cards, 0)
        self.player.jail_turns = 2
        self.player.get_out_of_jail_cards = 1
        self.assertEqual(self.player._jail_status.jail_turns, 2)
        self.assertEqual(self.player._jail_status.get_out_of_jail_cards, 1)

    def test_repr(self):
        # Branch: coverage for __repr__
        self.assertIn("Alice", repr(self.player))
        self.assertIn("balance=1500", repr(self.player))

if __name__ == "__main__":
    unittest.main()
