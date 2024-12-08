from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd
from src.tasks.tasks import test_task

facilities_router = APIRouter(prefix="/facilities", tags=["Удобства"])


@facilities_router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    """
    Получение всех удобств
    """

    return await db.facilities.get_all()

    # facilities_from_cache = await redis_manager.get("facilities")
    #
    # if not facilities_from_cache:
    #     print("Чтение из базы данных")
    #     facilities = await db.facilities.get_all()
    #     facilities_schemas: list[dict] = [f.model_dump() for f in facilities]
    #     facilities_json = json.dumps(facilities_schemas)
    #     await redis_manager.set("facilities", facilities_json, 10)
    #     return facilities
    #
    # else:
    #     facilities_dicts = json.loads(facilities_from_cache)
    #     return facilities_dicts


@facilities_router.post("")
async def post_facility(db: DBDep, facility_data: FacilityAdd):
    """
    Добавления нового удобства
    """

    facility = await db.facilities.add(facility_data)
    await db.commit()

    test_task.delay()

    return {"status": "OK", "data": facility}
