from typing import List

from graph.Node import Node


class Score:
    def local_score(self, node: int, parents: List[int] = None) -> float:
        raise NotImplementedError

    def local_score_diff(self, x: int, y: int, z: List[int] = None):
        raise NotImplementedError

    def get_variables(self) -> List[Node]:
        raise NotImplementedError

    def is_effect_edge(self, bump: float) -> bool:
        raise NotImplementedError

    def get_sample_size(self) -> int:
        raise NotImplementedError

    def get_variable(self) -> None:
        raise NotImplementedError

    def get_max_degree(self) -> int:
        raise NotImplementedError

    def determines(self, z: List[Node], y: Node) -> bool:
        raise NotImplementedError

    def default_score(self):
        return self
