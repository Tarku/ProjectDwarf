# Drawing.Tileset.py

from pygame import image, surface, Vector2, transform
from utils import TILES_PER_SCREEN
from math import floor

class Tileset:

    image: surface.Surface

    tiles: list

    tileWidth: int
    tileHeight: int

    width: int
    height: int

    def __init__(self, c_imagePath: str, c_tileWidth: int, c_tileHeight: int):
        try:
            self.image = image.load(c_imagePath).convert_alpha()

        except FileNotFoundError:

            print(f"Couldn't load Tileset. Cause: Image not found.")
            self.image = surface.Surface(Vector2(96, 96))

        self.tileWidth = c_tileWidth
        self.tileHeight = c_tileHeight

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def Load(self):
        tileNumberX = floor(self.width / self.tileWidth)
        tileNumberY = floor(self.height / self.tileHeight)

        self.tiles = [[None for _ in range(tileNumberX)] for _ in range(tileNumberY)]

        for y in range(tileNumberY):
            for x in range(tileNumberX):
                tile = self.image.subsurface(
                    x * self.tileWidth,
                    y * self.tileHeight,
                    self.tileWidth,
                    self.tileHeight
                )

                self.tiles[y][x] = tile

    def GetTile(self, tilePosition: (Vector2, tuple)):
        tileX, tileY = 0, 0

        if isinstance(tilePosition, Vector2):
            tileX, tileY = tilePosition.x, tilePosition.y

        if isinstance(tilePosition, tuple):
            tileX, tileY = tilePosition[0], tilePosition[1]

        tileNumberX = self.width // self.tileWidth
        tileNumberY = self.height // self.tileHeight

        if not (0 <= tileX <= tileNumberX):
            print(f"Can't Get Tile from Tileset at <{tileX}> <{tileY}>. Cause: X value given is out of bounds.")
            return None

        if not (0 <= tileY <= tileNumberY):
            print(f"Can't Get Tile from Tileset at <{tileX}> <{tileY}>. Cause: Y value given is out of bounds.")
            return None

        return self.tiles[tileY][tileX]



