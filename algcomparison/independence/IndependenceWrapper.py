from typing import List
from search.idt.IndependenceTest import IndependenceTest
from algcomparison.utils.HasParameters import HasParameters
from data.DataType import DataType
from data.DataModel import DataModel


class IndependenceWrapper(HasParameters):
    """
    Interface that algorithm must implement.
    """

    def get_parameters(self) -> List[str]:
        """ Returns the parameters that this search uses.

        """
        raise NotImplementedError

    def get_data_type(self) -> DataType:
        """ Returns the data type that the search requires, whether continuous, discrete, or mixed

        :return: data type
        """
        raise NotImplementedError

    def get_description(self) -> str:
        """ Returns a short description of this independence test.

        :return: description
        """
        raise NotImplementedError

    def get_test(self, dataset: DataModel, **parameters) -> IndependenceTest:
        """ Returns Independence Test instance
        """
        raise NotImplementedError
