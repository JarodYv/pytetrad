from enum import Enum
from graph.Graph import Graph
from graph.Triple import Triple
from graph.Endpoint import Endpoint
from graph.GraphUtils import GraphUtils
from search.IndependenceTest import IndependenceTest
from search.ConflictRule import ConflictRule
from search.GraphSearch import GraphSearch
from search.MeekRules import MeekRules
from search.Fas import Fas
from search.SepsetMap import SepsetMap
from search.SearchGraphUtils import SearchGraphUtils
from search.OrientCollidersMaxP import OrientCollidersMaxP
from data.Knowledge import Knowledge
from data.Knowledge2 import Knowledge2
from graph.Node import Node
from typing import List, Set
import logging
import time
import itertools


class FasType(Enum):
    REGULAR = 1
    STABLE = 2


class Concurrent(Enum):
    YES = 1
    NO = 2


class ColliderDiscovery(Enum):
    FAS_SEPSETS = 1
    CONSERVATIVE = 2
    MAX_P = 3


class PcAll(GraphSearch):
    """ Implements a conservative version of PC, in which the Markov condition is assumed
    but faithfulness is tested locally.
    """

    def __init__(self, independence_test: IndependenceTest, initial_graph: Graph):
        if not independence_test:
            raise ValueError
        self.independence_test = independence_test
        self.init_graph: Graph = initial_graph
        self.aggressively_prevent_cycles: bool = False
        self.collider_discovery: ColliderDiscovery = ColliderDiscovery.FAS_SEPSETS
        self.conflict_rule: ConflictRule = ConflictRule.OVERWRITE
        self.fas_type = FasType.REGULAR
        self.concurrent = Concurrent.YES
        self.depth: int = 1000
        self.elapsed_time: int = 0
        self.knowledge: Knowledge = Knowledge2()
        self.logger = logging.getLogger("PcAll")
        self.verbose: bool = False
        self.use_heuristic: bool = False
        self.max_path_length: int = 0
        self.heuristic: int = 0
        self.graph = None
        self.ambiguous_triples = None
        self.collider_triples = None
        self.non_collider_triples = None
        self.sepsets = None

    def get_elapsed_time(self) -> int:
        return self.elapsed_time

    def search(self) -> Graph:
        return self.search_nodes(self.get_independence_test().get_variables())

    def search_nodes(self, nodes: List[Node]) -> Graph:
        self.logger.info("Starting CPC algorithm")
        self.logger.info(f"Independence test = {self.get_independence_test()}.")
        self.ambiguous_triples = Set[Triple]()
        self.collider_triples = Set[Triple]()
        self.non_collider_triples = Set[Triple]()
        self.independence_test.set_verbose(self.verbose)
        start_time = time.time_ns()

        all_nodes = self.get_independence_test().get_variables()
        for n in nodes:
            if n not in all_nodes:
                raise ValueError("All of the given nodes must be in the domain of the independence test provided.")
        if self.fas_type == FasType.REGULAR:
            if self.concurrent == Concurrent.NO:
                fas = Fas(self.init_graph, self.get_independence_test())
                fas.set_heuristic(self.heuristic)
            else:
                fas = FasConcurrent(self.init_graph, self.get_independence_test())
                fas.setStable(False)
        else:
            if self.concurrent == Concurrent.NO:
                fas = Fas(self.init_graph, self.get_independence_test())
                fas.setStable(True)
            else:
                fas = FasConcurrent(self.init_graph, self.get_independence_test())
                fas.setStable(True)

        fas.set_knowledge(self.get_knowledge())
        fas.set_depth(self.get_depth())
        fas.set_verbose(self.verbose)

        self.graph = fas.search()
        self.sepsets = fas.get_sepsets()

        SearchGraphUtils.pc_orient_bk(self.knowledge, self.graph, nodes)

        if self.collider_discovery == ColliderDiscovery.FAS_SEPSETS:
            self.orient_colliders_using_sepsets(self.sepsets, self.knowledge, self.graph, self.verbose,
                                                self.conflict_rule)
        elif self.collider_discovery == ColliderDiscovery.MAX_P:
            if self.verbose:
                print("MaxP orientation...")
            orient_colliders_max_p: OrientCollidersMaxP = OrientCollidersMaxP(self.independence_test)
            orient_colliders_max_p.set_conflict_rule(self.conflict_rule)
            orient_colliders_max_p.set_use_heuristic(self.use_heuristic)
            orient_colliders_max_p.set_max_path_length(self.max_path_length)
            orient_colliders_max_p.set_depth(self.depth)
            orient_colliders_max_p.orient(self.graph)
        elif self.collider_discovery == ColliderDiscovery.CONSERVATIVE:
            if self.verbose:
                print("CPC orientation...")
            self.orient_unshielded_triples_conservative(self.knowledge)

        self.graph = GraphUtils.replace_node(self.graph, nodes)
        meek_rules: MeekRules = MeekRules()
        meek_rules.set_knowledge(self.knowledge)
        meek_rules.set_verbose(True)
        meek_rules.orient_implied(self.graph)
        self.logger.info(f"\nReturning this graph: {self.graph}")

        self.elapsed_time = time.time_ns() - start_time
        self.logger.info(f"Elapsed time = {self.elapsed_time} ms")
        self.log_triples()

        return self.graph

    def orient_unshielded_triples_conservative(self, knowledge: Knowledge):
        self.logger.info("Starting Collider Orientation:")
        self.collider_triples = Set[Triple]()
        self.non_collider_triples = Set[Triple]()
        self.ambiguous_triples = Set[Triple]()
        nodes = self.graph.get_nodes()
        for y in nodes:
            adjacent_nodes = self.graph.get_adjacent_nodes(y)
            if len(adjacent_nodes) < 2:
                continue
            combinations = itertools.combinations(range(len(adjacent_nodes), 2))
            for combination in combinations:
                x = adjacent_nodes[combination[0]]
                z = adjacent_nodes[combination[1]]
                if self.graph.is_adjacent_to(x, z):
                    continue

                sepsetsxz = self._get_sepsets(x, z, self.graph)
                if self._is_collider_sepset(y, sepsetsxz):
                    if self._collider_allowed(x, y, z, knowledge):
                        PcAll._orient_collider(x, y, z, self.conflict_rule, self.graph)
                    self.collider_triples.add(Triple(x, y, z))
                elif self._is_non_collider_sepset(y, sepsetsxz):
                    self.non_collider_triples.add(Triple(x, y, z))
                else:
                    triple = Triple(x, y, z)
                    self.ambiguous_triples.add(triple)
                    self.graph.add_ambiguous_triple(triple.get_x(), triple.get_y(), triple.get_z())
        self.logger.info("Finishing Collider Orientation.")

    def _get_sepsets(self, i: Node, k: Node, g: Graph) -> List[List[Node]]:
        adj_i = g.get_adjacent_nodes(i)
        adj_k = g.get_adjacent_nodes(k)
        sepsets = List[List[Node]]()
        _max = max(len(adj_i), len(adj_k)) + 1
        for d in range(_max):
            if len(adj_i) >= 2 and d <= len(adj_i):
                combinations = itertools.combinations(range(len(adj_i)), d)
                for combination in combinations:
                    v = GraphUtils.as_list(combination, adj_i)
                    if self.get_independence_test().is_independent(i, k, v):
                        sepsets.append(v)
            if len(adj_k) >= 2 and d <= len(adj_k):
                combinations = itertools.combinations(range(len(adj_k)), d)
                for combination in combinations:
                    v = GraphUtils.as_list(combination, adj_k)
                    if self.get_independence_test().is_independent(i, k, v):
                        sepsets.append(v)
        return sepsets

    def _is_collider_sepset(self, j: Node, sepsets: List[List[Node]]) -> bool:
        if len(sepsets) == 0:
            return False
        for sep in sepsets:
            if j in sep:
                return False
        return True

    def _is_non_collider_sepset(self, j: Node, sepsets: List[List[Node]]) -> bool:
        if len(sepsets) == 0:
            return False
        for sep in sepsets:
            if j not in sep:
                return False
        return True

    def _collider_allowed(self, x: Node, y: Node, z: Node, knowledge: Knowledge) -> bool:
        return PcAll.is_arrowpoint_allowed(x, y, knowledge) and PcAll.is_arrowpoint_allowed(z, y, knowledge)

    @classmethod
    def _orient_collider(cls, x: Node, y: Node, z: Node, conflict_rule: ConflictRule, graph: Graph):
        if conflict_rule == ConflictRule.PRIORITY:
            if not (graph.get_endpoint(y, x) == Endpoint.ARROW or graph.get_endpoint(y, z) == Endpoint.ARROW):
                graph.remove_connecting_edge(x, y)
                graph.remove_connecting_edge(z, y)
                graph.add_directed_edge(x, y)
                graph.add_directed_edge(z, y)
        elif conflict_rule == ConflictRule.BIDIRECTED:
            graph.set_endpoint(x, y, Endpoint.ARROW)
            graph.set_endpoint(z, y, Endpoint.ARROW)
        elif conflict_rule == ConflictRule.OVERWRITE:
            graph.remove_connecting_edge(x, y)
            graph.remove_connecting_edge(z, y)
            graph.add_directed_edge(x, y)
            graph.add_directed_edge(z, y)

    def orient_colliders_using_sepsets(self, sep: SepsetMap, knowledge: Knowledge, graph: Graph, verbose: bool,
                                       conflict_rule: ConflictRule):
        """ Step C of PC; orients colliders using specified sepset.
        That is, orients x *-* y *-* z as x *-> y <-* z just in case y is in Sepset({x, z}).

        :return:
        """
        if verbose:
            print("FAS Sepset orientation...")
        self.logger.info("Starting Collider Orientation:")
        nodes = graph.get_nodes()
        for b in nodes:
            adjacent_nodes = graph.get_adjacent_nodes(b)
            if len(adjacent_nodes) < 2:
                continue
            combinations = itertools.combinations(range(len(adjacent_nodes), 2))
            for combination in combinations:
                a = adjacent_nodes[combination[0]]
                c = adjacent_nodes[combination[1]]
                if self.graph.is_adjacent_to(a, c):
                    continue
                sepset = sep.get(a, c)
                s2 = list(sepset)
                if b not in s2:
                    s2.append(b)
                if b not in sepset and PcAll.is_arrowpoint_allowed(a, b, knowledge) and PcAll.is_arrowpoint_allowed(c,
                                                                                                                    b,
                                                                                                                    knowledge):
                    self.orient_collider(a, b, c, graph, conflict_rule)
                    if verbose:
                        print(f"Collider orientation <{a}, {b}, {c}> sepset = {sepset}")

    def log_triples(self):
        self.logger.info("\nCollider triples:")
        for t in self.collider_triples:
            self.logger.info(f"Collider: {str(t)}")

        self.logger.info("\nNon-collider triples:")
        for t in self.non_collider_triples:
            self.logger.info(f"Non-collider: {str(t)}")

        self.logger.info("\nAmbiguous triples (i.e. list of triples for which " +
                         "\nthere is ambiguous data about whether they are colliderDiscovery or not):")
        for t in self.ambiguous_triples:
            self.logger.info(f"Ambiguous: {str(t)}")

    def is_aggressively_prevent_cycles(self) -> bool:
        return self.aggressively_prevent_cycles

    def set_aggressively_prevent_cycles(self, aggressively_prevent_cycles: bool):
        self.aggressively_prevent_cycles = aggressively_prevent_cycles

    def set_collider_discovery(self, collider_discovery: ColliderDiscovery):
        self.collider_discovery = collider_discovery

    def set_conflict_rule(self, conflict_rule: ConflictRule):
        self.conflict_rule = conflict_rule

    def set_depth(self, depth: int):
        if depth < -1:
            raise ValueError(f"Depth must be -1 or >= 0: {depth}")
        self.depth = depth

    def set_heuristic(self, heuristic: int):
        self.heuristic = heuristic

    def set_use_heuristic(self, use_heuristic: bool):
        self.use_heuristic = use_heuristic

    def set_max_path_length(self, max_path_length: int):
        self.max_path_length = max_path_length

    def get_max_path_length(self) -> int:
        return self.max_path_length

    def get_depth(self) -> int:
        return self.depth

    def get_knowledge(self) -> Knowledge:
        return self.knowledge

    def set_knowledge(self, knowledge: Knowledge):
        self.knowledge = knowledge

    def get_independence_test(self) -> IndependenceTest:
        return self.independence_test

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def set_fas_type(self, _type: FasType):
        self.fas_type = _type

    def set_concurrent(self, _concurrent: Concurrent):
        self.concurrent = _concurrent

    @classmethod
    def is_arrowpoint_allowed(cls, from_node, to_node, knowledge: Knowledge) -> bool:
        """ Checks if an arrowpoint is allowed by background knowledge.

        :param from_node:
        :param to_node:
        :param knowledge:
        :return:
        """
        if not knowledge:
            return True
        return not knowledge.is_required(str(to_node), str(from_node)) and not knowledge.is_forbidden(str(from_node),
                                                                                                      str(to_node))
