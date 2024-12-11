from datetime import date

from fastapi import APIRouter, Query, Body
from fastapi_cache.decorator import cache

from src.api.dependencies import DBDep
from src.cache.cache_decorator import my_cache
from src.schemas.hotels import HotelPatch, PaginationDep, HotelAdd

hotels_router = APIRouter(prefix="/hotels", tags=["Отели"])


@hotels_router.get("")
@cache(expire=10)
async def get_hotels(
        pagination: PaginationDep,
        db: DBDep,
        title: str | None = Query(None, description="Название отеля"),
        location: str | None = Query(None, description="Расположение отеля"),
        date_from: date = Query(example="2024-12-01"),
        date_to: date = Query(example="2024-12-10"),
):
    limit = pagination.per_page or 1
    offset = limit * (pagination.page - 1)

    # return await db.hotels.get_all_hotels(title=title, location=location, limit=limit, offset=offset)
    return await db.hotels.get_hotels_by_date(
        date_from=date_from,
        date_to=date_to,
        title=title,
        location=location,
        limit=limit,
        offset=offset,
    )


@hotels_router.get("/{hotel_id}")
@cache(expire=10)
async def get_hotel(hotel_id: int, db: DBDep):
    return await db.hotels.get_one_or_none(id=hotel_id)


@hotels_router.post("")
async def create_hotel(
        db: DBDep,
        hotel_data: HotelAdd = Body(openapi_examples={
            "1": {
                "summary": "Madrid",
                "value": {
                    "title": "Мадрид",
                    "location": "madrid",
                }
            },
            "2": {
                "summary": "Barcelona",
                "value": {
                    "title": "Барселона",
                    "location": "barcelona",
                }
            }
        })
):
    hotel = await db.hotels.add(hotel_data)
    await db.commit()
    return {"status": "OK", "data": hotel}


@hotels_router.delete("/{hotel_id}")
async def delete_hotel(hotel_id: int, db: DBDep):
    await db.hotels.delete(id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@hotels_router.put("/{hotel_id}")
async def put_hotel(hotel_id: int, hotel_data: HotelAdd, db: DBDep):
    await db.hotels.edit(hotel_data, id=hotel_id)
    await db.commit()
    return {"status": "OK"}


@hotels_router.patch("/{hotel_id}")
async def patch_hotel(hotel_id: int, hotel_data: HotelPatch, db: DBDep):
    await db.hotels.edit(hotel_data, exclude_unset=True, id=hotel_id)
    await db.commit()
    return {"status": "OK"}
