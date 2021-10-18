from typing import List

from data.DataModel import DataModel
from data.DataType import DataType
from util.Parameters import Parameters
from .IndependenceWrapper import IndependenceWrapper


class FisherZ(IndependenceWrapper):
    """
    Wrapper for Fisher Z test.
    """

    def get_description(self) -> str:
        return "Fisher Z test"

    def get_parameters(self) -> List[str]:
        return ["alpha"]

    def get_data_type(self) -> DataType:
        return DataType.Continuous

    def get_test(self, dataset: DataModel, **parameters):
        alpha = parameters.get("alpha", 0)
        if isinstance(dataset, CovarianceMatrix):
            return IndTestFisherZ(dataset, alpha)
        elif isinstance(dataset, DataSet):
            return IndTestFisherZ(dataset, alpha)
        raise ValueError("Expecting eithet a data set or a covariance matrix.")
