MISSION_TYPES = {
    "delivery": ["driver"],
    "rescue": ["driver", "strategist"],
    "heist": ["driver", "mechanic", "strategist"],
    "repair": ["mechanic"]
}

def get_required_roles(mission_type):
    return MISSION_TYPES.get(mission_type, [])

def validate_mission_requirements(manager, mission_type):
    required_roles = get_required_roles(mission_type)
    crew = manager.get_crew()
    
    available_roles = [member["role"] for member in crew.values()]
    
    for role in required_roles:
        if role not in available_roles:
            return False, f"Missing required role: {role}"
    return True, "All requirements met."
