from typing import Set, Dict, List

from search.ImpliedOrientation import ImpliedOrientation
from data.IKnowledge import IKnowledge
from data.Knowledge import Knowledge
from graph.Graph import Graph
from graph.Node import Node
from graph.Edge import Edge
from graph.Edges import Edges
import logging


class MeekRules(ImpliedOrientation):
    """
    Implements Meek's complete orientation rule set for PC
    (Chris Meek (1995), "Causal inference and causal explanation with background knowledge"),
    modified for Conservative PC to check non-colliders against recorded non-colliders before orienting.

    Rule R4 is only performed if knowledge is nonempty.
    """

    def __init__(self):
        self.knowledge = Knowledge()
        self.use_rule4 = not self.knowledge.is_empty()
        self.aggressively_prevent_cycles = False
        self.verbose = False
        self.is_revert_to_unshielded_colliders = True
        self.changed_edges = Dict[Edge, Edge]
        self.logger = logging.getLogger("MeekRules")

    def set_knowledge(self, knowledge: IKnowledge):
        if not knowledge:
            raise ValueError
        self.knowledge = knowledge

    def orient_implied(self, graph: Graph) -> Set[Node]:
        visited: Set[Node] = Set[Node]()
        self.logger.info("Starting Orientation Step D.")
        if self.is_revert_to_unshielded_colliders:
            self.revert_to_unshielded_colliders(graph.get_nodes(), graph, visited)
        oriented = True
        while oriented:
            oriented = False
            for edge in graph.get_graph_edges():
                if not Edges.is_undirected_edge(edge):
                    continue
                x: Node = edge.get_node1()
                y: Node = edge.get_node2()
                oriented = self.meek_r1(x, y, graph, visited) or self.meek_r1(y, x, graph, visited) or \
                           self.meek_r2(x, y, graph, visited) or self.meek_r2(y, x, graph, visited) or \
                           self.meek_r3(x, y, graph, visited) or self.meek_r3(y, x, graph, visited) or \
                           self.meek_r4(x, y, graph, visited) or self.meek_r4(y, x, graph, visited)
        self.logger.info("Finishing Orientation Step D.")
        return visited

    def revert_to_unshielded_colliders(self, nodes: List[Node], graph: Graph, visited: Set[Node]):
        reverted = True
        while reverted:
            reverted = False
            for node in nodes:
                if self._revert_to_unshielded_colliders(node, graph, visited):
                    reverted = True

    def _revert_to_unshielded_colliders(self, y: Node, graph: Graph, visited: Set[Node]) -> bool:
        did = False
        patterns = graph.get_parents(y)
        for p in patterns:
            for q in patterns:
                if not (p == q or graph.is_adjacent_to(p, q)):
                    break
            else:
                continue
            if self.knowledge.is_forbidden(y.get_name(), p.get_name()) or self.knowledge.is_required(p.get_name(),
                                                                                                     y.get_name()):
                continue
            graph.remove_connecting_edge(p, y)
            graph.add_undirected_edge(p, y)
            visited.add(p)
            visited.add(y)
            did = True
        return did

    def set_revert_to_unshielded_colliders(self, revert_to_unshielded_colliders: bool):
        self.is_revert_to_unshielded_colliders = revert_to_unshielded_colliders

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    @staticmethod
    def is_arrowpoint_allowed(from_node: Node, to_node: Node, knowledge: IKnowledge) -> bool:
        if knowledge.is_empty():
            return True
        return not knowledge.is_required(str(to_node), str(from_node)) and not knowledge.is_forbidden(str(from_node),
                                                                                                      str(to_node))

    def direct(self, a: Node, c: Node, graph: Graph, visited: Set[Node]) -> bool:
        if not MeekRules.is_arrowpoint_allowed(a, c, self.knowledge):
            return False
        if not Edges.is_undirected_edge(graph.get_edge(a, c)):
            return False

        before = graph.get_edge(a, c)
        after = Edges.directed_edge(a, c)

        visited.add(a)
        visited.add(c)

        graph.remove_edge(before)
        graph.add_edge(after)

        return True

    @staticmethod
    def get_common_adjacents(x: Node, y: Node, graph: Graph) -> Set[Node]:
        adj_x: Set[Node] = set(graph.get_adjacent_nodes(x))
        adj_y: Set[Node] = set(graph.get_adjacent_nodes(y))
        return adj_x & adj_y

    def meek_r1(self, b: Node, c: Node, graph: Graph, visited: Set[Node]) -> bool:
        """
        Meek's rule R1: if a-->b, b---c, and a not adj to c, then b-->c
        """
        for a in graph.get_parents(b):
            if graph.is_adjacent_to(c, a):
                continue
            if self.direct(b, c, graph, visited):
                # log(SearchLogUtils.edgeOrientedMsg("Meek R1 triangle (" + a + "-->" + b + "---" + c + ")", graph.getEdge(b, c)));
                return True
        return False

    def meek_r2(self, a: Node, c: Node, graph: Graph, visited: Set[Node]) -> bool:
        """
        If a-->b-->c, a--c, then a-->c.
        """
        adjacent_nodes = graph.get_adjacent_nodes(c)
        adjacent_nodes.remove(a)
        common = MeekRules.get_common_adjacents(a, c, graph)
        for b in common:
            if graph.is_directed_from_to(a, b) and graph.is_directed_from_to(b, c):
                if self.r2_helper(a, b, c, graph, visited):
                    return True

            if graph.is_directed_from_to(c, b) and graph.is_directed_from_to(b, a):
                if self.r2_helper(c, b, a, graph, visited):
                    return True

        return False

    def r2_helper(self, a: Node, b: Node, c: Node, graph: Graph, visited: Set[Node]) -> bool:
        directed = self.direct(a, c, graph, visited)
        # log(SearchLogUtils.edgeOrientedMsg(
        #     "Meek R2 triangle (" + a + "-->" + b + "-->" + c + ", " + a + "---" + c + ")", graph.getEdge(a, c)));
        return directed

    def meek_r3(self, d: Node, a: Node, graph: Graph, visited: Set[Node]) -> bool:
        """
        Meek's rule R3. If d--a, d--b, d--c, b-->a, c-->a, then orient d-->a.
        """
        adjacent_nodes = list(MeekRules.get_common_adjacents(a, d, graph))
        if len(adjacent_nodes) < 2:
            return False
        for i in range(0, len(adjacent_nodes)):
            for j in range(i + 1, len(adjacent_nodes)):
                b = adjacent_nodes[i]
                c = adjacent_nodes[j]
                if not graph.is_adjacent_to(b, c):
                    if self.r3_helper(a, d, b, c, graph, visited):
                        return True
        return False

    def r3_helper(self, a: Node, d: Node, b: Node, c: Node, graph: Graph, visited: Set[Node]) -> bool:
        oriented = False

        b4 = graph.is_undirected_from_to(d, a)
        b5 = graph.is_undirected_from_to(d, b)
        b6 = graph.is_undirected_from_to(d, c)
        b7 = graph.is_directed_from_to(b, a)
        b8 = graph.is_directed_from_to(c, a)

        if b4 and b5 and b6 and b7 and b8:
            oriented = self.direct(d, a, graph, visited)
            # log(SearchLogUtils.edgeOrientedMsg("Meek R3 " + d + "--" + a + ", " + b + ", "
            #                                    + c, graph.getEdge(d, a)));
        return oriented

    def meek_r4(self, a: Node, b: Node, graph: Graph, visited: Set[Node]) -> bool:
        if not self.use_rule4:
            return False

        for c in graph.get_parents(b):
            adj = MeekRules.get_common_adjacents(a, c, graph)
            if b in adj:
                adj.remove(b)
            for d in adj:
                if graph.is_adjacent_to(b, d):
                    continue
                dc = graph.get_edge(d, c)
                if not dc.points_towards(c):
                    continue
                if graph.get_edge(a, d).is_directed():
                    continue
                if self.direct(a, b, graph, visited):
                    # log(SearchLogUtils.edgeOrientedMsg("Meek R4 using " + c + ", " + d, graph.getEdge(a, b)));
                    return True
        return False
