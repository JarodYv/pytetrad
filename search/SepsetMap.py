from typing import List, Dict, Set
from graph.Node import Node


class SepsetMap:
    """
    Stores a map from pairs of nodes to separating sets--that is, for each unordered pair of nodes {node1, node2}
    in a graph, stores a set of nodes conditional on which node1 and node2 are independent (where the nodes are
    considered as variables) or stores null if the pair was not judged to be independent. (Note that if
    a sepset is non-null and empty, that should means that the compared nodes were found to be independent conditional
    on the empty set, whereas if a sepset is null, that should mean that no set was found yet conditional on which
    the compared nodes are independent. So at the end of the search, a null sepset carries different information
    from an empty sepset.)

    We cast the variable-like objects to Node to allow them either to be variables explicitly or else to be graph
    nodes that in some model could be considered as variables. This allows us to use d-separation as a graphical
    indicator of what independence in models ideally should be.
    """

    def __init__(self, sepset=None):
        self.parents = Dict[Node, Set[Node]]
        if sepset:
            self.sepsets = dict(sepset.sepsets)
            self.p_values = dict(sepset.p_values)
        else:
            self.sepsets = Dict[Set[Node], List[Node]]()
            self.p_values = Dict[Set[Node], float]()

    def sets(self, x: Node, y: Node, z: List[Node]):
        """ Sets the sepset for {x, y} to be z. Note that {x, y} is unordered.

        :param x:
        :param y:
        :param z:
        :return:
        """
        pair = [x, y]
        if not z:
            del self.sepsets[pair]
        else:
            self.sepsets[pair] = z

    def gets(self, a: Node, b: Node) -> List[Node]:
        """ Retrieves the sepset previously set for {a, b}, or null if no such set was previously set.

        :param a:
        :param b:
        :return:
        """
        pair = [a, b]
        return self.sepsets.get(pair, Node)

    def get_p_value(self, x: Node, y: Node) -> float:
        pair = [x, y]
        return self.p_values.get(pair, 0)


