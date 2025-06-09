
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
    INFANTRY_CORPS = "infantry_corps"
    GUARD_CORPS = "guard_corps"
    CAVALRY_SQUADRON = "cavalry_squadron"
    ARTILLERY_BATTERY = "artillery_battery"
    MILITIA = "militia"
    FLEET_CHANNEL = "fleet_channel" # Existing from setup
    INFANTRY_DIVISION = "infantry_division" # Existing from setup

    @classmethod
    def from_string(cls, s: str):
        try:
            return cls(s.lower())
        except ValueError:
            return None
