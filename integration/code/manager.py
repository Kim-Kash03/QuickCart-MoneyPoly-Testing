from modules.registration import Registration
from modules.crew import CrewManagement

class StreetRaceManager:
    def __init__(self):
        self.registration = Registration()
        self.crew = CrewManagement(self.registration)
        self.inventory = None
        self.race_management = None
        self.results = None
        self.mission_planning = None
        self.tuning = None
        self.reputation = None

    def run(self):
        print("StreetRace Manager Initialized with Registration and Crew Modules.")
        # Placeholder for main loop or logic
