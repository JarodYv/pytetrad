import logging
from typing import Set, Dict, List, Optional

from data.IKnowledge import IKnowledge
from data.Knowledge import Knowledge
from graph.EdgeListGraph import EdgeListGraph
from graph.Graph import Graph
from graph.Node import Node
from graph.Triple import Triple
from search.IFas import IFas
from search.idt.IndependenceTest import IndependenceTest
from search.SepsetMap import SepsetMap


class FasConcurrent(IFas):
    """
    Implements the "fast adjacency search" used in several causal algorithm in this package.
    In the fast adjacency search, at a given stage of the search,
    an edge X*-*Y is removed from the graph if X _||_ Y | S, where S is a subset
    of size d either of adj(X) or of adj(Y), where d is the depth of the search.
    The fast adjacency search performs this procedure for each pair of adjacent edges
    in the graph and for each depth d = 0, 1, 2, ..., d1, where d1 is either
    the maximum depth or else the first such depth at which no edges can be removed.
    The interpretation of this adjacency search is different for different algorithm,
    depending on the assumptions of the algorithm. A mapping from {x, y} to
    S({x, y}) is returned for edges x *-* y that have been removed.

    This variant uses the PC-Stable modification, calculating independence in parallel within each depth.
    It uses a slightly different algorithm from FasStableConcurrent, probably better.
    """

    def __init__(self, test: IndependenceTest, graph: Optional[Graph] = None):
        self.test = test
        if graph:
            self.initial_graph = graph
        else:
            self.initial_graph = graph
        self.stable = True
        self.chunk = 1000
        self.verbose = False
        self.sepsets = SepsetMap()
        self.num_independence_tests = 0
        self.depth = 1000
        self.knowledge = Knowledge()
        self.logger = logging.Logger("FasConcurrent")

    def search(self) -> Graph:
        self.logger.info("Starting Fast Adjacency Search.")
        # graph = EdgeListGraphSingleConnections(self.test.get_variables())
        graph = EdgeListGraph(nodes=self.test.get_variables())
        self.sepsets = SepsetMap()
        _depth = self.depth
        if _depth == -1:
            _depth = 1000
        adjacencies: Dict[Node, Set[Node]] = {}
        nodes = graph.get_nodes()
        for node in nodes:
            adjacencies[node] = set()
        for d in range(_depth + 1):
            more = self.search_at_depth0(nodes, adjacencies) if d == 0 else self.search_at_depth(d, nodes, adjacencies)
            if not more:
                break

        if self.verbose:
            print("Finished with search, constructing Graph...\n")

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                x = nodes[i]
                y = nodes[j]
                if y in adjacencies.get(x):
                    graph.add_undirected_edge(x, y)

        if self.verbose:
            print("Finished constructing Graph\n")
            self.logger.info("Finishing Fast Adjacency Search.")

        return graph

    def search_at_depth0(self, nodes: List[Node], adjacencies: Dict[Node, Set[Node]]) -> bool:
        # FIXME
        if self.verbose:
            print("Searching at depth 0.\n")
        empty = []
        return self.free_degree(nodes, adjacencies) > self.depth

    def search_at_depth(self, depth: int, nodes: List[Node], adjacencies: Dict[Node, Set[Node]]) -> bool:
        # FIXME
        if self.verbose:
            print(f"Searching at depth {depth}\n")
        return self.free_degree(nodes, adjacencies) > depth

    def free_degree(self, nodes: List[Node], adjacencies: Dict[Node, Set[Node]]) -> int:
        max_degree = 0
        for x in nodes:
            opposites = adjacencies.get(x)
            for y in opposites:
                adjx = set(opposites)
                adjx.remove(x)
                if len(adjx) > max_degree:
                    max_degree = len(adjx)
        return max_degree

    def search_with_node(self, nodes) -> Optional[Graph]:
        return None

    def get_elapsed_time(self) -> int:
        return 0

    def get_depth(self):
        return self.depth

    def set_depth(self, depth: int):
        if depth < -1:
            raise ValueError("Depth must be -1 (unlimited) or >= 0.")
        self.depth = depth

    def is_aggressively_prevent_cycles(self) -> bool:
        return False

    def set_aggressively_prevent_cycles(self, v: bool):
        pass

    def get_independence_test(self) -> IndependenceTest:
        return self.test

    def get_knowledge(self) -> IKnowledge:
        return self.knowledge

    def set_knowledge(self, knowledge: IKnowledge):
        if knowledge:
            self.knowledge = knowledge
        else:
            raise ValueError("Cannot set knowledge to null")

    def get_num_independence_tests(self):
        return self.num_independence_tests

    def set_true_graph(self, graph):
        pass

    def get_nodes(self) -> Optional[List[Node]]:
        return None

    def get_ambiguous_triples(self, node: Node) -> Optional[List[Triple]]:
        return None

    def get_sepsets(self) -> SepsetMap:
        return self.sepsets

    def set_initial_graph(self, graph: Graph):
        self.initial_graph = graph

    def get_logger(self):
        return self.logger

    def is_verbose(self) -> bool:
        return self.verbose

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def get_num_dependence_judgments(self) -> int:
        return 0
