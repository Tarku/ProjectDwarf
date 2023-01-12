# Drawing.IsometricView.py

import pygame
from drawing.tileset import *
from random import randint
from utils import *
from math import floor

class IsometricView:

    map: list
    tileset: Tileset

    def __init__(self, c_map: list, c_tileset: Tileset):
        self.map = c_map
        self.tileset = c_tileset

    def View(self, display, offset):
        mapHeight = len(self.map)
        mapWidth = len(self.map[0])

        group = pygame.sprite.Group()

        xStart = display.get_width() / 2 - self.tileset.tileWidth / 2
        yStart = display.get_height() / 2 - (self.tileset.tileHeight / 2) * (TILES_PER_SCREEN / 2)

        screenWidth = display.get_width()
        ratio = screenWidth / TILES_PER_SCREEN

        for y in range(TILES_PER_SCREEN):
            for x in range(TILES_PER_SCREEN):
                oX, oY = offset

                oX = ClampValue(oX, 0, mapWidth - TILES_PER_SCREEN)
                oY = ClampValue(oY, 0, mapHeight - TILES_PER_SCREEN)

                adjustedX = x + oX
                adjustedY = y + oY

                try:
                    position = self.map[adjustedY][adjustedX]

                    tileimage = self.tileset.GetTile(position)

                    screenX = xStart + (x - y) * tileimage.get_width() // 2
                    screenY = yStart + (x + y) * tileimage.get_height() // 6

                    rect = (screenX, screenY, self.tileset.tileWidth, self.tileset.tileHeight)

                    if 0 <= x * ratio < display.get_width() and 0 <= y * ratio < display.get_height():
                        sprite = pygame.sprite.Sprite(group)

                        sprite.rect = rect
                        sprite.image = tileimage

                except IndexError:
                    pass

        group.draw(display)





