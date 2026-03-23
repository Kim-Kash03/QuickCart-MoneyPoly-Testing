import pytest
import os
import sys

# Add the 'code' directory to sys.path so 'manager' and 'modules' can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../code')))

from manager import StreetRaceManager

@pytest.fixture
def manager():
    return StreetRaceManager()

def test_full_integration_flow(manager):
    # 1. Registration & Crew Management
    dom_id = manager.register_member("Dom", "driver")
    mia_id = manager.register_member("Mia", "strategist")
    tej_id = manager.register_member("Tej", "mechanic")
    
    assert dom_id == 1
    assert manager.get_crew()[1]["role"] == "driver"
    
    # 2. Inventory
    manager.add_inventory_item("cars", "Supra")
    manager.add_inventory_item("parts", "Turbo")
    manager.add_inventory_item("parts", "Nitrous")
    
    inventory = manager.get_inventory()
    assert "Supra" in inventory["cars"]
    assert inventory["cars"]["Supra"]["status"] == "Healthy"
    assert len(inventory["parts"]) == 2
    
    # 3. Race Management
    # Ensure non-drivers cannot race
    assert manager.create_race("Race 1", mia_id, "Supra") == False
    # Ensure drivers can race
    assert manager.create_race("Race 1", dom_id, "Supra") == True
    
    races = manager.get_races()
    assert len(races) == 1
    assert races[0]["status"] == "Scheduled"
    
    # 4. Results & Reputation
    # Dom wins 1st place!
    assert manager.record_race_result(1, 1) == True
    
    # Check Cash Update ($1000 for 1st)
    assert manager.get_inventory()["cash"] == 1000
    
    # Check Skill Update
    assert manager.get_crew()[1]["skill_level"] == 2
    
    # Check Reputation (5 pts for 1st)
    rep_status = manager.get_reputation_status()
    assert rep_status["reputation"] == 5
    
    # Do another race to trigger sponsorship (needs 10 rep for Local Garage)
    manager.create_race("Race 2", dom_id, "Supra")
    manager.record_race_result(2, 1)
    
    # Reputation should be 10 now, unlocking Local Garage
    rep_status = manager.get_reputation_status()
    assert rep_status["reputation"] == 10
    assert rep_status["sponsor"] == "Local Garage"
    
    # Cash should be: 1000 (Race 1) + 1000 (Race 2) + 500 (Sponsor Bonus) = 2500
    assert manager.get_inventory()["cash"] == 2500
    
    # Parts should be: 2 (Initial) + 1 (Sponsor Bonus) = 3
    assert len(manager.get_inventory()["parts"]) == 3
    
    # 5. Tuning & Upgrades
    # Tier 2 costs $1500 and 2 parts
    assert manager.upgrade_car("Supra", 2) == True
    
    # Verify resources deducted (2500 - 1500 = 1000 cash, 3 - 2 = 1 part left)
    inventory = manager.get_inventory()
    assert inventory["cash"] == 1000
    assert len(inventory["parts"]) == 1
    assert inventory["cars"]["Supra"]["tier"] == 2
    assert inventory["cars"]["Supra"]["performance"] == 1.2
    
    # 6. Mission Planning
    # Damage the car manually to test repair mission
    manager.damage_car("Supra")
    assert inventory["cars"]["Supra"]["status"] == "Damaged"
    
    # Try a repair mission (requires mechanic, which Tej is)
    assert manager.assign_mission("Fix It", "repair") == True
    
    # Verify car is healthy again
    assert inventory["cars"]["Supra"]["status"] == "Healthy"
    
    # Try a heist mission (requires driver, mechanic, strategist)
    assert manager.assign_mission("The Big Score", "heist") == True
    
    assert len(manager.get_missions()) == 2
