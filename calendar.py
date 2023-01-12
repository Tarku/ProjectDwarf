# Calendar.py

from utils import FPS
from math import log

MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]

class Season:
    '''
    The Season class for the game.\n
    Use the "se_" prefix for in-code variable identification.
    '''

    name: str
    temperatureOffset: float

    def __init__(self, c_name: str, c_temperatureOffset: float):
        self.name = c_name
        self.temperatureOffset = c_temperatureOffset


se_Winter = Season(
    "season.winter",
    -2.0
)

se_Spring = Season(
    "season.spring",
    -0.5
)

se_Summer = Season(
    "season.summer",
    1.0
)

se_Autumn = Season(
    "season.autumn",
    -1.0
)


class CalendarInfo:
    '''
    The CalendarInfo class for the game.\n
    Use the "cli_" prefix for in-code variable identification.
    '''

    ticksPerHour: float
    hoursPerDay: float
    daysPerMonth: float
    monthsPerYear: float

    seasonsLengthInMonths: float
    seasons: [Season]

    def __init__(self, c_ticksPerHour: float, c_hoursPerDay: float, c_daysPerMonth: float, c_monthsPerYear: float, c_seasons: [Season]):
        self.ticksPerHour = c_ticksPerHour
        self.hoursPerDay = c_hoursPerDay
        self.daysPerMonth = c_daysPerMonth
        self.monthsPerYear = c_monthsPerYear
        self.seasons = c_seasons
        self.seasonsLengthInMonths = self.monthsPerYear // len(c_seasons)


cli_DefaultInfo = CalendarInfo(
    c_ticksPerHour=20,
    c_hoursPerDay=24,
    c_daysPerMonth=30,
    c_monthsPerYear=12,
    c_seasons=[se_Winter, se_Spring, se_Summer, se_Autumn]
)

class Calendar:

    calendarInfo: CalendarInfo
    calendarTicks: int

    startingYear: int

    currentHour: int
    currentDay: int
    currentMonth: int
    currentYear: int

    currentSeason: Season
    seasonIndex: int

    def __init__(self, c_calendarInfo: CalendarInfo, c_startingYear: int = 0):
        self.calendarInfo = c_calendarInfo

        self.calendarTicks = 0
        self.startingYear = c_startingYear

        self.currentHour = 0
        self.currentDay = 0
        self.currentMonth = 0
        self.currentYear = self.startingYear

        self.seasonIndex = 0

    def Update(self):
        self.calendarTicks += 1

        if self.calendarTicks >= self.calendarInfo.ticksPerHour:
            self.calendarTicks = 0
            self.currentHour += 1

        if self.currentHour >= self.calendarInfo.hoursPerDay:
            self.currentHour = 0
            self.currentDay += 1

        if self.currentDay >= self.calendarInfo.daysPerMonth:
            self.currentDay = 0
            self.currentMonth += 1

        if self.currentMonth % self.calendarInfo.seasonsLengthInMonths == 0:
            self.seasonIndex += 1

            if self.seasonIndex >= len(self.calendarInfo.seasons) - 1:
                self.seasonIndex = 0

            self.currentSeason = self.calendarInfo.seasons[self.seasonIndex]

        if self.currentMonth >= self.calendarInfo.monthsPerYear:
            self.currentMonth = 0
            self.currentYear += 1

    def GetDateString(self):
        return f'{self.currentDay + 1} {MONTH_NAMES[self.currentMonth]}, Year {self.currentYear}'

    def GetHourString(self):
        return f'{self.currentHour}h'

    def GetFullString(self):
        return f'{self.currentHour}h; {self.currentDay + 1} {MONTH_NAMES[self.currentMonth]}, Year {self.currentYear}'



