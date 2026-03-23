# Crew Management Module

def validate_role(role):
    valid_roles = ['driver', 'mechanic', 'strategist']
    return role in valid_roles

def validate_skill_level(level):
    try:
        level = int(level)
        return 1 <= level <= 10
    except ValueError:
        return False
