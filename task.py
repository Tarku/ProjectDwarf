# Task.py

from itempair import *
from weapon import *
from colony import *
from building import *
from utils import *

all_tasks = []
all_building_tasks = []
all_item_tasks = []
all_designation_tasks = []

class Task:

    '''
    The Task class.\n
    Use the "ts_" prefix for in-code variable identification
    '''

    def __init__(self, name: str, requirements: list, results: dict):
        self.name = name
        self.requirements = requirements # [ItemPair(mat_WOOD, 20)]
        self.results = results # {TaskResultTypes.BUILDING: ws_CarpentersTable}

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

                print(
                    f"Successfully performed Task <{self.name}>."
                )

            elif resultType is TaskResultType.BUILDING:

                if not isinstance(result, Building):

                    print(
                        f"Can't perform Task <{self.name}>. Cause: Type mismatch."
                    )
                    return None

                print(
                    f"Successfully performed Task <{self.name}>."
                )
                buildings.append(result)

            else:

                print(
                    f"Can't perform Task <{self.name}>. Cause: Unknown TaskResultType."
                )
                return None

        if requirementNumber is len(self.requirements):
            for requirement in self.requirements:
                item = requirement.item

                count = requirement.count
                inventory[item] -= count

            return True


ts_CraftDarkScythe = Task(
    name = "task.craftdarkscythe",
    requirements = [
        ItemPair(
            mat_GOLD,
            50
        ),
        ItemPair(
            mat_STEEL,
            20
        )
    ],
    results = {
        TaskResultType.ITEM : ItemPair(wp_DarkScythe, 1)
    }
).Register()

