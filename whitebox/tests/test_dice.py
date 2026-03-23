import unittest
import sys
import os
import random
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

from moneypoly.dice import Dice

class TestDice(unittest.TestCase):
    def setUp(self):
        self.dice = Dice()

    def test_reset(self):
        self.dice.die1 = 3
        self.dice.die2 = 3
        self.dice.doubles_streak = 2
        self.dice.reset()
        self.assertEqual(self.dice.die1, 0)
        self.assertEqual(self.dice.die2, 0)
        self.assertEqual(self.dice.doubles_streak, 0)

    def test_roll_doubles(self):
        # Mock random to return doubles
        orig_randint = random.randint
        random.randint = lambda a, b: 4
        try:
            total = self.dice.roll()
            self.assertEqual(total, 8)
            self.assertTrue(self.dice.is_doubles())
            self.assertEqual(self.dice.doubles_streak, 1)
        finally:
            random.randint = orig_randint

    def test_roll_non_doubles(self):
        # Mock random to return different values
        rolls = [2, 5]
        orig_randint = random.randint
        random.randint = lambda a, b: rolls.pop(0)
        try:
            self.dice.doubles_streak = 2 # Start with a streak
            total = self.dice.roll()
            self.assertEqual(total, 7)
            self.assertFalse(self.dice.is_doubles())
            self.assertEqual(self.dice.doubles_streak, 0) # Should reset
        finally:
            random.randint = orig_randint

    def test_total(self):
        self.dice.die1 = 1
        self.dice.die2 = 6
        self.assertEqual(self.dice.total(), 7)

    def test_describe(self):
        self.dice.die1 = 3
        self.dice.die2 = 4
        self.assertEqual(self.dice.describe(), "3 + 4 = 7")

        self.dice.die1 = 6
        self.dice.die2 = 6
        self.assertEqual(self.dice.describe(), "6 + 6 = 12 (DOUBLES)")

    def test_initial_state(self):
        dice = Dice()
        self.assertEqual(dice.die1, 0)
        self.assertEqual(dice.die2, 0)
        self.assertEqual(dice.doubles_streak, 0)

    def test_roll_range(self):
        # Branch/Variable state: many rolls
        for _ in range(100):
            val = self.dice.roll()
            self.assertGreaterEqual(val, 2)
            self.assertLessEqual(val, 10) # 1-5 + 1-5 = 10

    def test_multiple_doubles_streak(self):
        # Branch/Variable state: consecutive doubles
        orig_randint = random.randint
        # Force three consecutive doubles
        random.randint = lambda a, b: 2
        try:
            self.dice.roll() # streak 1
            self.assertEqual(self.dice.doubles_streak, 1)
            self.dice.roll() # streak 2
            self.assertEqual(self.dice.doubles_streak, 2)
            self.dice.roll() # streak 3
            self.assertEqual(self.dice.doubles_streak, 3)
        finally:
            random.randint = orig_randint

    def test_repr(self):
        self.assertIn("Dice", repr(self.dice))
        self.assertIn("streak=0", repr(self.dice))

if __name__ == "__main__":
    unittest.main()
