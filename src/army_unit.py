
from typing import Optional

class ArmyUnit:
    def __init__(self, unit_id: str, unit_type_id: str, base_attack: int, base_defense: int, 
                 owning_faction_id: str, soldiers: int = 1000, 
                 leading_general_id: Optional[str] = None):
        self.unit_id = unit_id
        self.unit_type_id = unit_type_id 
        self.base_attack = base_attack
        self.base_defense = base_defense
        self.owning_faction_id = owning_faction_id
        self.leading_general_id: Optional[str] = leading_general_id
        self.soldiers = soldiers
        self.max_soldiers = soldiers 
        self.morale = 100 
        self.current_location_city_id: Optional[str] = None 

    def __str__(self):
        leader_str = f", Leader: {self.leading_general_id}" if self.leading_general_id else ""
        return f"Unit: {self.unit_id} ({self.unit_type_id}), ATK:{self.base_attack}, DEF:{self.base_defense}, Soldiers: {self.soldiers}, Faction: {self.owning_faction_id}, Location: {self.current_location_city_id or 'Field'}{leader_str}"

    def take_damage(self, damage: int):
        self.soldiers -= damage
        if self.soldiers < 0:
            self.soldiers = 0
        return self.soldiers == 0 # Returns True if unit is destroyed
