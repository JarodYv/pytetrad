from search.idt.IndependenceTest import IndependenceTest
from SepsetMap import SepsetMap
from data.Knowledge import Knowledge
from graph.Triple import Triple
from graph.Graph import Graph
from graph.Node import Node
from typing import List


class IFas:
    """
    An interface for fast adjacency searches (i.e. PC adjacency searches).
    """

    def is_aggressively_prevent_cycles(self) -> bool:
        raise NotImplementedError

    def set_aggressively_prevent_cycles(self, v: bool):
        raise NotImplementedError

    def get_independence_test(self) -> IndependenceTest:
        raise NotImplementedError

    def get_knowledge(self) -> Knowledge:
        raise NotImplementedError

    def set_knowledge(self, knowledge: Knowledge):
        raise NotImplementedError

    def get_sepsets(self) -> SepsetMap:
        raise NotImplementedError

    def get_depth(self) -> int:
        raise NotImplementedError

    def set_depth(self, depth: int):
        raise NotImplementedError

    def search(self) -> Graph:
        raise NotImplementedError

    def search_with_node(self, nodes: List[Node]) -> Graph | None:
        raise NotImplementedError

    def get_elapsed_time(self) -> int:
        raise NotImplementedError

    def get_num_independence_tests(self) -> int:
        raise NotImplementedError

    def set_true_graph(self, true_graph: Graph):
        raise NotImplementedError

    def get_nodes(self) -> List[Node] | None:
        raise NotImplementedError

    def get_ambiguous_triples(self, node: Node) -> List[Triple] | None:
        raise NotImplementedError

    def is_verbose(self) -> bool:
        raise NotImplementedError

    def set_verbose(self, verbose: bool):
        raise NotImplementedError

    def get_num_dependence_judgments(self) -> int:
        raise NotImplementedError
