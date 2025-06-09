
from faction import Faction
from city import City
from general import General
from army_unit import ArmyUnit
from game_map import GameMap
from game_state import GameState
from game_enums import UnitType, DiplomaticStatus # Import DiplomaticStatus

def setup_initial_state() -> GameState:
    # 1. Create Game Map
    europe_map = GameMap(map_id="europe_1805")

    # 2. Create Cities and add to map
    paris = City(city_id="paris", name="Paris", region_id="ile_de_france")
    london = City(city_id="london", name="London", region_id="greater_london")
    vienna = City(city_id="vienna", name="Vienna", region_id="austria_proper")
    berlin = City(city_id="berlin", name="Berlin", region_id="brandenburg")
    marseille = City(city_id="marseille", name="Marseille", region_id="provence")
    lyon = City(city_id="lyon", name="Lyon", region_id="rhone_alpes")

    europe_map.add_city(paris)
    europe_map.add_city(london)
    europe_map.add_city(vienna)
    europe_map.add_city(berlin)
    europe_map.add_city(marseille)
    europe_map.add_city(lyon)

    # Define Adjacencies
    europe_map.add_adjacency("paris", "lyon")
    europe_map.add_adjacency("lyon", "marseille")
    europe_map.add_adjacency("paris", "berlin")
    europe_map.add_adjacency("berlin", "vienna")

    # 3. Create Game State
    game = GameState(game_map_obj=europe_map)

    # 4. Create Factions and add to game state
    # Order matters for diplomacy init if not handled carefully
    france = Faction(faction_id="france", name="French Empire", short_name="France", capital_city_id="paris")
    game.add_faction(france)
    britain = Faction(faction_id="britain", name="Great Britain", short_name="Britain", capital_city_id="london")
    game.add_faction(britain)
    austria = Faction(faction_id="austria", name="Austrian Empire", short_name="Austria", capital_city_id="vienna")
    game.add_faction(austria)
    prussia = Faction(faction_id="prussia", name="Kingdom of Prussia", short_name="Prussia", capital_city_id="berlin")
    game.add_faction(prussia)
    
    game.player_faction_id = "france"

    # Set Initial Diplomatic Status (after all factions are added)
    game.set_diplomatic_status("france", "britain", DiplomaticStatus.WAR, -100)
    game.set_diplomatic_status("france", "austria", DiplomaticStatus.WAR, -80)
    game.set_diplomatic_status("france", "prussia", DiplomaticStatus.PEACE, -20)
    game.set_diplomatic_status("britain", "austria", DiplomaticStatus.ALLIANCE, 70)
    game.set_diplomatic_status("britain", "prussia", DiplomaticStatus.PEACE, 30)
    game.set_diplomatic_status("austria", "prussia", DiplomaticStatus.PEACE, 10)

    # 5. Assign cities to factions
    game.assign_city_to_faction("paris", "france")
    game.assign_city_to_faction("lyon", "france")
    game.assign_city_to_faction("marseille", "france")
    game.assign_city_to_faction("london", "britain")
    game.assign_city_to_faction("vienna", "austria")
    game.assign_city_to_faction("berlin", "prussia")

    # 6. Create Generals and add to game state
    napoleon = General(general_id="napoleon", name="Napoleon Bonaparte", faction_id="france", command=95, attack_skill=90, defense_skill=80)
    france.leader_general_id = "napoleon"
    davout = General(general_id="davout", name="Louis Davout", faction_id="france", command=85, attack_skill=80, defense_skill=75)
    nelson = General(general_id="nelson", name="Horatio Nelson", faction_id="britain", command=90, attack_skill=70, defense_skill=60)
    britain.leader_general_id = "nelson"
    archduke_charles = General(general_id="archduke_charles", name="Archduke Charles", faction_id="austria", command=80, attack_skill=75, defense_skill=80)
    austria.leader_general_id = "archduke_charles"
    blucher = General(general_id="blucher", name="Gebhard von Blucher", faction_id="prussia", command=82, attack_skill=80, defense_skill=70)
    prussia.leader_general_id = "blucher"

    game.add_general(napoleon)
    game.add_general(davout)
    game.add_general(nelson)
    game.add_general(archduke_charles)
    game.add_general(blucher)

    # 7. Place Generals in cities
    game.place_general_in_city("napoleon", "paris")
    game.place_general_in_city("davout", "lyon")
    game.place_general_in_city("nelson", "london")
    game.place_general_in_city("archduke_charles", "vienna")
    game.place_general_in_city("blucher", "berlin")
 
    ut_inf_corps = UnitType.INFANTRY_CORPS
    ut_guard_corps = UnitType.GUARD_CORPS
    ut_inf_div = UnitType.INFANTRY_DIVISION
    ut_fleet = UnitType.FLEET_CHANNEL

    fra_corps_1 = ArmyUnit(unit_id="fra_corps_1", unit_type_id=ut_inf_corps.type_id, base_attack=ut_inf_corps.base_attack, base_defense=ut_inf_corps.base_defense, owning_faction_id="france", soldiers=ut_inf_corps.default_soldiers, leading_general_id="davout")
    fra_guard = ArmyUnit(unit_id="fra_guard", unit_type_id=ut_guard_corps.type_id, base_attack=ut_guard_corps.base_attack, base_defense=ut_guard_corps.base_defense, owning_faction_id="france", soldiers=ut_guard_corps.default_soldiers, leading_general_id="napoleon")
    bri_fleet_1 = ArmyUnit(unit_id="bri_fleet_1", unit_type_id=ut_fleet.type_id, base_attack=ut_fleet.base_attack, base_defense=ut_fleet.base_defense, owning_faction_id="britain", soldiers=ut_fleet.default_soldiers, leading_general_id="nelson") 
    aus_army_1 = ArmyUnit(unit_id="aus_army_1", unit_type_id=ut_inf_div.type_id, base_attack=ut_inf_div.base_attack, base_defense=ut_inf_div.base_defense, owning_faction_id="austria", soldiers=ut_inf_div.default_soldiers, leading_general_id="archduke_charles")
    pru_corps_1 = ArmyUnit(unit_id="pru_corps_1", unit_type_id=ut_inf_corps.type_id, base_attack=ut_inf_corps.base_attack, base_defense=ut_inf_corps.base_defense, owning_faction_id="prussia", soldiers=22000, leading_general_id="blucher")

    game.add_army_unit(fra_corps_1)
    game.add_army_unit(fra_guard)
    game.add_army_unit(bri_fleet_1)
    game.add_army_unit(aus_army_1)
    game.add_army_unit(pru_corps_1)

    # 9. Place units in cities
    game.place_unit_in_city("fra_corps_1", "lyon")
    game.place_unit_in_city("fra_guard", "paris")
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
    print("  info diplomacy [faction_id]        - Show diplomatic relations (e.g., info diplomacy or info diplomacy france)")
    print("  move unit <unit_id> to <city_id>   - Move YOUR unit to an ADJACENT city (e.g., move unit fra_guard to lyon)")
    print("  develop city <id> <b_type>         - Start development in a city (e.g., develop city paris market). Allowed: market, barracks")
    print("  recruit unit <u_type> in <city_id> [with <gen_id>] - Recruit a new unit in YOUR CAPITAL (e.g., recruit unit infantry_corps in paris with napoleon)")
    print("                                     Allowed unit types: infantry_corps, guard_corps, cavalry_squadron, artillery_battery, militia")
    print("  summary                          - Display current game state summary")
    print("  next turn                        - Advance to the next turn (triggers auto-combat if applicable)")
    print("  exit                             - Exit the game")

    while True:
        player_faction_name = game_state.factions[game_state.player_faction_id].short_name if game_state.player_faction_id and game_state.player_faction_id in game_state.factions else "NoPlayer"
        command_input = input(f"\nTurn {game_state.current_turn} ({player_faction_name})> ").strip().lower()
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
            game_state.display_summary() 
        elif action == "info" and len(parts) >= 2:
            sub_command = parts[1]
            if sub_command == "city" and len(parts) == 3:
                print(game_state.get_city_details_str(parts[2]))
            elif sub_command == "general" and len(parts) == 3:
                print(game_state.get_general_details_str(parts[2]))
            elif sub_command == "faction" and len(parts) == 3:
                print(game_state.get_faction_details_str(parts[2]))
            elif sub_command == "diplomacy":
                focus_faction_param = parts[2] if len(parts) == 3 else None
                print(game_state.get_diplomacy_summary_str(focus_faction_param))
            else:
                print(f"Unknown or incomplete info command: 'info {sub_command} ...'. Supported: city <id>, general <id>, faction <id>, diplomacy [faction_id]")
        elif action == "move" and len(parts) == 5 and parts[1] == "unit" and parts[3] == "to":
            # ... (move unit logic - no changes)
            unit_id_to_move = parts[2]
            target_city_id_for_move = parts[4]
            print(game_state.move_unit(unit_id_to_move, target_city_id_for_move))
        elif action == "move" and (len(parts) < 5 or parts[1] != "unit" or parts[3] != "to"):
             print("Invalid move command. Format: move unit <unit_id> to <target_city_id>")
        elif action == "develop" and len(parts) == 4 and parts[1] == "city":
            # ... (develop city logic - no changes)
            city_id_to_develop = parts[2]
            building_type_to_develop = parts[3]
            print(game_state.develop_building_in_city(city_id_to_develop, building_type_to_develop))
        elif action == "develop" and (len(parts) < 4 or parts[1] != "city"):
            print("Invalid develop command. Format: develop city <city_id> <building_type>")
        elif action == "recruit" and len(parts) >= 5 and parts[1] == "unit" and parts[3] == "in":
            # ... (recruit unit logic - no changes)
            unit_type_to_recruit = parts[2]
            city_id_for_recruit = parts[4]
            general_id_for_recruit = None
            if len(parts) == 7 and parts[5] == "with":
                general_id_for_recruit = parts[6]
            elif len(parts) == 5:
                pass 
            else:
                print("Invalid recruit command format. Use: recruit unit <type> in <city_id> [with <general_id>]")
                continue
            print(game_state.recruit_unit(unit_type_to_recruit, city_id_for_recruit, general_id_for_recruit))
        elif action == "recruit" : 
            print("Invalid recruit command. Format: recruit unit <type> in <city_id> [with <general_id>]")
        else:
            print(f"Unknown command: '{command_input}'. Type 'help' for a list of commands (not yet implemented, use displayed list).")


if __name__ == "__main__":
    print("Setting up Napoleon Game Prototype v0.1.10 (with diplomacy info command)...")
    current_game_state = setup_initial_state()
    print("\n--- Initial Game State Summary ---")
    current_game_state.display_summary()

    # Display initial diplomacy for the player
    # print(current_game_state.get_diplomacy_summary_str())

    game_loop(current_game_state)

    print("\nPrototype simulation finished.")

