import itertools

from search.idt.IndependenceTest import IndependenceTest
from search.ConflictRule import ConflictRule
from data.Knowledge import Knowledge
from data.Knowledge2 import Knowledge2
from graph.Graph import Graph
from graph.Edges import Edges
from graph.GraphUtils import GraphUtils
from graph.Node import Node
from graph.Endpoint import Endpoint
from graph.Triple import Triple
from typing import Dict, List, Set


class OrientCollidersMaxP:
    """
    This is an optimization of the CCD (Cyclic Causal Discovery) algorithm by Thomas Richardson.
    """

    def __init__(self, test: IndependenceTest):
        if not test:
            raise ValueError
        self.independence_test = test
        self.depth: int = -1
        self.elapsed: int = 0
        self.knowledge: Knowledge = Knowledge2()
        self.use_heuristic: bool = False
        self.max_path_length: int = 3
        self.conflict_rule = ConflictRule.OVERWRITE

    def get_depth(self) -> int:
        """ Return the depth of search for the Fast Adjacency Search.

        :return:
        """
        return self.depth

    def set_depth(self, depth: int):
        """ Set the depth of search for the Fast Adjacency Search

        :param depth: The depth of search for the Fast Adjacency Search
        :return:
        """
        self.depth = depth

    def get_elapsed_time(self) -> int:
        return self.elapsed

    def is_use_heuristic(self) -> bool:
        return self.use_heuristic

    def set_use_heuristic(self, use_heuristic: bool):
        self.use_heuristic = use_heuristic

    def get_max_path_length(self) -> int:
        return self.max_path_length

    def set_max_path_length(self, max_path_length: int):
        self.max_path_length = max_path_length

    def get_conflict_rule(self) -> ConflictRule:
        return self.conflict_rule

    def set_conflict_rule(self, conflict_rule: ConflictRule):
        self.conflict_rule = conflict_rule

    def orient(self, graph: Graph):
        self._add_colliders(graph)

    def _add_colliders(self, graph: Graph):
        scores = Dict[Triple, float]()
        nodes = graph.get_nodes()
        for node in nodes:
            self._do_node(graph, scores, node)
        triple_list = list(scores.keys())
        # Most independent ones first.
        triple_list.sort(key=lambda x: scores[x], reverse=True)
        for triple in triple_list:
            print(f"{triple} score = {scores.get(triple)}")
            a = triple.get_x()
            b = triple.get_y()
            c = triple.get_z()
            self._orient_collider(graph, a, b, c, self.get_conflict_rule())

    def _do_node(self, graph: Graph, scores: Dict[Triple, float], b: Node):
        adjacent_nodes = graph.get_adjacent_nodes(b)
        if len(adjacent_nodes) < 2:
            return
        combinations = itertools.combinations(range(len(adjacent_nodes)), 2)
        for combination in combinations:
            a = adjacent_nodes[combination[0]]
            c = adjacent_nodes[combination[1]]
            # Skip triples that are shielded.
            if graph.is_adjacent_to(a, c):
                continue
            if self.use_heuristic:
                if self._exists_short_path(a, c, self.max_path_length, graph):
                    self._test_collider_max_p(graph, scores, a, b, c)
                else:
                    self._test_collider_heuristic(graph, scores, a, b, c)
            else:
                self._test_collider_max_p(graph, scores, a, b, c)

    def _orient_collider(self, graph: Graph, a: Node, b: Node, c: Node, conflict_rule: ConflictRule):
        if self.knowledge.is_forbidden(a.get_name(), b.get_name()):
            return
        if self.knowledge.is_forbidden(c.get_name(), b.get_name()):
            return
        OrientCollidersMaxP.orient_collider(a, b, c, graph, conflict_rule)

    def _test_collider_max_p(self, graph: Graph, scores: Dict[Triple, float], a: Node, b: Node, c: Node):
        adj_a = graph.get_adjacent_nodes(a)
        adj_c = graph.get_adjacent_nodes(c)
        adj_a.remove(c)
        adj_a.remove(a)
        p = 0.0
        S = None
        p_sum1 = 0.0
        p_sum2 = 0.0
        count1 = 0
        count2 = 0
        combinations = itertools.combinations(range(len(adj_a)), self.depth)
        for combination in combinations:
            s = GraphUtils.as_list(combination, adj_a)
            self.independence_test.is_independents(a, c, s)
            _p = self.independence_test.get_p_value()
            if _p > p:
                p = _p
                S = s
            if _p < self.independence_test.get_alpha():
                continue
            if b in s:
                p_sum1 += p
                count1 += 1
            else:
                p_sum2 += p
                count2 += 1
        combinations = itertools.combinations(range(len(adj_c)), self.depth)
        for combination in combinations:
            s = GraphUtils.as_list(combination, adj_c)
            self.independence_test.is_independents(a, c, s)
            _p = self.independence_test.get_p_value()
            if _p > p:
                p = _p
                S = s
            if _p < self.independence_test.get_alpha():
                continue
            if b in s:
                p_sum1 += p
                count1 += 1
            else:
                p_sum2 += p
                count2 += 1
        avg1 = p_sum1 / count1
        avg2 = p_sum2 / count2

        if S and b not in S:
            scores[Triple(a, b, c)] = p

    def _test_collider_heuristic(self, graph: Graph, colliders: Dict[Triple, float], a: Node, b: Node, c: Node):
        if self.knowledge.is_forbidden(a.get_name(), b.get_name()):
            return
        if self.knowledge.is_forbidden(c.get_name(), b.get_name()):
            return
        self.independence_test.is_independent(a, c)
        s1 = self.independence_test.get_score()
        self.independence_test.is_independent(a, c, b)
        s2 = self.independence_test.get_score()
        my_collider_2 = s2 > s1
        if graph.is_adjacent_to(a, c):
            return
        if len(graph.get_connecting_edges(a, b)) > 1 or len(graph.get_connecting_edges(b, c)) > 1:
            return
        if my_collider_2:
            colliders[Triple(a, b, c)] = abs(s2)

    def _exists_short_path(self, x: Node, z: Node, bound: int, graph: Graph) -> bool:
        Q = List[Node]()
        V = Set[Node]()
        Q.append(x)
        V.add(x)
        distance = 0
        e = None
        while len(Q) > 0:
            t = Q.pop(1)
            if e == t:
                e = None
                distance += 1
                if distance > (1000 if bound == -1 else bound):
                    return False
            for u in graph.get_adjacent_nodes(t):
                edge = graph.get_edge(t, u)
                c = Edges.traverse(t, edge)
                if not c:
                    continue
                if c == z and distance > 2:
                    return True
                if c not in V:
                    V.add(c)
                    Q.remove(c)
                    if not e:
                        e = u
        return False

    @classmethod
    def orient_collider(cls, x: Node, y: Node, z: Node, graph: Graph, conflict_rule: ConflictRule):
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
