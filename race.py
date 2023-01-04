# Race.py

from random import choice
from naminglanguage import *

all_races = []
all_names_by_race = {}

class Race:
    '''
    The Race class for the game.\n
    Use the "rc_" prefix for in-code variable identification.
    '''

    name: str
    adjective: str
    lifeSpan: int
    childAge: int
    adultAge: int
    language: NamingLanguage

    def __init__(self, c_name: str, c_adjective: str, c_lifeSpan: int, c_childAge: int, c_adultAge: int, c_language: NamingLanguage):
        self.name = c_name
        self.adjective = c_adjective
        self.lifeSpan = c_lifeSpan
        self.childAge = c_childAge
        self.adultAge = c_adultAge
        self.language = c_language

    def Register(self):
        all_races.append(self)
        return self


rc_Human = Race(
    c_name="race.human",
    c_adjective="race.adjective.human",
    c_lifeSpan=75,
    c_childAge=3,
    c_adultAge=12,
    c_language=nl_Humanish
)
rc_Human.Register()

rc_Dwarf = Race(
    c_name="race.dwarf",
    c_adjective="race.adjective.dwarf",
    c_lifeSpan=180,
    c_childAge=3,
    c_adultAge=12,
    c_language=nl_Dwarvish
)
rc_Dwarf.Register()

rc_Vampire = Race(
    c_name="race.vampire",
    c_adjective="race.adjective.vampire",
    c_lifeSpan=800,
    c_childAge=50,
    c_adultAge=220,
    c_language=nl_Vampirish
)
rc_Vampire.Register()

rc_HighElf = Race(
    c_name="race.high_elf",
    c_adjective="race.adjective.high_elf",
    c_lifeSpan=450,
    c_childAge=20,
    c_adultAge=110,
    c_language=nl_HighElvish
)
rc_HighElf.Register()
