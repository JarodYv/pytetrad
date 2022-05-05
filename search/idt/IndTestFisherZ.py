import math
from typing import List, Optional, Dict

import numpy as np
from pandas import DataFrame
import scipy.stats as st

from data.CorrelationMatrix import CorrelationMatrix
from data.CovarianceMatrix import CovarianceMatrix
from data.DataModel import DataModel
from data.DataSet import DataSet
from graph.Node import Node
from search.idt.IndependenceTest import IndependenceTest


class IndTestFisherZ(IndependenceTest):
    """
    Checks conditional independence of variable in a continuous data set using Fisher's Z test.
    See Spirtes, Glymour and Scheines - "Causation, Prediction and Search" 2nd edition, page 94.
    """

    def __init__(self, dataset: Optional[DataSet] = None, data: Optional[DataFrame] = None,
                 variables: Optional[List[Node]] = None, alpha: float = 0):
        self.alpha = alpha
        if alpha < 0 or alpha > 1:
            raise ValueError("Alpha mut be in [0, 1]")
        if dataset is None:
            self.dataset = DataSet(data)
            self.cor = CorrelationMatrix.from_dataset(self.dataset)
            self.variables = list(variables)
        else:
            self.dataset = dataset
            if not (self.dataset.is_continuous()):
                raise ValueError("Data set must be continuous.")

            if not self.dataset.exists_missing_value():
                self.cor = CovarianceMatrix.from_dataset(self.dataset)
                self.variables = self.cor.get_variables()
            else:
                self.cor = CorrelationMatrix.from_dataset(self.dataset)
                self.variables = list(dataset.get_variables())
        self.indexMap = IndTestFisherZ.index_map(self.variables)
        self.nameMap = IndTestFisherZ.name_map(self.variables)
        self.set_alpha(alpha)
        self.nodesHash: Dict[Node, int] = {}
        for i, v in enumerate(self.variables):
            self.nodesHash[v] = i
        self.r = 0.0
        self.p = 0.0
        self.verbose = False

    def is_independents(self, x: Node, y: Node, z: List[Node]) -> bool:
        """
        Determines whether variable x is independent of variable y given a list of conditioning variables z.

        Args:
            x: the 1st variable being compared.
            y: the 2nd variable being compared.
            z: the list of conditioning variables.
        Returns:
            True iff x _||_ y | z
        """
        p = self.cal_p_value(x, y, z)
        if np.isnan(p):
            return True
        else:
            return p > self.alpha

    def is_independent(self, x: Node, y: Node, z: Optional[Node] = None) -> bool:
        return self.is_independents(x, y, [z])

    def is_dependents(self, x: Node, y: Node, z: List[Node]) -> bool:
        return not self.is_independents(x, y, z)

    def is_dependent(self, x: Node, y: Node, z: Optional[Node] = None) -> bool:
        return self.is_dependents(x, y, [z])

    def get_p_value(self) -> float:
        return self.p

    def cal_p_value(self, x: Node, y: Node, z: List[Node]) -> float:
        """
        Calculate the p value

        Args:
            x: the 1st variable being compared.
            y: the 2nd variable being compared.
            z: the list of conditioning variables.
        Returns:
            p-value
        """

        if self.cov_matrix():
            r = self._partial_correlation(x, y, z, None)
            n = self.sample_size()
        else:
            all_vars = list(z)
            all_vars.append(x)
            all_vars.append(y)
            rows = self._get_rows(all_vars)
            r = self._get_r(x, y, z, rows)
            n = len(rows)
        self.r = r
        q = 0.5 * (math.log(1.0 + abs(r)) - math.log(1.0 - abs(r)))
        fisher_z = math.sqrt(n - 3. - len(z)) * q
        self.p = 2 * (1.0 - st.norm.cdf(fisher_z))
        return self.p

    def cov_matrix(self):
        return self.cor

    def sample_size(self) -> int:
        return self.cov_matrix().get_sample_size()

    def get_variables(self) -> List[Node]:
        pass

    def get_variable(self) -> Node:
        pass

    def get_variable_names(self) -> List[str]:
        pass

    def determines(self, z: List[Node], y: Node) -> bool:
        pass

    def get_alpha(self) -> float:
        return self.alpha

    def set_alpha(self, alpha: float):
        if alpha < 0 or alpha > 1:
            raise ValueError(f"Significance out of range: {alpha}")
        self.alpha = alpha

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
        return self.alpha - self.p

    def set_verbose(self, verbose: bool):
        self.verbose = verbose

    def is_verbose(self) -> bool:
        return self.verbose

    def ind_test_subset(self, nodes: List[Node]):
        pass

    @classmethod
    def index_map(cls, nodes: List[Node]) -> Dict[Node, int]:
        imap: Dict[Node, int] = {}
        for i, n in enumerate(nodes):
            imap[n] = i
        return imap

    @classmethod
    def name_map(cls, nodes: List[Node]) -> Dict[str, Node]:
        nmap: Dict[str, Node] = {}
        for n in nodes:
            nmap[n.get_name()] = n
        return nmap

    def _get_rows(self, allVars: List[Node]) -> list:
        rows = []
        for i, r in self.dataset.data.iterrows():
            for node in allVars:
                if np.isnan(r[node.get_name()]):
                    break
            rows.append(i)
        return rows

    def _get_r(self, x: Node, y: Node, z: List[Node], rows: Optional[List[int]]) -> float:
        try:
            return self._partial_correlation(x, y, z, rows)
        except:
            raise ValueError("SingularMatrixException")

    def _partial_correlation(self, x: Node, y: Node, z: List[Node], rows: Optional[List[int]]) -> float:
        indices = [self.indexMap[x], self.indexMap[y]]
        for n in z:
            indices.append(self.indexMap[n])
        cor: Optional[DataFrame] = None
        if self.cor is None:
            cov = self.get_cov(rows, indices)
            cor = MatrixUtils.convertCovToCorr(cov)
        else:
            cor = self.cor.get_selection(indices, indices)
        if len(z) == 0:
            return cor[0, 1]
        return StatUtils.partialCorrelation(cor)
