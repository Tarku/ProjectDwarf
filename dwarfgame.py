# DwarfGame.py

import pygame
import sys

from time import perf_counter

from colors import *
from drawing.text import *
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
from calendar import *

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

    calendar: Calendar

    def __init__(self):
        pygame.init()

        pygame.display.set_icon(ICON_IMAGE)
        pygame.display.set_caption("Project Dwarf - Loading")

        pygame.mouse.set_cursor(CURSOR)

        # Open option files

        self.options = Options("options.txt")
        self.keybindings = Options("keybindings.txt")

        # Get parameters

        self.display = pygame.display.set_mode(DISPLAY_SIZE)

        self.currentLanguage = self.options.Get("language")
        self.localization = Localization(self.currentLanguage)

        self.loadingStringsIndex = 0

        self.ticks = 0

        self.paused = False

    def GetInScreenMiddle(self, size: Vector2) -> tuple:
        positionX = HALF_WIN_WIDTH - (size.x // 2)
        positionY = HALF_WIN_HEIGHT - (size.y // 2)
        return positionX, positionY

    def DisplayStartingText(self, color: (int, int, int) = WHITE):
        text = self.localization.Get(
            LOADING_SCREEN_STRINGS[self.loadingStringsIndex]
        )

        position = Vector2(HALF_WIN_WIDTH, HALF_WIN_HEIGHT)

        render = TITLE_FONT.render(
            text,
            FONT_ANTIALIASING,
            color
        )
        self.display.fill(BLACK)
        self.display.blit(
            render,
            (position.x - render.get_width() // 2, position.y - render.get_height() // 2)
        )

        pygame.display.flip()

    def DisplayFPSCount(self, color: (int, int, int), position: (int, int)):
        fpsCount = self.clock.get_fps()
        fpsCount = floor(fpsCount)

        fpsText = self.localization.Get("special.fps", (
            fpsCount
        ))

        DisplayText(fpsText, position, color)

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

        self.calendar = Calendar(cli_DefaultInfo)

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

        self.loadingStringsIndex += 1
        self.DisplayStartingText()

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

                print("Game ran during {} seconds.".format(round(self.ticks / FPS, 1)))

                pygame.quit()
                sys.exit()

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
        self.calendar.Update()

        pygame.display.set_caption(TITLE.format(int(self.clock.get_fps())))

        for member in self.colony.members:
            member.Update(self)

    def HandleScreen(self):
        loc = self.localization

        self.display.fill(DARK_VIOLET)

        self.currentScreen.SwitchTo(self)

        # self.DisplayFPSCount(YELLOW, (0, 0))

        if self.paused:

            text = DEFAULT_FONT.render(loc.Get("menu.paused"), FONT_ANTIALIASING, WHITE, BLACK)
            self.display.blit(text, (HALF_WIN_WIDTH - text.get_width() // 2, EDGE_PADDING))


    def Run(self):
        self.Load()

        self.running = True

        # Start of game loop

        while self.running:
            self.HandleScreen()
            self.HandleKeybinds()

            if not self.paused:
                self.HandleUpdates()
                self.ticks += 1

            pygame.display.flip()
            self.clock.tick(FPS)
