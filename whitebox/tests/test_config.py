import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

import moneypoly.config as config

class TestConfig(unittest.TestCase):
    def test_starting_balance(self):
        self.assertEqual(config.STARTING_BALANCE, 1500)

    def test_go_salary(self):
        self.assertEqual(config.GO_SALARY, 200)

    def test_board_size(self):
        self.assertEqual(config.BOARD_SIZE, 40)

    def test_jail_position(self):
        self.assertEqual(config.JAIL_POSITION, 10)

    def test_go_to_jail_position(self):
        self.assertEqual(config.GO_TO_JAIL_POSITION, 30)

    def test_free_parking_position(self):
        self.assertEqual(config.FREE_PARKING_POSITION, 20)

    def test_income_tax_position(self):
        self.assertEqual(config.INCOME_TAX_POSITION, 4)

    def test_luxury_tax_position(self):
        self.assertEqual(config.LUXURY_TAX_POSITION, 38)

    def test_income_tax_amount(self):
        self.assertEqual(config.INCOME_TAX_AMOUNT, 200)

    def test_luxury_tax_amount(self):
        self.assertEqual(config.LUXURY_TAX_AMOUNT, 75)

    def test_jail_fine(self):
        self.assertEqual(config.JAIL_FINE, 50)

    def test_max_turns(self):
        self.assertEqual(config.MAX_TURNS, 100)

    def test_auction_min_increment(self):
        self.assertEqual(config.AUCTION_MIN_INCREMENT, 10)

    def test_bank_starting_funds(self):
        self.assertEqual(config.BANK_STARTING_FUNDS, 20580)

if __name__ == "__main__":
    unittest.main()
