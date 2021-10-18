from typing import List
from graph.Node import Node


class VariableSource:
    """ Interface implemented by classes, instantiations of which are associated with
    lists of variables. Such lists of variables are used for a number of purposes--
    creating data sets, creating graphs, comparing one data to another, and so on.
    """

    def get_variables(self) -> List[Node]:
        """Return the list of variables associated with this object.

        :return:
        """
        raise NotImplementedError

    def get_variable_names(self) -> List[str]:
        """ Return the variable names associated with this object.

        :return:
        """
        raise NotImplementedError
