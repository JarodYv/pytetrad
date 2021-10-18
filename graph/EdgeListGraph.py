import itertools

from Graph import Graph
from GraphUtils import GraphUtils
from Node import Node
from typing import List, Dict, Set
from Edges import Edges
from Edge import Edge
from Endpoint import Endpoint
from Triple import Triple
from NodeType import NodeType
from TimeLagGraph import TimeLagGraph


class EdgeListGraph(Graph):
    """
    Stores a graph a list of lists of edges adjacent to each node in the graph,
    with an additional list storing all of the edges in the graph. The edges are
    of the form N1 *-# N2. Multiple edges may be added per node pair to this
    graph, with the caveat that all edges of the form N1 *-# N2 will be
    considered equal. For example, if the edge X --> Y is added to the graph,
    another edge X --> Y may not be added, although an edge Y --> X may be added.
    Edges from nodes to themselves may also be added.
    """

    def __init__(self, graph: Graph, nodes: List[Node]):
        self.edge_lists = Dict[Node, List[Edge]]()
        self.nodes = List[Node]()
        self.edges_set = Set[Node]()
        self.names_hash = Dict[str, Node]()
        self.pattern = False
        self.pag = False
        self.stuff_removed_since_last_triple_access = False
        self.attributes = Dict[str, object]()
        self.ambiguous_triples = Set[Triple]()
        self.underline_triples = Set[Triple]()
        self.dotted_underline_triples = Set[Triple]()
        self.highlighted_edges = Set[Edge]()
        self.ancestors = None
        if graph:
            self.transfer_nodes_and_edges(graph)
            self.transfer_attributes(graph)
            self.ambiguous_triples = graph.get_ambiguous_triples()
            self.dotted_underline_triples = graph.get_dotted_underlines()
            self.underline_triples = graph.get_underlines()
            for edge in graph.get_graph_edges():
                if graph.is_high_lighted(edge):
                    self.set_high_lighted(edge, True)
            for node in self.nodes:
                self.names_hash[node.get_name()] = node
            self.pag = graph.is_pag()
            self.pattern = graph.is_pattern()
        if nodes:
            for node in nodes:
                if not self.add_node(node):
                    raise ValueError
                self.names_hash[node.get_name()] = node

    def add_bidirected_edge(self, node1: Node, node2: Node) -> bool:
        """
        Adds a bidirected edge to the graph from node A to node B.
        """
        return self.add_edge(Edges.bidirected_edge(node1, node2))

    def add_directed_edge(self, node1: Node, node2: Node) -> bool:
        """
        Adds a directed edge to the graph from node A to node B.
        """
        return self.add_edge(Edges.directed_edge(node1, node2))

    def add_undirected_edge(self, node1: Node, node2: Node) -> bool:
        """
        Adds an undirected edge to the graph from node A to node B.
        """
        return self.add_edge(Edges.undirected_edge(node1, node2))

    def add_nondirected_edge(self, node1: Node, node2: Node) -> bool:
        """
        Adds a nondirected edge to the graph from node A to node B.
        """
        return self.add_edge(Edges.nondirected_edge(node1, node2))

    def add_partially_oriented_edge(self, node1: Node, node2: Node) -> bool:
        """
        Adds a partially oriented edge to the graph from node A to node B.
        """
        return self.add_edge(Edges.partially_oriented_edge(node1, node2))

    def add_edge(self, edge: Edge) -> bool:
        if not edge:
            raise ValueError()
        edge_list1 = self.edge_lists.get(edge.get_node1())
        edge_list2 = self.edge_lists.get(edge.get_node2())
        if edge in edge_list1:
            return True
        edge_list1.append(edge)
        edge_list2.append(edge)
        self.edges_set.add(edge)

        if Edges.is_directed_edge(edge):
            node = Edges.get_directed_edge_tail(edge)
            if node.get_node_type() == NodeType.ERROR:
                pass
        self.ancestors = None
        return True

    def add_node(self, node: Node) -> bool:
        """
        Adds a node to the graph. Precondition: The proposed name of the node
        cannot already be used by any other node in the same graph.
        """
        if not node:
            raise ValueError()
        if node in self.nodes:
            return True
        if self.get_node(node.get_name()):
            if node in self.nodes:
                self.names_hash[node.get_name()] = node

        if node in self.edge_lists.keys():
            return False
        self.edge_lists[node] = List[Edge]()
        self.nodes.append(node)
        self.names_hash[node.get_name()] = node
        if node.get_node_type() == NodeType.ERROR:
            pass
        return True

    def clear(self):
        edges = self.get_graph_edges()
        edges.clear()
        self.nodes.clear()
        self.names_hash.clear()
        self.edge_lists.clear()

    def contains_edge(self, edge: Edge) -> bool:
        return edge in self.edges_set

    def contains_node(self, node: Node) -> bool:
        return node in self.nodes

    def exists_directed_cycle(self) -> bool:
        for node in self.get_nodes():
            if self.exists_directed_path_from_to(node, node):
                return True
        return False

    def exists_directed_path_from_to(self, node1: Node, node2: Node) -> bool:
        """
        Return true if there is a directed path from node1 to node2.
        """
        Q = List[Node]()
        V = Set[Node]()
        Q.append(node1)
        V.add(node1)
        started = False
        while len(Q) > 0:
            t = Q.pop(0)
            if started and t == node2:
                return True
            started = True
            for c in self.get_children(t):
                if c not in V:
                    V.add(c)
                    Q.append(c)

    def exists_undirected_path_from_to(self, node1: Node, node2: Node) -> bool:
        return self.exists_undirected_path_visit(node1, node2, Set[Node]())

    def exists_undirected_path_visit(self, node1: Node, node2: Node, path: Set[Node]) -> bool:
        """
        Return true if there is a directed path from node1 to node2.
        """
        path.add(node1)
        for edge in self.get_node_edges(node1):
            child = Edges.traverse(node1, edge)
            if not child:
                continue
            if child == node2:
                return True
            if child in path:
                continue
            if self.exists_undirected_path_visit(child, node2, path):
                return True
        path.remove(node1)
        return False

    def exists_semidirected_path_from_to(self, node1: Node, nodes: List[Node]) -> bool:
        return self.exists_semidirected_path_visit(node1, nodes, List[Node]())

    def exists_semidirected_path_visit(self, node1: Node, nodes: List[Node], path: List[Node]) -> bool:
        path.append(node1)
        for edge in self.get_node_edges(node1):
            child = Edges.traverse_semi_directed(node1, edge)
            if not child:
                continue
            if child in nodes:
                return True
            if child in path:
                continue
            if self.exists_semidirected_path_visit(child, nodes, path):
                return True
        path.remove(node1)
        return False

    def exists_inducing_path(self, node1: Node, node2: Node) -> bool:
        """
        Determines whether an inducing path exists between node1 and node2,
        given a set O of observed nodes and a set sem of conditioned nodes.
        """
        return node1 == node2 or GraphUtils.exists_directed_path_from_to(node1, node2, self)

    def exists_trek(self, node1: Node, node2: Node) -> bool:
        """
         Determines whether a trek exists between two nodes in the graph.
         A trek exists if there is a directed path between the two nodes or else,
         for some third node in the graph, there is a path to each of the two nodes in question.
        """
        for node in self.get_nodes():
            if self.is_ancestor_of(node, node1) and self.is_ancestor_of(node, node2):
                return True
        return False

    def __eq__(self, other):
        pass

    def fully_connect(self, endpoint: Endpoint):
        """
        Resets the graph so that it is fully connects it using #-# edges, where # is the given endpoint.
        """
        self.edges_set.clear()
        self.edge_lists.clear()
        for node in self.nodes:
            self.edge_lists[node] = List[Edge]()

        combinations = itertools.combinations(self.nodes, 2)
        for combination in combinations:
            node1 = combination[0]
            node2 = combination[1]
            edge = Edge(node1, node2, endpoint, endpoint)
            self.add_edge(edge)

    def reorient_all_with(self, endpoint: Endpoint):
        for edge in list(self.edges_set):
            a = edge.get_node1()
            b = edge.get_node2()
            self.set_endpoint(a, b, endpoint)
            self.set_endpoint(b, a, endpoint)

    def get_adjacent_nodes(self, node: Node) -> List[Node]:
        """ the set of nodes adjacent to the given node. If there are multiple edges between X and Y,
        Y will show up twice in the list of adjacencies for X, for optimality; simply create a list
        an and array from these to eliminate the duplication.
        """
        edges = self.edge_lists.get(node)
        adj = List[Node]()
        for edge in edges:
            if not edge:
                continue
            z = edge.get_distal_node(node)
            if z not in adj:
                adj.append(z)
        return adj

    def get_ancestors(self, nodes: List[Node]) -> List[Node]:
        pass

    def get_children(self, node: Node) -> List[Node]:
        pass

    def get_connectivity(self) -> int:
        pass

    def get_descendants(self, nodes: List[Node]) -> List[Node]:
        pass

    def get_edge(self, node1: Node, node2: Node) -> Edge:
        pass

    def get_directed_edge(self, node1: Node, node2: Node) -> Edge:
        pass

    def get_node_edges(self, node: Node) -> List[Edge]:
        pass

    def get_connecting_edges(self, node1: Node, node2: Node) -> List[Edge]:
        """
        he edges connecting node1 and node2.
        """
        edges = self.edge_lists.get(node1)
        if not edges:
            return List[Node]()
        _edges = List[Node]()
        for edge in edges:
            if edge.get_distal_node(node1) == node2:
                _edges.append(edge)
        return _edges

    def get_graph_edges(self) -> Set[Edge]:
        return Set[Edge](self.edges_set)

    def get_endpoint(self, node1: Node, node2: Node) -> Endpoint:
        """
        return the endpoint along the edge from node to node2 at the node2 end.
        """
        edges = self.get_node_edges(node2)
        for edge in edges:
            if edge.get_distal_node(node2) == node1:
                return edge.get_proximal_endpoint(node2)
        return None

    def get_in_degree(self, node: Node) -> int:
        return len(self.get_parents(node))

    def get_out_degree(self, node: Node) -> int:
        return len(self.get_children(node))

    def get_degree(self, node: Node) -> int:
        return len(self.edge_lists.get(node))

    def get_node(self, name: str) -> Node:
        """
        return the node with the given name, or null if no such node exists.
        """
        return self.names_hash.get(name, None)

    def get_nodes(self) -> List[Node]:
        return list(self.nodes)

    def get_node_names(self) -> List[str]:
        names = List[str]()
        for node in self.get_nodes():
            names.append(node.get_name())
        return names

    def get_num_edges(self) -> int:
        """
        return the number of edges in the (entire) graph.
        """
        return len(self.edges_set)

    def get_num_connected_edges(self, node: Node) -> int:
        """
        return the number of edges connected to a particular node in the graph.
        """
        edges = self.edge_lists.get(node)
        return len(edges) if edges else 0

    def get_num_nodes(self) -> int:
        """
        return the number of nodes in the graph.
        """
        return len(self.names_hash)

    def get_parents(self, node: Node) -> List[Node]:
        """
        return the list of parents for a node.
        """
        parents = List[Node]()
        edges = self.edge_lists.get(node)
        for edge in edges:
            if not edge:
                continue
            endpoint1 = edge.get_distal_endpoint(node)
            endpoint2 = edge.get_proximal_endpoint(node)
            if endpoint1 == Endpoint.TAIL and endpoint2 == Endpoint.ARROW:
                parents.append(edge.get_distal_node(node))
        return parents

    def is_adjacent_to(self, node1: Node, node2: Node) -> bool:
        if not node1 or not node2 or not self.edge_lists.get(node1) or not self.edge_lists.get(node2):
            return False
        for edge in self.edge_lists.get(node1):
            if Edges.traverse(node1, edge) == node2:
                return True
        return False

    def is_ancestor_of(self, node1: Node, node2: Node) -> bool:
        return node1 in self.get_ancestors([node2])

    def possible_ancestor(self, node1: Node, node2: Node) -> bool:
        return self.exists_semidirected_path_from_to(node1, [node2])

    def is_child_of(self, node1: Node, node2: Node) -> bool:
        """
        Determines whether one node is a child of another.
        """
        for edge in self.get_node_edges(node2):
            sub = Edges.traverse_directed(node2, edge)
            if sub == node1:
                return True
        return False

    def is_parent_of(self, node1: Node, node2: Node) -> bool:
        """
        Determines whether one node is a parent of another.
        """
        for edge in self.get_node_edges(node1):
            sub = Edges.traverse_directed(node1, edge)
            if sub == node2:
                return True
        return False

    def is_proper_ancestor_of(self, node1: Node, node2: Node) -> bool:
        """
        Determines whether one node is a proper ancestor of another.
        """
        return node1 != node2 and self.is_ancestor_of(node1, node2)

    def is_proper_descendent_of(self, node1: Node, node2: Node) -> bool:
        return node1 != node2 and self.is_descendent_of(node1, node2);

    def is_descendent_of(self, node1: Node, node2: Node) -> bool:
        """
        Determines whether one node is a descendent of another.
        """
        return node1 == node2 or GraphUtils.exists_directed_path_from_to(node2, node1, self)

    def def_non_descendent(self, node1: Node, node2: Node) -> bool:
        return not self.possible_ancestor(node1, node2)

    def is_def_noncollider(self, node1: Node, node2: Node, node3: Node) -> bool:
        edges = self.get_node_edges(node2)
        circle12 = False
        circle32 = False
        for edge in edges:
            _node1 = edge.get_distal_node(node2) == node1
            _node3 = edge.get_distal_node(node2) == node3
            if _node1 and edge.points_toward(node1):
                return True
            if _node3 and edge.points_toward(node3):
                return True
            if _node1 and edge.get_proximal_endpoint(node2) == Endpoint.CIRCLE:
                circle12 = True
            if _node3 and edge.get_proximal_endpoint(node2) == Endpoint.CIRCLE:
                circle32 = True
            if circle12 and circle32 and not self.is_adjacent_to(node1, node2):
                return True
        return False

    def is_def_collider(self, node1: Node, node2: Node, node3: Node) -> bool:
        edge1 = self.get_edge(node1, node2)
        edge2 = self.get_edge(node2, node3)
        return edge1 and edge2 and edge1.get_proximal_endpoint(node2) == Endpoint.ARROW and edge2.get_proximal_endpoint(
            node2) == Endpoint.ARROW

    def is_d_connected_to(self, x: Node, y: Node, z: List[Node]) -> bool:
        return GraphUtils.is_d_connected_to(x, y, z, self)

    def is_d_separated_from(self, node1: Node, node2: Node, z: List[Node]) -> bool:
        return not self.is_d_connected_to(node1, node2, z)

    def poss_d_connected_to(self, node1: Node, node2: Node, z: List[Node]) -> bool:
        pass

    def is_pattern(self) -> bool:
        return self.pattern

    def set_pattern(self, pattern: bool):
        self.pattern = pattern

    def is_pag(self) -> bool:
        return self.pag

    def set_pag(self, pag: bool):
        self.pag = pag

    def is_directed_from_to(self, node1: Node, node2: Node) -> bool:
        edges = self.get_connecting_edges(node1, node2)
        if len(edges) != 1:
            return False
        edge = edges[0]
        return edge.points_toward(node2)

    def is_undirected_from_to(self, node1: Node, node2: Node) -> bool:
        edge = self.get_edge(node1, node2)
        return not edge and edge.get_endpoint1() == Endpoint.TAIL and edge.get_endpoint2() == Endpoint.TAIL

    def def_visible(self, edge: Edge) -> bool:
        """
        Return true if the given edge is definitely visible
        """
        if self.contains_edge(edge):
            a = Edges.get_directed_edge_tail(edge)
            b = Edges.get_directed_edge_head(edge)
            for c in self.get_adjacent_nodes(a):
                if not (c == b or self.is_adjacent_to(c, b)):
                    e = self.get_edge(c, a)
                    if e.get_proximal_endpoint(a) == Endpoint.ARROW:
                        return True
            return EdgeListGraph.visible_edge_helper(a, b, self)
        else:
            raise ValueError("Given edge is not in the graph.")

    @classmethod
    def visible_edge_helper(cls, a: Node, b: Node, graph: Graph):
        if not a.get_node_type() == NodeType.MEASURED:
            raise ValueError()
        if not b.get_node_type() == NodeType.MEASURED:
            raise ValueError()
        path = List[Node]()
        path.append(a)
        for c in graph.get_nodes_into(a, Endpoint.ARROW):
            if graph.is_parent_of(c, a):
                return True
            if cls.visible_edge_helper_visit(graph, c, a, b, path):
                return True
        return False

    @classmethod
    def visible_edge_helper_visit(cls, graph: Graph, c: Node, a: Node, b: Node, path: List[Node]) -> bool:
        if a in path:
            return False
        path.append(a)
        if a == b:
            return True
        for d in graph.get_nodes_into(a, Endpoint.ARROW):
            if graph.is_parent_of(d, c):
                return True
            if a.get_node_type() == NodeType.MEASURED:
                if not graph.is_def_collider(d, c, a):
                    continue
            if graph.is_def_collider(d, c, a):
                if not graph.is_parent_of(c, b):
                    continue
            if cls.visible_edge_helper_visit(graph, d, c, b, path):
                return True
        path.remove(a)
        return False

    def is_exogenous(self, node: Node) -> bool:
        """
        Determines whether a node in a graph is exogenous.
        """
        return self.get_in_degree(node) == 0

    def get_nodes_into(self, node: Node, endpoint: Endpoint) -> List[Node]:
        pass

    def get_nodes_out_of(self, node: Node, endpoint: Endpoint) -> List[Node]:
        pass

    def remove_edge(self, edge: Edge) -> bool:
        """
        Removes an edge from the graph. (Note: It is dangerous to make a
        recursive call to this method (as it stands) from a method containing
        certain types of iterators. The problem is that if one uses an iterator
        that iterates over the edges of node A or node B, and tries in the
        process to remove those edges using this method, a concurrent
        modification exception will be thrown.)
        """
        if edge in self.edges_set:
            return False

        edge_list1 = self.edge_lists.get(edge.get_node1())
        edge_list2 = self.edge_lists.get(edge.get_node2())
        edge_list1 = list(edge_list1)
        edge_list2 = list(edge_list2)
        self.edges_set.remove(edge)
        edge_list1.remove(edge)
        edge_list2.remove(edge)
        self.edge_lists[edge.get_node1()] = edge_list1
        self.edge_lists[edge.get_node2()] = edge_list2

        self.highlighted_edges.remove(edge)
        self.stuff_removed_since_last_triple_access = True
        self.ancestors = None
        self.get_pcs().firePropertyChange("edgeRemoved", edge, None)
        return True

    def remove_connecting_edge(self, node1: Node, node2: Node) -> bool:
        """
        Removes the edge connecting the two given nodes.
        """
        edges = self.get_connecting_edges(node1, node2)
        if len(edges) > 1:
            raise ValueError(f"There is more than one edge between {node1} and {node2}")
        return self.remove_edges(edges)

    def remove_connecting_edges(self, node1: Node, node2: Node) -> bool:
        pass

    def remove_edges(self, edges: List[Edge]) -> bool:
        change = False
        for edge in edges:
            _change = self.remove_edge(edge)
            change |= _change
        return change

    def remove_node(self, node: Node) -> bool:
        pass

    def remove_nodes(self, nodes: List[Node]) -> bool:
        pass

    def set_endpoint(self, node1: Node, node2: Node, endpoint: Endpoint) -> bool:
        pass

    def subgraph(self, nodes: List[Node]):
        pass

    def transfer_nodes_and_edges(self, graph):
        if not graph:
            raise ValueError("No graph was provided.")
        for node in graph.get_nodes():
            if not self.add_node(node):
                raise ValueError()
        for edge in graph.get_graph_edges():
            if not self.add_edge(edge):
                raise ValueError()

        self.ancestors = None

    def transfer_attributes(self, graph):
        if not graph:
            raise ValueError("No graph was provided.")
        self.attributes = {**graph.get_all_attributes()}

    def get_ambiguous_triples(self) -> Set[Triple]:
        pass

    def get_underlines(self) -> Set[Triple]:
        pass

    def get_dotted_underlines(self) -> Set[Triple]:
        pass

    def is_ambiguous_triple(self, node1: Node, node2: Node, node3: Node) -> bool:
        pass

    def is_underline_triple(self, node1: Node, node2: Node, node3: Node) -> bool:
        pass

    def is_dotted_underline_triple(self, node1: Node, node2: Node, node3: Node) -> bool:
        pass

    def add_ambiguous_triple(self, node1: Node, node2: Node, node3: Node):
        pass

    def add_underline_triple(self, node1: Node, node2: Node, node3: Node):
        pass

    def add_dotted_underline_triple(self, node1: Node, node2: Node, node3: Node):
        pass

    def remove_ambiguous_triple(self, node1: Node, node2: Node, node3: Node):
        pass

    def remove_underline_triple(self, node1: Node, node2: Node, node3: Node):
        pass

    def remove_dotted_underline_triple(self, node1: Node, node2: Node, node3: Node):
        pass

    def set_ambiguous_triples(self, triples: Set):
        pass

    def set_underline_triples(self, triples: Set):
        pass

    def set_dotted_underline_triples(self, triples: Set):
        pass

    def get_causal_ordering(self) -> List[Node]:
        pass

    def set_high_lighted(self, edge: Edge, highlighted: bool):
        pass

    def is_high_lighted(self, edge: Edge) -> bool:
        pass

    def is_parameterizable(self, node: Node) -> bool:
        pass

    def is_time_lag_model(self) -> bool:
        return False

    def get_time_lag_graph(self) -> TimeLagGraph:
        return None

    def remove_triples_not_in_graph(self):
        pass

    def get_sepset(self, node1: Node, node2: Node) -> List[Node]:
        pass

    def set_nodes(self, nodes: List[Node]):
        pass

    def get_all_attributes(self) -> Dict[str, object]:
        pass

    def get_attribute(self, key: str) -> object:
        pass

    def remove_attribute(self, key: str):
        pass

    def add_attribute(self, key: str, value: object):
        pass
