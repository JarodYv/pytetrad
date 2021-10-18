from typing import Set, List, Iterable
from data.KnowledgeGroup import KnowledgeGroup
from data.KnowledgeEdge import KnowledgeEdge
from graph.Graph import Graph
from graph.Node import Node


class Knowledge:
    def add2tier(self, tier: int, var: str):
        raise NotImplementedError

    def add2tiers_by_var_names(self, var_names: List[str]):
        raise NotImplementedError

    def add_knowledge_group(self, group: KnowledgeGroup):
        raise NotImplementedError

    def add_variable(self, var_name: str):
        raise NotImplementedError

    def clear(self):
        raise NotImplementedError

    def explicitly_4_bidden_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        raise NotImplementedError

    def explicitly_required_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        raise NotImplementedError

    def forbidden_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        raise NotImplementedError

    def get_knowledge_groups(self) -> List[KnowledgeGroup]:
        raise NotImplementedError

    def get_variables(self) -> List[str]:
        raise NotImplementedError

    def get_variables_not_in_tiers(self) -> List[str]:
        raise NotImplementedError

    def get_tier(self, tier: int) -> List[str]:
        raise NotImplementedError

    def get_num_tiers(self) -> int:
        raise NotImplementedError

    def is_default_2_knowledge_layout(self) -> bool:
        raise NotImplementedError

    def is_forbidden(self, var1: str, var2: str) -> bool:
        raise NotImplementedError

    def is_forbidden_by_groups(self, var1: str, var2: str) -> bool:
        raise NotImplementedError

    def is_forbidden_by_tiers(self, var1: str, var2: str) -> bool:
        raise NotImplementedError

    def is_required(self, var1: str, var2: str) -> bool:
        raise NotImplementedError

    def is_required_by_groups(self, var1: str, var2: str) -> bool:
        raise NotImplementedError

    def is_empty(self) -> bool:
        raise NotImplementedError

    def is_tier_forbidden_within(self, tier: int) -> bool:
        raise NotImplementedError

    def is_violated_by(self, g: Graph) -> bool:
        raise NotImplementedError

    def no_edge_required(self, x: str, y: str) -> bool:
        raise NotImplementedError

    def remove_from_tiers(self, var: str):
        raise NotImplementedError

    def remove_knowledge_group(self, index: int):
        raise NotImplementedError

    def remove_variable(self, var_name: str):
        raise NotImplementedError

    def required_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        raise NotImplementedError

    def set_forbidden(self, var1: str, var2: str):
        raise NotImplementedError

    def remove_forbidden(self, spec1: str, spec2: str):
        raise NotImplementedError

    def set_required(self, var1: str, var2: str):
        raise NotImplementedError

    def remove_required(self, var1: str, var2: str):
        raise NotImplementedError

    def set_knowledge_group(self, index: int, group: KnowledgeGroup):
        raise NotImplementedError

    def set_tier(self, tier: int, vars: List[str]):
        raise NotImplementedError

    def set_tier_forbidden_within(self, tier: int, forbidden: bool):
        raise NotImplementedError

    def get_max_tier_forbidden_within(self) -> int:
        raise NotImplementedError

    def set_default_2_knowledge_layout(self, default_2_knowledge_layout: bool):
        raise NotImplementedError

    def is_in_which_tier(self, node: Node) -> int:
        raise NotImplementedError

    def get_list_of_required_edges(self) -> List[KnowledgeEdge]:
        raise

    def get_list_of_explicitly_required_edges(self) -> List[KnowledgeEdge]:
        raise NotImplementedError

    def get_list_of_forbidden_edges(self) -> List[KnowledgeEdge]:
        raise NotImplementedError

    def get_list_of_explicitly_forbidden_edges(self) -> List[KnowledgeEdge]:
        raise NotImplementedError

    def is_only_can_cause_next_tier(self, tier: int) -> bool:
        raise NotImplementedError

    def set_only_can_cause_next_tier(self, tier: int, only_causes_next: bool):
        raise NotImplementedError
