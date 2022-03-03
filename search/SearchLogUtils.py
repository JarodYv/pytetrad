from typing import List

from graph.Node import Node


def independence_fact(x: Node, y: Node, cond: List[Node]) -> str:
    s = f"{x.get_name()} _||_ {y.get_name()}"
    if cond and len(cond) > 0:
        s += f" | {cond[0]}"
    for i in range(1, len(cond)):
        s += f", {cond[i]}"
    return s


def independence_fact_msg(x: Node, y: Node, cond: List[Node], p: float) -> str:
    s = f"Independence accepted: {independence_fact(x, y, cond)}"
    s = "{}\tp = {:.4f}\n".format(s, p)
    return s
