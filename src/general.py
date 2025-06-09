'''
from typing import Optional

class General:
    def __init__(self, general_id: str, name: str, faction_id: Optional[str] = None, command: int = 50, attack_skill: int = 50, defense_skill: int = 50):
        self.general_id = general_id
        self.name = name
        self.faction_id: Optional[str] = faction_id
        self.command = command
        self.attack_skill = attack_skill
        self.defense_skill = defense_skill
        self.loyalty = 100 # Example
        self.current_location_city_id: Optional[str] = None

    def __str__(self):
        return f"General: {self.name} (ID: {self.general_id}), Faction: {self.faction_id or 'None'}, Location: {self.current_location_city_id or 'N/A'}"
'''