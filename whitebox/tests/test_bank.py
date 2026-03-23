import unittest
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

from moneypoly.bank import Bank
from moneypoly.player import Player

class TestBank(unittest.TestCase):
    def setUp(self):
        self.bank = Bank()
        self.player = Player("Test")

    def test_initial_balance(self):
        # Branch: initial state
        self.assertEqual(self.bank.get_balance(), 20580)

    def test_collect_positive(self):
        # Branch: collect normal
        self.bank.collect(500)
        self.assertEqual(self.bank.get_balance(), 20580 + 500)

    def test_collect_negative_and_zero(self):
        # Edge case: negative or zero collect
        # BUG: collect does not raise ValueError for negative numbers.
        # Intended behavior: negative amounts should be invalid or ignored.
        old_balance = self.bank.get_balance()
        self.bank.collect(-10)
        # Should NOT subtract from balance
        self.assertEqual(self.bank.get_balance(), old_balance)
        self.bank.collect(0)
        self.assertEqual(self.bank.get_balance(), old_balance)

    def test_pay_out_normal(self):
        # Branch/Edge case: exact and less than funds
        paid = self.bank.pay_out(580)
        self.assertEqual(paid, 580)
        self.assertEqual(self.bank.get_balance(), 20000)

    def test_pay_out_negative_or_zero(self):
        # Edge case: pay out 0 or negative
        self.assertEqual(self.bank.pay_out(0), 0)
        self.assertEqual(self.bank.get_balance(), 20580)
        self.assertEqual(self.bank.pay_out(-100), 0) # code returns 0 when amount <= 0

    def test_pay_out_insufficient_funds(self):
        # Edge case: amount > funds
        with self.assertRaises(ValueError):
            self.bank.pay_out(25000)

    def test_give_loan_normal(self):
        # Branch: valid loan
        self.bank.give_loan(self.player, 500)
        self.assertEqual(self.player.balance, 2000)
        # BUG: Bank funds don't decrease on give_loan. Intended behavior: bank balance should decrease.
        self.assertEqual(self.bank.get_balance(), 20080) # 20580 - 500

    def test_give_loan_negative_or_zero(self):
        # Edge case: negative loan
        self.bank.give_loan(self.player, -200)
        self.assertEqual(self.player.balance, 1500)

    def test_give_loan_insufficient_bank_funds(self):
        # Edge case: loan > bank funds
        # BUG: give_loan does not check bank funds or raise an error
        self.bank.give_loan(self.player, 50000)

    def test_loan_metrics(self):
        # Branch/Variable state: multiple loans
        self.bank.give_loan(self.player, 500)
        p2 = Player("Bob")
        self.bank.give_loan(p2, 1000)
        self.assertEqual(self.bank.loan_count(), 2)
        self.assertEqual(self.bank.total_loans_issued(), 1500)

    def test_summary(self):
        # Branch: coverage for summary printing
        self.bank.collect(100)
        self.bank.give_loan(self.player, 50)
        # Should not raise error
        self.bank.summary()

    def test_repr(self):
        # Branch: coverage for __repr__
        self.assertIn("Bank", repr(self.bank))
        self.assertIn("funds=20580", repr(self.bank))

if __name__ == "__main__":
    unittest.main()
