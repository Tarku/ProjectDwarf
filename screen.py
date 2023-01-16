# Screen.py
import pygame

from colors import *
from drawing.misc import DisplayHorizontalLine, DisplayBackground
from utils import *
from collections.abc import Sized
from task import *
from workshop import Workshop
from drawing.text import *


all_screens = []
all_parent_screens = {}

class Prompt:
    title: str
    string: str
    padding: int

    def __init__(self, game, c_title: str = "", c_padding: int = 10):
        self.title = c_title
        self.game = game

        self.string = ""
        self.padding = c_padding


    def GetString(self):
        return self.string

    def Draw(self, event):
        titleLen = len(self.string) * NORMAL_FONT_SIZE
        x = HALF_WIN_WIDTH - titleLen // 2
        y = HALF_WIN_HEIGHT - NORMAL_FONT_SIZE // 2
        height = self.padding * 2 + NORMAL_FONT_SIZE
        width = self.padding * 2 + titleLen

        backgroundRectangle = pygame.surface.Surface((width, height))
        backgroundRectangle.fill(BLACK)

        pygame.display.get_surface().blit(backgroundRectangle, (x, y))

        DisplayMiddleText(self.string, y, WHITE)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.string = self.string[:-1]
            else:
                self.string += event.unicode


            
        

class Screen:
    '''
    The Screen class for the game.\n
    Use the "sc_" prefix for in-code variable identification.
    '''

    name: str
    title: str
    doesShowTitle: bool
    hasKeyguides: bool
    keybind: int
    parentScreen: 'Screen, None'
    isParent: bool
    runFunction: str

    def __init__(self, name: str, keybind: int, parentScreen: 'Screen, None' = None, isParent: bool = False, doesShowTitle: bool = True, hasKeyguides: bool = True, runFunction: str = None):
        self.name = name
        self.title = f"title.{name}"
        self.doesShowTitle = doesShowTitle
        self.hasKeyguides = hasKeyguides
        self.keybind = keybind
        self.parentScreen = parentScreen
        self.isParent = isParent
        self.runFunction = runFunction

        if isParent:
            all_parent_screens[self] = list()

        if parentScreen is not None:
            all_parent_screens[self.parentScreen].append(self)

    def SwitchTo(self, game):
        game.currentScreen = self

        loc = game.localization

        if self.runFunction is not None:
            eval(self.runFunction)

        if self.doesShowTitle:
            DisplayScreenTitle(
                loc.Get(self.title),
                YELLOW
            )

        self.ShowKeyguides(game)

    def CheckKeybind(self, game, eventKey: int):
        if eventKey == self.keybind:
            self.SwitchTo(game)
        elif eventKey == Keys.ESCAPE:
            if self.parentScreen is not None:
                self.parentScreen.SwitchTo(game)

    def ShowKeyguides(self, game):
        loc = game.localization
        if self.hasKeyguides:
            DisplayLeftText(loc.Get("keyguide.buildings"), 450, GRAY)
            DisplayLeftText(loc.Get("keyguide.inventory"), 475, WHITE)
            DisplayLeftText(loc.Get("keyguide.events"), 500, GRAY)
            DisplayLeftText(loc.Get("keyguide.units"), 525, WHITE)
            DisplayLeftText(loc.Get("keyguide.designations"), 550, GRAY)
            DisplayLeftText(loc.Get("keyguide.map"), 575, WHITE)

    def CheckChildKeybinds(self, game, eventKey: int):
        if not self.isParent:
            print(
                f"Cannot check Screen <{self.name}>'s Childs' Keybinds. Cause: Screen <{self.name}> is not a parent"
            )
            return

        if self not in all_parent_screens:
            print(
                f"Cannot check Screen <{self.name}>'s Childs' Keybinds. Cause: Screen is somehow not in "
                f"all_parent_screens. "
            )
            return

        for child in all_parent_screens[self]:
            child.CheckKeybind(game, eventKey)

        return True

    def CheckSpecialKeybinds(self, game, eventKey: int):
        pass

