# Drawing/Text.py

from utils import *
import pygame
from pygame.math import Vector2 as Vec

def DisplayText(text: str, position: tuple, color: tuple):
    display = pygame.display.get_surface()

    displayText = DEFAULT_FONT.render(text, FONT_ANTIALIASING, color)
    display.blit(displayText, position)


def DisplayMiddleText(text: str, y: int, color: tuple):
    display = pygame.display.get_surface()

    displayText = DEFAULT_FONT.render(text, FONT_ANTIALIASING, color)
    x = HALF_WIN_WIDTH - (displayText.get_width() / 2)

    display.blit(displayText, Vec(x, y))


def DisplayRightText(text: str, y: int, color: tuple):
    display = pygame.display.get_surface()

    displayText = DEFAULT_FONT.render(text, FONT_ANTIALIASING, color)
    x = WINDOW_WIDTH - displayText.get_width() - EDGE_PADDING

    display.blit(displayText, Vec(x, y))


def DisplayLeftText(text: str, y: int, color: tuple):
    display = pygame.display.get_surface()

    displayText = DEFAULT_FONT.render(text, FONT_ANTIALIASING, color)

    display.blit(displayText, Vec(EDGE_PADDING, y))


def DisplayScreenTitle(text: str, color: tuple):
    display = pygame.display.get_surface()

    displayText = TITLE_FONT.render(text, FONT_ANTIALIASING, color)

    x = HALF_WIN_WIDTH - displayText.get_width() / 2
    display.blit(displayText, Vec(x, EDGE_PADDING))
