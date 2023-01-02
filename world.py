# World.py


from perlin_noise import PerlinNoise
from time import time as fTime
from numpy import arange
from os import mkdir
from pygame.surface import Surface
from options import Options
from pygame import image, display, sprite, transform
from utils import *
from math import floor
from drawing.tileset import *
from drawing.isometricview import *

class World:

    '''
    The World class for the game.\n
    Use the "wld_" prefix for in-code variable identification.
    '''

    heightmap : list
    temperatureMap : list
    humidityMap : list

    heightTiles : list
    temperatureTiles : list

    heightTemperatureTiles : list

    screen: Surface

    isometricView: IsometricView

    def __init__(self, screen: Surface, seed: int = fTime()):
        self.seed = seed

        self.screen = screen

        self.options = Options(
            "options.txt"
        )
        self.worldgenOptions = Options(
            "worldgen.txt"
        )

        self.mapTileset = Tileset("assets\\images\\iso_tileset.png", 64, 96)

        # Height related
        self.mountainsLevel = float(
            self.worldgenOptions.Get("mountains_level")
        )
        self.hillsLevel = float(
            self.worldgenOptions.Get("hills_level")
        )
        self.seaLevel = float(
             self.worldgenOptions.Get("sea_level")
        )
        self.deepSeaLevel = float(
             self.worldgenOptions.Get("deep_sea_level")
        )

        # Temperature related
        self.hotLevel = float(
             self.worldgenOptions.Get("hot_level")
        )
        self.warmLevel = float(
             self.worldgenOptions.Get("warm_level")
        )
        self.temperateLevel = float(
             self.worldgenOptions.Get("temperate_level")
        )
        self.coldLevel = float(
             self.worldgenOptions.Get("cold_level")
        )
        self.freezingLevel = float(
             self.worldgenOptions.Get("freezing_level")
        )

        self.width = self.worldgenOptions.Get("width")
        self.height = self.worldgenOptions.Get("height")

        self.verboseLogging = self.options.GetBool("verbose_logging")

        self.size = (
            self.width,
            self.height
        )

        self.octaves = self.worldgenOptions.Get("octaves")

        self.perlins = [PerlinNoise(seed=seed, octaves=self.octaves / i) for i in range(1, 6)]
        self.humidityNoise = PerlinNoise(seed=seed, octaves = 12)

        self.mapTileset.Load(display=screen)

    def JoinTileInfo(self):
        self.heightTemperatureTiles = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]

        for y in range(self.height):
            for x in range(self.width):
                height = self.heightTiles[y][x]
                temperature = self.temperatureTiles[y][x]

                self.heightTemperatureTiles[y][x] = (temperature, height)

        self.isometricView = IsometricView(self.heightTemperatureTiles, self.mapTileset)

    def DumpToFile(self):
        dumpedHeightmap = ""
        dumpedTemperatureMap = ""
        dumpedHumidityMap = ""

        for y in range(self.height):
            for x in range(self.width):
                if self.heightmap[y][x] > float(self.mountainsLevel):
                    dumpedHeightmap += "Δ"
                elif self.heightmap[y][x] > float(self.hillsLevel):
                    dumpedHeightmap += "▵"
                elif self.heightmap[y][x] > float(self.lowHillsLevel):
                    dumpedHeightmap += "."
                elif self.heightmap[y][x] > float(self.seaLevel):
                    dumpedHeightmap += "'"
                else:
                    dumpedHeightmap += "-"

                if self.temperatureMap[y][x] > float(self.hotLevel):
                    dumpedTemperatureMap += "H"
                elif self.temperatureMap[y][x] > float(self.warmLevel):
                    dumpedTemperatureMap += "W"
                elif self.temperatureMap[y][x] > float(self.temperateLevel):
                    dumpedTemperatureMap += "T"
                elif self.temperatureMap[y][x] > float(self.coldLevel):
                    dumpedTemperatureMap += "C"
                else:
                    dumpedTemperatureMap += "F"

                if self.humidityMap[y][x] > 0.8:
                    dumpedHumidityMap += "H"
                elif self.humidityMap[y][x] > 0.4:
                    dumpedHumidityMap += "W"
                elif self.humidityMap[y][x] > -0.4:
                    dumpedHumidityMap += "M"
                elif self.humidityMap[y][x] > -0.8:
                    dumpedHumidityMap += "D"
                else:
                    dumpedHumidityMap += "A"

            dumpedHeightmap += "\n"
            dumpedTemperatureMap += "\n"
            dumpedHumidityMap += "\n"

        mkdir(f'dumps/{int(fTime())}')

        heightmapFileName = f'dumps/{int(fTime())}/heightmap.txt'
        temperatureMapFileName = f'dumps/{int(fTime())}/temperature.txt'
        humidityMapFileName = f'dumps/{int(fTime())}/humidity.txt'

        with open(heightmapFileName, "w+", encoding='utf-8') as file:
            file.write(dumpedHeightmap)

        with open(temperatureMapFileName, "w+") as file:
            file.write(dumpedTemperatureMap)

        with open(humidityMapFileName, "w+") as file:
            file.write(dumpedHumidityMap)

    def IsTileOcean(self, position: tuple[int, int]):
        if not self.heightmap:
            print(
                "Cannot determine whether tile is ocean or not. Cause: Heightmap hasn't been created yet."
            )
            return None

        if self.heightmap[position[1]][position[0]] <= float(self.seaLevel):
            return True
        else:
            return False

    def GenerateHeightmap(self):
        self.heightmap = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.heightTiles = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]
        totalTilesGenerated = 0
        for y in range(self.height):
            for x in range(self.width):
                height = 0
                totalTilesGenerated += 1

                for perlin in self.perlins:
                    height += perlin.noise([x / 50, y / 50])

                self.heightmap[y][x] = height

                if height > self.mountainsLevel:
                    self.heightTiles[y][x] = 0

                elif height > self.hillsLevel:
                    self.heightTiles[y][x] = 1

                elif height > self.seaLevel:
                    self.heightTiles[y][x] = 2

                elif height > self.deepSeaLevel:
                    self.heightTiles[y][x] = 3

                else:
                    self.heightTiles[y][x] = 4

            if self.verboseLogging:
                print(f"Heightmap tiles generated: {totalTilesGenerated}")

        if self.verboseLogging:
            print("Successfully generated Heightmap!")

    def FindHighestPointInRange(self, position: tuple[int, int], radius: int):
        minX = position[0] - radius
        minY = position[1] - radius

        maxX = position[0] + radius
        maxY = position[1] + radius

        heights = []
        positions = []

        for y in range(self.height):
            for x in range(self.width):
                if minX < x < maxX and minY < y < maxY:
                    heights.append(
                        self.heightmap[y][x]
                    )
                    positions.append(
                        (x, y)
                    )

        maxHeight = max(heights)

        maxPosition = positions[
            heights.index(
                maxHeight
            )
        ]

        return maxPosition

    def GenerateTemperatureMap(self):
        self.temperatureMap = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]
        self.temperatureTiles = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]

        tempModel = []
        step = (4 / self.height)

        for temp in arange(-1.0, 1.0, step):
            tempModel.append(temp)

        for temp in arange(1.0, -1.0, -step):
            tempModel.append(temp)

        for y in range(self.height):
            for x in range(self.width):
                altitudeTemperatureOffset = self.heightmap[y][x] * 0.25
                temperature = tempModel[y]

                if not self.IsTileOcean((x, y)):
                    temperature -= altitudeTemperatureOffset

                self.temperatureMap[y][x] = temperature

                if temperature > self.hotLevel:
                    self.temperatureTiles[y][x] = 4

                elif temperature > self.warmLevel:
                    self.temperatureTiles[y][x] = 3

                elif temperature > self.temperateLevel:
                    self.temperatureTiles[y][x] = 0

                elif temperature > self.coldLevel:
                    self.temperatureTiles[y][x] = 2

                else:
                    self.temperatureTiles[y][x] = 1


    def GenerateHumidityMap(self):
        self.humidityMap = [
            [0 for _ in range(self.width)] for _ in range(self.height)
        ]
        totalTilesGenerated = 0
        for y in range(self.height):
            for x in range(self.width):
                totalTilesGenerated += 1
                a = self.humidityNoise.noise([x / self.width, y / self.height])
                self.humidityMap[y][x] = a

            if self.verboseLogging:
                print(f"HumidityMap tiles generated: {totalTilesGenerated}")

    def ShowMap(self, offset: tuple):
        self.isometricView.View(self.screen, offset)

        display.flip()

