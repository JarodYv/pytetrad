from enum import Enum


class DataType(Enum):
    Continuous = 1
    Discrete = 2
    Mixed = 3
    Graph = 4
    Covariance = 5
    All = 6

    def __str__(self):
        return self.name
