# Utils.py

from enum import Enum
import pygame

# Game launching
ICON_IMAGE = pygame.image.load(
    "assets\\images\\icon.png"
)

TITLE = "Dwarf Game"

# Options

SEPARATOR = "="
COMMENT_SYMBOL = "; "
TRUE = "TRUE"
FALSE = "FALSE"

# Menu stuff

class Screen(Enum):
    COLONY = 0,
    BUILDINGS = 1,
    BUILDING_MENU = 2,
    BUILDING_TASKS = 3,
    EVENTS = 4,
    INVENTORY = 5,
    UNITS = 6,
    DESIGNATIONS = 7,
    MAP = 8,
    UNIT_PRESENTATION = 9

# Tasks

class TaskType (Enum):
    DEFAULT = 0
    CRAFT_ITEM = 1
    BUILDING = 2,
    DESIGNATION = 3

class TaskResultType (Enum):
    ITEM = 0,
    BUILDING = 1

# Map

TILES_PER_SCREEN = 50

# Colony-related

HEADSTART_QUANTITY = 2000

# Person-related
class GenderType(Enum):
    MASCULINE = 0,
    FEMININE = 1,
    NEUTER = 2,
    INANIMATE = 3


all_genders = [
    GenderType.MASCULINE,
    GenderType.FEMININE,
    GenderType.NEUTER,
    GenderType.INANIMATE
]
# Faction-related

FACTION_SYLLABLES_PATH = "assets\\names\\factions\\syllables.txt"

class FactionRelationship(Enum):
    NEUTRAL = 0
    ALLY = 1
    ENEMY = 2


# Miscelleanous

class Direction(Enum):
    NORTH = 0,
    SOUTH = 1,
    WEST = 2
    EAST = 3

class EventType(Enum):
    VISITOR = 0,
    VISITOR_GIFT = 1,
    COLONY_NAME_PROMPT = 2