from typing import List
from graph import Node
from data.DataModel import DataModel


class IndependenceTest:
    """ Interface implemented by classes that do conditional independence testing.
    These classes are capable of serving as conditional independence "oracles" for constraint-based searches.
    """

    def ind_test_subset(self, nodes: List[Node]):
        raise NotImplementedError

    def is_independent(self, x: Node, y: Node, z: List[Node]) -> bool:
        """ Return true if the given independence question is judged true, false if not.
        The independence question is of the form x _||_ y | z, z = <z1,...,zn>,
        where x, y, z1,...,zn are variables in the list returned by getVariableNames().

        :param x:
        :param y:
        :param z:
        :return:
        """
        raise NotImplementedError

    def is_dependent(self, x: Node, y: Node, z: List[Node]) -> bool:
        """ Return true if the given independence question is judged false, true if not.
        The independence question is of the form x _||_ y | z, z = <z1,...,zn>,
        where x, y, z1,...,zn are variables in the list returned by getVariableNames().

        :param x:
        :param y:
        :param z:
        :return:
        """
        raise NotImplementedError

    def get_p_value(self) -> float:
        """ Return the probability associated with the most recently executed independence test,
        of Double.NaN if p value is not meaningful for tis test.

        :return:
        """
        raise NotImplementedError

    def get_variables(self) -> List[Node]:
        """ The list of variables over which this independence checker is capable of
        determinining independence relations.

        :return:
        """
        raise NotImplementedError

    def get_variable(self) -> Node:
        """ Return the variable by the given name.

        :return:
        """
        raise NotImplementedError

    def get_variable_names(self) -> List[str]:
        """ Return the list of names for the variables in getNodesInEvidence.

        :return:
        """
        raise NotImplementedError

    def determines(self, z: List[Node], y: Node) -> bool:
        """ Return true if y is determined the variable in z

        :param z:
        :param y:
        :return:
        """
        raise NotImplementedError

    def get_alpha(self) -> float:
        """ Return the significance level of the independence test.

        :return:
        """
        raise NotImplementedError

    def set_alpha(self, alpha: float):
        """ Sets the significance level.

        :param alpha:
        :return:
        """
        raise NotImplementedError

    def get_data(self) -> DataModel:
        raise NotImplementedError

    def get_cov(self) -> CovarianceMatrix:
        raise NotImplementedError

    def get_datasets(self) -> List[DataSet]:
        raise NotImplementedError

    def get_sample_size(self) -> int:
        raise NotImplementedError

    def get_cov_matrices(self) -> List[Matrix]:
        raise NotImplementedError

    def get_score(self) -> float:
        raise NotImplementedError

    def set_verbose(self, verbose: bool):
        raise NotImplementedError

    def is_verbose(self) -> bool:
        raise NotImplementedError
