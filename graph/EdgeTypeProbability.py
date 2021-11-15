from enum import Enum
from typing import List
from graph.EdgeProperty import EdgeProperty


class EdgeTypeProbability:
    class EdgeType(Enum):
        nil = 1
        ta = 2  # tail - arrow
        at = 3  # arrow - tail
        ca = 4  # circle - arrow
        ac = 5  # arrow - circle
        cc = 6  # circle - circle
        aa = 7  # arrow - arrow
        tt = 8  # tail - tail

    def __init__(self, edge_type: EdgeType, properties: List[EdgeProperty], probability: float):
        self.edge_type = edge_type
        self.properties = properties
        self.probability = probability

    def get_edge_type(self) -> EdgeType:
        return self.edge_type

    def set_edge_type(self, _type: EdgeType):
        self.edge_type = _type

    def add_property(self, _property: EdgeProperty):
        if not self.properties:
            self.properties = []
        if _property not in self.properties:
            self.properties.append(_property)

    def remove_property(self, _property: EdgeProperty):
        if self.properties and _property in self.properties:
            self.properties.remove(_property)

    def get_properties(self) -> List[EdgeProperty]:
        return self.properties

    def get_probability(self) -> float:
        return self.probability

    def set_probability(self, _probability: float):
        self.probability = _probability
