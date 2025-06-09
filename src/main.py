'''
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
    berlin = City(city_id="berlin", name="Berlin", region_id="brandenburg") # Expanded

    europe_map.add_city(paris)
    europe_map.add_city(london)
    europe_map.add_city(vienna)
    europe_map.add_city(berlin)

    # 3. Create Game State
    game = GameState(game_map_obj=europe_map)

    # 4. Create Factions and add to game state
    france = Faction(faction_id="france", name="French Empire", short_name="France", capital_city_id="paris")
    britain = Faction(faction_id="britain", name="Great Britain", short_name="Britain", capital_city_id="london")
    austria = Faction(faction_id="austria", name="Austrian Empire", short_name="Austria", capital_city_id="vienna")
    prussia = Faction(faction_id="prussia", name="Kingdom of Prussia", short_name="Prussia", capital_city_id="berlin") # Expanded

    game.add_faction(france)
    game.add_faction(britain)
    game.add_faction(austria)
    game.add_faction(prussia) # Expanded
    game.player_faction_id = "france"

    # 5. Assign cities to factions
    game.assign_city_to_faction("paris", "france")
    game.assign_city_to_faction("london", "britain")
    game.assign_city_to_faction("vienna", "austria")
    game.assign_city_to_faction("berlin", "prussia") # Expanded

    # 6. Create Generals and add to game state
    napoleon = General(general_id="napoleon", name="Napoleon Bonaparte", faction_id="france", command=95, attack_skill=90, defense_skill=80)
    davout = General(general_id="davout", name="Louis Davout", faction_id="france", command=85, attack_skill=80, defense_skill=75)
    nelson = General(general_id="nelson", name="Horatio Nelson", faction_id="britain", command=90)
    archduke_charles = General(general_id="archduke_charles", name="Archduke Charles", faction_id="austria", command=80)
    blucher = General(general_id="blucher", name="Gebhard von Blucher", faction_id="prussia", command=82) # Expanded

    game.add_general(napoleon)
    game.add_general(davout)
    game.add_general(nelson)
    game.add_general(archduke_charles)
    game.add_general(blucher) # Expanded

    # 7. Place Generals in cities
    game.place_general_in_city("napoleon", "paris")
    game.place_general_in_city("davout", "paris")
    game.place_general_in_city("nelson", "london")
    game.place_general_in_city("archduke_charles", "vienna")
    game.place_general_in_city("blucher", "berlin") # Expanded


    # 8. Create Army Units and add to game state
    fra_corps_1 = ArmyUnit(unit_id="fra_corps_1", unit_type_id="infantry_corps", owning_faction_id="france", soldiers=25000, leading_general_id="davout")
    bri_fleet_1 = ArmyUnit(unit_id="bri_fleet_1", unit_type_id="fleet_channel", owning_faction_id="britain", soldiers=100) 
    aus_army_1 = ArmyUnit(unit_id="aus_army_1", unit_type_id="infantry_division", owning_faction_id="austria", soldiers=30000, leading_general_id="archduke_charles")
    pru_corps_1 = ArmyUnit(unit_id="pru_corps_1", unit_type_id="infantry_corps", owning_faction_id="prussia", soldiers=22000, leading_general_id="blucher") # Expanded

    game.add_army_unit(fra_corps_1)
    game.add_army_unit(bri_fleet_1)
    game.add_army_unit(aus_army_1)
    game.add_army_unit(pru_corps_1) # Expanded

    # 9. Place units in cities
    game.place_unit_in_city("fra_corps_1", "paris") 
    game.place_unit_in_city("bri_fleet_1", "london") 
    game.place_unit_in_city("aus_army_1", "vienna") 
    game.place_unit_in_city("pru_corps_1", "berlin")


    return game

def game_loop(game_state: GameState):
    print("\n--- Napoleon Game Prototype Command Mode ---")
    print("Available commands:")
    print("  info city <city_id>  - Show details for a city (e.g., info city paris)")
    print("  summary              - Display current game state summary")
    print("  next turn            - Advance to the next turn")
    print("  exit                 - Exit the game")

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
            game_state.display_summary() # Display summary after each turn for now
        elif action == "info" and len(parts) > 2 and parts[1] == "city":
            city_id_to_info = parts[2]
            print(game_state.get_city_details_str(city_id_to_info))
        else:
            print(f"Unknown command: '{command_input}'. Type 'exit' to quit.")


if __name__ == "__main__":
    print("Setting up Napoleon Game Prototype v0.1.1 (with commands)...")
    current_game_state = setup_initial_state()
    print("\n--- Initial Game State Summary ---")
    current_game_state.display_summary()

    game_loop(current_game_state)

    print("\nPrototype simulation finished.")
'''