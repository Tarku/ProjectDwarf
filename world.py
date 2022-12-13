# World.py


from perlin_noise import PerlinNoise
from time import time as fTime, perf_counter
from numpy import arange
from os import mkdir
from pygame.surface import Surface
from options import Options
from pygame import image, display, sprite, transform
from random import choice
from enum import Enum
from utils import *
from itertools import chain

class World:

    '''
    The World class for the game.\n
    Use the "wld_" prefix for in-code variable identification.
    '''

    heightmap : list
    temperatureMap : list
    humidityMap : list

    def __init__(self, seed: int = fTime()):
        self.seed = seed

        self.worldgenOptions = Options(
            "worldgen.txt"
        )

        self.tileSet = image.load(
            "assets\\images\\map_tileset.png"
        ).convert_alpha()

        # Height related
        self.mountainsLevel = self.worldgenOptions.Get("mountains_level")
        self.hillsLevel = self.worldgenOptions.Get("hills_level")
        self.lowHillsLevel = self.worldgenOptions.Get("low_hills_level")
        self.seaLevel = self.worldgenOptions.Get("sea_level")

        # Temperature related
        self.hotLevel = self.worldgenOptions.Get("hot_level")
        self.warmLevel = self.worldgenOptions.Get("warm_level")
        self.temperateLevel = self.worldgenOptions.Get("temperate_level")
        self.coldLevel = self.worldgenOptions.Get("cold_level")
        self.freezingLevel = self.worldgenOptions.Get("freezing_level")

        self.width = self.worldgenOptions.Get("width")
        self.height = self.worldgenOptions.Get("height")

        self.worldDump = self.worldgenOptions.GetBool("dump_world")
        self.verboseLogging = self.worldgenOptions.GetBool("verbose_logging")

        self.size = (
            self.width,
            self.height
        )

        self.octaves = self.worldgenOptions.Get("octaves")

        self.perlins = [PerlinNoise(seed=seed, octaves=self.octaves / i) for i in range(1, 4)]
        self.humidityNoise = PerlinNoise(seed=seed, octaves = 12)

    def DumpToFile(self):
        if not self.worldDump:
            return

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
        totalTilesGenerated = 0
        for y in range(self.height):
            for x in range(self.width):
                a = 0
                totalTilesGenerated += 1
                for perlin in self.perlins:
                    a += perlin.noise([x / 100, y / 100])
                self.heightmap[y][x] = a

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

        tempModel = []
        step = (4 / self.height)

        for temp in arange(-1.0, 1.0, step):
            tempModel.append(temp)

        for temp in arange(1.0, -1.0, -step):
            tempModel.append(temp)

        for y in range(self.height):
            for x in range(self.width):
                altitudeTemperatureOffset = self.heightmap[y][x] * 0.25

                if self.IsTileOcean((x, y)):
                    self.temperatureMap[y][x] = tempModel[y]
                else:
                    self.temperatureMap[y][x] = tempModel[y] - altitudeTemperatureOffset

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

    def ShowMap(self, screen: Surface, offset: tuple):
        tileGroup = sprite.Group()

        for y in range(self.height):
            for x in range(self.width):

                if self.heightmap[y][x] > float(self.mountainsLevel) * 1.8:
                    tileX = 0
                elif self.heightmap[y][x] > float(self.hillsLevel):
                    tileX = 1
                elif self.heightmap[y][x] > float(self.lowHillsLevel) * 0.7:
                    tileX = 2
                elif self.heightmap[y][x] > float(self.seaLevel):
                    tileX = 3
                else:
                    tileX = 4

                if self.temperatureMap[y][x] > float(self.hotLevel):
                    tileY = 4
                elif self.temperatureMap[y][x] > float(self.warmLevel):
                    tileY = 3
                elif self.temperatureMap[y][x] > float(self.temperateLevel):
                    tileY = 2
                elif self.temperatureMap[y][x] > float(self.coldLevel):
                    tileY = 1
                else:
                    tileY = 0

                separateTile = self.tileSet.subsurface(
                        [tileX * 8, tileY * 8, 8, 8]
                    )

                tileSprite = sprite.Sprite()
                ratio = screen.get_width() / TILES_PER_SCREEN

                tileSprite.image = transform.scale(
                    separateTile,
                    (
                        ratio,
                        ratio
                    )
                )
                screenX = x * ratio + offset[0]
                screenY = y * ratio + offset[1]

                tileSprite.rect = [screenX, screenY, ratio, ratio]

                if -ratio < screenX < screen.get_width() and -ratio < screenY < screen.get_height():
                    tileGroup.add(tileSprite)

        tileGroup.draw(screen)

        display.flip()

