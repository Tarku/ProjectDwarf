# DwarfGame.py

import pygame
import multiprocessing as mpc

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

    eventLog: list
    itemSelectionIndices: dict

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

        self.normalFontSize = self.options.Get("normal_font_size")
        self.titleFontSize = self.options.Get("title_font_size")
        self.fontName = self.options.Get("font")
        self.currentLanguage = self.options.Get("language")

        self.localization = Localization(self.currentLanguage)

        self.font = pygame.font.SysFont(self.fontName, self.normalFontSize)
        self.titleFont = pygame.font.SysFont(self.fontName, self.titleFontSize, bold=True)

        self.buildingSelectionIndex = 0
        self.buildingTaskSelectionIndex = 0
        self.workshopTaskSelectionIndex = 0
        self.unitSelectionIndex = 0
        self.eventSelectionIndex = 0
        self.itemSelectionIndex = 0
        self.ticks = 0

        self.isEnterKeyPressed = False
        self.isTKeyPressed = False

        self.mapCameraOffset = (0, 0)

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

    def DisplayStartingText(self, backgroundColor: (int, int, int), fontName: str, text: str, fontSize: int, position: (int, int), color: (int, int, int), antialiasing: bool = False, bold: bool = False, italic: bool = False):

        tmpFont = pygame.font.SysFont(
            name=fontName,
            size=fontSize,
            bold=bold,
            italic=italic
        )
        render = tmpFont.render(
            text,
            antialiasing,
            color
        )
        self.display.fill(backgroundColor)
        self.display.blit(
            render,
            (position[0] - render.get_width() / 2, position[1] - render.get_height() / 2)
        )

        pygame.display.flip()

    def Load(self):
        self.loading = True
        loc = self.localization

        print("Loading game...")

        self.DisplayStartingText(
            BLACK,
            self.fontName,
            loc.Get("loading.game"),
            32,
            (
                self.displaySize[0] / 2,
                self.displaySize[1] / 2
            ),
            WHITE,
            bold=True,
            antialiasing=True
        )

        self.clock = pygame.time.Clock()

        # Menu stuff

        self.currentScreen = Screen.COLONY
        self.eventLog = list()

        # Faction-related

        self.DisplayStartingText(BLACK, self.fontName, loc.Get("loading.faction"), 24, (
            self.displaySize[0] / 2, self.displaySize[1] / 2
        ), WHITE, bold=True, antialiasing=True)

        self.faction = Faction(name="New Arrivals")
        self.faction.Register()

        self.DisplayStartingText(BLACK, self.fontName, loc.Get("loading.colony"), 24, (
            self.displaySize[0] / 2, self.displaySize[1] / 2
        ), WHITE, bold=True, antialiasing=True)
        # Colony-related

        self.colony = Colony(name="New Town", faction=self.faction)
        self.colony.Register()

        self.DisplayStartingText(BLACK, self.fontName, loc.Get("loading.giving_headstart"), 24, (
            self.displaySize[0] / 2, self.displaySize[1] / 2
        ), WHITE, bold=True, antialiasing=True)

        self.colony.GiveHeadstart()

        self.DisplayStartingText(BLACK, self.fontName, loc.Get("loading.populate_colony"), 24, (
            self.displaySize[0] / 2, self.displaySize[1] / 2
        ), WHITE, bold=True, antialiasing=True)

        self.colony.Populate(
            count=15,
            races=[rc_Dwarf, rc_Human],
            genders=[gd_Masculine, gd_Feminine],
            minAge=1,
            maxAge=120
        )

        # World Generation

        print("World generation...")

        self.DisplayStartingText(BLACK, self.fontName, loc.Get("loading.worldgen"), 24, (
            self.displaySize[0] / 2, self.displaySize[1] / 2
        ), WHITE, bold=True, antialiasing=True)

        start = perf_counter()

        self.world = World()

        self.world.GenerateHeightmap()
        self.world.GenerateTemperatureMap()
        self.world.GenerateHumidityMap()

        end = perf_counter()

        self.DisplayStartingText(BLACK, self.fontName, loc.Get("loading.parcel"), 24, (
            self.displaySize[0] / 2, self.displaySize[1] / 2
        ), WHITE, bold=True, antialiasing=True)

        self.parcel = Parcel(0.4, 0.2, 1)

        self.DisplayStartingText(BLACK, self.fontName, loc.Get("loading.done"), 24, (
            self.displaySize[0] / 2, self.displaySize[1] / 2
        ), WHITE, bold=True, antialiasing=True)

        print(f"World generation done. Time spent : {end - start}s")

        self.loading = False

    def HandleKeybinds(self):

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.currentScreen = Screen.EVENTS

                elif event.key == pygame.K_c:
                    self.currentScreen = Screen.COLONY

                elif event.key == pygame.K_m:
                    if self.currentScreen is not Screen.MAP:
                        self.currentScreen = Screen.MAP

                elif event.key == pygame.K_u:
                    self.currentScreen = Screen.UNITS

                elif event.key == pygame.K_i:
                    self.currentScreen = Screen.INVENTORY

                elif event.key == pygame.K_t:
                    if self.currentScreen is Screen.BUILDINGS and self.colony.buildings:
                        self.currentScreen = Screen.BUILDING_TASKS

                elif event.key == pygame.K_RETURN:
                    if self.currentScreen is Screen.BUILDINGS:
                        self.currentScreen = Screen.BUILDING_MENU

                    elif self.currentScreen is Screen.BUILDING_MENU:
                        all_building_tasks[
                            self.buildingTaskSelectionIndex
                        ].TryAt(self.colony)

                    elif self.currentScreen is Screen.UNITS:
                        self.currentScreen = Screen.UNIT_PRESENTATION

                elif event.key == pygame.K_b:
                    self.currentScreen = Screen.BUILDINGS

                elif event.key == pygame.K_d:
                    self.currentScreen = Screen.DESIGNATIONS

                elif event.key == pygame.K_ESCAPE:
                    if self.currentScreen is Screen.BUILDING_TASKS:
                        self.currentScreen = Screen.BUILDINGS

                    elif self.currentScreen is Screen.BUILDING_MENU:
                        self.currentScreen = Screen.BUILDINGS

                    elif self.currentScreen is Screen.UNIT_PRESENTATION:
                        self.currentScreen = Screen.UNITS

                    else:
                        self.currentScreen = Screen.COLONY

                elif event.key == pygame.K_UP:
                    if self.currentScreen is Screen.BUILDINGS:
                        self.buildingSelectionIndex -= 1

                    elif self.currentScreen is Screen.BUILDING_MENU:
                        self.buildingTaskSelectionIndex -= 1

                    elif self.currentScreen is Screen.UNITS:
                        self.unitSelectionIndex -= 1

                    elif self.currentScreen is Screen.EVENTS:
                        self.eventSelectionIndex -= 1

                    elif self.currentScreen is Screen.INVENTORY:
                        self.itemSelectionIndex -= 1

                    elif self.currentScreen is Screen.MAP:
                        self.mapCameraOffset = (
                            self.mapCameraOffset[0],
                            self.mapCameraOffset[1] + MAP_SCROLL_AMOUNT
                        )

                elif event.key == pygame.K_DOWN:
                    if self.currentScreen is Screen.BUILDINGS:
                        self.buildingSelectionIndex += 1

                    elif self.currentScreen is Screen.BUILDING_MENU:
                        self.buildingTaskSelectionIndex += 1

                    elif self.currentScreen is Screen.UNITS:
                        self.unitSelectionIndex += 1

                    elif self.currentScreen is Screen.EVENTS:
                        self.eventSelectionIndex += 1

                    elif self.currentScreen is Screen.INVENTORY:
                        self.itemSelectionIndex += 1

                    elif self.currentScreen is Screen.MAP:
                        self.mapCameraOffset = (
                            self.mapCameraOffset[0],
                            self.mapCameraOffset[1] - MAP_SCROLL_AMOUNT
                        )

                elif event.key == pygame.K_LEFT:
                    if self.currentScreen is Screen.MAP:
                        self.mapCameraOffset = (
                            self.mapCameraOffset[0] + MAP_SCROLL_AMOUNT,
                            self.mapCameraOffset[1]
                        )
                elif event.key == pygame.K_RIGHT:
                    if self.currentScreen is Screen.MAP:
                        self.mapCameraOffset = (
                            self.mapCameraOffset[0] - MAP_SCROLL_AMOUNT,
                            self.mapCameraOffset[1]
                        )
                else:
                    pass

    def HandleScreen(self):
        loc = self.localization

        # Beginning of the horrible if-elif-elif-... to check what to show depending
        # on the currentScreen.

        if self.currentScreen == Screen.COLONY:

            self.DisplayScreenTitle(loc.Get("title.colony"), YELLOW)

            self.DisplayMiddleText(loc.Get("colony.model", (self.colony.name, self.colony.faction.name)), 100,
                                   LIGHT_GRAY)
            self.DisplayMiddleText(loc.Get("colony.population", len(self.colony.members)), 150, LIGHT_GRAY)

        elif self.currentScreen == Screen.MAP:

            self.world.ShowMap(self.display, self.mapCameraOffset)

        elif self.currentScreen == Screen.EVENTS:

            self.DisplayScreenTitle(loc.Get("title.events"), YELLOW)

        elif self.currentScreen == Screen.DESIGNATIONS:

            self.DisplayScreenTitle(loc.Get("title.designations"), YELLOW)

        elif self.currentScreen == Screen.INVENTORY:

            self.DisplayScreenTitle(loc.Get("title.inventory"), YELLOW)

            quantity = len(
                self.colony.inventory.keys()
            )

            self.itemSelectionIndex = LoopValue(self.itemSelectionIndex, 0, quantity)

            self.DisplayMiddleText(
                loc.Get("colony.inventory", quantity), 200, WHITE)

            if quantity == 0:
                text = loc.Get("menu.empty")
            else:
                text = loc.Get("selection.inventory", (
                    self.itemSelectionIndex + 1,
                    quantity,
                    loc.Get(
                        list(
                            self.colony.inventory.items()
                        )[self.itemSelectionIndex][0].name
                    ),
                    list(
                        self.colony.inventory.items()
                    )[self.itemSelectionIndex][1]
                ))

                self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

            self.DisplayMiddleText(
                text,
                250,
                YELLOW
            )

        elif self.currentScreen == Screen.BUILDINGS:
            self.DisplayScreenTitle(loc.Get("title.buildings"), YELLOW)

            quantity = len(self.colony.buildings)

            self.DisplayMiddleText(
                loc.Get("colony.buildings", quantity), 200, WHITE)

            self.buildingSelectionIndex = LoopValue(self.buildingSelectionIndex, 0, quantity)

            if quantity == 0:
                text = loc.Get("menu.empty")
            else:
                text = loc.Get("selection.building", (
                    self.buildingSelectionIndex + 1,
                    quantity,
                    loc.Get(
                        self.colony.buildings[self.buildingSelectionIndex].name
                    )
                ))

                self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

            self.DisplayMiddleText(text, 250, YELLOW)

            self.DisplayRightText(loc.Get("keyguide.buildingmenu"), 475, WHITE)

        elif self.currentScreen == Screen.BUILDING_TASKS:
            if not self.colony.buildings:
                self.DisplayMiddleText("Nothing to show there", 250, RED)
            else:

                self.DisplayScreenTitle(
                    loc.Get("title.buildings_tasks", loc.Get(self.colony.buildings[self.buildingSelectionIndex].name)),
                    YELLOW
                )

                self.DisplayMiddleText(
                    loc.Get("building.activetasks", (
                        loc.Get(self.colony.buildings[self.buildingSelectionIndex].name),
                        len(
                            self.colony.buildings[self.buildingSelectionIndex].activeTasks
                        )
                    )), 150, WHITE
                )

        elif self.currentScreen is Screen.BUILDING_MENU:

            self.DisplayScreenTitle(loc.Get("title.building_menu"), YELLOW)

            quantity = len(
                all_building_tasks
            )
            task = None

            self.buildingTaskSelectionIndex = LoopValue(self.buildingTaskSelectionIndex, 0, quantity)

            if quantity == 0:
                taskText = loc.Get("menu.empty")
            else:
                task = all_building_tasks[self.buildingTaskSelectionIndex]
                taskText = loc.Get("selection.task", (
                    self.buildingTaskSelectionIndex + 1,
                    quantity,
                    loc.Get(
                        task.name
                    )
                ))

                taskRequiredItems = task.RequiredItemsString()
                localizedTaskRequiredItems = []

                for taskRequiredItem in taskRequiredItems:
                    split = taskRequiredItem.split(" ")
                    localizationString = split[0]
                    count = split[1]
                    localizedTaskRequiredItems.append(
                        f"{loc.Get(localizationString)} {count}"
                    )

                self.DisplayMiddleText(loc.Get("task.cost", (
                    ", ".join(localizedTaskRequiredItems)
                )), 275, YELLOW)

                self.DisplayRightText(loc.Get("menu.select"), 500, YELLOW)

                self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

            self.DisplayMiddleText(
                taskText,
                250,
                WHITE
            )

            self.DisplayRightText(
                loc.Get("keyguide.escape"),
                475,
                WHITE
            )

        elif self.currentScreen is Screen.UNITS:

            self.DisplayScreenTitle(loc.Get("title.units"), YELLOW)

            quantity = len(
                self.colony.members
            )

            self.unitSelectionIndex = LoopValue(self.unitSelectionIndex, 0, quantity)

            if quantity == 0:
                text = loc.Get("menu.empty")
            else:
                text = loc.Get(
                    "selection.unit",
                    (
                        self.unitSelectionIndex + 1,
                        quantity,
                        self.colony.members[self.unitSelectionIndex].name,
                        loc.Get(

                            self.colony.members[self.unitSelectionIndex].GetAgeName()
                        ),
                        loc.Get(
                            self.colony.members[self.unitSelectionIndex].race.name
                        ),
                        self.colony.members[self.unitSelectionIndex].gender.symbol
                    )
                )

                self.DisplayRightText(loc.Get("menu.select"), 500, YELLOW)

                self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

            self.DisplayMiddleText(
                text,
                250,
                WHITE
            )

        elif self.currentScreen == Screen.UNIT_PRESENTATION:

            unit: Person
            if not self.colony.members:
                self.DisplayMiddleText(
                    loc.Get("menu.empty"),
                    250,
                    WHITE
                )
            else:

                unit = self.colony.members[
                    self.unitSelectionIndex
                ]

                self.DisplayScreenTitle(loc.Get("title.unit_presentation", unit.name), YELLOW)

                personality = loc.Get(
                    unit.GetPersonalityString()
                )

                # Shorthands (again, it's for my sanity)

                subj = loc.Get(
                    unit.pronoun.subject
                )
                obj = loc.Get(
                    unit.pronoun.object
                )
                refl = loc.Get(
                    unit.pronoun.reflexive
                )
                poss = loc.Get(
                    unit.pronoun.possessive
                )
                possPron = loc.Get(
                    unit.pronoun.possessivePronoun
                )

                self.DisplayMiddleText(
                    loc.Get(
                        "unit.presentation",
                        (
                            subj,
                            personality,
                            subj,
                            unit.age
                        ),
                    ),
                    250,
                    WHITE
                )

        if self.currentScreen is not Screen.MAP:

            self.DisplayText(loc.Get("keyguide.colony"), (0, 425), WHITE)
            self.DisplayText(loc.Get("keyguide.buildings"), (0, 450), LIGHT_GRAY)
            self.DisplayText(loc.Get("keyguide.inventory"), (0, 475), WHITE)
            self.DisplayText(loc.Get("keyguide.events"), (0, 500), LIGHT_GRAY)
            self.DisplayText(loc.Get("keyguide.units"), (0, 525), WHITE)
            self.DisplayText(loc.Get("keyguide.designations"), (0, 550), LIGHT_GRAY)
            self.DisplayText(loc.Get("keyguide.map"), (0, 575), WHITE)

    def Run(self):
        self.Load()

        self.running = True

        # Start of game loop

        while self.running:
            # Background filling
            self.display.fill(DARK_BLUE)

            self.HandleKeybinds()
            self.HandleScreen()

            self.ticks += 1

            pygame.display.flip()

            self.clock.tick(60)
