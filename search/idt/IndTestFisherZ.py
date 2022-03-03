from typing import List

import numpy as np

from data.DataModel import DataModel
from data.DataSet import DataSet
from graph.Node import Node
from search.idt.IndependenceTest import IndependenceTest


class IndTestFisherZ(IndependenceTest):
    """
    Checks conditional independence of variable in a continuous data set using Fisher's Z test.
    See Spirtes, Glymour and Scheines - "Causation, Prediction and Search" 2nd edition, page 94.
    """

    def __init__(self, data: DataSet, alpha: float):
        self.data = data
        if not (self.data.is_continuous()):
            raise ValueError("Data set must be continuous.")
        if not self.data.exists_missing_value():
            pass

    def is_independent(self, x: Node, y: Node, z: List[Node]) -> bool:
        pass

    def is_dependent(self, x: Node, y: Node, z: List[Node]) -> bool:
        pass

    def get_p_value(self) -> float:
        pass

    def get_variables(self) -> List[Node]:
        pass

    def get_variable(self) -> Node:
        pass

    def get_variable_names(self) -> List[str]:
        pass

    def determines(self, z: List[Node], y: Node) -> bool:
        pass

    def get_alpha(self) -> float:
        pass

    def set_alpha(self, alpha: float):
        pass

    def get_data(self) -> DataModel:
        pass

    def get_cov(self):
        pass

    def get_datasets(self) -> List:
        pass

    def get_sample_size(self) -> int:
        pass

    def get_cov_matrices(self) -> List[np.ndarray]:
        pass

    def get_score(self) -> float:
        pass

    def set_verbose(self, verbose: bool):
        pass

    def is_verbose(self) -> bool:
        pass

    def ind_test_subset(self, nodes: List[Node]):
        pass
