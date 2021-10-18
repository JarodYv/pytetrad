from enum import Enum


class ConflictRule(Enum):
    PRIORITY = 1
    BIDIRECTED = 2
    OVERWRITE = 3
