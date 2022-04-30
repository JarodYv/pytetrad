from typing import Optional, List

from pandas import DataFrame

from data.DataModel import DataModel
from data.IKnowledge import IKnowledge
from graph.Node import Node


class ICovarianceMatrix(DataModel):
    """
    Interface for covariance matrices. Implemented in different ways.
    """

    def get_name(self) -> str:
        raise NotImplementedError

    def set_name(self, name: str):
        raise NotImplementedError

    def is_continuous(self) -> bool:
        raise NotImplementedError

    def is_discrete(self) -> bool:
        raise NotImplementedError

    def is_mixed(self) -> bool:
        raise NotImplementedError

    def get_variable(self, name: str) -> Optional[Node]:
        raise NotImplementedError

    def get_variables(self) -> List[Node]:
        raise NotImplementedError

    def get_variable_names(self) -> List[str]:
        raise NotImplementedError

    def get_knowledge(self) -> IKnowledge:
        raise NotImplementedError

    def set_knowledge(self, knowledge: Optional[IKnowledge]):
        raise NotImplementedError

    def get_dimension(self) -> int:
        raise NotImplementedError

    def get_sample_size(self) -> int:
        raise NotImplementedError

    def get_submatrix_by_index(self, indices):
        raise NotImplementedError

    def get_submatrix_by_name(self, names):
        raise NotImplementedError

    def get_value(self, i: int, j: int):
        raise NotImplementedError

    def set_matrix(self, matrix: DataFrame):
        raise NotImplementedError

    def set_sample_size(self, sample_size: int):
        raise NotImplementedError

    def set_value(self, i: int, j: int, v: float) -> float:
        raise NotImplementedError

    def get_size(self) -> int:
        raise NotImplementedError

    def get_matrix(self) -> DataFrame:
        raise NotImplementedError
