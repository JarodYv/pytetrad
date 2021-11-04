from graph.Node import Node
from graph.NodeType import NodeType
from graph.NodeVariableType import NodeVariableType
from graph.NodeEqualityMode import NodeEqualityMode
from typing import Dict



class GraphNode(Node):
    """
    Implements a basic node in a graph--that is, a node that is not itself a variable.
    """

    def __init__(self, name: str = None, node: Node = None):
        self.name = "??"
        self.node_type = NodeType.MEASURED
        self.node_variable_type = NodeVariableType.DOMAIN
        self.center_x = -1
        self.center_y = -1
        self.attributes = Dict[str, object]()
        if not name:
            self.name = name
        if not node:
            self.name = node.get_name()
            self.node_type = node.get_node_type()
            self.center_x = node.get_center_x()
            self.center_y = node.get_center_y()

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        if not name:
            raise ValueError("Name must not be null.")
        self.name = name

    def get_node_type(self) -> NodeType:
        return self.node_type

    def set_node_type(self, node_type: NodeType):
        if not node_type:
            raise ValueError("Node type must not be null.")
        self.node_type = node_type

    def get_node_variable_type(self) -> NodeVariableType:
        return self.node_variable_type

    def set_node_variable_type(self, variable_type: NodeVariableType):
        self.node_variable_type = variable_type

    def get_center_x(self) -> int:
        return self.center_x

    def set_center_x(self, center_x: int):
        self.center_x = center_x

    def get_center_y(self) -> int:
        return self.center_y

    def set_center_y(self, center_y: int):
        self.center_y = center_y

    def set_center(self, center_x: int, center_y: int):
        self.center_x = center_x
        self.center_y = center_y

    def like(self, name: str):
        node = GraphNode(name)
        node.set_node_type(self.node_type)
        return node

    def get_all_attributes(self) -> Dict[str, object]:
        return self.attributes

    def get_attribute(self, key: str) -> object:
        return self.attributes.get(key, None)

    def remove_attribute(self, key: str):
        if key in self.attributes:
            del self.attributes[key]

    def add_attribute(self, key: str, value: object):
        self.attributes[key] = value

    def __hash__(self):
        if NodeEqualityMode.get_equality_type() == NodeEqualityMode.NodeEqualityType.OBJECT:
            return hash(self)
        if NodeEqualityMode.get_equality_type() == NodeEqualityMode.NodeEqualityType.NAME:
            return hash(self.name)

    def __eq__(self, other):
        if NodeEqualityMode.get_equality_type() == NodeEqualityMode.NodeEqualityType.OBJECT:
            return self == other
        if NodeEqualityMode.get_equality_type() == NodeEqualityMode.NodeEqualityType.NAME:
            return isinstance(other, GraphNode) and other.get_name() == self.name
