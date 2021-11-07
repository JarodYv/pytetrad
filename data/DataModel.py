from data.KnowledgeTransferable import KnowledgeTransferable
from data.VariableSource import VariableSource
from graph.Node import Node
from data.Knowledge import Knowledge
from typing import List


class DataModel(KnowledgeTransferable, VariableSource):
    """ Interface implemented by classes, instantiations of which can serve as data models in Tetrad.
    Data models may be named if desired; if provided, these names will be used for display purposes.

    This interface is relatively free of methods, mainly because classes that can
    serve as data models in Tetrad are diverse, including continuous and discrete
    data sets, covariance and correlation matrices, graphs, and lists of other
    data models. So this is primarily a tagging interface.
    """

    def get_name(self) -> str:
        """ return the name of the data model (maybe null).

        """
        raise NotImplementedError

    def set_name(self, name: str):
        """ Sets the name of the data model (maybe null).

        """
        raise NotImplementedError

    def is_continuous(self) -> bool:
        raise NotImplementedError

    def is_discrete(self) -> bool:
        raise NotImplementedError

    def is_mixed(self) -> bool:
        raise NotImplementedError

    def get_variable(self, name: str) -> Node:
        raise NotImplementedError

    def get_variables(self) -> List[Node]:
        raise NotImplementedError

    def get_variable_names(self) -> List[str]:
        raise NotImplementedError

    def get_knowledge(self) -> Knowledge:
        raise NotImplementedError

    def set_knowledge(self, knowledge: Knowledge):
        raise NotImplementedError
