from algcomparison.independence.IndependenceWrapper import IndependenceWrapper


class TakesIndependenceWrapper:
    def set_independence_wrapper(self, wrapper: IndependenceWrapper):
        raise NotImplementedError

    def get_independence_wrapper(self) -> IndependenceWrapper:
        raise NotImplementedError
