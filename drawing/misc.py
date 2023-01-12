# Drawing/Misc.py

import pygame
from pygame.surface import Surface
from pygame.math import Vector2
from utils import *

def DisplayHorizontalLine(color: tuple, yPosition: int, width: int = 2):
    display = pygame.display.get_surface()

    horizontalLine = Surface((WINDOW_WIDTH, width))
    horizontalLine.fill(color)

    display.blit(horizontalLine, Vector2(0, yPosition - width / 2))

def DisplayBackground(color: tuple, yPosition: int, width: int = 25, opacity: int = 127):
    display = pygame.display.get_surface()

    background = Surface((WINDOW_WIDTH, width))
    background.fill(color)
    background.set_alpha(opacity)

    display.blit(background, Vector2(0, yPosition))
