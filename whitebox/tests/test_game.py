import unittest
from unittest.mock import patch, MagicMock
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'code', 'moneypoly'))

from moneypoly.game import Game
from moneypoly.player import Player

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(["P1", "P2"])

    def test_init_and_advance(self):
        self.assertEqual(self.game.current_player().name, "P1")
        self.game.advance_turn()
        self.assertEqual(self.game.current_player().name, "P2")
        self.game.advance_turn()
        self.assertEqual(self.game.current_player().name, "P1")
        self.assertEqual(self.game.turn_number, 2)

    def test_find_winner_logical_bug(self):
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        p1.balance = 2000
        p2.balance = 1000
        winner = self.game.find_winner()
        # BUG: it incorrectly picks p2 using min()
        self.assertEqual(winner.name, "P1")

    def test_check_bankruptcy(self):
        p1 = self.game.players[0]
        p1.balance = -10
        self.game._check_bankruptcy(p1)
        self.assertTrue(p1.is_eliminated)
        self.assertNotIn(p1, self.game.players)

    @patch('builtins.input', return_value='s')
    def test_handle_property_tile_skip(self, mock_input):
        p1 = self.game.current_player()
        prop = self.game.board.get_property_at(1)
        self.game._handle_property_tile(p1, prop)
        self.assertIsNone(prop.owner)

    @patch('builtins.input', return_value='b')
    def test_handle_property_tile_buy_success(self, mock_input):
        p1 = self.game.current_player()
        prop = self.game.board.get_property_at(1)
        self.game._handle_property_tile(p1, prop)
        self.assertEqual(prop.owner, p1)

    @patch('builtins.input', return_value='b')
    def test_handle_property_tile_buy_fail_insufficient_funds(self, mock_input):
        p1 = self.game.current_player()
        p1.balance = 10
        prop = self.game.board.get_property_at(39) # Boardwalk = 400
        self.game._handle_property_tile(p1, prop)
        self.assertIsNone(prop.owner)

    @patch('moneypoly.ui.safe_int_input', side_effect=[100, 0])
    def test_auction_property_success(self, mock_input):
        p1 = self.game.current_player()
        prop = self.game.board.get_property_at(1)
        self.game.auction_property(prop)
        self.assertEqual(prop.owner, p1)
        self.assertEqual(p1.balance, 1400) # 1500 - 100

    def test_pay_rent(self):
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        prop = self.game.board.get_property_at(1)
        prop.owner = p2
        self.game.pay_rent(p1, prop)
        # BUG: Med Ave rent is 2, but all_owned_by logic error doubles it to 4. Also, the owner never receives it! (sink)
        # Intended: rent 2, p2 balance 1502
        self.assertEqual(p1.balance, 1498)
        self.assertEqual(p2.balance, 1502)

    def test_trade_success(self):
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        prop = self.game.board.get_property_at(1)
        prop.owner = p1
        p1.add_property(prop)
        
        success = self.game.trade(p1, p2, prop, 100)
        self.assertTrue(success)
        self.assertEqual(prop.owner, p2)
        # BUG: The seller P1 never receives the cash. Intended: balance should be 1600.
        self.assertEqual(p1.balance, 1600)
        self.assertEqual(p2.balance, 1400)
        
    def test_trade_fail_not_owned(self):
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        prop = self.game.board.get_property_at(1) # Unowned
        success = self.game.trade(p1, p2, prop, 100)
        self.assertFalse(success)
        
    def test_trade_fail_no_money(self):
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        p2.balance = 50
        prop = self.game.board.get_property_at(1)
        prop.owner = p1
        success = self.game.trade(p1, p2, prop, 100)
        self.assertFalse(success)

    def test_mortgage_and_unmortgage(self):
        p1 = self.game.players[0]
        prop = self.game.board.get_property_at(1)
        prop.owner = p1
        p1.add_property(prop)
        
        # Test mortgage success
        self.assertTrue(self.game.mortgage_property(p1, prop))
        self.assertTrue(prop.is_mortgaged)
        self.assertEqual(p1.balance, 1530) # 1500 + 30 (mortgage val for Med Ave)
        
        # Test unmortgage success
        self.assertTrue(self.game.unmortgage_property(p1, prop))
        self.assertFalse(prop.is_mortgaged)
        self.assertEqual(p1.balance, 1497) # 1530 - int(30 * 1.1) -> 1530 - 33 = 1497

    def test_mortgage_unowned(self):
        p1 = self.game.players[0]
        prop = self.game.board.get_property_at(1)
        self.assertFalse(self.game.mortgage_property(p1, prop))

    @patch('builtins.input', return_value='s')
    @patch('moneypoly.ui.confirm', return_value=True)
    def test_handle_jail_turn_pay_fine(self, mock_confirm, mock_input):
        p1 = self.game.players[0]
        p1.go_to_jail()
        with patch.object(self.game.dice, 'roll', return_value=1):
            self.game._handle_jail_turn(p1)
        self.assertFalse(p1.in_jail)
        # BUG: player is never actually charged money for the fine, it stays at 1500. Intended: 1450.
        self.assertEqual(p1.balance, 1450)

    @patch('builtins.input', return_value='s')
    @patch('moneypoly.ui.confirm', return_value=False)
    def test_handle_jail_turn_wait(self, mock_confirm, mock_input):
        p1 = self.game.players[0]
        p1.go_to_jail()
        with patch.object(self.game.dice, 'roll', return_value=1):
            self.game._handle_jail_turn(p1)
        self.assertTrue(p1.in_jail)
        self.assertEqual(p1.jail_turns, 1)

    def test_move_and_resolve_income_tax(self):
        p1 = self.game.players[0]
        self.game._move_and_resolve(p1, 4) # position 4 is income tax
        self.assertEqual(p1.balance, 1300) # 1500 - 200

    def test_tile_luxury_tax(self):
        # Branch/Variable state: landing on luxury tax
        p1 = self.game.players[0]
        self.game._tile_luxury_tax(p1, 38)
        self.assertEqual(p1.balance, 1425) # 1500 - 75
        # Bank collects 75
        self.assertEqual(self.game.bank.get_balance(), 20580 + 75)

    def test_tile_go_to_jail(self):
        # Branch/Variable state: landing on go to jail
        p1 = self.game.players[0]
        self.game._tile_go_to_jail(p1, 30)
        self.assertEqual(p1.position, 10)
        self.assertTrue(p1.in_jail)

    def test_card_collect_pay(self):
        # Branch: card action collect/pay
        p1 = self.game.players[0]
        self.game._card_collect(p1, 100)
        self.assertEqual(p1.balance, 1600)
        self.game._card_pay(p1, 50)
        self.assertEqual(p1.balance, 1550)

    def test_card_move_to_with_go_salary_bug(self):
        # Branch: card action move_to
        p1 = self.game.players[0]
        p1.position = 35
        # Move to position 5 (passed Go)
        self.game._card_move_to(p1, 5)
        self.assertEqual(p1.position, 5)
        # Verify Go salary added
        self.assertEqual(p1.balance, 1700)

    def test_card_birthday_and_collect_all(self):
        # Branch: multi-player card actions
        p1 = self.game.players[0]
        p2 = self.game.players[1]
        self.game._card_birthday(p1, 50)
        self.assertEqual(p1.balance, 1550)
        self.assertEqual(p2.balance, 1450)
        self.game._card_collect_from_all(p1, 50)
        self.assertEqual(p1.balance, 1600)
        self.assertEqual(p2.balance, 1400)

    def test_card_jail_handling(self):
        # Branch: card action jail/jail_free
        p1 = self.game.players[0]
        self.game._card_jail_free(p1, 0)
        self.assertEqual(p1.get_out_of_jail_cards, 1)
        self.game._card_jail(p1, 0)
        self.assertTrue(p1.in_jail)

    def test_buy_property_fail(self):
        # Branch/Edge case: cannot afford
        p1 = self.game.players[0]
        p1.balance = 50
        prop = self.game.board.get_property_at(1) # price 60
        self.assertFalse(self.game.buy_property(p1, prop))
        self.assertEqual(p1.balance, 50)
        self.assertIsNone(prop.owner)

    def test_buy_property_success(self):
        # Branch: normal purchase
        p1 = self.game.players[0]
        prop = self.game.board.get_property_at(1)
        self.assertTrue(self.game.buy_property(p1, prop))
        self.assertEqual(p1.balance, 1440)
        self.assertEqual(prop.owner, p1)
        self.assertEqual(self.game.bank.get_balance(), 20580 + 60)

    def test_check_bankruptcy_property_release(self):
        # Branch: property cleanup on bankruptcy
        p1 = self.game.players[0]
        prop = self.game.board.get_property_at(1)
        self.game.buy_property(p1, prop)
        p1.balance = -1
        self.game._check_bankruptcy(p1)
        self.assertIsNone(prop.owner)
        self.assertFalse(prop.is_mortgaged)
        self.assertEqual(len(p1.properties), 0)

    def test_find_winner_edge_cases(self):
        # Edge case: 1 player, 0 players
        winner = self.game.find_winner()
        self.assertIsNotNone(winner)
        self.game.players = []
        self.assertIsNone(self.game.find_winner())

    def test_advance_turn_wrap_multi(self):
        # Branch: wrap with 3+ players
        game = Game(["P1", "P2", "P3"])
        self.assertEqual(game.current_index, 0)
        game.advance_turn()
        self.assertEqual(game.current_index, 1)
        game.advance_turn()
        self.assertEqual(game.current_index, 2)
        game.advance_turn()
        self.assertEqual(game.current_index, 0)

    def test_game_decks_init(self):
        # Branch: initial state
        self.assertEqual(len(self.game.decks.chance.cards), 12)
        self.assertEqual(len(self.game.decks.community.cards), 12)

    def test_game_state_properties(self):
        # Branch: accessibility/setability (simple sanity checks)
        self.assertEqual(self.game.current_index, 0)
        self.assertEqual(self.game.turn_number, 0)
        self.assertTrue(self.game.running)
        self.game.current_index = 1
        self.game.turn_number = 5
        self.game.running = False
        self.assertEqual(self.game.current_index, 1)
        self.assertEqual(self.game.turn_number, 5)
        self.assertFalse(self.game.running)

if __name__ == "__main__":
    unittest.main()