class ColonyScreen(Screen):
    def __init__(self, keybind: int):
        Screen.__init__(
            self,
            name="colony",
            keybind=keybind,
            parentScreen=None,
            isParent=True,
            doesShowTitle=False,
            hasKeyguides=True
        )

    def SwitchTo(self, game):
        Screen.SwitchTo(self, game)

        loc = game.localization

        DisplayBackground(DARK_GRAY, EDGE_PADDING, 25, 255)

        DisplayRightText(game.calendar.GetDateString(), EDGE_PADDING, WHITE)

        DisplayLeftText(game.calendar.GetHourString(), EDGE_PADDING, WHITE)

        DisplayLeftText(
            loc.Get(
                "colony.wealth",
                (
                    game.colony.GetWealth()
                )
            ),
            50,
            YELLOW
        )

        DisplayRightText(
            loc.Get(
                "colony.idlers",
                (
                    game.colony.GetIdlerNumber()
                )
            ),
            50,
            YELLOW
        )

        DisplayRightText(
            loc.Get(
                "colony.in_bed",
                (
                    game.colony.GetAsleepNumber()
                )
            ),
            75,
            ORANGE
        )

        DisplayMiddleText(
            loc.Get(
                "colony.population",
                (
                    game.colony.GetPopulation()
                )
            ),
            50,
            GREEN
        )

        DisplayMiddleText(
            loc.Get(
                "colony.mood",
                (
                    game.colony.GetMin("mood"),
                    game.colony.GetMedian("mood"),
                    game.colony.GetMax("mood"),
                    game.colony.immigrationMoodNeeded
                )
            ),
            200,
            GRAY
        )

        DisplayMiddleText(
            loc.Get(
                "colony.food_level",
                (
                    game.colony.GetMin("foodLevel"),
                    game.colony.GetMedian("foodLevel"),
                    game.colony.GetMax("foodLevel")
                )
            ),
            250,
            WHITE
        )

        DisplayMiddleText(
            loc.Get(
                "colony.sleep",
                (
                    game.colony.GetMin("sleep"),
                    game.colony.GetMedian("sleep"),
                    game.colony.GetMax("sleep")
                )
            ),
            300,
            GRAY
        )

        game.eventLog.Show(game)


class MapScreen(Screen):
    mapOffset: (int, int)

    def __init__(self, keybind: int, parentScreen: 'Screen, None' = None, isParent: bool = False):
        Screen.__init__(
            self,
            name="map",
            keybind=keybind,
            parentScreen=parentScreen,
            isParent=isParent,
            doesShowTitle=False,
            hasKeyguides=False
        )
        self.mapOffset = (0, 0)

    def SwitchTo(self, game):
        Screen.SwitchTo(self, game)
        game.world.ShowMap(self.mapOffset)

        x, y = self.mapOffset

        DisplayMiddleText("X: {}".format(x), 50, YELLOW)
        DisplayMiddleText("Y: {}".format(y), 75, YELLOW)

        DisplayMiddleText("X: {}".format(x + TILES_PER_SCREEN), 500, YELLOW)
        DisplayMiddleText("Y: {}".format(y + TILES_PER_SCREEN), 525, YELLOW)

    def CheckSpecialKeybinds(self, game, eventKey: int):
        x, y = self.mapOffset

        match eventKey:
            case Keys.UP_ARROW:
                self.mapOffset = (x, y - MAP_SCROLL_AMOUNT)
            case Keys.DOWN_ARROW:
                self.mapOffset = (x, y + MAP_SCROLL_AMOUNT)
            case Keys.LEFT_ARROW:
                self.mapOffset = (x - MAP_SCROLL_AMOUNT, y)
            case Keys.RIGHT_ARROW:
                self.mapOffset = (x + MAP_SCROLL_AMOUNT, y)

        self.mapOffset = (
            ClampValue(self.mapOffset[0], 0, game.world.width - TILES_PER_SCREEN),
            ClampValue(self.mapOffset[1], 0, game.world.height - TILES_PER_SCREEN)
        )


