from data.Knowledge import KnowledgeEdge
from graph.Graph import Graph
from graph.Node import Node
from typing import Set


class ImpliedOrientation:
    """
    Adds any orientations implied by the given orientation.
    """

    def set_knowledge(self, knowledge: KnowledgeEdge):
        """ Sets knowledge.

        :param knowledge:
        :return:
        """
        raise NotImplementedError

    def orient_implied(self, graph: Graph) -> Set[Node]:
        """ Adds implied orientations.

        :param graph:
        :return:
        """
        raise NotImplementedError
