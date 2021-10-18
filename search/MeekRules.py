from typing import Set, Dict

from ImpliedOrientation import ImpliedOrientation
from data.Knowledge import Knowledge
from data.Knowledge2 import Knowledge2
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
        self.knowledge = Knowledge2()
        self.use_rule4 = not self.knowledge.is_empty()
        self.aggressively_prevent_cycles = False
        self.verbose = False
        self.revert_to_unshielded_colliders = True
        self.changed_edges = Dict[Edge, Edge]
        self.logger = logging.getLogger("MeekRules")

    def set_knowledge(self, knowledge: Knowledge):
        if not knowledge:
            raise ValueError
        self.knowledge = knowledge

    def orient_implied(self, graph: Graph) -> Set[Node]:
        visited: Set[Node] = Set[Node]()
        self.logger.info("Starting Orientation Step D.")
        if self.revert_to_unshielded_colliders:
            self.revertToUnshieldedColliders(graph.get_nodes(), graph, visited)
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

    def set_verbose(self, verbose: bool):
        self.verbose = verbose
