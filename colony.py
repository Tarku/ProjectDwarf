# Colony.py

from material import *
from faction import *
from itempair import *

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
            self.AddToInventory(
                ItemPair(
                    material,
                    HEADSTART_QUANTITY
                )
            )

    def UpdateInventory(self):
        for (item, count) in self.inventory.items():
            if count <= 0:
                self.inventory.pop(item)

    def AddToInventory(self, itemPair: ItemPair):
        item = itemPair.item
        count = itemPair.count

        if item not in self.inventory:
            self.inventory[item] = count
        else:
            self.inventory[item] += count

    def RemoveFromInventory(self, itemPair: ItemPair):
        item = itemPair.item
        count = itemPair.count

        if item not in self.inventory:
            print(
                f"Can't remove {item.name} from inventory. Cause: Item is not in Inventory."
            )
            return

        if count > self.inventory[item]:
            print(
                f"Can't remove {item.name} x{count} from inventory. Cause: Item is not in sufficient quantity."
            )
            return

        self.inventory[item] -= count
        self.UpdateInventory()


    def AddMember(self, member: Person):
        self.members.append(member)