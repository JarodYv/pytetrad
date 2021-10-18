from typing import List
from util.Parameters import Parameters
from algcomparison.utils.HasParameters import HasParameters
from data.DataType import DataType
from data.DataModel import DataModel


class IndependenceWrapper(HasParameters):
    """
    Interface that algorithm must implement.
    """

    def get_parameters(self) -> List[str]:
        raise NotImplementedError

    def get_data_type(self) -> DataType:
        """ Returns the data type that the search requires, whether continuous, discrete, or mixed

        :return:
        """
        raise NotImplementedError

    def get_description(self) -> str:
        """ Returns a short of this independence test.

        :return:
        """
        raise NotImplementedError

    def get_test(self, dataset: DataModel, **parameters):
        """ Returns true iff x and y are independent conditional on z for the given data set.

        :param dataset: The data set to test independence against
        :param parameters: The parameters of the test
        :return: True if independence holds
        """
        raise NotImplementedError