class SelectionScreen(Screen):
    name: str
    title: str
    doesShowTitle: bool
    iterableString: str
    iterable: Sized
    iterableLength: int

    color: [int, int, int]

    localizationStringArguments: str
    selectionIndex: int

    parentScreen: 'Screen, None'

    def __init__(self, name: str, keybind: int, color: [int, int, int], iterableString: str, localizationStringArguments: str, parentScreen: 'Screen, None' = None, isParent: bool = False):
        Screen.__init__(
            self,
            name=name,
            keybind=keybind,
            parentScreen=parentScreen,
            isParent=isParent,
            doesShowTitle=True,
            hasKeyguides=True
        )

        self.parentScreen = parentScreen
        self.iterableString = iterableString
        self.selectionIndex = 0
        self.localizationStringArguments = localizationStringArguments
        self.color = color


    def SwitchTo(self, game):
        text: str = "menu.empty"

        Screen.SwitchTo(self, game)

        evalString = self.iterableString
        selectionString = f"selection.{self.name}"

        self.iterable = eval(evalString, {"main": game, "colony": game.colony, "world": game.world,
                                          "building_tasks": all_building_tasks})

        if type(self.iterable) is dict:
            self.iterable = list(
                self.iterable.items()
            )

        self.iterableLength = len(
            self.iterable
        )
        arguments = [self.selectionIndex + 1, self.iterableLength]

        if not self.iterable:
            text = game.localization.Get(
                "menu.empty"
            )
        else:
            otherArguments = list(
                map(
                    lambda arg: eval(arg, {"object": self.iterable[self.selectionIndex], "L": game.localization.Get}),
                    self.localizationStringArguments.split(",")
                )
            )

            arguments.extend(
                otherArguments
            )
            argumentsTuple = tuple(arguments)

            text = game.localization.Get(
                selectionString,
                argumentsTuple
            )

            DisplayRightText(game.localization.Get("menu.previous"), 425, YELLOW)
            DisplayRightText(game.localization.Get("menu.next"), 450, YELLOW)

        DisplayMiddleText(
            text,
            250,
            self.color
        )

    def CheckSpecialKeybinds(self, game, eventKey: int):
        match eventKey:
            case Keys.UP_ARROW:
                self.selectionIndex -= 1
            case Keys.DOWN_ARROW:
                self.selectionIndex += 1
            case Keys.PAGE_UP:
                self.selectionIndex -= 5
            case Keys.PAGE_DOWN:
                self.selectionIndex += 5

        self.selectionIndex = LoopValue(self.selectionIndex, 0, self.iterableLength)

class InventoryScreen(SelectionScreen):
    selectionIndex: int
    iterableLength: int
    iterable: Sized

    def __init__(self):
        SelectionScreen.__init__(self, name="inventory", keybind=pygame.K_i, color=YELLOW, iterableString="", localizationStringArguments="", parentScreen=sc_Colony, isParent=False)

        self.selectionIndex = 0

    def SwitchTo(self, game):
        Screen.SwitchTo(self, game)
        loc = game.localization

        self.iterable = list(game.colony.inventory.items())
        self.iterableLength = len(self.iterable)

        text = loc.Get("menu.empty")

        if self.iterableLength > 0:
            self.selectionIndex = LoopValue(self.selectionIndex, 0, self.iterableLength)
            item, count = self.iterable[self.selectionIndex]

            if isinstance(item, CorpseItem):
                arguments = (
                    self.selectionIndex + 1,
                    self.iterableLength,
                    loc.Get("corpseitem.corpse", (
                        item.owner.name,
                        loc.Get(item.owner.GetAgeName()),
                        loc.Get(item.owner.race.adjective)
                    )),
                    count
                )
            else:
                arguments = (
                    self.selectionIndex + 1,
                    self.iterableLength,
                    loc.Get(item.name),
                    count
                )

            text = loc.Get("selection.inventory", arguments)

            DisplayRightText(loc.Get("menu.previous"), 425, YELLOW)
            DisplayRightText(loc.Get("menu.next"), 450, YELLOW)

        DisplayMiddleText(
            text,
            250,
            YELLOW
        )

    def CheckSpecialKeybinds(self, game, eventKey: int):
        SelectionScreen.CheckSpecialKeybinds(self, game, eventKey)


