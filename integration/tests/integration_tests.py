import pytest
import os
import sys
from unittest.mock import patch

# Add the 'code' directory to sys.path so 'manager' and 'modules' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))

from manager import StreetRaceManager

@pytest.fixture
def manager():
    return StreetRaceManager()

# --- 1. Registration & Crew Management ---
def test_registration_valid(manager):
    """Test valid member registration."""
    assert manager.register_member("Dom", "driver") == 1
    assert manager.get_crew()[1]["name"] == "Dom"

def test_registration_invalid_role(manager):
    """Test registration with an unsupported role."""
    assert manager.register_member("Brian", "racer") is None

def test_registration_empty_name(manager):
    """Test registration with an empty name."""
    assert manager.register_member("", "driver") is None

def test_update_role_valid(manager):
    """Test updating a member's role to another valid role."""
    manager.register_member("Dom", "driver")
    assert manager.update_role(1, "mechanic") is True
    assert manager.get_crew()[1]["role"] == "mechanic"

def test_update_role_invalid_member(manager):
    """Test updating a role for a non-existent member."""
    assert manager.update_role(99, "driver") is False

def test_update_role_invalid_role(manager):
    """Test updating a role to an unsupported value."""
    manager.register_member("Dom", "driver")
    assert manager.update_role(1, "pilot") is False

def test_update_skill_valid(manager):
    """Test updating a member's skill level within valid bounds."""
    manager.register_member("Dom", "driver")
    assert manager.update_skill_level(1, 10) is True
    assert manager.get_crew()[1]["skill_level"] == 10

def test_update_skill_out_of_bounds(manager):
    """Test updating a skill level outside the 1-10 range."""
    manager.register_member("Dom", "driver")
    assert manager.update_skill_level(1, 11) is False
    assert manager.update_skill_level(1, 0) is False

# --- 2. Inventory Management ---
def test_add_inventory_car(manager):
    """Test adding a car to the inventory."""
    assert manager.add_inventory_item("cars", "Supra") is True
    assert "Supra" in manager.get_inventory()["cars"]

def test_add_inventory_parts(manager):
    """Test adding parts to the inventory."""
    assert manager.add_inventory_item("parts", "Turbo") is True
    assert "Turbo" in manager.get_inventory()["parts"]

def test_add_inventory_invalid_type(manager):
    """Test adding an item with an invalid category."""
    assert manager.add_inventory_item("fuel", "Nitro") is False

def test_car_damage_logic(manager):
    """Test that damaging a car correctly updates its status."""
    manager.add_inventory_item("cars", "Supra")
    assert manager.damage_car("Supra") is True
    assert manager.get_inventory()["cars"]["Supra"]["status"] == "Damaged"

def test_car_repair_logic(manager):
    """Test that repairing a car restores it to Healthy status."""
    manager.add_inventory_item("cars", "Supra")
    manager.damage_car("Supra")
    assert manager.repair_car("Supra") is True
    assert manager.get_inventory()["cars"]["Supra"]["status"] == "Healthy"

def test_damage_non_existent_car(manager):
    """Test damaging a car that isn't in the inventory."""
    assert manager.damage_car("Skyline") is False

# --- 3. Race Management ---
def test_create_race_valid(manager):
    """Test valid race creation with a driver and a car."""
    dom_id = manager.register_member("Dom", "driver")
    manager.add_inventory_item("cars", "Supra")
    assert manager.create_race("Race 1", dom_id, "Supra") is True

def test_create_race_non_driver(manager):
    """Test that non-drivers cannot be assigned to races."""
    mia_id = manager.register_member("Mia", "strategist")
    manager.add_inventory_item("cars", "Supra")
    assert manager.create_race("Race 1", mia_id, "Supra") is False

def test_create_race_non_existent_car(manager):
    """Test race creation with a non-existent car."""
    dom_id = manager.register_member("Dom", "driver")
    assert manager.create_race("Race 1", dom_id, "Skyline") is False

def test_record_result_prizes(manager):
    """Test that prize money is correctly awarded for 1st place."""
    dom_id = manager.register_member("Dom", "driver")
    manager.add_inventory_item("cars", "Supra")
    manager.create_race("R1", dom_id, "Supra")
    # Prize for 1st is 1000
    with patch('random.random', return_value=0.5): # Avoid car damage
        assert manager.record_race_result(1, 1) is True
    assert manager.get_inventory()["cash"] == 1000

def test_record_result_skill_up(manager):
    """Test that winning a race increases the driver's skill."""
    dom_id = manager.register_member("Dom", "driver")
    manager.add_inventory_item("cars", "Supra")
    manager.create_race("R1", dom_id, "Supra")
    with patch('random.random', return_value=0.5):
        manager.record_race_result(1, 1)
    assert manager.get_crew()[dom_id]["skill_level"] == 2

