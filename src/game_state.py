
from typing import Dict, List, Optional, Set, Tuple
from army_unit import ArmyUnit 
from game_enums import UnitType, DiplomaticStatus 
from faction import Faction 
import math 
import random 

COMBAT_LATHALITY_FACTOR = 0.15 
GENERAL_ATTACK_BONUS_DIVISOR = 5.0
GENERAL_DEFENSE_BONUS_DIVISOR = 5.0
GENERAL_COMMAND_EFFICIENCY_DIVISOR = 200.0
CITY_DEFENSE_BONUS_MULTIPLIER = 1.25

class GameState:
    def __init__(self, game_map_obj): 
        self.current_turn = 1
        self.game_map = game_map_obj 
        self.factions: Dict[str, Faction] = {} 
        self.generals: Dict[str, any] = {} 
        self.army_units: Dict[str, ArmyUnit] = {} 
        self.player_faction_id: Optional[str] = None
        self.allowed_building_types = ["market", "barracks"]

    def add_faction(self, faction_obj: Faction):
        self.factions[faction_obj.faction_id] = faction_obj
        for other_faction_id in self.factions:
            if other_faction_id != faction_obj.faction_id:
                if other_faction_id not in faction_obj.diplomatic_relations:
                    self.set_diplomatic_status(faction_obj.faction_id, other_faction_id, DiplomaticStatus.PEACE, 0)
                other_faction = self.factions[other_faction_id]
                if faction_obj.faction_id not in other_faction.diplomatic_relations:
                     self.set_diplomatic_status(other_faction_id, faction_obj.faction_id, DiplomaticStatus.PEACE, 0)

    def get_faction(self, faction_id: str) -> Optional[Faction]: 
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
            if unit.owning_faction_id and unit.owning_faction_id in self.factions:
                faction = self.factions[unit.owning_faction_id]
                if unit_id_to_remove in faction.army_units_list_ids:
                    faction.army_units_list_ids.remove(unit_id_to_remove)
            if unit.current_location_city_id and unit.current_location_city_id in self.game_map.cities:
                city = self.game_map.cities[unit.current_location_city_id]
                if unit_id_to_remove in city.garrisoned_units:
                    city.garrisoned_units.remove(unit_id_to_remove)

    def assign_city_to_faction(self, city_id: str, faction_id: str):
        city = self.game_map.get_city(city_id)
        new_faction_obj = self.factions.get(faction_id)
        if city and new_faction_obj:
            if city.current_owner_faction_id and city.current_owner_faction_id in self.factions:
                old_owner_faction = self.factions[city.current_owner_faction_id]
                if city_id in old_owner_faction.controlled_cities_ids:
                    old_owner_faction.controlled_cities_ids.remove(city_id)
            city.current_owner_faction_id = faction_id
            if city_id not in new_faction_obj.controlled_cities_ids:
                new_faction_obj.controlled_cities_ids.append(city_id)
            print(f"INFO: City {city.name} (ID: {city_id}) is now controlled by {new_faction_obj.name}.")
        elif not city:
            print(f"ERROR: Cannot assign city {city_id} - city not found.")
        elif not new_faction_obj:
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
            print(f"- {general_obj.name} (ID: {general_id}), Faction: {general_obj.faction_id or 'N/A'}, Location: {general_obj.current_location_city_id or 'Field'}, CMD:{general_obj.command} ATK:{general_obj.attack_skill} DEF:{general_obj.defense_skill}")
        print("\nArmy Units:")
        for unit_id, unit_obj in self.army_units.items():
            print(f"- {str(unit_obj)}")

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
                    garrison_details.append(f"  - {str(unit)}")
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

    def move_unit(self, unit_id: str, target_city_id: str, acting_faction_id: Optional[str] = None) -> str:
        unit = self.army_units.get(unit_id)
        if not unit:
            return f"Error: Unit with ID '{unit_id}' not found."
        
        controller_faction_id = acting_faction_id if acting_faction_id else self.player_faction_id
        if not controller_faction_id:
             return f"Error: No controlling faction identified for move command."
        
        # Allow AI to move its own units, player to move player units
        if unit.owning_faction_id != controller_faction_id:
            controller_name = self.factions[controller_faction_id].short_name if controller_faction_id in self.factions else controller_faction_id
            return f"Error: Unit {unit_id} ({unit.unit_type_id}) does not belong to {controller_name}. Cannot command."

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
        
        moved_by_str = self.factions[controller_faction_id].short_name if controller_faction_id in self.factions else controller_faction_id
        return f"Unit {unit_id} ({unit.unit_type_id}) successfully moved from {current_city_obj.name} to {target_city.name} by {moved_by_str}."

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
            capital_name = self.game_map.get_city(player_faction.capital_city_id).name if player_faction.capital_city_id and self.game_map.get_city(player_faction.capital_city_id) else 'N/A'
            return f"Error: Units can currently only be recruited in your capital city ({capital_name})."
        unit_type_enum = UnitType.from_string(unit_type_str)
        if not unit_type_enum:
            allowed_types_list = [ut.type_id for ut in UnitType if ut not in [UnitType.FLEET_CHANNEL, UnitType.INFANTRY_DIVISION]] 
            return f"Error: Invalid unit type '{unit_type_str}'. Allowed types: {', '.join(allowed_types_list)}"
        soldiers = unit_type_enum.default_soldiers
        base_atk = unit_type_enum.base_attack
        base_def = unit_type_enum.base_defense
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
        new_unit = ArmyUnit(unit_id=new_unit_id, unit_type_id=unit_type_enum.type_id, 
                            base_attack=base_atk, base_defense=base_def,
                            owning_faction_id=self.player_faction_id, soldiers=soldiers, 
                            leading_general_id=assigned_general_id)
        self.add_army_unit(new_unit)
        self.place_unit_in_city(new_unit_id, city_id)
        recruit_msg = f"Successfully recruited {unit_type_enum.type_id} ({new_unit_id}) with BA:{base_atk}/BD:{base_def} and {soldiers} soldiers in {city.name} for {player_faction.name}."
        if assigned_general_id:
            recruit_msg += f" Led by General {self.generals[assigned_general_id].name}."
        return recruit_msg

    def set_diplomatic_status(self, faction1_id: str, faction2_id: str, status: DiplomaticStatus, relation_value: int = 0):
        f1 = self.factions.get(faction1_id)
        f2 = self.factions.get(faction2_id)
        if not f1 or not f2:
            print(f"ERROR: Cannot set diplomatic status between {faction1_id} and {faction2_id}. One or both factions not found.")
            return
        if faction1_id == faction2_id:
             return
        f1.diplomatic_relations[faction2_id] = {"status": status, "relation_value": relation_value, "treaties": []}
        f2.diplomatic_relations[faction1_id] = {"status": status, "relation_value": relation_value, "treaties": []}

    def get_diplomacy_summary_str(self, focus_faction_id_param: Optional[str] = None) -> str:
        focus_faction_id = focus_faction_id_param if focus_faction_id_param else self.player_faction_id
        if not focus_faction_id or focus_faction_id not in self.factions:
            return f"Error: Focus faction ID '{focus_faction_id if focus_faction_id else 'None'}' not found or player faction not set."
        focus_faction = self.factions[focus_faction_id]
        summary_lines = [f"--- Diplomatic Relations for {focus_faction.name} (ID: {focus_faction_id}) ---"]
        if not focus_faction.diplomatic_relations:
            summary_lines.append("  No diplomatic relations established yet.")
        for target_faction_id, relations in sorted(focus_faction.diplomatic_relations.items()):
            target_faction = self.factions.get(target_faction_id)
            if target_faction:
                status_val = relations.get("status")
                status_str = status_val.value if isinstance(status_val, DiplomaticStatus) else str(status_val)
                relation_val = relations.get("relation_value", "N/A")
                summary_lines.append(f"  - vs {target_faction.name} (ID: {target_faction_id}): {status_str}, Relation: {relation_val}")
            else:
                summary_lines.append(f"  - vs {target_faction_id}: Error - Target faction details not found.")
        return "\n".join(summary_lines)

    def _calculate_effective_stats(self, unit: ArmyUnit, is_defending_in_city: bool) -> Tuple[float, float, float]:
        eff_attack = float(unit.base_attack)
        eff_defense = float(unit.base_defense)
        eff_soldiers_for_attack = float(unit.soldiers)
        general = self.generals.get(unit.leading_general_id) if unit.leading_general_id else None
        if general:
            eff_attack += general.attack_skill / GENERAL_ATTACK_BONUS_DIVISOR
            eff_defense += general.defense_skill / GENERAL_DEFENSE_BONUS_DIVISOR
            eff_soldiers_for_attack *= (1 + general.command / GENERAL_COMMAND_EFFICIENCY_DIVISOR)
        if is_defending_in_city:
            eff_defense *= CITY_DEFENSE_BONUS_MULTIPLIER
        return max(1.0, eff_attack), max(1.0, eff_defense), max(1.0, eff_soldiers_for_attack)

    def _resolve_battle_in_city(self, city_obj) -> List[str]:
        battle_log = []
        present_unit_ids = list(city_obj.garrisoned_units)
        units_in_city = [self.army_units[uid] for uid in present_unit_ids if uid in self.army_units and self.army_units[uid].soldiers > 0]
        if not units_in_city:
            return battle_log
        factions_present: Set[str] = set(unit.owning_faction_id for unit in units_in_city)
        if len(factions_present) <= 1:
            return battle_log 
        battle_log.append(f"\n--- Battle in {city_obj.name} (ID: {city_obj.city_id}, Turn {self.current_turn}) ---")
        original_owner_id = city_obj.current_owner_faction_id
        battle_log.append(f"  City originally owned by: {self.factions[original_owner_id].short_name if original_owner_id and original_owner_id in self.factions else 'Unowned'}")
        units_by_faction: Dict[str, List[ArmyUnit]] = {faction_id: [] for faction_id in factions_present}
        for unit in units_in_city:
            units_by_faction[unit.owning_faction_id].append(unit)
        defender_faction_id = original_owner_id 
        attacker_faction_ids = [fid for fid in factions_present if fid != defender_faction_id]
        if not attacker_faction_ids:
            battle_log.append("  No attackers identified. Skipping combat.")
            return battle_log
        battle_log.append(f"  Defending Faction: {self.factions[defender_faction_id].short_name if defender_faction_id and defender_faction_id in self.factions else 'N/A'}")
        battle_log.append(f"  Attacking Factions: {[self.factions[fid].short_name for fid in attacker_faction_ids if fid in self.factions]}")
        if defender_faction_id and defender_faction_id in units_by_faction:
            current_defender_units = [u for u in units_by_faction[defender_faction_id] if u.soldiers > 0]
            all_attacker_units_for_targeting = [u for fid in attacker_faction_ids for u in units_by_faction.get(fid, []) if u.soldiers > 0]
            if current_defender_units and all_attacker_units_for_targeting:
                battle_log.append(f"  -- Defender's ({self.factions[defender_faction_id].short_name}) Attack Phase --")
                for def_unit in current_defender_units:
                    if not all_attacker_units_for_targeting: break
                    target_att_unit = random.choice(all_attacker_units_for_targeting)
                    att_eff, _, soldiers_eff_att = self._calculate_effective_stats(def_unit, True)
                    _, def_eff_target, _ = self._calculate_effective_stats(target_att_unit, False)
                    damage_ratio = att_eff / (att_eff + def_eff_target) 
                    potential_casualties = soldiers_eff_att * damage_ratio * COMBAT_LATHALITY_FACTOR
                    actual_casualties = math.ceil(potential_casualties * random.uniform(0.8, 1.2))
                    actual_casualties = max(1, min(actual_casualties, target_att_unit.soldiers))
                    battle_log.append(f"    D:{def_unit.unit_id}({def_unit.soldiers}) [EA:{att_eff:.1f} ES:{soldiers_eff_att:.0f}] attacks A:{target_att_unit.unit_id}({target_att_unit.soldiers}) [ED:{def_eff_target:.1f}]")
                    destroyed = target_att_unit.take_damage(actual_casualties)
                    battle_log.append(f"      {target_att_unit.unit_id} takes {actual_casualties} casualties. {target_att_unit.soldiers} remain.")
                    if destroyed:
                        battle_log.append(f"      Unit {target_att_unit.unit_id} has been destroyed!")
                        self._remove_unit(target_att_unit.unit_id)
                        all_attacker_units_for_targeting = [u for u in all_attacker_units_for_targeting if u.unit_id != target_att_unit.unit_id]
        all_attacker_units_for_attacking = [u for fid in attacker_faction_ids for u in units_by_faction.get(fid, []) if u.unit_id in self.army_units and self.army_units[u.unit_id].soldiers > 0]
        if all_attacker_units_for_attacking:
            current_defender_units_for_targeting = [u for u in units_by_faction.get(defender_faction_id, []) if u.unit_id in self.army_units and self.army_units[u.unit_id].soldiers > 0]
            if current_defender_units_for_targeting:
                battle_log.append(f"  -- Attackers' ({', '.join([self.factions[fid].short_name for fid in attacker_faction_ids if fid in self.factions])}) Attack Phase --")
                for att_unit in all_attacker_units_for_attacking:
                    if not current_defender_units_for_targeting: break
                    target_def_unit = random.choice(current_defender_units_for_targeting)
                    att_eff, _, soldiers_eff_att = self._calculate_effective_stats(att_unit, False)
                    _, def_eff_target, _ = self._calculate_effective_stats(target_def_unit, True)
                    damage_ratio = att_eff / (att_eff + def_eff_target) 
                    potential_casualties = soldiers_eff_att * damage_ratio * COMBAT_LATHALITY_FACTOR
                    actual_casualties = math.ceil(potential_casualties * random.uniform(0.8, 1.2))
                    actual_casualties = max(1, min(actual_casualties, target_def_unit.soldiers))
                    battle_log.append(f"    A:{att_unit.unit_id}({att_unit.soldiers}) [EA:{att_eff:.1f} ES:{soldiers_eff_att:.0f}] attacks D:{target_def_unit.unit_id}({target_def_unit.soldiers}) [ED:{def_eff_target:.1f}]")
                    destroyed = target_def_unit.take_damage(actual_casualties)
                    battle_log.append(f"      {target_def_unit.unit_id} takes {actual_casualties} casualties. {target_def_unit.soldiers} remain.")
                    if destroyed:
                        battle_log.append(f"      Unit {target_def_unit.unit_id} has been destroyed!")
                        self._remove_unit(target_def_unit.unit_id)
                        current_defender_units_for_targeting = [u for u in current_defender_units_for_targeting if u.unit_id != target_def_unit.unit_id]
        defender_units_after_battle = [u for u in units_by_faction.get(original_owner_id, []) if u.unit_id in self.army_units and self.army_units[u.unit_id].soldiers > 0]
        if not defender_units_after_battle and original_owner_id in factions_present:
            surviving_attacker_factions_map: Dict[str, int] = {}
            for fid in attacker_faction_ids:
                faction_units = [u for u in units_by_faction.get(fid, []) if u.unit_id in self.army_units and self.army_units[u.unit_id].soldiers > 0]
                if faction_units:
                    surviving_attacker_factions_map[fid] = sum(u.soldiers for u in faction_units)
            if surviving_attacker_factions_map:
                new_owner_id = max(surviving_attacker_factions_map, key=surviving_attacker_factions_map.get)
                if new_owner_id != original_owner_id:
                    battle_log.append(f"  DEFENDERS WIPED OUT! {city_obj.name} has been occupied by {self.factions[new_owner_id].name}!")
                    self.assign_city_to_faction(city_obj.city_id, new_owner_id)
            else: 
                battle_log.append(f"  All forces in {city_obj.name} have been wiped out. City remains with {self.factions[original_owner_id].short_name if original_owner_id and original_owner_id in self.factions else 'Unowned'}.")
        elif original_owner_id in factions_present: 
             battle_log.append(f"  {self.factions[original_owner_id].short_name} holds {city_obj.name}.")
        elif not original_owner_id:
            remaining_factions_in_city = set(u.owning_faction_id for u in self.army_units.values() if u.current_location_city_id == city_obj.city_id and u.soldiers > 0)
            if len(remaining_factions_in_city) == 1:
                new_owner_id = remaining_factions_in_city.pop()
                battle_log.append(f"  {city_obj.name} was unowned and is now claimed by {self.factions[new_owner_id].name}!")
                self.assign_city_to_faction(city_obj.city_id, new_owner_id)
            else:
                battle_log.append(f"  {city_obj.name} remains unowned or contested.")
        battle_log.append(f"--- Battle in {city_obj.name} resolved. ---")
        return battle_log

    def _resolve_all_city_battles(self):
        all_battle_logs = []
        for city_id in list(self.game_map.cities.keys()): 
            city_obj = self.game_map.get_city(city_id)
            if city_obj:
                log_entries = self._resolve_battle_in_city(city_obj)
                if log_entries:
                    all_battle_logs.extend(log_entries)
        if all_battle_logs:
            print("\n=== Combat Phase Report ===")
            for log_entry in all_battle_logs:
                print(log_entry)
            print("=========================")

    def _process_ai_faction_turn(self, faction_id: str):
        faction = self.factions.get(faction_id)
        if not faction or faction_id == self.player_faction_id:
            return

        ai_log = [f"\n--- AI Turn: {faction.short_name} (ID: {faction_id}) ---"]
        action_taken = False
        
        # Get all units owned by this AI faction that are in a city and have soldiers
        ai_units_in_cities = [u for u_id in faction.army_units_list_ids 
                              if (u := self.army_units.get(u_id)) and 
                                 u.current_location_city_id and 
                                 u.soldiers > 0]
        if not ai_units_in_cities:
            ai_log.append(f"  AI {faction.short_name} has no units in any city to move.")
        else:
            unit_to_move = random.choice(ai_units_in_cities)
            current_city_id = unit_to_move.current_location_city_id
            current_city_name = self.game_map.cities[current_city_id].name if current_city_id in self.game_map.cities else current_city_id

            # Prefer to move to adjacent enemy (WAR) cities
            target_cities_war = []
            target_cities_other = []

            if current_city_id and current_city_id in self.game_map.adjacency_list:
                for adj_city_id in self.game_map.adjacency_list[current_city_id]:
                    adj_city_obj = self.game_map.get_city(adj_city_id)
                    if not adj_city_obj: continue

                    # Check if target city is owned by an enemy at WAR
                    if adj_city_obj.current_owner_faction_id and \ 
                       adj_city_obj.current_owner_faction_id != faction_id and \ 
                       adj_city_obj.current_owner_faction_id in faction.diplomatic_relations and \ 
                       faction.diplomatic_relations[adj_city_obj.current_owner_faction_id].get("status") == DiplomaticStatus.WAR:
                        target_cities_war.append(adj_city_id)
                    else:
                        target_cities_other.append(adj_city_id)
                
                chosen_target_city_id = None
                if target_cities_war:
                    chosen_target_city_id = random.choice(target_cities_war)
                    ai_log.append(f"  AI {faction.short_name} unit {unit_to_move.unit_id} in {current_city_name} is targeting enemy city: {chosen_target_city_id}!")
                elif target_cities_other:
                    chosen_target_city_id = random.choice(target_cities_other)
                    ai_log.append(f"  AI {faction.short_name} unit {unit_to_move.unit_id} in {current_city_name} randomly targets adjacent city: {chosen_target_city_id}.")
                
                if chosen_target_city_id:
                    move_result = self.move_unit(unit_to_move.unit_id, chosen_target_city_id, acting_faction_id=faction_id)
                    ai_log.append(f"    Move Result: {move_result}")
                    action_taken = True
                else:
                    ai_log.append(f"  AI {faction.short_name}: Unit {unit_to_move.unit_id} in {current_city_name} has no valid adjacent cities to move to.")
            else:
                ai_log.append(f"  AI {faction.short_name}: Unit {unit_to_move.unit_id} in {current_city_name} - city has no adjacencies defined.")

        if not action_taken and not ai_units_in_cities: # If no units or no action was taken and had units initially (e.g. no valid moves)
             pass # No log needed if no units to begin with or no valid moves found, already logged
        elif not action_taken and ai_units_in_cities: # Had units, but couldn't make a move
            ai_log.append(f"  AI {faction.short_name} took no action with its units this turn (e.g. no valid moves from current positions).")
        
        if len(ai_log) > 1: # Only print if there's more than the header
            for entry in ai_log:
                print(entry)

    def next_turn(self):
        self.current_turn += 1
        print(f"\n--- Advanced to Turn {self.current_turn} ---")
        
        # Player Faction Income (example)
        if self.player_faction_id and self.player_faction_id in self.factions:
            player_faction_obj = self.factions[self.player_faction_id]
            income = 0
            for city_id_in_faction in list(player_faction_obj.controlled_cities_ids):
                city = self.game_map.get_city(city_id_in_faction)
                if city:
                    income += city.economy // 10 
            player_faction_obj.treasury += income
            print(f"  {player_faction_obj.short_name} received {income} gold. Treasury: {player_faction_obj.treasury}")

        print("\n-- AI Factions Processing --")
        for faction_id_ai in self.factions:
            if faction_id_ai != self.player_faction_id:
                self._process_ai_faction_turn(faction_id_ai)
                ai_faction_obj = self.factions[faction_id_ai]
                ai_income = 0
                for city_id_ai in list(ai_faction_obj.controlled_cities_ids):
                    city_ai = self.game_map.get_city(city_id_ai)
                    if city_ai:
                        ai_income += city_ai.economy // 10 
                ai_faction_obj.treasury += ai_income
        print("--------------------------")

        self._resolve_all_city_battles()

