PRIZES = {
    1: 1000, # 1st place
    2: 500,  # 2nd place
    3: 200   # 3rd place
}

def calculate_prize(position):
    return PRIZES.get(position, 0)

def format_result(result):
    return f"Race: {result['name']} | Driver: {result['driver_name']} | Position: {result['position']} | Prize: ${result['prize']}"
