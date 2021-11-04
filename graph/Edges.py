from graph.Edge import Edge
from graph.Node import Node
from graph.Endpoint import Endpoint


class Edges:
    """
    This factory class produces edges of the types commonly used for Tetrad-style graphs.
    For each method in the class, one supplies a pair of nodes, and an edge is returned,
    connecting those nodes, of the specified type.  Methods are also included to help determine
    whether a specified edge falls into one of the types produced by this factory.

    It's entirely possible to produce edges of these types other than by using this factory.
    For randomUtil, an edge counts as a directed edge just in case it has one null endpoint and one arrow endpoint.
    Any edge which has one null endpoint and one arrow endpoint will do,
    whether or not this factory produced it.  These helper methods provide a uniform way of
    testing whether an edge is in fact, e.g., a directed edge (or any of the other types).
    """

    @classmethod
    def bidirected_edge(cls, node1: Node, node2: Node) -> Edge:
        """
        Constructs a new bidirected edge from node1 to node2 (<->)
        """
        return Edge(node1, node2, Endpoint.ARROW, Endpoint.ARROW)

    @classmethod
    def undirected_edge(cls, node1: Node, node2: Node) -> Edge:
        """
        Constructs a new undirected edge from nodeA to nodeB (--).
        """
        return Edge(node1, node2, Endpoint.TAIL, Endpoint.TAIL)

    @classmethod
    def nondirected_edge(cls, node1: Node, node2: Node) -> Edge:
        """
        Constructs a new nondirected edge from nodeA to nodeB (o-o).
        """
        return Edge(node1, node2, Endpoint.CIRCLE, Endpoint.CIRCLE)

    @classmethod
    def directed_edge(cls, node1: Node, node2: Node) -> Edge:
        """
        Constructs a new directed edge from nodeA to nodeB (-->).
        """
        return Edge(node1, node2, Endpoint.TAIL, Endpoint.ARROW)

    @classmethod
    def partially_oriented_edge(cls, node1: Node, node2: Node) -> Edge:
        """
        Constructs a new partially oriented edge from nodeA to nodeB (o->).
        """
        return Edge(node1, node2, Endpoint.CIRCLE, Endpoint.ARROW)

    @classmethod
    def is_undirected_edge(cls, edge: Edge) -> bool:
        """ Return true if the edge is an undirected edge (-)

        :param edge:
        :return:
        """
        return edge.get_endpoint1() == Endpoint.TAIL and edge.get_endpoint2() == Endpoint.TAIL

    @classmethod
    def traverse(cls, node: Node, edge: Edge) -> Node:
        """ Return the node opposite the given node along the given edge.

        :param node:
        :param edge:
        :return:
        """
        if not node:
            return None
        if node == edge.get_node1():
            return edge.get_node2()
        elif node == edge.get_node2():
            return edge.get_node1()
        return None

    @classmethod
    def traverse_directed(cls, node: Node, edge: Edge) -> Node:
        """
        For A -> B, given A, returns B
        For A <- B, given B, returns A
        otherwise returns null.
        """
        if node == edge.get_node1():
            if edge.get_endpoint1() == Endpoint.TAIL and edge.get_endpoint2() == Endpoint.ARROW:
                return edge.get_node2()
        elif node == edge.get_node2():
            if edge.get_endpoint1() == Endpoint.ARROW and edge.get_endpoint2() == Endpoint.TAIL:
                return edge.get_node1()
        return None

    @classmethod
    def traverse_semi_directed(cls, node: Node, edge: Edge) -> Node:
        """
        For A --* B or A o-* B, given A, returns B.
        """
        if node == edge.get_node1():
            if edge.get_endpoint1() == Endpoint.TAIL or edge.get_endpoint1() == Endpoint.CIRCLE:
                return edge.get_node2()
        elif node == edge.get_node2():
            if edge.get_endpoint2() == Endpoint.TAIL or edge.get_endpoint2() == Endpoint.CIRCLE:
                return edge.get_node1()
        return None

    @classmethod
    def is_directed_edge(cls, edge: Edge) -> bool:
        """
        return true if the given edge is a directed edge (-->)
        """
        if edge.get_endpoint1() == Endpoint.TAIL:
            if edge.get_endpoint2() == Endpoint.ARROW:
                return True
        elif edge.get_endpoint2() == Endpoint.TAIL:
            if edge.get_endpoint1() == Endpoint.ARROW:
                return True
        return False

    @classmethod
    def get_directed_edge_tail(cls, edge: Edge) -> Node:
        """
        For a directed edge, returns the node adjacent to the null endpoint.
        """
        if edge.get_endpoint2() == Endpoint.ARROW and edge.get_endpoint1() == Endpoint.TAIL:
            return edge.get_node1()
        if edge.get_endpoint1() == Endpoint.ARROW and edge.get_endpoint2() == Endpoint.TAIL:
            return edge.get_node2()
        raise ValueError(f"Not a directed edge: {edge}")

    @classmethod
    def get_directed_edge_head(cls, edge: Edge) -> Node:
        """
        For a directed edge, returns the node adjacent to the arrow endpoint.
        """
        if edge.get_endpoint1() == Endpoint.ARROW and edge.get_endpoint2() == Endpoint.TAIL:
            return edge.get_node1()
        if edge.get_endpoint2() == Endpoint.ARROW and edge.get_endpoint1() == Endpoint.TAIL:
            return edge.get_node2()
        raise ValueError(f"Not a directed edge: {edge}")

    @classmethod
    def pointing_left(cls, endpoint1: Endpoint, endpoint2: Endpoint) -> bool:
        """ Is the edge points from right to left?

        :param endpoint1:
        :param endpoint2:
        :return: returns True if the edge is pointing "left"
        """
        return endpoint1 == Endpoint.ARROW and (endpoint2 == Endpoint.TAIL or endpoint2 == Endpoint.CIRCLE)
