'''
from typing import Optional

class ArmyUnit:
    def __init__(self, unit_id: str, unit_type_id: str, owning_faction_id: str, soldiers: int = 1000, leading_general_id: Optional[str] = None):
        self.unit_id = unit_id
        self.unit_type_id = unit_type_id # e.g., "line_infantry", "cuirassier"
        self.owning_faction_id = owning_faction_id
        self.leading_general_id: Optional[str] = leading_general_id
        self.soldiers = soldiers
        self.max_soldiers = soldiers
        self.morale = 100
        self.current_location_city_id: Optional[str] = None # Or coordinates

    def __str__(self):
        return f"Unit: {self.unit_id} ({self.unit_type_id}), Soldiers: {self.soldiers}, Faction: {self.owning_faction_id}, Location: {self.current_location_city_id or 'N/A'}"
'''