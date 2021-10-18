from typing import List
from data import DataModel
from algcomparison.utils.HasParameters import HasParameters
from data.DataType import DataType
from graph.Node import Node
from search.Score import Score


class ScoreWrapper(HasParameters):
    """
    Interface that algorithm must implement.
    """

    def get_score(self, dataset: DataModel, **parameters) -> Score:
        """ Returns true if x and y are independent conditional on z for the given data set.

        :param dataset: The data set to test independence against.
        :param parameters: The parameters of the test.
        :return:
        """
        raise NotImplementedError

    def get_description(self) -> str:
        """ Returns a short of this independence test.

        :return: This description.
        """
        raise NotImplementedError

    def get_data_type(self) -> DataType:
        """ Returns the data type that the search requires, whether continuous, discrete, or mixed.

        :return: This type.
        """
        raise NotImplementedError

    def get_variable(self) -> Node:
        """ Returns the variable with the given name.

        """
        raise NotImplementedError

    def get_parameters(self) -> List[str]:
        raise NotImplementedError
