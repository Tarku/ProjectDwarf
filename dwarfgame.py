# DwarfGame.py

import pygame

from colors import *
from material import *
from gameevent import *
from colony import *
from person import *
from faction import *
from workshop import *
from weapon import *
from localization import *
from screentype import *
from options import *
from world import *
from time import perf_counter
from utils import *


ICON_IMAGE = pygame.image.load(
    "assets\\images\\icon.png"
)

TITLE = "Dwarf Game"


class DwarfGame:

    '''
    The DwarfGame class.\n
    The base class for the whole game.
    '''

    def __init__(self):
        self.options = Options("options.txt")
        self.keybindings = Options("keybindings.txt")

        self.displaySize = (
            self.options.Get("window_width"),
            self.options.Get("window_height")
        )

        pygame.init()

        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON_IMAGE)

        self.display = pygame.display.set_mode(
            self.displaySize
        )

        self.currentLanguage = self.options.Get("language")

        self.localization = Localization(self.currentLanguage)

        self.running = True
        self.clock = None

        self.fontName = self.options.Get("font")

        self.normalFontSize = self.options.Get("normal_font_size")
        self.titleFontSize = self.options.Get("title_font_size")

        self.font = pygame.font.SysFont(self.fontName, self.normalFontSize)
        self.titleFont = pygame.font.SysFont(self.fontName, self.titleFontSize)

        self.displayText = None
        self.eventLog = []

        self.currentScreen = Screen.COLONY

        self.fc_Faction = Faction("Newcomers")
        self.fc_AllyFaction = Faction()

        self.fc_AllyFaction.GenerateName(minLength=2, maxLength=3)

        print(self.fc_AllyFaction.name)

        self.col_Colony = Colony("New Colony", self.fc_Faction).Register()

        self.ps_Governor = Person("Governor James").Register()
        self.ps_Governor2 = Person("Governor Kol").Register()

        self.col_Colony.AddMember(self.ps_Governor)
        self.col_Colony.AddMember(self.ps_Governor2)

        self.ge_GovernorVisit = GameEvent("Governor Visit", {
            EventType.VISITOR: self.ps_Governor
        }, 1, 500)

        self.ge_namePrompt = GameEvent("Prompt", {
            EventType.COLONY_NAME_PROMPT: self.ps_Governor2
        })

        self.ge_A = GameEvent("A", {
            EventType.VISITOR_GIFT: {
                "Visitor": self.ps_Governor,
                "Item": mat_WOOD,
                "Count": 50
            }
        }, 50, 500)

        self.buildingSelectionIndex = 0
        self.buildingTaskSelectionIndex = 0
        self.unitSelectionIndex = 0
        self.eventSelectionIndex = 0
        self.itemSelectionIndex = 0

        self.isEnterKeyPressed = False
        self.isTKeyPressed = False

        self.mapCameraOffset = (0, 0)

        self.col_Colony.GiveHeadstart()

        print("World generation...")
        start = perf_counter()

        self.wld_World = World()

        self.wld_World.GenerateHeightmap()
        self.wld_World.GenerateTemperatureMap()
        self.wld_World.GenerateHumidityMap()

        self.wld_World.DumpToFile()
        end = perf_counter()

        print(f"World generation done. Time spent : {end - start}s")

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
         positionY = y
         self.display.blit(self.displayText, (
             positionX,
             positionY
         ))

    def DisplayLeftText(self, text: str, y: int, color: tuple):
         self.displayText = self.font.render(text, True, color)
         positionX = 0
         positionY = y
         self.display.blit(self.displayText, (
             positionX,
             positionY
         ))

    def DisplayScreenTitle(self, text: str, color: tuple):
        self.displayText = self.titleFont.render(text, True, color)
        positionX = (self.display.get_width() / 2) - (self.displayText.get_width() / 2)
        positionY = 0
        self.display.blit(self.displayText, (
            positionX,
            positionY
        ))

    def Run(self):
        self.clock = pygame.time.Clock()
        loc = self.localization # Shorthand

        while self.running:

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_e:
                        self.currentScreen = Screen.EVENTS

                    elif event.key == pygame.K_c:
                        self.currentScreen = Screen.COLONY

                    elif event.key == pygame.K_m and self.currentScreen is not Screen.MAP:
                        self.currentScreen = Screen.MAP

                    elif event.key == pygame.K_ESCAPE and self.currentScreen is Screen.MAP:
                        self.currentScreen = Screen.COLONY

                    elif event.key == pygame.K_u:
                        self.currentScreen = Screen.UNITS

                    elif event.key == pygame.K_i:
                        self.currentScreen = Screen.INVENTORY

                    elif event.key == pygame.K_t and self.currentScreen is Screen.BUILDINGS:
                        self.currentScreen = Screen.BUILDING_TASKS

                    elif event.key == pygame.K_RETURN and self.currentScreen is Screen.BUILDINGS:
                        self.currentScreen = Screen.BUILDING_MENU

                    elif event.key == pygame.K_RETURN and self.currentScreen is Screen.BUILDING_MENU:
                        all_building_tasks [
                            self.buildingTaskSelectionIndex
                        ].TryAt(self.col_Colony)

                    elif event.key == pygame.K_b:
                        self.currentScreen = Screen.BUILDINGS

                    elif event.key == pygame.K_d:
                        self.currentScreen = Screen.DESIGNATIONS

                    elif event.key == pygame.K_ESCAPE:
                        if self.currentScreen is Screen.BUILDING_TASKS:
                            self.currentScreen = Screen.BUILDINGS

                        elif self.currentScreen is Screen.BUILDING_MENU:
                            self.currentScreen = Screen.BUILDINGS

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
                                self.mapCameraOffset[1] + (
                                        self.display.get_height() / TILES_PER_SCREEN
                                )
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
                                self.mapCameraOffset[1] - (
                                        self.display.get_height() / TILES_PER_SCREEN
                                )
                            )
                    elif event.key == pygame.K_LEFT:
                        if self.currentScreen is Screen.MAP:
                            self.mapCameraOffset = (
                                self.mapCameraOffset[0] + (
                                        self.display.get_width() / TILES_PER_SCREEN
                                ),
                                self.mapCameraOffset[1]
                            )
                    elif event.key == pygame.K_RIGHT:
                        if self.currentScreen is Screen.MAP:
                            self.mapCameraOffset = (
                                self.mapCameraOffset[0] - (
                                        self.display.get_width() / TILES_PER_SCREEN
                                ),
                                self.mapCameraOffset[1]
                            )
                    else:
                        pass

            self.display.fill(DARK_BLUE)

            if self.currentScreen is not Screen.MAP:
                self.DisplayText(loc.Get("keyguide.colony"), (0, 425), WHITE)
                self.DisplayText(loc.Get("keyguide.buildings"), (0, 450), LIGHT_GRAY)
                self.DisplayText(loc.Get("keyguide.inventory"), (0, 475), WHITE)
                self.DisplayText(loc.Get("keyguide.events"), (0, 500), LIGHT_GRAY)
                self.DisplayText(loc.Get("keyguide.units"), (0, 525), WHITE)
                self.DisplayText(loc.Get("keyguide.designations"), (0, 550), LIGHT_GRAY)
                self.DisplayText(loc.Get("keyguide.map"), (0, 575), WHITE)

            if self.currentScreen == Screen.COLONY:

                self.DisplayScreenTitle(loc.Get("title.colony"), YELLOW)

                self.DisplayMiddleText(loc.Get("colony.model", (self.col_Colony.name, self.col_Colony.faction.name)), 100, LIGHT_GRAY)
                self.DisplayMiddleText(loc.Get("colony.population", len(self.col_Colony.members)), 150, LIGHT_GRAY)

            elif self.currentScreen == Screen.MAP:

                self.wld_World.ShowMap(self.display, self.mapCameraOffset)

            elif self.currentScreen == Screen.EVENTS:

                self.DisplayScreenTitle(loc.Get("title.events"), YELLOW)

                eventQuantity = len(
                    self.eventLog
                )

                if self.eventSelectionIndex == eventQuantity:
                    self.eventSelectionIndex = 0

                if self.eventSelectionIndex < 0:
                    self.eventSelectionIndex = eventQuantity - 1

                if eventQuantity == 0:
                    eventText = loc.Get("menu.empty")
                else:
                    eventText = loc.Get("selection.event", (self.eventSelectionIndex + 1, eventQuantity, self.eventLog[self.eventSelectionIndex]))

                    # self.DisplayRightText(f"Select: <Enter>", 500, YELLOW)

                    self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                    self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

                self.DisplayMiddleText(
                    eventText,
                    250,
                    WHITE
                )

            elif self.currentScreen == Screen.DESIGNATIONS:

                self.DisplayScreenTitle(loc.Get("title.designations"), YELLOW)

            elif self.currentScreen == Screen.INVENTORY:

                self.DisplayScreenTitle(loc.Get("title.inventory"), YELLOW)

                itemQuantity = len(
                    self.col_Colony.inventory.keys()
                )

                if self.itemSelectionIndex > itemQuantity - 1:
                    self.itemSelectionIndex = 0

                if self.itemSelectionIndex < 0:
                    self.itemSelectionIndex = itemQuantity - 1

                self.DisplayScreenTitle(loc.Get("title.inventory"), YELLOW)

                self.DisplayMiddleText(
                    loc.Get("colony.inventory", itemQuantity), 200, WHITE)

                if itemQuantity is 0:
                    itemText = loc.Get("menu.empty")
                else:
                    itemText = loc.Get("selection.inventory", (
                        self.itemSelectionIndex + 1,
                        itemQuantity,
                        loc.Get(
                            list(
                                self.col_Colony.inventory.items()
                            )[self.itemSelectionIndex][0].name
                        ),
                        list(
                            self.col_Colony.inventory.items()
                        )[self.itemSelectionIndex][1]
                    ))

                    self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                    self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

                self.DisplayMiddleText(
                    itemText,
                    250,
                    YELLOW
                )

            elif self.currentScreen == Screen.BUILDINGS:

                buildingQuantity = len(
                    self.col_Colony.buildings
                )

                if self.buildingSelectionIndex > buildingQuantity - 1:
                    self.buildingSelectionIndex = 0

                if self.buildingSelectionIndex < 0:
                    self.buildingSelectionIndex = buildingQuantity - 1

                buildingText = ""

                self.DisplayScreenTitle(loc.Get("title.buildings"), YELLOW)

                self.DisplayMiddleText(
                     loc.Get("colony.buildings", buildingQuantity), 200, WHITE)

                if buildingQuantity is 0:
                    buildingText = loc.Get("menu.empty")
                else:
                    buildingText = loc.Get("selection.building", (
                        self.buildingSelectionIndex + 1,
                        buildingQuantity,
                        loc.Get(
                            self.col_Colony.buildings[self.buildingSelectionIndex].name
                        )
                    ))

                    self.DisplayRightText(loc.Get("keyguide.tasks"), 500, YELLOW)

                    self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                    self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

                self.DisplayMiddleText(
                    buildingText,
                    250,
                    WHITE
                )

                self.DisplayRightText(loc.Get("keyguide.buildingmenu"), 475, WHITE)

            elif self.currentScreen == Screen.BUILDING_TASKS:
                self.DisplayScreenTitle(
                    loc.Get("title.buildings_tasks", loc.Get(self.col_Colony.buildings[self.buildingSelectionIndex].name)),
                    YELLOW
                )

                self.DisplayMiddleText(
                    loc.Get("building.activetasks", (
                        loc.Get(self.col_Colony.buildings[self.buildingSelectionIndex].name),
                        len(
                            self.col_Colony.buildings[self.buildingSelectionIndex].activeTasks
                        )
                    )), 250, WHITE
                )

            elif self.currentScreen is Screen.BUILDING_MENU:

                self.DisplayScreenTitle(loc.Get("title.building_menu"), YELLOW)

                taskQuantity = len(
                    all_building_tasks
                )
                task = None

                if self.buildingTaskSelectionIndex == taskQuantity:
                    self.buildingTaskSelectionIndex = 0

                if self.buildingTaskSelectionIndex < 0:
                    self.buildingTaskSelectionIndex = taskQuantity - 1

                if taskQuantity is 0:
                    taskText = loc.Get("menu.empty")
                else:
                    task = all_building_tasks[self.buildingTaskSelectionIndex]
                    taskText = loc.Get("selection.task", (
                        self.buildingTaskSelectionIndex + 1,
                        taskQuantity,
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

                unitsQuantity = len(
                    self.col_Colony.members
                )

                if self.unitSelectionIndex == unitsQuantity:
                    self.unitSelectionIndex = 0

                if self.unitSelectionIndex < 0:
                    self.unitSelectionIndex = unitsQuantity - 1

                if unitsQuantity is 0:
                    unitText = loc.Get("empty")
                else:
                    unitText = loc.Get("selection.unit", (self.unitSelectionIndex + 1, unitsQuantity, self.col_Colony.members[self.unitSelectionIndex].name))

                    self.DisplayRightText(loc.Get("menu.select"), 500, YELLOW)

                    self.DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
                    self.DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

                self.DisplayMiddleText(
                    unitText,
                    250,
                    WHITE
                )

            pygame.display.flip()

            self.clock.tick(60)
