# StreetRace Manager Integration Report

## Designed Modules
The StreetRace Manager system consists of 8 interconnected modules:
1. **Registration**: Registers crew members with names and roles.
2. **Crew Management**: Manages roles (e.g., driver, mechanic, strategist) and skill levels (1-10).
3. **Inventory**: Tracks cars, spare parts, tools, and cash balance.
4. **Race Management**: Creates races, validates that only drivers can race, and checks car availability.
5. **Results**: Records race outcomes, awards prize money (updates cash), and increases driver skill on wins. Includes a chance of car damage.
6. **Mission Planning**: Assigns missions (e.g., delivery, rescue, repair) and verifies required roles. Repair missions fix damaged cars.
7. **Tuning & Upgrades (Extra 1)**: Allows upgrading cars (performance boost) using cash, parts, and a mechanic.
8. **Reputation & Sponsorship (Extra 2)**: Tracks team fame from race wins and unlocks sponsorships that grant cash/parts bonuses.

## Integration & Data Flow
The `main.py` CLI uses a central `manager.py` to route data between modules. Business rule interactions are robustly implemented:
- **Role Enforcement**: `manager.create_race` checks the `crew` dictionary to ensure the selected participant is a 'driver'. `manager.assign_mission` checks available roles against required roles (e.g., a 'heist' needs a driver, mechanic, and strategist).
- **Asset/Currency Flow**: `record_race_result` calculates the prize and calls `update_cash` on the inventory. Winning a race also calls logic in the `reputation` module to increase fame and unlock sponsorships (which again updates inventory cash and parts).
- **Damage & Repair Loop**: After a race, there is a chance (`damage_car`) that a car enters a "Damaged" status. A "repair" mission (requiring a mechanic) calls `repair_car` to reset the status to "Healthy".
- **Upgrade Constraints**: `upgrade_car` checks for sufficient cash and parts in inventory *and* verifies that a mechanic exists in the crew before applying the performance boost.

## Testing Strategy
Integration tests were designed using `pytest` in `tests/integration_tests.py` to verify data flow across all components, simulating a full user journey: Registration -> Inventory Setup -> Racing -> Checking Cash/Reputation/Upgrades -> Damage/Repair Missions. All edge cases (e.g., non-drivers racing, insufficient cash for tuning) were tested and validated.

## Verification Results
The integration suite in `tests/integration_tests.py` was executed using `pytest`. All test cases passed successfully, confirming:
- **Registration & Roles**: Crew members can be registered and their roles (driver, mechanic, strategist) are correctly validated.
- **Racing**: Drivers and cars are correctly matched for races; non-drivers are blocked.
- **Economics**: Race prizes and sponsorship bonuses correctly flow into the inventory cash balance.
- **Maintenance**: Car damage is correctly handled and repair missions (requiring mechanics) successfully restore car health.
- **Mission Planning**: Complex missions (like 'heist') correctly verify that all required roles are present in the crew.
- **Tuning**: Multi-resource constraints (cash, parts, and mechanic) for car upgrades are enforced.
- **Reputation**: Winning races correctly builds team fame and unlocks tiered sponsorship rewards.

Final status: **System Integrated and Verified.**
