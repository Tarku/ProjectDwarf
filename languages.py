# Languages.py

all_languages = []

class Language:
    '''
    The Language class for the game.\n
    Use the "lang_" prefix for in-code variable identification.
    '''

    def __init__(self, name):
        self.name = name

    def Register(self):
        all_languages.append(self)
        return self


lang_English = Language("English").Register()
lang_French = Language("French").Register()
lang_German = Language("German").Register()
lang_Spanish = Language("Spanish").Register()