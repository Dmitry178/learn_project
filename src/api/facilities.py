from fastapi import APIRouter
from fastapi_cache.decorator import cache

from src.dependencies import DBDep
from src.exceptions import ObjectAlreadyExistsException, FacilityExistsHTTP
from src.schemas.facilities import FacilityAdd
from src.services.facilities import FacilitiesService

facilities_router = APIRouter(prefix="/facilities", tags=["Удобства"])


@facilities_router.get("")
@cache(expire=10)
async def get_facilities(db: DBDep):
    """
    Получение всех удобств
    """

    return await FacilitiesService(db).get_facilities()


@facilities_router.post("")
async def post_facility(db: DBDep, facility_data: FacilityAdd):
    """
    Добавления нового удобства
    """

    try:
        facility = await FacilitiesService(db).post_facility(facility_data)
        return {"status": "OK", "data": facility}

    except ObjectAlreadyExistsException:
        raise FacilityExistsHTTP
