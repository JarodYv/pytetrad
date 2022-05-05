from data.IKnowledge import IKnowledge


class HasKnowledge:
    def get_knowledge(self) -> IKnowledge:
        raise NotImplementedError

    def set_knowledge(self, knowledge: IKnowledge):
        raise NotImplementedError
