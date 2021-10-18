from enum import Enum


class Endpoint(Enum):
    """
    A typesafe enumeration of the types of endpoints that are permitted in
    Tetrad-style graphs: null (-), arrow (->), and circle (-o).
    """
    TAIL = 1
    ARROW = 2
    CIRCLE = 3
    STAR = 4
    NULL = 5

    def __str__(self):
        return self.name
