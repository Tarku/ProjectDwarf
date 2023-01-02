# MaterialType.py

materials_by_materialtype = {}

class MaterialType:
    '''
    The MaterialType class for the game.\n
    Use the "mtt_" prefix for in-game variable identification.
    '''
    name: str
    isFuel: bool

    def __init__(self, name: str, isFuel: bool = False):
        self.name = name
        self.isFuel = isFuel

    def Register(self):
        materials_by_materialtype[self] = list()
        return self


mtt_Wood = MaterialType(
    name="materialtype.wood"  # E.g. "any wood x20"
).Register()

mtt_Stone = MaterialType(
    name="materialtype.stone"
).Register()

mtt_IronBar = MaterialType(
    name="materialtype.iron"
).Register()

mtt_SteelBar = MaterialType(
    name="materialtype.steel"
).Register()

mtt_CopperBar = MaterialType(
    name="materialtype.copper"
).Register()

mtt_GoldBar = MaterialType(
    name="materialtype.gold"
).Register()

mtt_SilverBar = MaterialType(
    name="materialtype.silver"
).Register()

mtt_Coal = MaterialType(
    name="materialtype.coal"
).Register()

mtt_Corpse = MaterialType(
    name="materialtype.corpse"
).Register()