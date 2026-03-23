from modules.registration import Registration
from modules.crew import CrewManagement
from modules.inventory import Inventory

class StreetRaceManager:
    def __init__(self):
        self.registration = Registration()
        self.crew = CrewManagement(self.registration)
        self.inventory = Inventory()
        self.race_management = None
        self.results = None
        self.mission_planning = None
        self.tuning = None
        self.reputation = None

    def run(self):
        print("StreetRace Manager Initialized with Registration, Crew, and Inventory Modules.")
        # Placeholder for main loop or logic
