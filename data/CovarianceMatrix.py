from typing import List, Optional, Any

from pandas import DataFrame

from data.DataSet import DataSet
from data.ICovarianceMatrix import ICovarianceMatrix
from data.IKnowledge import IKnowledge
from graph.Node import Node


class CovarianceMatrix(ICovarianceMatrix):

    def __init__(self, variables: List[Node], matrix: DataFrame, sample_size: int):
        if len(variables) > matrix.shape[0] and len(variables) != matrix.shape[1]:
            raise ValueError("# variables not equal to matrix dimension.")
        self.variables = variables
        self.sample_size = sample_size
        self._covariances_matrix = DataFrame(matrix)  # This is not calculating covariances, just storing them.
        self.name = ""
        self.knowledge: Optional[IKnowledge] = None

    @classmethod
    def from_dataset(cls, dataset: DataSet, bias_corrected: bool = True):
        if not dataset.is_continuous():
            raise ValueError("Dataset is not a continuous data set.")
        variables = list(dataset.get_variables())
        matrix = dataset.get_data().cov()
        sample_size = dataset.get_num_rows()
        return cls(variables, matrix, sample_size)

    @classmethod
    def from_covariance_matrix(cls, cov: ICovarianceMatrix):
        return cls(cov.get_variables(), cov.get_matrix(), cov.get_sample_size())

    def get_name(self) -> str:
        """
        Gets the name of the covariance matrix.

        Returns:
            the name of the covariance matrix
        """
        return self.name

    def set_name(self, name: str):
        self.name = name

    def is_continuous(self) -> bool:
        return True

    def is_discrete(self) -> bool:
        return False

    def is_mixed(self) -> bool:
        return False

    def get_variable(self, name: str) -> Optional[Node]:
        for v in self.variables:
            if v.get_name() == name:
                return v
        return None

    def get_variables(self) -> List[Node]:
        return self.variables

    def get_variable_names(self) -> List[str]:
        names: List[str] = []
        for v in self.variables:
            names.append(v.get_name())
        return names

    def remove_variables(self, remains: List[str]):
        raise ValueError("")

    def get_knowledge(self) -> IKnowledge:
        return self.knowledge

    def set_knowledge(self, knowledge: Optional[IKnowledge]):
        if knowledge is None:
            raise ValueError("knowledge is None")
        self.knowledge = knowledge.copy()

    def get_sample_size(self) -> int:
        """
        The size of the sample used to calculate this covariance matrix.

        Returns:
            the size of the sample
        """
        return self.sample_size

    def set_sample_size(self, sample_size: int):
        self.sample_size = sample_size

    def get_matrix(self) -> DataFrame:
        return self._covariances_matrix

    def set_matrix(self, matrix: DataFrame):
        raise ValueError("Setting matrix is not allowed")

    def get_size(self) -> int:
        """
        return the size of the square matrix
        """
        return self._covariances_matrix.shape[1]

    def get_value(self, i: int, j: int) -> Any:
        """
        return the value of element (i,j) in the matrix
        """
        return self._covariances_matrix.iat[i, j]

    def set_value(self, i: int, j: int, v: float):
        self._covariances_matrix.iat[i, j] = v
        self._covariances_matrix.iat[j, i] = v

    def get_submatrix_by_name(self, var_names: List[str]):
        submatrix_vars: List[Node] = []
        for submatrix_var_name in var_names:
            if submatrix_var_name.startswith("E_"):
                continue
            submatrix_vars.append(self.get_variable(submatrix_var_name))
        if not all([v in self.get_variables() for v in submatrix_vars]):
            raise ValueError("The variables in the submatrix must be in the original matrix")
        if None in submatrix_vars:
            raise ValueError("The variable name has None")
        cov = self.get_matrix().loc[var_names, var_names]
        return CovarianceMatrix(variables=submatrix_vars, matrix=cov, sample_size=self.get_sample_size())

    def get_submatrix_by_index(self, indices: List[int]):
        if max(indices) >= self.get_size():
            raise ValueError()
        submatrix_vars: List[Node] = []
        for i in indices:
            submatrix_vars.append(self.get_variables()[i])
        cov = self.get_matrix().iloc[indices, indices]
        return CovarianceMatrix(variables=submatrix_vars, matrix=cov, sample_size=self.get_sample_size())

    def get_dimension(self) -> int:
        """
        Returns:
            return the dimension of the covariance matrix.
        """
        return len(self.variables)

    def __str__(self) -> str:
        s = "{}\n{}".format(self.sample_size, self._covariances_matrix.to_string())
        return s