class BuildingMenuScreen(SelectionScreen):
    name: str
    title: str
    doesShowTitle: bool
    iterableString: str
    iterable: 'list, dict'
    iterableLength: int

    color: [int, int, int]

    localizationStringArguments: str
    selectionIndex: int
    actionKeybind: int

    def __init__(self, keybind: int, color: [int, int, int], iterableString: str,
                 localizationStringArguments: str,
                 parentScreen: 'Screen, None' = None,
                 isParent: bool = False,
                 actionKeybind: int = Keys.ENTER):
        SelectionScreen.__init__(
            self,
            name="building_menu",
            keybind=keybind,
            parentScreen=parentScreen,
            color=color,
            iterableString=iterableString,
            localizationStringArguments=localizationStringArguments,
            isParent=isParent
        )

        self.isParent = isParent
        self.parentScreen = parentScreen

        self.iterableString = iterableString
        self.selectionIndex = 0
        self.localizationStringArguments = localizationStringArguments
        self.color = color
        self.actionKeybind = actionKeybind

    def SwitchTo(self, game):
        text: str = "menu.empty"

        Screen.SwitchTo(self, game)

        evalString = self.iterableString

        self.iterable = eval(evalString, {"main": game, "colony": game.colony, "world": game.world,
                                          "building_tasks": all_building_tasks})
        self.iterableLength = len(
            self.iterable
        )

        if type(self.iterable) is dict:
            self.iterable = list(
                self.iterable.items()
            )

        task = self.iterable[self.selectionIndex]

        arguments = [self.selectionIndex + 1, self.iterableLength]

        if not self.iterable:
            text = game.localization.Get(
                "menu.empty"
            )
        else:
            otherArguments = list(
                map(
                    lambda arg: eval(arg, {"object": self.iterable[self.selectionIndex], "L": game.localization.Get}),
                    self.localizationStringArguments.split(",")
                )
            )

            taskResult = list(
                task.results.values()
            )[0]

            count = game.colony.buildings.count(taskResult)

            otherArguments.extend([count])

            arguments.extend(
                otherArguments
            )
            argumentsTuple = tuple(arguments)

            text = game.localization.Get(
                "selection.building_menu",
                argumentsTuple
            )

            DisplayRightText(game.localization.Get("menu.previous"), 425, YELLOW)
            DisplayRightText(game.localization.Get("menu.next"), 450, YELLOW)

        taskRequiredItems = task.RequiredItemsString()
        localizedTaskRequiredItems = []

        for taskRequiredItem in taskRequiredItems:
            split = taskRequiredItem.split(" ")
            localizationString = split[0]
            count = split[1]
            localizedTaskRequiredItems.append(
                f"{game.localization.Get(localizationString)} {count}"
            )

        DisplayMiddleText(
            text,
            250,
            self.color
        )

        DisplayMiddleText(game.localization.Get("task.cost", (
            ", ".join(localizedTaskRequiredItems)
        )), 275, YELLOW)

        DisplayRightText(game.localization.Get("menu.select"), 500, YELLOW)

        DisplayRightText(game.localization.Get("menu.previous"), 425, YELLOW)
        DisplayRightText(game.localization.Get("menu.next"), 450, YELLOW)

    def CheckSpecialKeybinds(self, game, eventKey: int):
        SelectionScreen.CheckSpecialKeybinds(self, game, eventKey)

        if eventKey == self.actionKeybind:
            all_building_tasks[self.selectionIndex].TryAt(game.colony)

class BuildingTasksScreen(Screen):
    def __init__(self, keybind: int):
        Screen.__init__(
            self,
            name="building_tasks",
            keybind=keybind,
            parentScreen=sc_Buildings,
            doesShowTitle=True,
            hasKeyguides=True
        )

    def SwitchTo(self, game):
        Screen.SwitchTo(self, game)
        buildings = game.colony.buildings
        selectionIndex = sc_Buildings.selectionIndex

        currentBuilding = buildings[selectionIndex]

        if isinstance(currentBuilding, Workshop):
            availableTasks = currentBuilding.tasks
            activeTasks = currentBuilding.activeTasks

            DisplayMiddleText(game.localization.Get())






