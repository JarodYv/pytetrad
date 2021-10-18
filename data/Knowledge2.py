from typing import List, Set, Dict, Iterable
from data.Knowledge import Knowledge
from data.KnowledgeEdge import KnowledgeEdge
from data.KnowledgeGroup import KnowledgeGroup
from graph.Graph import Graph
from graph.Node import Node
from graph.OrderedPair import OrderedPair


class Knowledge2(Knowledge):
    """
    Stores information about required and forbidden edges and common causes for use in algorithm.
    This information can be set edge by edge or else globally via temporal tiers.
    When setting temporal tiers, all edges from later tiers to earlier tiers are forbidden.

    For this class, all variable names are referenced by name only.
    This is because the same Knowledge object is intended to plug into different graphs
    with MyNodes that possibly have the same names. Thus, if the Knowledge object forbids
    the edge X --> Y, then it forbids any edge which connects a MyNode named "X" to a MyNode named "Y",
    even if the underlying MyNodes themselves named "X" and "Y", respectively, are not the same.

    In place of variable names, wildcard expressions containing the wildcard '*'
    may be substituted. These will be matched to as many myNodes as possible.
    The '*' wildcard matches any string of consecutive characters up until the
    following character is encountered. Thus, "X*a" will match "X123a" and "X45a".
    """

    def __init__(self, nodes: List[str] = None, knowledge=None):
        self.default_to_knowledge_layout: bool = False
        self.variables = Set[str]()
        if not nodes:
            for n in nodes:
                if self.check_var_name(n):
                    self.variables.add(n)
                else:
                    raise NameError(f"Bad variable node {n}.")
        if not knowledge:
            self.default_to_knowledge_layout = knowledge.default_to_knowledge_layout
            self.variables = Set[str](knowledge.variables)
            self.for_bidden_rules_specs = list(knowledge.for_bidden_rules_specs)
            self.required_rules_specs = list(knowledge.required_rules_specs)
            self.tier_specs = list(knowledge.tier_specs)
            self.knowledge_groups = list(knowledge.knowledge_groups)
            self.knowledge_group_rules = dict(knowledge.knowledge_group_rules)
        else:
            self.for_bidden_rules_specs = List[OrderedPair[Set[str]]]()
            self.required_rules_specs = List[OrderedPair[Set[str]]]()
            self.tier_specs = List[Set[str]]()
            self.knowledge_groups = List[KnowledgeGroup]()
            self.knowledge_group_rules = Dict[KnowledgeGroup, OrderedPair[Set[str]]]()

    def add2tier(self, tier: int, var: str):
        pass

    def add2tiers_by_var_names(self, var_names: List[str]):
        pass

    def add_knowledge_group(self, group: KnowledgeGroup):
        pass

    def add_variable(self, var_name: str):
        pass

    def clear(self):
        pass

    def explicitly_4_bidden_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        pass

    def explicitly_required_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        pass

    def forbidden_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        pass

    def get_knowledge_groups(self) -> List[KnowledgeGroup]:
        pass

    def get_variables(self) -> List[str]:
        pass

    def get_variables_not_in_tiers(self) -> List[str]:
        pass

    def get_tier(self, tier: int) -> List[str]:
        pass

    def get_num_tiers(self) -> int:
        pass

    def is_default_2_knowledge_layout(self) -> bool:
        pass

    def is_forbidden(self, var1: str, var2: str) -> bool:
        pass

    def is_forbidden_by_groups(self, var1: str, var2: str) -> bool:
        pass

    def is_forbidden_by_tiers(self, var1: str, var2: str) -> bool:
        pass

    def is_required(self, var1: str, var2: str) -> bool:
        pass

    def is_required_by_groups(self, var1: str, var2: str) -> bool:
        pass

    def is_empty(self) -> bool:
        pass

    def is_tier_forbidden_within(self, tier: int) -> bool:
        pass

    def is_violated_by(self, g: Graph) -> bool:
        pass

    def no_edge_required(self, x: str, y: str) -> bool:
        pass

    def remove_from_tiers(self, var: str):
        pass

    def remove_knowledge_group(self, index: int):
        pass

    def remove_variable(self, var_name: str):
        pass

    def required_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        pass

    def set_forbidden(self, var1: str, var2: str):
        pass

    def remove_forbidden(self, spec1: str, spec2: str):
        pass

    def set_required(self, var1: str, var2: str):
        pass

    def remove_required(self, var1: str, var2: str):
        pass

    def set_knowledge_group(self, index: int, group: KnowledgeGroup):
        pass

    def set_tier(self, tier: int, vars: List[str]):
        pass

    def set_tier_forbidden_within(self, tier: int, forbidden: bool):
        pass

    def get_max_tier_forbidden_within(self) -> int:
        pass

    def set_default_2_knowledge_layout(self, default_2_knowledge_layout: bool):
        pass

    def is_in_which_tier(self, node: Node) -> int:
        pass

    def get_list_of_explicitly_required_edges(self) -> List[KnowledgeEdge]:
        pass

    def get_list_of_forbidden_edges(self) -> List[KnowledgeEdge]:
        pass

    def get_list_of_explicitly_forbidden_edges(self) -> List[KnowledgeEdge]:
        pass

    def is_only_can_cause_next_tier(self, tier: int) -> bool:
        pass

    def set_only_can_cause_next_tier(self, tier: int, only_causes_next: bool):
        pass

    def check_var_name(self, name: str) -> bool:
        return False
