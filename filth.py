# Filth.py

class Filth:
    '''
    The Filth class.\n
    Use the "flt_" prefix for in-code variable identification.
    '''

    name: str
    doesPolluteWater: bool

    def __init__(self, c_name: str, c_doesPolluteWater: bool):
        self.name = c_name
        self.doesPolluteWater = c_doesPolluteWater

