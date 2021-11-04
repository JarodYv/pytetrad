from enum import Enum


class EdgeProperty(Enum):
    dd = 1
    nl = 2
    pd = 3
    pl = 4

    def __str__(self):
        return self.name
