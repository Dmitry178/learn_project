from fastapi import APIRouter

from src.api.dependencies import DBDep
from src.schemas.facilities import FacilityAdd

facilities_router = APIRouter(prefix="/facilities", tags=["Удобства"])


@facilities_router.get("")
async def get_facilities(db: DBDep):
    """
    Получение всех удобств
    """

    return await db.facilities.get_all()


@facilities_router.post("")
async def post_facility(db: DBDep, facility_data: FacilityAdd):
    """
    Добавления нового удобства
    """

    facility = await db.facilities.add(facility_data)
    await db.commit()
    return {"status": "OK", "data": facility}
