from data.Knowledge import Knowledge


class HasKnowledge:
    def get_knowledge(self) -> Knowledge:
        raise NotImplementedError

    def set_knowledge(self, knowledge: Knowledge):
        raise NotImplementedError
