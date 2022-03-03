import itertools
import logging
from typing import List, Dict, Set

from IFas import IFas
from data.Knowledge import Knowledge
from data.Knowledge2 import Knowledge2
from graph.Edge import Edge
from graph.Edges import Edges
from graph.Graph import Graph
from graph.EdgeListGraph import EdgeListGraph
from graph.GraphUtils import GraphUtils
from graph.Node import Node
from graph.Triple import Triple
from search.SearchLogUtils import independence_fact, independence_fact_msg
from search.idt.IndependenceTest import IndependenceTest
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
        # Initial graph.
        if initial_graph:
            self.init_graph = EdgeListGraph(initial_graph)

        # The independence test. This should be appropriate to the types
        self.test = test

        # Specification of which edges are forbidden or required.
        self.knowledge = Knowledge2()

        # FAS-Stable
        self.stable = False

        # True iff verbose output should be printed.
        self.verbose = False

        # The sepsets found during the search.
        self.sepset = SepsetMap()

        # Which heuristic to use to fix variable order (1, 2, 3, or 0 = none).
        self.heuristic = 0

        # The number of dependence judgements. Temporary.
        self.numDependenceJudgement = 0

        # The number of independence tests.
        self.numIndependenceTests = 0

        # The maximum number of variables conditioned on in any conditional independence test.
        # If the depth is -1, it will be taken to be the maximum value, which is 1000.
        # Otherwise, it should be set to a non-negative integer.
        self.depth = 1000

        self.logger = logging.Logger("Fas")

    def is_aggressively_prevent_cycles(self) -> bool:
        return False

    def set_aggressively_prevent_cycles(self, v: bool):
        pass

    def get_independence_test(self) -> IndependenceTest:
        return self.test

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
        """
        Discovers all adjacencies in data.  The procedure is to remove edges in the graph which connect pairs of
        variables which are independent conditional on some other set of variables in the graph (the "sepset").
        These are removed in tiers. First, edges which are independent conditional on zero other variables are removed,
        then edges which are independent conditional on one other variable are removed, then two, then three, and so on,
        until no more edges can be removed from the graph. The edges which remain in the graph after this procedure are
        the adjacencies in the data.

        @return a SepSet, which indicates which variables are independent conditional on which other variables
        """
        self.logger.info("Starting Fast Adjacency Search.")
        _depth = 1000 if self.depth == -1 else self.depth
        self.sepset = SepsetMap()
        edges: List[Edge] = []
        nodes: List[Node] = list(self.test.get_variables())
        scores: Dict[Edge, float] = {}

        if self.heuristic == 1:
            nodes.sort()

        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                edges.append(Edges.undirected_edge(nodes[i], nodes[j]))

        for edge in edges:
            self.test.is_independents(edge.get_node1(), edge.get_node2(), [])
            scores[edge] = self.test.get_score()

        if self.heuristic == 2 or self.heuristic == 3:
            edges = [k for k, v in sorted(scores.items(), key=lambda item: item[1])]

        adjacencies: Dict[Node, Set[Node]] = {}
        for node in nodes:
            s = set()
            for _node in nodes:
                if _node == node:
                    continue
                s.add(_node)
            adjacencies[node] = s

        for edge in list(edges):
            if scores[edge] < 0 or \
                    (self.knowledge.is_forbidden(edge.get_node1().get_name(), edge.get_node2().get_name()) and
                     self.knowledge.is_forbidden(edge.get_node2().get_name(), edge.get_node1().get_name())):
                edges.remove(edge)
                adjacencies[edge.get_node1()].remove(edge.get_node2())
                adjacencies[edge.get_node2()].remove(edge.get_node1())
                self.sepset.sets(edge.get_node1(), edge.get_node2(), [])

        for d in range(1, _depth):
            if self.stable:
                adjacencies_copy = {}
                for k, v in adjacencies.items():
                    adjacencies_copy[k] = set(v)
                adjacencies = adjacencies_copy
            more = self.search_at_depth(scores, edges, self.test, adjacencies, d)
            if not more:
                break

        # The search graph.
        # It is assumed going in that all of the true adjacencies of x are in this graph for every node
        # x. It is hoped (i.e. true in the large sample limit) that true adjacencies are never removed.
        graph = EdgeListGraph(nodes=nodes)
        for i in range(len(nodes)):
            for j in range(i + 1, len(nodes)):
                x = nodes[i]
                y = nodes[j]
                if y in adjacencies[x]:
                    graph.add_undirected_edge(x, y)

        self.logger.info("Finishing Fast Adjacency Search.")
        return graph

    def search_at_depth(self, scores: Dict[Edge, float], edges: List[Edge], test: IndependenceTest,
                        adjacencies: Dict[Node, Set[Node]], depth: int) -> bool:
        for edge in edges:
            x = edge.get_node1()
            y = edge.get_node2()
            # if Thread.currentThread().isInterrupted():
            #    break
            if depth == 0 and self.init_graph:
                x2 = self.init_graph.get_node(x.get_name())
                y2 = self.init_graph.get_node(y.get_name())
                if not self.init_graph.is_adjacent_to(x2, y2):
                    continue
            self.check_side(scores, test, adjacencies, depth, x, y)
            self.check_side(scores, test, adjacencies, depth, y, x)

        return self.free_degree(adjacencies) > depth

    def free_degree(self, adjacencies: Dict[Node, Set[Node]]) -> int:
        max_degree = 0
        for k, v in adjacencies.items():
            for y in v:
                adjx = set(v)
                adjx.remove(y)
                if len(adjx) > max_degree:
                    max_degree = len(adjx)
        return max_degree

    def check_side(self, scores: Dict[Edge, float], test: IndependenceTest, adjacencies: Dict[Node, Set[Node]],
                   depth: int, x: Node, y: Node):
        if y not in adjacencies[x]:
            return

        _adjx = list(adjacencies[x])
        _adjx.remove(y)

        if self.heuristic == 1 or self.heuristic == 2:
            _adjx.sort()

        ppx = self.possible_parents(x, _adjx, self.knowledge, y)
        scores2 = {}

        for node in ppx:
            _score = scores[Edges.undirected_edge(node, x)]
            scores2[node] = _score

        if self.heuristic == 3:
            ppx = [k for k, v in sorted(scores2.items(), key=lambda item: item[1], reverse=True)]

        if len(ppx) > depth:
            combinations = itertools.combinations(ppx, 2)
            for choice in combinations:
                # if (Thread.currentThread().isInterrupted())
                #   break
                z = GraphUtils.as_list(choice, ppx)
                self.numIndependenceTests += 1
                independent = test.is_independents(x, y, z)
                if not independent:
                    self.numDependenceJudgement += 1
                no_edge_required = self.knowledge.no_edge_required(x.get_name(), y.get_name())
                if independent and no_edge_required:
                    adjacencies.get(x).remove(y)
                    adjacencies.get(y).remove(x)
                    self.get_sepsets().sets(x, y, z)
                    if self.verbose:
                        self.logger.info("{} score = {:.2e}".format(independence_fact(x, y, z), test.get_score()))
                        print(independence_fact_msg(x, y, z, test.get_p_value()))

    def possible_parents(self, x: Node, adjx: List[Node], knowledge: Knowledge, y: Node) -> List[Node]:
        possible_parents = []
        _x = x.get_name()
        for z in adjx:
            if y == z:
                continue
            _z = z.get_name()
            if self.possible_parent_of(_z, _x, knowledge):
                possible_parents.append(z)

        return possible_parents

    def possible_parent_of(self, z: str, x: str, knowledge: Knowledge) -> bool:
        return not knowledge.is_forbidden(z, x) and not knowledge.is_required(x, z)

    def search_with_node(self, nodes: List[Node]) -> Graph | None:
        return None

    def get_elapsed_time(self) -> int:
        return 0

    def get_num_independence_tests(self) -> int:
        return self.numIndependenceTests

    def set_true_graph(self, true_graph: Graph):
        pass

    def get_nodes(self) -> List[Node] | None:
        return self.test.get_variables()

    def get_ambiguous_triples(self, node: Node) -> List[Triple] | None:
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
