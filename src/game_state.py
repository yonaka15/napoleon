
from typing import Dict, List, Optional, Set
from army_unit import ArmyUnit 
from game_enums import UnitType 
import math # For ceiling division
import random # For random target selection in simple combat

class GameState:
    def __init__(self, game_map_obj): 
        self.current_turn = 1
        self.game_map = game_map_obj 
        self.factions: Dict[str, any] = {} 
        self.generals: Dict[str, any] = {} 
        self.army_units: Dict[str, ArmyUnit] = {} 
        self.player_faction_id: Optional[str] = None
        self.allowed_building_types = ["market", "barracks"]

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

    def add_army_unit(self, unit_obj: ArmyUnit): 
        self.army_units[unit_obj.unit_id] = unit_obj
        if unit_obj.owning_faction_id:
             faction = self.factions.get(unit_obj.owning_faction_id)
             if faction:
                faction.army_units_list_ids.append(unit_obj.unit_id)

    def _remove_unit(self, unit_id_to_remove: str):
        unit = self.army_units.pop(unit_id_to_remove, None)
        if unit:
            print(f"DEBUG: Removing unit {unit_id_to_remove} from game state army_units list.")
            # Remove from faction's list
            if unit.owning_faction_id and unit.owning_faction_id in self.factions:
                faction = self.factions[unit.owning_faction_id]
                if unit_id_to_remove in faction.army_units_list_ids:
                    faction.army_units_list_ids.remove(unit_id_to_remove)
                    print(f"DEBUG: Removed unit {unit_id_to_remove} from faction {faction.faction_id} list.")
            
            # Remove from city's garrison if it was in one
            if unit.current_location_city_id and unit.current_location_city_id in self.game_map.cities:
                city = self.game_map.cities[unit.current_location_city_id]
                if unit_id_to_remove in city.garrisoned_units:
                    city.garrisoned_units.remove(unit_id_to_remove)
                    print(f"DEBUG: Removed unit {unit_id_to_remove} from city {city.city_id} garrison.")
        else:
            print(f"DEBUG: Attempted to remove unit {unit_id_to_remove}, but it was not found in army_units.")


    def assign_city_to_faction(self, city_id: str, faction_id: str):
        city = self.game_map.get_city(city_id)
        faction = self.factions.get(faction_id)
        if city and faction:
            # If city had a previous owner, remove it from their list
            if city.current_owner_faction_id and city.current_owner_faction_id in self.factions:
                old_owner_faction = self.factions[city.current_owner_faction_id]
                if city_id in old_owner_faction.controlled_cities_ids:
                    old_owner_faction.controlled_cities_ids.remove(city_id)

            city.current_owner_faction_id = faction_id
            if city_id not in faction.controlled_cities_ids:
                faction.controlled_cities_ids.append(city_id)
            print(f"INFO: City {city.name} (ID: {city_id}) is now controlled by {faction.name}.")
        elif not city:
            print(f"ERROR: Cannot assign city {city_id} - city not found.")
        elif not faction:
            print(f"ERROR: Cannot assign city {city_id} to faction {faction_id} - faction not found.")


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
            print(f"- {faction_obj.name} (ID: {faction_id}), Capital: {faction_obj.capital_city_id or 'N/A'}, Treasury: {faction_obj.treasury}")
        print("\nCities:")
        for city_id, city_obj in self.game_map.cities.items():
            owner_name = "Unowned"
            if city_obj.current_owner_faction_id and city_obj.current_owner_faction_id in self.factions:
                owner_name = self.factions[city_obj.current_owner_faction_id].short_name
            garrison_count = len(city_obj.garrisoned_units)
            print(f"- {city_obj.name} (ID: {city_id}), Owner: {owner_name}, Garrison: {garrison_count} units")
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
            print(f"- {str(unit_obj)}") # Using unit_obj.__str__()

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
                    garrison_details.append(f"  - {str(unit)}") # Using unit.__str__()
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
            unit_descs = [str(self.army_units.get(u_id)) if self.army_units.get(u_id) else u_id for u_id in faction.army_units_list_ids]
            army_units_str = "\n  - " + "\n  - ".join(unit_descs) if unit_descs else "None"
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
            return f"Error: Units can currently only be recruited in your capital city ({self.game_map.get_city(player_faction.capital_city_id).name if player_faction.capital_city_id else 'N/A'})."
        unit_type_enum = UnitType.from_string(unit_type_str)
        if not unit_type_enum:
            allowed_types_list = [ut.value for ut in UnitType if ut not in [UnitType.FLEET_CHANNEL, UnitType.INFANTRY_DIVISION]] 
            return f"Error: Invalid unit type '{unit_type_str}'. Allowed types: {', '.join(allowed_types_list)}"
        default_soldiers = {
            UnitType.INFANTRY_CORPS: 20000, UnitType.GUARD_CORPS: 15000,
            UnitType.CAVALRY_SQUADRON: 5000, UnitType.ARTILLERY_BATTERY: 2000,
            UnitType.MILITIA: 10000 }
        soldiers = default_soldiers.get(unit_type_enum, 1000)
        new_unit_id = f"{self.player_faction_id}_unit_{len(self.army_units) + sum(1 for u in self.army_units.values() if u.owning_faction_id == self.player_faction_id) + 1}"
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

    def _resolve_battle_in_city(self, city_obj) -> List[str]:
        battle_log = []
        units_in_city = [self.army_units[uid] for uid in city_obj.garrisoned_units if uid in self.army_units]
        if not units_in_city:
            return battle_log

        factions_present: Set[str] = set(unit.owning_faction_id for unit in units_in_city)
        if len(factions_present) <= 1:
            return battle_log # No battle if only one or zero factions present

        battle_log.append(f"\n--- Battle in {city_obj.name} (Turn {self.current_turn}) ---")
        original_owner_id = city_obj.current_owner_faction_id

        # Simple combat: All non-owners vs owner (if owner has units)
        # More complex (e.g., multi-sided free-for-all or alliances) can be added later.
        
        # Group units by faction
        units_by_faction: Dict[str, List[ArmyUnit]] = {faction_id: [] for faction_id in factions_present}
        for unit in units_in_city:
            units_by_faction[unit.owning_faction_id].append(unit)

        defender_faction_id = original_owner_id
        attacker_faction_ids = [fid for fid in factions_present if fid != defender_faction_id]

        if not attacker_faction_ids: # Should not happen if len(factions_present) > 1
            battle_log.append("  No attackers identified despite multiple factions. Skipping combat.")
            return battle_log

        # --- Defender's Turn (if defenders exist) ---
        defender_units = units_by_faction.get(defender_faction_id, [])
        if defender_units:
            defender_total_force = sum(u.soldiers for u in defender_units)
            # Defender attacks one random attacker unit (from any attacking faction)
            all_attacker_units = [u for fid in attacker_faction_ids for u in units_by_faction.get(fid, []) if u.soldiers > 0]
            if all_attacker_units:
                target_attacker_unit = random.choice(all_attacker_units)
                damage_to_attacker = math.ceil(defender_total_force * 0.1) # Defender deals 10% of their force
                damage_to_attacker = max(1, damage_to_attacker) # Minimum 1 damage
                battle_log.append(f"  {self.factions[defender_faction_id].short_name} (Defenders, {defender_total_force} total soldiers) attack! Target: {target_attacker_unit.unit_id} ({target_attacker_unit.unit_type_id}) of {self.factions[target_attacker_unit.owning_faction_id].short_name}.")
                destroyed = target_attacker_unit.take_damage(damage_to_attacker)
                battle_log.append(f"    {target_attacker_unit.unit_id} takes {damage_to_attacker} damage, {target_attacker_unit.soldiers} soldiers remain.")
                if destroyed:
                    battle_log.append(f"    Unit {target_attacker_unit.unit_id} has been destroyed!")
                    self._remove_unit(target_attacker_unit.unit_id)
                    # Update local list for this battle resolution
                    units_by_faction[target_attacker_unit.owning_faction_id] = [u for u in units_by_faction[target_attacker_unit.owning_faction_id] if u.unit_id != target_attacker_unit.unit_id]
            else:
                battle_log.append(f"  {self.factions[defender_faction_id].short_name} (Defenders) find no attacker units to target.")
        else:
            battle_log.append("  No defending units from original owner present.")

        # --- Attackers' Turn (combined for simplicity) ---
        all_attacker_units_remaining = [u for fid in attacker_faction_ids for u in units_by_faction.get(fid, []) if u.soldiers > 0]
        if all_attacker_units_remaining:
            attacker_total_force = sum(u.soldiers for u in all_attacker_units_remaining)
            # Attackers attack one random defender unit
            defender_units_remaining = [u for u in units_by_faction.get(defender_faction_id, []) if u.soldiers > 0]
            if defender_units_remaining:
                target_defender_unit = random.choice(defender_units_remaining)
                damage_to_defender = math.ceil(attacker_total_force * 0.1) # Attackers deal 10% of their combined force
                damage_to_defender = max(1, damage_to_defender)
                battle_log.append(f"  Combined Attackers ({attacker_total_force} total soldiers) attack! Target: {target_defender_unit.unit_id} ({target_defender_unit.unit_type_id}) of {self.factions[target_defender_unit.owning_faction_id].short_name}.")
                destroyed = target_defender_unit.take_damage(damage_to_defender)
                battle_log.append(f"    {target_defender_unit.unit_id} takes {damage_to_defender} damage, {target_defender_unit.soldiers} soldiers remain.")
                if destroyed:
                    battle_log.append(f"    Unit {target_defender_unit.unit_id} has been destroyed!")
                    self._remove_unit(target_defender_unit.unit_id)
                    units_by_faction[target_defender_unit.owning_faction_id] = [u for u in units_by_faction[target_defender_unit.owning_faction_id] if u.unit_id != target_defender_unit.unit_id]
            else:
                battle_log.append("  Combined Attackers find no defender units to target.")
        else:
            battle_log.append("  No attacker units remaining or present.")

        # --- City Occupation Check ---
        # Check if original defender still has units in the city
        defender_units_after_battle = [u for u in units_by_faction.get(original_owner_id, []) if u.soldiers > 0]
        if not defender_units_after_battle and original_owner_id: # Original owner wiped out or wasn't there
            # Check if any attackers remain
            surviving_attacker_factions: Dict[str, int] = {}
            for fid in attacker_faction_ids:
                faction_units = [u for u in units_by_faction.get(fid, []) if u.soldiers > 0]
                if faction_units:
                    surviving_attacker_factions[fid] = sum(u.soldiers for u in faction_units)
            
            if surviving_attacker_factions:
                # Strongest surviving attacker faction takes the city
                new_owner_id = max(surviving_attacker_factions, key=surviving_attacker_factions.get)
                if new_owner_id != original_owner_id:
                    battle_log.append(f"  DEFENDERS WIPED OUT! {city_obj.name} has been occupied by {self.factions[new_owner_id].name}!")
                    self.assign_city_to_faction(city_obj.city_id, new_owner_id)
                else:
                    battle_log.append(f"  Defenders held {city_obj.name} (or re-occupied immediately).") 
            else:
                battle_log.append(f"  All forces in {city_obj.name} have been wiped out. City becomes unowned (or remains with original if no attackers).")
                # Potentially set to unowned if no original owner either, or handle based on rules
                if original_owner_id: # If there was an owner and they are gone, and no attackers to take it
                    # This case means city might become neutral or revert to a default state if needed.
                    # For now, if attackers are also wiped out, it might remain with original if they had no units (edge case)
                    # or if no original owner, it stays unowned. This part might need more rules.
                    pass 
        elif original_owner_id: # Original owner still has units
             battle_log.append(f"  {self.factions[original_owner_id].short_name} holds {city_obj.name}.")
        else: # No original owner and potentially no one took it
            battle_log.append(f"  {city_obj.name} remains unowned or state unchanged after inconclusive battle.")

        battle_log.append(f"--- Battle in {city_obj.name} resolved. ---")
        return battle_log

    def _resolve_all_city_battles(self):
        all_battle_logs = []
        for city_id in list(self.game_map.cities.keys()): # Iterate over copy of keys in case cities dict changes
            city_obj = self.game_map.get_city(city_id)
            if city_obj:
                log_entries = self._resolve_battle_in_city(city_obj)
                if log_entries:
                    all_battle_logs.extend(log_entries)
        if all_battle_logs:
            for log_entry in all_battle_logs:
                print(log_entry)
        else:
            print("No battles occurred this turn.")

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
        
        self._resolve_all_city_battles() # Resolve battles at the end of the turn