class UnitsScreen(SelectionScreen):
    name: str
    title: str
    doesShowTitle: bool
    iterableString: str
    iterable: Sized
    iterableLength: int
    isParent: bool
    parentScreen: 'Screen, None'

    color: [int, int, int]

    localizationStringArguments: str
    selectionIndex: int
    actionKeybind: int

    def __init__(self, keybind: int, color: [int, int, int],
                 localizationStringArguments: str,
                 parentScreen: 'Screen, None' = None,
                 isParent: bool = False,
                 actionKeybind: int = Keys.ENTER):
        SelectionScreen.__init__(
            self,
            name="units",
            keybind=keybind,
            parentScreen=parentScreen,
            color=color,
            iterableString="colony.members",
            localizationStringArguments=localizationStringArguments,
            isParent=isParent
        )

        self.selectionIndex = 0
        self.localizationStringArguments = localizationStringArguments
        self.color = color
        self.isParent = isParent
        self.parentScreen = parentScreen
        self.actionKeybind = actionKeybind

    def SwitchTo(self, game):
        text: str = game.localization.Get("menu.empty")

        Screen.SwitchTo(self, game)

        evalString = self.iterableString
        selectionString = f"selection.units"

        self.iterable = eval(evalString, {"main": game, "colony": game.colony, "world": game.world,
                                          "building_tasks": all_building_tasks})
        self.iterableLength = len(
            self.iterable
        )

        if type(self.iterable) is dict:
            self.iterable = list(
                self.iterable.items()
            )

        arguments = [self.selectionIndex + 1, self.iterableLength]

        if self.iterable:
            if self.iterable[self.selectionIndex].isAlive is False:
                return

            otherArguments = list(
                map(
                    lambda arg: eval(arg,
                                     {"object": self.iterable[self.selectionIndex], "L": game.localization.Get}),
                    self.localizationStringArguments.split(",")
                )
            )

            arguments.extend(
                otherArguments
            )
            argumentsTuple = tuple(arguments)

            text = game.localization.Get(
                selectionString,
                argumentsTuple
            )

            DisplayRightText(game.localization.Get("menu.previous"), 425, YELLOW)
            DisplayRightText(game.localization.Get("menu.next"), 450, YELLOW)

        DisplayMiddleText(
            text,
            250,
            self.color
        )



    def CheckSpecialKeybinds(self, game, eventKey: int):
        SelectionScreen.CheckSpecialKeybinds(self, game, eventKey)


