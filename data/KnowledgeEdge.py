class KnowledgeEdge:
    def __init__(self, from_node: str, to_node: str):
        if not from_node or not to_node:
            raise ValueError("from or to is none")
        self.from_node = from_node
        self.to_node = to_node

    def get_from(self) -> str:
        return self.from_node

    def get_to(self) -> str:
        return self.to_node

    def __str__(self):
        return f"{self.from_node} --> {self.to_node}"

    def __eq__(self, other):
        if not other:
            return False
        if not type(other) == type(self):
            return False
        return self.to_node == other.to_node and self.from_node == other.from_node

    def __hash__(self):
        hash_code = 31 + hash(self.from_node)
        return 37 * hash_code + hash(self.to_node)
