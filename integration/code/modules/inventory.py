class Inventory:
    def __init__(self, initial_cash=10000):
        self.cars = {}  # {name: {"condition": 100, "performance": 1.0}}
        self.parts = {} # {name: quantity}
        self.tools = []
        self.cash = initial_cash

    def add_car(self, name, condition=100, performance=1.0):
        if name in self.cars:
            return False, f"Car '{name}' already exists in inventory."
        self.cars[name] = {"condition": condition, "performance": performance}
        return True, f"Car '{name}' added to inventory."

    def add_part(self, name, quantity):
        self.parts[name] = self.parts.get(name, 0) + quantity
        return True, f"Added {quantity} of '{name}' to parts."

    def use_part(self, name, quantity):
        if self.parts.get(name, 0) < quantity:
            return False, f"Not enough '{name}' in inventory."
        self.parts[name] -= quantity
        return True, f"Used {quantity} of '{name}'."

    def update_cash(self, amount):
        self.cash += amount
        return True, f"Cash balance updated. New balance: {self.cash}"

    def get_car(self, name):
        return self.cars.get(name)

    def get_status(self):
        return {
            "cash": self.cash,
            "cars": self.cars,
            "parts": self.parts,
            "tools": self.tools
        }
