# Drawing.Tileset.py

from pygame import image, surface, Vector2, transform
from utils import TILES_PER_SCREEN

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
            self.image = surface.Surface(Vector2(90, 90))

        self.tileWidth = c_tileWidth
        self.tileHeight = c_tileHeight

        self.width = self.image.get_width()
        self.height = self.image.get_height()

    def Load(self, display):
        tileNumberX = int(self.width / self.tileWidth)
        tileNumberY = int(self.height / self.tileHeight)

        ratioX = display.get_width() / TILES_PER_SCREEN
        ratioY = display.get_height() / TILES_PER_SCREEN

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


    def GetTile(self, tilePosition: [int, int]):
        tileX, tileY = tilePosition

        tileNumberX = int(self.width / self.tileWidth)
        tileNumberY = int(self.height / self.tileHeight)

        if not (0 <= tileX <= tileNumberX):
            print(f"Can't Get Tile from Tileset at <{tileX}> <{tileY}>. Cause: X value given is out of bounds.")
            return None

        if not (0 <= tileY <= tileNumberY):
            print(f"Can't Get Tile from Tileset at <{tileX}> <{tileY}>. Cause: Y value given is out of bounds.")
            return None

        return self.tiles[tileY][tileX]



