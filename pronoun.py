# Pronoun.py

from utils import GenderType

class Pronoun:
    '''
    The Pronoun class for the game.\n
    Use the "pr_" prefix for in-game variable identification.
    '''

    subject: str  # He She They It
    object: str  # Him Her Them It
    reflexive: str  # Himself Herself Themselves Itself
    possessive: str # His Her Their Its
    possessivePronoun: str  # His Hers Theirs Its

    def __init__(
            self,
            subjectForm: str,
            objectForm: str,
            reflexiveForm: str,
            possessiveForm: str,
            possessivePronounForm: str):

        self.subject = subjectForm
        self.object = objectForm
        self.reflexive = reflexiveForm
        self.possessive = possessiveForm
        self.possessivePronoun = possessivePronounForm


pr_Masculine = Pronoun(
    "pronoun.masculine.subject",
    "pronoun.masculine.object",
    "pronoun.masculine.reflexive",
    "pronoun.masculine.possessive_adjective",
    "pronoun.masculine.possessive_pronoun",
)

pr_Feminine = Pronoun(
    "pronoun.feminine.subject",
    "pronoun.feminine.object",
    "pronoun.feminine.reflexive",
    "pronoun.feminine.possessive_adjective",
    "pronoun.feminine.possessive_pronoun",
)

pr_Neuter = Pronoun(
    "pronoun.neuter.subject",
    "pronoun.neuter.object",
    "pronoun.neuter.reflexive",
    "pronoun.neuter.possessive_adjective",
    "pronoun.neuter.possessive_pronoun",
)

pr_Inanimate = Pronoun(
    "pronoun.inanimate.subject",
    "pronoun.inanimate.object",
    "pronoun.inanimate.reflexive",
    "pronoun.inanimate.possessive_adjective",
    "pronoun.inanimate.possessive_pronoun",
)

pronounsByGender = {
    GenderType.MASCULINE: pr_Masculine,
    GenderType.FEMININE: pr_Feminine,
    GenderType.NEUTER: pr_Neuter,
    GenderType.INANIMATE: pr_Inanimate
}