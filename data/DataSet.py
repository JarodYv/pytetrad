from typing import List
import pandas as pd
from data.DataModel import DataModel
from data.Knowledge import Knowledge
from data.Knowledge2 import Knowledge2
from graph.Node import Node


class DataSet(DataModel):
    def __init__(self, data: pd.DataFrame):
        self.data = data
        self.variables = List[Node]()
        self.name = ""
        self.knowledge = Knowledge2()

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def is_continuous(self) -> bool:
        pass

    def is_discrete(self) -> bool:
        pass

    def is_mixed(self) -> bool:
        pass

    def get_variable(self, name: str) -> Node:
        pass

    def get_variables(self) -> List[Node]:
        pass

    def get_variable_names(self) -> List[str]:
        pass

    def get_knowledge(self) -> Knowledge:
        pass

    def set_knowledge(self, knowledge: Knowledge):
        pass