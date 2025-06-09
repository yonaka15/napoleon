'''
from typing import Optional
# from faction import Faction # Avoid circular dependency for now

class City:
    def __init__(self, city_id: str, name: str, region_id: str, owner_faction_id: Optional[str] = None):
        self.city_id = city_id
        self.name = name
        self.region_id = region_id
        self.current_owner_faction_id: Optional[str] = owner_faction_id
        self.population = 50000 # Example
        self.economy = 100 # Example
        self.industry = 50 # Example
        self.garrisoned_units = []

    def __str__(self):
        return f"City: {self.name} (ID: {self.city_id}), Region: {self.region_id}, Owner: {self.current_owner_faction_id or 'Unowned'}"
'''