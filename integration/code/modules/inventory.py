# Inventory Module

VALID_ITEM_TYPES = ['cars', 'parts', 'tools']

def validate_item_type(item_type):
    return item_type in VALID_ITEM_TYPES

def format_inventory(inventory):
    output = "--- Inventory ---\n"
    output += f"Cash: ${inventory['cash']}\n"
    for item_type in VALID_ITEM_TYPES:
        items = inventory.get(item_type, [])
        output += f"{item_type.capitalize()}: {', '.join(items) if items else 'None'}\n"
    return output
