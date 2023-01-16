# Utils.py

from enum import Enum
import pygame

pygame.init()

# Game launching
ICON_IMAGE = pygame.image.load(
    "assets/images/icon.png"
)

CURSOR_IMAGE = pygame.image.load(
    "assets/images/cursor.png"
)

CURSOR = pygame.cursors.Cursor((0, 0), CURSOR_IMAGE)

LOADING_SCREEN_STRINGS = [
    "loading.game",
    "loading.faction",
    "loading.colony",
    "loading.giving_headstart",
    "loading.populate_colony",
    "loading.worldgen",
    "loading.parcel",
    "loading.menus",
    "loading.done"
]

WINDOW_WIDTH = 704
WINDOW_HEIGHT = 704

EDGE_PADDING = 20

HALF_WIN_WIDTH = WINDOW_WIDTH // 2
HALF_WIN_HEIGHT = WINDOW_HEIGHT // 2

DISPLAY_SIZE = (WINDOW_WIDTH, WINDOW_HEIGHT)

TITLE = "Project Dwarf - {} FPS"
FPS = 20

# Text related

FONT_NAME = "Arial"

NORMAL_FONT_SIZE = 18
TITLE_FONT_SIZE = 24
STATUS_FONT_SIZE = 32

FONT_ANTIALIASING = True

DEFAULT_FONT = pygame.font.SysFont(FONT_NAME, NORMAL_FONT_SIZE)
BOLD_FONT = pygame.font.SysFont(FONT_NAME, NORMAL_FONT_SIZE, bold=True)
TITLE_FONT = pygame.font.SysFont(FONT_NAME, TITLE_FONT_SIZE, bold=True)
OTHER_FONT = pygame.font.SysFont(FONT_NAME, STATUS_FONT_SIZE, bold=True)

# Options

SEPARATOR = "="
LIST_SEPARATOR = ","
COMMENT_SYMBOL = "; "
TRUE = "TRUE"
FALSE = "FALSE"

# Menu stuff

class Keys:
    ESCAPE = pygame.K_ESCAPE
    UP_ARROW = pygame.K_UP
    DOWN_ARROW = pygame.K_DOWN
    LEFT_ARROW = pygame.K_LEFT
    RIGHT_ARROW = pygame.K_RIGHT
    ENTER = pygame.K_RETURN
    PAGE_UP = pygame.K_PAGEUP
    PAGE_DOWN = pygame.K_PAGEDOWN
    MENU_PREV = pygame.K_UP
    MENU_NEXT = pygame.K_DOWN

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

TILES_PER_SCREEN = 11  # This should be a divisor of

MAP_SCROLL_AMOUNT: int = 1  # By how many tiles the map should be scrolled at using arrow keys

# Colony-related

HEADSTART_QUANTITY = 50000
BASE_POPULATION = 10
IMMIGRATION_MOOD_NEEDED = 30
MAX_IMMIGRATION_MOOD_NEEDED = 120
IMMIGRATION_MOOD_LOST = 4

# Person-related

BASE_DEATH_MOOD_LOSS = 4
DEATH_MOOD_LOSS_FACTOR = 10

MOOD_LOSS_RATE = 0.08
HUNGER_LOSS_RATE = 1.2
SLEEP_LOSS_RATE = 1.1
RECREATION_LOSS_RATE = 0.4
HYDRATION_LOSS_RATE = 2.1

CHITCHAT_OPINION_GAIN = 1.6
DEEP_TALK_OPINION_GAIN = 12

TICKS_PER_HOUR = 20

BASE_SOCIALIZE_TIMER = 2.5 * TICKS_PER_HOUR

MIN_INTROVERTNESS = 0.7
MAX_INTROVERTNESS = 2.4

MIN_XENOPHOBIA = 0.25
MAX_XENOPHOBIA = 2.5

MIN_RACISM = 0.75
MAX_RACISM = 1.85

BASE_BED_SLEEP_RATE = 3.8
BASE_BED_MOOD_RATE = 0.16

MIN_VARIATION = .87
MAX_VARIATION = 1.16

MIN_MOOD = -100.0
MAX_MOOD = 100.0

MIN_RECREATION = 0.0
MAX_RECREATION = 100.0

MIN_FOOD_LEVEL = 0.0
MAX_FOOD_LEVEL = 100.0

MIN_HYDRATION_LEVEL = 0.0
MAX_HYDRATION_LEVEL = 100.0

MIN_SLEEP = 0.0
MAX_SLEEP = 100.0

EAT_ACTION_PCT = 25.0
SLEEP_ACTION_PCT = 25.0
DRINK_ACTION_PCT = 25.0
RECREATION_ACTION_PCT = 25.0

MALNUTRITION_WORSENING = 0.01
DEHYDRATION_WORSENING = 0.03

MAX_BERSERK_LEVEL = -35
MIN_BERSERK_LEVEL = -100

MIN_CONSCIOUSNESS = 0.0
MAX_CONSCIOUSNESS = 100.0

MIGRANT_ARRIVAL_CHANCE_PCT = 35

# Faction-related

FACTION_SYLLABLES_PATH = "assets\\names\\factions\\syllables.txt"
FACTION_BASE_AMOUNT = 4

class TILESET:
    MOUNTAIN_TEMPERATE = (0, 0)
    MOUNTAIN_FREEZING = (1, 0)
    MOUNTAIN_TAIGA = (2, 0)
    MOUNTAIN_SAVANNA = (3, 0)
    MOUNTAIN_DESERT = (4, 0)

    HILLS_TEMPERATE = (0, 1)
    HILLS_FREEZING = (1, 1)
    HILLS_TAIGA = (2, 1)
    HILLS_SAVANNA = (3, 1)
    HILLS_DESERT = (4, 1)

    PLAINS_TEMPERATE = (0, 2)
    PLAINS_FREEZING = (1, 2)
    PLAINS_TAIGA = (2, 2)
    PLAINS_SAVANNA = (3, 2)
    PLAINS_DESERT = (4, 2)

    SEA = (5, 0)
    DEEP_SEA = (6, 0)

class FactionRelationship(Enum):
    NEUTRAL = 0
    ALLY = 1
    ENEMY = 2


# Miscelleanous

TILE_SIZE = 16
PC_TILES_PATH = "assets\\images\\parcel_tileset.png"

def LoopValue(value: 'int, float', minNumber: 'int, float', maxNumber: 'int, float'):
    if value > maxNumber - 1:
        value = minNumber

    if value < minNumber:
        value = maxNumber - 1

    return value

def ClampValue(value: 'int, float', minNumber: 'int, float', maxNumber: 'int, float', isInclusive: bool = True):
    return max(minNumber, min(value, maxNumber))

def ClampTuple(values: tuple, minNumber: int, maxNumber: int):
    return tuple(
        map(
            lambda val: ClampValue(val, minNumber, maxNumber),
            values
        )
    )

def SplitGet(string: str, separator: str, index: int):
    return string.split(separator)[index]
class Direction(Enum):
    NORTH = 0,
    SOUTH = 1,
    WEST = 2
    EAST = 3

class EventType(Enum):
    VISITOR = 0,
    VISITOR_GIFT = 1,
    COLONY_NAME_PROMPT = 2


class HungerState(Enum):
    FED = 0,
    HUNGRY = 1,
    RAVENOUSLY_HUNGRY = 2
    MALNOURISHED = 3


class ThirstState(Enum):
    HYDRATED = 0,
    THIRSTY = 1,
    VERY_THIRSTY = 2
    DEHYDRATED = 3