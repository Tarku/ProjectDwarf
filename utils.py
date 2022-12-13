# Utils.py

from enum import Enum


class Direction(Enum):
    NORTH = 0,
    SOUTH = 1,
    WEST = 2
    EAST = 3


class MoveEnvironment(Enum):
    HIGHER = 0,
    LOWER = 1


DIRECTIONS = {
    Direction.NORTH: (0, -1),
    Direction.SOUTH: (0, 1),
    Direction.WEST: (-1, 0),
    Direction.EAST: (1, 0)
}


MOVE_COST = {
    MoveEnvironment.HIGHER: 2,
    MoveEnvironment.LOWER: -4
}

TILES_PER_SCREEN = 60