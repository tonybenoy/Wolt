from datetime import datetime
from functools import lru_cache
from typing import Dict, List, Tuple

from fastapi import HTTPException

from src.constants import MINTIME, TypeChoices


@lru_cache()
def get_time_from_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%I:%M %p")


def get_open_close_time(
    timings: List[Dict[str, int]],
    previously_left_open: bool = False,
) -> Tuple[List[str], bool]:
    response = []
    open_time = close_time = MINTIME
    closed = append_comma = False

    for timing in timings:
        if TypeChoices.open == timing["type"]:
            open_time = timing["value"]
            response.append(
                f"{', 'if append_comma else ''}"
                f"{get_time_from_timestamp(timing['value'])}"
            )
            append_comma = closed = False
        if TypeChoices.close == timing["type"]:
            close_time = timing["value"]
            response.append(f" - {get_time_from_timestamp(timing['value'])}")
            closed = True
            append_comma = False if previously_left_open else True
            if not previously_left_open:
                if close_time < open_time:
                    raise HTTPException(
                        status_code=422,
                        detail="Closing time cannot be less than opening time",
                    )
            previously_left_open = False
    return response, closed
