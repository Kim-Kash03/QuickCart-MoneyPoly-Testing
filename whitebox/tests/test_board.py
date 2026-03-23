import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

from moneypoly.board import Board
from moneypoly.player import Player

class TestBoard(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.player = Player("Alice")

    def test_init(self):
        self.assertEqual(len(self.board.groups), 8)
        self.assertEqual(len(self.board.properties), 22)

    def test_get_property_at_valid(self):
        prop = self.board.get_property_at(1)
        self.assertIsNotNone(prop)
        self.assertEqual(prop.name, "Mediterranean Avenue")

    def test_get_property_at_invalid(self):
        self.assertIsNone(self.board.get_property_at(0))
        self.assertIsNone(self.board.get_property_at(50))

    def test_get_tile_type(self):
        self.assertEqual(self.board.get_tile_type(0), "go")
        self.assertEqual(self.board.get_tile_type(1), "property")
        self.assertEqual(self.board.get_tile_type(50), "blank") # Edge case

    def test_is_purchasable_unowned(self):
        self.assertTrue(self.board.is_purchasable(1)) # Med Avenue
        
    def test_is_purchasable_owned(self):
        prop = self.board.get_property_at(1)
        prop.owner = self.player
        self.assertFalse(self.board.is_purchasable(1))
        
    def test_is_purchasable_mortgaged(self):
        prop = self.board.get_property_at(1)
        prop.owner = None
        prop.is_mortgaged = True
        self.assertFalse(self.board.is_purchasable(1))
        
    def test_is_purchasable_special(self):
        self.assertFalse(self.board.is_purchasable(0)) # Go
        
    def test_is_special_tile(self):
        self.assertTrue(self.board.is_special_tile(0))
        self.assertTrue(self.board.is_special_tile(10))
        self.assertFalse(self.board.is_special_tile(1))
        
    def test_properties_owned_by(self):
        prop = self.board.get_property_at(1)
        prop.owner = self.player
        owned = self.board.properties_owned_by(self.player)
        self.assertIn(prop, owned)
        self.assertEqual(len(owned), 1)
        
    def test_all_special_tiles(self):
        # Branch/Edge case: all special tile mappings
        mapping = {
            0: "go", 10: "jail", 30: "go_to_jail", 20: "free_parking",
            4: "income_tax", 38: "luxury_tax",
            2: "community_chest", 17: "community_chest", 33: "community_chest",
            7: "chance", 22: "chance", 36: "chance",
            5: "railroad", 15: "railroad", 25: "railroad", 35: "railroad"
        }
        for pos, ttype in mapping.items():
            self.assertEqual(self.board.get_tile_type(pos), ttype, f"Tile at {pos} should be {ttype}")

    def test_groups_init(self):
        # Branch: coverage for _create_groups
        self.assertEqual(len(self.board.groups), 8)
        expected_keys = [
            "brown", "light_blue", "pink", "orange", 
            "red", "yellow", "green", "dark_blue"
        ]
        for key in expected_keys:
            self.assertIn(key, self.board.groups)
            self.assertEqual(self.board.groups[key].color, key)

    def test_repr(self):
        # Branch: coverage for __repr__
        self.assertIn("Board", repr(self.board))
        self.assertIn("22 properties", repr(self.board))

if __name__ == "__main__":
    unittest.main()
