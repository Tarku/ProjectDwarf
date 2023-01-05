# DwarfGame.py

import pygame

from time import perf_counter


# Clearly not the best coding practices I know but who cares

from colors import *
from material import *
from gameevent import *
from colony import *
from person import *
from faction import *
from workshop import *
from weapon import *
from localization import *
from options import *
from world import *
from utils import *
from parcel import *
from screen import *
from eventlog import EventLog
from naminglanguage import *

class DwarfGame:

    '''
    The DwarfGame class.\n
    The base class for the whole game.
    '''

    running: bool
    loading: bool

    clock: pygame.time.Clock
    displayText: pygame.Surface
    world: World
    parcel: Parcel
    colony: Colony
    faction: Faction
    currentScreen: Screen

    ticks: int

    eventLog: EventLog

    loadingStrings: list

    def __init__(self):
        pygame.init()

        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON_IMAGE)

        # Open option files

        self.options = Options("options.txt")
        self.keybindings = Options("keybindings.txt")

        # Get parameters

        self.displaySize = (
            self.options.Get("window_width"),
            self.options.Get("window_height")
        )

        self.display = pygame.display.set_mode(
            self.displaySize
        )

        self.loadingStrings = self.options.GetList("loading_strings", ",")

        self.normalFontSize = self.options.Get("normal_font_size")
        self.titleFontSize = self.options.Get("title_font_size")
        self.fontName = self.options.Get("font")

        self.currentLanguage = self.options.Get("language")
        self.localization = Localization(self.currentLanguage)

        self.font = pygame.font.SysFont("Arial", self.normalFontSize)
        self.titleFont = pygame.font.SysFont("Arial", bold=True, size=self.titleFontSize)
        self.pausedFont = pygame.font.SysFont("Arial", 50)

        self.loadingStringsIndex = 0

        self.ticks = 0

        self.paused = False

        self.isEnterKeyPressed = False
        self.isTKeyPressed = False

    def GetInScreenMiddle(self, size):
        positionX = (self.display.get_width() / 2) - (size[0] / 2)
        positionY = (self.display.get_height() / 2) - (size[1] / 2)
        return (
            positionX, positionY
        )

    def DisplayText(self, text: str, position: tuple, color: tuple):
        self.displayText = self.font.render(text, True, color)
        self.display.blit(self.displayText, position)

    def DisplayMiddleText(self, text: str, y: int, color: tuple):
        self.displayText = self.font.render(text, True, color)
        positionX = (self.display.get_width() / 2) - (self.displayText.get_width() / 2)
        positionY = y
        self.display.blit(self.displayText, (
            positionX,
            positionY
        ))

    def DisplayRightText(self, text: str, y: int, color: tuple):
        self.displayText = self.font.render(text, True, color)
        positionX = (self.display.get_width()) - (self.displayText.get_width())
        self.display.blit(self.displayText, (
            positionX,
            y
        ))

    def DisplayLeftText(self, text: str, y: int, color: tuple):
        self.displayText = self.font.render(text, True, color)
        self.display.blit(self.displayText, (
            0,
            y
        ))

    def DisplayScreenTitle(self, text: str, color: tuple):
        self.displayText = self.titleFont.render(text, True, color)
        positionX = (self.display.get_width() / 2) - (self.displayText.get_width() / 2)
        self.display.blit(self.displayText, (
            positionX,
            0
        ))

    def DisplayStartingText(self, color: (int, int, int) = WHITE, antialiasing: bool = True):
        text = self.localization.Get(
            self.loadingStrings[self.loadingStringsIndex]
        )

        position = (
            self.displaySize[0] / 2,
            self.displaySize[1] / 2
        )

        tmpFont = self.titleFont

        render = tmpFont.render(
            text,
            antialiasing,
            color
        )
        self.display.fill(BLACK)
        self.display.blit(
            render,
            (position[0] - render.get_width() / 2, position[1] - render.get_height() / 2)
        )

        pygame.display.flip()

    def DisplayFPSCount(self, color: (int, int, int), position: (int, int)):
        fpsCount = self.clock.get_fps()
        fpsCount = floor(fpsCount)

        fpsText = self.localization.Get("special.fps", (
            fpsCount
        ))

        self.DisplayText(fpsText, position, color)

    def DisplayHorizontalLine(self, color: tuple, yPosition: int, width: int = 2):
        horizontalLine = surface.Surface((self.display.get_width(), width))
        horizontalLine.fill(color)

        self.display.blit(horizontalLine, Vector2(0, yPosition - width / 2))

    def Load(self):
        self.loading = True
        loc = self.localization

        print("Loading game...")

        self.DisplayStartingText()

        self.clock = pygame.time.Clock()

        # Loading tileset

        # Menu stuff

        self.currentScreen = sc_Colony
        self.eventLog = EventLog(self)

        # Faction-related

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

        self.faction = Faction(name="New Arrivals")
        self.faction.Register()

        # Colony-related

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

        self.colony = Colony(name="New Town", faction=self.faction)
        self.colony.Register()

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

        self.colony.GiveHeadstart()

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

        self.colony.Populate(
            count=BASE_POPULATION,
            races=[rc_Dwarf, rc_Human, rc_Vampire, rc_HighElf],
            genders=[gd_Masculine, gd_Feminine],
            minAge=1,
            maxAge=120
        )

        # World Generation

        print("World generation...")

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

        start = perf_counter()

        self.world = World(self.display)

        self.world.GenerateHeightmap()
        self.world.GenerateTemperatureMap()
        self.world.GenerateHumidityMap()

        self.world.JoinTileInfo()

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

        self.parcel = Parcel(0.4, 0.2, 1)

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

        end = perf_counter()

        print(f"World generation done. Time spent : {end - start}s")

        for screen in all_screens:
            if isinstance(screen, SelectionScreen):
                screen.Load(self)

        self.loading = False

    def HandleCheatShortcuts(self, key):
        allUnits = self.colony.members

        match key:
            case pygame.K_KP4:
                if not self.colony.GetAliveUnits():
                    return

                randomUnit = choice(self.colony.GetAliveUnits())
                randomUnit.Die(self, "magic")

            case pygame.K_KP7:
                self.colony.Populate(1, [gd_Masculine, gd_Feminine], [rc_Dwarf, rc_Human, rc_HighElf, rc_Vampire])
                unitName = self.colony.members[-1].name

                self.eventLog.Add("event.debug_populate", unitName, EventMode.POSITIVE)

    def HandleKeybinds(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                self.currentScreen.CheckKeybind(self, event.key)
                self.HandleCheatShortcuts(event.key)

                if self.currentScreen.isParent:
                    self.currentScreen.CheckChildKeybinds(self, event.key)

                if type(self.currentScreen) is MapScreen:
                    self.currentScreen.CheckSpecialKeybinds(self, event.key)

                if isinstance(self.currentScreen, SelectionScreen):
                    self.currentScreen.CheckSpecialKeybinds(self, event.key)

                if event.key == pygame.K_SPACE:
                    if self.paused:
                        self.paused = False
                    else:
                        self.paused = True


    def HandleUpdates(self):
        self.colony.Update(self)

        for member in self.colony.members:
            member.Update(self)

    def HandleScreen(self):
        loc = self.localization

        self.currentScreen.SwitchTo(self)

        self.DisplayFPSCount(YELLOW, (0, 0))


        if self.paused:
            text = self.pausedFont.render(loc.Get("menu.paused"), True, WHITE, BLACK)
            self.display.blit(
                text,
                Vector2(
                    self.display.get_width() // 2 - text.get_width() // 2,
                    self.display.get_height() // 2 - text.get_height() // 2
                )
            )

        # Beginning of the horrible if-elif-elif-... to check what to show depending
        # on the currentScreen.

    def Run(self):
        self.Load()

        self.running = True

        # Start of game loop

        while self.running:
            # Background filling
            self.display.fill(DARK_VIOLET)

            self.HandleScreen()
            self.HandleKeybinds()

            if not self.paused:
                self.HandleUpdates()

                self.ticks += 1

            pygame.display.flip()

            self.clock.tick(FPS)

        print("Game ended in {} seconds.".format(
            round(self.ticks / FPS, 1)
        ))
