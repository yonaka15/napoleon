'''
from typing import Dict, List
# from city import City # Avoid circular dependency for now

class GameMap:
    def __init__(self, map_id: str):
        self.map_id = map_id
        self.cities: Dict[str, any] = {} # City objects, keyed by city_id
        self.regions: Dict[str, any] = {} # Region objects, keyed by region_id

    def add_city(self, city_obj):
        self.cities[city_obj.city_id] = city_obj

    def get_city(self, city_id: str):
        return self.cities.get(city_id)

    def __str__(self):
        return f"Map: {self.map_id}, Cities: {len(self.cities)}"
'''