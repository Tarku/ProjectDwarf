# Person.py

from random import randint, choice, uniform, gauss, sample
from math import cos

from mentalstate import MentalState
from personality import Personality, all_personalities
from gender import *
from race import *
from material import *
from utils import *
from building import *
from ailment import *
from itempair import *
from statistics import median
from eventlog import EventMode

all_persons = []

class Person:

    '''
    The Person class.\n
    Use the "ps_" prefix for in-code variable identification.
    '''

    name: str
    age: int
    isWorking: bool
    isAlive: bool
    isAsleep: bool

    personality: Personality

    mood: float
    foodLevel: float
    sleep: float

    gender: Gender
    race: Race

    mentalState: MentalState

    def __init__(
            self, name: str, gender: Gender, race: Race = rc_Dwarf, age: int = 20, personality: Personality = None):
        self.name = name

        self.isWorking = False
        self.isAsleep = False
        self.isAlive = True

        self.lookingForSocializationMate = False

        self.age = age
        self.gender = gender

        self.ailments = {}  # {Ailment: Severity}

        self.opinions = {}
        self.unitCompability = {}

        self.race = race

        self.foodLevel = MAX_FOOD_LEVEL
        self.sleep = MAX_SLEEP
        self.hydration = MAX_HYDRATION_LEVEL
        self.consciousness = MAX_CONSCIOUSNESS

        self.introvertness = uniform(MIN_INTROVERTNESS, MAX_INTROVERTNESS)
        self.xenophobia = uniform(MIN_XENOPHOBIA, MAX_XENOPHOBIA)
        self.racism = uniform(MIN_RACISM, MAX_RACISM)

        self.tact = gauss(1, 0.5)

        self.socializeTimer = self.introvertness * BASE_SOCIALIZE_TIMER

        self.mentalStateTimer = 0
        self.mood = 0

        self.pronoun = gender.pronoun

        if personality is None:
            self.personality = choice(all_personalities)
        else:
            self.personality = personality

        if self.name == "":
            self.name = self.GenerateRandomName()
        else:
            self.name = name

        self.hungerVariationPCT = uniform(MIN_VARIATION, MAX_VARIATION)
        self.moodVariationPCT = uniform(MIN_VARIATION, MAX_VARIATION)
        self.hydrationVariationPCT = uniform(MIN_VARIATION, MAX_VARIATION)
        self.sleepVariationPCT = uniform(MIN_VARIATION, MAX_VARIATION)

        self.hungerDivisor = 1

        self.hungerState = HungerState.FED

        self.foodLossPerFrame = (HUNGER_LOSS_RATE * self.hungerVariationPCT) / FPS
        self.moodLossPerFrame = (MOOD_LOSS_RATE * self.moodVariationPCT) / FPS

    def Register(self):
        all_persons.append(self)
        return self

    def DoImmigrationMoodLoss(self, migrantCount: int):
        self.mood -= IMMIGRATION_MOOD_LOST * self.moodVariationPCT * (migrantCount / 2) * self.xenophobia

    def TryEat(self, game):
        for item in list(game.colony.inventory.keys()):
            if isinstance(item, FoodItem):
                item.OnEat(eater=self, game=game)
                game.colony.inventory[item] -= 1
                return True
        return None

    def UseBedUntilMaxSleep(self, game, bed, isGround: bool = False):
        if self.sleep < MAX_SLEEP:
            bed.OnUse(game, self)

            if not isGround:
                bed.isBeingUsed = True

            self.isAsleep = True
        else:
            if not isGround:
                bed.isBeingUsed = False

            self.isAsleep = False

    def TrySleep(self, game):

        for bed in game.colony.beds:
            if bed.isBeingUsed:
                continue
            else:
                self.UseBedUntilMaxSleep(game, bed)
                return True

        self.UseBedUntilMaxSleep(game, bd_bed_Ground, isGround=True)
        return True

    def ResetSocializationTimer(self):
        self.socializeTimer = self.introvertness * BASE_SOCIALIZE_TIMER

    def ResetSocializationStatus(self):
        self.lookingForSocializationMate = False

    def ResetSocialization(self):
        self.ResetSocializationTimer()
        self.ResetSocializationStatus()

    def SocializationAndOpinionChange(self, game, otherParticipant: 'Person', offset: float):
        self.ResetSocialization()
        otherParticipant.ResetSocialization()

        self.ChangeOpinion(otherParticipant, offset)

    def GetDeepTalkChance(self, otherPerson: 'Person'):
        if otherPerson not in self.opinions.keys():
            return 0

        if self.opinions[otherPerson] < 0:
            return 0

        else:
            return (self.opinions[otherPerson] / 100) * 2


    def TrySocialize(self, game):
        otherParticipant: 'Person' = choice(game.colony.members)

        if otherParticipant is self:
            return

        if not otherParticipant.lookingForSocializationMate:
            return

        if self.isAsleep or otherParticipant.isAsleep:
            return

        if self.isWorking or otherParticipant.isWorking:
            return

        if not self.isAlive:
            return

        if not otherParticipant.isAlive:
            return

        randomChance = uniform(0.0, 1.0)
        if self.GetDeepTalkChance(otherParticipant) >= randomChance:
            self.SocializationAndOpinionChange(game, otherParticipant, DEEP_TALK_OPINION_GAIN)
            game.eventLog.Add(
                "event.deep_talk",
                (
                    self.name,
                    otherParticipant.name,
                    self.opinions[otherParticipant]
                ),
                EventMode.POSITIVE
            )

        else:
            if self.race is not otherParticipant.race:
                self.SocializationAndOpinionChange(game, otherParticipant, CHITCHAT_OPINION_GAIN * (1 / self.racism))
            else:
                self.SocializationAndOpinionChange(game, otherParticipant, CHITCHAT_OPINION_GAIN)

            game.eventLog.Add(
                "event.chitchat",
                (
                    self.name,
                    otherParticipant.name,
                    self.opinions[otherParticipant]
                ),
                EventMode.INFO
            )

    def Die(self, game, reason):
        self.isAlive = False

        deathString = f"death.{reason}"

        game.colony.MoodChange(-4)
        game.colony.AddToInventory(
            ItemPair(
                CorpseItem(
                    owner=self,
                    localization=game.localization
                ),
                1
            )
        )

        game.eventLog.Add(deathString, self.name, EventMode.PERIL)

    def UpdateAilments(self, game):
        if self.ailments:
            for ailment in self.ailments:
                ailment.Update(game, self)
                ailment.OnEffect(self)

    def UpdateLevels(self, game):
        self.foodLevel -= self.foodLossPerFrame / self.hungerDivisor

        self.mood -= self.moodLossPerFrame

        self.socializeTimer -= 1 / FPS

        if not self.isAsleep:
            self.sleep -= (SLEEP_LOSS_RATE * self.sleepVariationPCT) / FPS

        self.mood = ClampValue(self.mood, MIN_MOOD, MAX_MOOD)
        self.foodLevel = ClampValue(self.foodLevel, MIN_FOOD_LEVEL, MAX_FOOD_LEVEL)
        self.sleep = ClampValue(self.sleep, MIN_SLEEP, MAX_SLEEP)

    def ChangeOpinion(self, other: 'Person', value: float):
        if other in self.opinions:
            self.opinions[other] += value
        else:
            self.opinions[other] = value

    def AttachAilment(self, ailment: Ailment):
        self.ailments[ailment] = ailment.initialSeverity

    def WorsenAilment(self, ailment: Ailment, amountPerSecond: float):
        if ailment not in self.ailments:
            print(
                f"Can't Worsen Ailment <{ailment.name}> on Person <{self.name}>. Cause: Person doesn't have this ailment."
            )
            return

        self.ailments[ailment] += amountPerSecond

    def RemoveAilment(self, ailment: Ailment):
        if ailment not in self.ailments:
            return

        self.ailments.pop(ailment)

    def CheckLevels(self, game):
        if self.socializeTimer <= 0:
            self.lookingForSocializationMate = True
            self.TrySocialize(game)

        if self.foodLevel > EAT_ACTION_PCT:
            self.RemoveAilment(alt_Starvation)
            self.hungerState = HungerState.FED

        if self.foodLevel <= EAT_ACTION_PCT:
            game.colony.UpdateInventory()
            attempt = self.TryEat(game)

            if not attempt and self.hungerState == HungerState.FED:
                self.mood -= 6
                self.hungerDivisor += 1
                self.hungerState = HungerState.HUNGRY

        if self.foodLevel <= EAT_ACTION_PCT / 2 and self.hungerState == HungerState.HUNGRY:
            self.mood -= 12
            self.hungerDivisor += 1
            self.hungerState = HungerState.RAVENOUSLY_HUNGRY

        if self.foodLevel <= 0 and self.hungerState == HungerState.RAVENOUSLY_HUNGRY:
            self.mood -= 20
            self.hungerDivisor += 1
            self.hungerState = HungerState.MALNOURISHED

            self.AttachAilment(alt_Starvation)

        if self.foodLevel <= 0 and self.hungerState == HungerState.MALNOURISHED:
            self.WorsenAilment(alt_Starvation, MALNUTRITION_WORSENING / 60)

        if self.sleep <= SLEEP_ACTION_PCT and not self.isAsleep:
            self.TrySleep(game)

        if self.isAsleep:
            self.TrySleep(game)

        if self.sleep <= 0:
            self.Die(game, "insomnia")

    def Update(self, game):
        if self.isAlive:
            self.UpdateAilments(game)
            self.CheckLevels(game)
            self.UpdateLevels(game)

    def GenerateRandomName(self):
        formattedRaceName = self.race.name.removeprefix(
            "race."
        )
        return choice(
            all_names_by_race.get(formattedRaceName)
        )

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
