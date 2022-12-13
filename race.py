# Race.py

all_races = []

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


rc_Human = Race(
    name="race.human",
    adjective="race.adjective.human",
    lifeSpan=75,
    childAge=3,
    adultAge=12
)
rc_Human.Register()

rc_Dwarf = Race(
    name="race.dwarf",
    adjective="race.adjective.dwarf",
    lifeSpan=180,
    childAge=3,
    adultAge=12
)
rc_Dwarf.Register()

rc_Vampire = Race(
    name="race.vampire",
    adjective="race.adjective.vampire",
    lifeSpan=800,
    childAge=50,
    adultAge=220
)
rc_Vampire.Register()

rc_HighElf = Race(
    name="race.high_elf",
    adjective="race.adjective.high_elf",
    lifeSpan=450,
    childAge=20,
    adultAge=110
)
rc_HighElf.Register()
