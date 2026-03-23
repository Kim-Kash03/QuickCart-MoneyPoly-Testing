class RaceManagement:
    def __init__(self, crew_module, inventory_module):
        self.crew = crew_module
        self.inventory = inventory_module
        self.races = {}

    def create_race(self, name, distance, difficulty):
        if name in self.races:
            return False, f"Race '{name}' already exists."
        self.races[name] = {
            "distance": distance,
            "difficulty": difficulty,
            "participants": [],
            "status": "planned"
        }
        return True, f"Race '{name}' created."

    def select_participant(self, race_name, driver_name, car_name):
        race = self.races.get(race_name)
        if not race:
            return False, f"Race '{race_name}' not found."
        
        # Check driver
        member_info = self.crew.get_member_info(driver_name)
        if not member_info or member_info.get("role") != "driver":
            return False, f"Member '{driver_name}' is not a registered driver."
        
        # Check car
        car = self.inventory.get_car(car_name)
        if not car:
            return False, f"Car '{car_name}' not found in inventory."
        
        race["participants"].append({"driver": driver_name, "car": car_name})
        return True, f"Added {driver_name} with {car_name} to {race_name}."

    def get_race(self, name):
        return self.races.get(name)
