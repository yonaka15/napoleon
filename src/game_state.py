
from typing import Dict, List, Optional
# from faction import Faction
# from general import General
# from city import City
# from army_unit import ArmyUnit
# from game_map import GameMap

class GameState:
    def __init__(self, game_map_obj): # game_map_obj: GameMap
        self.current_turn = 1
        self.game_map = game_map_obj # GameMap instance
        self.factions: Dict[str, any] = {} # Faction objects, keyed by faction_id
        self.generals: Dict[str, any] = {} # General objects, keyed by general_id
        self.army_units: Dict[str, any] = {} # ArmyUnit objects, keyed by unit_id
        self.player_faction_id: Optional[str] = None

    def add_faction(self, faction_obj):
        self.factions[faction_obj.faction_id] = faction_obj

    def get_faction(self, faction_id: str):
        return self.factions.get(faction_id)

    def add_general(self, general_obj):
        self.generals[general_obj.general_id] = general_obj
        if general_obj.faction_id:
            faction = self.factions.get(general_obj.faction_id)
            if faction:
                faction.generals_list_ids.append(general_obj.general_id)


    def add_army_unit(self, unit_obj):
        self.army_units[unit_obj.unit_id] = unit_obj
        if unit_obj.owning_faction_id:
             faction = self.factions.get(unit_obj.owning_faction_id)
             if faction:
                faction.army_units_list_ids.append(unit_obj.unit_id)


    def assign_city_to_faction(self, city_id: str, faction_id: str):
        city = self.game_map.get_city(city_id)
        faction = self.factions.get(faction_id)
        if city and faction:
            city.current_owner_faction_id = faction_id
            if city_id not in faction.controlled_cities_ids:
                faction.controlled_cities_ids.append(city_id)

    def place_general_in_city(self, general_id: str, city_id: str):
        general = self.generals.get(general_id)
        city = self.game_map.get_city(city_id)
        if general and city:
            general.current_location_city_id = city_id

    def place_unit_in_city(self, unit_id: str, city_id: str):
        unit = self.army_units.get(unit_id)
        city = self.game_map.get_city(city_id)
        if unit and city:
            unit.current_location_city_id = city_id
            if unit_id not in city.garrisoned_units: # Ensure garrison list exists
                city.garrisoned_units.append(unit_id)


    def display_summary(self):
        print(f"--- Game State: Turn {self.current_turn} ---")
        print(f"Map: {self.game_map.map_id} with {len(self.game_map.cities)} cities.")
        if self.player_faction_id:
            player_faction = self.factions.get(self.player_faction_id)
            if player_faction:
                 print(f"Player is controlling: {player_faction.name}")

        print("\nFactions:")
        for faction_id, faction_obj in self.factions.items():
            print(f"- {faction_obj.name} (ID: {faction_id})")
            # print(f"  Capital: {faction_obj.capital_city_id or 'N/A'}, Treasury: {faction_obj.treasury}")
            # print(f"  Cities: {faction_obj.controlled_cities_ids}")
            # print(f"  Generals: {faction_obj.generals_list_ids}")
            # print(f"  Units: {faction_obj.army_units_list_ids}")


        print("\nCities:")
        for city_id, city_obj in self.game_map.cities.items():
            owner_name = "Unowned"
            if city_obj.current_owner_faction_id and city_obj.current_owner_faction_id in self.factions:
                owner_name = self.factions[city_obj.current_owner_faction_id].short_name
            print(f"- {city_obj.name} (ID: {city_id}), Owner: {owner_name}") # Simplified summary

        print("\nGenerals:")
        for general_id, general_obj in self.generals.items():
            faction_name = "N/A"
            if general_obj.faction_id and general_obj.faction_id in self.factions:
                faction_name = self.factions[general_obj.faction_id].short_name
            print(f"- {general_obj.name} (ID: {general_id}), Faction: {faction_name}, Location: {general_obj.current_location_city_id or 'Field'}")

        print("\nArmy Units:")
        for unit_id, unit_obj in self.army_units.items():
            faction_name = "N/A"
            if unit_obj.owning_faction_id and unit_obj.owning_faction_id in self.factions:
                faction_name = self.factions[unit_obj.owning_faction_id].short_name
            print(f"- Unit {unit_id} ({unit_obj.unit_type_id}), Faction: {faction_name}, Location: {unit_obj.current_location_city_id or 'Field'}, Soldiers: {unit_obj.soldiers}")

    def get_city_details_str(self, city_id: str) -> str:
        city = self.game_map.get_city(city_id)
        if not city:
            return f"Error: City with ID '{city_id}' not found."

        details = [f"--- City Details: {city.name} (ID: {city_id}) ---"]
        details.append(f"Region: {city.region_id}")
        owner_name = "Unowned"
        if city.current_owner_faction_id:
            faction = self.factions.get(city.current_owner_faction_id)
            if faction:
                owner_name = f"{faction.name} (ID: {faction.faction_id})"
        details.append(f"Owner: {owner_name}")
        details.append(f"Population: {city.population}")
        details.append(f"Economy: {city.economy}")
        details.append(f"Industry: {city.industry}")
        
        garrison_str = "None"
        if city.garrisoned_units:
            garrison_details = []
            for unit_id in city.garrisoned_units:
                unit = self.army_units.get(unit_id)
                if unit:
                    garrison_details.append(f"  - {unit.unit_id} ({unit.unit_type_id}, {unit.soldiers} soldiers)")
                else:
                    garrison_details.append(f"  - {unit_id} (Error: Unit details not found)")
            if garrison_details:
                 garrison_str = "\n" + "\n".join(garrison_details)
        details.append(f"Garrison: {garrison_str}")
        
        return "\n".join(details)

    def get_general_details_str(self, general_id: str) -> str:
        general = self.generals.get(general_id)
        if not general:
            return f"Error: General with ID '{general_id}' not found."

        details = [f"--- General Details: {general.name} (ID: {general_id}) ---"]
        faction_name = "None"
        if general.faction_id:
            faction = self.factions.get(general.faction_id)
            if faction:
                faction_name = f"{faction.name} (ID: {faction.faction_id})"
        details.append(f"Faction: {faction_name}")
        details.append(f"Command: {general.command}")
        details.append(f"Attack Skill: {general.attack_skill}")
        details.append(f"Defense Skill: {general.defense_skill}")
        details.append(f"Loyalty: {general.loyalty}")
        location_name = "Field (Not in a city)"
        if general.current_location_city_id:
            city = self.game_map.get_city(general.current_location_city_id)
            if city:
                location_name = f"{city.name} (ID: {city.city_id})"
            else:
                location_name = f"Unknown City (ID: {general.current_location_city_id})"
        details.append(f"Current Location: {location_name}")
        # Add more details like led units if implemented
        return "\n".join(details)

    def get_faction_details_str(self, faction_id: str) -> str:
        faction = self.factions.get(faction_id)
        if not faction:
            return f"Error: Faction with ID '{faction_id}' not found."

        details = [f"--- Faction Details: {faction.name} (ID: {faction_id}) ---"]
        details.append(f"Short Name: {faction.short_name}")
        leader_name = "None"
        if faction.leader_general_id:
            leader = self.generals.get(faction.leader_general_id)
            if leader:
                leader_name = f"{leader.name} (ID: {leader.general_id})"
        details.append(f"Leader: {leader_name}")
        capital_name = "None"
        if faction.capital_city_id:
            capital = self.game_map.get_city(faction.capital_city_id)
            if capital:
                capital_name = f"{capital.name} (ID: {capital.city_id})"
        details.append(f"Capital: {capital_name}")
        details.append(f"Treasury: {faction.treasury}")
        details.append(f"Food Reserves: {faction.food_reserves}")
        details.append(f"Manpower Pool: {faction.manpower_pool}")
        
        controlled_cities_str = "None"
        if faction.controlled_cities_ids:
            city_names = [self.game_map.get_city(c_id).name if self.game_map.get_city(c_id) else c_id for c_id in faction.controlled_cities_ids]
            controlled_cities_str = ", ".join(city_names)
        details.append(f"Controlled Cities: {controlled_cities_str}")

        generals_str = "None"
        if faction.generals_list_ids:
            general_names = [self.generals.get(g_id).name if self.generals.get(g_id) else g_id for g_id in faction.generals_list_ids]
            generals_str = ", ".join(general_names)
        details.append(f"Generals: {generals_str}")

        army_units_str = "None"
        if faction.army_units_list_ids:
            unit_descs = [f"{u_id} ({self.army_units.get(u_id).unit_type_id})" if self.army_units.get(u_id) else u_id for u_id in faction.army_units_list_ids]
            army_units_str = ", ".join(unit_descs)
        details.append(f"Army Units: {army_units_str}")
        
        return "\n".join(details)

    def move_unit(self, unit_id: str, target_city_id: str) -> str:
        unit = self.army_units.get(unit_id)
        if not unit:
            return f"Error: Unit with ID '{unit_id}' not found."

        target_city = self.game_map.get_city(target_city_id)
        if not target_city:
            return f"Error: Target city with ID '{target_city_id}' not found."

        # Remove unit from its current city's garrison, if any
        if unit.current_location_city_id:
            current_city = self.game_map.get_city(unit.current_location_city_id)
            if current_city and unit_id in current_city.garrisoned_units:
                current_city.garrisoned_units.remove(unit_id)
        
        # Update unit's location
        unit.current_location_city_id = target_city_id
        
        # Add unit to the target city's garrison
        if unit_id not in target_city.garrisoned_units:
            target_city.garrisoned_units.append(unit_id)
            
        return f"Unit {unit_id} successfully moved to {target_city.name} (ID: {target_city_id})."

    def next_turn(self):
        self.current_turn += 1
        print(f"\n--- Advanced to Turn {self.current_turn} ---")
        # Example: Simple income for each faction
        for faction_obj in self.factions.values():
            income = 0
            for city_id in faction_obj.controlled_cities_ids:
                city = self.game_map.get_city(city_id)
                if city:
                    income += city.economy // 10 # Simple income based on economy
            faction_obj.treasury += income
            print(f"{faction_obj.short_name} received {income} gold. Treasury: {faction_obj.treasury}")
