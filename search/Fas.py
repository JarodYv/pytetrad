import logging
from typing import List

from IFas import IFas
from data.Knowledge import Knowledge
from data.Knowledge2 import Knowledge2
from graph.Graph import Graph
from graph.EdgeListGraph import EdgeListGraph
from graph.Node import Node
from graph.Triple import Triple
from search.IndependenceTest import IndependenceTest
from search.SepsetMap import SepsetMap


class Fas(IFas):
    """
    Implements the "fast adjacency search" used in several causal algorithm in this package.
    In the fast adjacency search, at a given stage of the search, an edge X*-*Y is removed from
    the graph if X _||_ Y | S, where S is a subset of size d either of adj(X) or of adj(Y),
    where d is the depth of the search. The fast adjacency search performs this procedure for each pair
    of adjacent edges in the graph and for each depth d = 0, 1, 2, ..., d1, where d1 is either
    the maximum depth or else the first such depth at which no edges can be removed.
    The interpretation of this adjacency search is different for different algorithm,
    depending on the assumptions of the algorithm. A mapping from {x, y} to S({x, y}) is returned
    for edges x *-* y that have been removed.

    Optionally uses Heuristic 3 from Causation, Prediction and Search,
    which (like FAS-Stable) renders the output invariant to the order of the input variables (See Tsagris).
    """

    def __init__(self, initial_graph: Graph, test: IndependenceTest):
        if initial_graph:
            self.init_graph = EdgeListGraph(initial_graph)
        self.test = test
        self.stable = False
        self.heuristic = 0
        self.verbose = False
        self.sepset = SepsetMap()
        self.numDependenceJudgement = 0
        self.numIndependenceTests = 0
        self.depth = 1000
        self.knowledge = Knowledge2()
        self.logger = logging.Logger("Fas")

    def is_aggressively_prevent_cycles(self):
        return False

    def set_aggressively_prevent_cycles(self, v: bool):
        pass

    def get_independence_test(self) -> IndependenceTest:
        return None

    def get_knowledge(self) -> Knowledge:
        return self.knowledge

    def set_knowledge(self, knowledge: Knowledge):
        if not knowledge:
            raise ValueError("Cannot set knowledge to null")
        self.knowledge = knowledge

    def get_sepsets(self) -> SepsetMap:
        return self.sepset

    def get_depth(self) -> int:
        return self.depth

    def set_depth(self, depth: int):
        if depth < -1:
            raise ValueError("Depth must be -1 (unlimited) or >= 0.")
        self.depth = depth

    def search(self) -> Graph:
        pass

    def search_with_node(self, nodes: List[Node]) -> Graph:
        return None

    def get_elapsed_time(self) -> int:
        pass

    def get_num_independence_tests(self) -> int:
        return self.numIndependenceTests

    def set_true_graph(self, true_graph: Graph):
        pass

    def get_nodes(self) -> List[Node]:
        return self.test.get_variables()

    def get_ambiguous_triples(self, node: Node) -> List[Triple]:
        return None

    def is_verbose(self) -> bool:
        return self.verbose

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def get_num_dependence_judgments(self) -> int:
        return self.numDependenceJudgement

    def set_heuristic(self, v: int):
        self.heuristic = v

    def set_stable(self, stable: bool):
        self.stable = stable
