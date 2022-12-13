# TaskType.py

from enum import *

class TaskType (Enum):
    DEFAULT = 0
    CRAFT_ITEM = 1
    BUILDING = 2,
    DESIGNATION = 3

class TaskResultType (Enum):
    ITEM = 0,
    BUILDING = 1