# --- 4. Reputation & Sponsorships ---
def test_sponsorship_tier_1_unlock(manager):
    """Test unlocking the Tier 1 sponsor (Local Garage) at 10 reputation."""
    dom_id = manager.register_member("Dom", "driver")
    manager.add_inventory_item("cars", "Supra")
    for i in range(1, 3): # 2 wins * 5 rep = 10 rep
        manager.create_race(f"R{i}", dom_id, "Supra")
        manager.record_race_result(i, 1)
    status = manager.get_reputation_status()
    assert status["reputation"] == 10
    assert status["sponsor"] == "Local Garage"

def test_sponsorship_tier_2_unlock(manager):
    """Test unlocking the Tier 2 sponsor (Speedhunters) at 30 reputation."""
    dom_id = manager.register_member("Dom", "driver")
    manager.add_inventory_item("cars", "Supra")
    for i in range(1, 7): # 6 wins * 5 rep = 30 rep
        manager.create_race(f"R{i}", dom_id, "Supra")
        manager.record_race_result(i, 1)
    assert manager.get_reputation_status()["sponsor"] == "Speedhunters"

def test_sponsorship_tier_3_unlock(manager):
    """Test unlocking the Tier 3 sponsor (Red Bull) at 60 reputation."""
    dom_id = manager.register_member("Dom", "driver")
    manager.add_inventory_item("cars", "Supra")
    for i in range(1, 13): # 12 wins * 5 rep = 60 rep
        manager.create_race(f"R{i}", dom_id, "Supra")
        manager.record_race_result(i, 1)
    assert manager.get_reputation_status()["sponsor"] == "Red Bull"

# --- 5. Mission Planning ---
def test_mission_delivery_reqs(manager):
    """Test delivery mission requirement (driver)."""
    manager.register_member("Dom", "driver")
    assert manager.assign_mission("Deliver Nitro", "delivery") is True

def test_mission_rescue_reqs(manager):
    """Test rescue mission requirements (driver + strategist)."""
    manager.register_member("Dom", "driver")
    manager.register_member("Mia", "strategist")
    assert manager.assign_mission("Rescue Brian", "rescue") is True

def test_mission_heist_reqs(manager):
    """Test heist mission requirements (driver + mechanic + strategist)."""
    manager.register_member("Dom", "driver")
    manager.register_member("Tej", "mechanic")
    manager.register_member("Mia", "strategist")
    assert manager.assign_mission("Bank Heist", "heist") is True

def test_mission_repair_auto_fix(manager):
    """Test that a repair mission automatically fixes a damaged car."""
    manager.register_member("Tej", "mechanic")
    manager.add_inventory_item("cars", "Supra")
    manager.damage_car("Supra")
    assert manager.assign_mission("Fix Supra", "repair") is True
    assert manager.get_inventory()["cars"]["Supra"]["status"] == "Healthy"

def test_mission_missing_mechanic(manager):
    """Test that a mission fails if a required role (mechanic) is missing."""
    manager.register_member("Dom", "driver")
    assert manager.assign_mission("Fix Car", "repair") is False

# --- 6. Tuning & Upgrades ---
def test_upgrade_tier_1_success(manager):
    """Test successful Tier 1 upgrade with all resources."""
    manager.register_member("Tej", "mechanic")
    manager.add_inventory_item("cars", "Supra")
    manager.update_cash(1000)
    manager.add_inventory_item("parts", "Spoiler")
    assert manager.upgrade_car("Supra", 1) is True
    assert manager.get_inventory()["cars"]["Supra"]["tier"] == 1
    assert manager.get_inventory()["cars"]["Supra"]["performance"] == 1.1

def test_upgrade_tier_3_success(manager):
    """Test successful Tier 3 upgrade with all resources."""
    manager.register_member("Tej", "mechanic")
    manager.add_inventory_item("cars", "Supra")
    manager.update_cash(6000)
    for _ in range(3): manager.add_inventory_item("parts", "P")
    assert manager.upgrade_car("Supra", 3) is True
    assert manager.get_inventory()["cars"]["Supra"]["tier"] == 3

def test_upgrade_insufficient_cash(manager):
    """Test that car upgrade fails due to lack of cash."""
    manager.register_member("Tej", "mechanic")
    manager.add_inventory_item("cars", "Supra")
    manager.add_inventory_item("parts", "P1")
    assert manager.upgrade_car("Supra", 1) is False

def test_upgrade_missing_mechanic(manager):
    """Test that car upgrade fails if no mechanic is in the crew."""
    manager.add_inventory_item("cars", "Supra")
    manager.update_cash(1000)
    manager.add_inventory_item("parts", "P1")
    assert manager.upgrade_car("Supra", 1) is False

