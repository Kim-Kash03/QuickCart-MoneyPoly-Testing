from modules.registration import validate_registration
from modules.crew import validate_role, validate_skill_level

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

    def get_crew(self):
        return self.crew
