from datetime import datetime
from functools import lru_cache
from typing import Dict, List, Tuple

from src.data_models import TypeChoices


@lru_cache()
def datetime_to_timestamp(dt: datetime) -> int:
    return int(dt.timestamp())


def get_time_from_timestamp(timestamp: int) -> str:
    return datetime.fromtimestamp(timestamp).strftime("%I:%M %p")


def get_open_close_time(
    timings: List[Dict[str, int]], previously_left_open: bool = False
) -> Tuple[List[str], bool]:
    response = []
    closed = False
    append_comma = False
    for timing in timings:
        if TypeChoices.open == timing["type"]:
            response.append(
                f"{', 'if append_comma else ''}"
                f"{get_time_from_timestamp(timing['value'])}"
            )
            append_comma = closed = False
        if TypeChoices.close == timing["type"]:
            response.append(f" - {get_time_from_timestamp(timing['value'])}")
            closed = True
            append_comma = False if previously_left_open else True
            previously_left_open = False
    return response, closed
