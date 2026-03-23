import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

from moneypoly.property import Property, PropertyGroup
from moneypoly.player import Player

class TestProperty(unittest.TestCase):
    def setUp(self):
        self.group = PropertyGroup("Test Group", "blue")
        self.prop1 = Property.create("Prop 1", 1, 100, 10, self.group)
        self.prop2 = Property.create("Prop 2", 2, 100, 10, self.group)
        self.player = Player("Alice")

    def test_all_owned_by_none(self):
        self.assertFalse(self.group.all_owned_by(None))

    def test_all_owned_by_player_empty(self):
        self.assertFalse(self.group.all_owned_by(self.player))

    def test_all_owned_by_player_partial(self):
        self.prop1.owner = self.player
        # BUG: The logic returns True prematurely (uses any() instead of all()).
        # Intended: Should be False as p2 is unowned.
        self.assertFalse(self.group.all_owned_by(self.player))

    def test_all_owned_by_player_full(self):
        self.prop1.owner = self.player
        self.prop2.owner = self.player
        self.assertTrue(self.group.all_owned_by(self.player))

    def test_get_rent_unowned(self):
        self.assertEqual(self.prop1.get_rent(), 10)

    def test_get_rent_mortgaged(self):
        self.prop1.owner = self.player
        self.prop1.mortgage()
        self.assertEqual(self.prop1.get_rent(), 0)

    def test_get_rent_full_group(self):
        self.prop1.owner = self.player
        self.prop2.owner = self.player
        self.assertEqual(self.prop1.get_rent(), 20) # 2x base rent

    def test_mortgage_normal(self):
        self.prop1.owner = self.player
        self.assertFalse(self.prop1.is_mortgaged)
        val = self.prop1.mortgage()
        self.assertEqual(val, 50) # Half price
        self.assertTrue(self.prop1.is_mortgaged)

    def test_mortgage_already_mortgaged(self):
        self.prop1.owner = self.player
        self.prop1.mortgage()
        self.assertEqual(self.prop1.mortgage(), 0)

    def test_unmortgage_normal(self):
        self.prop1.owner = self.player
        self.prop1.mortgage()
        val = self.prop1.unmortgage()
        self.assertEqual(val, int(50 * 1.1)) # 110% of mortgage value = 55
        self.assertFalse(self.prop1.is_mortgaged)

    def test_unmortgage_not_mortgaged(self):
        self.prop1.owner = self.player
        self.assertEqual(self.prop1.unmortgage(), 0)

    def test_auto_registration(self):
        # Branch: coverage for __init__ auto-registration
        group = PropertyGroup("Extra", "white")
        prop = Property.create("Extra Prop", 50, 100, 10, group)
        self.assertIn(prop, group.properties)

    def test_property_config(self):
        # Branch: coverage for PropertyConfig dataclass
        from moneypoly.property import PropertyConfig
        cfg = PropertyConfig("cfg", 10, 100, 20, self.group)
        self.assertEqual(cfg.name, "cfg")
        self.assertEqual(cfg.position, 10)
        self.assertEqual(cfg.price, 100)
        self.assertEqual(cfg.base_rent, 20)
        self.assertEqual(cfg.group, self.group)

    def test_property_create(self):
        # Branch/Variable state: verification of create() classmethod
        prop = Property.create("Named", 15, 200, 25, self.group)
        self.assertEqual(prop.name, "Named")
        self.assertEqual(prop.position, 15)
        self.assertEqual(prop.price, 200)
        self.assertEqual(prop.base_rent, 25)
        self.assertEqual(prop.group, self.group)

    def test_is_available(self):
        # Branch: coverage for is_available
        self.assertTrue(self.prop1.is_available())
        self.prop1.owner = self.player
        self.assertFalse(self.prop1.is_available())
        self.prop1.owner = None
        self.prop1.mortgage()
        self.assertFalse(self.prop1.is_available())

    def test_owner_counts(self):
        # Branch/Variable state: multiple owners in group
        self.prop1.owner = self.player
        p2 = Player("Bob")
        self.prop2.owner = p2
        counts = self.group.get_owner_counts()
        self.assertEqual(counts[self.player], 1)
        self.assertEqual(counts[p2], 1)

    def test_add_property_backlink(self):
        # Branch: coverage for add_property back-linking
        group2 = PropertyGroup("NewGroup", "grey")
        self.group.add_property(self.prop1)
        group2.add_property(self.prop1)
        self.assertEqual(self.prop1.group, group2)
        self.assertIn(self.prop1, group2.properties)

    def test_group_size(self):
        # Branch: size() coverage
        self.assertEqual(self.group.size(), 2) # prop1 and prop2 added in setUp

    def test_reprs(self):
        # Branch: coverage for __repr__ methods
        self.assertIn("Property", repr(self.prop1))
        self.assertIn("Prop 1", repr(self.prop1))
        self.assertIn("PropertyGroup", repr(self.group))
        self.assertIn("Test Group", repr(self.group))

if __name__ == "__main__":
    unittest.main()
