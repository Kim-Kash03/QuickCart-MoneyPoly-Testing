import sys
from manager import StreetRaceManager
from modules.inventory import format_inventory
from modules.race import format_race
from modules.results import format_result

def main():
    manager = StreetRaceManager()
    print("=== StreetRace Manager ===")
    
    while True:
        print("\nOptions:")
        print("1. Register Crew Member")
        print("2. View Crew")
        print("3. Update Member Role")
        print("4. Update Member Skill Level")
        print("5. View Inventory")
        print("6. Add Item to Inventory")
        print("7. Create Race")
        print("8. View Scheduled Races")
        print("9. Record Race Result")
        print("10. View Race Results")
        print("11. Assign Mission")
        print("12. View Missions")
        print("13. Upgrade/Tune Car")
        print("14. View Team Reputation")
        print("15. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            name = input("Enter member name: ")
            role = input("Enter role (driver, mechanic, strategist): ")
            member_id = manager.register_member(name, role)
            if member_id:
                print(f"Member registered with ID: {member_id}")
        
        elif choice == '2':
            crew = manager.get_crew()
            if not crew:
                print("No crew members registered.")
            else:
                for mid, data in crew.items():
                    print(f"ID: {mid} | Name: {data['name']} | Role: {data['role']} | Skill: {data['skill_level']}")
        
        elif choice == '3':
            try:
                mid = int(input("Enter member ID: "))
                new_role = input("Enter new role: ")
                if manager.update_role(mid, new_role):
                    print("Role updated successfully.")
            except ValueError:
                print("Invalid input. Member ID must be an integer.")

        elif choice == '4':
            try:
                mid = int(input("Enter member ID: "))
                new_level = input("Enter new skill level (1-10): ")
                if manager.update_skill_level(mid, new_level):
                    print("Skill level updated successfully.")
            except ValueError:
                print("Invalid input. Member ID must be an integer.")

        elif choice == '5':
            print(format_inventory(manager.get_inventory()))

        elif choice == '6':
            item_type = input("Enter item type (cars, parts, tools): ")
            item_name = input("Enter item name/model: ")
            if manager.add_inventory_item(item_type, item_name):
                print(f"{item_name} added to {item_type}.")

        elif choice == '7':
            race_name = input("Enter race name: ")
            try:
                mid = int(input("Enter driver ID: "))
                car_name = input("Enter car name: ")
                if manager.create_race(race_name, mid, car_name):
                    print(f"Race '{race_name}' created successfully.")
            except ValueError:
                print("Invalid input. Driver ID must be an integer.")

        elif choice == '8':
            races = manager.get_races()
            if not races:
                print("No races scheduled.")
            else:
                for race in races:
                    print(format_race(race))

        elif choice == '9':
            try:
                rid = int(input("Enter race ID: "))
                pos = int(input("Enter position (1, 2, 3, etc.): "))
                if manager.record_race_result(rid, pos):
                    print("Race result recorded.")
            except ValueError:
                print("Invalid input. Race ID and Position must be integers.")

        elif choice == '10':
            races = manager.get_races()
            completed_races = [r for r in races if r["status"] == "Completed"]
            if not completed_races:
                print("No race results recorded.")
            else:
                for race in completed_races:
                    print(format_result(race))

        elif choice == '11':
            mission_name = input("Enter mission name: ")
            print("Types: delivery, rescue, heist, repair")
            mission_type = input("Enter mission type: ")
            if manager.assign_mission(mission_name, mission_type):
                print(f"Mission '{mission_name}' assigned successfully.")

        elif choice == '12':
            missions = manager.get_missions()
            if not missions:
                print("No missions assigned.")
            else:
                for m in missions:
                    print(f"Name: {m['name']} | Type: {m['type']} | Status: {m['status']}")

        elif choice == '13':
            car_name = input("Enter car name: ")
            try:
                tier = int(input("Enter upgrade tier (1, 2, 3): "))
                if manager.upgrade_car(car_name, tier):
                    print("Tuning complete.")
            except ValueError:
                print("Invalid input. Tier must be 1, 2, or 3.")

        elif choice == '14':
            status = manager.get_reputation_status()
            print("--- Team Status ---")
            print(f"Reputation Points: {status['reputation']}")
            print(f"Active Sponsor: {status['sponsor'] if status['sponsor'] else 'None'}")

        elif choice == '15':
            print("Exiting StreetRace Manager. Stay safe on the streets!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
