# Gender.py

from pronoun import *

all_genders = []

class Gender:
    '''
        The Gender class for the game.\n
        Use the "gd_" prefix for in-code variable identification.
    '''

    name: str
    symbol: str
    canBePregnant: bool

    def __init__(self, name: str, symbol: str, canBePregnant: bool = False):
        self.name = name
        self.symbol = symbol
        self.canBePregnant = canBePregnant

        self.pronoun = Pronoun(name)

    def Register(self):
        all_genders.append(self)
        return self


gd_Masculine = Gender(
    name="masculine",
    symbol="♂"
)

gd_Feminine = Gender(
    name="feminine",
    symbol="♀"
)

gd_Neuter = Gender(
    name="neuter",
    symbol="○"
)

gd_None = Gender(
    name="none",
    symbol="☼"
)