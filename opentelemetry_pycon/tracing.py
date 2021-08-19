import datetime
import random

import fastapi
import httpx
import redis


FASTAPI_ROUTER: fastapi.APIRouter = fastapi.APIRouter()
RESPONSES: list[str] = ["Привет", "Привет!"]


@FASTAPI_ROUTER.post("/hello/")
async def hello() -> dict:
    """Go to `/responses/random/` endpoint."""
    async with httpx.AsyncClient() as async_client:
        response: httpx.Response = await async_client.post("http://localhost:9999/responses/random/")
        return {'hello': response.json()['response']}


@FASTAPI_ROUTER.post("/responses/random/")
def random_response() -> dict:
    """Return random response from predefined list."""
    response_text: str = random.choice(RESPONSES)
    redis_client: redis.Redis = redis.Redis(host='redis', port=6379, db=0)
    redis_client.hset('responses', datetime.datetime.now().isoformat(), response_text)
    return {'response': response_text}
