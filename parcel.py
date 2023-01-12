# Parcel.py

from layer import Layer
from pygame import Vector2

class Parcel:
    '''
    The Parcel class for the game.\n
    Use the "pc_" prefix for in-code variable identification.
    '''

    averageHeight: float
    temperature: float
    humidity: float
    layers: list[Layer]

    def __init__(self, averageHeight: float = 0, temperature : float = 0, humidity : float = 0):
        self.averageHeight = averageHeight
        self.temperature = temperature
        self.humidity = humidity

        self.layers = [
            Layer() for _ in range(100)
        ]
