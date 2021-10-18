from typing import Dict
from graph.NodeType import NodeType
from graph.NodeVariableType import NodeVariableType


class Node:
    """
    Represents an object with a name, node type, and position that can serve as a node in a graph.
    """

    def get_name(self) -> str:
        """ Get the name of the node

        :return: the name of the node
        """
        pass

    def set_name(self, name: str):
        """ Sets the name of this node

        :param name: the name of the node
        :return:
        """
        pass

    def get_node_type(self) -> NodeType:
        """ Get node type of the variable

        :return: the node type of the variable
        """
        pass

    def set_node_type(self, node_type: NodeType):
        """ Set the node type of the variable

        :param node_type: the node type of the variable
        :return:
        """
        pass

    def get_node_variable_type(self) -> NodeVariableType:
        """ Get the intervention type

        :return: the intervention type
        """
        pass

    def set_node_variable_type(self, variable_type: NodeVariableType):
        """ Set the type for this node variable

        :param variable_type: the type for this node variable
        :return:
        """
        pass

    # @return the x coordinate of the center of the node
    def get_center_x(self):
        pass

    # sets the x coordinate of the center of the node
    def set_center_x(self, center_x: int):
        pass

    # @return the y coordinate of the center of the node
    def get_center_y(self):
        pass

    # sets the y coordinate of the center of the node
    def set_center_y(self, center_y: int):
        pass

    # sets the [x, y] coordinates of the center of the node
    def set_center(self, center_x: int, center_y: int):
        pass

    # creates a new node of the same type as this one with the given name
    def like(self, name: str):
        pass

    def get_all_attributes(self) -> Dict[str, object]:
        pass

    def get_attribute(self, key: str) -> object:
        pass

    def remove_attribute(self, key: str):
        pass

    def add_attribute(self, key: str, value: object):
        pass
