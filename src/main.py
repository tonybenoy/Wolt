from typing import Dict

from fastapi import FastAPI

from src.constants import Tags
from src.logging import get_logger
from src.routers import timings

app = FastAPI()

app.include_router(router=timings.router)
logger = get_logger(
    __name__,
)


@app.get("/test", tags=[Tags.test])
async def test() -> Dict[str, str]:
    return {
        "result": "success",
        "msg": "It works!",
    }
