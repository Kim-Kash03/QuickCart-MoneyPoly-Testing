class Registration:
    def __init__(self):
        self.crew_members = {}

    def register_crew_member(self, name, role):
        if name in self.crew_members:
            return False, f"Crew member '{name}' is already registered."
        self.crew_members[name] = {"role": role, "name": name}
        return True, f"Crew member '{name}' registered as '{role}'."

    def get_crew_member(self, name):
        return self.crew_members.get(name)

    def list_all_members(self):
        return list(self.crew_members.keys())
