# Faction.py

from random import randint
from person import *
from utils import FactionRelationship, FACTION_SYLLABLES_PATH

all_factions = []
all_faction_types = []

class FactionShell:
    pass

class FactionType:
    name: str
    canWomenRule: bool
    minimumAgeToRule: int

    def __init__(self, c_name: str, c_canWomenRule: bool = True, c_minimumAgeToRule: int = 15):
        self.name = c_name
        self.canWomenRule = c_canWomenRule
        self.minimumAgeToRule = c_minimumAgeToRule

    def Register(self):
        all_faction_types.append(self)
        return self


ft_DemocraticFaction = FactionType(
    "democratic_faction",
    True,
    18
).Register()

ft_DemocraticRepublic = FactionType(
    "democratic_republic",
    True,
    18
).Register()

ft_Republic = FactionType(
    "republic",
    True,
    18
).Register()

ft_FreeState = FactionType(
    "free_state",
    False,
    21
).Register()

ft_Consulate = FactionType(
    "consulate",
    False,
    21
).Register()

ft_Kingdom1 = FactionType(
    "kingdom",
    False,
    32
).Register()

ft_Kingdom2 = FactionType(
    "kingdom",
    True,
    32
).Register()

ft_Empire = FactionType(
    "empire",
    False,
    32
).Register()

class Faction(FactionShell):

    '''
    The Faction class.\n
    Use the "fc_" prefix for in-code variable identification.
    '''
    def __init__(self, c_type: FactionType, c_name: str = "", c_race: Race = rc_Dwarf):
        self.name = c_name
        self.type = c_type

        self.race = c_race

        if self.type.canWomenRule:
            allowedGendersToRule = [gd_Masculine, gd_Feminine]
        else:
            allowedGendersToRule = [gd_Masculine]

        self.leader = Person("", choice(allowedGendersToRule), self.race, randint(self.type.minimumAgeToRule, self.race.lifeSpan))

        self.members = []
        self.members.append(self.leader)

        self.relationships = {}

    def Register(self):
        all_factions.append(self)
        return self

    def GenerateName(self, game):

        randomName = self.race.language.GenerateName()
        raceAdjective = game.localization.Get(self.race.adjective)
        factionTypeName = game.localization.Get(f"factiontype.{self.type.name}")

        possibleStrings = [f"{raceAdjective} {factionTypeName} of {randomName}", f"{randomName} {factionTypeName}"]

        self.name = choice(possibleStrings)



    def AddRelationship(self, otherFaction, relationshipStatus: FactionRelationship):

        if otherFaction in self.relationships.keys():
            print(
                f"Can't add Relationship <{relationshipStatus.name}> to Faction <{self.name}> with Faction <{otherFaction.name}>. Cause: Faction already has another relationship (Current: <{self.relationships[otherFaction]}>.")
            return False

        if self.relationships.get(relationshipStatus) is not None:
            print(
                f"Can't add Relationship <{relationshipStatus.name}> to Faction <{self.name}> with Faction <{otherFaction.name}>. Cause: Relationship already exists."
            )
            return False

        print(
            f"Successfully added Relationship <{relationshipStatus.name}> to Faction <{self.name}> with Faction <{otherFaction.name}>."
        )
        self.relationships[otherFaction] = relationshipStatus
        return True

    def SetRelationship(self, otherFaction: FactionShell, relationshipStatus: FactionRelationship):
        if not otherFaction in self.relationships.keys():
            print(
                f"Can't set Relationship <{relationshipStatus.name}> to Faction <{self.name}> with Faction <{otherFaction.name}>. Cause: Relationship does not exist yet."
            )
            return False

        self.relationships[otherFaction] = relationshipStatus
        print(
            f"Successfully set Relationship <{relationshipStatus.name}> to Faction <{self.name}> with Faction <{otherFaction.name}>."
        )

        return True

    def RemoveRelationship(self, otherFaction: FactionShell, relationshipStatus: FactionRelationship):
        if not otherFaction in self.relationships.keys():
            print(
                f"Can't remove Relationship <{relationshipStatus.name}> from Faction <{self.name}> with Faction <{otherFaction.name}>. Cause: Relationship does not exist."
            )
            return False

        if self.relationships.get(otherFaction) is not relationshipStatus:
            print(
                f"Can't remove Relationship <{relationshipStatus.name}> from Faction <{self.name}> with Faction <{otherFaction.name}>. Cause: Relationship mismatch (Current relationship: <{self.relationships.get(otherFaction).name}>."
            )
            return False

        del(
            self.relationships[otherFaction]
        )
        print(
            f"Successfully removed Relationship <{relationshipStatus.name}> from Faction <{self.name}> with Faction <{otherFaction.name}>."
        )
        return True

    def GetRelationship(self, otherFaction: FactionShell):
        if not otherFaction in self.relationships.keys():
            print(
                f"Can't get Relationship from Faction <{self.name}> with Faction <{otherFaction.name}>. Cause: Relationship does not exist."
            )
            return None

        print(
            f"Successfully got Relationship from Faction <{self.name}> with Faction <{otherFaction.name}>."
        )
        return self.relationships.get(otherFaction)

