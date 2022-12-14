# Race.py

from random import choice

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

    def __init__(self, name: str, adjective: str, lifeSpan: int, childAge: int, adultAge: int):
        self.name = name
        self.adjective = adjective
        self.lifeSpan = lifeSpan
        self.childAge = childAge
        self.adultAge = adultAge

    def Register(self):
        all_races.append(self)
        return self

    def LoadNames(self):
        formattedRaceName = self.name.removeprefix(
            "race."
        )
        filePath = f"assets\\names\\persons\\{formattedRaceName}.txt"

        try:
            with open(filePath, "r", encoding="utf-8") as file:
                readFile = file.read()
                cutFile = readFile.split("\n")

                cutFile = list(
                    map(lambda x: x.capitalize(), cutFile)
                )

                all_names_by_race[formattedRaceName] = cutFile

        except FileNotFoundError:
            all_names_by_race[formattedRaceName] = ["Dunno McUnknown"]


rc_Human = Race(
    name="race.human",
    adjective="race.adjective.human",
    lifeSpan=75,
    childAge=3,
    adultAge=12
)
rc_Human.Register()
rc_Human.LoadNames()

rc_Dwarf = Race(
    name="race.dwarf",
    adjective="race.adjective.dwarf",
    lifeSpan=180,
    childAge=3,
    adultAge=12
)
rc_Dwarf.Register()
rc_Dwarf.LoadNames()

rc_Vampire = Race(
    name="race.vampire",
    adjective="race.adjective.vampire",
    lifeSpan=800,
    childAge=50,
    adultAge=220
)
rc_Vampire.Register()
rc_Vampire.LoadNames()

rc_HighElf = Race(
    name="race.high_elf",
    adjective="race.adjective.high_elf",
    lifeSpan=450,
    childAge=20,
    adultAge=110
)
rc_HighElf.Register()
rc_HighElf.LoadNames()
