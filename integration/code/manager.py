from modules.registration import validate_registration
from modules.crew import validate_role, validate_skill_level
from modules.inventory import validate_item_type
from modules.race import validate_race_participants

class StreetRaceManager:
    def __init__(self):
        self.crew = {} # member_id: {name, role, skill_level}
        self.inventory = {
            "cars": [],
            "parts": [],
            "tools": [],
            "cash": 0
        }
        self.races = []
        self.missions = []

    def register_member(self, name, role):
        if not validate_registration(name, role):
            print(f"Error: Invalid registration for {name} with role {role}.")
            return None
        
        member_id = len(self.crew) + 1
        self.crew[member_id] = {
            "name": name,
            "role": role,
            "skill_level": 1 # Default 
        }
        return member_id

    def update_role(self, member_id, new_role):
        if member_id not in self.crew:
            print(f"Error: Member ID {member_id} not found.")
            return False
        if not validate_role(new_role):
            print(f"Error: Invalid role {new_role}.")
            return False
        self.crew[member_id]["role"] = new_role
        return True

    def update_skill_level(self, member_id, new_level):
        if member_id not in self.crew:
            print(f"Error: Member ID {member_id} not found.")
            return False
        if not validate_skill_level(new_level):
            print(f"Error: Invalid skill level {new_level}. Must be between 1 and 10.")
            return False
        self.crew[member_id]["skill_level"] = int(new_level)
        return True

    def add_inventory_item(self, item_type, item_name):
        if not validate_item_type(item_type):
            print(f"Error: Invalid item type {item_type}.")
            return False
        self.inventory[item_type].append(item_name)
        return True

    def update_cash(self, amount):
        self.inventory["cash"] += amount
        return True

    def get_inventory(self):
        return self.inventory

    def create_race(self, race_name, driver_id, car_name):
        valid, message = validate_race_participants(self, driver_id, car_name)
        if not valid:
            print(f"Error: {message}")
            return False
        
        race = {
            "id": len(self.races) + 1,
            "name": race_name,
            "driver_id": driver_id,
            "driver_name": self.crew[driver_id]["name"],
            "car_name": car_name,
            "status": "Scheduled"
        }
        self.races.append(race)
        return True

    def get_races(self):
        return self.races

    def get_crew(self):
        return self.crew
