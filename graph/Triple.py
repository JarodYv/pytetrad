from graph.Node import Node
from typing import List
from graph import Graph


class Triple:
    """
    Stores a triple (x, y, z) of nodes.
    Note that (x, y, z) = (z, y, x).
    Useful for marking graphs.
    """

    def __init__(self, x: Node, y: Node, z: Node):
        if not x or not y or not z:
            raise ValueError
        self.x = x
        self.y = y
        self.z = z

    def get_x(self) -> Node:
        return self.x

    def get_y(self) -> Node:
        return self.y

    def get_z(self) -> Node:
        return self.z

    def __hash__(self):
        hash_code = 17
        hash_code += 19 * hash(self.x) * hash(self.z)
        hash_code += 23 * hash(self.y)
        return hash_code

    def __eq__(self, other):
        if not other or not isinstance(other, Triple):
            return False
        return self.x == other.x and self.y == other.y and self.z == other.z or self.x == other.z and self.y == other.y and self.z == other.x

    def __str__(self):
        return f"<{self.x}, {self.y}, {self.z}>"

    def along_path_in(self, graph: Graph) -> bool:
        return graph.is_adjacent_to(self.x, self.y) and graph.is_adjacent_to(self.y, self.z) and self.x != self.z

    @classmethod
    def path_string(cls, graph: Graph, x: Node, y: Node, z: Node):
        from graph.GraphUtils import GraphUtils
        path: List[Node] = [x, y, z]
        return GraphUtils.path_string(path, graph)
