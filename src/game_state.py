
from typing import Dict, List, Optional
from army_unit import ArmyUnit # Import ArmyUnit
from game_enums import UnitType # Import UnitType

class GameState:
    def __init__(self, game_map_obj): # game_map_obj: GameMap
        self.current_turn = 1
        self.game_map = game_map_obj # GameMap instance
        self.factions: Dict[str, any] = {} # Faction objects, keyed by faction_id
        self.generals: Dict[str, any] = {} # General objects, keyed by general_id
        self.army_units: Dict[str, ArmyUnit] = {} # ArmyUnit objects, keyed by unit_id, type hint ArmyUnit
        self.player_faction_id: Optional[str] = None
        self.allowed_building_types = ["market", "barracks"] # Initial list

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

    def add_army_unit(self, unit_obj: ArmyUnit): # Type hint ArmyUnit
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
            player_faction = self.factions.get(self.player_faction_id)
            if player_faction:
                 print(f"Player is controlling: {player_faction.name}")
        print("\nFactions:")
        for faction_id, faction_obj in self.factions.items():
            print(f"- {faction_obj.name} (ID: {faction_id})")
        print("\nCities:")
        for city_id, city_obj in self.game_map.cities.items():
            owner_name = "Unowned"
            if city_obj.current_owner_faction_id and city_obj.current_owner_faction_id in self.factions:
                owner_name = self.factions[city_obj.current_owner_faction_id].short_name
            print(f"- {city_obj.name} (ID: {city_id}), Owner: {owner_name}")
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
            for unit_id_in_garrison in city.garrisoned_units:
                unit = self.army_units.get(unit_id_in_garrison)
                if unit:
                    garrison_details.append(f"  - {unit.unit_id} ({unit.unit_type_id}, {unit.soldiers} soldiers)")
                else:
                    garrison_details.append(f"  - {unit_id_in_garrison} (Error: Unit details not found)")
            if garrison_details:
                 garrison_str = "\n" + "\n".join(garrison_details)
        details.append(f"Garrison: {garrison_str}")
        adj_cities = self.game_map.adjacency_list.get(city_id, set())
        adj_str = ", ".join(adj_cities) if adj_cities else "None"
        details.append(f"Adjacent Cities: {adj_str}")
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
        if unit.owning_faction_id != self.player_faction_id:
            return f"Error: Unit {unit_id} ({unit.unit_type_id}) is not yours to command. Belongs to {unit.owning_faction_id}."
        target_city = self.game_map.get_city(target_city_id)
        if not target_city:
            return f"Error: Target city with ID '{target_city_id}' not found."
        current_city_id = unit.current_location_city_id
        if not current_city_id:
            return f"Error: Unit {unit_id} ({unit.unit_type_id}) is not currently in any city and cannot move."
        current_city_obj = self.game_map.get_city(current_city_id)
        if not current_city_obj:
             return f"Error: Current city for unit {unit_id} (ID: {current_city_id}) not found."
        if current_city_id == target_city_id:
            return f"Error: Unit {unit_id} ({unit.unit_type_id}) is already in {target_city.name}."
        if not self.game_map.are_adjacent(current_city_id, target_city_id):
            return f"Error: Unit {unit_id} ({unit.unit_type_id}) cannot move from {current_city_obj.name} to {target_city.name}. Cities are not adjacent."
        if unit_id in current_city_obj.garrisoned_units:
            current_city_obj.garrisoned_units.remove(unit_id)
        unit.current_location_city_id = target_city_id
        if unit_id not in target_city.garrisoned_units:
            target_city.garrisoned_units.append(unit_id)
        return f"Unit {unit_id} ({unit.unit_type_id}) successfully moved from {current_city_obj.name} to {target_city.name}."

    def develop_building_in_city(self, city_id: str, building_type: str) -> str:
        city = self.game_map.get_city(city_id)
        if not city:
            return f"Error: City with ID '{city_id}' not found."
        if building_type not in self.allowed_building_types:
            return f"Error: Building type '{building_type}' is not allowed. Allowed types: {', '.join(self.allowed_building_types)}"
        return f"{city.name} has started development of {building_type}. (Note: This is a prototype, actual construction not yet implemented.)"

    def recruit_unit(self, unit_type_str: str, city_id: str, general_id_str: Optional[str] = None) -> str:
        city = self.game_map.get_city(city_id)
        if not city:
            return f"Error: City with ID '{city_id}' not found for recruitment."

        player_faction = self.factions.get(self.player_faction_id)
        if not player_faction or city.current_owner_faction_id != self.player_faction_id:
            return f"Error: City {city.name} is not controlled by your faction ({self.player_faction_id})."

        if city_id != player_faction.capital_city_id:
            return f"Error: Units can currently only be recruited in your capital city ({player_faction.capital_city_id})."

        unit_type_enum = UnitType.from_string(unit_type_str)
        if not unit_type_enum:
            allowed_types = ", ".join([ut.value for ut in UnitType if ut not in [UnitType.FLEET_CHANNEL, UnitType.INFANTRY_DIVISION]]) # Exclude non-standard for now
            return f"Error: Invalid unit type '{unit_type_str}'. Allowed types: {allowed_types}"

        # Default soldier counts (can be moved to UnitType enum or a config file later)
        default_soldiers = {
            UnitType.INFANTRY_CORPS: 20000,
            UnitType.GUARD_CORPS: 15000,
            UnitType.CAVALRY_SQUADRON: 5000,
            UnitType.ARTILLERY_BATTERY: 2000,
            UnitType.MILITIA: 10000
        }
        soldiers = default_soldiers.get(unit_type_enum, 1000) # Default to 1000 if not specified

        new_unit_id = f"{self.player_faction_id}_unit_{len(self.army_units) + 1}" # Simple unique ID
        
        assigned_general_id = None
        if general_id_str:
            general_to_assign = self.generals.get(general_id_str)
            if not general_to_assign:
                return f"Error: General with ID '{general_id_str}' not found."
            if general_to_assign.faction_id != self.player_faction_id:
                return f"Error: General {general_to_assign.name} does not belong to your faction."
            if general_to_assign.current_location_city_id != city_id:
                return f"Error: General {general_to_assign.name} is not in {city.name} to lead the new unit."
            assigned_general_id = general_id_str

        new_unit = ArmyUnit(unit_id=new_unit_id, unit_type_id=unit_type_enum.value, 
                            owning_faction_id=self.player_faction_id, soldiers=soldiers, 
                            leading_general_id=assigned_general_id)
        
        self.add_army_unit(new_unit)
        self.place_unit_in_city(new_unit_id, city_id)

        recruit_msg = f"Successfully recruited {unit_type_enum.value} ({new_unit_id}) with {soldiers} soldiers in {city.name} for {player_faction.name}."
        if assigned_general_id:
            recruit_msg += f" Led by General {self.generals[assigned_general_id].name}."
        return recruit_msg

    def next_turn(self):
        self.current_turn += 1
        print(f"\n--- Advanced to Turn {self.current_turn} ---")
        for faction_obj in self.factions.values():
            income = 0
            for city_id_in_faction in faction_obj.controlled_cities_ids:
                city = self.game_map.get_city(city_id_in_faction)
                if city:
                    income += city.economy // 10 
            faction_obj.treasury += income
            if faction_obj.faction_id == self.player_faction_id:
                 print(f"{faction_obj.short_name} received {income} gold. Treasury: {faction_obj.treasury}")

