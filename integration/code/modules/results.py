class Results:
    def __init__(self, race_module, crew_module, inventory_module):
        self.race_management = race_module
        self.crew = crew_module
        self.inventory = inventory_module
        self.outcomes = []

    def record_outcome(self, race_name, rankings, prize_money, damages=None):
        """
        rankings: list of driver names in order of finish
        damages: dict of {car_name: damage_amount}
        """
        race = self.race_management.get_race(race_name)
        if not race:
            return False, f"Race '{race_name}' not found."
        
        # Update prize money in inventory
        self.inventory.update_cash(prize_money)
        
        # Update skill levels of drivers based on performance (stub logic)
        for rank, driver in enumerate(rankings):
            current_skill = self.crew.get_skill_level(driver)
            bonus = 0.5 if rank == 0 else 0.1
            self.crew.set_skill_level(driver, current_skill + bonus)
        
        # Handle car damage
        if damages:
            for car_name, damage in damages.items():
                car = self.inventory.get_car(car_name)
                if car:
                    car["condition"] = max(0, car["condition"] - damage)
        
        self.outcomes.append({
            "race": race_name,
            "rankings": rankings,
            "prize": prize_money
        })
        race["status"] = "completed"
        return True, f"Outcome for '{race_name}' recorded. Prize: {prize_money}"

    def get_outcomes(self):
        return self.outcomes
