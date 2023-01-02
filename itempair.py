# ItemPair.py

from material import *

class ItemPair:

    '''
    The ItemPair class.
    Use the "ip_" prefix for in-code identification.
    '''

    def __init__(self, item: Material, count: int):
        self.item = item
        self.count = count

    def __str__(self):
        return f'{self.item.name} x{self.count}'
