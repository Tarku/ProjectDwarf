# Building.py

from utils import BASE_BED_SLEEP_RATE, FPS, BASE_BED_MOOD_RATE, MAX_SLEEP, MAX_HYDRATION_LEVEL
from ailment import *

class Building:

    '''
    The Building class.\n
    Use the "bd_" prefix for in-code variable identification.
    '''

    def __init__(self, c_name: str, c_value: float):
        '''

        :param name: The name of the Building
        :param stats: The stats of the Building
        '''

        self.name = c_name
        self.value = c_value

        self.isBeingUsed = False

    def OnUse(self, game, user):
        self.isBeingUsed = True

class RecreationBuilding(Building):
    '''
    The RecreationBuilding class.\n
    Use the "bd_rec_" prefix for in-code variable identification.
    '''
    recreationOffsetPerSecond: float

    def __init__(self, c_name: str, c_value: float, c_recreationOffsetPerSecond: float = 2.5):
        Building.__init__(self, c_name, c_value)

        self.recreationOffsetPerSecond = c_recreationOffsetPerSecond

    def OnUse(self, game, user):
        Building.OnUse(self, game, user)

        user.recreation += (self.recreationOffsetPerSecond / FPS)

class HydrationBuilding(Building):
    '''
    The HydrationBuilding class.\n
    Use the "bd_hyd_" prefix for in-code variable identification.
    '''
    hydrationOffsetPerSecond: float
    isDrinkingSafe: bool

    def __init__(self, c_name: str, c_value: float, c_hydrationOffsetPerSecond: float = 10.0, c_isDrinkingSafe: bool = True):
        Building.__init__(self, c_name, c_value)

        self.hydrationOffsetPerSecond = c_hydrationOffsetPerSecond
        self.isDrinkingSafe = c_isDrinkingSafe

    def OnUse(self, game, user):
        Building.OnUse(self, game, user)

        if not self.isDrinkingSafe:
            user.AttachAilment(alt_Cholera)
            user.hydration = MAX_HYDRATION_LEVEL / 2
        else:
            user.hydration = MAX_HYDRATION_LEVEL


class Bed(Building):
    '''
    The Bed class.\n
    Use the "bd_bed_" prefix for in-code variable identification.
    '''
    comfort: float
    sleepEfficiencyPCT: float

    def __init__(self, c_name: str, c_value: float, c_comfort: float = 0.5, c_sleepEfficiencyPCT: float = .5):
        Building.__init__(self, c_name, c_value)

        self.comfort = c_comfort
        self.sleepEfficiencyPCT = c_sleepEfficiencyPCT

        self.sleepRestaurationRate = (BASE_BED_SLEEP_RATE * self.sleepEfficiencyPCT) / FPS
        self.moodRestaurationRate = (self.comfort * BASE_BED_MOOD_RATE) / FPS

    def OnUse(self, game, user):
        Building.OnUse(self, game, user)

        user.sleep += self.sleepRestaurationRate
        user.mood += self.moodRestaurationRate


bd_hyd_Well = HydrationBuilding(
    c_name="building.well",
    c_value=10.5,
    c_isDrinkingSafe=True,
    c_hydrationOffsetPerSecond=15
)

bd_bed_Ground = Bed(
    c_name="default.ground",
    c_comfort=0.5,
    c_sleepEfficiencyPCT=.70,
    c_value=0
)

bd_bed_WoodenBed = Bed(
    c_name="building.wooden_bed",
    c_comfort=1.5,
    c_sleepEfficiencyPCT=1.2,
    c_value=12.5
)

bd_rec_ChessTable = RecreationBuilding(
    c_name="building.chess_table",
    c_value=15.8,
    c_recreationOffsetPerSecond=2.2
)