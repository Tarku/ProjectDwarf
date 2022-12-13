# Person.py

from random import randint, choice
from personality import Personality, all_personalities
from utils import GenderType
from pronoun import *

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
    gender: GenderType
    pronoun: Pronoun

    def __init__(self, name: str, gender: GenderType, age: int = 20, personality: Personality = None):
        self.name = name
        self.isWorking = False

        self.age = age
        self.gender = gender

        self.pronoun = pronounsByGender.get(
            self.gender
        )

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