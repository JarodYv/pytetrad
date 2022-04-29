from graph.EdgeProperty import EdgeProperty
from graph.Edges import Edges
from graph.Node import Node
from util import Color
from typing import List, Optional
from graph.EdgeTypeProbability import EdgeTypeProbability
from graph.Endpoint import Endpoint
from graph.NodeEqualityMode import NodeEqualityMode


class Edge:
    """
    Represents an edge node1 *-# node2 where * and # are endpoints of type
    Endpoint--that is, Endpoint.TAIL, Endpoint.ARROW, or Endpoint.CIRCLE.
    Note that because speed is of the essence, and Edge cannot be compared to an
    object of any other type; this will throw an exception.
    """

    def __init__(self, node1: Node, node2: Node, endpoint1: Endpoint, endpoint2: Endpoint):
        """ Constructs a new edge by specifying the nodes it connects and the endpoint types.

        :param node1: the first node
        :param node2: the second node
        :param endpoint1: the endpoint at the first node
        :param endpoint2: the endpoint at the second node
        """
        if node1 is None or node2 is None:
            raise TypeError('Nodes must not be of NoneType. node1 = ' + str(node1) + ' node2 = ' + str(node2))

        if endpoint1 is None or endpoint2 is None:
            raise TypeError(
                'Endpoints must not be of NoneType. endpoint1 = ' + str(endpoint1) + ' endpoint2 = ' + str(endpoint2))

        # assign nodes and endpoints; if the edge points left, flip it
        if Edges.pointing_left(endpoint1, endpoint2):
            self.node1: Node = node2
            self.node2: Node = node1
            self.endpoint1: Endpoint = endpoint2
            self.endpoint2: Endpoint = endpoint1
        else:
            self.node1: Node = node1
            self.node2: Node = node2
            self.endpoint1: Endpoint = endpoint1
            self.endpoint2: Endpoint = endpoint2

        self.properties: List[EdgeProperty] = []
        self.edge_type_probabilities: List[EdgeTypeProbability] = []
        self.bold: bool = False
        self.color: Color = None

    def get_node1(self) -> Node:
        """ return the A node

        """
        return self.node1

    def get_node2(self) -> Node:
        """ return the B node

        """
        return self.node2

    def get_endpoint1(self) -> Endpoint:
        """ return the endpoint of the edge at the A node

        """
        return self.endpoint1

    def get_endpoint2(self) -> Endpoint:
        """ return the endpoint of the edge at the B node

        """
        return self.endpoint2

    def set_endpoint1(self, endpoint: Endpoint):
        """ set the endpoint of the edge at the A node

        """
        self.endpoint1 = endpoint

    def set_endpoint2(self, endpoint: Endpoint):
        """ set the endpoint of the edge at the B node

        """
        self.endpoint2 = endpoint

    def is_null(self) -> bool:
        return self.endpoint1 == Endpoint.NULL and self.endpoint2 == Endpoint.NULL

    def get_line_color(self) -> Color:
        return self.color

    def set_line_color(self, color: Color):
        self.color = color

    def is_bold(self) -> bool:
        return self.bold

    def set_bold(self, bold: bool):
        self.bold = bold

    def add_property(self, _property: EdgeProperty):
        if not self.properties:
            self.properties = []
        if _property not in self.properties:
            self.properties.append(_property)

    def remove_property(self, _property: EdgeProperty):
        if _property in self.properties:
            self.properties.remove(_property)

    def get_properties(self) -> List[EdgeProperty]:
        return self.properties

    def add_edge_type_probability(self, _property: EdgeTypeProbability):
        if not self.edge_type_probabilities:
            self.edge_type_probabilities = []
        if _property not in self.edge_type_probabilities:
            self.edge_type_probabilities.append(_property)

    def remove_edge_type_probability(self, _property: EdgeTypeProbability):
        if _property in self.edge_type_probabilities:
            self.edge_type_probabilities.remove(_property)

    def get_edge_type_probabilities(self) -> List[EdgeTypeProbability]:
        return self.edge_type_probabilities

    def get_proximal_endpoint(self, node: Node) -> Optional[Endpoint]:
        """ return the endpoint nearest to the given node;
        if the given node is not along the edge, returns NoneType

        """
        if self.node1 is node:
            return self.endpoint1
        elif self.node2 is node:
            return self.endpoint2
        else:
            return None

    def get_distal_endpoint(self, node: Node) -> Optional[Endpoint]:
        """ return the endpoint furthest from the given node;
        if the given node is not along the edge, returns NoneType

        """
        if self.node1 is node:
            return self.endpoint2
        elif self.node2 is node:
            return self.endpoint1
        else:
            return None

    def get_distal_node(self, node: Node) -> Optional[Node]:
        """ traverses the edge in an undirected fashion:
        given one node along the edge, returns the node at the opposite end of the edge

        """
        if self.node1 is node:
            return self.node2
        elif self.node2 is node:
            return self.node1
        else:
            return None

    def is_directed(self) -> bool:
        """
        return true just in case this edge is directed.
        """
        return Edges.is_directed_edge(self)

    def points_towards(self, node: Node) -> bool:
        """ check if the edge is pointing toward the given node
        There are 2 cases: x --> node or x o--> node.

        :param node: given node
        :return:
        """
        proximal = self.get_proximal_endpoint(node)
        if not proximal:
            return False
        distal = self.get_distal_endpoint(node)
        if not distal:
            return False
        return proximal == Endpoint.ARROW and (distal == Endpoint.TAIL or distal == Endpoint.CIRCLE)

    def __eq__(self, other):
        if not other or not isinstance(other, Edge):
            return False
        if self == other:
            return True
        if NodeEqualityMode.get_equality_type() == NodeEqualityMode.NodeEqualityType.OBJECT:
            if self.node1 == other.node1 and self.node2 == other.node2:
                equal = self.endpoint1 == other.endpoint1 and self.endpoint2 == other.endpoint2
            else:
                equal = self.node1 == other.node2 and self.node2 == self.node1 and self.endpoint1 == other.endpoint2 and self.endpoint2 == other.endpoint1
            return equal
        elif NodeEqualityMode.get_equality_type() == NodeEqualityMode.NodeEqualityType.NAME:
            if self.node1.get_name() == other.node1.get_name() and self.node2.get_name() == other.node2.get_name():
                equal = self.endpoint1 == other.endpoint1 and self.endpoint2 == other.endpoint2
            else:
                equal = self.node1.get_name() == other.node2.get_name() and self.node2.get_name() == self.node1.get_name() and self.endpoint1 == other.endpoint2 and self.endpoint2 == other.endpoint1
            return equal
        else:
            raise ValueError()

    def __hash__(self):
        return hash(self.node1) + hash(self.node2)

    def __str__(self):
        node1 = self.get_node1()
        node2 = self.get_node2()

        endpoint1 = self.get_endpoint1()
        endpoint2 = self.get_endpoint2()

        end1 = ""
        if endpoint1 is Endpoint.TAIL:
            end1 = "-"
        elif endpoint1 is Endpoint.ARROW:
            end1 = "<"
        elif endpoint1 is Endpoint.CIRCLE:
            end1 = "o"

        end2 = ""
        if endpoint2 is Endpoint.TAIL:
            end2 = "-"
        elif endpoint2 is Endpoint.ARROW:
            end2 = ">"
        elif endpoint2 is Endpoint.CIRCLE:
            end2 = "o"
        s = f"{node1.get_name()} {end1}-{end2} {node2.get_name()}"
        # Bootstrapping edge type distribution
        if self.edge_type_probabilities:
            n1 = self.node1.get_name()
            n2 = self.node2.get_name()
            for p in self.edge_type_probabilities:
                prob = p.get_probability()
                if prob > 0:
                    edge_type = p.get_edge_type()
                    if edge_type == EdgeTypeProbability.EdgeType.nil:
                        _type = "no edge"
                    elif edge_type == EdgeTypeProbability.EdgeType.ta:
                        _type = "-->"
                    elif edge_type == EdgeTypeProbability.EdgeType.at:
                        _type = "<--"
                    elif edge_type == EdgeTypeProbability.EdgeType.ca:
                        _type = "o->"
                    elif edge_type == EdgeTypeProbability.EdgeType.ac:
                        _type = "<-o"
                    elif edge_type == EdgeTypeProbability.EdgeType.cc:
                        _type = "o-o"
                    elif edge_type == EdgeTypeProbability.EdgeType.aa:
                        _type = "<->"
                    elif edge_type == EdgeTypeProbability.EdgeType.tt:
                        _type = "---"
                    else:
                        _type = ""
                    if not edge_type == EdgeTypeProbability.EdgeType.nil:
                        _type = n1 + " " + _type + " " + n2
                    properties = p.get_properties()
                    if properties:
                        for _p in properties:
                            _type += " %s" % _p
                    s += ("[%s]: %.4f;" % (_type, p.get_probability()))
        if self.properties:
            for p in self.properties:
                s += (" %s" % p)
        return s

    def pointing_left(self) -> bool:
        """ Is the edge points from right to left?

        :return: returns True if the edge is pointing "left"
        """
        return self.endpoint1 == Endpoint.ARROW and (
                self.endpoint2 == Endpoint.TAIL or self.endpoint2 == Endpoint.CIRCLE)
