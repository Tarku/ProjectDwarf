# Workshop.py

from material import *
from colony import*
from weapon import*
from building import*
from itempair import*
from task import*

all_workshops = []

class Workshop (Building):

    '''
    The Workshop class.\n
    Use the "ws_" prefix for in-code variable identification.
    '''

    def __init__(self, name: str, tasks: list):
        self.name = name
        self.tasks = tasks

        self.activeTasks = []

    def Register(self):
        all_workshops.append(self)
        return self


ws_CarpentersTable = Workshop (
    name = "building.carpenterstable",
    tasks = [
        ts_CraftDarkScythe
    ]
).Register()

ts_BuildCarpentersWorkshop = Task (
    name = "task.buildcarpenterstable",
    requirements = [
        ItemPair (
            mat_WOOD,
            5
        ),
        ItemPair (
            mat_STEEL,
            1
        ),
        ItemPair (
            mat_STEEL,
            1
        ),
        ItemPair (
            mat_STEEL,
            1
        )
    ],
    results = {
        TaskResultType.BUILDING : ws_CarpentersTable
    }
).Register(TaskType.BUILDING)

ws_MasonsTable = Workshop (
    name = "building.masonstable",
    tasks = [
        ts_CraftDarkScythe
    ]
).Register()

ts_BuildMasonsTable = Task (
    name = "task.buildmasonstable",
    requirements = [
        ItemPair (
            mat_STONE,
            5
        )
    ],
    results = {
        TaskResultType.BUILDING : ws_MasonsTable
    }
).Register(TaskType.BUILDING)


