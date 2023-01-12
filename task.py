# Task.py

from itempair import *
from weapon import *
from colony import *
from building import *
from utils import *
from options import *

all_tasks = []
all_building_tasks = []
all_item_tasks = []
all_designation_tasks = []

class Task:

    '''
    The Task class.\n
    Use the "ts_" prefix for in-code variable identification
    '''

    name: str
    requirements: list[ItemPair, ...]
    results: dict
    options: Options
    verboseLogging: bool

    def __init__(self, name: str, requirements: list, results: dict):
        self.name = name
        self.requirements = requirements # [ItemPair(mat_WOOD, 20)]
        self.results = results # {TaskResultTypes.BUILDING: ws_CarpentersTable}
        self.options = Options("options.txt")
        self.verboseLogging = self.options.GetBool("verbose_logging")

    def GetRequirements(self):
        return self.requirements

    def GetRequiredItems(self):
        return [item.item for item in self.requirements]

    def GetRequiredCounts(self):
        return [item.count for item in self.requirements]

    def RequiredItemsString(self, count=True):
        temp = []

        for itemPair in self.requirements:
            if count:
                temp.append(f"{itemPair.item.name} x{itemPair.count}")
            else:
                temp.append(f"{itemPair.item.name}")

        return temp


    def GetResults(self):
        return self.results

    def GetResultsType(self):
        return [type(result) for result in self.results.keys()]

    def Register(self, registerType = TaskType.DEFAULT):
        if self.verboseLogging:
            print(
                f"Successfully registered Task <{self.name}>."
            )
        if registerType is TaskType.DEFAULT:
            all_tasks.append(self)
        elif registerType is TaskType.CRAFT_ITEM:
            all_tasks.append(self)
            all_item_tasks.append(self)
        elif registerType is TaskType.BUILDING:
            all_tasks.append(self)
            all_building_tasks.append(self)
        elif registerType is TaskType.DESIGNATION:
            all_tasks.append(self)
            all_building_tasks.append(self)

        return self

    def TryAt(self, colony: Colony):
        requirementNumber = 0 # This mainly exists for Logging purposes

        inventory = colony.inventory
        buildings = colony.buildings

        for requirement in self.requirements:
            item = requirement.item
            count = requirement.count

            if type(requirement) is not ItemPair:
                print(
                    f"Can't perform Task <{self.name}>. Cause: Type mismatch."
                )
                return None

            if type(item) is MaterialType:

                if item not in colony.GetCountByMaterialType():
                    print(
                        f"Can't perform Task <{self.name}>. Cause: MaterialType <{item.name}> inexistant in inventory."
                    )
                    return

                aftermath = colony.GetCountByMaterialType()[item] - count

                if aftermath < 0:
                    print(
                        f"Can't perform Task <{self.name}>. Cause: MaterialType <{item.name}> is in insufficient quantity."
                    )
                    return

                addedItems = 0

                while colony.GetCountByMaterialType()[item] > aftermath:
                    for invItem in inventory.keys():
                        if addedItems < count and invItem.materialType == item:
                            while inventory[invItem] > 0:
                                inventory[invItem] -= 1
                                addedItems += 1

                                if addedItems < count:
                                    continue
                                else:
                                    break

                colony.UpdateInventory()

                requirementNumber += 1

            else:

                if item not in inventory:
                    print(
                        f"Can't perform Task <{self.name}>. Cause: Unavailable Item <{item.name}> in Colony <{colony.name}>."
                    )
                    return None

                if inventory[item] < count:
                    print(
                        f"Can't perform Task <{self.name}>. Cause: Not enough of Item <{item.name}> in Colony <{colony.name}>."
                    )
                    return None

                if self.verboseLogging:
                    print(
                        f"Successfully fit Requirement <{requirementNumber}> for Task <{self.name}>."
                    )

                requirementNumber += 1

        for (resultType, result) in self.results.items():

            if resultType is TaskResultType.ITEM:

                if not isinstance(result, ItemPair):
                    print(
                        f"Can't perform Task <{self.name}>. Cause: Type mismatch."
                    )
                    return None

                item = result.item
                count = result.count

                if item not in inventory:
                    inventory[item] = count
                else:
                    inventory[item] += count

                if self.verboseLogging:
                    print(
                        f"Successfully performed Task <{self.name}>."
                    )

            elif resultType is TaskResultType.BUILDING:

                if not isinstance(result, Building):

                    print(
                        f"Can't perform Task <{self.name}>. Cause: Type mismatch."
                    )
                    return None

                if self.verboseLogging:
                    print(
                        f"Successfully performed Task <{self.name}>."
                    )

                buildings.append(result)

                if isinstance(result, Bed):
                    colony.beds.append(result)

            else:

                print(
                    f"Can't perform Task <{self.name}>. Cause: Unknown TaskResultType."
                )
                return None


ts_CraftDarkScythe = Task(
    name="task.craftdarkscythe",
    requirements=[
        ItemPair(
            mtt_GoldBar,
            50
        ),
        ItemPair(
            mtt_SteelBar,
            20
        )
    ],
    results={
        TaskResultType.ITEM: ItemPair(wp_DarkScythe, 1)
    }
).Register()

ts_BuildBed = Task(
    name="task.build_bed",
    requirements=[
        ItemPair(
            mtt_Wood,
            10
        )
    ],
    results={
        TaskResultType.BUILDING: bd_bed_WoodenBed
    }
).Register(TaskType.BUILDING)

ts_BuildChessTable = Task(
    name="task.build_chess_table",
    requirements=[
        ItemPair(
            mtt_Wood,
            15
        ),
        ItemPair(
            mtt_Stone,
            5
        ),
    ],
    results={
        TaskResultType.BUILDING: bd_rec_ChessTable
    }
).Register(TaskType.BUILDING)

ts_BuildWell = Task(
    name="task.build_well",
    requirements=[
        ItemPair(
            mtt_Stone,
            10
        ),
        ItemPair(
            mtt_Bucket,
            1
        )
    ],
    results={
        TaskResultType.BUILDING: bd_hyd_Well
    }
).Register(TaskType.BUILDING)