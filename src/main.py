from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI

import sys
from pathlib import Path

from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

from src.init import redis_manager

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import auth_router
from src.api.default import default_router
from src.api.hotels import hotels_router
from src.api.rooms import rooms_router
from src.api.booking import bookings_router
from src.api.facilities import facilities_router
from src.api.load import load_router


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa

    # старт приложения
    await redis_manager.connect()
    FastAPICache.init(RedisBackend(redis_manager.redis), prefix="fastapi-cache")

    yield

    # остановка приложения
    await redis_manager.close()


app = FastAPI(lifespan=lifespan)

app.include_router(default_router)
app.include_router(auth_router)
app.include_router(hotels_router)
app.include_router(rooms_router)
app.include_router(bookings_router)
app.include_router(facilities_router)
app.include_router(load_router)

if __name__ == "__main__":
    uvicorn.run("main:app", reload=True, port=8001)
