# Tile.py

from itempair import ItemPair
from utils import TILE_SIZE
from material import *

all_tiles = []

class Tile:
    '''
    The Tile class for the game.\n
    Use the "tile_" prefix for in-code variable identification.
    '''

    name: str
    textureFile: str
    textureCoordinates: tuple[int, int]
    drops: list[ItemPair]
    isLiquid: bool

    def __init__(self, name: str, drops: list[ItemPair], isLiquid: bool = False, textureFile: str = "assets\\images\\parcel_tileset.png", textureCoordinates: tuple[int, int] = (0, 0)):
        self.name = name
        self.textureFile = textureFile
        self.textureCoordinates = textureCoordinates
        self.drops = drops

    def Register(self):
        all_tiles.append(self)
        return self


tile_Air = Tile(
    name="tile.air",
    drops=[]
)

tile_Basalt = Tile(
    name="tile.basalt",
    drops=[
        ItemPair(mat_Basalt, 1)
    ]
)


