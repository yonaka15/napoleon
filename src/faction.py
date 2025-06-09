
from typing import Optional, Dict, List, Any

class Faction:
    def __init__(self, faction_id: str, name: str, short_name: str, leader_id: str = None, capital_city_id: str = None):
        self.faction_id = faction_id
        self.name = name
        self.short_name = short_name
        self.leader_general_id = leader_id
        self.capital_city_id = capital_city_id
        self.controlled_cities_ids: List[str] = []
        self.generals_list_ids: List[str] = []
        self.army_units_list_ids: List[str] = []
        self.treasury = 1000  # Example starting value
        self.food_reserves = 500 # Example starting value
        self.manpower_pool = 10000 # Example starting value
        # diplomatic_relations: Dict[target_faction_id, Dict["status": DiplomaticStatus, "relation_value": int, "treaties": List[str]]]
        self.diplomatic_relations: Dict[str, Dict[str, Any]] = {} 

    def __str__(self):
        return f"Faction: {self.name} (ID: {self.faction_id}), Capital: {self.capital_city_id or 'N/A'}"
