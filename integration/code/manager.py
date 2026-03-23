from modules.registration import Registration
from modules.crew import CrewManagement
from modules.inventory import Inventory
from modules.race import RaceManagement
from modules.results import Results
from modules.mission import MissionPlanning

class StreetRaceManager:
    def __init__(self):
        self.registration = Registration()
        self.crew = CrewManagement(self.registration)
        self.inventory = Inventory()
        self.race_management = RaceManagement(self.crew, self.inventory)
        self.results = Results(self.race_management, self.crew, self.inventory)
        self.mission_planning = MissionPlanning(self.crew, self.inventory)
        self.tuning = None
        self.reputation = None

    def run(self):
        print("StreetRace Manager Initialized with All Core Modules.")
        # Placeholder for main loop or logic
