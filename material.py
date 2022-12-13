# Material.py

import pygame

mat_all = []

class Material:

    '''
    The Material class.\n
    Use the "mat_" prefix for in-code variable identification.
    '''

    def __init__(self, name, value):
        self.name = name
        self.value = value

        #self.icon = pygame.image.load(
        #   f"assets\\images\\{name.lower()}.png"
        #)

    def Register(self):
        mat_all.append(self)
        return self


mat_WOOD = Material("material.wood", 2).Register()
mat_STONE = Material("material.stone", 1).Register()
mat_IRON = Material("material.iron", 4).Register()
mat_COPPER = Material("material.copper", 3).Register()
mat_STEEL = Material("material.steel", 6).Register()
mat_SILVER = Material("material.silver", 8).Register()
mat_GOLD = Material("material.gold", 32).Register()