import asyncio
import time

from fastapi import APIRouter
from starlette.responses import RedirectResponse

load_router = APIRouter(tags=["Нагрузочное тестирование"])


@load_router.get("/", summary="Редирект на Swagger UI")
def redirect():
    return RedirectResponse("/docs")


@load_router.get("/sync/{id}")
def sync_func(id: int):
    # print(f"sync. Потоков: {threading.active_count()}")
    print(f"sync. Начал {id}: {time.time():.2f}")
    time.sleep(3)
    print(f"sync. Закончил {id}: {time.time():.2f}")


@load_router.get("/async/{id}")
async def async_func(id: int):
    # print(f"async. Потоков: {threading.active_count()}")
    # print(f"async. Начал {id}: {time.time():.2f}")
    await asyncio.sleep(3)
    # print(f"async. Закончил {id}: {time.time():.2f}")
    return {'success': True}
