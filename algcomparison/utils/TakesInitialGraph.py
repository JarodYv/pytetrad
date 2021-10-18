from graph.Graph import Graph
from algcomparison.algorithm.Algorithm import Algorithm


class TakesInitialGraph:
    """
    Tags an algorithm that can take an initial graph as input.
    """

    def get_initial_graph(self) -> Graph:
        raise NotImplementedError

    def set_initial_graph(self, graph: Graph):
        raise NotImplementedError

    def set_initial_graph_from_algorithm(self, algorithm: Algorithm):
        raise NotImplementedError
