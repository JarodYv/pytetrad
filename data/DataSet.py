from typing import List, Optional
from pandas import DataFrame
from data.DataModel import DataModel
from data.IKnowledge import IKnowledge
from data.Knowledge import Knowledge
from graph.Node import Node


class DataSet(DataModel):
    def __init__(self, data: DataFrame):
        # The container storing the data. Rows are cases; columns are variables.
        # The order of columns is coordinated with the order of variables in getVariables().
        self.data: DataFrame = data

        # The list of variables. These correspond column wise to the columns of data.
        self.variables: List[Node] = []

        # The name of the data model. This is not used internally;
        # It is only here in case an external class wants this dataset to have a name.
        self.name = ""

        # The knowledge associated with this data.
        self.knowledge = Knowledge()
        self.has_missing_value = self.data.isnull().values.any() or self.data.isnull().values.any()

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

    def get_variable(self, name: str) -> Optional[Node]:
        pass

    def get_variables(self) -> List[Node]:
        pass

    def get_variable_names(self) -> List[str]:
        pass

    def get_knowledge(self) -> IKnowledge:
        pass

    def set_knowledge(self, knowledge: Optional[IKnowledge]):
        pass

    def exists_missing_value(self) -> bool:
        return self.has_missing_value

    def get_num_rows(self) -> int:
        """
        return the number of rows in the data set.
        """
        return self.data.shape[1]

    def get_data(self) -> DataFrame:
        return self.data
