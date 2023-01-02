# ItemQuality.py

class ItemQuality:

    '''
    The ItemQuality class for the game.
    Use the "iq_" prefix for in-code variable identification.
    '''

    name: str
    valueIncidence: float

    def __init__(self, name: str, valueIncidence: float):
        self.name = name
        self.valueIncidence = valueIncidence


iq_UnconceivablyBad = ItemQuality(
    "quality.unconceivably_bad",
    0.01
)

iq_Terrible = ItemQuality(
    "quality.terrible",
    0.05
)

iq_Awful = ItemQuality(
    "quality.awful",
    0.25
)

iq_Poor = ItemQuality(
    "quality.poor",
    0.75
)

iq_Base = ItemQuality(
    "quality.normal",
    1.0
)

iq_Good = ItemQuality(
    "quality.good",
    1.75
)

iq_Excellent = ItemQuality(
    "quality.excellent",
    2.5
)

iq_Masterwork = ItemQuality(
    "quality.masterwork",
    5.0
)

iq_Legendary = ItemQuality(
    "quality.legendary",
    10.0
)