from typing import Dict, Set


class Parameters:
    def __init__(self, param=None):
        if param and isinstance(param, Parameters):
            self.parameters = dict(param.parameters)
            self.used_parameters = set(param.used_parameters)
            self.overridden_parameters = dict(param.overriddenParameters)
