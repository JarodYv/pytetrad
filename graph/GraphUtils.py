from graph.Graph import Graph
from graph.Node import Node
from graph.Edge import Edge
from graph.Edges import Edges
from graph.Triple import Triple
from graph.Endpoint import Endpoint
from graph.EdgeProperty import EdgeProperty
from typing import List, Set, Dict


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
        from graph.EdgeListGraph import EdgeListGraph
        reference = EdgeListGraph(nodes=new_variables)
        converted_graph = EdgeListGraph(nodes=new_variables)
        if not original_graph:
            return None
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

    @classmethod
    def add_pag_coloring(cls, graph: Graph):
        for edge in graph.get_graph_edges():
            if not Edges.is_directed_edge(edge):
                continue
            x = Edges.get_directed_edge_tail(edge)
            y = Edges.get_directed_edge_head(edge)

            graph.remove_edge(edge)
            graph.add_edge(edge)

            xy_edge = graph.get_edge(x, y)
            graph.remove_edge(xy_edge)

            if cls.exists_semi_directed_path(x, y, graph):
                edge.add_property(EdgeProperty.pd)
            else:
                edge.add_property(EdgeProperty.dd)  # green

            graph.add_edge(xy_edge)
            if graph.def_visible(edge):
                edge.add_property(EdgeProperty.nl)  # bold
            else:
                edge.add_property(EdgeProperty.pl)

    @classmethod
    def exists_semi_directed_path(cls, node1: Node, node2: Node, graph: Graph) -> bool:
        q = list()
        v = set()
        for n in graph.get_adjacent_nodes(node1):
            edge = graph.get_edge(node1, n)
            c = Edges.traverse_semi_directed(node1, edge)
            if not c:
                continue
            if c not in v:
                v.add(c)
                q.append(c)
        while len(q) > 0:
            t = q.pop(0)
            if t == node2:
                return True
            for n in graph.get_adjacent_nodes(t):
                edge = graph.get_edge(t, n)
                c = Edges.traverse_semi_directed(t, edge)
                if not c:
                    continue
                if c not in v:
                    v.add(c)
                    q.append(c)
        return False

    @classmethod
    def graph_nodes2text(cls, graph: Graph, title: str, delimiter: str) -> str:
        fmt = list()
        if title and len(title):
            fmt.append("%s\n" % title)
        nodes = graph.get_nodes()
        size = len(nodes) if nodes else 0
        count = 0
        for node in nodes:
            count += 1
            fmt.append(f"%s%s" % (node.get_name(), delimiter if count < size else ""))

        return "".join(fmt)

    @classmethod
    def graph_edges2text(cls, graph: Graph, title: str) -> str:
        fmt = list()
        if title and len(title):
            fmt.append("%s\n" % title)
        edges = list(graph.get_graph_edges())
        # Edges.sortEdges(edges)
        size = len(edges)
        count = 0
        for edge in edges:
            count += 1
            # We will print edge's properties in the edge (via toString() function) level.
            # List<Edge.Property> properties = edge.getProperties();
            if count < size:
                fmt.append("%d. %s\n" % (count, edge))
            else:
                fmt.append("%d. %s" % (count, edge))
        return "".join(fmt)

    @classmethod
    def graph_attributes2text(cls, graph: Graph, title: str) -> str:
        attributes = graph.get_all_attributes()
        if attributes and len(attributes) > 0:
            fmt = list()
            if title and len(title):
                fmt.append("%s\n" % title)
            for key in attributes:
                value = attributes[key]
                fmt.append("%s: %s\n" % (key, value))
            return "".join(fmt)
        return ""

    @classmethod
    def graph_node_attributes2text(cls, graph: Graph, title: str, delimiter: str) -> str:
        nodes = graph.get_nodes()
        graph_node_attributes = Dict[str, Dict[str, object]]()
        for node in nodes:
            attributes = node.get_all_attributes()
            if attributes and len(attributes) > 0:
                for key in attributes:
                    value = attributes[key]
                    if key in graph_node_attributes:
                        node_attributes = graph_node_attributes.get(key)
                    else:
                        node_attributes = {}
                    node_attributes[node.get_name()] = value
                    graph_node_attributes[key] = node_attributes

        if len(graph_node_attributes) > 0:
            fmt = list()
            if title and len(title) > 0:
                fmt.append("%s" % title)
            for key in graph_node_attributes:
                node_attributes = graph_node_attributes[key]
                size = len(node_attributes)
                count = 0
                fmt.append("\n%s: [" % key)
                for node_name in node_attributes:
                    count += 1
                    value = node_attributes[node_name]
                    fmt.append("%s: %s%s" % (node_name, value, delimiter if count < size else ""))
                fmt.append("]")
            return "".join(fmt)
        return ""

    @classmethod
    def triples2text(cls, triples: Set[Triple], title: str) -> str:
        fmt = list()
        if title and len(title) > 0:
            fmt.append("%s\n" % title)
        size = len(triples) if triples else 0
        if size > 0:
            count = 0
            for triple in triples:
                count += 1
                fmt.append("%s\n" % triple if count < size else "%s" % triple)

        return "".join(fmt)

    @classmethod
    def graph2text(cls, graph: Graph):
        # add edge properties relating to edge coloring of PAGs
        if graph.is_pag():
            cls.add_pag_coloring(graph)
        fmt = list()
        fmt.append("%s\n\n" % cls.graph_nodes2text(graph, "Graph Nodes:", ";"))
        fmt.append("%s\n" % cls.graph_edges2text(graph, "Graph Edges:"))

        # Graph Attributes
        graph_attributes = cls.graph_attributes2text(graph, "Graph Attributes:")
        if graph_attributes:
            fmt.append("%s\n" % graph_attributes)

        # Nodes Attributes
        graph_node_attributes = cls.graph_node_attributes2text(graph, "Graph Node Attributes:", ";")
        if graph_node_attributes:
            fmt.append("%s\n" % graph_node_attributes)

        ambiguous_triples = graph.get_ambiguous_triples()
        if not ambiguous_triples and len(ambiguous_triples) > 0:
            fmt.append("\n\n%s" % cls.triples2text(ambiguous_triples,
                                                   "Ambiguous triples (i.e. list of triples for which there is "
                                                   "ambiguous data about whether they are colliders or not):"))

        underline_triples = graph.get_underlines()
        if not underline_triples and len(underline_triples) > 0:
            fmt.append("\n\n%s" % cls.triples2text(underline_triples, "Underline triples:"))

        dotted_underline_triples = graph.get_dotted_underlines()
        if not dotted_underline_triples and len(dotted_underline_triples) > 0:
            fmt.append("\n\n%s" % cls.triples2text(dotted_underline_triples, "Dotted underline triples:"))

        return "".join(fmt)
