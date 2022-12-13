# Faction.py

from random import randint
from person import *
from utils import FactionRelationship, FACTION_SYLLABLES_PATH

all_factions = []

class FactionShell:
    pass

class Faction(FactionShell):

    '''
    The Faction class.\n
    Use the "fc_" prefix for in-code variable identification.
    '''

    def __init__(self, name = ""):
        self.name = name

        self.members = []

        self.relationships = {}

    def Register(self):
        all_factions.append(self)
        return self

    def GenerateName(self, minLength = 1, maxLength = 4):
        '''
        Generates a random name for the faction from the syllables in assets/names/factions.txt .
        '''

        tempName = ""

        randomNumber = randint(minLength, maxLength + 1)
        syllableFile = open(FACTION_SYLLABLES_PATH, 'r', encoding='utf-8')

        uncutSyllables = syllableFile.read()
        cutSyllables = uncutSyllables.split("\n")

        syllablesCount = len(cutSyllables)

        for _ in range(randomNumber):
            syllableNo = randint(0, syllablesCount)
            tempName += cutSyllables[syllableNo - 1]

        self.name = tempName

        syllableFile.close()

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

