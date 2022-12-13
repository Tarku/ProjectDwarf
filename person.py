# Person.py

all_persons = []

class Person:

    '''
    The Person class.\n
    Use the "ps_" prefix for in-code variable identification.
    '''

    def __init__(self, name):
        self.name = name
        self.isWorking = False

        self.mood = 0

    def Register(self):
        all_persons.append(self)
        return self