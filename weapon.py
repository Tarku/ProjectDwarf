# Weapon.py

from material import *


class Weapon (Material):

    '''
    The Weapon class.\n
    Use the "wp_" prefix for in-code variable identification.
    '''

    def __init__(self, name: str, value: int, stats: dict):
        self.name = name
        self.value = value
        self.stats = stats


wp_DarkScythe = Weapon(
    "Dark Scythe",
    150,
    {
        "AttackDamage": 20
    }
)

