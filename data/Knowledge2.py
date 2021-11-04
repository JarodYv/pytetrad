from typing import List, Set, Dict, Iterable
from data.Knowledge import Knowledge
from data.KnowledgeEdge import KnowledgeEdge
from data.KnowledgeGroup import KnowledgeGroup
from graph.Edges import Edges
from graph.Graph import Graph
from graph.Node import Node
from graph.OrderedPair import OrderedPair
import re


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
    VARNAME_PATTERN = re.compile("[A-Za-z0-9:_\\-\\.]+")
    SPEC_PATTERN = re.compile("[A-Za-z0-9:-_,\\-\\.*]+")
    COMMAN_DELIM = re.compile(",")

    def __init__(self, nodes: List[str] = None, knowledge=None):
        self.default_to_knowledge_layout: bool = False
        self.variables = Set[str]()
        if not nodes:
            for n in nodes:
                if self._check_var_name(n):
                    self.variables.add(n)
                else:
                    raise NameError(f"Bad variable node {n}.")
        if not knowledge:
            self.default_to_knowledge_layout = knowledge.default_to_knowledge_layout
            self.variables = Set[str](knowledge.variables)
            self.forbidden_rules_specs = list(knowledge.forbidden_rules_specs)
            self.required_rules_specs = list(knowledge.required_rules_specs)
            self.tier_specs = list(knowledge.tier_specs)
            self.knowledge_groups = list(knowledge.knowledge_groups)
            self.knowledge_group_rules = dict(knowledge.knowledge_group_rules)
        else:
            self.forbidden_rules_specs = List[OrderedPair[Set[str]]]()
            self.required_rules_specs = List[OrderedPair[Set[str]]]()
            self.tier_specs = List[Set[str]]()
            self.knowledge_groups = List[KnowledgeGroup]()
            self.knowledge_group_rules = Dict[KnowledgeGroup, OrderedPair[Set[str]]]()

    def _check_var_name(self, name: str) -> bool:
        return True if Knowledge2.VARNAME_PATTERN.match(name) else False

    def _check_spec(self, spec: str) -> str:
        matcher = Knowledge2.SPEC_PATTERN.match(spec)
        if not matcher:
            raise ValueError(f"{spec}: Pattern names can consist of alphabetic "
                             f"characters plus :, _, -, and .. A wildcard '*' "
                             f"may be included to match a string of such characters.")
        return spec.replace(".", "\\.")

    def _get_extent(self, spec: str) -> Set[str]:
        var = Set[str]()
        if "*" in spec:
            patterns = [re.compile(s.replace("*", ".*")) for s in self._split(spec)]
            var = {v for p in patterns if p for v in self.variables if p.match(v)}
        else:
            if spec in self.variables:
                var.add(spec)
        return var

    def _split(self, spec: str) -> Set[str]:
        specs = {s.strip() for s in spec.split(",") if s.strip()}
        return specs

    def _ensure_tiers(self, tier: int):
        for i in range(len(self.tier_specs), tier + 1):
            self.tier_specs.append(set())
            for j in range(i):
                self.forbidden_rules_specs.append(OrderedPair(self.tier_specs[i], self.tier_specs[j]))

    def _get_group_rule(self, group: KnowledgeGroup) -> OrderedPair[Set[str]]:
        from_extent = Set[str]()
        var = group.get_from_variables()
        for v in var:
            from_extent |= self._get_extent(v)
        to_extent = Set[str]()
        var = group.get_to_variables()
        for v in var:
            to_extent |= self._get_extent(v)
        return OrderedPair(from_extent, to_extent)

    def _forbidden_tier_rules(self) -> Set[OrderedPair[Set[str]]]:
        rules = Set[OrderedPair[Set[str]]]()
        for i, r in enumerate(self.tier_specs):
            if self.is_tier_forbidden_within(i):
                rules.add(OrderedPair(r, r))
        for i, r in enumerate(self.tier_specs):
            if self.is_only_can_cause_next_tier(i):
                for j in self.tier_specs[i + 2:]:
                    rules.add(OrderedPair(r, j))
        for i, r in enumerate(self.tier_specs):
            for j in self.tier_specs[i + 1:]:
                rules.add(OrderedPair(j, r))
        return rules

    def add2tier(self, tier: int, spec: str):
        """
        Adds the given variable or wildcard pattern to the given tier.
        The tier is a non-negative integer.
        """
        if tier < 0:
            raise ValueError
        if not spec:
            raise ValueError
        self.add_variable(spec)
        spec = self._check_spec(spec)
        self._ensure_tiers(tier)
        for name in self._get_extent(spec):
            if self._check_var_name(name):
                self.variables.add(name)
                self.tier_specs[tier].add(name)

    def add2tiers_by_var_names(self, var_names: List[str]):
        """
        Puts a variable into tier i if its name is xxx:ti for some xxx and some
        """
        for n in var_names:
            if self._check_var_name(n):
                index = n.rindex(":t")
                if index >= 0:
                    self.add2tier(int(n[index + 2]), n)
            else:
                raise ValueError(f"Bad variable node {n}.")

        for n in var_names:
            if n not in self.variables:
                self.variables.add(n)

    def add_knowledge_group(self, group: KnowledgeGroup):
        """
        Adds a knowledge group. Legacy method, replaced by setForbidden,
        setRequired with patterns. Needed for the interface.
        """
        self.knowledge_groups.append(group)
        o = self._get_group_rule(group)
        self.knowledge_group_rules[group] = o

        if group.get_type() == FORBIDDEN:
            self.forbidden_rules_specs.append(o)
        elif group.get_type() == REQUIRED:
            self.required_rules_specs.append(o)

    def add_variable(self, var_name: str):
        if var_name not in self.variables and self._check_var_name(var_name):
            self.variables.add(var_name)

    def clear(self):
        """
        Removes explicit knowledge and tier information.
        """
        self.forbidden_rules_specs.clear()
        self.required_rules_specs.clear()
        self.tier_specs.clear()

    def explicitly_4_bidden_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        """
        Iterator over the knowledge's explicitly forbidden edges.
        """
        copy = set(self.forbidden_rules_specs)
        forbidden_rules = self._forbidden_tier_rules()
        copy.remove(forbidden_rules)
        for g in self.knowledge_groups:
            copy.remove(self.knowledge_group_rules.get(g))
        edges = Set[KnowledgeEdge]()
        for n in copy:
            for x in n.get_first():
                for y in n.get_second():
                    edges.add(KnowledgeEdge(x, y))
        return edges

    def explicitly_required_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        """
        Iterator over the KnowledgeEdge's explicitly required edges.
        """
        return self.required_edges_iterator()

    def forbidden_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        """
        Iterator over the KnowledgeEdge's representing forbidden edges.
        """
        edges = Set[KnowledgeEdge]()
        for r in self.forbidden_rules_specs:
            for x in r.get_first():
                for y in r.get_second():
                    edges.add(KnowledgeEdge(x, y))
        return edges

    def get_knowledge_groups(self) -> List[KnowledgeGroup]:
        return list(self.knowledge_groups)

    def get_variables(self) -> List[str]:
        var_list = list(self.variables)
        var_list.sort()
        return var_list

    def get_variables_not_in_tiers(self) -> List[str]:
        not_in_tier = set(self.variables)
        for t in self.tier_specs:
            if t in not_in_tier:
                not_in_tier.remove(t)
        return list(not_in_tier)

    def get_tier(self, tier: int) -> List[str]:
        self._ensure_tiers(tier)
        tire_list = list(self.tier_specs[tier])
        tire_list.sort()
        return tire_list

    def get_num_tiers(self) -> int:
        return len(self.tier_specs)

    def is_default_2_knowledge_layout(self) -> bool:
        return self.default_to_knowledge_layout

    def is_forbidden_by_rules(self, var1: str, var2: str) -> bool:
        if var1 == var2:
            return False
        for r in self.forbidden_rules_specs:
            if var1 in r.get_first() and var2 in r.get_second():
                return True
        return False

    def is_forbidden(self, var1: str, var2: str) -> bool:
        """
        Determines whether the edge var1 --> var2 is forbidden.
        """
        if self.is_required(var1, var2):
            return False
        return self.is_forbidden_by_rules(var1, var2) or self.is_forbidden_by_tiers(var1, var2)

    def is_forbidden_by_groups(self, var1: str, var2: str) -> bool:
        s = {self._get_group_rule(g) for g in self.knowledge_groups if g.get_type() == KnowledgeGroup.FORBIDDEN}
        for r in s:
            if var1 in r.get_first() and var2 in r.get_second():
                return True
        return False

    def is_forbidden_by_tiers(self, var1: str, var2: str) -> bool:
        for r in self._forbidden_tier_rules():
            if var1 in r.get_first() and var2 in r.get_second():
                return True
        return False

    def is_required(self, var1: str, var2: str) -> bool:
        """
        Determines whether the edge var1 --> var2 is required.
        """
        if var1 == var2:
            return False
        for r in self.required_rules_specs:
            if var1 in r.get_first() and var2 in r.get_second():
                return True
        return False

    def is_required_by_groups(self, var1: str, var2: str) -> bool:
        s = {self._get_group_rule(g) for g in self.knowledge_groups if g.get_type() == KnowledgeGroup.REQUIRED}
        for r in s:
            if var1 in r.get_first() and var2 in r.get_second():
                return True
        return False

    def is_empty(self) -> bool:
        """
        true if there is no background knowledge recorded.
        """
        return len(self.forbidden_rules_specs) == 0 \
               and len(self.required_rules_specs) == 0 \
               and len(self.tier_specs) == 0

    def is_tier_forbidden_within(self, tier: int) -> bool:
        """
        Checks whether it is the case that any variable is forbidden by any other
        variable within a given tier.
        """
        self._ensure_tiers(tier)
        vars_in_tier = self.tier_specs[tier]
        if len(vars_in_tier) == 0:
            return False
        return OrderedPair(vars_in_tier, vars_in_tier) in self.forbidden_rules_specs

    def is_violated_by(self, g: Graph) -> bool:
        if not g:
            raise ValueError("Sorry, a graph hasn't been provided.")
        for e in g.get_graph_edges():
            if e.is_directed():
                f = Edges.get_directed_edge_tail(e)
                t = Edges.get_directed_edge_head(e)
                return self.is_forbidden(f.get_name(), t.get_name())

        return False

    def no_edge_required(self, x: str, y: str) -> bool:
        return not (self.is_required(x, y) or self.is_required(y, x))

    def remove_from_tiers(self, spec: str):
        """
        Removes the given variable by name or search string from all tiers.
        """
        if not spec:
            raise ValueError()
        spec = self._check_spec(spec)
        for s in self._get_extent(spec):
            for tire in self.tier_specs:
                if s in tire:
                    tire.remove(s)

    def remove_knowledge_group(self, index: int):
        """
        Removes the knowledge group at the given index.
        """
        old = self.knowledge_group_rules.get(self.knowledge_groups[index])
        if old in self.forbidden_rules_specs:
            self.forbidden_rules_specs.remove(old)
        if old in self.required_rules_specs:
            self.required_rules_specs.remove(old)
        self.knowledge_groups.remove(old)

    def remove_variable(self, name: str):
        """
        Removes the given variable from the list of myNodes and all rules.
        """
        if not self._check_var_name(name):
            raise ValueError(f"Bad variable name: {name}")
        self.variables.remove(name)
        for r in self.forbidden_rules_specs:
            r.get_first().remove(name)
            r.get_second().remove(name)
        for r in self.required_rules_specs:
            r.get_first().remove(name)
            r.get_second().remove(name)
        for t in self.tier_specs:
            t.remove(name)

    def required_edges_iterator(self) -> Iterable[KnowledgeEdge]:
        """
        Iterator over the KnowledgeEdge's representing required edges.
        """
        edges = Set[KnowledgeEdge]()
        for r in self.required_rules_specs:
            for s1 in r.get_first():
                for s2 in r.get_second():
                    if s1 != s2:
                        edges.add(KnowledgeEdge(s1, s2))
        return edges

    def set_forbidden(self, var1: str, var2: str):
        """
        Marks the edge var1 --> var2 as forbid.
        """
        self.add_variable(var1)
        self.add_variable(var2)

        var1 = self._check_spec(var1)
        var2 = self._check_spec(var2)

        f1 = self._get_extent(var1)
        f2 = self._get_extent(var2)

        self.forbidden_rules_specs.append(OrderedPair(f1, f2))

    def remove_forbidden(self, var1: str, var2: str):
        """
        Marks the edge var1 --> var2 as not forbid.
        """
        var1 = self._check_spec(var1)
        var2 = self._check_spec(var2)

        f1 = self._get_extent(var1)
        f2 = self._get_extent(var2)

        self.forbidden_rules_specs.remove(OrderedPair(f1, f2))

    def set_required(self, var1: str, var2: str):
        """
        Marks the edge var1 --> var2 as required.
        """
        self.add_variable(var1)
        self.add_variable(var2)

        var1 = self._check_spec(var1)
        var2 = self._check_spec(var2)

        f1 = self._get_extent(var1)
        f2 = self._get_extent(var2)

        for f in f1:
            self.variables.add(f)
        for f in f2:
            self.variables.add(f)

        self.required_rules_specs.append(OrderedPair(f1, f2))

    def remove_required(self, var1: str, var2: str):
        """
        Marks the edge var1 --> var2 as not required.
        """
        var1 = self._check_spec(var1)
        var2 = self._check_spec(var2)

        f1 = self._get_extent(var1)
        f2 = self._get_extent(var2)

        self.required_rules_specs.remove(OrderedPair(f1, f2))

    def set_knowledge_group(self, index: int, group: KnowledgeGroup):
        pass

    def set_tier(self, tier: int, specs: List[str]):
        """
        Sets the variable in a given tier to the specified list.
        """
        self._ensure_tiers(tier)
        vars_in_tier = self.tier_specs[tier]
        if vars_in_tier:
            vars_in_tier.clear()
        for var in specs:
            self.add2tier(tier, var)

    def set_tier_forbidden_within(self, tier: int, forbidden: bool):
        """
        Forbids any variable from being parent of any other variable
        within the given tier, or cancels this forbidding.
        """
        self._ensure_tiers(tier)
        vars_in_tier = self.tier_specs[tier]
        if forbidden:
            self.forbidden_rules_specs.append(OrderedPair(vars_in_tier, vars_in_tier))
        else:
            self.forbidden_rules_specs.remove(OrderedPair(vars_in_tier, vars_in_tier))

    def get_max_tier_forbidden_within(self) -> int:
        """
        return the largest indes of a tier in which every variable is forbidden
        by every other variable, or -1 if there is not such tier.
        """
        for i in range(len(self.tier_specs), -1, -1):
            if self.is_tier_forbidden_within(i):
                return i
        return -1

    def set_default_2_knowledge_layout(self, default_2_knowledge_layout: bool):
        self.default_to_knowledge_layout = default_2_knowledge_layout

    def is_in_which_tier(self, node: Node) -> int:
        """
        Returns the index of the tier of node if it's in a tier, otherwise -1.
        """
        for i in range(len(self.tier_specs)):
            tire = self.tier_specs[i]
            for t in tire:
                if t == node.get_name():
                    return i
        return -1

    def get_list_of_explicitly_required_edges(self) -> List[KnowledgeEdge]:
        # edges = List[KnowledgeEdge]()
        # for r in self.required_rules_specs:
        #     for e1 in r.get_first():
        #         for e2 in r.get_second():
        #             if e1 != e2:
        #                 edges.append(KnowledgeEdge(e1, e2))
        # return edges
        return self.get_list_of_required_edges()

    def get_list_of_forbidden_edges(self) -> List[KnowledgeEdge]:
        edges = List[KnowledgeEdge]()
        for r in self.forbidden_rules_specs:
            for e1 in r.get_first():
                for e2 in r.get_second():
                    if e1 != e2:
                        edges.append(KnowledgeEdge(e1, e2))
        return edges

    def get_list_of_explicitly_forbidden_edges(self) -> List[KnowledgeEdge]:
        copy = set(self.forbidden_rules_specs)
        rules = self._forbidden_tier_rules()
        for r in rules:
            if r in copy:
                copy.remove(r)
        for k in self.knowledge_groups:
            copy.remove(self.knowledge_group_rules.get(k))

        edges = List[KnowledgeEdge]()
        for c in copy:
            for e1 in c.get_first():
                for e2 in c.get_second():
                    edges.append(KnowledgeEdge(e1, e2))
        return edges

    def is_only_can_cause_next_tier(self, tier: int) -> bool:
        self._ensure_tiers(tier)
        vars_in_tier = self.tier_specs[tier]
        if len(vars_in_tier) == 0:
            return False
        if tier + 2 >= len(self.tier_specs):
            return False
        for i in range(tier + 2, len(self.tier_specs)):
            t = self.tier_specs[i]
            o = OrderedPair(vars_in_tier, t)
            if o not in self.forbidden_rules_specs:
                return False
        return True

    def set_only_can_cause_next_tier(self, tier: int, only_causes_next: bool):
        self._ensure_tiers(tier)
        vars_in_tier = self.tier_specs[tier]
        for i in range(tier + 2, len(self.tier_specs)):
            t = self.tier_specs[i]
            o = OrderedPair(vars_in_tier, t)
            if only_causes_next:
                self.forbidden_rules_specs.append(o)
            else:
                self.forbidden_rules_specs.remove(o)

    def __copy__(self):
        return Knowledge2(nodes=[], knowledge=self)

    def __eq__(self, other):
        if not other or not isinstance(other, Knowledge2):
            return False
        return self.forbidden_rules_specs == other.forbidden_rules_specs and \
               self.required_rules_specs == other.required_rules_specs and self.tier_specs == other.tier_specs

    def __hash__(self):
        hash_code = 37
        hash_code += 17 * hash(self.variables) + 37
        hash_code += 17 * hash(self.forbidden_rules_specs) + 37
        hash_code += 17 * hash(self.required_rules_specs) + 37
        hash_code += 17 * hash(self.tier_specs) + 37
        return hash_code

    def __str__(self):
        s = "/knowledge\naddtemporal\n"
        for i in range(self.get_num_tiers()):
            forbidden_within = "*" if self.is_tier_forbidden_within(i) else ""
            only_can_cause_next_tier = "-" if self.is_only_can_cause_next_tier(i) else ""
            s += f"\n{i + 1}{forbidden_within}{only_can_cause_next_tier} "
            tire = self.get_tier(i)
            if tire:
                s += " "
                s += " ".join(tire)

        s += "\n\nforbiddirect"
        for e in self.forbidden_edges_iterator():
            f = e.get_from()
            t = e.get_to()
            if self.is_forbidden_by_tiers(f, t):
                continue
            s += f"\n{f} {t}"

        s += "\n\nrequiredirect"
        for e in self.required_edges_iterator():
            f = e.get_from()
            t = e.get_to()
            s += f"\n{f} {t}"

        return s
