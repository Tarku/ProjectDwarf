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
        word = randomStructure = choice(self.wordStructures)

        consonantCount = randomStructure.count("C")
        vowelCount = randomStructure.count("V")

        for _ in range(consonantCount):
            word = word.replace("C", choice(self.consonants), 1)

        for _ in range(vowelCount):
            word = word.replace("V", choice(self.vowels), 1)

        return word.capitalize()


nl_Humanish = NamingLanguage(
    c_vowels=["a", "e", "i", "o", "u"],
    c_consonants=["k", "p", "s", "t", "w", "l", "j", "m", "n"],
    c_wordStructures=["CV", "CVn", "CVCVn", "VCV", "VCVn", "CVCVCVn"]
)

nl_Dwarvish = NamingLanguage(
    c_vowels=["â", "î", "û", "a", "i", "u"],
    c_consonants=["sh", "t", "k", "b", "d", "j", "h", "kh", "gh", "t'", "s'", "z'", "q", "r", "s", "z", "y", "l", "f", "th", "dh", "2", "3", "w"],
    c_wordStructures=["CVCVC", "CVCV", "VnCVC"]
)

nl_Vampirish = NamingLanguage(
    c_vowels=["a", "e", "o", "u", "y", "i"],
    c_consonants=["g", "t", "j", "k", "m", "mh", "n"],
    c_wordStructures=["VCVC", "CVCula", "VCVck", "VrCVCula"]
)

nl_HighElvish = NamingLanguage(
    c_vowels=["a", "e", "é", "o", "ó́", "u", "i"],
    c_consonants=["l", "m", "n", "r", "p", "t", "k", "b", "d", "g", "y", "w"],
    c_wordStructures=["VCVCë", "CVCVCë", "VrCV", "VrCVCë"]
)
