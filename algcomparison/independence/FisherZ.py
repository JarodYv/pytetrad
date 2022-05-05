from typing import List

from data.CovarianceMatrix import CovarianceMatrix
from data.DataModel import DataModel
from data.DataSet import DataSet
from data.DataType import DataType
from search.idt.IndTestFisherZ import IndTestFisherZ
from search.idt.IndependenceTest import IndependenceTest
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

    def get_test(self, dataset: DataModel, **parameters) -> IndependenceTest:
        alpha = parameters.get("alpha", 0)
        if isinstance(dataset, CovarianceMatrix):
            return IndTestFisherZ(dataset, alpha)
        elif isinstance(dataset, DataSet):
            return IndTestFisherZ(dataset, alpha)
        raise ValueError("Expecting either a data set or a covariance matrix.")
