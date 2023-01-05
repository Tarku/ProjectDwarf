# Ailment.py

from utils import FPS

class Ailment:
    '''
    The Ailment class for the game.\n
    Use the "alt_" prefix for in-code variable identification.
    '''

    name: str
    initialSeverity: float
    maxSeverity: float
    lethalSeverity: float

    consciousnessOffset: float

    def __init__(self, name: str, initialSeverity: float, maxSeverity: float, lethalSeverity: float, consciousnessOffset: float = 0.0):
        self.name = name
        self.initialSeverity = initialSeverity
        self.maxSeverity = maxSeverity
        self.lethalSeverity = lethalSeverity

        self.consciousnessOffset = consciousnessOffset

    def Update(self, game, person):
        if self not in person.ailments:
            return

        if person.ailments[self] <= self.lethalSeverity:
            return

        deathString = f"ailment.{self.name}"
        person.Die(game, deathString)

    def OnEffect(self, person):
        if self not in person.ailments:
            return

        severity = person.ailments[self]

        person.consciousness -= self.consciousnessOffset * (severity + 1) / FPS


alt_BloodLoss = Ailment(
    name="blood_loss",
    initialSeverity=0.0,
    maxSeverity=1.0,
    lethalSeverity=1.0,
    consciousnessOffset=-2.5
)

alt_Starvation = Ailment(
    name="starvation",
    initialSeverity=0.0,
    maxSeverity=1.0,
    lethalSeverity=1.0,
    consciousnessOffset=-1.5
)