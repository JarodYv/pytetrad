from KnowledgeTransferable import KnowledgeTransferable
from VariableSource import VariableSource
from graph.Node import Node
from Knowledge import Knowledge
from typing import List


class DataModel(KnowledgeTransferable, VariableSource):
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
