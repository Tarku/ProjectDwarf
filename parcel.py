# Parcel.py

class Parcel:
    averageHeight : float
    temperature : float
    humidity : float

    def __init__(self, averageHeight : float, temperature : float, humidity : float):
        self.averageHeight = averageHeight
        self.temperature = temperature
        self.humidity = humidity
