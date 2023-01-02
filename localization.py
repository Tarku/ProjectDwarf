# LocalizedString.py
import collections

from languages import *
from options import *
from utils import SplitGet
from collections import *


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

    def RoundValue(self, value: float):
        return round(value, 1)

    def Get(self, string: str, formatArguments = None):
        formattedString = None

        if string not in self.languageData.data:
            print(f"Cannot get localization string <{string}>.")
            return string

        if formatArguments is None:
            formattedString = self.languageData.data[string]

            return formattedString

        if isinstance(formatArguments, (list, tuple)):
            formatArguments = list(formatArguments)

            for arg in list(formatArguments):
                if isinstance(arg, float):
                    formatArguments[formatArguments.index(arg)] = self.RoundValue(arg)

            formattedString = self.languageData.data[string].format(*formatArguments)
        else:
            if isinstance(formatArguments, float):
                formatArguments = self.RoundValue(formatArguments)

            formattedString = self.languageData.data[string].format(formatArguments)
        '''try:

        except TypeError:
            formattedString = self.languageData.data[string]'''

        return formattedString
