# Layer.py

from tile import *
from pygame import Vector2
from filth import *

class Layer:
    '''
    The Layer class for the game.\n
    Use the "ly_" prefix for in-code variable identification.
    '''

    tiles: list[list, ...]
    width: int
    height: int
    altitude: int

    def __init__(self, altitude: int = 100, width: int = 100, height: int = 100):
        self.altitude = altitude
        self.width = width
        self.height = height

        self.tiles = [
            [
                tile_Air for _ in range(width)
            ] for _ in range(height)
        ]

        self.filthMap = [
            [None for _ in range(100)] for _ in range(100)
        ]

    def AddFilth(self, position: Vector2, filth: Filth):
        x, y = position.x, position.y
        self.filthMap[y][x] = filth

    def GetTile(self, position: Vector2):
        x, y = position.x, position.y
        return self.tiles[y][x]

    def SetTile(self, position: Vector2, tile: Tile):
        x, y = position.x, position.y
        self.tiles[y][x] = tile


