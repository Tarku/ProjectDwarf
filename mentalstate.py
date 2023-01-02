# MentalState.py
from random import randint

from utils import MIN_BERSERK_LEVEL, MAX_BERSERK_LEVEL

class MentalState:

    '''
    The MentalState class for the game.\n
    Use the "mst_" prefix for in-code variable identification.
    '''

    name: str
    moodMin: float
    moodMax: float

    minLength: int
    maxLength: int

    def __init__(self, c_name: str, c_moodMin: float, c_moodMax: float, c_minLength: int, c_maxLength: int):
        self.name = c_name

        self.moodMin = c_moodMin
        self.moodMax = c_moodMax

        self.minLength = c_minLength
        self.maxLength = c_maxLength


    def ApplyOn(self, person):
        person.mentalState = self
        person.mentalStateTimer = randint(self.minLength, self.maxLength)

    def Update(self, person):
        pass


class Berserk(MentalState):
    def __init__(self):
        MentalState.__init__(self, c_name="mental_state.berserk", c_moodMin=MIN_BERSERK_LEVEL, c_moodMax=MAX_BERSERK_LEVEL, c_minLength=1200, c_maxLength=4500)