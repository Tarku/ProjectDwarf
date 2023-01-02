# Options.py

from utils import *

class Options:
    '''
    The Options class of the game.
    Use the "op_" prefix for in-code variable identification.
    '''

    lines = []
    data = {}
    filename : str

    def __init__(self, filename = "options.txt"):
        self.filename = filename
        try:
            self.file = open(filename, encoding="utf-8")

            self.read = self.file.read()

            self.lines = self.read.split("\n")

            if not self.lines:
                print("Empty file.")

            for line in self.lines:

                if not (line.startswith(COMMENT_SYMBOL) or not line):

                    # print(line)

                    split_line = line.split(SEPARATOR)

                    name = split_line[0]
                    value = split_line[1]

                    name = name.lower()

                    if value.isnumeric():
                        value = int(value)

                    self.data[name] = value
                else:
                    continue

        except FileNotFoundError:
            print(
                f"Cannot open file <{filename}>. Cause: File does not exist."
            )

    def Get(self, string: str):
        if string not in self.data.keys():
            print(
                f"Cannot find string <{string}> in options file <{self.filename}>."
            )
            return None

        return self.data[string]

    def GetList(self, string: str, separator: str = SEPARATOR):
        if string not in self.data.keys():
            print(
                f"Cannot find string <{string}> in options file <{self.filename}>."
            )
            return None

        returnValue = self.data[string].split(separator)
        return returnValue

    def GetBool(self, string: str):
        if string not in self.data.keys():
            print(
                f"Cannot find string <{string}> in options file <{self.filename}>."
            )
            return None

        value = self.data[string]
        result : bool = False

        if value.capitalize() == TRUE:
            result = True

        elif value.capitalize() == FALSE:
            result = False

        return result
