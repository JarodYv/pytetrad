from data.IKnowledge import IKnowledge


class KnowledgeTransferable:
    """ Interface implemented by classes that are capable of participating
    in the transfer of knowledge objects.
    """

    def get_knowledge(self) -> IKnowledge:
        raise NotImplementedError

    def set_knowledge(self, knowledge: IKnowledge):
        raise NotImplementedError
