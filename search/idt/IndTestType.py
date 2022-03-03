from enum import Enum

from data.DataType import DataType


class IndTestType:
    def __init__(self, name: str, data_type: DataType):
        self.name = name
        self.data_type = data_type

    def __str__(self):
        return self.name

    def get_name(self) -> str:
        return self.name

    def get_data_type(self) -> DataType:
        return self.data_type


class IndTest(Enum):
    DEFAULT: IndTestType("Default", DataType.All)
    FISHER_Z: IndTestType("Fisher's Z", DataType.Continuous)
    G_SQUARE: IndTestType("G Square", DataType.Discrete)
