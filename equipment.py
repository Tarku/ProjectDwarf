# Equipment.py

from enum import Enum
from material import Material

class EquipmentSlot(Enum):
    LEFT_HAND = 0
    RIGHT_HAND = 1
    HEAD = 2
    BODY = 3
    BELT = 4
    LEGS = 5
    FEET = 6

class EquipmentStats:
    # Weapon specific
    bluntDamage: float
    sharpDamage: float

    # Armor specific
    baseDamageAbsorption: float
    bluntProtection: float
    sharpProtection: float
    coverage: float

    def __init__(self, c_bluntDamage = -1.0, c_sharpDamage = -1.0, c_baseDamageAbsorption = -1.0, c_bluntProtection = -1.0, c_sharpProtection = -1.0, c_coverage = -1.0):
        self.bluntDamage = c_bluntDamage
        self.sharpDamage = c_sharpDamage

        self.baseDamageAbsorption = c_baseDamageAbsorption
        self.bluntProtection = c_bluntProtection
        self.sharpProtection = c_sharpProtection
        self.coverage = c_coverage


class Equipment(Material):
    equipmentSlot: list[EquipmentSlot]
    equipmentStats: EquipmentStats

    def __init__(self, c_name: str, c_value: int, c_equipmentSlot: list[EquipmentSlot], c_equipmentStats: EquipmentStats):
        Material.__init__(self, c_name, c_value)
        self.equipmentSlot = c_equipmentSlot
        self.equipmentStats = c_equipmentStats


