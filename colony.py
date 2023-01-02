# Colony.py

from material import *
from faction import *
from itempair import *
from utils import *
from personality import *
from statistics import median, mean
from math import floor

all_colonies = []

class Colony:

    '''
    The Workshop class.\n
    Use the "col_" prefix for in-code variable identification.
    '''

    def __init__(self, name: str, faction: Faction):
        self.name = name

        self.buildings = []
        self.members = []

        self.inventory = {}

        self.beds = []

        self.faction = faction

        self.immigrationMoodNeeded = IMMIGRATION_MOOD_NEEDED
        self.totalMigrantWaves = 0


    def Register(self):
        all_colonies.append(self)
        return self

    def Update(self, game):
        if self.GetAverage("mood") >= self.immigrationMoodNeeded:
            if MIGRANT_ARRIVAL_CHANCE_PCT / FPS >= (randint(1, 10000) / 100):
                migrantCount = self.MigrantsArrival(game)

                for person in self.members:
                    person.DoImmigrationMoodLoss(migrantCount)

                self.immigrationMoodNeeded = IMMIGRATION_MOOD_NEEDED * (self.totalMigrantWaves + 1) * 0.75
                self.immigrationMoodNeeded = ClampValue(self.immigrationMoodNeeded, IMMIGRATION_MOOD_NEEDED, MAX_IMMIGRATION_MOOD_NEEDED)

    def MoodChange(self, count: int):
        for person in self.members:
            person.mood += count * person.moodVariationPCT

    def Populate(self, count: int, genders: list, races: list, minAge: int = 20, maxAge: int = 80):
        for _ in range(count):
            dude = Person(
                name="",
                race=choice(races),
                gender=choice(genders),
                age=randint(minAge, maxAge)
            )
            self.members.append(
                dude
            )

    def GetCountByMaterialType(self):
        temp = {}

        for (item, count) in self.inventory.items():
            itemMaterialType = item.materialType

            if itemMaterialType in temp.keys():
                temp[itemMaterialType] += count
            else:
                temp[itemMaterialType] = count

        return temp

    def MigrantsArrival(self, game, races: [Race] = all_races, genders: [Gender] = all_genders, minNumber: int = 2, maxNumber: int = 5, minAge: int = 20, maxAge: int = 80):
        migrantQuantity = randint(minNumber, maxNumber)

        self.Populate(migrantQuantity, genders=[gd_Masculine, gd_Feminine], races=races, minAge=minAge, maxAge=maxAge)

        self.totalMigrantWaves += 1

        game.eventLog.Add("event.migrants", migrantQuantity, EventMode.POSITIVE)

        return migrantQuantity

    def GetWealth(self):
        wealth = 0

        for (item, count) in self.inventory.items():
            wealth += item.value * count

        for building in self.buildings:
            wealth += building.value

        return wealth

    def GetIdlerNumber(self):
        allIdlers = []
        for person in self.members:
            if not person.isWorking and not person.isAsleep and person.isAlive:
                allIdlers.append(person)
        return len(allIdlers)

    def GetAsleepNumber(self):
        allAsleeps = []
        for person in self.members:
            if person.isAsleep and person.isAlive:
                allAsleeps.append(person)
        return len(allAsleeps)

    def GetAll(self, variableName: str):
        allVars = []
        for person in self.members:
            if person.isAlive:
                value = eval(f"person.{variableName}")
                allVars.append(value)

        return allVars

    def GetMedian(self, variableName: str):
        allVars = self.GetAll(variableName)

        try:
            return round(
                median(
                    allVars
                ) * 2
            ) / 2
        except ValueError:
            return 0

    def GetAverage(self, variableName: str):
        allVars = self.GetAll(variableName)

        try:
            return floor(
                mean(
                    allVars
                )
            )
        except ValueError:
            return 0

    def GetMin(self, variableName: str):
        allVars = self.GetAll(variableName)

        try:
            return floor(
                min(
                    allVars
                )
            )
        except ValueError:
            return 0

    def GetMax(self, variableName: str):
        allVars = self.GetAll(variableName)

        try:
            return floor(
                max(
                    allVars
                )
            )

        except ValueError:
            return 0

    def GiveHeadstart(self):
        for item in all_materials:
            self.inventory[item] = HEADSTART_QUANTITY

    def GetPopulation(self):
        population = 0

        for person in self.members:
            if person.isAlive:
                population += 1

        return population

    def UpdateInventory(self):
        for item in list(self.inventory.keys()):
            count = self.inventory[item]
            if count <= 0:
                self.inventory.pop(item)

    def AddToInventory(self, itemPair: ItemPair):
        item = itemPair.item
        count = itemPair.count

        if item not in self.inventory:
            self.inventory[item] = count
        else:
            self.inventory[item] += count

    def RemoveFromInventory(self, itemPair: ItemPair):
        item = itemPair.item
        count = itemPair.count

        if item not in self.inventory:
            print(
                f"Can't remove {item.name} from inventory. Cause: Item is not in Inventory."
            )
            return

        if count > self.inventory[item]:
            print(
                f"Can't remove {item.name} x{count} from inventory. Cause: Item is not in sufficient quantity."
            )
            return

        self.inventory[item] -= count
        self.UpdateInventory()


    def AddMember(self, member: Person):
        self.members.append(member)