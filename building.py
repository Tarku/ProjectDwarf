# Building.py

from utils import BASE_BED_SLEEP_RATE, FPS, BASE_BED_MOOD_RATE, MAX_SLEEP

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
    moodOffsetPerSecond: float

    def __init__(self, c_name: str, c_value: float, c_moodOffsetPerSecond: float = 0.1):
        Building.__init__(self, c_name, c_value)

        self.moodOffsetPerSecond = c_moodOffsetPerSecond

    def OnUse(self, game, user):
        Building.OnUse(self, game, user)

        user.mood += (self.moodOffsetPerSecond / FPS)


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
    c_moodOffsetPerSecond=1.2
)