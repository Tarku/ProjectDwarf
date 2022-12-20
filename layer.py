# Layer.py

from tile import *

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

    def GetTile(self, position: tuple[int, int]):
        x, y = position
        return self.tiles[y][x]

    def SetTile(self, position: tuple[int, int], tile: Tile):
        x, y = position
        self.tiles[y][x] = tile


