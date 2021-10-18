from typing import List


class HasParameters:
    """
    Tags a gadget as having parameters
    """

    def get_parameters(self) -> List[str]:
        """ Returns the list of parameter names that are used.
        These are looked up in ParamMap, so if they're not already defined they'll need to be defined there.

        :return:
        """
        raise NotImplementedError
