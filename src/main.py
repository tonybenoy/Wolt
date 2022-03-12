from typing import Dict

import arrow
from fastapi import FastAPI

app = FastAPI()


@app.get("/test")
async def test() -> Dict[str, str]:
    return {
        "result": "success",
        "message": f"It worked {arrow.now().humanize()}!",
    }
