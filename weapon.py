# Weapon.py

from equipment import *


class Weapon (Equipment):

    '''
    The Weapon class.\n
    Use the "wp_" prefix for in-code variable identification.
    '''

    def __init__(self, name: str, value: int, weaponStats: EquipmentStats):
        Equipment.__init__(self, name, value, [EquipmentSlot.LEFT_HAND, EquipmentSlot.RIGHT_HAND], weaponStats)


wp_DarkScythe = Weapon(
    "weapon_darkscythe",
    150,
    weaponStats=EquipmentStats(
        c_bluntDamage=0.15,
        c_sharpDamage=0.45
    )
)

