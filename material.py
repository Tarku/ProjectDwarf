# Material.py

from materialtype import *
from utils import MAX_FOOD_LEVEL

all_materials = []
all_food_items = []

class Material:

    '''
    The Material class.\n
    Use the "mat_" prefix for in-code variable identification.
    '''
    name: str
    value: int
    materialType: MaterialType

    def __init__(self, name: str, value: int = 1, materialType: MaterialType = None):
        self.name = name
        self.value = value
        self.materialType = materialType

    def Register(self):
        all_materials.append(self)

        if self.materialType is not None:
            materials_by_materialtype[self.materialType] = self
        return self


class CorpseItem(Material):
    '''
    The CorpseItem class.\n
    Use the "cps_" prefix for in-code variable identification.
    '''

    def __init__(self, owner, localization):

        self.owner = owner

        ownerName = self.owner.name
        ownerRace = self.owner.race.name
        ownerAgeName = self.owner.GetAgeName()

        corpseString = localization.Get(
            "corpseitem.corpse",
            (
                ownerName,
                ownerAgeName,
                ownerRace
            )
        )

        Material.__init__(self, corpseString, value=0, materialType=mtt_Corpse)


class FoodItem(Material):

    '''
    The FoodItem class.\n
    Use the "fdi_" prefix for in-code variable identification.
    '''
    name: str
    value: int
    fillPCT: int
    moodBuff: int

    def __init__(self, name: str, value: int, fillPCT: int, moodBuff: int = 0):
        Material.__init__(self, name=name, value=value, materialType=None)

        self.moodBuff = moodBuff
        self.fillPCT = fillPCT

    def Register(self):
        Material.Register(self)
        all_food_items.append(self)
        return self

    def OnEat(self, eater, game):
        eater.mood += self.moodBuff
        eater.foodLevel = (self.fillPCT / 100) * MAX_FOOD_LEVEL


fdi_MushroomSoup = FoodItem(
    name="fooditem.mushroom_soup",
    value=10,
    fillPCT=80,
    moodBuff=10
).Register()

fdi_RottenFlesh = FoodItem(
    name="fooditem.rotten_flesh",
    value=2,
    fillPCT=5,
    moodBuff=-15
).Register()


mat_OakWood = Material(
    name="material.oak_wood",
    value=2,
    materialType=mtt_Wood
).Register()

mat_CherryWood = Material(
    name="material.cherry_wood",
    value=2,
    materialType=mtt_Wood
).Register()

mat_AspenWood = Material(
    name="material.aspen_wood",
    value=2,
    materialType=mtt_Wood
).Register()

mat_Basalt = Material(
    name="material.basalt",
    value=1,
    materialType=mtt_Stone
).Register()

mat_Claystone = Material(
    name="material.claystone",
    value=1,
    materialType=mtt_Stone
).Register()

mat_Granite = Material(
    name="material.granite",
    value=1,
    materialType=mtt_Stone
).Register()

mat_IronBar = Material(
    name="material.iron",
    value=4,
    materialType=mtt_IronBar
).Register()

mat_CopperBar = Material(
    name="material.copper",
    value=3,
    materialType=mtt_CopperBar
).Register()

mat_SteelBar = Material(
    name="material.steel",
    value=6,
    materialType=mtt_SteelBar
).Register()

mat_SilverBar = Material(
    name="material.silver",
    value=16,
    materialType=mtt_SilverBar
).Register()

mat_GoldBar = Material(
    name="material.gold",
    value=32,
    materialType=mtt_GoldBar
).Register()