class UnitsPresentationScreen(Screen):
    name: str
    title: str
    doesShowTitle: bool
    mapOffset: (int, int)
    parentScreen: 'Screen, None'

    def __init__(self, keybind: int, parentScreen: 'Screen, None' = None, isParent: bool = False):
        Screen.__init__(
            self,
            name="unit_presentation",
            keybind=keybind,
            parentScreen=parentScreen,
            isParent=isParent,
            doesShowTitle=True,
            hasKeyguides=True
        )
        self.mapOffset = (0, 0)
        self.parentScreen = parentScreen

    def SwitchTo(self, game):
        game.currentScreen = self

        loc = game.localization

        text = "menu.empty"

        if self.runFunction is not None:
            eval(self.runFunction)

        if game.colony.members:

            unit: Person = game.colony.members[
                self.parentScreen.selectionIndex
            ]

            if self.doesShowTitle:
                DisplayScreenTitle(
                    loc.Get(self.title, unit.name),
                    YELLOW
                )

            DisplayScreenTitle(loc.Get("title.unit_presentation", unit.name), YELLOW)

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

            DisplayLeftText(
                loc.Get(
                    "unit.food_level",
                    (
                        round(unit.foodLevel, 1)
                    )
                ),
                50,
                ORANGE
            )

            DisplayMiddleText(
                loc.Get(
                    "unit.hydration",
                    (
                        round(unit.hydration, 1)
                    )
                ),
                50,
                CYAN
            )

            DisplayRightText(
                loc.Get(
                    "unit.sleep",
                    (
                        round(unit.sleep, 1)
                    )
                ),
                50,
                PURPLE
            )

            DisplayMiddleText(
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

        self.ShowKeyguides(game)

    def CheckKeybind(self, game, eventKey: int):
        Screen.CheckKeybind(self, game, eventKey)

class EventLogScreen(Screen):
    selectionIndex: int = 0
    eventAmount: int

    def __init__(self, keybind: int):
        Screen.__init__(self, name="event_log", keybind=keybind, isParent=False, doesShowTitle=True, parentScreen=sc_Colony)
        
    def SwitchTo(self, game):
        Screen.SwitchTo(self, game)

        self.eventAmount = len(game.eventLog)
        menuText = game.localization.Get("menu.empty")

        if game.eventLog:
            menuText = game.localization.Get(
                "selection.events",
                (
                    self.selectionIndex + 1,
                    self.eventAmount,
                    game.eventLog[self.selectionIndex]
                )
            )
            menuColor = game.eventLog.log[self.selectionIndex].mode[0]

            DisplayMiddleText(menuText, 250, menuColor)

        else:
            DisplayMiddleText(menuText, 250, WHITE)

    def CheckSpecialKeybinds(self, game, eventKey: int):
        match eventKey:
            case Keys.MENU_PREV:
                self.eventAmount -= 1
            case Keys.MENU_NEXT:
                self.eventAmount += 1

        self.selectionIndex = LoopValue(self.selectionIndex, 0, self.eventAmount)

class FactionScreen(Screen):
    selectionIndex: int = 0
    factionAmount: int

    def __init__(self, keybind: int, parentScreen: Screen):
        Screen.__init__(self, name="faction_screen", keybind=keybind, isParent=True, doesShowTitle=True, parentScreen=parentScreen)

    def SwitchTo(self, game):
        Screen.SwitchTo(self, game)

        self.factionAmount = len(all_factions)
        menuText = game.localization.Get("menu.empty")

        if all_factions:
            selectedFaction = all_factions[self.selectionIndex]

            if selectedFaction == game.faction:
                menuText = game.localization.Get("selection.own_faction", (self.selectionIndex + 1, self.factionAmount, selectedFaction.name))
            else:
                menuText = game.localization.Get("selection.faction", (self.selectionIndex + 1, self.factionAmount, selectedFaction.name))


        DisplayMiddleText(menuText, 250, WHITE)

    def CheckSpecialKeybinds(self, game, eventKey: int):
        match eventKey:
            case Keys.MENU_PREV:
                self.selectionIndex -= 1
            case Keys.MENU_NEXT:
                self.selectionIndex += 1

        self.selectionIndex = LoopValue(self.selectionIndex, 0, self.factionAmount)

class FactionPresentationScreen(Screen):
    def __init__(self, keybind: int):
        Screen.__init__(self, name="faction_presentation", keybind=keybind, parentScreen=sc_Factions, isParent=False, doesShowTitle=False)

    def SwitchTo(self, game):
        Screen.SwitchTo(self, game)

        selectedFaction = all_factions[sc_Factions.selectionIndex]

        DisplayScreenTitle(selectedFaction.name, YELLOW)

        DisplayMiddleText(game.localization.Get("factionmenu.leader", selectedFaction.leader.name), 150, WHITE)


sc_Colony = ColonyScreen(pygame.K_c)

sc_Events = EventLogScreen(
    keybind=pygame.K_e
)
sc_Inventory = InventoryScreen()

sc_Factions = FactionScreen(
    keybind=pygame.K_f,
    parentScreen=sc_Colony
)

sc_FactionPresentationMenu = FactionPresentationScreen(
    keybind=pygame.K_RETURN
)

sc_Units = UnitsScreen(
    keybind=pygame.K_u,
    color=WHITE,
    localizationStringArguments="object.name,L(object.GetAgeName()),L(object.race.name),object.GetGenderSymbol()",
    parentScreen=sc_Colony,
    isParent=True
)

sc_UnitsPresentation = UnitsPresentationScreen(
    keybind=Keys.ENTER,
    parentScreen=sc_Units,
    isParent=False
)

sc_Buildings = SelectionScreen(
    name="buildings",
    keybind=pygame.K_b,
    iterableString="colony.buildings",
    color=WHITE,
    localizationStringArguments="L(object.name)",
    parentScreen=sc_Colony,
    isParent=True
)

'''sc_BuildingsTasks = SelectionScreen(
    name="building_tasks",
    keybind=pygame.K_t,
    iterableString="colony.buildings"
)'''

sc_BuildingMenu = BuildingMenuScreen(
    keybind=pygame.K_o,
    iterableString="building_tasks",
    color=WHITE,
    localizationStringArguments="L(object.name)",
    parentScreen=sc_Buildings,
    isParent=False,
    actionKeybind=Keys.ENTER
)

sc_Map = MapScreen(pygame.K_m, sc_Colony)

