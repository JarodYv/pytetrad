from typing import List

from data.CovarianceMatrix import CovarianceMatrix
from data.DataSet import DataSet
from graph.Node import Node
from pandas import DataFrame


class CorrelationMatrix(CovarianceMatrix):
    """ Stores a correlation matrix together with variable names and sample size;
    intended as a representation of a data set.

    """

    def __init__(self, variables: List[Node], matrix: DataFrame, sample_size: int):
        super(CorrelationMatrix, self).__init__(variables, matrix, sample_size)

    @classmethod
    def from_dataset(cls, dataset: DataSet, bias_corrected: bool = True):
        if dataset.exists_missing_value():
            raise ValueError("Dataset is not a continuous data set.")
        super(CorrelationMatrix, cls).from_dataset(dataset, bias_corrected)

    def set_matrix(self, matrix: DataFrame):
        if matrix.shape[0] != matrix.shape[1]:
            raise ValueError("Matrix must be square.")
        for i in range(matrix.shape[0]):
            if abs(matrix.iloc[i, i] - 1.0) > 1.e-5:
                raise ValueError("For a correlation matrix, variances (diagonal elements) must be 1.0")
        super(CorrelationMatrix, self).set_matrix(matrix)
