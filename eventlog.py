# EventLog.py

from colors import *
from pygame.surface import Surface
from pygame.font import *
from pygame import Vector2, Rect
from utils import *

from drawing.text import *
from drawing.misc import *

class EventMode:
    PERIL = (RED, BLACK)
    POSITIVE = ((72, 147, 72), (17, 40, 17))
    INFO = (BLACK, LIGHT_GRAY)


class EventLogMessage:
    text: str
    mode: EventMode

    def __init__(self, c_text: str, c_formatArguments = None, c_mode: EventMode = EventMode.INFO):
        self.text = c_text
        self.formatArguments = c_formatArguments
        self.mode = c_mode


class EventLog:

    __log: [EventLogMessage] = []

    def __init__(self, game):
        self.game = game

    def __len__(self):
        return len(self.__log)

    def __getitem__(self, item):
        return self.game.localization.Get(self.__log[item].text, self.__log[item].formatArguments)

    def Add(self, text: str, formatArguments = None, mode: EventMode = EventMode.INFO):
        self.__log.insert(0, EventLogMessage(text, formatArguments, mode))

    def Show(self, game):
        loc = game.localization

        if not self.__log:
            return

        fontColor, backgroundColor = self.__log[0].mode
        text = self.__log[0].text

        arguments = self.__log[0].formatArguments

        if arguments is None:
            formattedText = loc.Get(text)
        else:
            formattedText = loc.Get(text, arguments)

        DisplayHorizontalLine(DARK_GRAY, 650, 3)
        DisplayHorizontalLine(DARK_GRAY, 650 + NORMAL_FONT_SIZE + (.25 * NORMAL_FONT_SIZE), 3)

        background = Surface(Vector2(WINDOW_WIDTH, NORMAL_FONT_SIZE + (.25 * NORMAL_FONT_SIZE)))
        background.fill(backgroundColor)

        game.display.blit(background, Rect(0, 650, NORMAL_FONT_SIZE + (.25 * NORMAL_FONT_SIZE), WINDOW_WIDTH))

        DisplayMiddleText(formattedText, 650, fontColor)
