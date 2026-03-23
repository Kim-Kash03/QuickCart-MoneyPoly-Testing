import sys
from manager import StreetRaceManager

def main():
    manager = StreetRaceManager()
    print("=== StreetRace Manager ===")
    
    while True:
        print("\nOptions:")
        print("1. Register Crew Member")
        print("2. View Crew")
        print("3. Exit")
        
        choice = input("Select an option: ")
        
        if choice == '1':
            name = input("Enter member name: ")
            role = input("Enter role (driver, mechanic, strategist): ")
            member_id = manager.register_member(name, role)
            print(f"Member registered with ID: {member_id}")
        
        elif choice == '2':
            crew = manager.get_crew()
            if not crew:
                print("No crew members registered.")
            for mid, data in crew.items():
                print(f"ID: {mid} | Name: {data['name']} | Role: {data['role']} | Skill: {data['skill_level']}")
        
        elif choice == '3':
            print("Exiting StreetRace Manager. Stay safe on the streets!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
