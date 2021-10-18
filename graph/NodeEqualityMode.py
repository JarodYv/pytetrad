from enum import Enum


class NodeEqualityMode:
    class NodeEqualityType(Enum):
        NAME = 1
        OBJECT = 2

    equality_type: NodeEqualityType = NodeEqualityType.NAME

    @classmethod
    def set_equality_mode(cls, _type: NodeEqualityType):
        cls.equality_type = _type

    @classmethod
    def get_equality_type(cls) -> NodeEqualityType:
        return cls.equality_type
