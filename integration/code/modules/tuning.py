UPGRADE_TIERS = {
    1: {"cost": 500, "parts_needed": 1, "boost": 0.1},
    2: {"cost": 1500, "parts_needed": 2, "boost": 0.2},
    3: {"cost": 5000, "parts_needed": 3, "boost": 0.5}
}

def validate_tuning_resources(manager, car_name, tier):
    if tier not in UPGRADE_TIERS:
        return False, "Invalid upgrade tier."
    
    config = UPGRADE_TIERS[tier]
    inventory = manager.get_inventory()
    
    # Check cash
    if inventory["cash"] < config["cost"]:
        return False, f"Insufficient cash. Need ${config['cost']}."
    
    # Check parts
    if len(inventory["parts"]) < config["parts_needed"]:
        return False, f"Insufficient spare parts. Need {config['parts_needed']}."
    
    # Check for mechanic
    crew = manager.get_crew()
    has_mechanic = any(m["role"] == "mechanic" for m in crew.values())
    if not has_mechanic:
        return False, "A mechanic is required for tuning."
    
    return True, "Resources available."

def apply_tuning(car_data, tier):
    boost = UPGRADE_TIERS[tier]["boost"]
    car_data["performance"] = car_data.get("performance", 1.0) + boost
    car_data["tier"] = tier
    return car_data
