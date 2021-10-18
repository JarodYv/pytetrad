from data.Knowledge import Knowledge


class KnowledgeTransferable:
    """Interface implemented by classes that are capable of participating
    in the transfer of knowledge objects.
    """

    def get_knowledge(self) -> Knowledge:
        raise NotImplementedError

    def set_knowledge(self, knowledge: Knowledge):
        raise NotImplementedError
