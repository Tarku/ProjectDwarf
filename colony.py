# Colony.py

from material import *
from faction import *

all_colonies = []

HEADSTART_QUANTITY = 2000

class Colony:

    '''
    The Workshop class.\n
    Use the "col_" prefix for in-code variable identification.
    '''

    def __init__(self, name: str, faction: Faction):
        self.name = name

        self.buildings = []
        self.members = []

        self.inventory = {}

        self.faction = faction

    def Register(self):
        all_colonies.append(self)
        return self

    def GiveHeadstart(self):
        for material in mat_all:
            self.inventory[material] = HEADSTART_QUANTITY

    def AddMember(self, member: Person):
        self.members.append(member)