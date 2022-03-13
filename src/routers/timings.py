from fastapi import APIRouter, HTTPException
from fastapi.responses import PlainTextResponse

from src.constants import Days, Tags, TypeChoices
from src.data_models import OpenHours
from src.main import get_logger
from src.utils import get_open_close_time

logger = get_logger(__name__)

router: APIRouter = APIRouter(tags=[Tags.timings])


@router.post(
    "/humanize-open-hours/",
    response_class=PlainTextResponse,
)
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
                    response[-1] + f"{previous_open_time}{closed_at}"
                )
                previous_open_time = None
            if not closed:
                previous_open_time = times.pop()
                logger.info(
                    f"restaurant opened at {previous_open_time} on"
                    + " {Days[day].value} but not closed"
                )
            time = "".join(times)
            response.append(f"{Days[day].value} : {time}")
    return "\n".join(response)
