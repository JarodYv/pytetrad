from typing import List

import numpy as np

from data.DataModel import DataModel
from graph.Node import Node
from search.idt.IndependenceTest import IndependenceTest


class IndTestChiSquare(IndependenceTest):
    """
    Checks the conditional independence X _||_ Y | S, where S is a set of discrete variable,
    and X and Y are discrete variable not in S, by applying a conditional Chi Square test.
    A description of such a test is given in Fienberg, "The Analysis of Cross-Classified Categorical Data" 2nd edition.
    The formula for degrees of freedom used in this test are equivalent to the formulation on page 142 of Fienberg.
    """

    def ind_test_subset(self, nodes: List[Node]):
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
