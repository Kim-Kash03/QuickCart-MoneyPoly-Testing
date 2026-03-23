class CrewManagement:
    def __init__(self, registration_module):
        self.registration = registration_module
        self.crew_data = {}

    def assign_role(self, name, role):
        member = self.registration.get_crew_member(name)
        if not member:
            return False, f"Cannot assign role. Crew member '{name}' is not registered."
        
        self.crew_data.setdefault(name, {"skill_level": 1})
        member["role"] = role
        return True, f"Role '{role}' assigned to '{name}'."

    def set_skill_level(self, name, level):
        if name not in self.crew_data:
            return False, f"Crew member '{name}' not found in crew data."
        self.crew_data[name]["skill_level"] = level
        return True, f"Skill level for '{name}' set to {level}."

    def get_skill_level(self, name):
        return self.crew_data.get(name, {}).get("skill_level", 0)

    def get_member_info(self, name):
        member = self.registration.get_crew_member(name)
        if member:
            member.update(self.crew_data.get(name, {}))
            return member
        return None
