import logging
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.responses import PlainTextResponse

from src.data_models import Days, OpenHours, TypeChoices
from src.utils import get_open_close_time

app = FastAPI()


def get_logger(name, level=logging.DEBUG) -> logging.Logger:
    FORMAT = "[%(levelname)s  %(name)s %(module)s:%(lineno)s - %(funcName)s() -\
         %(asctime)s]\n\t %(message)s \n"
    TIME_FORMAT = "%d.%m.%Y %I:%M:%S %p"

    logging.basicConfig(format=FORMAT, datefmt=TIME_FORMAT, level=level)

    logger = logging.getLogger(name)
    return logger


logger = get_logger(__name__)


@app.get("/test")
async def test() -> Dict[str, str]:
    return {
        "result": "success",
        "msg": "It works!",
    }


@app.post("/humanize-open-hours/", response_class=PlainTextResponse)
async def humanize_open_hours(open_hours: OpenHours) -> str:
    days = open_hours.dict()
    response = []
    previous_open_time = None
    for day, timing in days.items():
        if not timing:
            response.append(f"{Days[day].value} : Closed")
        else:
            times, closed = get_open_close_time(
                timings=timing,
                previously_left_open=True if previous_open_time else False,
            )
            if previous_open_time:
                if timing[0]["type"] != TypeChoices.close:
                    raise HTTPException(
                        status_code=422, detail="Closing time not available"
                    )
                closed_at = times.pop(0)
                response[-1] = (
                    response[-1]
                    + f"{previous_open_time}\
                    {closed_at}"
                )
                previous_open_time = None
            if not closed:
                previous_open_time = times.pop()
                logger.info(
                    f"restaurant opened at {previous_open_time}\
                         on {Days[day].value} but not closed"
                )
            time = "".join(times)
            response.append(f"{Days[day].value} : {time}")
    return "\n".join(response)
