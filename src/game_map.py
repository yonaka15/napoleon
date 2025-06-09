from typing import Dict, List, Set # Add Set

class GameMap:
    def __init__(self, map_id: str):
        self.map_id = map_id
        self.cities: Dict[str, any] = {} # City objects, keyed by city_id
        self.regions: Dict[str, any] = {} # Region objects, keyed by region_id
        self.adjacency_list: Dict[str, Set[str]] = {} # New: Stores city adjacencies

    def add_city(self, city_obj):
        self.cities[city_obj.city_id] = city_obj
        if city_obj.city_id not in self.adjacency_list: # Initialize adjacency set for new city
            self.adjacency_list[city_obj.city_id] = set()

    def get_city(self, city_id: str):
        return self.cities.get(city_id)

    def add_adjacency(self, city1_id: str, city2_id: str):
        if city1_id not in self.cities or city2_id not in self.cities:
            print(f"Warning: Attempting to add adjacency for non-existent city: {city1_id} or {city2_id}")
            return
        self.adjacency_list.setdefault(city1_id, set()).add(city2_id)
        self.adjacency_list.setdefault(city2_id, set()).add(city1_id)

    def are_adjacent(self, city1_id: str, city2_id: str) -> bool:
        if city1_id not in self.cities or city2_id not in self.cities:
            return False
        return city2_id in self.adjacency_list.get(city1_id, set())

    def __str__(self):
        return f"Map: {self.map_id}, Cities: {len(self.cities)}, Adjacencies Defined for {len(self.adjacency_list)} cities"
