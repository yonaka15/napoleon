'''
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
            if unit_id not in city.garrisoned_units:
                city.garrisoned_units.append(unit_id)


    def display_summary(self):
        print(f"--- Game State: Turn {self.current_turn} ---")
        print(f"Map: {self.game_map.map_id} with {len(self.game_map.cities)} cities.")
        if self.player_faction_id:
            print(f"Player is controlling: {self.factions.get(self.player_faction_id).name}")

        print("\nFactions:")
        for faction_id, faction_obj in self.factions.items():
            print(f"- {faction_obj.name} (ID: {faction_id})")
            print(f"  Capital: {faction_obj.capital_city_id or 'N/A'}, Treasury: {faction_obj.treasury}")
            print(f"  Cities: {faction_obj.controlled_cities_ids}")
            print(f"  Generals: {faction_obj.generals_list_ids}")
            print(f"  Units: {faction_obj.army_units_list_ids}")


        print("\nCities:")
        for city_id, city_obj in self.game_map.cities.items():
            owner_name = "Unowned"
            if city_obj.current_owner_faction_id and city_obj.current_owner_faction_id in self.factions:
                owner_name = self.factions[city_obj.current_owner_faction_id].short_name
            print(f"- {city_obj.name} (ID: {city_id}), Owner: {owner_name}, Garrison: {city_obj.garrisoned_units}")

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

    def next_turn(self):
        self.current_turn += 1
        print(f"\n--- Advanced to Turn {self.current_turn} ---")
        # Add more turn processing logic here in the future
        # For example, resource collection, unit movement AI, etc.
'''