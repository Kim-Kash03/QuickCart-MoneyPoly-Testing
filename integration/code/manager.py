import os
from modules.registration import validate_registration

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

    def get_crew(self):
        return self.crew
