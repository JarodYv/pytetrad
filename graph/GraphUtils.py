from Graph import Graph
from EdgeListGraph import EdgeListGraph
from Node import Node
from Edge import Edge
from Edges import Edges
from Endpoint import Endpoint
from typing import List


class GraphUtils:
    @classmethod
    def path_string(cls, path: List[Node], graph: Graph) -> str:
        conditioning_vars = List[Node]()
        return cls.path_string_with_condition(graph, path, conditioning_vars)

    @classmethod
    def path_string_with_condition(cls, graph: Graph, path: List[Node], conditioning_vars: List[Node]) -> str:
        if len(path) < 2:
            return "NO PATH"
        first_node = path[0]
        path_string: str = str(first_node)
        if first_node in conditioning_vars:
            path_string += "(C)"
        for i in range(1, len(path)):
            n0: Node = path[i - 1]
            n1: Node = path[i]
            edge: Edge = graph.get_edge(n0, n1)
            if not edge:
                path_string += "(-)"
            else:
                endpoint0: Endpoint = edge.get_proximal_endpoint(n0)
                endpoint1: Endpoint = edge.get_proximal_endpoint(n1)
                if endpoint0 == Endpoint.ARROW:
                    path_string += "<"
                elif endpoint0 == Endpoint.TAIL:
                    path_string += "-"
                elif endpoint0 == Endpoint.CIRCLE:
                    path_string += "o"
                path_string += "-"
                if endpoint1 == Endpoint.ARROW:
                    path_string += ">"
                elif endpoint1 == Endpoint.TAIL:
                    path_string += "-"
                elif endpoint1 == Endpoint.CIRCLE:
                    path_string += "o"
                path_string += str(n1)
                if n1 in conditioning_vars:
                    path_string += "(C)"
        return path_string

    @classmethod
    def replace_node(cls, original_graph: Graph, new_variables: List[Node]) -> Graph:
        """ Converts the given graph, <code>originalGraph</code>, to use the new variables
        (with the same names as the old).

        :param original_graph: The graph to be converted.
        :param new_variables: The new variables to use, with the same names as the old ones.
        :return: A new, converted, graph
        """
        reference = EdgeListGraph(new_variables)
        converted_graph = EdgeListGraph(new_variables)
        if not original_graph:
            return Node
        for edge in original_graph.get_graph_edges():
            node1 = reference.get_node(edge.get_node1().get_name())
            node2 = reference.get_node(edge.get_node2().get_name())
            if not node1:
                node1 = edge.get_node1()

            if not node2:
                node2 = edge.get_node2()

            if not node1:
                raise ValueError(f"Couldn't find a node by the name {edge.get_node1().get_name()}")

            if not node2:
                raise ValueError(f"Couldn't find a node by the name {edge.get_node2().get_name()}")

            if not converted_graph.contains_node(node1):
                converted_graph.add_node(node1)

            if not converted_graph.contains_node(node2):
                converted_graph.add_node(node2)

            endpoint1 = edge.get_endpoint1()
            endpoint2 = edge.get_endpoint2()
            new_edge = Edge(node1, node2, endpoint1, endpoint2)
            converted_graph.add_edge(new_edge)

        for triple in original_graph.get_underlines():
            converted_graph.add_underline_triple(converted_graph.get_node(triple.get_x().get_name()),
                                                 converted_graph.get_node(triple.get_y().get_name()),
                                                 converted_graph.get_node(triple.get_z().get_name()))

        for triple in original_graph.get_dotted_underlines():
            converted_graph.add_dotted_underline_triple(converted_graph.get_node(triple.get_x().get_name()),
                                                        converted_graph.get_node(triple.get_y().get_name()),
                                                        converted_graph.get_node(triple.get_z().get_name()))

        for triple in original_graph.get_ambiguous_triples():
            converted_graph.add_ambiguous_triple(converted_graph.get_node(triple.get_x().get_name()),
                                                 converted_graph.get_node(triple.get_y().get_name()),
                                                 converted_graph.get_node(triple.get_z().get_name()))

        return converted_graph

    @classmethod
    def as_list(cls, indices: List[int], nodes: List[Node]) -> List[Node]:
        """ Constructs a list of nodes from the given <code>nodes</code> list at the given indices in that list.

        :param indices: The indices of the desired nodes in <code>nodes</code>.
        :param nodes: The list of nodes from which we select a sublist.
        :return: The sublist selected
        """
        _list = List[Node]()
        for i in indices:
            _list.append(nodes[i])
        return _list

    @classmethod
    def exists_directed_path_from_to(cls, node1: Node, node2: Node, graph: Graph) -> bool:
        return cls.exists_directed_path_visit(node1, node2, List[Node](), -1, graph)

    @classmethod
    def exists_directed_path_visit(cls, node1: Node, node2: Node, path: List[Node], depth: int, graph: Graph):
        path.append(node1)
        depth = 0x7fffffff if depth == -1 else depth
        if len(path) >= depth:
            return False
        for edge in graph.get_node_edges(node1):
            child = Edges.traverse_directed(node1, edge)
            if len(graph.get_connecting_edges(node1, child)) == 2:
                return True
            if not child:
                continue
            if child == node2:
                return True
            if child in path:
                continue
            if cls.exists_directed_path_visit(child, node2, path, depth, graph):
                return True
        path.remove(node1)
        return False

    @classmethod
    def is_d_connected_to(cls, x: Node, y: Node, z: List[Node], graph: Graph) -> bool:
        return cls._is_d_connected_to_1(x, y, z, graph)

    @classmethod
    def _is_d_connected_to_1(cls, x: Node, y: Node, z: List[Node], graph: Graph) -> bool:
        pass
