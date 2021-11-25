from enum import Enum


class EdgeProperty(Enum):
    dd = 1  # definitely direct, A is a direct cause of B
    nl = 2  # definitely visible, A and B do not have a latent confounder
    pd = 3
    pl = 4

    def __str__(self):
        return self.name
