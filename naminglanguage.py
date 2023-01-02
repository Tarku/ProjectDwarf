# NamingLanguage.py

from random import choice

class NamingLanguage:
    vowels = []
    consonants = []

    wordStructures = []

    def __init__(self, c_vowels: list, c_consonants: list, c_wordStructures: list):
        self.vowels = c_vowels
        self.consonants = c_consonants

        self.wordStructures = c_wordStructures

    def GenerateName(self):
        randomStructure = choice(self.wordStructures)



