def validate_registration(name, role):
    valid_roles = ['driver', 'mechanic', 'strategist']
    if not name or role not in valid_roles:
        return False
    return True
