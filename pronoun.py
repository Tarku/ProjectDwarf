# Pronoun.py

from gender import *

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
            self, base: str):

        self.subject = f"pronoun.{base}.subject"
        self.object = f"pronoun.{base}.object"
        self.reflexive = f"pronoun.{base}.reflexive"
        self.possessive = f"pronoun.{base}.possessive_adjective"
        self.possessivePronoun = f"pronoun.{base}.possessive_pronoun"
