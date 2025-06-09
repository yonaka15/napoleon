
from faction import Faction
from city import City
from general import General
from army_unit import ArmyUnit
from game_map import GameMap
from game_state import GameState

def setup_initial_state() -> GameState:
    # 1. Create Game Map
    europe_map = GameMap(map_id="europe_1805")

    # 2. Create Cities and add to map
    paris = City(city_id="paris", name="Paris", region_id="ile_de_france")
    london = City(city_id="london", name="London", region_id="greater_london")
    vienna = City(city_id="vienna", name="Vienna", region_id="austria_proper")
    berlin = City(city_id="berlin", name="Berlin", region_id="brandenburg")
    marseille = City(city_id="marseille", name="Marseille", region_id="provence") # New city for adjacency
    lyon = City(city_id="lyon", name="Lyon", region_id="rhone_alpes")             # New city for adjacency

    europe_map.add_city(paris)
    europe_map.add_city(london)
    europe_map.add_city(vienna)
    europe_map.add_city(berlin)
    europe_map.add_city(marseille) # Add new city to map
    europe_map.add_city(lyon)      # Add new city to map

    # Define Adjacencies
    europe_map.add_adjacency("paris", "lyon")
    europe_map.add_adjacency("lyon", "marseille")
    europe_map.add_adjacency("paris", "berlin") # For testing direct long move before adjacency check
    europe_map.add_adjacency("berlin", "vienna")
    # paris <-> london = NOT adjacent in this setup
    # paris <-> vienna = NOT directly adjacent
    # lyon <-> berlin = NOT adjacent

    # 3. Create Game State
    game = GameState(game_map_obj=europe_map)

    # 4. Create Factions and add to game state
    france = Faction(faction_id="france", name="French Empire", short_name="France", capital_city_id="paris")
    britain = Faction(faction_id="britain", name="Great Britain", short_name="Britain", capital_city_id="london")
    austria = Faction(faction_id="austria", name="Austrian Empire", short_name="Austria", capital_city_id="vienna")
    prussia = Faction(faction_id="prussia", name="Kingdom of Prussia", short_name="Prussia", capital_city_id="berlin")

    game.add_faction(france)
    game.add_faction(britain)
    game.add_faction(austria)
    game.add_faction(prussia)
    game.player_faction_id = "france"

    # 5. Assign cities to factions
    game.assign_city_to_faction("paris", "france")
    game.assign_city_to_faction("lyon", "france")      # Lyon to France
    game.assign_city_to_faction("marseille", "france") # Marseille to France
    game.assign_city_to_faction("london", "britain")
    game.assign_city_to_faction("vienna", "austria")
    game.assign_city_to_faction("berlin", "prussia")

    # 6. Create Generals and add to game state
    napoleon = General(general_id="napoleon", name="Napoleon Bonaparte", faction_id="france", command=95, attack_skill=90, defense_skill=80)
    france.leader_general_id = "napoleon" # Set faction leader
    davout = General(general_id="davout", name="Louis Davout", faction_id="france", command=85, attack_skill=80, defense_skill=75)
    nelson = General(general_id="nelson", name="Horatio Nelson", faction_id="britain", command=90)
    britain.leader_general_id = "nelson"
    archduke_charles = General(general_id="archduke_charles", name="Archduke Charles", faction_id="austria", command=80)
    austria.leader_general_id = "archduke_charles"
    blucher = General(general_id="blucher", name="Gebhard von Blucher", faction_id="prussia", command=82)
    prussia.leader_general_id = "blucher"

    game.add_general(napoleon)
    game.add_general(davout)
    game.add_general(nelson)
    game.add_general(archduke_charles)
    game.add_general(blucher)

    # 7. Place Generals in cities
    game.place_general_in_city("napoleon", "paris")
    game.place_general_in_city("davout", "lyon") # Davout in Lyon
    game.place_general_in_city("nelson", "london")
    game.place_general_in_city("archduke_charles", "vienna")
    game.place_general_in_city("blucher", "berlin")

    # 8. Create Army Units and add to game state
    fra_corps_1 = ArmyUnit(unit_id="fra_corps_1", unit_type_id="infantry_corps", owning_faction_id="france", soldiers=25000, leading_general_id="davout")
    fra_guard = ArmyUnit(unit_id="fra_guard", unit_type_id="guard_corps", owning_faction_id="france", soldiers=15000, leading_general_id="napoleon")
    bri_fleet_1 = ArmyUnit(unit_id="bri_fleet_1", unit_type_id="fleet_channel", owning_faction_id="britain", soldiers=100)
    aus_army_1 = ArmyUnit(unit_id="aus_army_1", unit_type_id="infantry_division", owning_faction_id="austria", soldiers=30000, leading_general_id="archduke_charles")
    pru_corps_1 = ArmyUnit(unit_id="pru_corps_1", unit_type_id="infantry_corps", owning_faction_id="prussia", soldiers=22000, leading_general_id="blucher")

    game.add_army_unit(fra_corps_1)
    game.add_army_unit(fra_guard)
    game.add_army_unit(bri_fleet_1)
    game.add_army_unit(aus_army_1)
    game.add_army_unit(pru_corps_1)

    # 9. Place units in cities
    game.place_unit_in_city("fra_corps_1", "lyon") # Davout's corps in Lyon
    game.place_unit_in_city("fra_guard", "paris")   # Guard in Paris with Napoleon
    game.place_unit_in_city("bri_fleet_1", "london")
    game.place_unit_in_city("aus_army_1", "vienna")
    game.place_unit_in_city("pru_corps_1", "berlin")

    return game

