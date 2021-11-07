from typing import TypeVar, Generic

T = TypeVar('T')


class OrderedPair(Generic[T]):
    """
    An ordered pair of objects.
    """

    def __init__(self, first: T, second: T):
        if not first:
            raise ValueError("1st node must not be null.")
        if not second:
            raise ValueError("2nd node must not be null.")

        self.first = first  # The "first" node.
        self.second = second  # The "second" node.

    def get_first(self) -> T:
        return self.first

    def get_second(self) -> T:
        return self.second

    def __hash__(self):
        return 13 * hash(self.first) + 67 * hash(self.second)

    def __eq__(self, other):
        if not other or not isinstance(other, OrderedPair):
            raise ValueError
        return self.first == other.first and self.second == other.second

    def __str__(self):
        return f"<{self.first}, {self.second}>"
