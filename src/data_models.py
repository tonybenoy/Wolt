from typing import List

from fastapi import HTTPException
from pydantic import BaseModel, validator

from src.constants import MAXTIME, MINTIME, TypeChoices


class Timing(BaseModel):
    type: TypeChoices
    value: int

    @validator("value")
    def validate_value(cls, v: int) -> int:
        if MINTIME <= v <= MAXTIME:
            return v
        else:
            raise HTTPException(
                status_code=422,
                detail=(
                    f"Timestamp not in range. Should be"
                    f" between {MINTIME} and {MAXTIME}"
                ),
            )


class OpenHours(BaseModel):
    monday: List[Timing] = []
    tuesday: List[Timing] = []
    wednesday: List[Timing] = []
    thursday: List[Timing] = []
    friday: List[Timing] = []
    saturday: List[Timing] = []
    sunday: List[Timing] = []
