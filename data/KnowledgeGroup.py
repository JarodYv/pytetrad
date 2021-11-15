from typing import Set, List
from util.StringUtils import compare_set

from data.KnowledgeEdge import KnowledgeEdge

REQUIRED = 1
FORBIDDEN = 2


class KnowledgeGroup:
    def __int__(self, k_type: int):
        if k_type != REQUIRED and k_type != FORBIDDEN:
            raise ValueError("The given type needs to be either REQUIRED or FORBIDDEN")
        self.k_type = k_type
        self.k_from = Set[str]()
        self.k_to = Set[str]()

    def __init__(self, k_type: int, k_from: Set[str], k_to: Set[str]):
        if k_type != REQUIRED and k_type != FORBIDDEN:
            raise ValueError("The given type needs to be either REQUIRED or FORBIDDEN")

        if not k_from:
            raise ValueError("The from set must not be null")

        if not k_to:
            raise ValueError("The to set must not be null")

        if k_from & k_to:
            raise ValueError("The from and to sets must not intersect")

        self.k_type = k_type
        self.k_from = k_from
        self.k_to = k_to

    def get_type(self) -> int:
        return self.k_type

    def is_empty(self) -> bool:
        return len(self.k_from) == 0 or len(self.k_to) == 0

    def get_from_variables(self) -> Set[str]:
        return self.k_from

    def get_to_variables(self) -> Set[str]:
        return self.k_to

    def get_edges(self) -> List[KnowledgeEdge]:
        edges = List[str]()
        for f in self.k_from:
            for t in self.k_to:
                edges.append(KnowledgeEdge(f, t))
        return edges

    def contains_edge(self, edge: KnowledgeEdge) -> bool:
        return edge.get_from() in self.k_from and edge.get_to() in self.k_to

    def __hash__(self):
        hash_code = 37
        hash_code += 17 * hash(self.k_from) + 37
        hash_code += 17 * hash(self.k_to) + 37
        hash_code += 17 * hash(self.k_type) + 37
        return hash_code

    def __eq__(self, other):
        if other == self:
            return True
        if not type(other) == type(self):
            return False
        return self.k_type == other.k_type and compare_set(self.k_from, other.k_from) and compare_set(
            self.k_to, other.k_to)

    def is_conflict(self, group):
        if not group:
            raise ValueError("the compared group must not be null")
        if not type(group) == type(self):
            raise ValueError("the arg is not a KnowledgeGroup")
        if not self.k_type == group.k_type:
            return (self.k_from & group.k_from) and (self.k_to & group.k_to)
        return False
