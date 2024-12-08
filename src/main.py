import asyncio
import multiprocessing
import subprocess

import uvicorn
import sys

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend
from pathlib import Path

from src.tasks.asyncio_tasks import run_send_email_regularly

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import auth_router
from src.api.booking import bookings_router
from src.api.default import default_router
from src.api.facilities import facilities_router
from src.api.hotels import hotels_router
from src.api.images import images_router
from src.api.load import load_router
from src.api.rooms import rooms_router
from src.init import redis_manager


@asynccontextmanager
async def lifespan(app: FastAPI):  # noqa

    # старт приложения
    # asyncio.create_task(run_send_email_regularly())  # noqa
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
app.include_router(images_router)
app.include_router(load_router)


def run_uvicorn():
    uvicorn.run("main:app", host="0.0.0.0", port=8001, reload=True)


def run_celery():
    command = ["celery", "--app=src.tasks.celery_app:celery_instance", "worker", "-l", "INFO", "-B"]
    subprocess.run(command)


if __name__ == "__main__":
    uvicorn_process = multiprocessing.Process(target=run_uvicorn)
    # celery_process = multiprocessing.Process(target=run_celery)

    uvicorn_process.start()
    # celery_process.start()

    uvicorn_process.join()
    # celery_process.join()
