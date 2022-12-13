# LocalizedString.py

from languages import *
from options import *

class Localization:
    language = None
    languageData: Options

    def __init__(self, language = lang_English):
        self.language = language

        self.LoadData()

    def SetLanguage(self, language: (str, Language)):
        self.language = language
        self.LoadData()

    def LoadData(self):
        if type(self.language) is str:
            self.languageData = Options(
                f"locale\\{self.language}.txt"
            )

        elif type(self.language) is Language:
            self.languageData = Options(
                f"locale\\{self.language}.txt"
            )

        else:
            print(
                f"Cannot load localization data. Cause: Unknown attribute type."
            )

    def Get(self, string: str, formatArguments = None):
        formattedString = None

        if string not in self.languageData.data:
            print(
                f"Cannot get localization string <{string}>."
            )
            return string

        if formatArguments is None:
            formattedString = self.languageData.data[string]

            return formattedString

        try:
            formattedString = self.languageData.data[string] % formatArguments

        except TypeError:
            formattedString = self.languageData.data[string]

        return formattedString

    def GetFormatted(self, string: str, formatArguments: tuple):
        formattedString = None

        if string not in self.languageData.data:
            print(
                f"Cannot get localization string <{string}>."
            )
            return string

        try:

            formattedString = self.languageData.data[string] % formatArguments

        except TypeError:

            formattedString = self.languageData.data[string]

        return formattedString

    def Replace(self, source):
        pass




