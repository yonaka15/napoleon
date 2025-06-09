
from enum import Enum

class TerrainType(Enum):
    PLAINS = "plains"
    FOREST = "forest"
    MOUNTAIN = "mountain"
    CITY = "city"

class UnitMovementType(Enum):
    FOOT = "foot"
    HORSE = "horse"
    ARTILLERY = "artillery"

class UnitType(Enum):
    # type_id_str, base_attack, base_defense, default_soldiers
    INFANTRY_CORPS = ("infantry_corps", 25, 20, 20000)
    GUARD_CORPS = ("guard_corps", 35, 25, 15000)
    CAVALRY_SQUADRON = ("cavalry_squadron", 30, 15, 5000) 
    ARTILLERY_BATTERY = ("artillery_battery", 40, 10, 2000) 
    MILITIA = ("militia", 15, 10, 10000)
    
    # For existing units in setup, to be aligned or phased out
    FLEET_CHANNEL = ("fleet_channel", 50, 30, 100) # Placeholder, naval combat is different
    INFANTRY_DIVISION = ("infantry_division", 20, 20, 30000) # Generic division, used by Austria initially

    def __init__(self, type_id_str, base_attack, base_defense, default_soldiers):
        self._type_id_str = type_id_str
        self._base_attack = base_attack
        self._base_defense = base_defense
        self._default_soldiers = default_soldiers

    @property
    def type_id(self):
        return self._type_id_str

    @property
    def base_attack(self):
        return self._base_attack

    @property
    def base_defense(self):
        return self._base_defense

    @property
    def default_soldiers(self):
        return self._default_soldiers

    @classmethod
    def from_string(cls, s: str):
        s_lower = s.lower()
        for member in cls:
            if member.type_id == s_lower:
                return member
        return None
