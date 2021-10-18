from graph.Graph import Graph


class GraphSearch:
    """
    Interface for a search method that returns a graph.
    """

    def search(self) -> Graph:
        raise NotImplementedError

    def get_elapsed_time(self) -> int:
        raise NotImplementedError
