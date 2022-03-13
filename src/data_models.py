from enum import Enum
from typing import List

from pydantic import BaseModel, validator

from src.constants import MAXTIME, MINTIME


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


class Timing(BaseModel):
    type: TypeChoices
    value: int

    @validator("value")
    def validate_value(cls, v: int) -> int:
        if MINTIME <= v <= MAXTIME:
            return v
        else:
            raise ValueError(
                f"Timestamp not in range. \
                    Should be between {MINTIME} and {MAXTIME}"
            )


class OpenHours(BaseModel):
    monday: List[Timing] = []
    tuesday: List[Timing] = []
    wednesday: List[Timing] = []
    thursday: List[Timing] = []
    friday: List[Timing] = []
    saturday: List[Timing] = []
    sunday: List[Timing] = []
