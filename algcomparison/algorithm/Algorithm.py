from algcomparison.utils.HasParameters import HasParameters
from graph import Graph
from util import Parameters
from data.DataType import DataType
from data.DataModel import DataModel
from typing import List


class Algorithm(HasParameters):
    """
    Interface that algorithm must implement
    """

    def search(self, dataset: DataModel, parameters: Parameters) -> Graph:
        """ Runs the search.

        :param dataset: The data set to run to the search on
        :param parameters:The parameters of the search
        :return: The result graph
        """
        raise NotImplementedError

    def get_comparison_graph(self, graph: Graph) -> Graph:
        """ Returns that graph that the result should be compared to

        :param graph: The true directed graph, if there is one
        :return: The comparison graph
        """
        raise NotImplementedError

    def get_description(self) -> str:
        """ Returns a short, one-line description of this algorithm.
        This will be printed in the report.

        :return: description of the algorithm
        """
        raise NotImplementedError

    def get_data_type(self) -> DataType:
        """ Returns the data type that the search requires, whether continuous, discrete, or mixed.

        :return: the data type that the algorithm requires
        """
        raise NotImplementedError

    def get_parameters(self) -> List[str]:
        """ Returns the parameters that this search uses.

        :return: A list of String names of parameters
        """
        raise NotImplementedError