def game_loop(game_state: GameState):
    print("\n--- Napoleon Game Prototype Command Mode ---")
    print("Available commands:")
    print("  info city <city_id>                - Show details for a city (e.g., info city paris)")
    print("  info general <gen_id>              - Show details for a general (e.g., info general napoleon)")
    print("  info faction <faction_id>          - Show details for a faction (e.g., info faction france)")
    print("  move unit <unit_id> to <city_id>   - Move a unit to an ADJACENT city (e.g., move unit fra_corps_1 to paris)")
    print("  develop city <id> <building_type>  - Start development in a city (e.g., develop city paris market). Allowed types: market, barracks")
    print("  summary                          - Display current game state summary")
    print("  next turn                        - Advance to the next turn")
    print("  exit                             - Exit the game")

    while True:
        command_input = input(f"\nTurn {game_state.current_turn}> ").strip().lower()
        parts = command_input.split()
        if not parts:
            continue

        action = parts[0]

        if action == "exit":
            print("Exiting game...")
            break
        elif action == "summary":
            game_state.display_summary()
        elif action == "next" and len(parts) > 1 and parts[1] == "turn":
            game_state.next_turn()
            # game_state.display_summary() # Display summary after each turn for now
        elif action == "info" and len(parts) > 2:
            sub_command = parts[1]
            target_id = parts[2]
            if sub_command == "city":
                print(game_state.get_city_details_str(target_id))
            elif sub_command == "general":
                print(game_state.get_general_details_str(target_id))
            elif sub_command == "faction":
                print(game_state.get_faction_details_str(target_id))
            else:
                print(f"Unknown info command: 'info {sub_command}'. Supported: city, general, faction")
        elif action == "move" and len(parts) == 5 and parts[1] == "unit" and parts[3] == "to":
            unit_id_to_move = parts[2]
            target_city_id_for_move = parts[4]
            print(game_state.move_unit(unit_id_to_move, target_city_id_for_move))
        elif action == "move" and (len(parts) < 5 or parts[1] != "unit" or parts[3] != "to"):
             print("Invalid move command. Format: move unit <unit_id> to <target_city_id>")
        elif action == "develop" and len(parts) == 4 and parts[1] == "city":
            city_id_to_develop = parts[2]
            building_type_to_develop = parts[3]
            print(game_state.develop_building_in_city(city_id_to_develop, building_type_to_develop))
        elif action == "develop" and (len(parts) < 4 or parts[1] != "city"):
            print("Invalid develop command. Format: develop city <city_id> <building_type>")
        else:
            print(f"Unknown command: '{command_input}'. Type 'help' for a list of commands (not yet implemented, use displayed list).")


if __name__ == "__main__":
    print("Setting up Napoleon Game Prototype v0.1.5 (with map adjacency)...")
    current_game_state = setup_initial_state()
    print("\n--- Initial Game State Summary ---")
    current_game_state.display_summary()

    game_loop(current_game_state)

    print("\nPrototype simulation finished.")

