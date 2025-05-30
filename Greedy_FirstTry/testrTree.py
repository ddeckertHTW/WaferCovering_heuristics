from collections import defaultdict
from rtree import index

class CoordinateSystem:
    def __init__(self):
        self.coordinates_data = {}
        self.dependencies = defaultdict(set)
        self.observers = defaultdict(list)
        self.idx = index.Index()

    def add_coordinate(self, x, y, values, linked_coordinates=None):
        self.coordinates_data[(x, y)] = values
        if linked_coordinates:
            for coord in linked_coordinates:
                self.dependencies[(x, y)].add(coord)
                self.dependencies[coord].add((x, y))
        self.idx.insert(len(self.coordinates_data) - 1, (x, y, x, y))
        self.notify_observers((x, y))

    def update_coordinate(self, x, y, values):
        if (x, y) in self.coordinates_data:
            self.coordinates_data[(x, y)] = values
            self.notify_observers((x, y))

    def add_observer(self, coord, observer_func):
        self.observers[coord].append(observer_func)

    def notify_observers(self, coord):
        for observer in self.observers[coord]:
            observer(coord, self.coordinates_data[coord])
        for linked_coord in self.dependencies[coord]:
            for observer in self.observers[linked_coord]:
                observer(linked_coord, self.coordinates_data[linked_coord])

    def query_by_value(self, key, value):
        result = []
        for coord, values in self.coordinates_data.items():
            if values.get(key) == value:
                result.append(coord)
        return result

    def get_linked_coordinates(self, x, y):
        return self.dependencies.get((x, y), set())

# Example usage
def observer(coord, values):
    print(f"Coordinate {coord} updated with values {values}")

cs = CoordinateSystem()
cs.add_coordinate(1, 2, {'name': 'A', 'type': 'residential'}, [(2, 3)])
cs.add_coordinate(2, 3, {'name': 'B', 'type': 'commercial'})
cs.add_coordinate(4, 5, {'name': 'C', 'type': 'residential'}, [(1, 2)])

cs.add_observer((1, 2), observer)
cs.add_observer((2, 3), observer)

# Querying coordinates where type is 'residential'
residential_coords = cs.query_by_value('type', 'residential')
print("Residential Coordinates:", residential_coords)

# Update coordinate (1, 2)
cs.update_coordinate(1, 2, {'name': 'A', 'type': 'industrial'})
