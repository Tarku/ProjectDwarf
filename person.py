# Person.py

from random import randint, choice
from personality import Personality, all_personalities
from gender import *
from race import *

all_persons = []

class Person:

    '''
    The Person class.\n
    Use the "ps_" prefix for in-code variable identification.
    '''

    name: str
    age: int
    isWorking: bool
    personality: Personality
    mood: int
    gender: Gender
    race: Race

    def __init__(self, name: str, gender: Gender, race: Race = rc_Dwarf, age: int = 20, personality: Personality = None):
        self.name = name
        self.isWorking = False

        self.age = age
        self.gender = gender

        self.race = race

        self.pronoun = gender.pronoun

        if personality is None:
            self.personality = choice(all_personalities)
        else:
            self.personality = personality

        self.mood = 0

    def Register(self):
        all_persons.append(self)
        return self

    def GetPersonalityString(self):
        return self.personality.name

    def GetGenderSymbol(self):
        return self.gender.symbol

    def GetAgeName(self):
        if self.age > self.race.adultAge:
            return "age.adult"
        elif self.age > self.race.childAge:
            return "age.child"
        else:
            return "age.baby"
