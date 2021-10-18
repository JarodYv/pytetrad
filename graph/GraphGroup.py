from Graph import Graph


class GraphGroup:
    def get_num_graphs(self) -> int:
        raise NotImplementedError

    def get_graph(self, index: int) -> Graph:
        """ Gets a graph at a specific index

        :param index: The index of the graph to return
        :return:
        """
        raise NotImplementedError

    def add_graph(self, g: Graph):
        """ Adds a graph to the graph group.

        :param g: The graph to add to group.
        :return:
        """
        raise NotImplementedError
