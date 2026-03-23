VALID_ITEM_TYPES = ['cars', 'parts', 'tools']

def validate_item_type(item_type):
    return item_type in VALID_ITEM_TYPES

def format_inventory(inventory):
    output = "--- Inventory ---\n"
    output += f"Cash: ${inventory['cash']}\n"
    
    # Cars
    cars = inventory.get('cars', {})
    output += "Cars: "
    if not cars:
        output += "None\n"
    else:
        car_list = []
        for name, data in cars.items():
            status = data["status"]
            perf = data.get("performance", 1.0)
            tier = data.get("tier", 0)
            car_list.append(f"{name} [{status}] (Perf: {perf:.1f}, Tier: {tier})")
        output += ", ".join(car_list) + "\n"
    
    # Other items
    for item_type in ['parts', 'tools']:
        items = inventory.get(item_type, [])
        output += f"{item_type.capitalize()}: {', '.join(items) if items else 'None'}\n"
    
    return output
