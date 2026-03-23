import sys
from manager import StreetRaceManager

def main():
    manager = StreetRaceManager()
    print("=== StreetRace Manager ===")
    
    while True:
        print("\nOptions:")
        print("1. Register Crew Member")
        print("2. View Crew")
        print("3. Update Member Role")
        print("4. Update Member Skill Level")
        print("5. Exit")
        
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
            print("Exiting StreetRace Manager. Stay safe on the streets!")
            break
        
        else:
            print("Invalid option. Please try again.")

if __name__ == "__main__":
    main()
