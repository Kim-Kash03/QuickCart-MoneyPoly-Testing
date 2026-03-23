# Race Management Module

def validate_race_participants(manager, driver_id, car_name):
    # Check if driver exists
    crew = manager.get_crew()
    if driver_id not in crew:
        return False, f"Driver ID {driver_id} not found."
    
    # Check if member is a driver
    if crew[driver_id]['role'] != 'driver':
        return False, f"Member {crew[driver_id]['name']} is not a driver."
    
    # Check if car exists in inventory
    inventory = manager.get_inventory()
    if car_name not in inventory['cars']:
        return False, f"Car {car_name} not found in inventory."
    
    return True, "Valid participants."

def format_race(race):
    return f"Race: {race['name']} | Driver: {race['driver_name']} | Car: {race['car_name']} | Status: {race['status']}"
