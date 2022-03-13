from enum import Enum


class TypeChoices(Enum):
    open = "open"
    close = "close"


class Days(Enum):
    monday = "Monday"
    tuesday = "Tuesday"
    wednesday = "Wednesday"
    thursday = "Thursday"
    friday = "Friday"
    saturday = "Saturday"
    sunday = "Sunday"


MINTIME = 1
MAXTIME = 86400


class Tags(Enum):
    timings = "Timings"
    test = "Test"
