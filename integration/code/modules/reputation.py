SPONSORSHIPS = {
    1: {"name": "Local Garage", "rep_needed": 10, "cash_bonus": 500, "parts_bonus": 1},
    2: {"name": "Speedhunters", "rep_needed": 30, "cash_bonus": 2000, "parts_bonus": 3},
    3: {"name": "Red Bull", "rep_needed": 60, "cash_bonus": 5000, "parts_bonus": 5}
}

def calculate_rep_gain(position):
    # Base reputation gain based on race position
    gains = {1: 5, 2: 2, 3: 1}
    return gains.get(position, 0)

def check_for_new_sponsor(current_rep, previous_rep):
    # Check if a new sponsorship threshold was crossed
    for level, data in SPONSORSHIPS.items():
        if current_rep >= data["rep_needed"] > previous_rep:
            return level, data
    return None, None
